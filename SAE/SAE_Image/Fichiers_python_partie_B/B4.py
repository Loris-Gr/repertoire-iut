from PIL import Image 

i = Image.open("IUT-Orleans.bmp") 
sortie = i.copy()
for y in range(i.size[1]) :
    for x in range(i.size[0]) :
        c = i.getpixel((x,y))
        (R,V,B) = c  
        if (R*R+V*V+B*B)>255*255*3/2 :
            sortie.putpixel((x,y),(255,255,255)) # pour le blanc
        else : 
            sortie.putpixel((x,y),(0,0,0)) # pour le noir
sortie.save("Imageout3.bmp")

