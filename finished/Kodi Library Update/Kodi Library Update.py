# Watcher Plugin to instruct Kodi to update library
# Trigger: Post-processing Finished

import sys
import os
import json
import urllib2

script, title, year, imdbid, resolution, rated, original_file, new_file_location, downloadid, finished_date, conf_json = sys.argv

scan_dir = os.path.splitpath('new_file_location')[0]

conf = json.loads(conf_json)
user = conf['User Name']
password = conf['Password']
kodi_address = conf['IP Address']
kodi_port = conf['Port']


if user:
    url = u'http://{}:{}@{}:{}/jsonrpc'.format(user, password, kodi_address, kodi_port)
else:
    url = u'http://{}:{}/jsonrpc'.format(kodi_address, kodi_port)

post_data = json.dumps({'jsonrpc': '2.0',
                        'id': 0,
                        'method': 'VideoLibrary.Scan',
                        'params': {'directory': scan_dir}
                        })

headers = {'User-Agent': 'Watcher'}

request = urllib2.Request(url, post_data, headers=headers)

try:
    response = json.loads(urllib2.urlopen(request))
    if response['result'] == 'OK':
        print 'KODI Response: "OK"'
        sys.exit(0)
    else:
        print 'KODI Response: {}'.format(response['result'])
except Exception, e:
    print str(e)
    sys.exit(1)

sys.exit(0)