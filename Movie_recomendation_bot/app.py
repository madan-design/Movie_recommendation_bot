from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Movie dataset with exactly 110 movies (fixed)
movies_data = pd.DataFrame({
    'id': range(1, 111),
    'title': [
        "The Shawshank Redemption", "The Dark Knight", "Inception", "Pulp Fiction", "The Godfather",
        "Forrest Gump", "The Matrix", "The Avengers", "Titanic", "Gladiator",
        "Interstellar", "Fight Club", "Goodfellas", "The Lion King", "The Departed",
        "Schindler's List", "The Green Mile", "Saving Private Ryan", "Braveheart", "The Prestige",
        "The Social Network", "The Wolf of Wall Street", "The Silence of the Lambs", "Joker", "Avengers: Endgame",
        "The Grand Budapest Hotel", "Django Unchained", "Whiplash", "A Beautiful Mind", "The Revenant",
        "Spider-Man: No Way Home", "Shutter Island", "Parasite", "1917", "Logan",
        "The Irishman", "Black Panther", "Doctor Strange", "Thor: Ragnarok", "Deadpool",
        "Mad Max: Fury Road", "John Wick", "La La Land", "The Greatest Showman", "Bohemian Rhapsody",
        "The Truman Show", "The Pursuit of Happyness", "The Big Short", "Moneyball", "The Martian",
        "Gravity", "The Theory of Everything", "Gone Girl", "The Hateful Eight", "Arrival",
        "Blade Runner 2049", "No Country for Old Men", "There Will Be Blood", "Once Upon a Time in Hollywood", "Dune",
        "The Batman", "No Time to Die", "Knives Out", "A Star Is Born", "The Lighthouse",
        "Tenet", "Soul", "Coco", "Zootopia", "Inside Out",
        "Frozen", "Encanto", "Moana", "Toy Story", "Finding Nemo",
        "The Incredibles", "Ratatouille", "Wall-E", "Up", "Monsters, Inc.",
        "How to Train Your Dragon", "Kung Fu Panda", "Shrek", "Madagascar", "The Secret Life of Pets",
        "The Lego Movie", "Despicable Me", "Cars", "Ice Age", "Rio",
        "Sing", "Trolls", "Cloudy with a Chance of Meatballs", "Wreck-It Ralph", "Big Hero 6",
        "Bolt", "Hercules", "Aladdin", "Mulan", "Pocahontas",
        "The Little Mermaid", "Beauty and the Beast", "Cinderella", "The Jungle Book", "Snow White and the Seven Dwarfs",
        "The Sound of Music", "Mary Poppins", "The Wizard of Oz", "Charlie and the Chocolate Factory", "Peter Pan"
    ],
    'genres': ["Drama"] * 110,  # Ensuring 110 genres
    'cast': ["Famous Actor, Popular Actress"] * 110,  # Ensuring 110 cast members
    'keywords': ["keyword1 keyword2 keyword3"] * 110,  # Ensuring 110 keywords
    'rating': np.random.uniform(7.5, 9.3, 110).round(1)  # Ensuring 110 ratings
})

# Convert titles to lowercase for case-insensitive matching
movies_data['title'] = movies_data['title'].str.lower()

# Create a TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_data['genres'] + " " + movies_data['cast'] + " " + movies_data['keywords'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        movie_name = request.form["movie_name"].strip().lower()
        if movie_name in movies_data['title'].values:
            idx = movies_data.index[movies_data['title'] == movie_name][0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
            recommended_movies = [movies_data.iloc[i[0]]['title'].title() for i in sim_scores]
            return render_template("index.html", recommended_movies=recommended_movies, searched_movie=movie_name.title())
        else:
            return render_template("index.html", error="Movie not found!")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
