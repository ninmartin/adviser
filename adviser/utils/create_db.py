import ast
import sqlite3
from sqlite3 import Error

dicts = []

def read_file(file: str):
    with open(file) as f:
        for line in f:
            res = ast.literal_eval(line)
            dicts.append(res)

def get_num_abilities():
    m = 0
    all_abilities = []
    for entry in dicts:
        m = max(m, len(entry['Abilities']))
        all_abilities.append(entry['Abilities'])
    print('Max number of abilities: %d\n' % (m))
    flat_list = [item for sublist in all_abilities for item in sublist]
    set_abilities = set(flat_list)
    print('Total number of abilities: ', len(set_abilities), '\n')

def get_num_types():
    m = 0
    all_types = []
    for entry in dicts:
        m = max(m, len(entry['Type']))
        all_types.append(entry['Type'])
    print('Max number of types: %d\n' % (m))
    flat_list = [item for sublist in all_types for item in sublist]
    set_types = set(flat_list)
    print('Total number of types: ', len(set_types), '\n')

def get_num_weaknesses():
    m = 0
    all_weaknesses = []
    for entry in dicts:
        m = max(m, len(entry['Weaknesses']))
        all_weaknesses.append(entry['Weaknesses'])
    print('Max number of weaknesses: %d\n' % (m))
    flat_list = [item for sublist in all_weaknesses for item in sublist]
    set_weaknesses = set(flat_list)
    print('Total number of weaknesses: ', len(set_weaknesses), '\n')

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS pokedex (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                height double NOT NULL,
                                weight double NOT NULL,
                                male boolean NOT NULL,
                                female boolean NOT NULL,
                                category text NOT NULL,
                                ability1 text NOT NULL,
                                ability2 text,
                                type1 text NOT NULL,
                                type2 text,
                                weakness1 text NOT NULL,
                                weakness2 text,
                                weakness3 text,
                                weakness4 text,
                                weakness5 text,
                                weakness6 text,
                                weakness7 text
                            ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def fill_table(conn):
    """ TODO: use empty string to fill non-full ability/type/weakness"""
    for entry in dicts:
        id = entry['Id']
        name = entry['Name']
        height = entry['Height']
        weight = entry['Weight']
        male = entry['Male']
        female = entry['Female']
        category = entry['Category']
        abilities = [None, None]
        types = [None, None]
        weaknesses = [None, None, None, None, None, None, None]
        
        
        sql = ''' INSERT INTO pokedex(id, name, height, weight, male, female, category, ability1, ability2, type1, type2, weakness1, weakness2, weakness3, weakness4, weakness5, weakness6, weakness7) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        for i in range(len(entry['Abilities'])):
            abilities[i] = entry['Abilities'][i]
        
        for i in range(len(entry['Type'])):
            types[i] = entry['Type'][i]

        for i in range(len(entry['Weaknesses'])):
            weaknesses[i] = entry['Weaknesses'][i]

        cur = conn.cursor()
        poketuple = (id, name, height, weight, male, female, category, abilities[0], abilities[1], types[0], types[1], weaknesses[0], weaknesses[1], weaknesses[2], weaknesses[3], weaknesses[4], weaknesses[5], weaknesses[6])
        print(poketuple)
        cur.execute(sql, poketuple)
        conn.commit()


def main():
    read_file('./pokedata.txt')
    get_num_abilities()
    get_num_types()
    get_num_weaknesses()
    conn = create_connection('pokedex.db')

    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")
    fill_table(conn)

if __name__ == "__main__":
    main()