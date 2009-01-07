## Thanks to dbr @ github for adding some unicode management code to this file :)

## TrailerPlaylist.py: uses dbr's appletrailers.py module to create an asx
## playlist (for my trusty Windows Media Player) that plays the movie poster for
## a specified duration (10 seconds) and then the trailer, currently for all
## 80-90 trailers on Apple.com. The m3u playlist excludes the posters.

## It would be nice to create a playlist for new titles only, and/or certain actors
## and/or certain genre, ...etc.


import sys, os, time
from appletrailers import Trailers

fn_m3u = "appletrailers.m3u"
fn_ASX = "appletrailers.asx"
poster_time = "00:10"

class Movies:
  def __init__(self, format = "480", path = None):
    self.format = format
    self.path   = path
    self.movies = None
    
    if self.path == None:
      self.path = os.getcwd()

  def RunTimeM3uString(self, ts):
    st = ts.split(':')
    if len(st[0]) > 0:
      return str(int(st[0]) * 60 + int(st[1]))
    else:
      return str(int(st[1]))


  def Write_ASX(self):
    path = os.path.join(self.path, fn_ASX)
    
    print "Using path: ", path

    try:
      f = open(path,'w+')

      f.write("<ASX version = \"3.0\">\n")
      f.write("<Title>Apple Trailers</Title>\n")

      for m in self.movies:
        f.write("<Entry>\n")
        f.write("  <Title>" + m.info.title.encode("UTF-8","ignore") + "</Title>\n")
        f.write("  <Duration value=\"" + poster_time.encode("UTF-8","ignore") + "\" />\n")
        f.write("  <Ref href = \"" + m.poster.location.encode("UTF-8","ignore") + "\" />\n")
        f.write("</Entry>\n")

      f.write("</ASX>\n")
      f.close()
    except IOError:
      print "ERROR - Movies()::Write(): Failed."
      raise
    


  def Write_m3u(self):
    path = os.path.join(self.path, fn_m3u)
    print "Using path: ", path

    try:
      f = open(path,'w+')
      f.write("#EXTM3U\n")
      for m in self.movies:
        rts = self.RunTimeM3uString(m.info.runtime)

        f.write("#EXTINF: %s,%s\n" % (rts, m.info.title.encode("UTF-8", "ignore")))
        f.write(m.preview.large.encode("UTF-8", "ignore") + '\n')
      f.close()
    except IOError:
      print "ERROR - Movies()::Write(): Failed."
      raise


  def GetMovies(self):
    self.movies = Trailers(self.format)

    for trailer in self.movies:
      print "Title:", trailer.info.title.encode("UTF-8", "ignore")
      print "Poster:", trailer.poster.location.encode("UTF-8", "ignore")
      print "Actors:", ", ".join(x.encode("UTF-8", "ignore") for x in trailer.cast)
      print "Trailer:", trailer.preview.large.encode("UTF-8", "ignore")
      print "*"*24

    print "total movies: ", len(self.movies)
      
  

def main():
  
  if len(sys.argv) > 1:
    size = sys.argv[1]
    print Trailers().res_lookup.keys()
    if size not in Trailers.res_lookup.keys():
      print "Resolution not valid, should be one of: %s" % (", ".join(Trailers.res_lookup.keys()))
      sys.exit(1)
    else:
      print size
  else:
    size = "480"

  m = Movies(format = size)
  m.GetMovies()
  m.Write_m3u()
  m.Write_ASX()


if __name__ == '__main__':
    main()

