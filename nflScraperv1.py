# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 23:33:35 2014

@author: swoop
"""


'''This program is designed in two parts: first, to grab NFL game ID's from
ESPN.com and save them to a .csv. Second, it will take that data (or any 
properly formatted .csv file) and download game scores, teams, and time which 
are then tweeted out. This requires that the .csv path be specified, as well
as that the user has a twitter account with the proper permissions. '''

import twitter
import requests
from lxml import html
import csv
import time
import random

###Step 1### Get ESPN Game ID'S
#results=[]
#
#for i in range(194,420):
#    try:
#        result=[]
#        page=requests.get('http://scores.espn.go.com/nfl/boxscore?gameId=400554'+str(i))
#        tree=html.fromstring(page.text)
#        timedate=tree.xpath('//*[@id="gamepackageTop"]/div[4]/div[2]/p[1]/text()')
#        team1=tree.xpath('//*[@id="matchup-nfl-400554'+str(i)+'"]/div[1]/div[2]/h3/a/text()')
#        team2=tree.xpath('//*[@id="matchup-nfl-400554'+str(i)+'"]/div[2]/div[2]/h3/a/text()')
#        timedate=str(timedate[0]).split(' ET, ')
#        result.append(timedate[1])
#        result.append(timedate[0])
#        result.append(team1[0])
#        result.append(team2[0])
#        result.append('400554'+str(i))
#        results.append(result)
#        print result
#    except Exception:
#        sys.exc_clear()
#        
##report=pd.DataFrame(results)
##pd.DataFrame(report).to_csv('/Users/swoop/Documents/Python/NFL.csv', sheet_name='Sheet1')
#print report

###Step 2###

def tweetScores(msg,accessToken='2193344742-iKr46uz1hRPvlmcC38JiTU0qRlJtJf5p2NylN2L',\
                        tokenSec='zAocuHCcugEIwvtp4IQX0f1RsplbrhR3ERbS7BqEUVwEq',\
                        cosKey='IkgKVEyGGQUzfjjZFAvMbodxF',\
                        conSec='HdzrI7MVKTKfRcqeK5dpsmn0BiBfKZbJ8QjqFCMspiGYc9vFG3'):
    my_auth = twitter.OAuth(accessToken,tokenSec,cosKey,conSec)
    twit = twitter.Twitter(auth=my_auth) 
    if msg != None:
        print msg
        twit.statuses.update(status=msg)
        
def scoreFetcher(url):
        page=requests.get('http://scores.espn.go.com/nfl/boxscore?gameId='+str(url))
        tree=html.fromstring(page.text)
        team1=tree.xpath('//*[@id="matchup-nfl-'+str(url)+'"]/div[1]/div[2]/h3/a/text()')
        team2=tree.xpath('//*[@id="matchup-nfl-'+str(url)+'"]/div[2]/div[2]/h3/a/text()')
        score1=tree.xpath('//*[@id="matchup-nfl-'+str(url)+'-awayScore"]/text()')
        score2=tree.xpath('//*[@id="matchup-nfl-'+str(url)+'-homeScore"]/text()')
        try:
            score1=score1[-1]
            score2=score2[-1]
        except:
            score1='TBD'
            score2='TBD'
            pass
        time=tree.xpath('//*[@id="gameStatusBarText"]/text()')
        if score1=='TBD':
#            result='Coming Up: '+date_long[-1]+' the '+team1[-1]+' vs. the '+team2[-1]
#            return result
            pass
        else:
            result='#NFL: #'+team1[-1]+' '+score1+' - '+score2+' #'+team2[-1]+', '+time[-1]      
            return result
            


def csvReader(fileStr):
    with open(fileStr, 'rb') as csvfile:
        urls=csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i in urls:
            nums=i[0]
            nums=nums.split(',')
        return nums       
            
def allTogetherMeow(NFLWeek):
    iteration=16
    nums=csvReader('/Users/swoop/Documents/Python/'+str(NFLWeek)+'.csv')
    while iteration==16 or iteration==0:
        for i in nums:
            msg=(scoreFetcher(i))
            try:
                tweetScores(msg)
                time.sleep(random.randrange(1, 4))
            except:
                pass
        time.sleep(900)
        iteration-=1
    while iteration>0 and iteration<16:
        try:
            for i in nums:
                msg=(scoreFetcher(i))
                last=[]
                try:
                    if msg[-1]!='l' and msg not in last:
                        tweetScores(msg)
                        last+=msg
                        time.sleep(random.randrange(1, 4))        
                except:
                    pass
            time.sleep(900)
            iteration-=1
        except:
            continue

allTogetherMeow('NFLWeek10')


