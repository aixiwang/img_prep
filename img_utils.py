# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2017, Aixi Wang <aixi.wang@hotmail.com>
# 
#=========================================================

import json
import os
import math
import time
from PIL import Image
DEBUG = 0

INPUT_FILE = './img/in_%%.jpg'
OUTPUT_FILE = './img/out_%%.jpg'
P2_FILE = './img/P2_%%.jpg'
P3_FILE = './img/P3_%%.jpg'
P4_FILE = './img/P4_%%.jpg'
ERR_FILE = './img/err_%%.jpg'

#----------------------
# find_subimg_rect
#----------------------
def find_subimg_rect(img):
    #h,w,n = img.shape
    w,h = img.size
    
    print 'find_subimg_rect:','h:',h,' w:',w
    x_max = 0
    x_min = w-1
    y_max = 0
    y_min = h-1

    flag = 0
    
    if img.mode != 'RGBA':
        img = img.convert('RGB')
    w,h = img.size
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            pix = pixels[x,y]
            if pix[0] == 255 and pix[1] == 0 and pix[2] == 0:
                #print y,x,img[y][x]
                flag = 1
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                    
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
       
    print 'find_mask_rect:',x_min,y_min,x_max,y_max
    
    if flag == 1:
        return 0,[[x_min,y_min],[x_max,y_max]]
    else:
        return -1,[[x_min,y_min],[x_max,y_max]]
        

#----------------------
# find_angle
#----------------------
def find_angle(img):
    #h,w,n = img.shape
    w,h = img.size

    print 'find_angle:','h:',h,' w:',w
    x_max = 0
    x_min = w-1
    y_max = 0
    y_min = h-1
    
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    flag = 0
    
    if img.mode != 'RGBA':
        img = img.convert('RGB')
    w,h = img.size
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            pix = pixels[x,y]
            if pix[0] == 255 and pix[1] == 0 and pix[2] == 0:
            
            #if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 255:
                #print y,x,img[y][x]
                flag = 1                   
                if x > x_max:
                    x_max = x
                    x2 = x
                    y2 = y
                    
                if x < x_min:
                    x_min = x
                    x1 = x
                    y1 = y
                    
    #print x_min,y_min,x_max,y_max
    
    if flag == 1:
        if x_max == x_min:
            angle = 90
        elif y_max == y_min:
            angle = 0
        else:
            l = math.sqrt((x1-x2)*(x1-x2) + (y2-y1)*(y2-y1))
            angle_hu = math.acos((x2-x1)/l)
            print 'angle_hu:',angle_hu
            angle = angle_hu*180.0/math.pi
        
        print 'angle:',angle
        
        return 0,angle
    else:
        return -1,0


#----------------------
# find_transform_points
#----------------------
def find_transform_points(img):
    #h,w,n = img.shape
    w,h = img.size

    
    points = []
    print 'find_transform_points:','h:',h,' w:',w,
    x_max = 0
    x_min = w-1
    y_max = 0
    y_min = h-1
    
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    flag = 0
    
    
    if img.mode != 'RGBA':
        img = img.convert('RGB')
    w,h = img.size
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            pix = pixels[x,y]
            if pix[0] == 255 and pix[1] == 0 and pix[2] == 0:
                flag = 1                                   
                points.append([x,y])
                    

    if flag == 1 and len(points) == 4:
        print points
        return 0,points
    else:
        return -1,[]
        

#----------------------
# find_segs_points
#----------------------
def find_segs_points(img):
    #h,w,n = img.shape
    w,h = img.size

    
    points = []
    print 'find_segs_points:','h:',h,' w:',w
    x_max = 0
    x_min = w-1
    y_max = 0
    y_min = h-1
    
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    flag = 0
    
    if img.mode != 'RGBA':
        img = img.convert('RGB')
    w,h = img.size
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            pix = pixels[x,y]
            if pix[0] == 255 and pix[1] == 0 and pix[2] == 0:
                flag = 1                                   
                points.append([x,y])
                    

    if flag == 1:
        print points
        return 0,points
    else:
        return -1,[]

#----------------------
# gen_config
#----------------------
def gen_config():
    mask_json = {}
    
    if os.path.exists('config.json'):
        try:
            f = open('config.json','rb')
            s = f.read()
            mask_json = json.loads(s)
            print 'read mask_json from file config.json'
            retcode = 0

        except:
            retcode = -1
        # return directly from config.json
        return retcode,mask_json

    #    
    # rebuild config.json
    #
    else:
        if os.path.exists('mask.bmp'):
            #retcode2,angle = find_angle(mask_img)
            mask_img = Image.open('mask.bmp')
            retcode1,transform_src = find_transform_points(mask_img)
        else:
            transform_src = []
            retcode1 = -1
            
        if os.path.exists('mask2.bmp'):
            mask_img = Image.open('mask2.bmp')
            retcode2,subimg_rect = find_subimg_rect(mask_img)
        else:
            retcode2 = -1
            subimg_rect = []
            
        if os.path.exists('mask3.bmp'):
            mask_img = Image.open('mask3.bmp')
            retcode3,seg_points = find_segs_points(mask_img)
        else:
            retcode3 = -1
            seg_points = []

        # get existed transform_des
        if os.path.exists('config2.json'):
            try:
                f = open('config2.json','rb')
                s = f.read()
                config2 = json.loads(s)
                transform_des = config2['transform_des']
                resize = config2['resize']
                rotate_base = config2['rotate_base']
                duration = config2['duration']
                seg_group_map = config2['seg_group_map']
                run_mode = config2['run_mode']
                print 'read mask_json from file config.json'

            except:
                transform_des = []
                resize = []
                rotate_base = 180
                duration = 60
                seg_group_map = []
                run_mode = 'normal'
        else:
            transform_des = []
            resize = []
            rotate_base = 180
            duration = 60
            seg_group_map = []
            run_mode = 'normal'
        retcode = 0

        mask_json = {
                     'subimg_rect':subimg_rect,
                     'seg_points':seg_points,
                     'resize':resize, 
                     'rotate':0,
                     'rotate_base':rotate_base,
                     'transform_src':transform_src,
                     'transform_des':transform_des,
                     'duration':duration,
                     'seg_group_map':seg_group_map,
                     'run_mode':run_mode
                    }
        mask_json_s = json.dumps(mask_json)
        f = open('config.json','wb')
        f.write(mask_json_s)
        f.close()
        print 'config.json generated'        
        return retcode,mask_json

#----------------------
# rotate
#----------------------
def rotate(img,angle):
    img2 = img.rotate(angle)
    return img2

#----------------------
# transform
#----------------------
def transform(img,points_src,points_des):
    #height = img.shape[0]
    #width = img.shape[1]
    w,h = img.size

    scale = 1
    print 'transform:',h,w
        
    #pts1 = np.float32(points_src)
    #pts2 = np.float32(points_des)
    #M = cv2.getPerspectiveTransform(pts1,pts2)    
    #dst = cv2.warpPerspective(img,M,(w,h))
    #return dst
    return img
    
#----------------------
# my_img_binarization
#---------------------- 
def my_img_binarization(f1,f2):
    img = Image.open(f1)

    w,h = img.size
    
    print 'f1:',f1,'h:',h,'w:',w
    new_image = Image.new('RGB', (w, h))

    pixels = new_image.load()        
    for x in range(w):
        for y in range(h):
            pix = pixels[x,y]
            pixels[x,y] = (255,255,255)

    pixels2 = img.load()
    sum = 0
    for x in range(w):
        for y in range(h):
            pix = pixels2[x,y]
            gray = (pix[0]*299 + pix[1]*587 + pix[2]*114 + 500)/1000  # (R*299 + G*587 + B*114 + 500)/1000
            sum += gray
            pixels2[x,y] = (gray,0,0)
            
    avg = sum/(h*w)        
    print 'avg:',avg                


    # binarization
    for x in range(w):
        for y in range(h):
            pix = pixels2[x,y]
            if pix[0] < avg:
                pixels[x,y] = (0,0,0)

    # remove isolated points
    for y in range(h):
        for x in range(w):
            pix = pixels[x,y]
            if pixels[x,y][0] == 0 and (y == 0 or y == (h-1)):
                pixels[x,y] = (255,255,255)
                
            elif pixels[x,y][0] == 0 and (x == 0 or x == (w-1)):
                pixels[x,y] = (255,255,255)
                
            elif pixels[x,y][0] == 0 and pixels[x-1,y-1][0] == 255 and pixels[x+1,y+1][0] == 255 and pixels[x,y-1][0] == 255 and pixels[x,y+1][0] == 255 and pixels[x-1,y][0] == 255 and pixels[x+1,y][0] == 255 and pixels[x+1,y-1][0] == 255 and pixels[x-1,y+1][0] == 255:
                pixels[x,y] = (255,255,255)
            else:
                pass

    new_image.save(f2)
    return 0, new_image

#----------------------------
# gen_filename
#----------------------------        
def gen_filename(f_template,t):
    t_s = time.strftime('%Y%m%d-%H%M%S', time.localtime(t))
    return f_template.replace('%%',t_s)

#----------------------------
# do_img_prep
#----------------------------    
def do_img_prep(input_file,output_file):
    retcode,json_mask = gen_config()

    #while True:
    
    t1 = time.time()
    f1 = gen_filename(INPUT_FILE,t1)
    f2 = gen_filename(P2_FILE,t1)
    f3 = gen_filename(P3_FILE,t1)
    f4 = gen_filename(P4_FILE,t1)
    err_f = gen_filename(ERR_FILE,t1)
    
    retcode,config_json = gen_config()

    #
    # init local config values
    #
    print 'mask_jon:',config_json
    subimg_rect = config_json['subimg_rect']
    resize = config_json['resize']
    rotate_deg = config_json['rotate']
    rotate_base = config_json['rotate_base']
    duration = config_json['duration']

    points_src = config_json['transform_src']
    points_des = config_json['transform_des']
    seg_points = config_json['seg_points']
    seg_group_map = config_json['seg_group_map']            
    run_mode = config_json['run_mode']
    
    # create folder for img storing
    if os.path.exists('./img') == False:
        os.system('mkdir img')
            
    
    if os.path.exists(input_file):        
        raw_image = Image.open(input_file)

        #if len(points_src) == 4 and len(points_des) == 4:
        #    print 'step 1 =================> do transforming ...'
        #    img2 = img_utils.transform(raw_image,points_src,points_des)

        if (rotate_base + rotate_deg) != 0:
            print 'step 2 =================> do rotating ...'
            img2 = rotate(raw_image, (rotate_base + rotate_deg)*(-1))
            
        else:
            img2 = raw_image
            
        img2.save(f2)
        
        if len(subimg_rect) > 0:
            print 'step 3 =================> do sub imaging ...'
        
            x1 = subimg_rect[0][0]
            y1 = subimg_rect[0][1]
            x2 = subimg_rect[1][0] 
            y2 = subimg_rect[1][1] 
           
            box = (x1, y1, x2, y2)
            img3 = img2.crop(box)

            img3.save(f3)

            print 'step 4 =================> do binarization ...'
            ret,new_image = my_img_binarization(f3,output_file)                               
            
            if len(seg_points)>0:
                print 'step 5 =================> do extract seg info. ..., TBD'

                
            if run_mode == 'normal':
                try:
                    os.remove(f2)
                    os.remove(f3)
                except:
                    pass
                

        else:
            print 'no subimg_rect defintion, passed reamaining steps'
            pass
        # call text recognition function here

        
#----------------------
# main
#----------------------
if __name__ == "__main__":
    pass
