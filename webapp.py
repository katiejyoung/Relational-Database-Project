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

#def films_by_genre():
#    genre = request.form.get('genre');
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film WHERE genre = %s" % (genre)
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
#    return render_template('genre.html', rows=result)

@webapp.route('/genre/<id>', methods=['POST','GET'])
def genre(id):
    if request.method == 'POST':
        genre_selected = request.form.get('genre_select')
    else:
        genre_selected = 1
        
    id=genre_selected
    db_connection = connect_to_database()
    query = "SELECT id, name FROM genre;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    query2 = "SELECT title FROM film f INNER JOIN film_genres g ON f.id = g.film_id AND g.genre_id = %s" % (id)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('genre.html', genres=result, genre_id=genre_selected, rows=result2);

@webapp.route('/filmAwards')
def awards():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
    return render_template('awards.html')

@webapp.route('/filmActors')
def actors():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#   print(result)
    return render_template('actors.html')

@webapp.route('/filmDirectors')
def directors():
#    db_connection = connect_to_database()
#    query = "SELECT id, title, language, year, runtime from film;"
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
    return render_template('directors.html')

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
