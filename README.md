# flask-basics
Basic To-Do list app used to understand the workings of Flask and Mongo.
This app was created by following this YouTube [tutorial](https://www.youtube.com/watch?v=Z1RJmh_OqeA) with some modifications. (MongoDB using Flask-PyMongo over SQLite)

## Quick Setup

#### Prerequisites
Make sure you are on a Unix environment and Python 3, Pip 3, MongoDB are installed before continuing the following steps.

1. Clone the repository using `git clone https://github.com/tahmid-haque/flask-basics.git`.
2. Change directory to `flask-basics` and use `python3 -m venv env`.
3. Change the environment using `. env/bin/activate`. You will notice a `(env)` appear at the start of your terminal prompt.
4. Run `pip3 install -r requirements.txt` to install necessary dependancies.
5. Before running the app, make sure there is a Mongo instance running on a separate terminal. If not, run `sudo mongod`.
5. To run the app, execute `python3 app.py` and head to `http://localhost:8000/` on a web browser.
