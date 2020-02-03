# -*- coding: utf-8 -*-
"""
Twit.py is a visualition tool using the Twitter API

@author Liam H.

"""

import tweepy
import numpy as np
import matplotlib.pyplot as plt

consumer_key = 'aIebVTqqpwsTG3ps4uKqXiktm'
consumer_secret = 'Lb88TLKTbb26YZgdneWJZeYgPHnHfWY6UMMN2YfB5OjYgjjXHt'
access_token = '622231144-CXjGU4RsfeIHdiQvheaAJaIMaLHkA5ZWFJNlC2SY'
access_token_secret = '2QFrdlE9ywxheWd8mwGy5cpLwDAbzyEVGthxVzR0L0kPe'



def filter_trends(trends):
    filtered = []
    for hashtag, count in trends:
        if count != None:
            filtered.append((hashtag,count))
    return filtered

def sort_trends(trends):
    trends.sort(key=lambda tup: tup[1])
    return trends

def plot_trends_pie(trend_data):
    labels = []
    sizes = []
    
    for trend,count in trend_data:
        labels.append(trend)
        sizes.append(count)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    
    plt.show()
    
def plot_trends_bar(trend_data):
    N = len(trend_data)
    data = []
    tags = []
    for trend,count in trend_data:
        data.append(count)
        tags.append(trend)
    ind = np.arange(N)
    width = 0.5
    
    plt.bar(ind, data, width, color='#d62728')
    
    plt.ylabel('Retweets')
    plt.title('Trends visualized by number of retweets')
    plt.xticks(ind, tags)
    plt.yticks(np.arange(0, max(data), min(data)))
    
    plt.show()

def pick_plot(opt, data):
    if(opt == 0):
        plot_trends_pie(data)
    elif(opt == 1):
        plot_trends_bar(data)

def main():
    print("####################################################################")
    print("Welcome to the 2017 United States Twitter Trend Vizualizer!")
    print("Please enter the two character region code for the area of interest.")
    print("Key: NW - North Western    NC - North Central    NE - North Eastern")
    print("     MW - Mid Western      MC - Mid Central      MW - Mid Western")
    print("     SW - South Western    SC - South Central    SE - South Eastern")
    print("####################################################################")
    
    
    
    woeids = {'NW':2490383,'NC':2451822,'NE':2477058,
              'MW':2436704,'MC':2430683,'ME':2358820,
              'SW':2487956,'SC':2388929,'SE':2450022}
    
    #Prevent any invalid input and set reg equal to the proper woeid
    reg = ""
    while reg not in woeids:
        reg = input("Region of interest: ")
    
    woeid = woeids[reg]
    
    #Allow the user to choose from visual options
    print("####################################################################")
    print("Please select a visualization option: ")
    print("Key:       P - Pie Chart                               B - Bar Chart")
    print("####################################################################")
    
    
    opts = {'P':0,'B':1}
    
    viz = ""
    while viz not in opts:
        viz = input("Enter single digit option key: ")
    opt = opts[viz]
    
    #Create api object using keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #Define threshold for number of top trends
    threshold = 10
    
    #Return US trends (WOEID) in JSON object
    trends1 = api.trends_place(woeid)
    data = trends1[0] 
    
    #Make a list of trends from JSON object
    trends = data['trends']
    
    #Seperate lists of names of hashtags and retweets
    names = [trend['name'] for trend in trends]
    counts = [trend['tweet_volume'] for trend in trends]
    
    #Tuple list of hashtags and retweets
    full = []
    for i in range(len(names)):
        full.append((names[i],counts[i]))
    
    #Filter the trends based on which have a given amount
    #of retweets
    full = filter_trends(full)
    
    #Sort with that number
    full = sort_trends(full)
    
    #Add to top trends and plot
    top_trends = []
    for i in range(threshold):
        top_trends.append(full[i])
    
    #Choose plot type based on user preference
    pick_plot(opt,top_trends)

main()

