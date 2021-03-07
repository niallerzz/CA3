def scrape_googledrive():

    import requests
    import bs4
    from dateutil import parser
    import datetime
    import re

    today = datetime.date.today()
    print (today)

    res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
    soup =bs4.BeautifulSoup(res.text,"lxml")
    
    videos = soup.find_all('div' ,class_ = 'Q5txwe')

scrape_googledrive()