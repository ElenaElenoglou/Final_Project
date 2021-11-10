from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

dataset = pd.read_csv('dataset_v4.csv').fillna('')
df_tfidf = pd.read_csv('tfidf_v4.csv')

app = Flask(__name__)
CORS(app) 

fields = ['program_id', 'title', 'tag_genre', 'tag_sous_genre_1', 'tag_sous_genre_2', 'ratio_liked', 'program_description']

@app.route('/programs', methods=['GET'])
def get_programs():
    search = request.args.get('search')
    res = dataset[dataset.title.str.contains(search)][fields]

    return jsonify(res.to_dict(orient='records'))

@app.route('/popularity', methods=['GET'])
def recommend_popularity():
    program_id = request.args.get('program_id')
    program_index = dataset[dataset.program_id == int(program_id)].index.values[0]
    program = dataset[dataset.program_id == int(program_id)].iloc[0]
    
    genre = program.tag_genre
    ss_genre_1 = program.tag_sous_genre_1
    ss_genre_2 = program.tag_sous_genre_2
    dataset_by_genre = dataset[dataset.tag_genre == genre]
    if ss_genre_2 == '':
        recommendations = dataset_by_genre[
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_1) | (dataset_by_genre.tag_sous_genre_2 == ss_genre_1)
        ]
    else:
        recommendations = dataset_by_genre[
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_1) & (dataset_by_genre.tag_sous_genre_2 == ss_genre_2) |
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_2) & (dataset_by_genre.tag_sous_genre_2 == ss_genre_1)
        ]

    recommendations_tfidf = df_tfidf.iloc[recommendations.index.values]
    program_vector = recommendations_tfidf.loc[program_index]
    recommendations['cos_similarity'] = cosine_similarity([program_vector], recommendations_tfidf)[0]
    res = recommendations[recommendations.program_id != int(program_id)].sort_values(by=['cos_similarity'], ascending=False)[fields + ['cos_similarity']]

    return jsonify(res.to_dict(orient='records'))

if __name__=='__main__':
    app.run(port = 5000, debug = True)