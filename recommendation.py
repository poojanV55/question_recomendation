# -*- coding: utf-8 -*-
"""recommendation_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cDMVGdmNXqtqh1mt8i6nJNQVgrhVJjCA
"""

import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from scipy.sparse import csr

#retrieving the data
def get_data():
  problem_data = pd.read_csv('Processed_prob.csv')
  problem_data['name'] = problem_data['name'].str.lower()
  problem_data = problem_data.dropna()
  problem_data['Que_id'] = np.arange(len(problem_data))

  return problem_data



def combine_data(data): 
  #creating list of important columns for rec eng
  columns = ['name','tags']
  
  
  #droping the not necessary columns
  # data = data.drop(columns=[ 'index','solved_count','rating'])
  # data = data.drop(columns=['contest_id', 'Que_id','index','solved_count','rating'])
  data = data.drop(columns=['contest_id', 'Que_id', 'solved_count', 'rating'])


  #changing the datatype of column as per requirment
  # data['name'] = data['name'].astype(str)
  # data['tags'] = data['tags'].astype(str)
  
  #Aggregating two important columns
  # data['important features'] = data[['name','tags']].agg(' '.join, axis=1)
  # data['Que_id'] = np.arange(len(data))

  data['important features'] = data[data.columns[0:2]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
  data = data.drop(columns=[ 'name','tags'])

  return data

def transform_data(data_combine, data_plot):
    #count and build the fit matrix  of the important feature
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['important features'])

    #Relate with frequantly repeated terms to show its importance
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_plot['tags'])

    #Obtain a single sparse matrix from two different count and tfid matrix
    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
    
    #Applying cosine similarity in both our matrix
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim

def recommend_questions(problem_title, data, combine, transform):

    # Store the indices of the name of question name in one series
    indices = pd.Series(data.index, index = data['name'])
    index = indices[problem_title]

    # Create a cosine score of the question relation in a list
    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:51]
    
    #Store top 20 questions in a list
    question_indices = [i[0] for i in sim_scores]

    #Stores the data of the recommended questions
    # question_id = data['Que_id'].iloc[question_indices]
    question_title = data['name'].iloc[question_indices]
    question_tags = data['tags'].iloc[question_indices].str.split(', ')
    contest_id = data['contest_id'].iloc[question_indices]
    question_index = data['index'].iloc[question_indices]
    solved_count = data['solved_count'].iloc[question_indices]
    rating = data['rating'].iloc[question_indices]

    #Create a dataframe of the recommended questions
    # recommendation_data = pd.DataFrame(columns=['Question_Id','Question_Name','Tags','Contest_Id','Question_Index'])
    recommendation_data = pd.DataFrame(columns=['name','tags','id','index','solved_count','rating'])


    # recommendation_data['Question_Id'] = question_id
    recommendation_data['name'] = question_title
    recommendation_data['tags'] = question_tags
    recommendation_data['id'] = contest_id
    recommendation_data['index'] = question_index
    recommendation_data['solved_count'] = solved_count
    recommendation_data['rating'] = rating

    return recommendation_data

def results(question_name):

    if question_name is None:
        question_name = ''

    question_name = question_name.lower()

    find_question = get_data()
    combine_result = combine_data(find_question)
    transform_result = transform_data(combine_result,find_question)


    if question_name not in find_question['name'].unique():
        return 'Question not in Database'
    
    else:
        question_name = question_name.lower()

        recommendations = recommend_questions(question_name, find_question, combine_result, transform_result)
        return recommendations.to_dict('records')

