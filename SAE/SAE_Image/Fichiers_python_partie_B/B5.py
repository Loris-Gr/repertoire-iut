from PIL import Image 

def cacher(i,b) :
    return i-(i%2)+b

def trouver(i) :
    return i%2

i = Image.open("hall-mod_0.bmp")
i_noir = Image.open("Imageout3.bmp")
sortie = i.copy()
for y in range(i.size[1]) :
    for x in range(i.size[0]) :
        c = i.getpixel((x,y))
        (R,V,B) = c
        R = R - R % 2
        try :
            pixel_noir = i_noir.getpixel((x,y))   # je teste si le pixel est sur l'image
        except :
            pixel_noir = (255,255,255)
        if pixel_noir == (0,0,0) :  # si le pixel est noir
            sortie.putpixel((x,y),(cacher(R,1),V,B))      
        else : # si i_noir == (255,255,255) soit si le pixel est blanc
            sortie.putpixel((x,y),(cacher(R,0),V,B)) 
sortie.save("Imageout_steg_1.bmp")

i = Image.open("Imageout_steg_1.bmp")
sortie = Image.new(i.mode, i.size)
for y in range(i.size[1]) :
    for x in range(i.size[0]) :
        c = i.getpixel((x,y))
        (R,V,B) = c
        if trouver(R) == 1 :
            sortie.putpixel((x,y),(0,0,0))
        else : # si trouver(R) == 0
            sortie.putpixel((x,y),(255,255,255))
sortie.save("Imageout3_trouver.bmp")