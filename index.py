import os
import re
import psutil
from time import process_time 
import csv

# Start time
startTime = process_time() 

#variable for unique list of words that was replace
uniqueWord = []
#variable for no. of times a word replace
wordFrequency = []

def createRequiredWordDictionary(enWord, frWord):
    """function to create french dictionary for only find words """
    dictionary_dict = {}  
    if(enWord == frWord.split(",")[0]):
        dictionary_dict[enWord] = frWord.split(",")[1]
    return dictionary_dict    

def readFile(file):
    """ read convert english words text file """
    findWordFile = open(file, "r")
    enlines = findWordFile.read()
    listOfLines = enlines.splitlines()
    return listOfLines

def freqency(content,findword):
    """Function used to find frequency of a word in given text"""
    freqList={}
    for key in findword:
        if content.count(key):
            freqList[key]= content.count(key)
            uniqueWord.append(key)
    return freqList


# read  content text
file = open("t8.shakespeare.txt", "r")
content = file.read()
#read find words file
listOfenLines=readFile("find_words.txt")
#read french dictionary file
listOffrLines=readFile("french_dictionary.csv")

findWordDict={}
for sub in list(map(createRequiredWordDictionary, listOfenLines, listOffrLines)):
    for key in sub:
        findWordDict[key]=sub[key]

wordFreq=freqency(content,listOfenLines)

for key,value in wordFreq.items():
    replacetxt=re.sub(key, findWordDict[key], content)
    content=replacetxt
    wordFrequency.append([key,findWordDict[key],value])

# write  new created text file after change english into french words
file_handle = open("t8.shakespeare.translate.txt", "w")
file_handle.write(content)
file_handle.close()

# Stop the time 
stopTime = process_time() 

print(uniqueWord)

# print(wordFrequency)

timeToProcress=stopTime-startTime

memoryUsed=psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

# save time to process and memory into performance.txt
file_handle = open("performance.txt", "w")
file_handle.write("Time to process: "+str(timeToProcress)+" seconds\nMemory used: "+str(memoryUsed)+" MB")
file_handle.close()

#Create csv file for store english word with its french word and also frequency count
with open('frequency.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["English word", "French word", "Frequency"])
    for element in wordFrequency:
        writer.writerow(element)
