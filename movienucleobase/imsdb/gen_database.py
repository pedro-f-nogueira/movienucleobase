"""
.. module:: movienucleobase.py
   :synopsis: Creates a SQLite database

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import sqlalchemy as sql
import utilities as util
import os



def build_database(movie):
    """
    Builds three mysql tables
    movies - info relevant to movies
    chars  - info relevant to chars
    interactions - info relevant to interactions / mentions
    You need to create a your_db_here_.db file for this to work
    """

    # Variables for chars table
    df_id_1, df_names, df_gender, df_n_scenes_real, df_scenes_real = movie.build_table_chars()

    # Variables for interactions table
    df_char_1, df_char_2, df_char_1_id, df_char_2_id, df_number = movie.build_table_interactions()

    script_dir = os.path.dirname(os.path.dirname(__file__))
    rel_path = 'pass.txt'
    abs_file_path = os.path.join(script_dir, rel_path)

    # grabs the user / password / ip of your MySql database
    var_user_pass_ip = []

    for line in open(abs_file_path, 'r'):
        var_user_pass_ip.append(line.split(":", 1)[1].rstrip())

    var_user_pass_ip = var_user_pass_ip[0] + ':' + var_user_pass_ip[1] + var_user_pass_ip[2]

    engine = sql.create_engine(
        'mysql://' + var_user_pass_ip + '/movies?charset=utf8&use_unicode=True',
        pool_size=100,
        pool_recycle=3600)

    conn = engine.connect()

    # Checks if table movies exists
    try:
        conn.execute('select 1 from movies')
    except:
        # Creates it
        conn.execute('''CREATE TABLE movies
           (
            id_movie     INT               PRIMARY KEY AUTO_INCREMENT,
            dsc_movie    varchar(100)      NOT NULL
            );'''
                     )

    # Checks if table chars exists
    try:
        conn.execute('select 1 from chars')
    except:
        # Data relevant to chars
        conn.execute('''CREATE TABLE chars
           (
            id_char                  INT   PRIMARY KEY,
            fk_movie                 INT   NOT NULL,
            name                     TEXT  NOT NULL,
            gender                   TEXT  NOT NULL,
            n_scenes                 INT   NOT NULL,
            scenes_appeared          TEXT  NOT NULL,
            n_scenes_mention         TEXT  ,
            scenes_mentioned         TEXT  ,
            FOREIGN KEY(fk_movie) REFERENCES movies(id_movie)
            );'''
                     )

    # Checks if table chars exists
    try:
        conn.execute('select 1 from interactions')
    except:
        # Data relevant to char interactions / mentions
        # type = 0 - interaction
        # type = 1 - mention
        conn.execute('''CREATE TABLE interactions
           (fk_movie                 INT   NOT NULL,
            fk_char_1                INT   NOT NULL,
            fk_char_2                INT   NOT NULL,
            n_interactions           INT   NOT NULL,
            type                     INT   NOT NULL,
            FOREIGN KEY(fk_movie) REFERENCES movies(id_movie),
            FOREIGN KEY(fk_char_1) REFERENCES chars(id_char),
            FOREIGN KEY(fk_char_2) REFERENCES chars(id_char)
            );'''
                     )

    # Checking if movie was already inserted
    check_exists = util.get_df_from_conn('SELECT count(*) as exist FROM movies WHERE dsc_movie = \'' + movie.title + '\'')
    check_exists = check_exists['exist'].iloc[0]

    if check_exists == 1:
        print 'Movie "' + movie.title + '" has already been inserted'
    elif check_exists > 1:
        print 'There is a problem with your database'
    else:
        print 'Inserting a new movie named..."' + movie.title + '"'
        # If it's a new movie then lets insert it
        # Populating movies table
        conn.execute(
                     'insert into movies (dsc_movie) values (%s)',
                     movie.title
                     )

        # Getting id_movie
        id_movie = util.get_df_from_conn('SELECT id_movie FROM movies WHERE dsc_movie = \'' + movie.title + '\'')

        # Populating chars table
        len_chars = len(df_id_1)
        for i in range(len_chars):
            conn.execute('insert into chars ' +
                         '(fk_movie, id_char, name, gender, n_scenes, scenes_appeared)'
                         'values (%s, %s, %s, %s, %s, %s)',
                         (id_movie['id_movie'].iloc[0],
                          df_id_1[i],
                          df_names[i],
                          df_gender[i],
                          df_n_scenes_real[i],
                          ','.join(map(str, df_scenes_real[i])),
                          )
                         )

        # Populating interactions table
        len_int = len(df_char_1_id)
        for i in range(len_int):
            conn.execute(
                         'insert into interactions' +
                         '(fk_movie, fk_char_1, fk_char_2, n_interactions, type)' +
                         'values (%s, %s, %s, %s, %s)',
                         (id_movie['id_movie'].iloc[0], df_char_1_id[i], df_char_2_id[i], df_number[i], 0)
                         )

        print 'Records for "' + movie.title + '" were created successfully!'

    conn.close()

