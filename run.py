import json
import os
import re
import requests
import sys


def _download(url, out=None):
    r = requests.get(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        },
        stream=bool(out),
        timeout=30,
    )
    if not out:
        return r.text
    with open(out, 'wb') as f:
        for _ in r.iter_content(4096):
            f.write(_)


if len(sys.argv) != 2:
    print('  Usage: python {} <issuu_url>'.format(sys.argv[0]))

html = _download(sys.argv[1])

config = re.search('({"config".+?});', html, re.DOTALL)
if not config:
    exit('Unable to find publication data')

j = json.loads(config.group(1))['document']

print('{}\n{}'.format(j['title'], '-' * len(j['title'])))

for i in range(1, j['pageCount'] + 1):
    print('Downloading page {}/{}'.format(i, j['pageCount']))
    url = 'https://image.isu.pub/{}/jpg/page_{}.jpg'.format(j['id'], i)
    _download(url, os.path.join(os.getcwd(), '{}-page{}.jpg'.format(j['documentName'], i)))

print ('{}\nFinished!'.format('-' * len(j['title'])))
