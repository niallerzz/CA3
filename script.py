from requests import get, post
import json
import os
from dateutil import parser
import datetime

# Module variables to connect to moodle api:
## Insert token and URL for your site here. 
## Mind that the endpoint can start with "/moodle" depending on your installation.

KEY = "8cc87cf406775101c2df87b07b3a170d" 
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT="/webservice/rest/server.php"
courseid = 19



def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    #print(parameters)
    response = post(URL+ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

################################################
# Rest-Api classes
################################################

class LocalGetSections(object):
    """Get settings of sections. Requires courseid. Optional you can specify sections via number or id."""
    def __init__(self, cid, secnums = [], secids = []):
        self.getsections = call('local_wsmanagesections_get_sections', courseid = cid, sectionnumbers = secnums, sectionids = secids)


class LocalUpdateSections(object):
    """Updates sectionnames. Requires: courseid and an array with sectionnumbers and sectionnames"""
    def __init__(self, cid, sectionsdata):
        self.updatesections = call('local_wsmanagesections_update_sections', courseid = cid, sections = sectionsdata)

def scrape_googledrive():

    import requests
    import bs4
    from dateutil import parser
    import datetime
    import re

    today = datetime.date.today()

    title = today

    res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
    soup =bs4.BeautifulSoup(res.text,"lxml")
    
    videos = soup.find_all('div' ,class_ = 'Q5txwe')

    # print(videos)
   
    for video in videos:
 
        video_id = video.parent.parent.parent.parent.attrs['data-id']

        print (video['aria-label'])

        # print(video)

        print('https://drive.google.com/file/d/'+video_id)




section = LocalGetSections(courseid)



today = datetime.date.today()

month = parser.parse(list(section.getsections)[1]['name'].split('-')[0])

print(month)
# Extract the week number from the start of the calendar year
print(month.strftime("%V"))

data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

new_summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/">Week 3: Modules</a><br><a href="https://mikhail-cct.github.io/ca3-test/wk1.pdf">wk3.pdf</a>'

data[0]['summary'] = new_summary

data[0]['section'] = 9

sec_write = LocalUpdateSections(courseid, data)

section = LocalGetSections(courseid)

# local_file_scan()

scrape_googledrive()

# for section in LocalGetSections(courseid).getsections:
#     print(section)

print(json.dumps(section.getsections[1]['summary'], indent = 4, sort_keys=True))



# verifycation


# str = 'an example word:cat!!'
# match = re.search(r'word:\w\w\w', str)
# # If-statement after search() tests if it succeeded
# if match:
#   print 'found', match.group() ## 'found word:cat'
# else:
#   print 'did not find'