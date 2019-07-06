import mysql.connector
import psycopg2
import os
from flask_bcrypt import generate_password_hash, check_password_hash

# for mysql
def connectDB(host='localhost', database='anthill', user='root', password='1234'):
    return mysql.connector.connect(host=host, database=database, user=user, password=password)


# for heroku postgresql
# DATABASE_URL = os.environ['DATABASE_URL']
# def connectDB():
#     return psycopg2.connect(DATABASE_URL, sslmode='require')


# Disconnect From Database
def disconnectDB(conn):
    conn.close()


# Execute A Query
def executeDB(conn, sql, values):
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    return cursor.lastrowid


# Query The Database
def queryDB(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    try:
        rows = cursor.fetchall()
    except:
        rows = []
    cursor.close()
    return rows


# Forms and Users
# Request Form
def request_form(name, email, phone, company, company_name, no_of_playgrounds, location, funding, budget, start_time, preferences):
    c = connectDB()
    executeDB(c, "insert into user(user_id, name, email, phone, company, company_name, no_of_playgrounds, location, funding, budget, preferences) values(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, email, phone, company, company_name, no_of_playgrounds, location, funding, budget, start_time, preferences))
    disconnectDB(c)
    return True


# Survey Form
def survey_form(project_name, field_type, google_location, address, no_of_students, min_age, max_age, snake_prone, public_location, vandalism_prone, soil_condition, play_elements, underground_connections, electric_posts, trees, rocks, water_logging, highway, waterbodies, disability, maintainance_required, additional_requirements, email):
    c = connectDB()
    executeDB(c, "update user set project_name=%s, field_type=%s, google_location=%s, address=%s, no_of_students=%s, min_age=%s, max_age=%s, snake_prone=%s, public_location=%s, vandalism_prone=%s, soil_condition=%s, play_elements=%s, underground_connections=%s, electric_posts=%s, trees=%s, rocks=%s, water_logging=%s, highway=%s, waterbodies=%s, disability=%s, maintainance_required=%s, additional_requirements=%s where email=%s", (project_name, field_type, google_location, address, no_of_students, min_age, max_age, snake_prone, public_location, vandalism_prone, soil_condition, play_elements, underground_connections, electric_posts, trees, rocks, water_logging, highway, waterbodies, disability, maintainance_required, additional_requirements, email))
    disconnectDB(c)
    return True



# Update User/ Basically Create account
def create_user(email, password):
    c = connectDB()
    user_id = str(user_id)
    password = generate_password_hash(password)
    password = str(password, "utf-8")
    executeDB(c, "update user set password=%s where email=%s", (password, email))
    disconnectDB(c)
    return True


# Login User
def login_user(email, password):
    c = connectDB()
    result = queryDB(c, "select * from user where email=%s'", (email, ))
    disconnectDB(c)
    if result:
        if check_password_hash(result[0][2], password):
            return result[0]
        else:
            return False
    else:
        return False


# Fetching Stuff
# Fetch single Request by User Id
def request_list_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from user where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Fetch Single Request by Email
def request_list_by_email(email):
    c = connectDB()
    result = queryDB(c, "select * from user where email=%s", (email, ))
    disconnectDB(c)
    return result


# Fetch all Requests
def request_list():
    c = connectDB()
    result = queryDB(c, "select * from user")
    disconnectDB(c)
    return result


