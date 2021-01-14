import requests
import pickle
import re
import db
# Thank god this comes incldued wtih python.
from html.parser import HTMLParser
def findwdg()->(dict):
    """ Returns the replies of a thread with wdg in it"""
    catalog=requests.get("https://a.4cdn.org/g/catalog.json")
    for page in catalog.json():
        for thread in page["threads"]:
            if("sub" in thread):
                if("/wdg/" in thread["sub"]):
                    threadnum = thread["no"]
                    return (requests.get(f"https://a.4cdn.org/g/thread/{threadnum}.json"))




class MyHTMLParser(HTMLParser):
    """Get the html from any posts that DOES have title: and progress:, and returns the acutal text"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.data=""
    def handle_data(self, data):
        self.data+=data
    def handle_starttag(self,tag, attrs):
        if(tag=="br"):
            self.data+="\n"
    def pop(self):
        tmp = self.data
        self.data=""
        return tmp

def parsepost(post):
    """ Given a post, try to parse out the relevant columsn, as listed below """
    regex = re.compile("title:.*\n|progress:.*\n")
    if(regex.search(post)!=None):
        # print(regex.findall(post))

        regexstring=''.join(map(lambda i: i+":.*\\n|", db.columns))
        regexstring = regexstring[0:-3]
        # print(regexstring)
        regex2 = re.compile(regexstring)
        flags=(regex2.findall(post))
        ans = {}
        for flag in flags:
            (column, data) = flag.split(":", 1)
            ans[column]=data.replace("\n", "")
        return ans
    return None




def main():
    """ The main function, mostly because I'm a shit python dev and my files
    can get REALLY CLUTTERED. What this script does is parse through /g/, 
    finds any wdg generals, and if it detects any post that has the format
    of
    keyword1: data1,
    keyword2: data2, etc, it will be parsed and added here
    the function below is mostly for showcasing it.
    """
    wdgPosts = findwdg()
    p = MyHTMLParser()
    db.init()
    for i in wdgPosts.json()["posts"]:
        p.feed(i["com"])
        parsedpost=parsepost(p.pop())
        if(parsedpost!=None):
            print(parsedpost)
            db.insertentry(parsedpost)
        p.close()
    list(map(lambda i:print(i), db.getall()))
main()
