# CSV reading reference:
# https://docs.python.org/3/library/csv.html

import csv
from SortFunctions import quick_sort

def main():
    # Reading my Letterboxd ratings using file reading and dictionaries
    # https://docs.python.org/3/library/csv.html
    movies = {}

    with open("data/letterboxd/ratings.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for movie in reader:
            name = movie["Name"]
            year = movie["Year"]
            rating = float(movie["Rating"])

            movies[(name, year)] = rating

    print("Total rated movies:", len(movies))

    for movie in list(movies.items())[:5]:
        print(movie)

    # Reading the MovieLens dataset and storing movies in a dictionary
    movielens = {}

    with open("data/movielens/movies.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for movie in reader:
            movie_id = movie["movieId"]
            title = movie["title"]
            genres = movie["genres"]

            movielens[movie_id] = (title, genres)

    print("\nTotal MovieLens movies:", len(movielens))

    for movie in list(movielens.items())[:5]:
        print(movie)

    # Using the dictionary counting method to calculate community ratings
    movie_ratings = {}

    with open("data/movielens/ratings.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            movie_id = row["movieId"]
            rating = float(row["rating"])

            if movie_id in movie_ratings:
                movie_ratings[movie_id][0] += rating
                movie_ratings[movie_id][1] += 1
            else:
                movie_ratings[movie_id] = [rating, 1]

    print("\nMovies with community ratings:", len(movie_ratings))

    for movie_id in list(movie_ratings.keys())[:5]:
        total = movie_ratings[movie_id][0]
        count = movie_ratings[movie_id][1]
        average = total / count

        print(movielens[movie_id][0], "- Average rating:", round(average, 2))
        
    # Using sets to keep track of movies I've already watched
    watched = set()

    with open("data/letterboxd/watched.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for movie in reader:
            name = movie["Name"]
            year = movie["Year"]

            watched.add((name, year))

    print("\nTotal watched movies:", len(watched))

    # Using dictionary lookups to match movies by name and year
    # Python dictionary reference:
    # https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
    matched = {}

    for movie_id, (title, genres) in movielens.items():
        if title.endswith(")") and "(" in title:
            name = title[:-7]
            year = title[-5:-1]

            if (name, year) in movies:
                matched[movie_id] = (name, movies[(name, year)], genres)

    print("\nMatched movies:", len(matched))

    for movie in list(matched.items())[:5]:
        print(movie)
    # Using the dictionary counting method to find my favorite genres
    genre_ratings = {}

    for movie_id, (name, rating, genres) in matched.items():
        for genre in genres.split("|"):
            if genre in genre_ratings:
                genre_ratings[genre][0] += rating
                genre_ratings[genre][1] += 1
            else:
                genre_ratings[genre] = [rating, 1]

    print("\nYour Genre Preferences:")

    for genre, (total, count) in genre_ratings.items():
        average = total / count
        print(genre, "- Average:", round(average, 2), "- Movies:", count)

    # Using sets to find movies I haven't watched yet
    unwatched = {}

    for movie_id, (title, genres) in movielens.items():
        if title.endswith(")") and "(" in title:
            name = title[:-7]
            year = title[-5:-1]

            if (name, year) not in watched:
                unwatched[movie_id] = (title, genres)

    print("\nUnwatched MovieLens movies:", len(unwatched))

    for movie in list(unwatched.items())[:5]:
        print(movie)

    # Movie recommendation reference:
    # https://github.com/smalec/movielens
    # https://developers.google.com/machine-learning/recommendation/content-based/basics
    recommendations = []

    for movie_id, (title, genres) in unwatched.items():
        if movie_id in movie_ratings:
            total = movie_ratings[movie_id][0]
            count = movie_ratings[movie_id][1]

            if count >= 10:
                community_average = total / count

                genre_total = 0
                genre_count = 0

                for genre in genres.split("|"):
                    if genre in genre_ratings:
                        genre_total += genre_ratings[genre][0] / genre_ratings[genre][1]
                        genre_count += 1

                if genre_count > 0:
                    personal_average = genre_total / genre_count

                    score = (personal_average + community_average) / 2

                    recommendations.append((title, round(score, 2)))

    print("\nTotal recommendation candidates:", len(recommendations))

    for movie in recommendations[:5]:
        print(movie)

    # Preparing the movie scores and titles for QuickSort
    ranked = []
    for title, score in recommendations:
        ranked.append((score, title))

    # Using QuickSort to rank the movies by their scores
    # https://www.geeksforgeeks.org/quick-sort/
    quick_sort(0, len(ranked) - 1, ranked)

    print("\nTOP 10 RECOMMENDED MOVIES")

    # Using list slicing to display the top 10 recommended movies
    for score, title in ranked[-10:][::-1]:
        print(title, "- Score:", score)

if __name__ == "__main__":
    main()