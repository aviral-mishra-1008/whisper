from django.shortcuts import render
import os
import numpy as np
from PIL import Image
import random
# Create your views here.

def home(request):
    try:
        try:
            os.remove('temp/output.png')
        except:
            pass
        return render(request,'home.html')
    except:
        return render(request,"error.html")

def encrypt(request):
    try:
        if request.method == 'POST':
            message = request.POST.get('message')
            image = request.FILES['image']
            
            # Save the image to the media folder
            image_path = os.path.join("temp", image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            output_path = os.path.join("temp","output.png")
            Encode(image_path,message,output_path)

            params = {}
            params['path'] = os.path.join('/media','output.png')
            os.remove(image_path)
            return render(request,'download.html',params)    
        
        return render(request,'encrypt.html')
    except:
        return render(request,"error.html")

def decrypt(request):
    try:
        if request.method == 'POST':
            image = request.FILES['image']
            
            # Save the image to the media folder
            imageName = image.name+str(random.randint(10000,999999))
            image_path = os.path.join("temp", imageName)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            message = Decode(image_path)
            print(message)
            params = {}
            params['message'] = message
            os.remove(image_path)
            return render(request,'message.html',params)
        return render(request,'decrypt.html')
    except:
        return render(request,'error.html')

#Helper Functions
def Encode(src_path, message, dest_path):

    #Opening the image and counting pixels while also checking the mode
    img = Image.open(src_path, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    n = 3

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "$$82"
    

    #Converting message to binary
    temp = []

    for i in message:
      temp.append(format(ord(i), "08b"))

    b_message = ''.join(temp)
    req_pixels = len(b_message)

    #encoding the data
    if req_pixels > total_pixels:
      print("ERROR: Larger Image Needed!!")

    else:
      index=0
      for p in range(total_pixels):
          for q in range(0, n):
              if index < req_pixels:
                  array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                  index += 1
        
    #Saving the encoding
    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest_path)

def Decode(src_path):

    img = Image.open(src_path, 'r')
    array = np.array(list(img.getdata()))
    n = 3

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, n):
            hidden_bits += (bin(array[p][q])[2:][-1])

    temp = []
    for i in range(0,len(hidden_bits),8):
        temp.append(hidden_bits[i:i+8])

    message = ""

    for i in range(len(temp)):
        if message[-4:] == "$$82":
            break
        else:
          message += chr(int(temp[i], 2))

    if "$$82" in message:
        message = message[:-4]
    else:
        message = "No Hidden Message Found"
    
    return message