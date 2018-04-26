from requests_html import HTMLSession
import re
import requests
import json
import os

session = HTMLSession()

resp = session.get('http://bento-shogun.jp/menu/today/')
resp.html.render(sleep=1)

bento_items = resp.html.xpath("//section[@class='item-list']/div[@class='item']")

rm_prefix = 'background-image:url('
rm_suffix = ');'
bentos = [
	{"img": bento.find('div.item-image')[0].attrs["style"].replace(rm_prefix, '').replace(rm_suffix, ''), "name": bento.find('span.item-name')[0].text}
	for bento in bento_items]

MESSAGE = '今日の弁当将軍をお知らせします！ :tada:'

attachments = [{
    "color": "#e4574e",
    "title": bento["name"],
    "image_url": bento["img"]
    } for bento in bentos]

payload = {
	"text": MESSAGE,
	"attachments": attachments}

SLACK_URL = os.environ['SLACK_URL']

requests.post(SLACK_URL, json.dumps(payload))