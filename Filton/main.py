#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Opinion

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
        return self.render_template("index.html")

class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

class GuestBookHandler(BaseHandler):
    def get(self):
        return self.render_template("guestbook.html")

class SaveHandler(BaseHandler):
    def post(self):
        first_last_name = self.request.get("name")
        email = self.request.get("email")
        opinion = self.request.get("opinion")

        if "<script>" in opinion:
            return self.write("Can't hack us!")

        save_opinion = Opinion(first_last_name=first_last_name, email=email, opinion=opinion)
        save_opinion.put()

        return self.render_template("saved.html")

class AllOpinionsHandler(BaseHandler):
    def get(self):
        opinions = Opinion.query().fetch()
        params = {
            "opinions": opinions
        }
        return self.render_template("opinions.html", params)

class EachOpinionHandler(BaseHandler):
    def get(self, opinion_id):

        opinion = Opinion.get_by_id(int(opinion_id))
        params = {
            "opinion": opinion
        }

        return self.render_template("opinions-details.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/saved', SaveHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/contact', ContactHandler),
    webapp2.Route('/guestbook', GuestBookHandler),
    webapp2.Route('/opinions', AllOpinionsHandler),
    webapp2.Route('/opinions-details/<opinion_id:\d+>', EachOpinionHandler),
], debug=True)
