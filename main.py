from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="steg/windowsxp_encoded.png"):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)

    decoded_image.save("steg/windowsxp_decode.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 50
    for line in textwrap.wrap(text_to_write, width=200):
        drawer.text((margin,offset), line, font=font)
        offset += 50
    return image_text

def encode_image(text_to_encode, template_image="steg/windowsxp.jpg"):
    template_image = Image.open(template_image)

    R = template_image.split()[0]
    G = template_image.split()[1]
    B = template_image.split()[2]

    template_image_size0 = template_image.size[0]
    template_image_size1 = template_image.size[1]

    text = write_text(text_to_encode, template_image.size)
    converted_text = text.convert('1')

    encoded_image = Image.new("RGB", (template_image_size0, template_image_size1))

    for x in range(template_image_size0):
        for y in range(template_image_size1):
            Rpixel = bin(R.getpixel((x, y)))
            converted_text_withpixel = bin(converted_text.getpixel((x, y)))

            if converted_text_withpixel[-1] == '0':
                Rpixel = Rpixel[:-1] + '0'
            else:
                Rpixel = Rpixel[:-1] + '1'

            pixel = encoded_image.load()
            pixel[x, y] = (int(Rpixel, 2), G.getpixel((x, y)), B.getpixel((x, y)))

    encoded_image.save("steg/windowsxp_encoded.png")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    # print("Encoding the image...")
    # encode_image('To jest przykladowy teksty')