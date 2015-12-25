# John C. Wright
# johnwright@eecs.berkeley.edu

import sqlite3
import flickrapi
import urllib
import os
import errno

class PhotoDB:

  api_key = u'e9495a30dea5740bb1da96c1aa60e954'
  api_secret = u'bde6f9256b82f199'
  user_id = '138731132@N05'
  photo_dir = '/tmp/pi-cture-frame/'
  db = photo_dir + 'photos.db'

  @classmethod
  def flickr():
    flickrapi.FlickrAPI(PhotoDB.api_key, PhotoDB.api_secret)

  def __init__(self):
    # Open a db connection
    self.conn = sqlite3.connect(self.db)
    cur = self.conn.cursor()

    # Does the photos dir exist?
    try:
      os.makedirs(self.photo_dir)
    except OSError as e:
      if e.errno == errno.EEXIST and os.path.isdir(self.photo_dir):
        pass
      else: raise

    # Does the photos table exist?
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='photos';")
    if cur.fetchone() is None:
      cur.execute('''CREATE TABLE photos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, flickr_id INTEGER,fmt TEXT, path TEXT,
                     title TEXT, width INTEGER, height INTEGER, date_taken INTEGER, date_uploaded INTEGER);''')
      cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS flickr_ids ON photos (flickr_id);")


  def add_photo(self, photo):
    cur = self.conn.cursor()
    cur.execute("INSERT INTO photos VALUES (NULL,?,?,?,?,?,?,?,?);",(photo.flickr_id, photo.fmt, photo.path,
      photo.title, photo.width, photo.height, photo.date_taken, photo.date_uploaded));
    # download the photo from the url
    urllib.urlretrieve(photo.url,filename=photo.path)
    if os.path.isfile(photo.path):
      self.conn.commit()
    else:
      self.conn.rollback()


  def get_photo_by_id(self, photo_id):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM photos WHERE id=?;",(photo_id,))
    return cur.fetchone()

  def get_photo_by_flickr_id(self, flickr_id):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM photos WHERE flickr_id=?;",(flickr_id,))
    return cur.fetchone()

  def get_random_photo(self):
    # Here's where we determine the probability for displaying a given photo
    # Returns a tuple containing a photo and a duration
    None


class Photo:

  # Constructor from flickr attributes
  def __init__(self, fa):
    self(fa['id'], fa['originalformat'], fa['title'], fa['url_o'], fa['width_o'], fa['height_o'], fa['datetaken'], fa['dateupload'])

  # Generic constructor
  def __init__(self, fid, fmt, title, url, w, h, dt, du):
    # Do stuff
    self.fmt = fmt
    self.flickr_id = fid
    self.path = PhotoDB.photo_dir + fid + '.' + fmt
    self.title = title
    self.url = url
    self.width = w
    self.height = h
    self.date_taken = dt
    self.date_uploaded = du

PhotoDB()
