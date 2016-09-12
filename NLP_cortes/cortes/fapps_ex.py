#p exercise fapps
import requests
import json

def test_fapps_get():#test API fapps by get
    r = requests.get('http://100.64.119.33:'+'35000'+'/fapps')
    res = r.content
    dic = json.loads(res)
    
    keylist = dic.keys()
    keylist.sort()
    for index in range(len(keylist)):
        #1
        r_get = requests.get('http://100.64.119.33:'+'35000'+'/fapps', params={keylist[index]: dic[keylist[index]]})
        #2
        dic_get = json.loads(r_get.content)
        #3
        print "TimediffFromLastCall: ", dic_get['DBG_TimediffFromLastCall']
        print "total: ", dic_get['total']
        print "used: ", dic_get['used']

def test_function():#just for test
    r = requests.get('http://100.64.119.33:35000/fapps')
    #print dir(r)
    #print r.content
    res = r.content
    dic = json.loads(res)
    keylist = dic.keys()
    for index in range(len(keylist)):
        print keylist[index]


if  __name__ == "__main__":

    print "------this is a line------"
    #test_function()
    test_fapps_get()
    print "------this is a line------"

