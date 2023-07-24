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
    for item in set_abilities:
        print("\"" + item + "\",")


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
    for item in set_types:
        print("\"" + item + "\",")


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
    for item in set_weaknesses:
        print("\"" + item + "\",")


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
                                id TEXT NOT NULL,
                                name TEXT PRIMARY KEY,
                                height TEXT NOT NULL,
                                weight TEXT NOT NULL,
                                male TEXT NOT NULL,
                                female TEXT NOT NULL,
                                category TEXT NOT NULL,
                                abilities TEXT NOT NULL,
                                types TEXT NOT NULL,
                                weaknesses TEXT NOT NULL,
                                caught TEXT NOT NULL
                            ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def fill_table(conn):
    for entry in dicts:
        id = entry['Id']
        name = entry['Name']
        height = entry['Height']
        weight = entry['Weight']
        if entry['Male']:
            male = 'True'
        else:
            male = 'False'
        if entry['Female']:
            female = 'True'
        else:
            female = 'False'
        category = entry['Category']
        abilities = ""
        types = ""
        weaknesses = ""
        caught = 'False'

        sql = ''' INSERT INTO pokedex(id, name, height, weight, male, female, category, abilities, types, weaknesses, caught) VALUES(?,?,?,?,?,?,?,?,?,?,?)'''

        a_list = sorted(entry['Abilities'])
        abilities = ','.join(a_list)

        t_list = sorted(entry['Type'])
        types = ','.join(t_list)

        w_list = sorted(entry['Weaknesses'])
        weaknesses = ','.join(w_list)
        cur = conn.cursor()
        poketuple = (id, name, height, weight, male, female,
                     category, abilities, types, weaknesses, caught)
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
