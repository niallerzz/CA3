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

# Weekly Files in href format
Slides = ('<a href="https://mikhail-cct.github.io/ca3-test/wk8/">wk8</a>')
PDF    = ('<a href="https://mikhail-cct.github.io/ca3-test/wk8.pdf">wk8.pdf</a>')
MP4    = ('<a href="https://drive.google.com/file/d/1hKgn7qnNlnd91_2YdzcFPwQvn5NeQS2A">2020-11-17 [18:05-19:40] – Prog: OO Approaches.mp4</a>')

# Saturday Classes, additonal files may be required
Slides_s = ('')
PDF_s    = ('')
MP4_s    = ('')


# moodle update system wrapped up in a function
def moodle_update():

    from dateutil import parser
    from datetime import date, timedelta
    

    section = LocalGetSections(courseid)
  
    print(json.dumps(section.getsections[1]['summary'], indent=4, sort_keys=True))

    # date parsed from moodle, timedelta added to manipulate the year
    month = parser.parse(list(section.getsections)[1]['name'].split('-')[0]) - timedelta(365)
    
    print(month)

    print(month.strftime("%V"))

    # calling the function to scan both local and endpoint files
    grab_video()
    
    # calling the function to grab video hash and convert into 'href' format
    scan_files()

    data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

    # Weekly Files in href format
    Slides = ('<a href="https://mikhail-cct.github.io/ca3-test/wk8/">wk8</a>')
    PDF    = ('<a href="https://mikhail-cct.github.io/ca3-test/wk8.pdf">wk8.pdf</a>')
    MP4    = ('<a href="https://drive.google.com/file/d/1hKgn7qnNlnd91_2YdzcFPwQvn5NeQS2A">2020-11-17 [18:05-19:40] – Prog: OO Approaches.mp4</a>')

    # Saturday Classes, additonal files may be required
    Slides_s = ('')
    PDF_s    = ('')
    MP4_s    = ('')

    # summary variabe that allows for the additional files 
    new_summary = (Slides + "<br>" + PDF + "<br>" + MP4 + "<br>" + Slides_s + "<br>" + PDF_s + "<br>" + MP4_s)
    
    
    data[0]['summary'] = new_summary

    data[0]['section'] = 8

    sec_write = LocalUpdateSections(courseid, data)

    print(input('Ready to send files Y or N? :')
    if "Y":
        print(json.dumps(section.getsections[1]['summary'], indent=4, sort_keys=True) + "#### Successfully Added To Moodle ####")
    elif "N":
        print('Take your time')
    else:
        return

   





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
    import pandas as pd
    
    
 
    res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX") 
    
    soup =bs4.BeautifulSoup(res.text,"lxml")
    
    videos = soup.find_all('div' ,class_ = 'Q5txwe')
   
    
    for video in videos:
 
        video_id = video.parent.parent.parent.parent.attrs['data-id']

        video_lable = (video['aria-label'])

        video_link = ('<a href="https://drive.google.com/file/d/'+ video_id +'">' + video_lable +'</a>' )
    
        print (video_link)



def scan_files():

    global new_summary
    global section_update_number
    from os import walk

    moodle_list = []
       
    for section in LocalGetSections(courseid).getsections:
            moodle_list.append(section.get('summary',))
    del moodle_list[0]
    # print (moodle_list)

    f = []
    for subdir, dirs, files in os.walk(path):
        for file in subdir:
            f.append(file)
    # print (f)

   






moodle_update()
    





