"""
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
#from urlresolver import common
#from urlresolver.resolver import UrlResolver, ResolverError

import re
import jsunpack
from net import Net

#from resolver.vidto import VodlockerResolver


class VodlockerResolver():
    name = "vodlocker.com"
    domains = ["vodlocker.com"]
    pattern = '(?://|\.)(vodlocker\.com)/(?:embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = Net()

    def get_media_url(self, url):
        items = self.get_host_and_id(url)
        host = items[0]
        media_id = items[1]
        pass#print "host, media_id =", host, media_id
        web_url = self.get_url(host, media_id)
        pass#print "web_url =", web_url

        link = self.net.http_GET(web_url).content
        if link.find('404 Not Found') >= 0:
            raise ResolverError('The requested video was not found.')

        video_link = str(re.compile('file[: ]*"(.+?)"').findall(link)[0])

        if len(video_link) > 0:
            return video_link
        else:
            raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):
        return 'http://vodlocker.com/embed-%s-640x400.html' % media_id

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
