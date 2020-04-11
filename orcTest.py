from PIL import Image
import pytesseract
import urllib.parse
import config
from identify_code import *

pytesseract.pytesseract.tesseract_cmd = r"C:\app\Tesseract\tesseract.exe"

img = Image.open('1.jpg')
img = img.convert('RGBA')
w, h = img.size[0], img.size[1]
print(w, h)
point_list = gen_white_black_points(img)
print_char_pic(w, h, point_list)
reduce_noisy(w, h, point_list)
print_char_pic(w, h, point_list)

img.putdata(point_list)
img.save("rebuild.png")

code=pytesseract.image_to_string(Image.open('rebuild.png'))
print('识别到的验证码为:'+str(code))