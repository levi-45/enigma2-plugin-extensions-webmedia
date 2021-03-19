"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import urllib
import urllib2
import jsunpack
from net import Net

IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'

class VideoMegaResolver():
    pass#print "In videomega 1="
    name = "videomega"
    domains = ["videomega.tv"]
    pattern = '(?://|\.)(videomega\.tv)/(?:(?:iframe|cdn|validatehash|view)\.php)?\?(?:ref|hashkey)=([a-zA-Z0-9]+)'

    def __init__(self):
        self.net = Net()

    def get_media_url(self, url):
        pass#print "In videomega get_media_url url =", url
        
        items = self.get_host_and_id(url)
        host = items[0]
        media_id = items[1]
        pass#print "host, media_id =", host, media_id
        web_url = self.get_url(host, media_id)
        pass#print "In videomega web_url =", web_url
        headers = {
            'User-Agent': IOS_USER_AGENT,
            'Referer': web_url
        }

        html = self.net.http_GET(web_url, headers=headers).content
        pass#print "In videomega html =", html
        if jsunpack.detect(html):
            js_data = jsunpack.unpack(html)
            match = re.search('"src"\s*,\s*"([^"]+)', js_data)
            pass#print "In videomega match =", match
        try:
            stream_url = match.group(1)

            r = urllib2.Request(stream_url, headers=headers)
            r = int(urllib2.urlopen(r, timeout=15).headers['Content-Length'])
            pass#print "In videomega r =", r
            if r > 1048576:
                stream_url += '|' + urllib.urlencode(headers)
                pass#print "In videomega stream_url =", stream_url
                return stream_url
        except:
            ResolverError("File Not Playable")

        raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):
        return 'http://videomega.tv/cdn.php?ref=%s' % media_id

    def get_host_and_id(self, url):
        '''
        The method that converts a host and media_id into a valid url

        Args:
            url (str): a valid url on the host this resolver resolves

        Returns:
            host (str): the host the link is on
            media_id (str): the media_id the can be returned by get_host_and_id
        '''
        r = re.search(self.pattern, url, re.I)
        if r:
            return r.groups()
        else:
            return False
