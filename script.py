from requests import get, post
import json
import os
from dateutil import parser
import datetime

# Module variables to connect to moodle api:
## Insert token and URL for your site here. 
## Mind that the endpoint can start with "/moodle" depending on your installation.

KEY = "bc7ad59923ad95f17dd955868790ccb5" 
URL = "http://f0ae7213ef73.eu.ngrok.io/"
ENDPOINT="/webservice/rest/server.php"
courseid = 3



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

# def grab_video():

#     import requests
#     import bs4
#     import re
#     from datetime import datetime, timedelta
#     import pandas as pd
    
    
#     current_datetime = datetime.now() 

#     start_date = current_datetime.strftime("%Y-%m-%d")

#     datestimeindex = pd.date_range(start_date, periods=14)
 
#     res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
#     soup =bs4.BeautifulSoup(res.text,"lxml")
    
#     videos = soup.find_all('div' ,class_ = 'Q5txwe')
   
    
#     for video in videos:
 
#         video_id = video.parent.parent.parent.parent.attrs['data-id']

#         video_lable = (video['aria-label'])

#         video_link = ('<a href="https://drive.google.com/file/d/'+ video_id +'">' + video_lable +'</a>' )
        
#         print(video_link)
        
# grab_video()


            


def scan_local_files():

    

    path = os.path.basename(r'C:\Users\customer\CA3\CA3\Sem1')

    listOfFile = os.listdir(path)
    completeFileList = list()
    for file in listOfFile:
        completePath = os.path.join(path,file)
        if os.path.isdir(completePath):
            completeFileList = completeFileList + scan_local_files(completePath)
        else:
            completeFileList.append(completePath)
            
        return completeFileList


    listOfFiles = scan_local_files(path)


 


# print(listOfFiles)


def scan_moodle():
    json_list =[]
    
    for section in LocalGetSections(courseid).getsections:
        json_list.append(section)

    new_list = []
    for dict in json_list:
        if dict['sectionnum'] == section_update_number:
            new_list.append(dict['summary'])

    return(new_list)

    



section = LocalGetSections(courseid)

data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

new_summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/">Week 1: Modules</a><br><a href="https://mikhail-cct.github.io/ca3-test/wk1.pdf">1.pdf</a><br>https://drive.google.com/file/d/1vyPoSlUc5hcXajllDyaqMKvlJOiYxbNH'

data[0]['summary'] = new_summary

section_update_number = 5

data[0]['section'] = section_update_number

sec_write = LocalUpdateSections(courseid, data)

section = LocalGetSections(courseid)

scan_moodle()

# scan_local_files()
            
            
    # print(json.dumps(section.getsections[1]['summary'], indent=4, sort_keys=True))
            




  
