from flask import Flask, render_template, url_for
from flask import request
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

@webapp.route('/')
def home():
    return render_template('index.html')

@webapp.route('/films')
#the name of this function is just a cosmetic thing
def films():
    db_connection = connect_to_database()
    query = "SELECT id, title, language, year, runtime from film;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('films.html', rows=result)

@webapp.route('/genre', methods=['POST','GET'])
def genre():
    if request.method == 'POST':
        genre_selected = request.form.get('genre_select');
    else:
        genre_selected = 1
    
    db_connection = connect_to_database()
    query = "SELECT id, name FROM genre;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    query2 = "SELECT title FROM film f INNER JOIN film_genres g ON f.id = g.film_id AND g.genre_id = %s" % (genre_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('genre.html', genres=result, genre_id=genre_selected, rows=result2);

@webapp.route('/awards')
def awards():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
    return render_template('awards.html')

@webapp.route('/actors')
def actors():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#   print(result)
    return render_template('actors.html')

@webapp.route('/directors')
def directors():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
    return render_template('directors.html')

#display update form and process any updates, using the same function
@webapp.route('/update_people/<id>', methods=['POST','GET'])
def update_people(id):
    db_connection = connect_to_database()
    if request.method == 'GET':

        people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s' % (id) 
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT planet_id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall();

        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print("Update people!");
        character_id = request.form['character_id'] 
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        print(request.form);

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        return (str(result.rowcount) + " row(s) updated");

#@webapp.route('/add_new_people', methods=['POST','GET'])
#def add_new_people():
#    db_connection = connect_to_database()
#    if request.method == 'GET':
#        query = 'SELECT id, title from film'
#        result = execute_query(db_connection, query).fetchall();
#        print(result)

#        return render_template('people_add_new.html', planets = result)
#    elif request.method == 'POST':
#        print("Add new people!");
#        fname = request.form['fname']
#        lname = request.form['lname']
#        age = request.form['age']
#        homeworld = request.form['homeworld']

#        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#        data = (fname, lname, age, homeworld)
#        execute_query(db_connection, query, data)
#        return ('Person added!');
