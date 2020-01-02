'''
Author: Rich, Wu
Date: 2019/12/30
Describe: Product more train and test image. Respectively, remove and filled up background.
'''


import os
import cv2
from glob import glob
import numpy as np
import xml.etree.ElementTree as ET

class productTestImage(object):

    def __init__(self, datasetPath="./datasets", storageDataset="JPEGImages", annotationPath="Annotations"):
        self.datasetPath = datasetPath 
        self.background = ['4710126041004_background', '4710126045460_background', '4714431053110_background'] 
        self.foreground = ['4710126041004_foreground', '4710126045460_foreground', '4714431053110_foreground']
        self.storageDataset = storageDataset
        self.classeifier = ['4710126041004', '4710126045460', '4714431053110']
        self.annotationPath = annotationPath

    
    def prettyXml(self, element, indent, newline, level = 0): 
        if element:  
            if element.text == None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    
        temp = list(element) 
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1): 
                subelement.tail = newline + indent * (level + 1)
            else:  
                subelement.tail = newline + indent * level
            self.prettyXml(subelement, indent, newline, level = level + 1)

    def productXMLFile(self, productNumber, bnd, fileName):
        annotation = ET.Element("annotation")
        filename = ET.SubElement(annotation, "filename")
        filename.text = fileName
        path = ET.SubElement(annotation, "path")
        path.text = (os.path.abspath(fileName))

        source = ET.SubElement(annotation, "source")
        database = ET.SubElement(source, "database")    
        database.text = "Unknown"

        size = ET.SubElement(annotation, "size")
        width = ET.SubElement(size, "width")
        height = ET.SubElement(size, "height")
        depth = ET.SubElement(size, "depth")
        width.text = "1920"
        height.text = "1080"
        depth.text = "3"

        segmented = ET.SubElement(annotation, "segmented")
        segmented.text = "0"
        for j in range(productNumber):
            objects = ET.SubElement(annotation, "object")
       
            name = ET.SubElement(objects, "name")
            pose = ET.SubElement(objects, "pose")
            truncated = ET.SubElement(objects, "truncated")
            difficult = ET.SubElement(objects, "difficult")
            name.text = bnd[j][0]
            pose.text = "Unspecified"
            truncated.text = "0"
            difficult.text = "0"
            bndbox = ET.SubElement(objects, "bndbox")
    
            
            XMIN = ET.SubElement(bndbox, "xmin")
            YMIN = ET.SubElement(bndbox, "ymin")
            XMAX = ET.SubElement(bndbox, "xmax")
            YMAX = ET.SubElement(bndbox, "ymax")
            XMIN.text = str(bnd[j][1])
            YMIN.text = str(bnd[j][2])
            XMAX.text = str(bnd[j][3])
            YMAX.text = str(bnd[j][4])

        tree = ET.ElementTree(annotation)
        #tree.write("test.xml", encoding='UTF-8')
        root = tree.getroot()
        self.prettyXml(root, '\t', '\n')
        tree.write(os.path.join(self.datasetPath ,self.annotationPath, fileName[:-4] + ".xml"), encoding='UTF-8')

    # Product One object in the background image
    # By productNumber: how many do need to product objects
    # choice = 0 : 4710126041004
    # choice = 1 : 4710126045460
    # choice = 2 : 4714431053110
    def produceObject(self, productNumber, i):

        foregroundImagesList = []
        foregroundRandomList = []
        bndbox = []

        choice = np.random.randint(0,3)
        backgroundImages = glob(os.path.join(self.datasetPath, self.background[choice], "*.png"))
        choice = np.random.randint(0,3,productNumber)
        for c in choice:
            foregroundImagesList.append(glob(os.path.join(self.datasetPath, self.foreground[c], "*.png")))

        backgroundRandom = np.random.randint(0, len(backgroundImages))
        for j in range(productNumber):
            foregroundRandomList.append(np.random.randint(0, len(foregroundImagesList[j])))

        
        background = cv2.imread(backgroundImages[backgroundRandom])

        for j in range(productNumber):
            foreground = cv2.imread(foregroundImagesList[j][foregroundRandomList[j]])
            
            ymin = np.random.randint(0, background.shape[0] -  foreground.shape[0])
            xmin = np.random.randint(0, background.shape[1] -  foreground.shape[1])

            ymax = int(ymin + foreground.shape[0])
            xmax = int(xmin + foreground.shape[1])
            
            bndbox.append([self.classeifier[choice[j]],xmin, ymin, xmax, ymax])
          
            
            for y in range(ymin, ymax, 1):
                for x in range(xmin, xmax, 1):
                    
                    if foreground[y-ymin,x-xmin, 0] != 0 and foreground[y-ymin,x-xmin,1] != 0 and foreground[y-ymin,x-xmin,2] != 0:
                        background[y,x] = foreground[y-ymin,x-xmin]
            
  
        cv2.imwrite(os.path.join(self.datasetPath ,self.storageDataset ,str(i) + ".jpg"), background)
        
        self.productXMLFile(productNumber=productNumber, bnd=bndbox, fileName=str(i)+".jpg")

demo_path = "demo"
 

for folder in range(0,10):
    path = os.path.join(demo_path, str(folder))
    path1 = os.path.join('./datasets',demo_path, str(folder))
    if not os.path.exists(path1):
        os.mkdir(path1)
    x = productTestImage(storageDataset=path, annotationPath=path)
    
    for i in range(100):
        objectNumbers = np.random.randint(low=0, high=4)
        x.produceObject(objectNumbers, i)
        print("{}/{}".format(path1,i))
    