import os
import pandas as pd
from xml.etree import ElementTree
from pprint import pprint




project_home = "/Users/pranita/OneDrive - Northeastern University/Northeastern University/Summer 2020/DS 5230 - Unsupervised Machine Learning/Project/Clinical Trials"
data_path = os.path.join(project_home,"MESH_desc2021.xml")

xmlFile = data_path
tree = ElementTree.parse(xmlFile)
root = tree.getroot()
all_descriptorRecords = root.findall('DescriptorRecord')

all_records=[]
exceptions = []
for i, descriptorRecord in enumerate(all_descriptorRecords):
    try:
        print(i, "::", descriptorRecord)
        record = {}
        record['DescriptorUI'] = descriptorRecord.find('DescriptorUI').text
        record['DescriptorName'] = descriptorRecord.find('DescriptorName').find('String').text

        if descriptorRecord.find('DateCreated') != None:
            record['DateCreated'] = '-'.join([descriptorRecord.find('DateCreated').find('Year').text,
                                              descriptorRecord.find('DateCreated').find('Month').text,
                                              descriptorRecord.find('DateCreated').find('Day').text])
        else:
            record['DateCreated'] = ''

        if descriptorRecord.find('DateRevised') != None:
            record['DateRevised'] = '-'.join([descriptorRecord.find('DateRevised').find('Year').text,
                                              descriptorRecord.find('DateRevised').find('Month').text,
                                              descriptorRecord.find('DateRevised').find('Day').text])
        else:
            record['DateRevised'] = ''

        if descriptorRecord.find('DateEstablished') != None:
            record['DateEstablished'] = '-'.join([descriptorRecord.find('DateEstablished').find('Year').text,
                                                  descriptorRecord.find('DateEstablished').find('Month').text,
                                                  descriptorRecord.find('DateEstablished').find('Day').text])
        else:
            record['DateEstablished'] = ''
        if descriptorRecord.find('AllowableQualifiersList') != None:
            record['AllowableQualifiersList'] = [(qualifier.find('QualifierReferredTo').find('QualifierUI').text, qualifier.find('QualifierReferredTo').find('QualifierName').
                                              find('String').text, qualifier.find('Abbreviation').text) for qualifier in descriptorRecord.find('AllowableQualifiersList').
                                                findall('AllowableQualifier')]
        else:
            record['AllowableQualifiersList'] = []

        if descriptorRecord.find('PharmalogicalActionList') != None:
            record['PharmalogicalActionList'] = [(pharmalogicalAction.find('DescriptorReferredTo').find('DescriptorUI').text, pharmalogicalAction.find('DescriptorReferredTo').
                                              find('DescriptorName').find('String').text) for pharmalogicalAction in descriptorRecord.find('PharmacologicalActionList').
                                                findall('PharmacologicalAction')]
        else:
            record['PharmalogicalActionList'] = []

        if descriptorRecord.find('TreeNumberList') != None:
            record['TreeNumberList'] = [treeNumber.text for treeNumber in
                                        descriptorRecord.find('TreeNumberList').findall('TreeNumber')]
        else:
            record['TreeNumberList'] = []

        if descriptorRecord.find('ConceptList') != None:
            concept_list = []
            for concept in descriptorRecord.find('ConceptList').findall('Concept'):
                c_ui = concept.find('ConceptUI').text
                c_name = concept.find('ConceptName').find('String').text
                if concept.find('RegistryNumber') != None:
                    c_reg = concept.find('RegistryNumber').text
                else:
                    c_reg = ''
                if concept.find('TermList') != None:
                    term_res = []
                    for term in concept.find('TermList').findall('Term'):
                        term_res.append((term.find('TermUI').text, term.find('String').text))
                else:
                    term_res = []
                concept_list.append((c_ui, c_name, c_reg, term_res))
            record['ConceptList_Terms'] = concept_list
        else:
            record['ConceptList_Terms'] = []
        all_records.append(record)
    except Exception as e:
        print(e)
        exceptions.append(i)

all_records_df = pd.Dataframe(all_records)
all_records_df.to_csv(os.path.join(project_home, "MESH_descriptors.csv"), index = False)