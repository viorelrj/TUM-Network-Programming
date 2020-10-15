import requests
import json
from threadpool import ThreadPool
from queue import Queue
from synchronizer import Syncrhonizer
from network import Server

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
def route_request(link, token, sync, pool):
    res = make_request(base_url + link, headers={'X-Access-Token': token})
    save_result(link, res)

    if 'link' in res:
        for l in res['link'].values():
            sync.add_dependency()
            pool.add_task(route_request, [l, token, sync, pool])
    sync.emit()


def make_table(src):
    def empty_row(keys):
        result = {}
        for item in keys:
            result[item] = None
        return result

    key_list = set()
    for item in src:
        for key in item:
            key_list.add(key)
    
    table = []
    for item in src:
        entry = empty_row(key_list)
        for key in item:
            entry[key] = item[key]
        table.append(entry)


class LocalServer():
    def __init__(self, table):
        self.__table = table
        self.__server = Server(self.__listen)
        self.__server.run()
        print('created server')

    def __listen(self, request):
        query = request['data']
        self.__dispatch(query)
        return(request)

    def __dispatch(self, query):
        def select_column(arr):
            res = []
            for item in self.__table:
                print(item)
                if (arr[0] in item):
                    res.append(item[arr[0]])
            print(res)


def main_request(pool):

    def callback():
        res = []
        pool.close()
        while (results_queue.qsize() != 0):
            res.append(results_queue.get()['content'])
        res = [item for sublist in res for item in sublist]
        LocalServer(res)



    r = make_request(base_url + '/register')
    sync = Syncrhonizer(lambda: callback())
    sync.add_dependency()
    pool.add_task(route_request, ['/home', r['access_token'], sync, pool])

pool = ThreadPool(6)
main_request(pool)

# server = LocalServer([])
