from PIL import Image 

i = Image.open("Imagetest.bmp")
sortie = i.copy()
for y in range(i.size[1]) :
    for x in range(i.size[0]) :
        c = i.getpixel((x,y))
        sortie.putpixel((y,x),c)
sortie.save("Imageout0.bmp")
