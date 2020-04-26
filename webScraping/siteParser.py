import urllib3, re, html
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib3.exceptions import HTTPError
from io import StringIO


locToGet = ''
pageData = None
errMsg = None
soup = None
msgOutput = True

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def loadAddress(address): 
    locToGet = address
    htmatch = re.compile('.*http.*')
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3;rv:36.0) Gecko/20100101 Firefox/36.0'}
    if(htmatch.match(locToGet) is None):
        locToGet = "http://" + locToGet
    if(len(locToGet) > 5):
        if(msgOutput):
            print("Ready to load page data for: " + locToGet + "which was derived from " + address)
        try:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager(2, headers=user_agent)
            r = http.request('GET', locToGet)
            pageData = r.data
            if(msgOutput):
                print("Page data loaded OK")
        except:
            if(msgOutput):
                print("Problem loading the page")
            return("Problem loading the page")
    extractText = ''
    soup = BeautifulSoup(pageData, 'html.parser')
    ttexts = soup.findAll(text=True)
    viz_text = filter(tag_visible, ttexts)
    allVisText = u"".join(t.strip() for t in viz_text)
    for word in allVisText.split():
        extractText = extractText + word + " "
    return(extractText)


print(loadAddress(""))

