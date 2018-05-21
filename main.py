#!/usr/bin/env python

import os
import jinja2
import webapp2
import re
import json
import mimetypes
import hashlib
from Infrastructure import filters


_SERVICE_WORKER_PATH = 'static/scripts/sw.js'

# Grab the version from the package.json.
version = None
# with open('./package.json') as f:
#     data = json.load(f)
#     version = data["version"]


# Set up the environment.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.filters["add_hash"] = filters.add_hash


class MainHandler(webapp2.RequestHandler):

    def get_template_info(self, url):
        template_info = {
            "path": url,
            "mimetype": (None, None),
            # Static files can be cached for a year, since there are hashes to
            # track changes to files, and so on. And we don't cache HTML.
            "cache": "public, max-age=31536000"
        }

        # If this is not a static file, use a template.
        if re.search(r"^static/", url) is None:
            template_info["path"] = "views/pages/" + url + ".html"

            # HTML files should expire immediately.
            template_info["cache"] = "private, no-cache"

        # Strip off the hash from the path we're looking for.
        template_info["path"] = re.sub(r'[a-f0-9]{64}.', '', template_info["path"])

        # Make a special exception for the Service Worker, since we serve it
        # from /bon/sw.js, even though the file lives elsewhere.
        if re.search("sw.js$", url) is not None:
            template_info["path"] = _SERVICE_WORKER_PATH

        template_info["mimetype"] = mimetypes.guess_type(template_info["path"])

        return template_info

    def get(self, url):

        template_info = self.get_template_info(url)
        print "+++++++++++++++++++++++++++++++template_info+++++++++++++++++++++++++++++++++++"
        print template_info
        content_type = "text/plain"
        response = {
            "code": 404,
            "content": "URL not found."
        }

        if template_info["mimetype"][0]:
            content_type = "%s; charset=utf-8" % template_info["mimetype"][0]

        try:
            print ("static imges path: " + template_info["path"])
            template = JINJA_ENVIRONMENT.get_template(template_info["path"])
            response["code"] = 200
            response["content"] = template.render(
                version=version,
                url=url
            )
        except jinja2.TemplateNotFound as template_name:
            template = JINJA_ENVIRONMENT.get_template("views/pages/404.html")
            response["content"] = template.render()
            print ("Template not found: %s (requested by %s)" %
                   (str(template_name), template_info["path"]))

        # Make an ETag for the content
        etag = hashlib.sha256()
        etag.update(response["content"].encode('utf-8'))

        self.response.status = response["code"]
        self.response.headers["Content-Type"] = content_type
        self.response.headers["ETag"] = etag.hexdigest()
        self.response.headers["Cache-Control"] = template_info["cache"]
        self.response.write(response["content"])

    def post(self, url):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(dict(self.request.POST)))
        pass


app = webapp2.WSGIApplication([
    ('/(.*)', MainHandler)
], debug=True)
