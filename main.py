import requests
import json
from threadpool import ThreadPool
from queue import Queue
from synchronizer import Syncrhonizer

import pprint
import xmltodict
import yaml
import csv
from io import StringIO

pp = pprint.PrettyPrinter(indent=4)

base_url = 'http://localhost:5000'

resultsDict = {
    'data': '',
    'link': {}
}

results_dict = {}

def parse_result(content, type):
    pass
    # if type == 'text/csv':
    #     # return csv.reader(StringIO(content), delimiter='')
    #     pass
    if type == 'application/xml':
        content = xmltodict.parse(content)
        # print(json.dumps(content, indent=4))
        # return content
    # elif type == 'application/x-yaml':
    #     content = yaml.parse(content)
    #     print(json.dumps(content, indent=4))
    #     return content
    # elif type == 'application/json':
    #     pass
    # else:
    #     raise Exception("Content type unknown")

def save_result(path, res):
    if 'data' in res:
        path = path.replace('/home', '')
        results_dict[path] = res['data']

        if 'mime_type' in res:
            parse_result(res['data'], res['mime_type'])

def make_request(url, **kwargs):
    headers = kwargs.get('headers', {})
    return json.loads(requests.get(url, headers=headers).text)

# Returns isLastNode
def route_request(link, token, sync, pool):
    res = make_request(base_url + link, headers={'X-Access-Token': token})
    save_result(link, res)

    if 'link' in res:
        for l in res['link'].values():
            sync.add_dependency()
            pool.add_task(route_request, (l, token, sync, pool))
    sync.emit()


def main_request(pool):
    def callback():
        print('hello')
        pool.close()

    r = make_request(base_url + '/register')
    sync = Syncrhonizer(lambda: callback())
    sync.add_dependency()
    pool.add_task(route_request, ('/home', r['access_token'], sync, pool))

pool = ThreadPool(6)
main_request(pool)


