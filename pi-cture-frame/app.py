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
    pilim = self.create_photo()

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

  def create_photo(self):
    photo = self.db.get_random_photo()
    pilim = Image.open(photo.path)
    if photo.rotation is not 0:
      pilim = pilim.rotate(-1*photo.rotation)

    # resize the image
    scale = float(self.w)/float(photo.width)
    if(photo.rotation in (90,270,-90,-270)):
      scale = float(self.h)/float(photo.height)

    # crop the image (if landscape)
    new_w = int(round(photo.width*scale))
    new_h = int(round(photo.height*scale))
    pilim = pilim.resize((new_w,new_h), Image.ANTIALIAS)
    if(photo.rotation not in (90,270,-90,-270)):
      v_margin = (new_h-self.h)/2
      pilim = pilim.crop((0,v_margin,self.w,v_margin+self.h))

    return pilim

  def update_picture(self):
    # Get the next picture
    pilim = self.create_photo()

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
