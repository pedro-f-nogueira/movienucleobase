import numpy as np
import pandas as pd
import sqlite3

def build_excel(movie):
    # Builds Excel with 5 columns
    # 1 - Id
    # 2 - Character name
    # 3 - Character gender
    # 4 - Number of scenes in which he appeared
    # 5 - Character he interacted with

    df_id_1, df_names, df_gender, df_n_scenes_real, df_scenes_real = movie.build_table_chars()

    dataframeMovie = {
                      'Id': pd.Series(df_id_1),
                      'Name': pd.Series(df_names),
                      'Gender': pd.Series(df_gender),
                      'Number_Scene_Appearances': pd.Series(df_n_scenes_real),
                      'Scene_Appearances': pd.Series(df_scenes_real),
                      }

    df = pd.DataFrame(dataframeMovie)

    #Create a Pandas Excel writer
    #writer = pd.ExcelWriter('LOTR_1.xlsx', engine='xlsxwriter')
    #df.to_excel(writer, sheet_name='Sheet1')
    #writer.save()

    # Builds Excel with 4 columns relative to interactions
    # 1 - Character 1 Name
    # 2 - Character 2 Name
    # 1 - Character 1 Id
    # 2 - Character 2 Id
    # 3 - Number of Interactions

    df_char_1, df_char_2, df_char_1_id, df_char_2_id, df_number = movie.build_table_interactions()

    DataFrameMovie = {
                      'Char_1': pd.Series(df_char_1),
                      'Char_2': pd.Series(df_char_2),
                      'Char_1_id': pd.Series(df_char_1_id),
                      'Char_2_id': pd.Series(df_char_2_id),
                      'Number_of_Interactions': pd.Series(df_number),
                      }

    df = pd.DataFrame(DataFrameMovie)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    #writer = pd.ExcelWriter('LOTR_2.xlsx', engine='xlsxwriter')
    #df.to_excel(writer, sheet_name='Sheet1')
    #writer.save()

    #SQLite Database - to be separated from this file

    conn = sqlite3.connect('test.db')

    conn.execute('''DROP TABLE IF EXISTS movies''')

    conn.execute('''DROP TABLE IF EXISTS chars''')

    conn.execute('''DROP TABLE IF EXISTS interactions''')

    #Creating tables
    #To do - checking if tables are already created

    #Data relevant to movies
    conn.execute('''CREATE TABLE movies
       (id_m                     INTEGER           PRIMARY KEY AUTOINCREMENT,
        name                     TEXT              NOT NULL
        );'''
                 )

    #Data relevant to chars
    conn.execute('''CREATE TABLE chars
       (id_m                     INT   NOT NULL,
        id_c                     INT   NOT NULL,
        name                     TEXT  NOT NULL,
        gender                   TEXT  NOT NULL,
        n_scenes                 INT   NOT NULL,
        n_scenes_descr           TEXT  NOT NULL,
        n_scenes_mention         TEXT  ,
        n_scenes_mention_descr   TEXT  ,
        FOREIGN KEY(id_m) REFERENCES movies(id_m)
        );'''
                 )

    #Data relevant to char interactions / mentions
    #type = 0 - interaction
    #type = 1 - mention
    conn.execute('''CREATE TABLE interactions
       (id_m                     INT   NOT NULL,
        char_1_id                INT   NOT NULL,
        char_2_id                INT   NOT NULL,
        n_interactions           INT   NOT NULL,
        type                     INT   NOT NULL,
        FOREIGN KEY(id_m) REFERENCES movies(id_m),
        FOREIGN KEY(char_1_id) REFERENCES chars(id_c),
        FOREIGN KEY(char_2_id) REFERENCES chars(id_c)
        );'''
                 )

    #to do - stop if movie has already been analyzed

    #Populating tables

    null = None
    #Populating movies table
    conn.execute('insert into movies ' +
                 '(id_m,' +
                 'name)' +
                 'values (?,?)',
                 (null,
                  movie.title))

    #Getting id_m
    cursor=conn.cursor()
    cursor.execute('SELECT MAX (id_m) FROM movies')
    id_m = cursor.fetchone()[0]

    #Populating chars table
    len_chars = len(df_id_1)
    for i in range(len_chars):
        conn.execute('insert into chars ' +
                     '(id_m,' +
                     'id_c,' +
                     'name,' +
                     'gender,' +
                     'n_scenes,' +
                     'n_scenes_descr,' +
                     'n_scenes_mention,' +
                     'n_scenes_mention_descr)' +
                     'values (?,?,?,?,?,?,?,?)',
                     (id_m,
                      df_id_1[i],
                      df_names[i],
                      df_gender[i],
                      df_n_scenes_real[i],
                      ','.join(map(str, df_scenes_real[i])),
                      null,
                      null))


    #Populating interactions table
    len_int = len(df_char_1_id)
    for i in range(len_int):
        conn.execute('insert into interactions' +
                     '(id_m,' +
                     'char_1_id,' +
                     'char_2_id,' +
                     'n_interactions,' +
                     'type)' +
                     'values (?,?,?,?,?)',
                     (id_m,
                      df_char_1_id[i],
                      df_char_2_id[i],
                      df_number[i],
                      0))


    conn.commit()

    print 'Records created successfully'

    conn.close()

