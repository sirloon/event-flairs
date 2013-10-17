from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail

import os, logging
import StringIO
import numpy
import omr
import json
import traceback


# Web app

class MainPage(webapp.RequestHandler):
    def get(self):

        template_values = {}

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def send_email(self,subject,body,pix,omrpix):
        mail.send_mail(sender="sebastien.lelong@gmail.com",
                       to="shootsheetapps@gmail.com",
                       subject=subject,
                       body=body,
                       attachments=[("pix.jpg",pix),("omr.jpg",omrpix)])

    def post(self):
        #logging.info("keys: %s" % self.request)
        pix = self.request.get('Filedata')
        #logging.error("pix(%s): %s" % (len(pix),pix))
        buf = StringIO.StringIO(pix)
        try:
            if self.request.get('pre'):
                # search best angle
                angle = omr.preomr(buf)
                omrpix,res = omr.omr(buf,angle)
            else:
                omrpix,res = omr.omr(buf,0)
            outb = StringIO.StringIO()
            omrpix.save(outb,format="JPEG")
            outb.seek(0)
            if res['errmsg']:
                self.send_email("Problem pix from OMR","%s" % res,pix,"")
        except Exception,e:
            self.send_email("Error pix from OMR","%s\n%s" % (e,traceback.format_exc()),pix,"")
            raise
        self.response.headers['Content-Type'] = 'application/json'
        json_res = json.dumps(res)
        if self.request.get('debug'):
            self.send_email("OK pix from OMR","%s" % res,pix,outb.buf)
        self.response.out.write(json_res)




application = webapp.WSGIApplication(
                                     [
                                        ('/', MainPage),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
