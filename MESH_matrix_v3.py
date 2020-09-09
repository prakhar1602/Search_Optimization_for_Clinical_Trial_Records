import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Load Data
project_home = "/Users/pranita/OneDrive - Northeastern University/Northeastern University/Summer 2020/DS 5230 - Unsupervised Machine Learning/Project/Clinical Trials"
records_data = pd.read_csv(os.path.join(project_home, "all_trials.csv"))
mesh_data = pd.read_csv(os.path.join(project_home, "MESH_Terms_v2.csv"))
punc ='!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'

# Process clinical records data
records_data = records_data[['id','title','brief_summary','detailed_description']] # Subset columns
records_data = records_data.replace(np.nan, '', regex=True) # Replace Null values with empty strings
records_data['article'] = records_data['title'].str.cat(records_data['brief_summary'], sep=" ").str.cat(records_data['detailed_description'], sep=" ") # Create Concatenated text using all data
records_data = records_data.drop(['title','brief_summary','detailed_description'], axis=1)
records_data['article'] = records_data['article'].str.lower()   ## lower case
records_data.article =  records_data.article.str.translate(str.maketrans('','',punc))   # Remove punctuations except '-', '_'
records_data.article =  records_data.article.str.strip()    # Remove whitespaces

# Process Mesh Data
mesh_data.Term =  mesh_data.Term.str.translate(str.maketrans('','',punc))
mesh_data.Term =  mesh_data.Term.str.strip()
mesh_data['Term'] = mesh_data['Term'].str.lower()

# Creating the mesh term vocabulary
mesh_vec = CountVectorizer(lowercase=True, token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
mesh_tdm = mesh_vec.fit_transform(mesh_data.Term)
mesh_vocab = mesh_vec.get_feature_names()
print(len(set(mesh_vocab))) # 78,224

################# For Count Vectorizer  #########################
# Creating the records vocablary - Binary
records_vec = CountVectorizer(lowercase=True, token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+', min_df = 0.01, binary= True) # atleast appearing in 1% records
records_tdm = records_vec.fit_transform(records_data['article'])
records_vocab = records_vec.get_feature_names()
print(len(set(records_vocab)))  #2,022

# Finding the common vocabulary - Binary
com_mesh_rec = set(mesh_vocab).intersection(set(records_vocab))
print(len(com_mesh_rec))    #1484

# Trimming TDM matrix using common vocabulary
records_tdm_df = pd.DataFrame(records_tdm.todense(), columns= records_vocab)
records_tdm_df = records_tdm_df[com_mesh_rec]
records_tdm_df = records_tdm_df.loc[(records_tdm_df.sum(axis=1) != 0), (records_tdm_df.sum(axis=0) != 0)] # remove rows and columns with sum 0
records_tdm_df.to_pickle(os.path.join(project_home, "mesh_matrix_countvec_v3.pkl"))

################ For TF-IDF matrix  #########################
# Creating the records vocablary - TF-IDF
records_tfidf_vec = TfidfVectorizer(lowercase=True, token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+', min_df = 0.01) # atleast appearing in 1% records
records_tfidf = records_tfidf_vec.fit_transform(records_data['article'])
records_tfidf_vocab = records_tfidf_vec.get_feature_names()
print(len(set(records_tfidf_vocab))) #2,022

# Finding the common vocabulary - TF-IDF
com_mesh_rec_tfidf = set(mesh_vocab).intersection(set(records_tfidf_vocab))
print(len(com_mesh_rec_tfidf)) #1,484

# Trimming TF-IDF matrix using common vocabulary
records_tfidf_df = pd.DataFrame(records_tfidf.todense(), columns= records_tfidf_vocab)
records_tfidf_df = records_tfidf_df[com_mesh_rec_tfidf]
records_tfidf_df = records_tfidf_df.loc[(records_tfidf_df.sum(axis=1) != 0.0), (records_tfidf_df.sum(axis=0) != 0.0)] # remove rows and columns with sum 0
records_tfidf_df.to_pickle(os.path.join(project_home, "mesh_matrix_tfidf_v3.pkl"))