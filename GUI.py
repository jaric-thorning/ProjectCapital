import datetime
from Tkinter import *
import tkMessageBox
import tkFileDialog
import random
import time

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
        self._width = 900
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

    def add_line(self, x0, y0, x1, y1, fill = None):
        new_line = Draw_line(x0, y0, x1, y1)
        if fill != None:
            new_line.set_fill(fill)
        else:
            new_line.set_fill("blue")
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

    def load_historic(self, share_temp, share_historic):
        self.clear()
        print share_temp.get_name()
        i = 0
        max_value = float(0.0)
        firstvalue = 0
        for day in share_historic:
            if float(day["Close"]) > max_value: max_value = float(day["Close"])
        print "Max Value: " + str(max_value)
        
        multiplyer = (self._canvas_height - 10)/max_value
        print "Multipler: " + str(multiplyer)
        for day in reversed(share_historic):
            
            
            #print "n: " + str(self._canvas_height - float(day["Close"]))
            #print float(day["Close"])

            if i != 0:
                if float(day["Close"]) < firstvalue:
                    self.add_line(i,self._canvas_height,i,self._canvas_height - float(day["Close"])*multiplyer, "red")
                else:
                    self.add_line(i,self._canvas_height,i,self._canvas_height - float(day["Close"])*multiplyer, "green")
                    
            else:
                self.add_line(i,self._canvas_height,i,self._canvas_height - float(day["Close"])*multiplyer)
                
            firstvalue = float(day["Close"])
            i += 1
            
        
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
        data = Frame(master)

        #ENTER LABEL   
        symbol = Label(data,text = "Enter Symbol:").pack(side=LEFT)

        #ENTER ENTRY
        self.date_entry = Entry(data)
        self.date_entry.pack(side=LEFT, fill = BOTH, expand = True)

        #ENTER BUTTON
        Button(data,text = "Enter", command = self.update_now).pack(side=LEFT)
        
        self.t_symbol = StringVar()
        self.t_close = StringVar()
        self.t_change = StringVar()
        

        self.share_change_color = StringVar()
        self.share_change_color.set("black")
        
        self.share_name = Label(data, textvariable = self.t_symbol)
        self.share_close = Label(data, textvariable = self.t_close)
        self.share_change = Label(data, textvariable = self.t_change, fg = self.share_change_color.get())

        self.share_name.pack(side=LEFT, padx = 5)
        self.share_close.pack(side=LEFT, padx = 5)
        self.share_change.pack(side=LEFT, padx = 5)

        data.pack(anchor = 'sw', padx = 5, pady = 5)

    def update_now(self):
        print "updating"
        share_string = str(self.date_entry.get()) + ".AX"
        share_temp = share.Stock_Info(share_string)
        p_date = '2013-01-01'
        t_date = time.strftime("%Y-%m-%d")
        share_historic = share_temp.get_historical1(p_date,t_date)
        self._boss.clear()
        self._boss.load_historic(share_temp, share_historic)
        self._boss.draw()

        share_temp.update_quote()
        self.t_symbol.set(share_temp.get_symbol())
        print share_temp.get_name()
        self.t_close.set(share_temp.get_quote())
        print share_temp.get_quote()
        self.t_change.set(share_temp.get_change() + "%")
        print share_temp.get_change()

        change = float(share_temp.get_change())
        if change < 0:
            self.share_change.config(fg = "red")
        elif change > 0:
            self.share_change.config(fg = "green")
        else:
            self.share_change.config(fg = "black")
        self.share_change.pack()
              
def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
