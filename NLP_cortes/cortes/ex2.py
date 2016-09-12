# exercise2
import requests
import json

def test_echo_get():#test API echo by get
    payload = {'key1':'value1', 'key2':'value2'}
    r = requests.get("http://100.64.119.33:35000/echo", params=payload)
    print type(payload)
    print r.url
    print r.headers['content-type']
    r_temp = r.content
    print r_temp
    dic1 = json.loads(r_temp)
    print dic1, type(dic1)
    

def test_function():#just for test
    verbs = requests.options('http://100.64.119.33:35000/echo')
    print verbs.headers['allow']

def test_echo_post():#test API echo by post
    payload = {'key1':'value1', 'key2':'value2'}
    print type(payload)
    headers = {'content-type': 'application/json'}
    r = requests.post("http://100.64.119.33:35000/echo", data=json.dumps(payload), headers=headers) 
    print r.content, type(r.content)
    r_temp = r.content
    dic1 = json.loads(r_temp)
    print dic1, type(dic1)

if  __name__ == "__main__":
    
    print "------this is a line------"
    test_echo_get()
    test_echo_post()
    print "------this is a line------"
