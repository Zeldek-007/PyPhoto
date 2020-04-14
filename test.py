#!/usr/bin/python

import numpy , PIL
import PIL.Image


pathPrefix = "/home/zeldek/Pictures/"
imagePath = "blue.png"
fullPath = pathPrefix+imagePath

srcImage = PIL.Image.open(fullPath)

#Prints.
#print(numpy.asarray(srcImage))    #WORKS
'''
for line in numpy.asarray(srcImage):
    #print(line)
    for pixel in line:
        print(pixel)
'''
#--#

#TEST TEST
array = numpy.asarray(srcImage)
#MUST SET WRITABLE
print(array.flags)

def adjust_saturation(r,g,b):

            #Init steppers.
            lineNumber = -1
            pixelNumber = -1

            imageAsArray = numpy.asarray(srcImage)
            #Python hates modifying over an iteration.
            imageAsArrayToIterate = imageAsArray
            for line in imageAsArrayToIterate:
                lineNumber += 1
                for _ in line:  #for pixel in line
                    pixelNumber += 1

                    #Test.
                    print(imageAsArray)
                    print(imageAsArray[lineNumber])
                    print(imageAsArray[lineNumber][pixelNumber])

                    #Finally do something.  DOESN'T WORK - ASSIGNMENT READ-ONLY???
                    imageAsArray[lineNumber][pixelNumber][0] = r  #r
                    imageAsArray[lineNumber][pixelNumber][1] = g  #g
                    imageAsArray[lineNumber][pixelNumber][2] = b  #b

            print(imageAsArray)

            




#adjust_saturation(0,0,0)