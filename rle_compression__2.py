from PIL import Image
import numpy as np
import cv2
import warnings
warnings.filterwarnings("ignore")

def encode(image, file_name='compressed_image.txt', bits=15):

    count_list = []
    count = 0
    prev = None
    fimage = image.flatten()
    size = 2**(bits+1) - 2**bits #32768 = 8000H
    
    for pixel in fimage:
        
        if prev == None:
            prev = pixel 
            count += 1
        else:
            if prev != pixel: # The current pixel is different from the previous one
                if count >= 3:
                    count_list.append((size+count, [prev]))
                else:
                    if count_list == []:
                        count_list.append((count, [prev]*count))
                    else: 
                        c, color = count_list[-1]
                        if c > size: 
                            count_list.append((count, [prev]*count))
                        else:
                            if c+count <= (2**bits)-1: # Make sure that we didn't use all of the 15 bits reserved for the color's sequence length 
                                count_list[-1] = (c+count, color+[prev]*count)
                            else:
                                count_list.append((count, [prev]*count))
                prev = pixel
                count = 1
            else: # The current pixel is like the previous one
                if count < (2**bits)-1: # Make sure that we didn't use all of the 15 bits reserved for the number of repetitions 
                    count += 1                    
                else:
                    count_list.append((size+count, [prev]))
                    prev = pixel
                    count = 1

    if count >= 3:
        count_list.append((size+count, [prev]))
    else:
        c, color = count_list[-1]
        if c > size:
            count_list.append((count, [prev]*count))
        else:
            if c+count <= (2**bits)-1:
                count_list[-1] = (c+count, color+[prev]*count)
            else:
                count_list.append((count, [prev]*count))

    # Hexa encoding
    with open(file_name,"w") as file:
        hexa_encoded = "".join(map(lambda x: "{0:04x}".format(x[0])+"".join(map(lambda y: "{0:02x}".format(y), x[1])), count_list))
        """ hexa_encoded = ""
        for count, colors in count_list:
            hexa_encoded += "{0:04x}".format(count)
            for color in colors:
                hexa_encoded += "{0:02x}".format(color) """
        file.write(hexa_encoded)
        
    # Compression rate
    rate = (1-(len(hexa_encoded)/2)/len(fimage))*100
    
    return hexa_encoded, rate

image1_np = np.array([[0, 1, 0, 1, 0, 1], 
                    [1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0], 
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0]])*255

image2_np = np.array([[0, 0, 0, 1, 1, 1], 
                    [1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1], 
                    [1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1]])*255

image3_np = np.array([[0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1], 
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]])*255

encoded, rate = encode(image1_np, file_name='compressed1.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 38/36 = -5.56%

encoded, rate = encode(image2_np, file_name='compressed2.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 24/36 = 33.33 %

encoded, rate = encode(image3_np, file_name='compressed3.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 9/36 = 75.00 %

img_gray = cv2.imread('random.jpg', cv2.IMREAD_GRAYSCALE)
_, img_bw = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
cv2.imwrite('random_bi.png', img_bw)
height, width = img_bw.shape # 787x444 = 349428
encoded, rate = encode(img_bw, file_name='random_compressed.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 4292/349428 = 98.77%

img_gray = cv2.imread('cablecar.bmp', cv2.IMREAD_GRAYSCALE)
_, img_bw = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
cv2.imwrite('cablecar_bi.png', img_bw)
height, width = img_bw.shape # 512x480 = 245760
encoded, rate = encode(img_bw, file_name='cablecar_compressed.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 22927/245760 = 90.67%
