# Combination of checkurl.py, checkwordindex.py, verifyindex.py
# 4 space
import requests
import json
import time
import re
import sys
from ConfigParser import ConfigParser
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

# 1 resultcontent = 1 crawljob
# extract words, split by space. Word post to /dosearch to search corresponding urls which contain the word
def checkwordindex(resultcontent):
    truecount = 0
    falsecount = 0
    indexresult = []#store result of word index in 1 crawljob [list of dic]
    key_numurl = {} #{ key : number of url in database }
    falsewords = []
    falseurl = []
    #for each url data in resultcontent
    for i in range(len(resultcontent)):
        #temporary store string of words
        words = ""
        if resultcontent[i]['ugSearchableWords']:
            words = resultcontent[i]['ugSearchableWords'].split(" ")
            #words = re.split('[ ,]+', resultcontent[i]['ugSearchableWords'])
        url = resultcontent[i]['ugUrl']
        #store info of 1 url
        dicinfo = {}
        dicinfo['ugCrawlJob'] = resultcontent[i]['ugCrawlJob']
        dicinfo['ugUrl'] = resultcontent[i]['ugUrl']
        dicinfo['words'] = []
        dicinfo['result'] = []
        #for each word from 1 url
        for j in range(len(words)):
            #print "-"*40
            #print words[j]
            #check the urls which include words[j]
            payload = {'pattern':words[j], 'countOnly':0, 'strCrawlJob':''}
            headers = {'content-type': 'application/json'}
            r = requests.post("http://100.64.119.25:45000/doSearch", data=json.dumps(payload), headers=headers, timeout=100)
            #print r
            dic = json.loads(r.content)
            #store number of url of this word
            if key_numurl.has_key(words[j]):
                pass
            else:
                key_numurl[words[j]] = len(dic['lstOut'])
            #check the corresponding url is exist or not
            exist = False
            for k in range(len(dic['lstOut'])):
                if dic['lstOut'][k]['ugUrl'] == url:
                    exist = True
                    truecount += 1
                    #print words[j], ":True"
                    break
            if exist == False:
                falsecount += 1
                #print words[j], ":False"
                falsewords.append(words[j])
                falseurl.append(resultcontent[i]['ugUrl'])
            #store existence of this word
            dicinfo['words'].append(words[j])
            dicinfo['result'].append(exist)
        #store info into indexresult
        indexresult.append(dicinfo)
    #Output as json file
    open(crawljob+"_result.json","w").write(json.dumps(indexresult))
    open(crawljob+"_keynum.json","w").write(json.dumps(key_numurl))
###########print###########
#    print "="*40
#    for i in range(len(indexresult)):
#        print "Crawljob:", indexresult[i]['ugCrawlJob']
#        print "Url:", indexresult[i]['ugUrl']
#        print "Words:", indexresult[i]['words']
#        print "Result:", indexresult[i]['result']
#    print "="*40
#    klist = key_numurl.keys()
#    for key in klist:
#        print key, ":", key_numurl[key]
#    print "="*40
#    print "true:", truecount
#    print "false:", falsecount
#    print falsewords, type(falsewords[0])
#    for url in range(len(falseurl)):
#        print falseurl[url]
###########print###########

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
    #print "="*50
    #for j in range(len(uiddata)):
    #    print uiddata[j]
    #print "="*50
    #if emptydata:
    #    print emptydata[0]['ugCrawlJob']
    #    print "Number of un-index doc:", emptycount
    #    print "Number of deleted doc:", deletecount
    #print "="*50
##########print##########
    #output as a json file
    if emptydata:
        jobname = emptydata[0]['ugCrawlJob']
        open(jobname+"_emptydata.json","w").write(json.dumps(uiddata))
    else:
        print "No empty data!"
    emptydata = []


start_time = time.time()
#python blackjack.py [crawljob] [action] [rows(optional)]
if  __name__ == "__main__":
    # instantiate
    config = ConfigParser()
    # parse existing file
    config.read('initial.ini')
    # read values from a section
    crawljob_ini = config.get('section_a', 'crawljob')
    action_ini = config.get('section_a', 'action')
    data_apps = config.get('section_a', 'data_apps')
    Lucas = config.get('section_a', 'Lucas')
    numRows_ini = config.get('section_a', 'numRows')
###
    if len(sys.argv) == 3:
        if sys.argv[1]:
            crawljob_ini = sys.argv[1]
        if sys.argv[2]:
            action_ini = sys.argv[2]
    elif len(sys.argv) == 4:
        if sys.argv[1]:
            crawljob_ini = sys.argv[1]
        if sys.argv[2]:
            action_ini = sys.argv[2]
        if sys.argv[3]:
            numRows_ini = sys.argv[3]
    else:
        print "Error input!"
        print "python blackjack.py [crawljob] [action] [rows(optional)]"
        sys.exit()
###
    #action exist or not
    if action_ini == "checkurl" or action_ini == "checkwordindex" or action_ini == "verifyindex":
        pass
    else:
        print action_ini
        print "Wrong action!"
        sys.exit()
    #rows > 0
    if int(numRows_ini) <= 0:
        print "Error numRows!"
        sys.exit()
    #load temp table
    _t = "_t1000"#defualt
    temptable = requests.get("http://100.64.119.160:35001/show/tables")
    table = json.loads(temptable.content)
    tablekeylist = table.keys()
    tablekeylist.sort()
    for i in range(len(tablekeylist)):
        if table[tablekeylist[i]]['data_statement'] == crawljob_ini:
            crawljob = table[tablekeylist[i]]['data_statement']
            _t = tablekeylist[i]
            break
    if _t == "_t1000":
        print "No corresponding crawljob!"
        sys.exit()
    #numbers of data in one request
    numRows = int(numRows_ini)
    print _t
    print crawljob
    reseturl = "http://100.64.119.160:35001/iterrows/"+_t+"/"+numRows_ini+"?yesImSureIwannaResetTheIterator=1"
    geturl = "http://100.64.119.160:35001/iterrows/"+_t+"/"+numRows_ini+"?csvColumns=ugUrl"
    checkurl = "http://100.64.119.25:45000/doSearchUrl"
    #collect data of 1 crawljob and store in resultcontent
    resultcontent = []
    keylist = ["ugCrawlJob", "ugUrl", "ugTitle", "ugSearchableWords"]

    #reset
    print requests.get(reseturl)

    while numRows == int(numRows_ini):
        get_content = get_response(geturl)
        numRows = int(get_content['numRows'])
        if numRows != 0:
            for i in range(0, numRows):
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

    if action_ini == 'checkurl':
        #Output as a json file
        open(crawljob+".json","w").write(json.dumps(resultcontent))
        print "Done!"
        print time.time() - start_time, "seconds"
        sys.exit()
    elif action_ini == 'checkwordindex':
        checkwordindex(resultcontent)
        print "Done!"
        print time.time() - start_time, "seconds"        
        sys.exit()
    elif action_ini == 'verifyindex':
        #check deleted data
        checkdelete()
        print "Done!"
        print time.time() - start_time, "seconds"
        sys.exit()
		
####print####
#    print "-"*48
#    print crawljob
#    for i in range(len(resultcontent)):
#        print resultcontent[i]['ugCrawlJob']
#        print resultcontent[i]['ugUrl']
#        print resultcontent[i]['ugTitle']
#        print resultcontent[i]['ugSearchableWords']
#        print "-"*48

#    print "Get data:", countdata
#    print " No data:", countNodata
#    print "Total:", countdata + countNodata
#    print "Total in result:", len(resultcontent)
#    print "-"*48
#    global countdata
#    global countNodata
#    countdata=0
#    countNodata=0

#    print "lost: ", lost
#    global lost
#    lost = {"ugCrawlJob":0, "ugUrl":0, "ugTitle":0, "ugSearchableWords":0}
#    print "-"*48
####print####
print time.time() - start_time, "seconds"


