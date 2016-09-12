# get url from 119.33 and check url in 119.25
# store the content of every url for checking correctness
# 4 space
import requests
import json
import time
#get urls of doc
def get_response(url):
    r = requests.get(url)
    dic_content = json.loads(r.content)
    
    return dic_content


countdata = 0
countNodata = 0
#check the correctness of indexed data in database and return content of url
def check_url(checkurl, params):
    r = requests.get(checkurl, params=params)
    dic_content = json.loads(r.content)
    if dic_content['lstRet']:
        global countdata
        countdata += 1
        print dic_content['lstRet'][0]['ugUrl']
        print "get!"
        return dic_content
    else:
        global countNodata 
        countNodata += 1
        print "No data" 


lost = {"ugCrawlJob":0, "ugUrl":0, "ugTitle":0, "ugSearchableWords":0}
#store data
#key not exist => give [] 
def storedata(content, keylist):
    data = {}

    for key in keylist:
        if content['lstRet'][0].has_key(key):
            data[key] = content['lstRet'][0][key].encode('UTF8')
        else:
            data[key] = []
            lost[key] += 1 

    return data
#data not exist => give None
def storenone(crawljob, url):
    data = {}

    data['ugCrawlJob'] = crawljob
    data['ugUrl'] = url
    data['ugTitle'] = None
    data['ugSearchableWords'] = None

    return data

start_time = time.time()
if  __name__ == "__main__":
    parker = "http://100.64.119.33:35001"
    #load temp table
    temptable = requests.get(parker+"/show/tables")
    table = json.loads(temptable.content)
    tablekeylist = table.keys()
    tablekeylist.sort()
    #for each crawljob in temptable
    for i in range(0,1):#len(tablekeylist)
        #numbers of data in one request
        rows = "1000"
        print tablekeylist[i]
        print table[tablekeylist[i]]['data_statement']
        crawljob = table[tablekeylist[i]]['data_statement']
        reseturl = "http://100.64.119.33:35001/iterrows/"+tablekeylist[i]+"/"+rows+"?yesImSureIwannaResetTheIterator=1"
        geturl = "http://100.64.119.33:35001/iterrows/"+tablekeylist[i]+"/"+rows+"?csvColumns=ugUrl"
        checkurl = "http://100.64.119.25:45000/doSearchUrl"
        #collect data of 1 crawljob and store in resultcontent
        resultcontent = []
        keylist = ["ugCrawlJob", "ugUrl", "ugTitle", "ugSearchableWords"]

        #reset
        print requests.get(reseturl)

        while int(rows) == 1000:
            get_content = get_response(geturl)
            rows = int(get_content['numRows'])
            if rows != 0:
                for i in range(0, rows):
                    params = {'url':get_content['lstRows'][i][0]}
                    content = check_url(checkurl, params)
                    #store data or give None
                    if content:
                        reply = storedata(content, keylist)
                        resultcontent.append(reply)
                    else:
                        print "No content"
                        reply = storenone(crawljob, get_content['lstRows'][i][0])
                        resultcontent.append(reply)
            else:
                print "No content or need reset"

        #Output as a json file
        #open(crawljob+".json","w").write(json.dumps(resultcontent))
####print####
        print "-"*48
        print crawljob
        for i in range(len(resultcontent)):
            print resultcontent[i]['ugCrawlJob']
            print resultcontent[i]['ugUrl']
            print resultcontent[i]['ugTitle']
            print resultcontent[i]['ugSearchableWords']
            print "-"*48

        print "Get data:", countdata
        print " No data:", countNodata
        print "Total:", countdata + countNodata
        print "Total in result:", len(resultcontent)
        print "-"*48
        global countdata
        global countNodata
        countdata=0
        countNodata=0

        print "lost: ", lost
        global lost
        lost = {"ugCrawlJob":0, "ugUrl":0, "ugTitle":0, "ugSearchableWords":0}
        print "-"*48
####print####
print time.time() - start_time, "seconds"

