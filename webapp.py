from flask import Flask, render_template, url_for, flash
from flask import request
from db_connector.db_connector import connect_to_database, execute_query
import logging
import string
#create the web application
webapp = Flask(__name__)
webapp.secret_key = 'vxBQYZpvBn'

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
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_genres g ON f.id = g.film_id AND g.genre_id = %s" % (genre_selected)
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

@webapp.route('/directors', methods=['POST','GET'])
def directors():
    valid_update_query = False
    
    if request.method == 'POST':
        director_selected = request.form.get('director_select');
        first_name = request.form['fname']
        last_name = request.form['lname']
        year_born = request.form['year_born']
        year_died = request.form['year_died']
        valid_update_query = True
    else:
        director_selected = 1
        valid_update_query = False

    # If the user has potentially entered UPDATE information, prepare the UPDATE query
    if valid_update_query:
        update_string = ''
        num_args = 0
        
        if first_name != '':
            update_string += "first_name = \'" + first_name + '\', '
            num_args += 1
        if last_name != '':
            update_string += "last_name = \'" + last_name + '\', '
            num_args += 1
        if year_born != '':
            update_string += "year_born = \'" + year_born + '\', '
            num_args += 1
        if year_died != '':
            update_string += "year_died = \'" + year_died + '\' '
            num_args += 1

        # If no arguments, this is not an UPDATE query
        if num_args == 0:
            valid_update_query = False
        elif num_args >= 1: # If one or more arguments, strip trailing comma
            update_string = update_string.rstrip(', ') + ' '
    
    # If this has proven to be a UPDATE query, perform it
    db_connection = connect_to_database()
    
    if valid_update_query:
        update_query = "UPDATE director SET " + update_string + "WHERE id = %s" % (director_selected) + ";"
        webapp.logger.error(update_query)
        execute_query(db_connection, update_query);
        flash("Entry updated!")

        # If the user has not entered a fname, lname, and year_born, this is an invalid query
        #if fname = '' || lname = '' || year_born = '':
        #    valid_query = False

    # Populate Film Dropdown
    query = "SELECT id, last_name FROM director;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    
    # Populate Films with Selected Director Table
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_direction d ON f.id = d.film_id AND d.director_id = %s" % (director_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('directors.html', directors=result, director_id=director_selected, rows=result2);

#display update form and process any updates, using the same function
#@webapp.route('/update_director/', methods=['POST','GET'])
#def update_director(id):
#    db_connection = connect_to_database()
#    if request.method == 'GET':

#        director_query = 'SELECT first_name, last_name, year_born, year_died from director WHERE id = %s' % (id) 
#        director_result = execute_query(db_connection, people_query).fetchone()

#        if people_result == None:
#            return "No such person found!"

#        planets_query = 'SELECT planet_id, name from bsg_planets'
#        planets_results = execute_query(db_connection, planets_query).fetchall();

#        return render_template('people_update.html', planets = planets_results, person = people_result)
#    elif request.method == 'POST':
#        print("Update people!");
#        character_id = request.form['character_id'] 
#        fname = request.form['fname']
#        lname = request.form['lname']
#        age = request.form['age']
#        homeworld = request.form['homeworld']

#        print(request.form);

#        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
#        data = (fname, lname, age, homeworld, character_id)
#        result = execute_query(db_connection, query, data)
#        return (str(result.rowcount) + " row(s) updated");

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
