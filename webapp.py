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

@webapp.route('/films', methods=['POST','GET'])
#the name of this function is just a cosmetic thing
def films():
    db_connection = connect_to_database()

    if request.method == 'POST' and request.form.get('deleteButton') == None:
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
    db_connection = connect_to_database()
    genre_selected = 1 # Default genre for showing films if not otherwise specified
    
    if request.method == 'POST' and request.form.get('composite_film_select') != None:
        # Add relationship into the film_genre composite table
        film_selected = request.form.get('composite_film_select')
        genre_selected = request.form.get('composite_genre_select')
        composite_insert_query = 'INSERT INTO film_genres (genre_id, film_id) VALUES (%s,%s)'
        data = (genre_selected, film_selected)
        print("Executing query")
        execute_query(db_connection, composite_insert_query, data)
    elif request.method == 'POST' and request.form.get('name') != None:
        # Add genre to genre table
        name = request.form['name']
        description = request.form['description']
        insert_query = 'INSERT INTO genre (name, description) VALUES (%s,%s)'
        data = (name, description)
        execute_query(db_connection, insert_query, data)
    elif request.method == 'POST':
        # If this is not an INSERT, just show the films in selected genre
        genre_selected = request.form.get('genre_select')

    # Genre dropdown
    query = "SELECT id, name FROM genre;"
    result = execute_query(db_connection, query).fetchall()
    print(result)

    # Film dropdown
    film_query = "SELECT id, title FROM film;"
    film_results = execute_query(db_connection, film_query).fetchall()

    # Show films in given genre
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_genres g ON f.id = g.film_id AND g.genre_id = %s" % (genre_selected)
    result2 = execute_query(db_connection, query2).fetchall()
    return render_template('genre.html', genres=result, films=film_results, genre_id=genre_selected, rows=result2)

@webapp.route('/awards', methods=['POST','GET'])
def awards():
    db_connection = connect_to_database()
    award_selected = 1

    if request.method == 'POST' and request.form.get('composite_film_select') != None:
        film_selected = request.form.get('composite_film_select')
        award_selected = request.form.get('composite_award_select')
        composite_insert_query = 'INSERT INTO film_awards (award_id, film_id) VALUES (%s,%s)'
        data = (award_selected, film_selected)
        print("Executing query")
        execute_query(db_connection, composite_insert_query, data)
    elif request.method == 'POST' and request.form.get('title') != None:
        # Add award to award table
        title = request.form['title']
        year_issued = request.form['year_issued']
        insert_query = 'INSERT INTO award (title, year_issued) VALUES (%s,%s)'
        data = (title, year_issued)
        execute_query(db_connection, insert_query, data)
    elif request.method == 'POST':
        # If this is not an INSERT, just show the films with selected award
        award_selected = request.form.get('award_select')
		
    # Award dropdown
    query = "SELECT id, title FROM award;"
    result = execute_query(db_connection, query).fetchall()
    print(result)

    # Film dropdown
    film_query = "SELECT id, title FROM film;"
    film_results = execute_query(db_connection, film_query).fetchall()

    # Show films with given award
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_awards a ON f.id = a.film_id AND a.award_id = %s" % (award_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('awards.html', awards=result, films=film_results, award_id=award_selected, rows=result2);

# @webapp.route('/actors', methods=['POST','GET'])
# def actors():
#     if request.method == 'POST':
#         actor_selected = request.form.get('actor_select');
#     else:
#         actor_selected = 1
		
#     id = actor_selected
#     db_connection = connect_to_database()
#     query = "SELECT id, last_name FROM actor;"
#     result = execute_query(db_connection, query).fetchall();
#     print(result)
#     query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_actors fa ON f.id = fa.film_id AND fa.actor_id = %s" % (id)
#     result2 = execute_query(db_connection, query2).fetchall();
#     return render_template('actors.html', actors=result, actor_id=actor_selected, rows=result2);

@webapp.route('/actors', methods=['POST','GET'])
def actors():
    actor_selected = 1 # Default selected actor unless otherwise specified
    db_connection = connect_to_database()

    if request.method == 'POST' and request.form.get('actor_select') != None:
        # Filter or update query
        actor_selected = request.form.get('actor_select')
    elif request.method == 'POST' and request.form.get('composite_film_select') != None:
        # Adding relationship to composite table film_direction
        film_selected = request.form.get('composite_film_select')
        actor_selected = request.form.get('composite_film_actor_select')
        composite_insert_query = 'INSERT INTO film_actors (actor_id, film_id) VALUES (%s,%s)'
        data = (actor_selected, film_selected)
        print("Executing query")
        execute_query(db_connection, composite_insert_query, data)
    elif request.method == 'POST' and request.form.get('fname_insert') != None:
        # Adding new actor to actor table
        first_name = request.form['fname_insert']
        last_name = request.form['lname_insert']
        year_born = request.form['year_born_insert']
        year_died = request.form['year_died_insert']
        insert_query = 'INSERT INTO actor (first_name, last_name, year_born, year_died) VALUES (%s,%s,%s,%s)'
        data = (first_name, last_name, year_born, year_died)
        execute_query(db_connection, insert_query, data)

    # Populate Actor Dropdown
    query = "SELECT id, last_name FROM actor;"
    result = execute_query(db_connection, query).fetchall();
    print(result)

    # Populate Film Dropdown
    film_query = "SELECT id, title FROM film;"
    film_results = execute_query(db_connection, film_query).fetchall()

    # Populate Films with Selected Director Table
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_actors fa ON f.id = fa.film_id AND fa.actor_id = %s" % (actor_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('actors.html', actors=result, actor_id=actor_selected, films=film_results, rows=result2);

@webapp.route('/directors', methods=['POST','GET'])
def directors():
    valid_update_query = False
    director_selected = 1 # Default selected director unless otherwise specified
    db_connection = connect_to_database()
    
    if request.method == 'POST' and request.form.get('director_select') != None:
        # Filter or update query
        director_selected = request.form.get('director_select');
        first_name = request.form['fname']
        last_name = request.form['lname']
        year_born = request.form['year_born']
        year_died = request.form['year_died']
        valid_update_query = True
    elif request.method == 'POST' and request.form.get('composite_film_select') != None:
        # Adding relationship to composite table film_direction
        film_selected = request.form.get('composite_film_select')
        director_selected = request.form.get('composite_film_director_select')
        composite_insert_query = 'INSERT INTO film_direction (director_id, film_id) VALUES (%s,%s)'
        data = (director_selected, film_selected)
        print("Executing query")
        execute_query(db_connection, composite_insert_query, data)
    elif request.method == 'POST' and request.form.get('fname_insert') != None:
        # Adding new director to director table
        first_name = request.form['fname_insert']
        last_name = request.form['lname_insert']
        year_born = request.form['year_born_insert']
        year_died = request.form['year_died_insert']
        insert_query = 'INSERT INTO director (first_name, last_name, year_born, year_died) VALUES (%s,%s,%s,%s)'
        data = (first_name, last_name, year_born, year_died)
        execute_query(db_connection, insert_query, data)
    else:
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
    if valid_update_query:
        update_query = "UPDATE director SET " + update_string + "WHERE id = %s" % (director_selected) + ";"
        webapp.logger.error(update_query)
        execute_query(db_connection, update_query);
        flash("Entry updated!")

        # If the user has not entered a fname, lname, and year_born, this is an invalid query
        #if fname = '' || lname = '' || year_born = '':
        #    valid_query = False

    # Populate Director Dropdown
    query = "SELECT id, last_name FROM director;"
    result = execute_query(db_connection, query).fetchall();
    print(result)

    # Populate Film Dropdown
    film_query = "SELECT id, title FROM film;"
    film_results = execute_query(db_connection, film_query).fetchall()
    
    # Populate Films with Selected Director Table
    query2 = "SELECT id, title, language, year, runtime FROM film f INNER JOIN film_direction d ON f.id = d.film_id AND d.director_id = %s" % (director_selected)
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('directors.html', directors=result, director_id=director_selected, films=film_results, rows=result2);
