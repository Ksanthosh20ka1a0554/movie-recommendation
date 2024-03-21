from flask import Flask, render_template,request
import requests
import os
from get_movies import predict_score
app = Flask(__name__)

# Replace 'YOUR_TMDB_API_KEY' with your actual TMDb API key
TMDB_API_KEY = '1c64a203b7f5857c1fe51152e973f865'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/recommendations",methods=['GET','POST'])
def predict():
    if request.method=="POST":
        movies_data=[]
        movie_name=request.form['movie']
        rec_movies = predict_score(movie_name)
        for movie in rec_movies:
            title = movie['title']
            movie_id = movie['id']
            rating = movie['rating']
            img_url = fetch_poster(movie_id)
            movie_data = {
                'url':img_url,
                'title':title,
                'rating':rating
            }
            movies_data.append(movie_data)

    return render_template('recommendations.html', movies=movies_data)


def get_movie_details(movie_id):
    url = f'{TMDB_BASE_URL}/movie/{movie_id}'
    params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
    response = requests.get(url, params=params)
    movie_data = response.json()
    return movie_data

def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(
            movie_id, TMDB_API_KEY
        )
    )
    data = response.json()
    if data["poster_path"] is None:
        poster_url = "https://picsum.photos/500/750"  # Placeholder image if no poster available
    else:
        poster_url = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return poster_url

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
