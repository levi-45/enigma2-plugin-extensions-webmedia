'''
thevideo urlresolver plugin
Copyright (C) 2014 Eldorado

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re
#from urlresolver import common
#from urlresolver.resolver import UrlResolver, ResolverError

import re
import jsunpack
from net import Net

import common

#from resolver.thevideo import TheVideoResolver


MAX_TRIES = 3

class TheVideoResolver():
    name = "thevideo"
    domains = ["thevideo.me"]
    pattern = '(?://|\.)(thevideo\.me)/(?:embed-|download/)?([0-9a-zA-Z]+)'
#    pattern = '(?://|\.)(thevideo\.me)/(?:embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = Net()

    def get_media_url(self, url):
        pass#print "In thevideo url =", url
        n1 = url.rfind("/")
        media_id = url[(n1+1):]
        web_url = "http://thevideo.me/embed-" + media_id + ".html"
        pass#print "web_url =", web_url
        headers = {
            'User-Agent': common.IE_USER_AGENT,
            'Referer': web_url
        }
        html = self.net.http_GET(web_url, headers=headers).content
        pass#print "html=", html
        r = re.findall(r"'?label'?\s*:\s*'([^']+)p'\s*,\s*'?file'?\s*:\s*'([^']+)", html)
        if not r:
#            raise ResolverError('Unable to locate link')
               pass#print "No r"
        else:
            max_quality = 0
            best_stream_url = None
            for quality, stream_url in r:
                if int(quality) >= max_quality:
                    best_stream_url = stream_url
                    max_quality = int(quality)
            if best_stream_url:
                return best_stream_url
            else:
                raise ResolverError('Unable to locate link')

    def get_url(self, host, media_id):
        return 'http://%s/embed-%s.html' % (host, media_id)
        
    def get_host_and_id(self, url):
        pass#print "In get_host_and_id url =", url 

        '''
        The method that converts a host and media_id into a valid url

        Args:
            url (str): a valid url on the host this resolver resolves

        Returns:
            host (str): the host the link is on
            media_id (str): the media_id the can be returned by get_host_and_id
        '''
        pass#print "In get_host_and_id url 2=", url 
        r = re.search(self.pattern, url, re.I)
        pass#print "In get_host_and_id r =", r
        if r:
            pass#print "In get_host_and_id r.groups() =", r.groups()
            return r.groups()
        else:
            return False
