from network import Server

def process(req):
    res_data = 'Yeah, thanks for ' + req['data'] 
    
    req['data'] = res_data
    return req

s = Server(process)
s.run()