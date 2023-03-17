import requests
from datetime import date, datetime, timedelta, timezone
import pytz
import json_tender
import post
import os

today = date.today().strftime("%Y-%m-%d")
key = os.environ.get('NEWSAPI')
#request = 'https://newsapi.org/v2/everything?q=((web3 OR crypto OR bitcoin OR ethereum OR defi OR tether OR stablecoin OR cardano OR binance OR coinbase OR solana OR dogecoin OR polkadot OR (smart AND contract) OR blockchain OR ICO) NOT (wrap OR podcast OR opinion))&searchIn=title&from='+today+'&sortBy=publishedAt&domains=techcrunch.com,bloomberg.com&language=en&apiKey=ff1d9159b15c46278fbb8727fc0a14a4'
#request = 'https://newsapi.org/v2/everything?q=((web3 OR crypto OR bitcoin OR ethereum OR defi OR tether OR stablecoin OR cardano OR binance OR coinbase OR solana OR dogecoin OR polkadot OR (smart AND contract) OR blockchain OR ICO) AND NOT (wrap OR wrapup OR podcast OR podcasts OR opinion))&searchIn=title&from='+today+'&sortBy=publishedAt&domains=techcrunch.com,bloomberg.com,coindesk.com,wsj.com,nyt.com,reuters.com,ft.com,venturebeat.com,theverge.com,wired.com,engadget.com,gizmodo.com,forbes.com,zerohedge.com,decrypt.co,cointelegraph.com&language=en&apiKey=ff1d9159b15c46278fbb8727fc0a14a4'
#request = 'https://newsapi.org/v2/everything?q=((web3 OR crypto OR bitcoin OR ethereum OR defi OR tether OR stablecoin OR cardano OR binance OR coinbase OR solana OR dogecoin OR polkadot OR (smart AND contract) OR blockchain OR ICO) AND NOT (wrap OR wrapup OR podcast OR podcasts OR opinion))&domains=techcrunch.com,bloomberg.com,coindesk.com,wsj.com,nyt.com,reuters.com,ft.com,venturebeat.com,theverge.com,wired.com,engadget.com,gizmodo.com,forbes.com,zerohedge.com,decrypt.co,cointelegraph.com&from='+today+'&language=en&sortBy=publishedAt&apiKey=ff1d9159b15c46278fbb8727fc0a14a4'
request = 'https://newsapi.org/v2/top-headlines?sources=ars-technica,associated-press,axios,bbc-news,bloomberg,business-insider,cnn,crypto-coins-news,engadget,financial-post,fortune,hacker-news,ign,independent,mashable,new-york-magazine,politico,recode,reuters,techcrunch,the-globe-and-mail,the-huffington-post,the-verge,the-wall-street-journal,the-washington-post,vice-news,wired&apiKey='+key
#request = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=ff1d9159b15c46278fbb8727fc0a14a4'
response = requests.get(request).json()
#print(response)
#print("Total Results: " + str(response['totalResults']))
#print(len(response['articles']))

for i in reversed(response['articles']):
    #print(i['title']+" "+i['publishedAt']+" "+i['source']['name'])
    time = i['publishedAt'][:19]+'Z'
    #calculate publish time delta
    pub = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
    difference = datetime.utcnow().replace(tzinfo=None) - pub
    hours, remainder = divmod(int(difference.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    #print("Published {} hours, {} minutes ago".format(hours, minutes))
    utc_tz = pytz.timezone("UTC")
    dt = utc_tz.localize(pub)
    est_tz = pytz.timezone("America/New_York")
    dt_est = dt.astimezone(est_tz)
    readable_time = dt_est.strftime("%Y-%m-%d %H:%M:%S %Z")

    #make sure not to publish old news
    if hours <= 25:
        #call other methods (local cache and poster)    
        append = {'title': i['title'], 'publishedAt': i['publishedAt'], 'author': i['author'], 'url': i['url'], 'source': i['source']['name'], 'index': 0}
        new = json_tender.write_json(append, 'log.json')
        if new: #tweet if new article
            post.post(append, readable_time)

