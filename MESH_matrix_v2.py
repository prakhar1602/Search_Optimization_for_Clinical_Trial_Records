import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# load data
project_home = "/Users/pranita/OneDrive - Northeastern University/Northeastern University/Summer 2020/DS 5230 - Unsupervised Machine Learning/Project/Clinical Trials"
records_data = pd.read_csv(os.path.join(project_home, "all_trials.csv"))
mesh_data = pd.read_csv(os.path.join(project_home, "MESH_Terms_v2.csv"))
records_data = records_data[['id','title','brief_summary','detailed_description']]
mesh_data = mesh_data[['TermUI','Term']]

# Replace Null values with empty strings
records_data = records_data.replace(np.nan, '', regex=True)

# Create Concatenated text using all data
records_data['article'] = records_data['title'].str.cat(records_data['brief_summary'], sep=" ").str.cat(records_data['detailed_description'], sep=" ")
records_data = records_data.drop(['title','brief_summary','detailed_description'], axis=1)

## lower case of MESH terms and text records
records_data['article'] = records_data['article'].str.lower()
mesh_data['Term'] = mesh_data['Term'].str.lower()

## Finding threshold for ngram_range
mesh_data['split'] = mesh_data['Term'].str.split()
mesh_data['len'] = mesh_data['split'].str.len()
mesh_data = mesh_data[mesh_data['len'] < 7]

## Create dictionary mapping of Mesh terms and Ids
mesh_map= dict(zip(mesh_data.Term, mesh_data.TermUI))
mesh_bow = list(mesh_map.keys()) ## defined vocab for Vectorizer

## Create TDM using counts
cv = CountVectorizer(vocabulary = mesh_bow, ngram_range= (1,6), token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
docs_tdm = cv.fit_transform(records_data['article'])

## Convert to dataframe and save (takes time & space)
docs_tdm_df = pd.DataFrame(docs_tdm.todense(), columns=cv.get_feature_names())
docs_tdm_df.to_csv(os.path.join(project_home, "MESH_TDM_count.csv"))

## Save files
import pickle
vocab_file = os.path.join(project_home,"mesh_vocab.pickle")
matrix_file = os.path.join(project_home,"mesh_matrix.pickle")
pickle.dump(cv.vocabulary_, open(vocab_file,"wb"))
pickle.dump(docs_tdm, open(matrix_file,"wb"))



######s
import pickle
file = os.path.join(project_home,"Mesh_tdm_count.pkl")
x = pickle.load(open(file, "wb"))

tfidf = pickle.load(open(matrix_file,"rb"))