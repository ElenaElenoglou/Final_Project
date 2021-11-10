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
    res = dataset[fields]

    return jsonify(res.to_dict(orient='records'))

@app.route('/genres', methods=['GET'])
def get_genres():
    res = dataset.tag_genre.unique()
    print("res", type(res), res)

    return jsonify(res[res.astype(bool)].tolist())

@app.route('/sous-genres', methods=['GET'])
def get_sous_genres():
    sous_genre_1 = dataset.tag_sous_genre_1.unique()
    sous_genre_2 = dataset.tag_sous_genre_2.unique()
    print("sous_genre_1", type(sous_genre_1), sous_genre_1)

    return jsonify(sous_genre_1[sous_genre_1.astype(bool)].tolist())

@app.route('/popularity', methods=['GET'])
def recommend_popularity():
    program_id = request.args.get('program_id')
    genres = request.args.getlist('genres[]')
    ss_genres = request.args.getlist('ss_genres[]')
    program_index = dataset[dataset.program_id == int(program_id)].index.values[0]

    recommendations = dataset[
        (dataset.tag_genre.isin(genres)) &
        (
            (dataset.tag_sous_genre_1.isin(ss_genres)) | (dataset.tag_sous_genre_2.isin(ss_genres))
        )
    ]

    recommendations_tfidf = df_tfidf.iloc[recommendations.index.values]
    print(genres)
    print(ss_genres)
    print('Hello')
    print(recommendations.index.values)
    print('Hello')
    print(recommendations_tfidf)
    print(program_index)
    program_vector = recommendations_tfidf.loc[program_index]
    recommendations['cos_similarity'] = cosine_similarity([program_vector], recommendations_tfidf)[0]
    res = recommendations[recommendations.program_id != int(program_id)].sort_values(by=['cos_similarity'], ascending=False)[fields + ['cos_similarity']]

    return jsonify(res.to_dict(orient='records'))

if __name__=='__main__':
    app.run(port = 5000, debug = True)