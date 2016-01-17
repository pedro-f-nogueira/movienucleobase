import numpy as np
import pandas as pd
import sqlite3

def build_excel(movie_chars_object,movie_title):
    # Builds Excel with 5 columns
    # 1 - Id
    # 2 - Character name
    # 3 - Character gender
    # 4 - Number of scenes in which he appeared
    # 5 - Character he interacted with

    Df_Id_1 = []
    Df_Names = []
    Df_Gender = []
    Df_N_scenes_real = []
    Df_scenes_real = []

    for character in movie_chars_object:
        Df_Id_1.append(character.id)
        Df_Names.append(character.name)
        Df_Gender.append(character.gender)
        Df_N_scenes_real.append(len(character.appeared_scenes))
        Df_scenes_real.append(character.appeared_scenes)

    DataFrameMovie = {
                      'Id' : pd.Series(Df_Id_1),
                      'Name' : pd.Series(Df_Names),
                      'Gender' : pd.Series(Df_Gender),
                      'Number_Scene_Appearances' : pd.Series(Df_N_scenes_real),
                      'Scene_Appearances' : pd.Series(Df_scenes_real),
                      }

    df = pd.DataFrame(DataFrameMovie)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    #writer = pd.ExcelWriter('LOTR_1.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    #df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    #writer.save()

    # Builds Excel with 4 columns relative to interactions
    # 1 - Id
    # 2 - Character 1
    # 3 - Character 2
    # 4 - Number of Interactions

    Df_Char_1 = []
    Df_Char_2 = []
    Df_Char_1_id = []
    Df_Char_2_id = []
    Df_Number = []

    for character in movie_chars_object:
        #iterates trough the dict
        for key, value in character.characters_interacted_with.iteritems():
            cont_var = 0
            len_df_names = len(Df_Names)
            #fills the arrays for the 1st element
            if character.name != key:
                for char in range(len_df_names):
                    if character.name == Df_Names[char]:
                        Df_Char_1.append(character.name)
                        Df_Char_1_id.append(Df_Id_1[char])
                    if key == Df_Names[char]:
                        Df_Char_2.append(key)
                        Df_Char_2_id.append(Df_Id_1[char])
                        Df_Number.append(value)
                        continue

            #checks for repeated interactions
            for record in range(len(Df_Char_1)):
                if Df_Char_1[record] == character.name and Df_Char_2[record] == key or Df_Char_1[record] == key and Df_Char_2[record] == character.name:
                    Df_Number[record] = Df_Number[record] + 1
                    cont_var = 1

            #skips if interactions is repeated
            if cont_var == 1:
                continue

            #appends values for new interactions
            if character.name != key:
                for char in range(len(Df_Names)):
                    if character.name == Df_Names[char]:
                        Df_Id_1.append(id)
                        Df_Char_1_id.append(Df_Id_1[char])
                        Df_Char_1.append(character.name)
                    if key == Df_Names[char]:
                        Df_Char_2_id.append(Df_Id_1[char])
                        Df_Char_2.append(key)
                        Df_Number.append(value)

    DataFrameMovie = {
                      'Char_1' : pd.Series(Df_Char_1),
                      'Char_2' : pd.Series(Df_Char_2),
                      'Char_1_id' : pd.Series(Df_Char_1_id),
                      'Char_2_id' : pd.Series(Df_Char_2_id),
                      'Number_of_Interactions' : pd.Series(Df_Number),
                      }

    df = pd.DataFrame(DataFrameMovie)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    #writer = pd.ExcelWriter('LOTR_2.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    #df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
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
        n_scenes_mention         TEXT  NOT NULL,
        n_scenes_mention_descr   TEXT  NOT NULL,
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
    conn.execute('''insert into movies (id_m,name) values (?,?)''', (null,movie_title))

    #Getting id_m
    cursor=conn.cursor()
    cursor.execute("SELECT MAX(id_m) FROM movies")
    id_m = cursor.fetchone()[0]

    #Populating chars table
    len_chars = len(Df_Id_1)
    for i in range(len_chars):
        conn.execute('''insert into chars (id_m, id_c,name, gender, n_scenes, n_scenes_descr, n_scenes_mention, n_scenes_mention_descr) values (?,?,?,?,?,?,?,?)'''
                     , (id_m,null,Df_Names[i],Df_Gender[i],Df_N_scenes_real[i],Df_scenes_real[i],null,null))


    #Populating interactions table
    len_int = len(Df_Char_1_id)
    for i in range(len_int):
        conn.execute('''insert into interactions (id_m, char_1_id, char_2_id, n_interactions, type) values (?,?,?,?,?)'''
                     , (id_m,Df_Char_1_id[i],Df_Char_2_id[i],Df_Number[i],0))


    conn.commit()

    print "Records created successfully"

    conn.close()

