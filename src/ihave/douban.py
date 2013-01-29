# -*- coding: utf-8 -*-
'''
Created on 2013-1-29

@author: Tony
'''
import urllib2
import json
 
bookurlbase = 'http://api.douban.com/v2/book/isbn/'
DOUBAN_APIKEY = '075021a5dbb9da0b15f064f1932d8e21' #豆瓣上申请的APIKEY
 
class DoubanAPI(object):
    def get_book_info(self,isbn):
        url = '%s%s?apikey=%s' % (bookurlbase, isbn, DOUBAN_APIKEY)
        resp = urllib2.urlopen(url)
        
        book = json.loads(resp.read())
        return book
        