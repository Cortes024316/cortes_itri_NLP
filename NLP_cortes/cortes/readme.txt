###
Readme document for python files in ~/nlp/cortes/
Author: Cortes
E-mail: briamoter951852@gmail.com
Date: 2016/08/30
###
---------------------------------------------------------------
[checkurl.py]
request urls from data_apps webservice and check the content of url in Lucas

-input:
  #change crawljob:
  change the number in range() in line 67 to fit the corresponding crawljob in temp table crawljob list

  #change rows(optional):
  change the rows in line 69 to adjust the number of url in one request

-output:
  #output as a file: crawljob.json (line 102)
  resultcontent format: list of dict
  [
    {
      'ugCrawlJob': "",
      'ugUrl': "",
      'ugTitle': "",
      'ugSearchableWords': "",
    },
    ...
  ]
---------------------------------------------------------------
[checkwordindex.py]
check the index correctness of url which contain specific words
record the number of urls which contain a specific word

-input:
  #change crawljob:
  change the number in range() in line 144 to fit the corresponding crawljob in temp table crawljob list

  #change rows(optional):
  change the rows in line 146 to adjust the number of url in one request

-output:
  #output as a file: crawljob_result.json (line 115)
  indexresult format: list of dict
  [
    {
      'ugCrawlJob': "",
      'ugUrl': "",
      'words': [abc, def, ...],
      'result': [True, True, False],
    },
    ...
  ]
  #output as a file: crawljob_keynum.json (line 116)
  key_numurl format: dict
  {
    'word1': 30,
    'word2': 20,
    ...
  }
---------------------------------------------------------------
[verifyindex.py]
empty data is not indexed in Lucas. Some empty data are deleted, some are not
Find the empty data which is not deleted

-input:
  #change crawljob:
  change the number in range() in line 115 to fit the corresponding crawljob in temp table crawljob list

  #change rows(optional):
  change the rows in line 117 to adjust the number of url in one request

-output:
  #output as a file: crawljob_emptydata.json (line 97)
  uiddata format: list
  [
    'uid1', 'uid2', 'uid3', ...
  ]
---------------------------------------------------------------
[blackjack.py]
combination of checkurl.py, checkwordindex.py, verifyindex.py

-input:
  #modify the parameter in initial.ini
   execute file: python blackjack.py

  #input parameter when execute file
   execute file: python blackjack.py [crawljob] [action] [rows(optional)]
   [crawljob]: the corresponding crawljob need to be loaded into temp table crawljob list
   [action]: checkurl, checkwordindex, verifyindex, corresponding to the functions in checkurl.py, checkwordindex.py, verifyindex.py
   [rows(optional)]: rows should > 0

-output:
  Please reference the output in checkurl.py, checkwordindex.py, verifyindex.py corresponding to different action
---------------------------------------------------------------
[ex1.py, ex2.py, fapps_ex.py, test_multiIP.py, unittest_combine.py, itestfunctionhere.py]
some practice and test file, not important
