'''
Author: Rich, Wu
Date: 2019/12/30
Describe: Preprocess images and xml file.
'''


import os
import os.path as osp
import cv2
import numpy as np
from glob import glob
import xml.etree.ElementTree as ET
import shutil

DATASETS = "./datasets/4714431053110"
ORIGINAL_PATH = "./datasets/JPEGImages"
ANNOTATION_PATH = "./datasets/Annotations"
FOREGROUND_PATH = "./datasets/4714431053110_foreground"
BACKGROUND_PATH = "./datasets/4714431053110_background"

if not osp.exists(FOREGROUND_PATH):
    os.mkdir(FOREGROUND_PATH)
if not osp.exists(BACKGROUND_PATH):
    os.mkdir(BACKGROUND_PATH)

def foregrond(fileName, xmin, ymin, xmax, ymax, storagePath):
    print("remove file name background:{}".format(fileName))
    image = cv2.imread(fileName)
    mask = np.zeros(image.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    h = ymax - ymin
    w = xmax - xmin

    rect = (xmin, ymin, w, h)
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = image*mask2[:,:,np.newaxis]
    img = img[ymin:ymax, xmin:xmax]
    
    cv2.imwrite(storagePath, img)

def background(image, xmin, ymin, xmax, ymax, storagePath):
    originalImg = cv2.imread(image)

    for i in range(ymin, ymax, 1):
        for j in range(xmin, xmax, 1):
            originalImg[i,j] = originalImg[i-1,j-1]
               
    
    cv2.imwrite(storagePath, originalImg)

def readXmlFile(fileName):

    xml = ET.parse(fileName)
    root = xml.getroot()
    
    objects = root.find("object") # find tag: object in annotation
    bndbox = objects.find("bndbox") # find tag bndbox in object

    # find xmin, ymin, xmax, ymax
    xmin = int(bndbox.find("xmin").text)
    ymin = int(bndbox.find("ymin").text)
    xmax = int(bndbox.find("xmax").text)
    ymax = int(bndbox.find("ymax").text)
    
    return xmin, ymin, xmax, ymax

def step_foreground():
    cameras = os.listdir(DATASETS)
    i = 1689
    for camera in cameras:
        cameraPath = osp.join(DATASETS, camera)
        folderList = os.listdir(cameraPath)
        for folder in folderList:
            images = glob(osp.join(cameraPath, folder, "*.png"))
            xmls = glob(osp.join(cameraPath, folder, "*.xml"))

            for image, xml in zip(images, xmls):
                #xmin, ymin, xmax, ymax = readXmlFile(xml)
                #foregrond(image, xmin, ymin, xmax, ymax, osp.join(FOREGROUND_PATH,str(i)+".png"))
                shutil.copy(src=image, dst=osp.join(ORIGINAL_PATH, str(i)+".jpg"))
                shutil.copy(src=xml, dst=osp.join(ANNOTATION_PATH , str(i) + ".xml"))
                i += 1

def step_background():
    cameras = os.listdir(DATASETS)
    i = 0
    for camera in cameras:
        cameraPath = osp.join(DATASETS, camera)
        folderList = os.listdir(cameraPath)
        for folder in folderList:
            images = glob(osp.join(cameraPath, folder, "*.png"))
            xmls = glob(osp.join(cameraPath, folder, "*.xml"))

            for image, xml in zip(images, xmls):
                xmin, ymin, xmax, ymax = readXmlFile(xml)
                background(image, xmin, ymin, xmax, ymax, osp.join(BACKGROUND_PATH,str(i)+".png"))
                i += 1
step_foreground()
#step_background()