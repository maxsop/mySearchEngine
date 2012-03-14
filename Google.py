import urllib

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

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


def crawl_web(seed, max_depth, max_pages):
    tocrawl = [seed]
    crawled = []
    depth = 0
    while depth <= max_depth:
    	while tocrawl:
	    current_depth_tocrawl = []
            page = tocrawl.pop()
    	    if page not in crawled:
        	  union(current_depth_tocrawl, get_all_links(get_page(page)))
            if len(crawled) < max_pages:
       		  crawled.append(page)
	depth = depth + 1
	union(tocrawl, current_depth_tocrawl)
    print crawled
crawl_web("http://www.python.org/psf/",1,100)
