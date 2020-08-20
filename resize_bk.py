from PIL import Image

im = Image.open("assets/sprites/background.png")
resized_im = im.resize(( 500 , 700 ))
resized_im.save('assets/sprites/background.png')
