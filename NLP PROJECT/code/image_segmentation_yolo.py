import os
import string
from pdf2image import convert_from_path
from pathlib import Path
import pytesseract
import detect_exp
from datetime import date
import pandas as pd
import cv2

def rfp_image_segmentation(pdf_file):
#   The model predicts the below classes(9 in total)
#    lab_dict = {0:'Footer', 1:'H1', 2:'H2', 3:'H3', 4:'H4', 5:'H5', 6:'Header', 7:'Image', 8:'P1', 9:'Table', 10:'table'}
    lab_dict = {0:'FullText', 1:'H1', 2 :'H2', 3:'H3', 4:'H4', 5:'P1', 6:'TOC', 7:'important_text', 8:'table'}
    today = date.today()
#   below method is used for sorting the text pieces in order
    def Sort(sub_li):
        sub_li.sort(key = lambda x: x[2])
        return sub_li

# getting the name of the file that came through API
    rfxpdf = "files_thruAPI/"+pdf_file
    filename = os.path.basename(str(rfxpdf))
    print(filename)

# creating a folder in the name of the file to store the pdf and the corresponding images(pages).
    folder_name = 'segmentation_run_data/rfx_pdf_folder/'+ str(today) +'/'+filename[:-4] + '/'
    predict_folder = 'segmentation_run_data/runs/detect/'+ str(today) +'/'+filename[:-4] + '/'

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(predict_folder):
        os.makedirs(predict_folder)

# converting the pages of the pdf to images and saving in the directory created above
    images = convert_from_path(rfxpdf, 500)
    for i, image in enumerate(images):
        fname = folder_name+str(i)+'.png'
        print(fname)
        image.save(fname, "PNG")

# running model prediction
    predictpath = detect_exp.detect(opt_source = folder_name, opt_project = predict_folder)
    print(predictpath)
    ###########################

# once the prediction algorithm runs on the images for predicting the different pieces of text, each image along with its prediction text file are read using the below code and converted to text.
    pages = {}
    for predicted_image in os.listdir(folder_name):
        print('Tesseract job started')
        count = 1
        if predicted_image.endswith('.png'):
            stemp = Path(predicted_image).stem
            img = cv2.imread(folder_name+predicted_image)
            dh, dw, _ = img.shape
#             label_path = predict_folder+'labels/'+stem+'.txt'
            label_path = str(predictpath)+'/labels/'+str(stemp)+'.txt'
            if os.path.exists(label_path):
                fl = open(label_path, 'r')
                data = fl.readlines()
                fl.close()

                # Getting the yolo coordinates to bounding box coordinates.
                boxes = []
                for dt in data:
                    lab, x, y, w, h = map(float, dt.split(' '))
                    l = int((x - w / 2) * dw)
                    r = int((x + w / 2) * dw)
                    t = int((y - h / 2) * dh)
                    b = int((y + h / 2) * dh)
                    if l < 0:
                        l = 0
                    if r > dw - 1:
                        r = dw - 1
                    if t < 0:
                        t = 0
                    if b > dh - 1:
                        b = dh - 1
                    cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
                    boxes.append([lab, l, t, r, b])
                boxes = Sort(boxes)

                # for dims,img,item in bounding_boxes:
                abc = string.ascii_lowercase + string.ascii_uppercase
                crops = {}
                i = 0
                for box in boxes:
                    lab,l,t,r,b = box
                    crops[str(int(lab))+abc[i]] = img[t-5:b+5,]
    #                 print(lab,l,t,r,b)
    #                 print(img[t:b,].shape)
                    cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
                    i+=1

# Extracing the text using pytesseract and placing the text in order for forming json structure.
                jsons = []
                count = 1
                tag = []
                df = pd.DataFrame(columns=['A','B'])
                for k,v in crops.items():
                    extracted = pytesseract.image_to_string(crops[k])
                    name = lab_dict[int(k[0])]
                    print(name)
                    print(type(name))
                    sortorder = count
                    dct = {"name": name,
                            "extracted": extracted,
                            "sortOrder": count}
                    count+=1
                    jsons.append(dct)
                    tag.append([name,extracted])
                    d1 = {'A': str(name)}
                    d2 = {'B': str(extracted)}
                    df.append(d1, ignore_index = True)
                    df.append(d2, ignore_index = True)
                x =pd.DataFrame(tag,columns=["name","extracted"])  
                x.to_csv("extracted.csv")
                df.to_csv("ex2.csv")

                pages['Page: '+str(stemp)] = jsons
            
            else:
                pages['Page: '+str(stemp)] = 'NA'
            print('page done' + str(stemp))
           
    return pages        

