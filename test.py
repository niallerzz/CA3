# def scrape_googledrive():

#     import requests
#     import bs4
#     from dateutil import parser
#     import datetime
#     import re

#     today = datetime.date.today()
#     print (today)

#     res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
#     soup =bs4.BeautifulSoup(res.text,"lxml")
    
#     videos = soup.find_all('div' ,class_ = 'Q5txwe')

# scrape_googledrive()




# def comparelists(LocalGetSections):

#     local_list = []
    
#     for dirname, dirnames, filenames in os.walk(r'C:\Users\customer\CA3\CA3\Files'):
#         for subdirname in dirnames:
#             os.path.join(dirname, subdirname)
#         for filename in filenames:
#             local_list = os.path.join(dirname, filename)
#             return (local_list)


#     sec = LocalGetSections(courseid)

#     for i in sec:
#         print(json.dumps(i['summary'], indent=4, sort_keys=True))
        
# comparelists()    




from datetime import datetime

now = datetime.now() # current date and time

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

time = now.strftime("%H:%M:%S")
print("time:", time)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)