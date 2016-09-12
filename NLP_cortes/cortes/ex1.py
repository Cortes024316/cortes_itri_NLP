# example 1
import requests
import json

def test_info():
    r = requests.get("http://100.64.119.33:35000/info")
    print dir(r) 
    print r.headers['content-type']
    print r.url
    print r.content,type(r.content)
    res = r.content
    #print res
    dic1 = json.loads(res)
    print dic1, type(dic1) 

if __name__ == "__main__":
    print "---test line---"
    test_info()
    print "---test line---"
