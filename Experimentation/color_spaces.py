from PIL import Image
import math

image = Image.open("car.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

def rgb_to_hsv(rgb_pixel):
    r = rgb_pixel[0]
    g = rgb_pixel[1]
    b = rgb_pixel[2]
    _max = max(r,g,b)
    _min = min(r,g,b)
    _dif = _max-_min

    h = 0
    s = 0
    v = 0
    if(_max > 0):

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
    _min = v - (s * v)
    _mid = 0
    _diff = (_max - _min)

    base_angle = 0
    if(1/6<h<=3/6):
        base_angle = 120
    if(3/6<h<=5/6):
        base_angle = 240

    rotate_positive = False
    if (0<h<=1/6 or 2/6<h<=3/6 or 4/6<h<=5/6):
        rotate_positive = True
    if rotate_positive:
        _mid = (h_360-base_angle)*_diff/60+_min
    else:
        _mid = (base_angle-h_360)*_diff/60+_min

    if _mid < _min:
        assert base_angle == 0 and rotate_positive == False
        _mid = (base_angle-(360*(h-1)))*_diff/60+_min
        pass
    
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

    rounding_buffer = 0.1
    r_255 = int(rgb_1[0]*255+rounding_buffer)
    g_255 = int(rgb_1[1]*255+rounding_buffer)
    b_255 = int(rgb_1[2]*255+rounding_buffer)
    rgb_255 = (r_255, g_255, b_255)

    return rgb_255

def hsv_shift(start_image, delta_h = 0, delta_s = 0, delta_v = 0):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            old_pixel = data[x,y]
            hsv_pixel = rgb_to_hsv(old_pixel)
            h = (hsv_pixel[0] + (delta_h%1) + 1) % 1

            s = min(hsv_pixel[1] + delta_s,1)
            s = max(hsv_pixel[1] + delta_s,0)

            v = min(hsv_pixel[2] + delta_v,1)
            v = max(hsv_pixel[2] + delta_v,0)

            new_pixel = hsv_to_rgb((h,s,v))

            temp_data[x,y] = new_pixel
    
    return temp_image

def hsv_product(start_image, delta_h = 0, delta_s = 1, delta_v = 1):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            old_pixel = data[x,y]
            hsv_pixel = rgb_to_hsv(old_pixel)
            h = (hsv_pixel[0] + (delta_h%1) + 1) % 1

            s = min(hsv_pixel[1] * delta_s,1)
            s = max(s,0)

            v = min(hsv_pixel[2] * delta_v,1)
            v = max(v,0)

            new_pixel = hsv_to_rgb((h,s,v))

            temp_data[x,y] = new_pixel
    
    return temp_image

def hsv_pow(start_image, delta_h = 0, delta_s = 1, delta_v = 1):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            old_pixel = data[x,y]
            hsv_pixel = rgb_to_hsv(old_pixel)
            h = (hsv_pixel[0] + (delta_h%1) + 1) % 1

            s = math.pow(hsv_pixel[1], delta_s)

            v = math.pow(hsv_pixel[2], delta_v)

            new_pixel = hsv_to_rgb((h,s,v))

            temp_data[x,y] = new_pixel
    
    return temp_image

def hue_crush(start_image, target_h, strength = 0):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    target_h %=1
    target_h +=1
    target_h %=1

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            old_pixel = data[x,y]
            hsv_pixel = rgb_to_hsv(old_pixel)

            h = hsv_pixel[0]
            s = hsv_pixel[1]
            v = hsv_pixel[2]

            new_h = h

            # left of hue wrap around
            if(target_h + .5 <= h):
                    new_h -= 1
            # right of hue wrap around
            elif(h <= target_h - .5):
                    new_h += 1

            dif = target_h - new_h
            dif_scaled = dif * strength

            new_h += dif_scaled
            if (new_h < 0 or new_h > 1):
                new_h %= 1
                new_h += 1
                new_h %= 1

            new_pixel = hsv_to_rgb((new_h,s,v))

            temp_data[x,y] = new_pixel

    return temp_image


# new_image = hsv_shift(image,5/6,-.5,-.5)
# new_image.save("hsv_shift.png")

# new_image = hsv_product(image,4/6,.5,.5)
# new_image.save("hsv_mult.png")

new_image = hsv_pow(image,0,2,2)
new_image.save("hsv_pow.png")

new_image = hsv_pow(image,0,1/2,1/2)
new_image.save("hsv_root.png")

# target_hue = 1/6 - 5/60
# new_image = hue_crush(image,target_hue,1)
# new_image.save("hue_crush.png")

# rgb_test = (50,100,75)
# print(rgb_test)
# for i in range(10):
#     hsv_test = rgb_to_hsv(rgb_test)
#     print(hsv_test)
#     rgb_test = hsv_to_rgb(hsv_test)
#     print(rgb_test)