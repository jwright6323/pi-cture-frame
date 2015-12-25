# John C. Wright
# johnwright@eecs.berkeley.edu

import flickrapi
import urllib
import os
import errno

api_key = u'e9495a30dea5740bb1da96c1aa60e954'
api_secret = u'bde6f9256b82f199'
user_id = '138731132@N05'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

photos = flickr.people.getPhotos(user_id=user_id, extras="url_o,date_taken,date_upload,original_format")
for x in photos[0]:
  print x.attrib
exit()

PHOTO_DIR = '/tmp/pi-cture-frame/'

try:
  os.makedirs(PHOTO_DIR)
except OSError as e:
  if e.errno == errno.EEXIST and os.path.isdir(PHOTO_DIR):
    pass
  else: raise

def get_photo(attrs):
  print attrs
  #urllib.urlretrieve('http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(originalsecret)s_o.jpg' % attrs,filename=PHOTO_DIR + '/' + attrs['id'] + '.jpg')

for x in photos[0]:
  get_photo(flickr.photos.getInfo(photo_id=x.attrib['id'])[0].attrib )
