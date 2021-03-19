# -*- coding: utf-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    ExoScrapers Project
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

import re
import urllib
import urlparse
#from exoscrapers.modules import cfscrape
from Plugins.Extensions.WebMedia.libshowtime import cleantitle
from Plugins.Extensions.WebMedia.libshowtime import client
from Plugins.Extensions.WebMedia.libshowtime import directstream

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


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['seriesonline.io']
        self.base_link = 'https://www2.seriesonline8.co'
        self.search_link = '/movie/search/%s'
#        self.scraper = cfscrape.create_scraper()

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def movie(self, imdb, title, localtitle, aliases, year):
        aliases = [{'country': 'us', 'title': 'The Hustlers at Scores'}, {'country': 'us', 'title': 'Hustlers'}, {'country': 'us', 'title': 'Hustlers'}]
        print "Here in movie imdb =", imdb
        print "Here in movie title =", title
        print "Here in movie localtitle =", localtitle
        print "Here in movie aliases =", aliases
        print "Here in movie year =", year

        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            print "Here in movie url =", url
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, aliases):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %01d' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
#            r = self.scraper.get(url).content
            r = getUrl(url)
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
            url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
            return url
        except:
            return

    def searchMovieX(self, title, year, aliases):
#        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            r = self.scraper.get(url).content
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
            except:
                url = None
                pass

            if (url == None):
                url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]

            url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
            return url
#        except:
#            return
    def searchMovie(self, title, year, aliases):
        print "Here in searchMovie title =", title
        print "Here in searchMovie year =", year
        print "Here in searchMovie aliases =", aliases
    
    
        try:
            title = cleantitle.normalize(title)
            print "Here in searchMovie title =", title
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            print "Here in searchMovie url =", url
#            r = self.scraper.get(url).content
            r = getUrl(url)
            print "Here in searchMovie r =", r
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            print "Here in searchMovie r 2=", r
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            print "Here in searchMovie r 3=", r
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            print "Here in searchMovie results =", results
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                print "Here in searchMovie r 4=", r
                url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
                print "Here in searchMovie url =", url
            except:
                url = None
                print "Here in searchMovie url 2=", url
                pass

            if (url == None):
                url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]
                print "Here in searchMovie url 3=", url

            url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
            print "Here in searchMovie url 4=", url
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            print "Here in sources aliases =", aliases
            print "Here in sources data =", data
            if 'tvshowtitle' in data:
                ep = data['episode']
                url = '%s/film/%s-season-%01d/watching.html?ep=%s' % (
                    self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), ep)
#                r = self.scraper.get(url).content
                r = getUrl(url)

                if url == None:
                    url = self.searchShow(data['tvshowtitle'], data['season'], aliases)

            else:
                url = self.searchMovie(data['title'], data['year'], aliases)

##            if url == None: raise Exception()
            if url == None: return sources
#            r = self.scraper.get(url).content
            r = getUrl(url)
            print "Here in sources r =", r
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            print "Here in sources r 2=", r
            if 'tvshowtitle' in data:
                ep = data['episode']
                links = client.parseDOM(r, 'a', attrs={'episode-data': ep}, ret='player-data')
            else:
                links = client.parseDOM(r, 'a', ret='player-data')
                print "Here in sources print links =", links
            for link in links:
                print "Here in sources print link =", link
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                    print "Here in sources print host =", host
#                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False,
                                    'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url



















