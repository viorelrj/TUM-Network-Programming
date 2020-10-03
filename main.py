import requests
import json
from threadpool import ThreadPool
from queue import Queue
from synchronizer import Syncrhonizer

base_url = 'http://localhost:5000'

resultsDict = {
    'data': '',
    'link': {}
}

def saveResult(path, data):
    target = resultsDict
    for step in path:
        if step == '': continue
        if step in target['link']:
            target = target['link'][step]
        else:
            target['link'][step] = {
                'data': '',
                'link': {}
            }
            target = target['link'][step]
    target['data'] = data

def get_to_dict(url, **kwargs):
    headers = kwargs.get('headers', {})
    return json.loads(requests.get(url, headers=headers).text)

# Returns isLastNode
def route_request(link, token):
    res = get_to_dict(base_url + link, headers={'X-Access-Token': token})
    path = link.replace('/home', '').replace('/route', '').replace('/', ' ').split(' ')
    if 'data' in res:
        saveResult(path, res['data'])


    sync = Syncrhonizer(lambda : print('finished on' + link))
    if 'link' in res:
        for l in res['link'].values():
            sync.children.put('')
            pool.add_task(route_request, (l, token), ret= lambda : sync.emit());
    

def main_request():
    r = get_to_dict(base_url + '/register')
    sync = Syncrhonizer(lambda: print('finished on main'))
    sync.children.put('')
    pool.add_task(route_request, ('/home', r['access_token']), ret=lambda : sync.emit())
    




pool = ThreadPool(6)
main_request()


