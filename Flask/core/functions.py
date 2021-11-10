import pandas as pd

dataset = pd.read_csv('../series_v4.csv')

# Function that takes in a program title as input and outputs most similar movies
def get_recommendations(program):
    genre = program.tag_genre
    ss_genre_1 = program.tag_sous_genre_1
    ss_genre_2 = program.tag_sous_genre_2
    dataset_by_genre = dataset[dataset.tag_genre == genre]
    if ss_genre_2:
        recommendations = dataset_by_genre[
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_1) & (dataset_by_genre.tag_sous_genre_2 == ss_genre_2) |
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_2) & (dataset_by_genre.tag_sous_genre_2 == ss_genre_1)
        ]
    else:
        recommendations = dataset_by_genre[
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_1) | (dataset_by_genre.tag_sous_genre_2 == ss_genre_1) |
            (dataset_by_genre.tag_sous_genre_1 == ss_genre_2) | (dataset_by_genre.tag_sous_genre_2 == ss_genre_2)
        ]
    return recommendations.sort_values(by=['ratio_liked', 'count_profile_like'], ascending=False)