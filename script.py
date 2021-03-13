from requests import get, post
import json
import os
from dateutil import parser
import datetime
import bs4


path = os.path.basename(r'C:\Users\customer\CA3\CA3\Sem1')
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

def grab_video():

    import requests
    import bs4
    import re
    from dateutil import parser
    from datetime import date, timedelta

    section = LocalGetSections(courseid)
  

    # date parsed from moodle, timedelta added to manipulate the year
    month = parser.parse(list(section.getsections)[1]['name'].split('-')[0]) - timedelta(365)
    
    adjutsed_date = (month.strftime('%Y-%m-%d'))

    print("Section date : ", adjutsed_date)
 
    res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
    soup =bs4.BeautifulSoup(res.text,"lxml")
    
    videos = soup.find_all('div' ,class_ = 'Q5txwe')
   
    
    for video in videos:
 
        video_id = video.parent.parent.parent.parent.attrs['data-id']

        video_lable = (video['data-tooltip'])

        video_link = ('<a href="https://drive.google.com/file/d/'+ video_id +'">' + video_lable +'</a>' )
    
        print(video_link)



def scan_files():
    

    from os import walk

    moodle_list = []
       
    for section in LocalGetSections(courseid).getsections:
            moodle_list.append(section.get('summary',0))
            
    del moodle_list[0]
    
    print("Files in Moodle directory : ", len(moodle_list))
    

    local_files = []

    for subdir, dirs, files in os.walk(path):
        for file in files:
            local_files.append(file)

    print("Files in local directory : ", len(local_files))
  
    return moodle_list
    
    
    
   
from collections import Counter


data = [{'section': 0, 'summary': '', }]

    # Weekly Files in href format
Slides = ('<a href="https://mikhail-cct.github.io/ca3-test/wk1/">wk12</a>')
PDF    = ('<a href="https://mikhail-cct.github.io/ca3-test/wk1.pdf">wk12.pdf</a>')
MP4    = ('<a href="https://drive.google.com/file/d/1vyPoSlUc5hcXajllDyaqMKvlJOiYxbNH">2020- [18:46-19:44] – Prog: OO Approaches.mp4</a>')

    # Saturday Classes, additonal files may be required
Slides_s = ('')
PDF_s    = ('')
MP4_s    = ('')

    # summary variabe that allows for the additional files 
new_summary = (Slides + "<br>" + PDF + "<br>" + MP4 + "<br>" + Slides_s + "<br>" + PDF_s + "<br>" + MP4_s)
    
data[0]['summary'] = new_summary

data[0]['section'] = 1

sec_write = LocalUpdateSections(courseid, data) 

section = LocalGetSections(courseid)

grab_video()

moodle_scan = scan_files()

print(json.dumps(section.getsections[1]['summary'], indent=4, sort_keys=True) + "#### Successfully Added To Moodle ####")
   






    





