import os
import pandas as pd
from xml.etree import ElementTree
from joblib import Parallel, delayed
from pprint import pprint
import re

project_home = "/Users/pranita/OneDrive - Northeastern University/Northeastern University/Summer 2020/DS 5230 - Unsupervised Machine Learning/Project/Clinical Trials"
data_dir = os.path.join(project_home,"AllPublicXML")

def extractXML(i, xmlFile):
    try:
        tree = ElementTree.parse(xmlFile)
        root = tree.getroot()
        trial = {}
        trial['id'] = root.find('id_info').find('nct_id').text
        trial['overall_status'] = root.find('overall_status').text
        trial['study_type'] = root.find('study_type').text
        if root.find('start_date') != None:
            trial['start_date'] = root.find('start_date').text
        else:
            trial['start_date'] = ''
        if root.find('enrollment') != None:
            trial['enrollment'] = root.find('enrollment').text
        else:
            trial['enrollment'] = ''
        trial['condition'] = root.find('condition').text
        if root.find('location_countries') != None:
            trial['location_countries'] = root.find('location_countries').find('country').text.upper()
        else:
            trial['location_countries'] = ''
        if root.find('intervention') != None:
            trial['intervention'] = root.find('intervention').find('intervention_name').text.upper()
        else:
            trial['intervention'] = ''
            trial['intervention_type'] = ''
        if root.find('official_title') == None:
            trial['title'] = root.find('brief_title').text
        else:
            trial['title'] = root.find('official_title').text
        date_string = root.find('required_header').find('download_date').text
        trial['date_processed'] = date_string.replace('ClinicalTrials.gov processed this data on ', '')
        trial['sponsors'] = root.find('sponsors').find('lead_sponsor').find('agency').text
        if root.find('brief_summary') != None:
            trial['brief_summary'] = trimws(root.find('brief_summary').find('textblock').text)
        else:
            trial['brief_summary'] = ''
        if root.find('detailed_description') != None:
            trial['detailed_description'] = trimws(root.find('detailed_description').find('textblock').text)
        else:
            trial['detailed_description'] = ''
        return(trial)
    except Exception as e:
        all_exceptions.append("ID:"+str(i)+"File: "+ xmlFile + "::::" + str(e))


def trimws(text):
    return ' '.join(text.split())


all_files = []
for base, dir, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.xml'):
            all_files.append(os.path.join(base, file))
# trials_df = pd.DataFrame()
all_exceptions = []
# all_files= all_files[:10]
all_trials = Parallel(n_jobs = -1, require= 'sharedmem', verbose = 10)(delayed(extractXML)(i,file) for i,file in enumerate(all_files))

filtered_trials = [trial for trial in all_trials if not trial is None]
filtered_trials_df = pd.DataFrame(filtered_trials)
filtered_trials_df.to_csv(os.path.join(project_home,"all_trials.csv"), index = False)



############
########
# import pandas as pd
# from joblib import Parallel, delayed
#
# def start(file, i):
#     trial = file + ";" + str(i)
#     record = extract(trial)
#     print(record)
#     if i%2 == 0:
#         print(i)
#         x.append(i)
#     return (record)
#     # df = pd.concat([df, curr_df])
#
# def extract(text):
#     xx ={}
#     xx['file'] = text.split(';')[0]
#     xx['id'] = text.split(';')[1]
#     return(xx)
# curr_df = []
# i=1
# x= []
# files = ['abc', 'def','xyz','mno','pqr','ghi','jkl','stu','vwx']
#
# all = Parallel(n_jobs = -1, require= 'sharedmem')(delayed(start)(file,i) for i, file in enumerate(files))


