# John C. Wright
# johnwright@eecs.berkeley.edu

import os
import Tkinter as tk

class Application(tk.Frame):

  def __init__(self):
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w,h))
    tk.Frame.__init__(self, root)
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    self.quitButton = tk.Button(self, text='Quit', command=self.quit)
    self.quitButton.grid()

app = Application()
app.master.title('Sample application')
app.mainloop()
