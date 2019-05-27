
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# 实例一个图片对象240 x 60:
width = 60 * 4
height = 60
# 图片颜色
clo = (43, 34, 88)  # 我觉得是紫蓝色
# 创建图片对象 参2参3是宽高和背景色
image = Image.new('RGB', (width, height), clo)

# 创建Font对象:
# 字体文件可以使用操作系统的，也可以网上下载
font = ImageFont.truetype('./font/CorporateS-RegularItalic.otf', 36)

# 创建Draw对象:
draw = ImageDraw.Draw(image)

# 输出文字:
str1 = "ren ren Python"
w = 4  # 距离图片左边距离
h = 10  # 距离图片上边距离
draw.text((w, h), str1, font=font)
# draw.text((w, h), str1)
# 模糊:
image.filter(ImageFilter.BLUR)
code_name = 'test_code_img.jpg'
save_dir = './{}'.format(code_name)
image.save(save_dir, 'jpeg')
print("已保存图片: {}".format(save_dir))