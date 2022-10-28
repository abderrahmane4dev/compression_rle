import qrcode
import glob
import cv2
import pandas as pd
import pathlib
img = qrcode.make('test text')

print(type(img))
print(img.size)
# <class 'qrcode.image.pil.PilImage'>
# (290, 290)
with open("compressed1.txt","r") as file:
        code = file.readlines()[0]
        img1=qrcode.make(code)
        img1.save('testimg.png')
img.save('qrcode_test.png')


def read_qr_code(filename):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return
value = read_qr_code('testimg.png')  
print(value)      