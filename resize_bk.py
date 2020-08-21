from PIL import Image

im = Image.open("assets/sprites/message.png")
resized_im = im.resize(( 400 , 500 ))
resized_im.save('assets/sprites/message.png')
