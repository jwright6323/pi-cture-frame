# John C. Wright
# johnwright@eecs.berkeley.edu

import os
import Tkinter as tk
from PIL import Image,ImageTk

class Application(tk.Frame):

  def __init__(self):
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w,h))
    root.title('Pi-cture Frame')
    tk.Frame.__init__(self, root)
    self.grid()
    im = ImageTk.PhotoImage(Image.open("/tmp/pi-cture-frame/23622236440.jpg").crop((0,0,1024,800)))
    panel = tk.Label(root, image = im)
    panel.image = im
    panel.pack(side = "bottom", fill="both", expand="yes")

app = Application()
app.mainloop()
