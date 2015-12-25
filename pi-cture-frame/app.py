# John C. Wright
# johnwright@eecs.berkeley.edu

import os
import Tkinter as tk
from PIL import Image,ImageTk
from photo_db import *

class Application(tk.Frame):

  picture_delay_s = 10
  db = PhotoDB()

  def __init__(self):
    # Start creating the Tk app
    self.root = tk.Tk()
    self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
    self.root.overrideredirect(1)
    self.root.geometry("%dx%d+0+0" % (self.w,self.h))
    self.root.title('Pi-cture Frame')
    self.root.configure(cursor="none")

    # Create the first picture
    photo = self.db.get_random_photo()
    pilim = Image.open(photo.path)
    if photo.rotation is not 0:
      pilim = pilim.rotate(-1*photo.rotation)

    # Crop the image and resize
    scale = float(self.w)/float(photo.width)
    if(photo.rotation in (90,270,-90,-270)):
      scale = float(self.h)/float(photo.height)

    pilim = pilim.resize((int(round(photo.width*scale)),int(round(photo.height*scale))), Image.ANTIALIAS)
    if(photo.rotation not in (90,270,-90,-270)):
      pilim = pilim.crop((0,0,self.w,self.h))

    # Convert to Tk
    im = ImageTk.PhotoImage(pilim)

    # Add to panel
    self.panel = tk.Label(self.root, image = im)
    self.panel.configure(background="black")

    # Prevent garbage collecting
    self.panel.image = im

    # Fullscreen
    self.panel.pack(side = "bottom", fill="both", expand="yes")

    # Initialize
    tk.Frame.__init__(self, self.root)
    self.grid()

  def update_picture(self):
    # Get the next picture
    photo = self.db.get_random_photo()
    pilim = Image.open(photo.path)
    if photo.rotation is not 0:
      pilim = pilim.rotate(-1*photo.rotation)

    # Crop the image and resize
    scale = float(self.w)/float(photo.width)
    if(photo.rotation in (90,270,-90,-270)):
      scale = float(self.h)/float(photo.height)

    pilim = pilim.resize((int(round(photo.width*scale)),int(round(photo.height*scale))), Image.ANTIALIAS)
    if(photo.rotation not in (90,270,-90,-270)):
      pilim = pilim.crop((0,0,self.w,self.h))

    # Convert to Tk
    im = ImageTk.PhotoImage(pilim)

    # Update panel
    self.panel.configure(image = im)

    # Prevent garbage collecting
    self.panel.image = im

    # Keep looping
    self.root.after(1000*self.picture_delay_s, self.update_picture)

if __name__=="__main__":
  app = Application()
  # Start the update loop
  app.root.after(1000*app.picture_delay_s, app.update_picture)
  app.mainloop()
