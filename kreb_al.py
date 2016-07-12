#I change something here for create a branch

#encoding:UTF-8

import urllib2 , re , pymongo ,sys

client = pymongo.MongoClient("localhost",27017)
db     = client.III
naked  = db.krebsonsecurity

def grab_page(href):
	#input a href , use urllib2 to grab all content
	req = urllib2.Request(href)
	res = urllib2.urlopen(req).read()
	
	return res

def grab_content(page):
	#input a page content , re processing , then return main content in page
	page = re.sub(r"\<a\s.*?>","",page)	
	page = re.sub(r"\<img\s.*?>","",page)	
	page = re.sub(r"\</a>","",page)	

	pattern = re.compile(r"\<div\sclass=\"entry\">[\s\r\n\t]*([\S\s\"\<>\t\n\r]*)\<!--\sYou")
	main    = pattern.findall(page)
	if len(main) > 0 :
		main    = main[0]

		main = re.sub(r"\<small>[\s\S\n\t\"]*\</small>","",main)
		main = re.sub(r"\n","",main)
		main = re.sub(r"\r","",main)
		main = re.sub(r"\t","",main)
		main = re.sub(r"\<.*?>","",main)
		main = re.sub(r"\<p.*?>","",main)
		main = re.sub(r"\</p>","",main)
		main = re.sub(r"\<div.*?>","",main)
		main = re.sub(r"\</div>","",main)

		return main
	else :
		return []

def grab_title(page):
	#input a page content , re processing , then return title in page
	pattern = re.compile(r"\<h2\sclass=\"post-title\">(.*?)\</h2>")
	title   = pattern.findall(page)
	return title[0]

def grab_href(page):
	#input a page content , re processing , then return href list
	pattern = re.compile(r"\"(http://krebsonsecurity.com/[0-9]*?/[0-9]*?/.*?/)\"")
	hrefs   = pattern.findall(page)
	return hrefs

def grab_date(href):
	#input a href , re processing , then return page's date
	req  = urllib2.Request(href)
	res  = urllib2.urlopen(req).read()
	ym_pattern   = re.compile(r"http://\S*/([0-9]*/[0-9]*/)\S*/")
	year_mon  = ym_pattern.findall(href)
	d_pattern = re.compile(r"\<span\sclass=\"date\">([0-9]*)\</span>")
	day = d_pattern.findall(res)
	posted_at = year_mon[0]+day[0]
	return posted_at

def grab_msg(page):
	#input a page content , re processing , then return all msgs
	return msg

def grab_terms(content):
	#input a cleaned text , re processing , then return terms list

	pattern = re.compile(r"[0-9a-zA-Z]{2,}")
	terms   = pattern.findall(content)

	return terms

def testing(href):
	try:
		urllib2.urlopen(href)
		return True
	except Exception:
		return False

for day in range(50):
	day    = day + 1
	target = "http://krebsonsecurity.com/2014/page/"+str(day)+"/"
	if testing(target) :
		page = grab_page(target)
		hrefs = grab_href(page)
		print "cur:",day
		for href in hrefs :
			cur_page    = grab_page(href)
			if naked.find({'href':href}).count() == 0 :
				title   = grab_title(cur_page)
				content = grab_content(cur_page)
				terms = grab_terms(content)
				posted_at = grab_date(href)
				print "Now inserting ..."+title
				post = {
					'title'     : title,
					'href'		: href ,
					'content'   : content, 
					'terms'     : terms ,
					'posted_at' : posted_at
				}
				naked.insert(post)
		print "done:",day 
	else :
		print target

