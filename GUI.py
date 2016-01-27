import datetime
from Tkinter import *
import tkMessageBox
import tkFileDialog
import random

import share

class App(object):
    '''Controls the running of the app'''
    def __init__(self, master = None):
        '''A controller class that runs the app
        Constructor: Controller(object)'''

        ## Graphics
        #TOP WINDOW
        self._master = master
        self._master.resizable(FALSE, FALSE)
        self._height = 300
        self._width = 500
        self._master.minsize(self._width, self._height)
        self._master.title("Project Capital")
        
        self._canvas_height = self._height - 50
        self._canvas_width = self._width
        self.options = OptionsFrame(master, self)
        self.options.pack(side = TOP, fill = X)

        self.canvas = Canvas(master, bg = "black", height = self._canvas_height, width = self._canvas_width)
        self.canvas.pack(side = TOP, fill = BOTH, expand = False)

        #File Button

        # create a toplevel menu
        menubar = Menu(master)
        menubar.add_command(label="Hello!")
        menubar.add_command(label="Quit!")
        
        # display the menu
        master.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open File")
        filemenu.add_command(label="Save File")
        filemenu.add_separator()
        filemenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=filemenu)

        ## Ops

        self._drawlist = []
        self.draw_example_graph()
        self.draw()

    
    def clear(self):
        self._drawlist = []
    def draw(self):
        self.canvas.delete(ALL)
        for draw in self._drawlist:
            self.canvas.create_line(draw.x0, draw.y0, draw.x1, draw.y1, fill = draw.get_fill())
        self.canvas.pack()

    def add_line(self, x0, y0, x1, y1):
        new_line = Draw_line(x0, y0, x1, y1)
        new_line.set_fill("red")
        self._drawlist.append(new_line)
        
    def draw_rect(self):
        self.add_line(-10,10,10,100)
        self.add_line(10,100,100,100)
        self.add_line(100,100,100,10)
        self.add_line(100,10,10,10)

    def draw_example_graph(self):
        r = random.randrange(0,self._canvas_height)
        randsum = 0
        for i in range(0, self._canvas_width):
            randnum = random.randrange(-1000,1000)
            r = r + randnum/100.00 - ((self._canvas_height + r/2)/self._canvas_height) + 1
            
            if r < 0: r = 0
            self.add_line(i,self._canvas_height,i,self._canvas_height - r)
    
        
class Draw_line(object):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.fill = "black"
    def set_fill(self, fill):
        self.fill = fill
        return
    def get_fill(self):
        return self.fill

class OptionsFrame(Frame):
    """Lower level GUI interface responsible for the interface to
    interact with the user.
    """
    def __init__ (self, master, boss):

        self._master = master
        self._boss = boss
        Frame.__init__(self, master)
        data = Frame(master, bg = "green")

        #data   
        Label(data,text = "Enter Symbol:").pack(side=LEFT)

        self.date_entry = Entry(data)
        self.date_entry.pack(side=LEFT, fill = BOTH, expand = True)
        
        Button(data,text = "Enter", command = self.update).pack(side=LEFT)
        data.pack(anchor = 'sw', padx = 5, pady = 5)

    def update(self):
        print "updating"
        self._boss.clear()
        self._boss.draw_example_graph()
        self._boss.draw()
                
def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
