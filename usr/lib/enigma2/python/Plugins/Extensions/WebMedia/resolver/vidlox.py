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
#from lib import helpers
import common
#from urlresolver.resolver import UrlResolver, ResolverError
from net import Net

import urllib2

def getUrl(url):
        print "Here in client2 getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def getUrl2(url, referer):
        print "Here in client2 getUrl2 url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link	


class VidloxResolver():
    name = "vidlox"
    domains = ['vidlox.tv', 'vidlox.me', 'vidlox.xyz']
    pattern = r'(?://|\.)(vidlox\.(?:tv|me|xyz))/(?:embed-|source/)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = Net()

    def get_media_url(self, url):
        items = self.get_host_and_id(url)
        host = items[0]
        #https%3A%2F%2Fvidlox.me%2Fembed-yq792yhurhic.html
        media_id = items[1]
        print "host, media_id =", host, media_id
        web_url = self.get_url(host, media_id)
#        headers = {'User-Agent': common.FF_USER_AGENT}
#        html = self.net.http_GET(web_url, headers=headers).content
        html = getUrl2(web_url, web_url)
        if html:
            _srcs = re.search(r'sources\s*:\s*\[(.+?)\]', html)
            
            """
            if _srcs:
                srcs = helpers.scrape_sources(_srcs.group(1), patterns=['''["'](?P<url>http[^"']+)'''], result_blacklist=['.m3u8'])
                if srcs:
                    headers.update({'Referer': web_url})
                    return helpers.pick_source(srcs) + helpers.append_headers(headers)

        raise ResolverError('Unable to locate link')
            """
            return _srcs[0]
            
    def get_url(self, host, media_id):
        url = "https://vidlox.me/embed-{" + media_id +"}.html"
#        return self._default_get_url(host, media_id, template='https://vidlox.me/embed-{media_id}.html')
        return url
        
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











