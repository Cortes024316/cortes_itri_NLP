# get url from 119.33 and check url in 119.25
# extract the emptydata and record the uid of not deleted docs
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
        #print dic_content['lstRet'][0]['ugUrl']
        #print "get!"
        return dic_content
    else:
        global countNodata
        countNodata += 1
        #print "No data"


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
emptydata = []
def storenone(crawljob, url):
    data = {}

    data['ugCrawlJob'] = crawljob
    data['ugUrl'] = url
    data['ugTitle'] = None
    data['ugSearchableWords'] = None

    global emptydata
    #record emptydata
    emptydata.append(data)
    return data

#check emptydata and record the uid of not deleted docs
def checkdelete():
    import sys
    sys.path.append('../')
    from ugDataStore import Ugds
    from ugDataStore import INVALID_UGC_UUID
    uiddata = []#store uiddata of 1 crawljob
    deletecount = 0
    emptycount = 0
    global emptydata
    #for each emptydata
    for i in range(len(emptydata)):
        ugdsHelper = Ugds(crawlJob=emptydata[i]['ugCrawlJob'],isDebug=1)
        docStoredInUgds = ugdsHelper.find(emptydata[i]['ugCrawlJob'],{'ugUrl':emptydata[i]['ugUrl']})

        if docStoredInUgds[0].get('ugDeleted') == 1:
            deletecount += 1
        else:
            emptycount += 1
            #print docStoredInUgds[0]['_id']
            uiddata.append(docStoredInUgds[0]['_id'])
        #print docStoredInUgds[0]['ugUrl']
        #print docStoredInUgds[0]['ugDeleted']
##########print##########
    print "="*50
    #for j in range(len(uiddata)):
    #    print uiddata[j]
    #print "="*50
    print emptydata[0]['ugCrawlJob']
    print "Number of un-index doc:", emptycount
    print "Number of deleted doc:", deletecount
    jobname = emptydata[0]['ugCrawlJob']
    print "="*50
##########print##########
    #output as a json file
    #open(jobname+"_emptydata.json","w").write(json.dumps(uiddata))
    emptydata = []
    

start_time = time.time()
if  __name__ == "__main__":
    #this is for test
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test_delete':
            checkdelete()
            sys.exit()
    #load temp table
    temptable = requests.get("http://100.64.119.33:35001/show/tables")
    table = json.loads(temptable.content)
    tablekeylist = table.keys()
    tablekeylist.sort()
    #for each crawljob in temptable
    for i in range(7,12):#len(tablekeylist)
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
                        #print "No content"
                        reply = storenone(crawljob, get_content['lstRows'][i][0])
                        resultcontent.append(reply)
            else:
                print "No content or need reset"
        #check deleted data
        checkdelete()
####print####
        #print "-"*48
        #print crawljob
        #for i in range(len(resultcontent)):
        #    if not resultcontent[i]['ugSearchableWords']:
        #        print resultcontent[i]['ugCrawlJob']
        #        print resultcontent[i]['ugUrl']
        #        print resultcontent[i]['ugTitle']
        #        print resultcontent[i]['ugSearchableWords']
        #        print "-"*48

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

