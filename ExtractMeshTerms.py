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
all_terms = []
terms_count = 0
for i, descriptorRecord in enumerate(all_descriptorRecords):
    print(i,"::", descriptorRecord.find('DescriptorName').find('String').text,"Terms till now:", terms_count)
    if descriptorRecord.find('ConceptList') != None:
        for concept in descriptorRecord.find('ConceptList').findall('Concept'):
            conceptID = concept.find('ConceptUI').text
            conceptName = concept.find('ConceptName').find('String').text
            if concept.find('TermList') != None:
                for term in concept.find('TermList').findall('Term'):
                    term_info = {}
                    term_info['CoceptID'] = conceptID
                    term_info['ConceptName'] = conceptName
                    term_info['TermUI'] = term.find('TermUI').text
                    term_info['Term'] = term.find('String').text
                    all_terms.append(term_info)
                    terms_count+=1

term_df = pd.DataFrame(all_terms)
term_df.to_csv(os.path.join(project_home,"MESH_Terms_v2.csv"), index=False)



########
from sklearn.feature_extraction.text import CountVectorizer
docs = ["I have laser evoked surgery tomorrow.","Apoorva has had laser-evoked surgery in the laser evoked surgery process last year."]
bow = ["laser-evoked", "surgery", "laser evoked"]
# cv = CountVectorizer(vocabulary = bow, token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
cv = CountVectorizer(vocabulary = bow, ngram_range= (1,2), token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
x = cv.fit_transform(docs)
cv.get_feature_names()
xx = pd.DataFrame(x.todense(), columns = cv.get_feature_names())

######
tfidf = TfidfVectorizer(vocabulary = myvocabulary, stop_words = 'english', ngram_range=(1,2))
feature_names = tfidf.get_feature_names()
corpus_index = [n for n in corpus]
rows, cols = tfs.nonzero()
for row, col in zip(rows, cols):
    print((feature_names[col], corpus_index[row]), tfs[row, col])

