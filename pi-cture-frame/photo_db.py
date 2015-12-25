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

  def update_database(self):
    for x in self.flickr.people.getPhotos(user_id=self.user_id, extras="url_o,date_taken,date_upload,original_format")[0]:
      if self.get_photo_by_flickr_id(x.attrib['id']) is None:
        # get new photo
        self.add_photo(Photo(x.attrib))


  def get_random_photo(self):
    # Here's where we determine the probability for displaying a given photo
    # Returns a tuple containing a photo and a duration
    None


class Photo:

  # Constructor from flickr attributes
  def __init__(self, fa):
    self.fmt = fa['originalformat']
    self.flickr_id = fa['id']
    self.path = PhotoDB.photo_dir + self.flickr_id + '.' + self.fmt
    self.title = fa['title']
    self.url = fa['url_o']
    self.width = fa['width_o']
    self.height = fa['height_o']
    self.date_taken = fa['datetaken'] # note the bug in the Flickr API
    self.date_uploaded = fa['dateupload'] # note the bug in the Flickr API


if __name__=="__main__"
  PhotoDB().update_database()
