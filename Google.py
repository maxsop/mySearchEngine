import urllib

### Getting url pages from the web ###
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

### Getting all links from the url pages ###
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

### Indexing the web ####
# index = [keyword, [url],[url]...]
def add_to_index(index, keyword, url):
    for entry in index:
	if entry[0] == keyword:
	   entry[1].append(url)
	   return
    index.append([keyword, [url]])#add new entry if keyword not in index

def lookup_index(index, keyword):
    for entry in index:
	if entry[0] == keyword:
	   return entry[1]
    return []
	   
def add_page_to_index(index, url, content):#rebulding or updating the the web index
	words = content.split()
	for word in words:
		add_to_index(index, word, url) 

### Building the web crawler ###
def crawl_web(seed, max_depth, max_pages):
    tocrawl = [seed]
    crawled = []
    index =[]
    depth = 0
    while depth <= max_depth:
    	while tocrawl:
	    current_depth_tocrawl = []
            page = tocrawl.pop()
    	    if page not in crawled:
		content = get_page(page)
		add_page_to_index(index, page, content)
        	union(current_depth_tocrawl, get_all_links(content))
            if len(crawled) < max_pages:
       		  crawled.append(page)
	depth = depth + 1
	union(tocrawl, current_depth_tocrawl)
    return index
   # print crawled
print lookup_index(crawl_web("http://www.python.org/", 1, 100), 'good')
