#MultiIP test
# 4 space
import requests
import json


def test_info(ip, port):
    r = requests.get("http://"+ip+":"+port+"/info")
    res = r.content
    dic = json.loads(res)#change to dic
    #print dic
    return dic

def test_echo(ip, port):
    payload = {'key1':'value1', 'key2':'value2'}
    headers = {'content-type': 'application/json'}
    r_get = requests.get("http://"+ip+":"+port+"/echo", params=payload)
    r_post = requests.post("http://"+ip+":"+port+"/echo", data=json.dumps(payload), headers=headers)
    dic_get = json.loads(r_get.content)
    dic_post = json.loads(r_post.content)
    print dic_get
    print dic_post
    return "==="

def test_fapps(ip, port):#test API fapps by get
    r = requests.get("http://"+ip+":"+port+"/fapps")
    res = r.content
    dic = json.loads(res)
    
    return dic

def test_function():#just for test
    print "test"

IPcontent = []
#[
#    'ip:port':{ 'info':{}, "fapps":{} },
#    'ip:port':{ 'info':{}, "fapps":{} },
#    ...
#]
def storecontent(ip, port, dic_info, dic_fapps):
    global IPcontent
    data_dict = {}
    data_dict[ip+':'+port] = {'info':dic_info, 'fapps':dic_fapps}
    IPcontent.append(data_dict)
    #IPcontent[ip+':'+port] = {'info':dic_info, 'fapps':dic_fapps}
    #print IPcontent
    return IPcontent

def sortbyvalue(listdic, listIPport, API, key):#exist or not?
    valuelist = []    
    for dic in listdic:
        for ip, port in listIPport:
            if dic.has_key(ip+':'+port):
                valuelist.append(dic[ip+':'+port][API][key])

    valuelist.sort()
    resultlistdic = []

    for value in valuelist:#duplicated value?has_no_key
        for dic in listdic:
            for ip, port in listIPport:
                if dic.has_key(ip+':'+port):
                    if dic[ip+':'+port][API][key] == value:
                        resultlistdic.append(dic)

    return resultlistdic
                        

if  __name__ == "__main__":

    listIPport = [('100.64.119.26','80'),('100.64.119.32','35000'),('100.64.119.34','25000')]
    for ip, port in listIPport:
        print "-"*40
        print ip+":"+port
        dic_info =  test_info(ip, port)
        dic_fapps =  test_fapps(ip, port)
        #store content
        listofdic_now = storecontent(ip, port, dic_info, dic_fapps)
        for dic in listofdic_now:
            for ip, port in listIPport:
                if dic.has_key(ip+':'+port):
                    print "OK."
        print "-"*40

    sorteddic = sortbyvalue(listofdic_now, listIPport, 'fapps', 'used')

    for dic in sorteddic:
        for ip, port in listIPport:
            if dic.has_key(ip+':'+port):
                print ip+':'+port+": "+dic[ip+':'+port]['fapps']['used']

    




#    test_function()
