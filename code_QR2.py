import qrcode
import cv2
import pandas as pd
import qrcode.image.svg
img = qrcode.make('test text')

print(type(img))
print(img.size)
# <class 'qrcode.image.pil.PilImage'>
# (290, 290)
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_M,
    box_size = 10,
    border = 4,
)

factory = qrcode.image.svg.SvgPathImage
with open("down_compressed.txt","r") as file:
        code = file.readlines()[0]
        t=0
        v=0
        data=[]
        print(len(code))
        while t<=len(code):
    
    # 2200 high capacity that qr code can takes
             data = code[t:t+2200]
       # Create an image from the QR Code instance
             img = qrcode.make(data)      
    # Save it somewhere, change the extension as needed:
             img.save("codeqr"+str(v)+".jpg")
             v+=1
            # data=code[t:t+2300]
             #mg=qrcode.make(data)
             #mg.save('idk.jpg')
             data=[]
             save=t
             t=t+2200
     
        


            

        
            


def read_qr_code(filename):

    
    try:
       
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value,point,straight = detect.detectAndDecode(img)
    
       
        return value
    except:
        return
stock="" 
t=""  
print("la valuer de v est ")
value=""
v=v-1
sum = v
v=0
print(v)   
while v<=sum  :
    value=read_qr_code("codeqr"+str(v)+".jpg")
    print("literation est")
    print(v)
   
    v=v+1
    
    stock =  str(stock) + str(value)
    t=""
    

with open("complex.txt","w") as file :
        file.write(stock)
        file.close()           

print(len(stock))    