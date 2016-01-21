from google.appengine.ext import ndb

class  Taskmanager(ndb.Model):
    naslov = ndb.StringProperty()
    sporocilo = ndb.TextProperty()
    je_koncan = ndb.BooleanProperty(default = False)
    nastanek = ndb.DateTimeProperty(auto_now_add=True)