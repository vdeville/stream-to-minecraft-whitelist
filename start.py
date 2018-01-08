#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

PROFILES_URL = "https://api.mojang.com/profiles/minecraft"
STREAM_WHITELIST_URL = "https://whitelist.twitchapps.com/list.php?id=warths5657829972d9b&format=json"
WHITELIST_FILE = "whitelist.json"


def _post(url, body, head):
    response = requests.post(url, data=body, headers=head)
    return response.json()


def find_profiles_by_names(names):
    result = []
    pages = [names[i:i + 100] for i in range(0, len(names), 100)]
    for page in pages:
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        body = json.dumps(page)
        result += _post(PROFILES_URL, body, headers)
    return result


def format_uuid(uuid):
    full_uuid = "%s-%s-%s-%s-%s" % (uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])
    return full_uuid


if __name__ == '__main__':
    # Get list from Sub Whitelist
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    request = requests.get(STREAM_WHITELIST_URL, headers=headers)
    if request.status_code == 200:
        result = request.json()
        names = []
        for name in result:
            names.append(result[name]['whitelist_name'])

        list_player = find_profiles_by_names(names)
        whitelist = []
        for player in list_player:
            full_uuid = format_uuid(player['id'])
            whitelist_block = {'uuid': full_uuid, 'name': player['name']}
            whitelist.append(whitelist_block)

        whitelist = json.dumps(whitelist, indent=4)
        try:
            with open(WHITELIST_FILE, 'w') as Whitelist:
                Whitelist.write(whitelist)
                Whitelist.close()
        except:
            print("Error when writing whitelist file")
