from flask import Flask, render_template, url_for, flash, request, redirect
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

@webapp.route('/films', methods=['POST','GET'])
#the name of this function is just a cosmetic thing
def films():
    db_connection = connect_to_database()

    if request.method == 'POST' and request.form['deleteButton'] == '':
        # Film being added
        title = request.form['title']
        language = request.form['language']
        year = request.form['year']
        runtime = request.form['runtime']
        insert_query = 'INSERT INTO film (title, language, year, runtime) VALUES (%s,%s,%s,%s)'
        data = (title, language, year, runtime)
        execute_query(db_connection, insert_query, data)
        flash('Film added!');
    elif request.method == 'POST':
        # Film being deleted
        deleteID = request.form['deleteButton']
        delete_query = "DELETE FROM film WHERE id = " + deleteID + ";"
        execute_query(db_connection, delete_query);

    # Display films in DB
    query = "SELECT id, title, language, year, runtime from film;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('films.html', rows=result)

@webapp.route('/genre', methods=['POST','GET'])
def genre():
    if request.method == 'POST':
        genre_selected = request.form.get('genre_select')
    else:
        genre_selected = 1
    
    db_connection = connect_to_database()
    query = "SELECT id, name FROM genre;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    query1 = "SELECT id, title FROM film;"
    result1 = execute_query(db_connection, query1).fetchall()
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_genres g ON f.id = g.film_id AND g.genre_id = %s" % (genre_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('genre.html', genres=result, genre_id=genre_selected, films=result1, rows=result2);

@webapp.route('/film_genre', methods=['POST','GET'])
def add_film_to_genre():
    db_connection = connect_to_database()

    if request.method == 'POST':
        film_selected = request.form.get('film_select')
        genre_selected = request.form.get('genre_select')
        insert_query = 'INSERT INTO film_genres (genre_id, film_id) VALUES (%s,%s)'
        data = (genre_selected, film_selected)
        print("Executing query")
        execute_query(db_connection, insert_query, data)
    else:
        film_selected = 1
        genre_selected = 1

    return redirect(url_for('genre'))

@webapp.route('/awards', methods=['POST','GET'])
def awards():
    if request.method == 'POST':
        award_selected = request.form.get('award_select');
    else:
        award_selected = 1
		
    id = award_selected
    db_connection = connect_to_database()
    query = "SELECT id, title FROM award;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_awards a ON f.id = a.film_id AND a.award_id = %s" % (id)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('awards.html', awards=result, award_id=award_selected, rows=result2);

@webapp.route('/actors', methods=['POST','GET'])
def actors():
    if request.method == 'POST':
        actor_selected = request.form.get('actor_select');
    else:
        actor_selected = 1
		
    id = actor_selected
    db_connection = connect_to_database()
    query = "SELECT id, last_name FROM actor;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_actors fa ON f.id = fa.film_id AND fa.actor_id = %s" % (id)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('actors.html', actors=result, actor_id=actor_selected, rows=result2);

@webapp.route('/directors', methods=['POST','GET'])
def directors():
    valid_update_query = False
    print("HI")
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
