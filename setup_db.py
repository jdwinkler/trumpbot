import psycopg2
import psycopg2.extras
import os

def get_db_credentials():

    return ('trump', 'james', 'winkler')

def reinitialize_db():

    db_name, user_name, password = get_db_credentials()

    connection = psycopg2.connect("dbname=%s user=%s host='localhost' password=%s" % (db_name, user_name, password))
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    db_schema = open(os.path.join(os.path.join(os.path.split(__file__)[0]),
                                  'schema','trump_db.sql'),'rU').readlines()
    db_schema = ''.join(db_schema)

    cursor.execute('drop schema if exists public cascade')
    cursor.execute('create schema public')

    cursor.execute(db_schema)

    connection.commit()
    connection.close()

if(__name__ == '__main__'):

    reinitialize_db()
