from flask import Flask, render_template, request, redirect, url_for    # Import Flask's utilities
from database import *  # Import database utilities

app = Flask(__name__)   # Initialize a flask app using current file
db = Database.getInstance(app)  # Get a database instance

@app.route('/', methods=['POST', 'GET'])    # Index page, show todo list
def index():
    if request.method == 'POST':    # If a POST request is received
        taskContent = request.form['content']   # Retrieve the body parameter
        try:
            db.insert('tasks', {"task": taskContent})   # Insert task into tasks database
            return redirect('/')    # Redirect back to home page
        except InsertFailureException: 
            return "There was an issue inserting your task."

    else:   # GET request
        try:
            tasks = db.query('tasks')   # Retrieve list of all tasks in tasks database
            return render_template('index.j2', tasks = tasks)   # Render the home page using the tasks variable
        except QueryFailureException:
            return "There was an issue locating your tasks."

@app.route('/delete/<id>')  # Delete route used to delete a task
def delete(id):
    try:
        db.delete('tasks', {"_id": id}) # Delete task matching id from tasks database
        return redirect('/')
    except DeleteFailureException:
        return "There was an issue removing your task."

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        taskContent = request.form['content']   # Get updated task content from request body
        try:
            db.update('tasks', {"_id": id}, {"$set": {"task": taskContent}})    # Update task matching id with new content
            return redirect('/')
        except UpdateFailureException:
            return "There was an issue updating your task."

    else:
        try:
            task = db.query('tasks', {"_id": id})   # Query database for task using id
            return render_template('update.j2', task = task[0]) # Show update page for task
        except QueryFailureException:
            return "There was an issue locating your task."

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)    # Open page on http://localhost:8000/ with debugging enabled to see