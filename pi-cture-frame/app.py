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
    img = "23289806914"
    pilim = Image.open("/tmp/pi-cture-frame/%s.jpg" % img).rotate(0)
    pilim.thumbnail((1024,800))
    im = ImageTk.PhotoImage(pilim)
    panel = tk.Label(root, image = im)
    panel.image = im
    panel.pack(side = "bottom", fill="both", expand="yes")

app = Application()
app.mainloop()
