#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/14 16:21
# @File    : main.py
# @Software: IntelliJ IDEA
import os
import sys
import cv2
from PIL import Image, ImageFont, ImageDraw

cur_path = os.path.dirname(os.path.abspath(sys.argv[0]))
last_path = os.path.dirname(cur_path)


class CharacterPaint:
    def __init__(self):
        # 用于黑白字符画
        # self.ascii_char = list("＄＠＃Ｂ％８＆ＷＭＸＺＯ０ＱＬＣＪＵＹＩｏａｘｈｋｂｄｐｑｗｍｚｃｙｕ"
        #                        "ｎ＊？＋＜＞／＼｜（）ｌ１｛｝［］ｒｊｆｔ～＿－！ｉ；：＾＂＇｀，　")
        # 用于脸色字符画
        self.ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

        self.video_folder = os.path.join(cur_path, 'input_videos')
        self.pic_folder = os.path.join(cur_path, 'pics')
        # 输出图片像素值
        self.size = (1920, 1080)
        # 视频FPS
        self.fps = 30
        # 输出字段尺寸
        # self.width, self.height, self.font_size = 96, 42, 20
        # self.width, self.height, self.font_size = 160, 70, 12
        # self.width, self.height, self.font_size = 192, 84, 10
        # self.width, self.height, self.font_size = 383, 108, 5
        self.width, self.height, self.font_size = 192, 84, 12

    def get_char(self, r, g, b, alpha=256):
        """
        图片转灰度值
        :param r:
        :param g:
        :param b:
        :param alpha:
        :return:
        """
        if alpha == 0:
            return ' '
        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray / unit)]

    def pic2pic(self, temp_path, image_path):
        """
        图片转彩色字符图
        :return:
        """

        im = Image.open(temp_path)
        WIDTH = int(im.width / 6)  # 高度比例为原图的1/6较好，由于字体宽度
        HEIGHT = int(im.height / 15)  # 高度比例为原图的1/15较好，由于字体高度
        im_txt = Image.new("RGB", (im.width, im.height), (231, 223, 223))
        im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
        txt = ""
        colors = []
        for i in range(HEIGHT):
            for j in range(WIDTH):
                pixel = im.getpixel((j, i))
                colors.append((pixel[0], pixel[1], pixel[2]))  # 记录像素颜色信息
                if len(pixel) == 4:
                    txt += self.get_char(pixel[0], pixel[1], pixel[2], pixel[3])
                else:
                    txt += self.get_char(pixel[0], pixel[1], pixel[2])
            txt += '\n'
            colors.append((0, 0, 0))
        dr = ImageDraw.Draw(im_txt)
        font = ImageFont.load_default().font  # 获取字体
        x = y = 0
        # 获取字体的宽高
        font_w, font_h = font.getsize(txt[1])
        font_w *= 1
        font_h *= 1

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
        :param image_path:
        :return:
        """
        im = Image.open(image_path)
        im = im.resize((self.width, self.height), Image.NEAREST)
        txt = ""
        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j, i)))
            txt += '\n'
        # print(txt)
        return txt

    def txt2pic(self, text, image_path):
        """
        文本转图片
        :return:
        """
        im = Image.new("RGB", self.size, (0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", os.path.join(cur_path, 'fonts', 'MSYH.TTF')), self.font_size)
        dr.text((0, 0), text, font=font, fill="#FFFFFF")
        im.save(image_path)

    def generate_txt_video(self, filename):
        """
        将视频转为图片
        :param filename:
        :return:
        """
        pic_path = os.path.join(self.pic_folder, os.path.basename(filename).split('.')[0])
        video_path = os.path.join(self.video_folder, filename)
        temp_image_path = os.path.join(pic_path, 'temp.jpg')
        dnt = 0
        if os.path.exists(pic_path):
            pass

        else:
            os.mkdir(pic_path)
        cap = cv2.VideoCapture(video_path)
        while True:
            # get a frame
            ret, image = cap.read()
            if image is None:
                break
            cv2.imencode('.jpg', image)[1].tofile(temp_image_path)
            # self.txt2pic(self.pic2txt(temp_image_path), os.path.join(pic_path, f'{dnt}.jpg'))
            self.pic2pic(temp_image_path, os.path.join(pic_path, f'{dnt}.jpg'))
            print(os.path.join(pic_path, f'{dnt}.jpg'))
            dnt = dnt + 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        os.remove(temp_image_path)
        cap.release()

    def pic2video(self):
        """
        图片合成视频
        :return:
        """
        # 可以用*'XVID'，*'DVIX'或*'X264'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # video_writer = cv2.VideoWriter(os.path.join(cur_path, 'output_videos', 'final.mp4'),
        #                                fourcc, self.fps, self.size, isColor=True)
        video_writer = cv2.VideoWriter(os.path.join(cur_path, 'output_videos', 'final.mp4'),
                                       fourcc, self.fps, (1280, 720), isColor=True)
        # 遍历文件夹下所有文件
        # 去除后3秒内容
        size = len(os.listdir(os.path.join(cur_path, 'pics', 'rose'))) - 65
        for i in range(size):
            frame = cv2.imread(os.path.join(self.pic_folder, 'rose', f'{i}.jpg'))
            video_writer.write(frame)
        video_writer.release()


if __name__ == '__main__':
    cp = CharacterPaint()
    vp = os.path.join(cur_path, 'input_videos', 'rose.mp4')
    cp.generate_txt_video(vp)
    cp.pic2video()
    # cp.pic2pic('pics\\rose\\500.jpg', 't.jpg')
