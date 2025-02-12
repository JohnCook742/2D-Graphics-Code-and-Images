from PIL import Image
import math
import hsv

image = Image.open("car.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

def rgb_to_hsv(rgb_pixel):
    r = rgb_pixel[0]
    g = rgb_pixel[1]
    b = rgb_pixel[2]

    h = 0
    s = 0
    v = 0
    if(max(r,g,b) > 0):
        _max = max(r,g,b)
        _dif = _max-min(r,g,b)

        v = _max/255
        s = (_dif)/_max
        h = find_hue(rgb_pixel, _max, _dif)

    hsv_pixel = (h,s,v)
    return hsv_pixel

def find_hue(rgb_pixel, _max, _dif):
    r = rgb_pixel[0]
    g = rgb_pixel[1]
    b = rgb_pixel[2]
    h_360 = 0
    if(_dif == 0):
        h_360 = 0
    elif(r == _max):
        h_360 = 0 + 60*(g-b)/_dif
    elif(g == _max):
        h_360 = 120 + 60*(b-r)/_dif
    else: # b == _max
        h_360 = 240 + 60*(r-g)/_dif

    if h_360 < 0: h_360 += 360

    return h_360/360

def hsv_to_rgb(hsv_pixel):
    h = hsv_pixel[0]
    s = hsv_pixel[1]
    v = hsv_pixel[2]

    h_360 = h*360
    _max = v
    _min = v-s*v
    _mid = 0
    _diff = _max - _min

    base_angle = 0
    if(1/6<h<=3/6):
        base_angle = 120
    elif(3/6<h<=5/6):
        base_angle = 240

    rotate_positive = False
    if (0<=h<1/6 or 2/6<=h<3/6 or 4/6<=h<5/6):
        rotate_positive = True
    if rotate_positive:
        _mid = (h_360-base_angle)*_diff/60+_min
    else:
        _mid = (base_angle-h_360)*_diff/60+_min
    
    rgb_1 = (0,0,0)
    if base_angle == 0:
        if rotate_positive:
            rgb_1 = (_max, _mid, _min)
        else:
            rgb_1 = (_max, _min, _mid)

    if base_angle == 120:
        if rotate_positive:
            rgb_1 = (_min, _max, _mid)
        else:
            rgb_1 = (_mid, _max, _min)
    
    if base_angle == 240:
        if rotate_positive:
            rgb_1 = (_mid, _min, _max)
        else:
            rgb_1 = (_min, _mid, _max)

    r_255 = int(rgb_1[0]*255)
    g_255 = int(rgb_1[1]*255)
    b_255 = int(rgb_1[2]*255)
    rgb_255 = (r_255, g_255, b_255)

    return rgb_255

def rgb_to_cmyk(rgb_pixel):
    rgb_scale = 255
    r = rgb_pixel[0]/rgb_scale
    g = rgb_pixel[1]/rgb_scale
    b = rgb_pixel[2]/rgb_scale

    v = max(r,g,b)
    k = 1-v
    if v == 0:
        return(0,0,0,1)
    c = 1 - r/v
    m = 1 - g/v
    y = 1 - b/v

    return (c,m,y,k)

def cmyk_to_rgb(cmyk_pixel):
    rgb_scale = 255
    c = cmyk_pixel[0]
    m = cmyk_pixel[1]
    y = cmyk_pixel[2]
    k = cmyk_pixel[3]

    round_buffer = 0.1
    v = 1-k
    r = int((v-v*c) * rgb_scale + round_buffer)
    g = int((v-v*m) * rgb_scale + round_buffer)
    b = int((v-v*y) * rgb_scale + round_buffer)

    return (r,g,b)

test_rgb = (100,90,89)
print(test_rgb)

print(rgb_to_hsv(test_rgb))
test_hsv = rgb_to_hsv(test_rgb)
print(hsv.hsv_to_rgb(test_hsv[0],test_hsv[1],test_hsv[2]))
print(hsv_to_rgb(test_hsv))

print(rgb_to_cmyk(test_rgb))
test_cmyk = rgb_to_cmyk(test_rgb)
print(cmyk_to_rgb(test_cmyk))
        