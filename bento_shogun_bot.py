import requests_html
import re
import requests
import json
import os


SLACK_URL = os.environ['SLACK_URL']


def post_bento_list_to_slack(bento_list):
    MESSAGE = '今日の弁当将軍をお知らせします！ :tada:'
    
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
    session = requests_html.HTMLSession()
    resp = session.get('http://bento-shogun.jp/menu/today/')
    resp.html.render(sleep=1)
    
    bento_items = resp.html.xpath("//section[@class='item-list']/div[@class='item']")
    
    rm_prefix = 'background-image:url('
    rm_suffix = ');'
    bentos = [
    	{"img": bento.find('div.item-image')[0].attrs["style"].replace(rm_prefix, '').replace(rm_suffix, ''), "name": bento.find('span.item-name')[0].text}
    	for bento in bento_items]
    return  bentos

if __name__=='__main__':
    bento_list = get_bento_list()
    post_bento_list_to_slack(bento_list)
