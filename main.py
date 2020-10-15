import requests
import json
from threadpool import ThreadPool
from queue import Queue
from synchronizer import Syncrhonizer
from network import Server

from concurrent import futures

import pprint
import xmltodict
import yaml
import csv
from io import StringIO
from queue import Queue

pp = pprint.PrettyPrinter(indent=4)
print_json = lambda content: print(json.dumps(content, indent=4))

base_url = 'http://localhost:5000'

results_queue = Queue()

def parse_result(res):
    content = res['data']
    content_type = res['mime_type'] if ('mime_type' in res) else 'application/x-yaml'

    if content_type == 'text/csv':
        f = StringIO(content)
        reader = csv.reader(f, delimiter=',')
        temp = list(reader)
        keys = temp[0]
        content = []
        for row in enumerate(temp[1:]):
            row = row[1]
            bit = {}
            for index, item in enumerate(row):
                bit[keys[index]] = item
            content.append(bit)
    if content_type == 'application/xml':
        content = xmltodict.parse(content)
        content = content['dataset']['record']
    elif content_type == 'application/x-yaml':
        content = yaml.safe_load(content)
    
    return content



def save_result(path, res):
    if 'data' in res:
        path = path.replace('/home', '')
        results_queue.put({
            'path': path,
            'content': parse_result(res)
        })


def make_request(url, **kwargs):
    headers = kwargs.get('headers', {})
    return json.loads(requests.get(url, headers=headers).text)

# Returns isLastNode
def route_request(link, token, pool):
    arr = []
    res = make_request(base_url + link, headers={'X-Access-Token': token})

    def req(link):
        return route_request(link, token, pool)

    if 'data' in res:
        arr.append(res)

    if 'link' in res:
        links = list(res['link'].values())
        children = pool.map(req, links)
        
        for child in children:
            arr += child
    
    return arr

class LocalServer():
    def __init__(self, table):
        self.__table = table
        self.__server = Server(self.__listen)
        self.__server.run()

    def __listen(self, request):
        query = request['data']
        try:
            res = self.__dispatch(query)
            request['data'] = json.dumps(res)
        except:
            pass
        return(request)

    def __dispatch(self, query):
        def select_column(arr):
            res = []
            for item in self.__table:
                if (arr[0] in item):
                    res.append(item[arr[0]])
            return res
        
        query = query.split(' ')
        if query[0] == 'selectColumn':
            return select_column(query[1:])


def main_request(pool):
    r = make_request(base_url + '/register')
    future = pool.submit(route_request, '/home', r['access_token'], pool)
    return future



with futures.ThreadPoolExecutor(max_workers=10) as executor:
    def flatten(l): return [item for sublist in l for item in sublist]
    res = main_request(executor)
    res = list(map(lambda x: parse_result(x), res.result()))
    res = flatten(res)

    


    server = LocalServer(res)
