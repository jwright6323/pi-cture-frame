# John C. Wright
# johnwright@eecs.berkeley.edu

import os
import Tkinter as tk
from PIL import Image,ImageTk
from photo_db import *

class Application(tk.Frame):

  picture_delay_s = 15
  db = PhotoDB()

  def __init__(self):
    # Start creating the Tk app
    self.root = tk.Tk()
    self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
    self.root.overrideredirect(1)
    self.root.geometry("%dx%d+0+0" % (self.w,self.h))
    self.root.title('Pi-cture Frame')

    # Create the first picture
    path,rot = self.db.get_random_photo()
    pilim = Image.open(path)
    if rot is not 0:
      pilim = pilim.rotate(-1*rot)

    # Crop the image and center using thumbnail
    pilim.thumbnail((self.w,self.h))

    # Convert to Tk
    im = ImageTk.PhotoImage(pilim)

    # Add to panel
    self.panel = tk.Label(self.root, image = im)

    # Prevent garbage collecting
    self.panel.image = im

    # Fullscreen
    self.panel.pack(side = "bottom", fill="both", expand="yes")

    # Initialize
    tk.Frame.__init__(self, self.root)
    self.grid()

  def update_picture(self):
    # Get the next picture
    path,rot = self.db.get_random_photo()
    pilim = Image.open(path)
    if rot is not 0:
      pilim = pilim.rotate(-1*rot)

    # Crop the image and center using thumbnail
    pilim.thumbnail((self.w,self.h))

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
