'''
    urlresolver Kodi plugin
    Copyright (C) 2018

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
'''
import json
import re
import jsunpack
from net import Net

FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'

class FembedResolver():
    name = "fembed"
    domains = ["fembed.com", "24hd.club", "vcdn.io", "sharinglink.club", "votrefiles.club"]
    pattern = r'(?://|\.)((?:fembed|24hd|vcdn|sharinglink|votrefiles)\.(?:com|club|io))/v/([a-zA-Z0-9-]+)'

    def __init__(self):
        self.net = Net()
        
    def get_media_url(self, url):
        print "In fembed url =", url
        items = self.get_host_and_id(url)
        host = items[0]
        media_id = items[1]
        print "host, media_id =", host, media_id
        web_url = self.get_url(host, media_id)
        print "In fembed web_url =", web_url
#        headers = {'Referer': web_url, 'User-Agent': common.RAND_UA}
        headers = {'Referer': web_url, 'User-Agent': FF_USER_AGENT}
        api_url = 'https://www.%s/api/source/%s' % (host, media_id)
        print "In fembed api_url =", api_url
        js_result = self.net.http_POST(api_url, form_data={'r': ''}, headers=headers).content
        print "In fembed api_url =", api_url
        if js_result:
#            try:
                js_data = json.loads(js_result)
                print "In fembed js_data =", js_data
                if js_data.get('success'):
                    sources = [(i.get('label'), i.get('file')) for i in js_data.get('data') if i.get('type') == 'mp4']
                    print "In fembed sources =", sources
#                    common.logger.log(sources)
#                    sources = helpers.sort_sources_list(sources)
#                    return helpers.pick_source(sources) + helpers.append_headers(headers)
#                    return sources
                    return sources[0][1]
                else:
                    raise Exception(js_data.get('data'))
#            except Exception as e:
#                raise ResolverError('Error getting video: %s' % e)
                
#        raise ResolverError('Video not found')

    def get_url(self, host, media_id):
#        return self._default_get_url(host, media_id, 'https://www.{host}/v/{media_id}')
         return 'https://www.' + host + '/v/' + media_id
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

    def pick_source(sources, auto_pick=None):
     if auto_pick is None:
        auto_pick = common.get_setting('auto_pick') == 'true'
        
     if len(sources) == 1:
        return sources[0][1]
     elif len(sources) > 1:
        if auto_pick:
            return sources[0][1]
        else:
            result = xbmcgui.Dialog().select(common.i18n('choose_the_link'), [str(source[0]) if source[0] else 'Unknown' for source in sources])
            if result == -1:
                raise ResolverError(common.i18n('no_link_selected'))
            else:
                return sources[result][1]
     else:
        raise ResolverError(common.i18n('no_video_link'))










