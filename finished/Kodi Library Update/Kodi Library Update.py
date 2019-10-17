#!/usr/bin/env/python3
# Watcher Plugin to instruct Kodi to update library
# Trigger: Post-processing Finished

import sys
import os
import json
import urllib.request

script, title, year, imdbid, resolution, rated, original_file, new_file_location, downloadid, finished_date, quality, conf_json = sys.argv

conf = json.loads(conf_json)
user = conf['username']
password = conf['password']
kodi_address = conf['address']
kodi_port = conf['port']


if user:
    url = u'http://{}:{}@{}:{}/jsonrpc'.format(user, password, kodi_address, kodi_port)
else:
    url = u'http://{}:{}/jsonrpc'.format(kodi_address, kodi_port)

directory = os.path.dirname(new_file_location)
if 'map_from' in conf and 'map_to' in conf and conf['map_from'] and conf['map_to']:
    directory = directory.replace(conf['map_from'], conf['map_to'])

post_data = json.dumps({
                        'jsonrpc': '2.0',
                        'id': 0,
                        'method': 'VideoLibrary.Scan',
                        'params': {
                            'directory': directory
                        }
                       })

headers = {'User-Agent': 'Watcher', 'Content-Type': 'application/json'}

request = urllib.request.Request(url, post_data.encode('utf-8'), headers=headers)

try:
    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode('utf-8'))
    if result['result'] == 'OK':
        print('KODI Response: "OK"')
        sys.exit(0)
    else:
        print('KODI Response: {}'.format(result['result']))
except Exception as e:
    print(str(e))
    sys.exit(1)

sys.exit(0)
