from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail

import os, logging
import json, urllib, urllib2
import traceback


# Web app
API_KEY = 'AIzaSyDkrW_qf_sLGzhFrHPjzDKZ-kXsS9SC22A'

class ShortUrlPage(webapp.RequestHandler):
    def get(self):
        longurl = self.request.get('longurl')
        service = self.request.get('service')
        results = {'short' : None}
        # bit.ly, in the future ?
        if service == 'goo.gl':
            post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=%s' % API_KEY
            postdata = {'longUrl':longurl}
            headers = {'Content-Type':'application/json'}
            req = urllib2.Request(
                post_url,
                json.dumps(postdata),
                headers
            )
            ret = urllib2.urlopen(req).read()
            results['short'] = json.loads(ret)['id'].replace("http://","https://")
        json_res = json.dumps(results)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.out.write(json_res)


application = webapp.WSGIApplication(
                                     [
                                        ('/shorturl', ShortUrlPage),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
