import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import os
import warnings
warnings.filterwarnings("ignore")

def show(img, figsize=(10, 10), title="Image"):
    figure=plt.figure(figsize=figsize)
    
    plt.imshow(img)
    plt.show()
    
    
    
nv = np.array(([[0,255,0,255,0,255],
               [255,0,255,0,255,0],
                [0,255,0,255,0,255],
                [255,0,255,0,255,0],
                [0,255,0,255,0,255],
                [255,0,255,0,255,0]]))   

 




def RLE_encoding(img,file_name="dah_compression.txt" ,bits=15):
       
    fimg = img.flatten()
    encoded=[]
    count = 0
    size = 2**(bits+1) - 2**bits
    prev = None 
    for pixel in fimg: 
        if prev== None : 
           prev= pixel  
           count+= 1  
        else :
              if  prev != pixel :
                  if count >= 3 :
                        encoded.append((size+count,[prev]))
                  else : 
                     if encoded==[] : 
                        encoded.append((count,[prev]*count))
                     else : 
                         c, color = encoded[-1]
                         if c > size: 
                            encoded.append((count, [prev]*count))
                         else : 
                            if c+count <= (2**bits )- 1 : 
                               encoded[-1]=(c+count,color+[prev]*count)   
                            else : 
                                encoded.append((count,[prev]*count)) 
                  count = 1 
                  prev=pixel                
              else : 
                   if count  < (2**bits)-1 : 
                      count+= 1 
                   else :
                      encoded.append((count+size,[prev])) 
                      count =1 
                      prev=pixel 

    if count >= 3 :
         encoded.append((count+size,[prev])) 
    else : 
          if encoded == []:
                        encoded.append((count, [prev]*count))
          else :           
                c, color = encoded[-1]
                if c>size  :
                  encoded.append((count,[prev]*count))
                else     :
                  if c+count <= (2**bits)-1:
                       encoded[-1] = (c+count, color+[prev]*count)
                  else:
                        encoded.append((count, [prev]*count))

          #hexa_coding                  
    with open(file_name,"w") as file:
        hexa_encoded = "".join(map(lambda x: "{0:04x}".format(x[0])+"".join(map(lambda y: "{0:02x}".format(y), x[1])), encoded))
        """ hexa_encoded = ""
        for count, colors in count_list:
            hexa_encoded += "{0:04x}".format(count)
            for color in colors:
                hexa_encoded += "{0:02x}".format(color) """
        file.write(hexa_encoded) 
    rate = (1-(len(hexa_encoded)/2)/len(fimg))*100
    
    return hexa_encoded, rate   

image1_np = np.array([[0, 1, 0, 1, 0, 1], 
                    [1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0], 
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0]])*255
encoded, rate = RLE_encoding(image1_np, file_name='compressed1dah.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 38/36 = -5.56%

   
