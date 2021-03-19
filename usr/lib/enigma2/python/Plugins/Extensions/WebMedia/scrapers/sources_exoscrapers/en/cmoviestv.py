# -*- coding: utf-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
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

"""
from openscrapers.modules import cfscrape
from openscrapers.modules import cleantitle
from openscrapers.modules import source_utils
"""
#from exoscrapers.modules import cfscrape
from Plugins.Extensions.WebMedia.libshowtime import cleantitle
from Plugins.Extensions.WebMedia.libshowtime import source_utils

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
		self.domains = ['cmovies.tv', 'cmovies.video', 'cmovieshd.bz']
		self.base_link = 'https://cmovies.tv'
		self.search_link = '/film/%s/watching.html?ep=0'
#		self.scraper = cfscrape.create_scraper()


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title).replace('--', '-')
			url = self.base_link + self.search_link % title
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			hostDict = hostDict + hostprDict

#			r = self.scraper.get(url).content
			r = getUrl(url)
			print "In cmoviestv url =", url
			print "In cmoviestv r =", r

			qual = re.compile('class="quality">(.+?)</span>').findall(r)
			for i in qual:
				info = i
				if '1080' in i:
					quality = '1080p'
				elif '720' in i:
					quality = '720p'
				else:
					quality = 'SD'
			u = re.compile('data-video="(.+?)"').findall(r)
                        print "In cmoviestv u =", u
			for url in u:
				if not url.startswith('http'):
					url =  "https:" + url
				if 'vidcloud' in url:
##					r = self.scraper.get(url).content
					r = getUrl(url)
					t = re.compile('data-video="(.+?)"').findall(r)
					for url in t:
						if not url.startswith('http'):
							url =  "https:" + url
						valid, host = source_utils.is_host_valid(url, hostDict)
##						if valid and 'vidcloud' not in url:
						if 'vidcloud' not in url:
							sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})

				valid, host = source_utils.is_host_valid(url, hostDict)

##				if valid and 'vidcloud' not in url:
				if 'vidcloud' not in url:
					sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
			return sources
		except:
			source_utils.scraper_error('CMOVIESTV')
			return sources


	def resolve(self, url):
		return url






