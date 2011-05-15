#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import re
import urllib
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
				
		template_values = {}
		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class APITester(webapp.RequestHandler):
    def post(self):		
		api_call = self.request.get('content')
		url_structure = re.match("https://www.googleapis.com/", api_call)
		if url_structure:
			api_read = urllib.urlopen(api_call).read()
			api_fail = re.search('error', api_read)
		
			template_values = {
				'api_fail': api_fail,
				'api_read': api_read,
				'api_call': api_call,
				}
		else:
			template_values = {}
			
		path = os.path.join(os.path.dirname(__file__), 'api_test.html')
		self.response.out.write(template.render(path, template_values))
	
application = webapp.WSGIApplication([('/', MainHandler),
										('/api_test', APITester)],
			                             debug=True)
def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
