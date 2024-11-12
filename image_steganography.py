from PIL import Image

def genData(data):
    # Convert input data into 8-bit binary representation.
    return [format(ord(i), '08b') for i in data]

def modPix(pix, data):
    # Modify pixels of the image according to the binary data.
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    
    for i in range(lendata):
        # Extracting pixels for modification
        pix = [value for value in imdata.__next__()[:3] +
                              imdata.__next__()[:3] +
                              imdata.__next__()[:3]]

        # Modify pixel values based on the binary data
        for j in range(8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                pix[j] = pix[j] - 1 if pix[j] != 0 else pix[j] + 1

        # Modify the last pixel to indicate end of message
        if i == lendata - 1:
            pix[-1] = pix[-1] - 1 if pix[-1] % 2 == 0 and pix[-1] != 0 else pix[-1] + 1
        else:
            pix[-1] -= 1 if pix[-1] % 2 != 0 else pix[-1]

        pix = tuple(pix)
        yield pix[:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    # Encode the data into the image.
    w, h = newimg.size
    x, y = 0, 0

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode():
    # Encode a message into an image.
    img_path = input("Enter image name (with extension): ")
    try:
        image = Image.open(img_path, 'r')
    except FileNotFoundError:
        print(f"Error: File {img_path} not found.")
        return

    data = input("Enter data to be encoded: ")
    if not data:
        print("Error: Data is empty.")
        return

    max_data_len = image.size[0] * image.size[1] * 3 // 8
    if len(data) > max_data_len:
        print("Error: Data too long for the image.")
        return

    newimg = image.copy()
    encode_enc(newimg, data)
    newimg.save("encoded_" + img_path)
    print("Data encoded successfully and saved as 'encoded_" + img_path + "'.")

def decode():
    # Decode the message from an image.
    img_path = input("Enter image name (with extension): ")
    try:
        image = Image.open(img_path, 'r')
    except FileNotFoundError:
        print(f"Error: File {img_path} not found.")
        return

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])

        if len(binstr) == 8:
            data += chr(int(binstr, 2))

        if pixels[-1] % 2 != 0:
            return data

def main():
    # Main function
    try:
        choice = int(input(":: Welcome to Steganography ::\n1. Encode\n2. Decode\nChoose an option: "))
        if choice == 1:
            encode()
        elif choice == 2:
            decoded_data = decode()
            if decoded_data:
                print("Decoded Data: " + decoded_data)
            else:
                print("No data decoded.")
        else:
            print("Error: Invalid choice. Please select 1 or 2.")
    except ValueError:
        print("Error: Invalid input. Please enter a number.")


main()
