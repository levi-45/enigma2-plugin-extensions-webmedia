'''
vidzi urlresolver plugin
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

#import re
import urllib
#from lib import jsunpack
#from urlresolver import common
#from urlresolver.resolver import UrlResolver, ResolverError

import re
import jsunpack
from net import Net

#from resolver.vidzi import VidziResolver
#         VidziResolver.get_media_url(url)


class VidziResolver():
    name = "vidzi"
    domains = ["vidzi.tv"]
    pattern = '(?://|\.)(vidzi\.tv)/(?:embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = Net()

#    def get_media_url(self, host, media_id):

    def get_media_url(self, url):
        items = self.get_host_and_id(url)
        host = items[0]
        media_id = items[1]
        pass#print "host, media_id =", host, media_id
    
        web_url = self.get_url(host, media_id)
        pass#print "web_url =", web_url
        html = self.net.http_GET(web_url).content

        if '404 Not Found' in html:
            raise ResolverError('File Not Found or removed')

        r = re.search('file\s*:\s*"([^"]+)', html)
        if r:
            return r.group(1) + '|' + urllib.urlencode({'Referer': 'http://vidzi.tv/nplayer/jwplayer.flash.swf'})
        else:
            for match in re.finditer('(eval\(function.*?)</script>', html, re.DOTALL):
                js_data = jsunpack.unpack(match.group(1))
                r = re.search('file\s*:\s*"([^"]+)', js_data)
                if r:
                    return r.group(1)

        raise ResolverError('Unable to locate link')

    def get_url(self, host, media_id):
        return 'http://%s/embed-%s.html' % (host, media_id)

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
