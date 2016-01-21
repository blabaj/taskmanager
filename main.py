#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Taskmanager
import time

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        vnosi = Taskmanager.query().fetch()
        params = {"vnosi":vnosi}
        time.sleep(0.1)
        return self.render_template("task.html", params)
    def post(self):
        naslov = self.request.get("naslov")
        if (len(naslov) == 0 or len(naslov.strip(' ')) == 0):
            napaka = {"napaka":"Naslov taska je potreben!"}
            return self.render_template("task.html", napaka)
        sporocilo = self.request.get("sporocilo")
        if (len(sporocilo) == 0 or len(sporocilo.strip(' ')) == 0):
            napaka = {"napaka":"Vsebina sporocila je potrebna!"}
            return self.render_template("task.html", napaka)
        vnos = Taskmanager(naslov = naslov, sporocilo=sporocilo)
        vnos.put()
        #pridobivanje vseh vnosov
        vnosi = Taskmanager.query().fetch()
        params = {"vnosi":vnosi}
        time.sleep(0.1)
        return self.render_template("task.html", params)

class VnosHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        time.sleep(0.1)
        return self.render_template("vnos.html", params)

class UrediHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        return self.render_template("uredi.html", params)
    def post(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        vrednost_vnosa = self.request.get("sporocilo")
        vnos.sporocilo = vrednost_vnosa
        vnos.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")

class BrisiHandler(BaseHandler):
    def get(self, vnos_id):

        vnos = Taskmanager.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        return self.render_template("brisi.html", params)
    def post(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        vnos.key.delete()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")

class KoncajHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        vnos.je_koncan = True
        vnos.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")

class AktivirajHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Taskmanager.get_by_id(int(vnos_id))
        vnos.je_koncan = False
        vnos.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name = "seznam-vnosov"),
    webapp2.Route('/vnos/<vnos_id:\d+>', VnosHandler),
    webapp2.Route('/vnos/uredi/<vnos_id:\d+>', UrediHandler),
    webapp2.Route('/vnos/brisi/<vnos_id:\d+>', BrisiHandler),
    webapp2.Route('/vnos/koncaj/<vnos_id:\d+>', KoncajHandler),
    webapp2.Route('/vnos/aktiviraj/<vnos_id:\d+>', AktivirajHandler)
], debug=True)
