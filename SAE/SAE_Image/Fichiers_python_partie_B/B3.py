from PIL import Image 

i = Image.open("IUT-Orleans.bmp") 
sortie = i.copy()
for y in range(i.size[1]) :
    for x in range(i.size[0]) :
        c = i.getpixel((x,y))
        gris = (c[0] + c[1] + c[2])//3 # (R+V+B)/3
        sortie.putpixel((x,y),(gris,gris,gris))
sortie.save("Imageout2.bmp")