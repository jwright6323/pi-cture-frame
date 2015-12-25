# John C. Wright
# johnwright@eecs.berkeley.edu

import sqlite3
import flickrapi
import urllib
import os
import errno
import random

class PhotoDB:

  api_key = u'e9495a30dea5740bb1da96c1aa60e954'
  api_secret = u'bde6f9256b82f199'
  user_id = '138731132@N05'
  photo_dir = '/home/pi/pi-cture-frame/photos/'
  db = photo_dir + 'photos.db'
  flickr = flickrapi.FlickrAPI(api_key, api_secret)

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
    self.conn.commit()
    if cur.fetchone() is None:
      cur.execute('''CREATE TABLE photos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, flickr_id INTEGER,fmt TEXT, path TEXT,
                     title TEXT, width INTEGER, height INTEGER, rotation INTEGER, date_taken INTEGER,
                     date_uploaded INTEGER);''')
      cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS flickr_ids ON photos (flickr_id);")
      self.conn.commit()


  def add_photo(self, photo):
    cur = self.conn.cursor()
    cur.execute("INSERT INTO photos VALUES (NULL,?,?,?,?,?,?,?,?,?);",(photo.flickr_id, photo.fmt, photo.path,
      photo.title, photo.width, photo.height, photo.rotation, photo.date_taken, photo.date_uploaded));
    # download the photo from the url
    urllib.urlretrieve(photo.url,filename=photo.path)
    if os.path.isfile(photo.path):
      self.conn.commit()
    else:
      self.conn.rollback()


  def get_photo_by_id(self, photo_id):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM photos WHERE id=?;",(photo_id,))
    self.conn.commit()
    return Photo.from_db(cur.fetchone())

  def get_photo_by_flickr_id(self, flickr_id):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM photos WHERE flickr_id=?;",(flickr_id,))
    self.conn.commit()
    return Photo.from_db(cur.fetchone())

  def update_database(self):
    for x in self.flickr.people.getPhotos(user_id=self.user_id, extras="url_o,date_taken,date_upload,original_format,rotate")[0]:
      if self.get_photo_by_flickr_id(x.attrib['id']) is None:
        rot = self.flickr.photos.getInfo(photo_id=x.attrib['id'])[0].attrib['rotation']
        # get new photo
        self.add_photo(Photo(x.attrib, rot))


  def get_random_photo(self):
    # Here's where we determine the probability for displaying a given photo
    cur = self.conn.cursor()
    # When applying weights use this, but for now just have equal weights
    #cur.execute("SELECT id,path,date_uploaded FROM photos;")
    cur.execute("SELECT max(id) FROM photos;")
    self.conn.commit()
    length = cur.fetchone()[0]
    x = None
    while x is None:
      x = self.get_photo_by_id(random.randint(1,length))
    return x


class Photo:

  # Constructor from flickr attributes
  def __init__(self, fa=None, rot=None):
    if fa is not None:
      self.fmt = fa['originalformat']
      self.flickr_id = fa['id']
      self.path = PhotoDB.photo_dir + self.flickr_id + '.' + self.fmt
      self.title = fa['title']
      self.url = fa['url_o']
      self.width = fa['width_o']
      self.height = fa['height_o']
      self.date_taken = fa['datetaken'] # note the bug in the Flickr API
      self.date_uploaded = fa['dateupload'] # note the bug in the Flickr API
      if rot is None:
        self.rotation = 0
      else:
        self.rotation = rot

  @staticmethod
  def from_db(db_resp):
    if db_resp is None:
      return None
    p = Photo()
    p.flickr_id = db_resp[1]
    p.fmt = db_resp[2]
    p.path = db_resp[3]
    p.title = db_resp[4]
    p.width = db_resp[5]
    p.height = db_resp[6]
    p.rotation = db_resp[7]
    p.date_taken = db_resp[8]
    p.date_uploaded = db_resp[9]
    return p


if __name__=="__main__":
  PhotoDB().update_database()
