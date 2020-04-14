#!/usr/bin/python3
# MrR Branch example

import tkinter as tk ; import tkinter.filedialog
import PIL ; import PIL.ImageTk
#NEW DEPENDENCY
import numpy

#Define root window.
root = tk.Tk()

#Init PIL Image source.
#DO NOT DELETE, BUT COMMENTED OUT WHILE TESTING FOR EFFICIENCY.
srcImage=PIL.Image.open(tk.filedialog.askopenfilename())
#srcImage=PIL.Image.open("/home/zeldek/Pictures/ship.jpg")
#Initialize PIL's tkinter-compatible PhotoImage to hold our base image.
imageIn = PIL.ImageTk.PhotoImage(image=srcImage)

#Create a frame holding image layers.
layersFrame = tk.Frame(root)
layersFrame.grid(row=1,column=0)

#Create a "label" holding the source image.
imLayer = tk.Label(layersFrame,image=imageIn)
imLayer.grid(row=0,column=0)

#Create the canvas we'll draw on.
canvas = tk.Canvas(layersFrame,width=srcImage.width,height=srcImage.height)
canvas.grid(row=0,column=0)
#LOAD IMAGE ONTO CANVAS
canvas.create_image(srcImage.width/2,srcImage.height/2,image=imageIn)

#Add a toolbox. :)
toolFrame = tk.Frame(root)
toolFrame.grid(row=0,column=0)

#Create a global, self-managing dictionary/database to persistently modify 
#values for plugins.
class database():
    
    # While the use of this __init__ is 
    #not currently intended to be used, it
    # allows a default set of keys to be imported into the database.
    #Perhaps preferences for different plugins could be stored in a file 
    # and recalled here?
    def __init__(self,defaultStore:dict=[]):
        self.keys:dict = defaultStore
    
    def addPluginKeyStore(self,keyStore:dict=[]):
        self.keys += keyStore 

    def addKeyStore(self,keyStore,key:dict):
        self.keys[keyStore] += key
    
    def modKey(self,keyStore,key,newValue):
        self.keys[keyStore][key]=newValue

propDB = database()

#Create core plugin system.
class plugin(tk.Button):

		def __init__(self,name="NAME",icon="img/default.png",
			bindToButton:bool=True):
			self.name = name
			self.icon = PIL.ImageTk.PhotoImage(PIL.Image.open(icon))
			#Use this attribute to control data such as 
                        #points of a polygon.
			self.memory = []
			super().__init__(toolFrame,image=self.icon,
				command=lambda:canvas.bind( "<Button 1>" , self.toolAct ) )
			#If tool is meant to act immediately on the whole 
                        #image, bindToButton=False.
			if not bindToButton:
				self.configure(command="")
				self.bind("<Button 1>",self.toolAct)

		#Override function in subclasses. 
                #MUST HAVE BOTH SELF & EVENT ARGUMENTS AT MINIMUM!!!
		def toolAct(self,event):
			print("Hello from __init__!")



#EXAMPLE PLUGIN
class lineTool(plugin):
    
    def __init__(self):
        super().__init__("LINE-TOOL")

    
    def toolAct(self,event):

        self.memory += [(event.x,event.y)]

        if len(self.memory) == 2:
            canvas.create_line(self.memory[0],self.memory[1])
            self.memory=[]  #Clear mem.


#HUGE THANKS TO
#https://
#stackoverflow.com/questions/9886274
#/how-can-i-convert-canvas-content-to-an-image   
# "Use Pillow to convert from  Postscript to PNG"

#SAVE PLUGIN
class saveTool(plugin):

    def __init__(self):
        super().__init__("SAVE-TOOL","img/default.png",False)

    def toolAct(self,event):
        #Ask what to save the file as!
        fileName = tk.filedialog.asksaveasfilename()
        #DEBUG
        print(fileName)
        #Create a version of the canvas that PIL can use.
        canvas.postscript(file=fileName)
        img = PIL.Image.open(fileName)
        img.save(fileName)

#COLOR SUBTRACTOR/ADDER PLUGIN
class hueTool(plugin):

    def __init__(self):
        super().__init__("HUE-TOOL","img/default.png",False)

    def adjust_saturation(self,r,g,b):

                #Init steppers.
                lineNumber = -1
                

                imageAsArray = numpy.array(srcImage)
                #Python hates modifying over an iteration.
                imageAsArrayToIterate = imageAsArray
                for line in imageAsArrayToIterate:
                    lineNumber += 1
                    pixelNumber = -1
                    for _ in line:  #for pixel in line
                        pixelNumber += 1

                        '''
                        #Test.
                        print(pixelNumber)

                        #Test.
                        print(imageAsArray)
                        print(imageAsArray[lineNumber])
                        '''

                        #Modify each channel individually, making sure not to go out of bounds.
                        channel = 0
                        for saturationAdjust in [r,g,b]:
                            if imageAsArray[line][pixelNumber][channel] + saturationAdjust < 0: imageAsArray[line][pixelNumber][channel] = 0
                            elif imageAsArray[line][pixelNumber][channel] + saturationAdjust > 255: imageAsArray[line][pixelNumber][channel] = 255
                            else: imageAsArray[line][pixelNumber][channel] += saturationAdjust

                return imageAsArray

    def toolAct(self,event):

        propFrame = tk.Frame()
        propFrame.grid(row=2,column=0,columnspan=3)
        
        #Create sliders for RGB manipulation.
        r_slider = tk.Scale(propFrame, from_=-255, to=255)
        r_slider.grid(row=0,column=0)

        g_slider = tk.Scale(propFrame, from_=-255, to=255)
        g_slider.grid(row=1,column=0)

        b_slider = tk.Scale(propFrame, from_=-255, to=255)
        b_slider.grid(row=2,column=0)
        



#Load plugins here.

line = lineTool()
line.grid(row=0,column=1)

save = saveTool()
save.grid(row=0,column=2)

hue = hueTool()
hue.grid(row=0,column=3)

#Start.
root.mainloop()
