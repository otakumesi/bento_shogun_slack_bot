import requests_html
import requests
import json
import os
import feedparser

SLACK_URL = os.environ['SLACK_URL']

def post_bento_list_to_slack(bento_list):
    MESSAGE = '今日のヘルシースタンドをお知らせします！ :tada: https://www.healthy-stand-japan.com/blog'

    attachments = [{
        "color": "#e4574e",
        "title": bento["name"],
        "image_url": bento["img"]
        } for bento in bento_list]

    payload = {
        "text": MESSAGE,
        "attachments": attachments}

    requests.post(SLACK_URL, json.dumps(payload))


def get_bento_list():
    rss = feedparser.parse('https://www.healthy-stand-japan.com/blog/feed.rss')
    url = rss['items'][0]['link']
    url = 'https://www.healthy-stand-japan.com/blog/2018/7/17'
    session = requests_html.HTMLSession()
    resp = session.get(url)
    brands = resp.html.find('h2')[0:2]
    names = resp.html.find('h3')[0:2]
    imgs = resp.html.find('p img')[0:2]

    bentos = [
        {"img": img.attrs['src'], "name": name.text + ' (' + brand.text + ')'}
        for brand, name, img in zip(brands, names, imgs)]
    return  bentos

if __name__=='__main__':
    bento_list = get_bento_list()
    post_bento_list_to_slack(bento_list)
