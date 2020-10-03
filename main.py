import requests
import json
from threadpool import ThreadPool
from queue import Queue
from synchronizer import Syncrhonizer

import pprint

base_url = 'http://localhost:5000'

resultsDict = {
    'data': '',
    'link': {}
}

results_dict = {}

def save_result(path, res):
    if 'data' in res:
        path = path.replace('/home', '')
        results_dict[path] = res['data']

def get_to_dict(url, **kwargs):
    headers = kwargs.get('headers', {})
    return json.loads(requests.get(url, headers=headers).text)

# Returns isLastNode
def route_request(link, token, sync):
    res = get_to_dict(base_url + link, headers={'X-Access-Token': token})
    save_result(link, res)

    if 'link' in res:
        for l in res['link'].values():
            sync.add_dependency()
            pool.add_task(route_request, (l, token, sync))
    sync.emit()


def main_request(pool):
    def callback():
        pool.close()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results_dict)

    r = get_to_dict(base_url + '/register')
    sync = Syncrhonizer(lambda: callback())
    sync.add_dependency()
    pool.add_task(route_request, ('/home', r['access_token'], sync))

pool = ThreadPool(6)
main_request(pool)


