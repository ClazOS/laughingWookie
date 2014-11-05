# -*- coding: utf-8 -*-
"""
Created on Mon Nov 3 23:33:35 2014

@author: swoop
"""

import twitter
import requests
from lxml import html
import random
import time

'''
This program is designed to scrape soccer score data from espnfc.com/scores, parse it, and 
post it to a twitter account. The function tweetScores() is a multipurpose function to tweet any
'msg' string which is passed to it. It requires Twitter Development access and the corresponding codes. 
The function scoreFetcher() builds a dict with an entry for the soccer league, and 
the games in the first div on the site. (There are future plans for the other leagues).
Finally, the function go() is designed to call the previous two periodically during a match day
to provide updated scores for the matches in progress.
''' 

def tweetScores(msg,accessToken='Yours here!',\
                        tokenSec='Yours here!',\
                        cosKey='Yours here!',\
                        conSec='Yours here!'):
    my_auth = twitter.OAuth(accessToken,tokenSec,cosKey,conSec)
    twit = twitter.Twitter(auth=my_auth) 
    if msg != None:
        print msg
        twit.statuses.update(status=msg)
    else:
        print 'Nuthin fo ya bahws.'
        
def scoreFetcher(): #returns a dict of 'fixtures'
        page=requests.get('http://www.espnfc.com/scores')
        tree=html.fromstring(page.text)
#        games=(int(str((tree.xpath('//*[@id="score-leagues"]/div[1]/h4/span/text()'))[0])[1]))
        league=tree.xpath('//*[@id="score-leagues"]/div[1]/h4/a/text()')
        fixtures={"League":league[-1]}
        counter=0
        for i in range(1,6):
            for j in range(1,3):
                    empty=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/@class')
                    if empty!=['empty-score']:
                        team1=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/div/div/div/div[1]/div[1]/span/text()')
                        team2=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/div/div/div/div[1]/div[2]/span/text()')
                        teams=team1[-1]+' vs. '+team2[-1]
                        try:                
                            score1=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/div/div/div/div[2]/div[1]/span/text()')
                            score2=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/div/div/div/div[2]/div[2]/span/text()') 
            #                minute=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+j+']/div['+i+']/div/div/div/div[3]/span[3]/text()')
                            scores=str(score1[-1])+' - '+str(score2[-1])#+', '+str(minute[-1])
                        except: 
                            kickoff=tree.xpath('//*[@id="score-leagues"]/div[1]/div['+str(i)+']/div['+str(j)+']/div/div/div/div[3]/span[2]/text()')   
                            scores=str(kickoff[-1])
                        counter+=1
                        fixtures['game'+str(counter)] = teams+' '+scores 
        return fixtures

def go(tweet='no'):#default will print; passing the string 'y' will Tweet scores.
    iteration=1
    while iteration>0:
        fixtures=scoreFetcher()
        for i in range(1,len(fixtures)):
            msg=fixtures['League']+': '+fixtures['game'+str(i)]
            if tweet=='y':
                try:
                    tweetScores(msg)
                except:
                    print 'hey now'
                    time.sleep(random.randrange(1, 4)) 
            else:
                print msg
        iteration-=1
#        time.sleep(580) 

go('y')