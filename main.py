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
import webapp2
import json
import png
import kmeans
from urllib2 import urlopen
from google.appengine.api import images

MAX = 100
PIXEL_SIZE = 3
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

def hex_string(pixel):
    output = ""
    for val in pixel:
        output += hex(val)[2:]
    return output

class GetColors(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        k = int(self.request.get('k', default_value=3))
        t = int(self.request.get('t', default_value=10))
        result = urlopen(url)
        # Get image
        if (result.getcode() == 200):
            data = result.read()
        img = images.Image(data)
        raw_width = img.width
        raw_height = img.height
        width = raw_width
        height = raw_height
        # Resize to max
        if raw_width > MAX and row_height > MAX:
            if raw_width > raw_height:
                height = MAX
                width = width * MAX / height
            else:
                width = MAX
                height = height * MAX / width
        img = images.resize(data, width, height)
        reader = png.Reader(bytes=img)
        # Get pixels
        (width, height, pixels, meta) = reader.read_flat()
        n = PIXEL_SIZE
        (means, counts) = kmeans.kmeans(k, pixels, n, 255, t)
        colors = [hex_string(means[i * n : i * n + n]) for i in range(len(counts))]
        output = {}
        output['colors'] = [{'color': colors[i], 'count': counts[i]} for i in range(len(counts))]        
        output['sum'] = sum(counts)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(output))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getColors', GetColors)
], debug=True)
