#!/usr/bin/python3

#Comments attempt to adhere to a limit of 79 columns as per PEP8.
#Otherwise, PEP regulations are entirely ignored because they're nonsensical.


import tkinter as tk ; import tkinter.filedialog
import PIL ; import PIL.ImageTk

#Define root window.
root = tk.Tk()

#Init PIL Image source.
#DO NOT DELETE, BUT COMMENTED OUT WHILE TESTING FOR EFFICIENCY.
#srcImage=PIL.Image.open(tk.filedialog.askopenfilename())
srcImage=PIL.Image.open("/home/zeldek/Pictures/ship.jpg")
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
    
    # While the use of this __init__ is not currently intended to be used, it
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

#Add a PROPERTIES frame to adjust plugin settings. Pls nu crash. :(
class propFrame(tk.Frame):

    def __init__(self):
        super().__init__(root)

    

propertyFrame = propFrame()
#TEMPLATE

#Create core plugins. :)
class plugin(tk.Button):

    def __init__(self,name="NAME",icon="img/default.png"):
        self.name = name
        self.icon = PIL.ImageTk.PhotoImage(PIL.Image.open(icon))
        #Use this attribute to control data such as points of a polygon.
        self.memory = []
        super().__init__(toolFrame,image=self.icon,command=lambda:canvas.bind( "<Button 1>" , self.toolAct ) )
    
    #OVERRIDE THIS FUNCTION WITH YOUR OWN IMPLEMENTATION. :)    #MUST HAVE BOTH SELF & EVENT ARGUMENTS AT MINIMUM!!!
    def toolAct(self,event):
        print("Hewwo from __init__!")


#EXAMPLE PLUGIN
class lineTool(plugin):
    
    def __init__(self):
        super().__init__("LINE-TOOL")

    
    def toolAct(self,event):

        self.memory += [(event.x,event.y)]

        if len(self.memory) == 2:
            canvas.create_line(self.memory[0],self.memory[1])
            self.memory=[]  #Clear mem.

#

#HUGE THANKS TO
#https://stackoverflow.com/questions/9886274/how-can-i-convert-canvas-content-to-an-image   
# "Use Pillow to convert from  Postscript to PNG"

#SAVE PLUGIN
class saveTool(plugin):

    def __init__(self):
        super().__init__("SAVE-TOOL")
    
    def toolAct(self,event):
        #Ask what to save the file as!
        fileName = tk.filedialog.asksaveasfilename()
        #DEBUG
        print(fileName)
        #Create a version of the canvas that PIL can use.
        canvas.postscript(file=fileName)
        img = PIL.Image.open(fileName)
        img.save(fileName)



#Load plugins here.

base = plugin()
base.grid(row=0,column=0)

line = lineTool()
line.grid(row=0,column=1)

save = saveTool()
save.grid(row=0,column=2)

#


#Populate the toolbox.

#TEST WORKED

# for plugin in range(10):
#     newButton = tk.Button(toolFrame)
#     newButton.grid(row=0,column=plugin)

###########  

root.mainloop()