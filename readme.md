# 视频转字符画
## 依赖
```shell
pip3 install opencv-python=4.5.5
pip3 install Pillow=8.3.1
pip3 install tqdm=4.61.2
```
## 使用
将视频放如input_videos文件夹，然后执行下述命令：
> python3 YOUR_PATH/character_paint/main.py
## 调试
脚本未对视频进行适配，当前只对彩色1280 * 720及像素画1920*1080作了适配，其它分辨率的不确定有用。  
调适方法如下：
```python
cp = CharacterPaint()
# 注释以下两行
# for i in os.listdir(cp.input_video_folder):
#     cp.pic2video(os.path.join(cp.input_video_folder, i), is_colorful=True)
# 供调节参数使用
# 使用该行作为调试入口，参数分别为输入/输出图片，图片路径可自定义
cp.pic2pic('pics\\rose\\550.jpg', 'test.jpg')
```
```python
# 以下参数在__init__中，通过调节各参数，可直观地在上个方法生成的test.jpg中看到字符在画面中的位置、大小等
# font_size会对应视频的精度，越小精度越高，渲染时间越长
# 输出字段尺寸
# 控制像素画的参数
# self.width, self.height, self.font_size = 96, 42, 20
# self.width, self.height, self.font_size = 160, 70, 12
self.width, self.height, self.font_size = 192, 84, 10
# self.width, self.height, self.font_size = 383, 108, 5

# 彩色图片配置
# self.font_size_color, self.width_ratio, self.height_ratio = 10, 6, 8
self.font_size_color, self.width_ratio, self.height_ratio = 8, 5, 9
# self.font_size_color, self.width_ratio, self.height_ratio = 6, 4, 7
```