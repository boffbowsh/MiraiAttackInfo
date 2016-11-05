from __future__ import print_function

import re, socket

from ipwhois import IPWhois
import tweepy

def lambda_handler(event, context):
    m = re.search(r"([0-9]{1,3}\.){3}[0-9]{1,3}", event['text'])
    if m:
        ip = m.group(0)
        whois = IPWhois(ip).lookup_rdap(depth=1)
        try:
            host, _, _ = socket.gethostbyaddr(ip)
            reverse = "Hostname: %s\n" % host
        except:
            reverse = ""

        status = "Whois name: %s\n%s%s" % (whois['network']['name'], reverse, event['url'])

        auth = tweepy.OAuthHandler(event['consumer_key'], event['consumer_secret'])
        auth.set_access_token(event['access_key'], event['access_secret'])
        api = tweepy.API(auth)
        api.update_status(status)
