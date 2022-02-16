#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/14 16:21
# @File    : main.py
# @Software: IntelliJ IDEA
import os
import sys
import time

import cv2
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm

cur_path = os.path.dirname(os.path.abspath(sys.argv[0]))
last_path = os.path.dirname(cur_path)


class CharacterPaint:
    def __init__(self):
        # 用于黑白字符画
        self.ascii_char = list("＄＠＃Ｂ％８＆ＷＭＸＺＯ０ＱＬＣＪＵＹＩｏａｘｈｋｂｄｐｑｗｍｚｃｙｕ"
                               "ｎ＊？＋＜＞／＼｜（）ｌ１｛｝［］ｒｊｆｔ～＿－！ｉ；：＾＂＇｀，　")
        # 用于脸色字符画
        self.ascii_char_color = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        # self.ascii_char_color = list("01")
        # 定义基础文件夹，无则新建
        self.input_video_folder = os.path.join(cur_path, 'input_videos')
        self.output_video_folder = os.path.join(cur_path, 'output_videos')
        self.pic_folder = os.path.join(cur_path, 'pics')
        os.makedirs(self.input_video_folder, exist_ok=True)
        os.makedirs(self.output_video_folder, exist_ok=True)
        os.makedirs(self.pic_folder, exist_ok=True)
        # 输出视频默认像素值
        self.size = (1920, 1080)
        # 视频FPS
        self.fps = 30
        # 尺寸这部分应该可以做成自动匹配，暂不搞了
        # 输出字段尺寸
        # self.width, self.height, self.font_size = 96, 42, 20
        # self.width, self.height, self.font_size = 160, 70, 12
        self.width, self.height, self.font_size = 192, 84, 10
        # self.width, self.height, self.font_size = 383, 108, 5

        # 彩色图片配置
        # self.font_size_color, self.width_ratio, self.height_ratio = 10, 6, 8
        self.font_size_color, self.width_ratio, self.height_ratio = 8, 5, 9
        # self.font_size_color, self.width_ratio, self.height_ratio = 6, 4, 7

    def get_char(self, r, g, b, alpha=256, color=True):
        """
        图片转灰度值
        :param r: 红色值
        :param g: 绿色值
        :param b: 蓝色值
        :param alpha: 透明度
        :param color: 是否生成彩色视频
        :return:
        """
        if alpha == 0:
            return ' '
        ascii_char = self.ascii_char_color if color is True else self.ascii_char
        length = len(ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length
        return ascii_char[int(gray / unit)]

    def pic2pic(self, temp_path, image_path):
        """
        图片转彩色字符图
        :param temp_path: 图片临时路径
        :param image_path: 图片最终存储位置
        :return:
        """

        im = Image.open(temp_path)
        width = int(im.width / self.width_ratio)  # 高度比例为原图的1/6较好，由于字体宽度
        height = int(im.height / self.height_ratio)  # 高度比例为原图的1/15较好，由于字体高度
        self.size = (im.width, im.height)
        im_txt = Image.new("RGB", self.size, (255, 255, 255))
        im = im.resize((width, height), Image.NEAREST)
        txt = ""
        colors = []
        for i in range(height):
            for j in range(width):
                pixel = im.getpixel((j, i))
                colors.append((pixel[0], pixel[1], pixel[2]))  # 记录像素颜色信息
                if len(pixel) == 4:
                    txt += self.get_char(pixel[0], pixel[1], pixel[2], pixel[3], color=True)
                else:
                    txt += self.get_char(pixel[0], pixel[1], pixel[2], color=True)
            txt += '\n'
            colors.append((0, 0, 0))
        dr = ImageDraw.Draw(im_txt)
        font = ImageFont.truetype(
            os.path.join("fonts", os.path.join(cur_path, 'fonts', 'Hack-Regular.ttf')), self.font_size_color
        )
        x = y = 0
        # 获取字体的宽高
        font_w, font_h = font.getsize(txt[1])

        # ImageDraw为每个ascii码进行上色
        for i in range(len(txt)):
            if txt[i] == '\n':
                x += font_h
                y = -font_w
            dr.text((y, x), txt[i], colors[i])
            y += font_w
        # 输出
        im_txt.save(image_path)

    def pic2txt(self, image_path):
        """
        将图片转为字符画
        :param image_path: 图片路径
        :return:
        """
        im = Image.open(image_path)
        im = im.resize((self.width, self.height), Image.NEAREST)
        txt = ""
        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j, i)), color=False)
            txt += '\n'
        # print(txt)
        return txt

    def txt2pic(self, text, image_path):
        """
        文本转图片
        :return:
        :param text: 文本
        :param image_path: 目标图片路径
        """
        im = Image.new("RGB", self.size, (0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(
            os.path.join("fonts", os.path.join(cur_path, 'fonts', 'MSYH.TTF')), self.font_size
        )
        dr.text((0, 0), text, font=font, fill="#FFFFFF")
        im.save(image_path)

    def generate_txt_video(self, filename, is_colorful=True):
        """
        将视频转为图片
        :param filename: 文件路径
        :param is_colorful: 是否生成彩色视频
        :return:
        """
        pic_path = os.path.join(self.pic_folder, os.path.basename(filename).split('.')[0])
        video_path = os.path.join(self.input_video_folder, filename)
        temp_image_path = os.path.join(pic_path, 'temp.jpg')
        dnt = 0
        if os.path.exists(pic_path):
            pass

        else:
            os.mkdir(pic_path)
        cap = cv2.VideoCapture(video_path)
        total_frame_nums = cap.get(7)
        for i in tqdm(range(int(total_frame_nums))):
            ret, image = cap.read()
            if image is None:
                break
            cv2.imencode('.jpg', image)[1].tofile(temp_image_path)
            if is_colorful:
                self.pic2pic(temp_image_path, os.path.join(pic_path, f'{dnt}.jpg'))
            else:
                self.txt2pic(self.pic2txt(temp_image_path), os.path.join(pic_path, f'{dnt}.jpg'))
            # print(os.path.join(pic_path, f'{dnt}.jpg'))
            dnt = dnt + 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        os.remove(temp_image_path)
        cap.release()
        print('\033[01;32m视频转换完成\033[0m')

    def pic2video(self, filename, is_colorful=True):
        """
        图片合成视频
        :param filename: 文件路径
        :param is_colorful: 是否生成彩色视频
        :return:
        """
        self.generate_txt_video(filename, is_colorful)
        # 给一点点间隔防止显示错位
        time.sleep(0.1)
        # 原视频名
        basename = os.path.basename(filename).split('.')[0]
        target_image_path = os.path.join(cur_path, 'pics', basename)
        # 使用第0个图作为视频的大小
        im = Image.open(os.path.join(target_image_path, '0.jpg'))
        self.size = (im.width, im.height)
        # 可以用*'XVID'，*'DVIX'或*'X264'，需要根据目标视频格式调节
        # 当前使用的参数是支持微信的
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(os.path.join(self.output_video_folder, f'{basename}_transferred.mp4'),
                                       fourcc, self.fps, self.size, isColor=True)
        # 遍历文件夹下所有文件
        # 因为我使用的视频编辑软件会在后边加2秒多的片尾，故要去除，注意取值是2 * 原视频fps，我这是2 * 30再加了点余量
        size = len(os.listdir(target_image_path)) - 65
        print('\033[01;32m执行视频合成\033[0m')
        time.sleep(0.1)
        for i in tqdm(range(size)):
            frame = cv2.imread(os.path.join(target_image_path, f'{i}.jpg'))
            video_writer.write(frame)
        video_writer.release()
        time.sleep(0.1)
        print('\033[01;32m视频生成完成\033[0m')


if __name__ == '__main__':
    cp = CharacterPaint()
    for i in os.listdir(cp.input_video_folder):
        cp.pic2video(os.path.join(cp.input_video_folder, i), is_colorful=True)
    # 供调节参数使用
    # cp.pic2pic('pics\\rose\\550.jpg', 'test.jpg')
