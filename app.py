import json
import math
from flask import Flask, jsonify, render_template, request, session
from random import random, choices, sample

app = Flask(__name__)
app.config.update(
  SECRET_KEY="UHUIGHIY87Y897098089GHGYY78Y8HKJHUY8Y8"  # Replace with a strong secret key
)

animes = json.load(open("animes.json"))

# Difficulty levels and corresponding rating difference ranges
difficulty_levels = {
  1: (0, 1),
  2: (0.5, 0.7),
  3: (0.3, 0.5),
}


def get_random_animes(difficulty=1, initial_anime=None):
  rating_diff_range = difficulty_levels[difficulty]

  if initial_anime:
    random_anime= initial_anime
  else:
    random_anime = sample(animes, 1)[0]

  def filter_by_rating_diff(anime):
    return 0 < abs(anime["rating"] - random_anime["rating"]) <= rating_diff_range[1]
  
  filtered_animes = [
    anime for anime in animes if anime["id"] != random_anime["id"] and filter_by_rating_diff(anime)
  ]

  if len(filtered_animes) < 2:
    rating_diff_range = (rating_diff_range[0] - 0.1, rating_diff_range[1] + 0.1)
    filtered_animes = [
      anime for anime in animes if anime["rating"] != random_anime["rating"] and filter_by_rating_diff(anime)
    ]

  return random_anime, choices(filtered_animes, k=1)[0]  # Return both animes



# ROUTES

@app.route("/")
def index():
  session["score"] = 0 
  # session["streak"] = 0 if "streak" not in session else session["streak"]
  return render_template("index.html", animes=animes[:46])  # Display some initial animes

@app.route("/guess")
def guess_anime():
  difficulty = 1  # Adjust based on user progress or other criteria
  session["score"] = 0 if "score" not in session else session["score"]
  anime1, anime2 = get_random_animes(difficulty)
  return render_template("guess.html", anime1=anime1, anime2=anime2)


@app.get("/submit")
def submit_guess():
  try:
    anime1 = animes[int(request.args.get("anime1"))]
    anime2 = animes[int(request.args.get("anime2"))]
    selected = int(request.args.get("selected"))

    correct_anime = max(anime1, anime2, key=lambda a: a["rating"])

    print(correct_anime['title'])

    if selected == correct_anime["id"]:
      print("i")
      session["score"] += 1
      if correct_anime['id'] == anime1['id']:
        return render_template(
          "guess.html",
          anime1=anime1,
          anime2=get_random_animes(difficulty=1, initial_anime=anime1)[1],
          show_rating=1,
        )
      else:
        return render_template(
          "guess.html",
          anime1=get_random_animes(difficulty=1, initial_anime=anime2)[1],
          anime2=anime2,
          show_rating=2,
        )
    else:
      session["streak"] = 0
      session["score"] = 0
      return render_template(
        "partials/lose_message.html",
        correct_anime=correct_anime,
        feedback="Incorrect! The correct anime was {} with a rating of {}".format(
          correct_anime["title"], correct_anime["rating"]
        ),
      )

  except (ValueError, KeyError):
    return jsonify({"error": "Invalid data submitted."})
