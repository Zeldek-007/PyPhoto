#!/usr/bin/python3

import tkinter as tk ; import tkinter.filedialog
import PIL ; import PIL.ImageTk

#Define root window.
root = tk.Tk()

#Init PIL Image source.
#srcImage=PIL.Image.open(tk.filedialog.askopenfilename())    #DO NOT DELETE, BUT COMMENTED OUT WHILE TESTING FOR EFFICIENCY
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

#Create core plugins. :)
class plugin(tk.Button):

    #Function called by a button bound to it as a command by clickToBind().
    def clickExec(self):
        print("Hello'z.")

    #Function called when the plugin button is pressed. Should bind the appropriate actions to their keys/mouse-buttons and
    #return a dictionary of keys for what parameters of the plugin are supported for adjustment.
    def clickToBind(self)->dict:
        canvas.bind("<Button-1>",self.clickExec)
        return []

    def __init__(self,name="NAME",icon="img/default.png"):
        self.name = name
        self.icon = PIL.ImageTk.PhotoImage(PIL.Image.open(icon))
        #
        super().__init__(root,image=self.icon,command=lambda:self.clickToBind())

    



testButton = plugin()


#Add a toolbox. :)
toolFrame = tk.Frame(root)

#Populate the toolbox.

testButton.grid(row=0,column=0)

#TEST WORKED

# for plugin in range(10):
#     newButton = tk.Button(toolFrame)
#     newButton.grid(row=0,column=plugin)

###########  

toolFrame.grid(row=0,column=0)

root.mainloop()