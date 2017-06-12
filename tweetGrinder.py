#!usr/bin/python
# -*- coding: utf-8 -*-

#============================================================#
#
# tweetGrinder 
#
# Description:
# A Python class for processing Tweets by category, cleaning the text and storing in a csv file.
# 
# Authors: L. Rheault, A. Musulan.
#
#=============================================================#

import json
import codecs
import re 
import pandas as pd
from HTMLParser import HTMLParser
from unidecode import unidecode
import os.path
import os, sys

class tweetGrinder(object):

    def __init__(self, outpath):
        
        self.outpath = outpath
        self.p = HTMLParser()
        self.colnames = ['id','date','user','type','raw_text','display_text','original_url', 'quoted_text']
        if not os.path.isfile(self.outpath): 
            savefile = pd.DataFrame([], columns = self.colnames)
            savefile.to_csv(self.outpath, index=False, sep=',', encoding='utf-8')

    def remove_non_ascii(self, text):
        return unidecode(unicode(text))

    def simpleURL(self, idd, user, text):
        url = 'https://www.twitter.com/'+user+'/status/'+str(idd)
        return url

    def transform(self, inpath, broken=None, length = None):

        self.path = inpath
        tweetStream = codecs.open(self.path, 'r', encoding='utf-8').readlines()
        if broken!=None:
            tweetStream = tweetStream[:-1]
        if length==None:
            self.length = 4
        else:
            self.length = length          

        for line in tweetStream:
            if line:
                try:
                    tweet = json.loads(line)
                    if 'user' in tweet:
                        if tweet['lang']=="en":
                            data = []
                            quoted_text = ''
                            if 'retweeted_status' in tweet:
                                if 'quoted_status' in tweet['retweeted_status']:
                                    if 'extended_tweet' in tweet['retweeted_status']['quoted_status']:
                                        quoted_text = tweet['retweeted_status']['quoted_status']['extended_tweet']['full_text']
                                    else:
                                        quoted_text = tweet['retweeted_status']['quoted_status']['text']
                                    if 'extended_tweet' in tweet['retweeted_status']:
                                        text = tweet['retweeted_status']['extended_tweet']['full_text']
                                        if 'display_text_range' in tweet['retweeted_status']['extended_tweet']:
                                            if type(tweet['retweeted_status']['extended_tweet']['display_text_range'])==list:
                                                st, en = tweet['retweeted_status']['extended_tweet']['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'quote_extended'
                                    else:
                                        text = tweet['text']
                                        if 'display_text_range' in tweet:
                                            if type(tweet['display_text_range'])==list:
                                                st, en = tweet['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'quote_normal'
                                else:
                                    if 'extended_tweet' in tweet['retweeted_status']:
                                        text = tweet['retweeted_status']['extended_tweet']['full_text']
                                        if 'display_text_range' in tweet['retweeted_status']['extended_tweet']:
                                            if type(tweet['retweeted_status']['extended_tweet']['display_text_range'])==list:
                                                st, en = tweet['retweeted_status']['extended_tweet']['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'retweet_extended'
                                    else:
                                        text = tweet['retweeted_status']['text']
                                        if 'display_text_range' in tweet['retweeted_status']:
                                            if type(tweet['retweeted_status']['display_text_range'])==list:
                                                st, en = tweet['retweeted_status']['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'retweet_normal'
                            else:
                                if 'quoted_status' in tweet:
                                    if 'extended_tweet' in tweet['quoted_status']:
                                        quoted_text = tweet['quoted_status']['extended_tweet']['full_text']
                                    else:
                                        quoted_text = tweet['quoted_status']['text']
                                    if 'extended_tweet' in tweet:
                                        text = tweet['extended_tweet']['full_text']
                                        if 'display_text_range' in tweet['extended_tweet']:
                                            if type(tweet['extended_tweet']['display_text_range'])==list:
                                                st, en = tweet['extended_tweet']['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'quote_extended'
                                    else:
                                        text = tweet['text']
                                        if 'display_text_range' in tweet:
                                            if type(tweet['display_text_range'])==list:
                                                st, en = tweet['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'quote_normal'
                                else:
                                    if 'extended_tweet' in tweet:
                                        text = tweet['extended_tweet']['full_text']
                                        if 'display_text_range' in tweet['extended_tweet']:
                                            if type(tweet['extended_tweet']['display_text_range'])==list:
                                                st, en = tweet['extended_tweet']['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'tweet_extended'
                                    else:
                                        text = tweet['text']
                                        if 'display_text_range' in tweet:
                                            if type(tweet['display_text_range'])==list:
                                                st, en = tweet['display_text_range']
                                                display_text = text[st:en]
                                        else: 
                                            display_text = text
                                        reference = 'tweet_normal'                          
                            text = self.p.unescape(text)
                            display_text = self.p.unescape(display_text) 
                            if display_text.startswith('RT') and ':' in display_text:
                                display_text = display_text.split(':',1)[1]
                            tokens = display_text.split(' ')
                            tokens = [t for t in tokens if not t.startswith('@') and not t.startswith('#')]
                            if len(tokens) >= self.length:
                                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
                                for u in urls:
                                    text = text.replace(u, "")
                                    display_text = display_text.replace(u, "")
                                text = text.replace('\n', " ").replace('\r', " ").replace('\t', " ").strip()
                                display_text = display_text.replace('\n', " ").replace('\r', " ").replace('\t', " ").strip()
                                idd = str(tweet['id'])            
                                user = tweet['user']['screen_name']                             
                                display_text = self.remove_non_ascii(display_text)
                                original_url = self.simpleURL(idd, user, display_text)
                                date = tweet['created_at']
                                data = [(idd, date, user, reference, text, display_text, original_url, quoted_text)]
                                df = pd.DataFrame(data)
                                df.to_csv(self.outpath, mode='a', sep=',', index=False, encoding='utf-8', header=None)
                except:
                    print "The following line could not processed:\n"
                    print "%s" %(line)
                    continue

    def sample(self, samplepath, n):
        if n is None:
            self.n = 1000
        else:
            self.n = n
        self.samplepath = samplepath
        temp = pd.read_csv(self.outpath, delimiter=',', dtype=object, header=0, names = self.colnames, encoding='utf-8')
        temp.drop_duplicates(['display_text'], inplace=True)  
        sample = temp.sample(self.n)
        sample.to_csv(self.samplepath, index=False, sep=',', encoding='utf-8')
