# -*- coding: utf-8 -*-
"""
@author: swoop
"""

import twitter
import requests
from lxml import html
import random
import time

'''
###Soccer Scraper v. 1.1
This program is designed to scrape soccer score data from espnfc.com/scores, parse it, and 
post it to a twitter account. The function tweetScores() is a multipurpose function to tweet any
'msg' string which is passed to it. It requires Twitter Development access and the corresponding codes. 
The function scoreFetcher() builds a dict with an entry for the soccer league, and 
the games in the first div on the site. (There are future plans for the other leagues).
Finally, the function go() is designed to call the previous two periodically during a match day
to provide updated scores for the matches in progress.
''' 

def tweetScores(msg,accessToken='',\
                        tokenSec='',\
                        cosKey='',\
                        conSec=''):
    my_auth = twitter.OAuth(accessToken,tokenSec,cosKey,conSec)
    twit = twitter.Twitter(auth=my_auth) 
    if msg != None:
        print msg
        twit.statuses.update(status=msg)
    else:
        print 'Nuthin fo ya bahws.'
        
def scoreFetcher(lRow): #returns a dict of 'fixtures', given an int corresponding with a League Row
        page=requests.get('http://www.espnfc.com/scores')
        tree=html.fromstring(page.text)
        counter=0
        league=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/h4/a/text()')
        fixtures={"League":league[-1]}
        for i in xrange(1,15):#Cycle through row divs; haven't seen more than 15...
            endOfList=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/@class')
            if endOfList==['score-group']:
                for j in xrange(1,3):#Cycle through columns, always 3
                        emptyScoreBox=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/@class')
                        if emptyScoreBox!=['empty-score'] or []:#Sometimes one column is empty, this ensures it's not
                            team1=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[1]/div[1]/span/text()')
                            team2=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[1]/div[2]/span/text()')
                            score1=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[2]/div[1]/span/text()')
                            score2=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[2]/div[2]/span/text()')
                            counter+=1
                            if len(score1)>0:#Game in progress or over
                                minute=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[3]/span//text()')
                                if minute[-1]=='HT' or minute[0]=='FT':#Game at Half or Full Time 
                                    fixtures['game'+str(counter)] = team1[0]+' '+score1[0]+' - '+score2[0]+' '+team2[0]+' '+minute[-1]+' #LiveScore #Soccer'
                                else:#Game On! Post minute'
                                    fixtures['game'+str(counter)] = team1[0]+' '+score1[0]+' - '+score2[0]+' '+team2[0]+' '+minute[-1]+' #LiveScore #Soccer'
                            else:#Game upcoming; gather Start Time
                                start=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[3]/span/text()')
                                if start[0]!=('ESPNDeportes' or 'ESPN' or 'ESPN2' or 'ESPN3'):#Element is Channel
                                    fixtures['game'+str(counter)] = team1[0]+' '+team2[0]+', '+start[0]+' #LiveScore #Soccer'
                                else:#Grab time from different span
                                    start=tree.xpath('//*[@id="score-leagues"]/div['+str(lRow)+']/div['+str(i)+']/div['+str(j)+']/div/div/div/div[3]/span[2]/text()')
                                    fixtures['game'+str(counter)] = team1[0]+' '+team2[0]+', '+start[0]+' #LiveScore #Soccer'
                               
        return fixtures

def go(tweet='no'):
    iteration=1
    while iteration>0:
        for h in xrange(1,5):
            fixtures=scoreFetcher(h)
            for i in xrange(1,len(fixtures)):
                msg=fixtures['League']+': '+fixtures['game'+str(i)]
                if tweet=='y':
                    try:
                        tweetScores(msg)
                        time.sleep(random.randrange(4, 6)) 
                    except:
                        print 'Duplicate Tweet. Continuing...'
                else:
                    print msg
            iteration-=1
    #        time.sleep(580) 

go()