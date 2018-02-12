from PIL import Image

img = Image.open("mask.bmp")
if img.mode != 'RGBA':
    img = img.convert('RGB')
    
img.show()
img2 = img.rotate(45)
img2.show()
    
w,h = img.size
pixels = img.load()

for x in range(w):
    for y in range(h):
        pix = pixels[x,y]
        #print pix[0],pix[1],pix[2]
        pixels[x,y] = (255,0,0)

img.show()

#img.point([0]*w*h)
#img.show()

        
        
