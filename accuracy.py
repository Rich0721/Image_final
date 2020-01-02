'''
Author: Rich, Wu
Date: 2019/12/30
Describe: Calculate accuracy by result.txt and demo.txt. 
'''



import os
from glob import glob
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

DEMO_XML_PATH = "./datasets/demo"
PATH = "./corrects"
RESULTS_FOLDER = "./results"


# Correct infomation are stored by xml file.
def xml_to_text(xml=None, textFile=None):

    tree = ET.parse(xml)
    root = tree.getroot()
    objects = root.findall("object")
    if len(objects) == 0:
        textFile.write("0")
    else:
        for obj in objects:
            name = obj.find("name").text
            textFile.write(name)
            textFile.write(" ")
    textFile.write("\n")

def run_change_file():
    for folder in range(10):
        textFile = open(os.path.join(PATH, str(folder) + ".txt"), 'w')
        xmls = glob(os.path.join(DEMO_XML_PATH, str(folder), "*.xml"))
        for f in xmls:
            xml_to_text(xml=f, textFile=textFile)
        textFile.close()

def read_file(File):
    
    demo = []
    with open(File, 'r') as f:
        line = f.readline()
        while line:
            line = line.split(' ')
            try:
                line.remove('\n')
            except ValueError:
                pass
            
            for i in range(len(line)):
                if line[i] == '0\n':
                    line[i] = '0'

            demo.append(line)
            line = f.readline()
    return demo

def calculate_accuracy():
    accuracy = []
    for folder in range(10):
        results = read_file(File=os.path.join(RESULTS_FOLDER, str(folder) + '.txt'))
        answers = read_file(File=os.path.join(PATH, str(folder) + '.txt'))
        TP = 0

        for result, answer in zip(results, answers):
            correct = True
            if len(result) == len(answer):
                sortResult = sorted(result)
                sortAnswer = sorted(answer)
                for i in range(len(result)):
                    if sortResult[i] != sortAnswer[i]:
                        correct = False
                        break
            else:
                correct = False
            if correct:
                TP += 1
        print("folder={}:{}".format(folder, TP/100))
        accuracy.append(TP/100)

    figure = plt.figure(figsize=(10,10))
    classes = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
    plt.bar(classes, accuracy)
    plt.xlabel("Folder")
    plt.ylabel("Accuracy")
    plt.title("Total Accuracy")
    plt.savefig("result1.jpg")

calculate_accuracy()
