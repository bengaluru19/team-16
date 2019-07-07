# import psycopg2
import os
from flask_bcrypt import generate_password_hash, check_password_hash
import mysql.connector

# for mysql
def connectDB(host='localhost', database='anthill', user='root', password='1010'):
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
    executeDB(c, "insert into user(user_id, name, email, phone, company, company_name, no_of_playgrounds, location, funding, budget, start_time, preferences) values(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, email, phone, company, company_name, no_of_playgrounds, location, funding, budget, start_time, preferences))
    disconnectDB(c)
    return True


# Survey Form
def survey_form(project_name, field_type, google_location, address, no_of_students, age, area, snake_prone, public_location, vandalism_prone, soil_condition, play_elements, underground_connections, electric_posts, trees, rocks, water_logging, highway, waterbodies, disability, maintainance_required, additional_requirements, email):
    c = connectDB()
    executeDB(c, "update user set project_name=%s, field_type=%s, google_location=%s, address=%s, no_of_students=%s, age=%s, area=%s, snake_prone=%s, public_location=%s, vandalism_prone=%s, soil_condition=%s, play_elements=%s, underground_connections=%s, electric_posts=%s, trees=%s, rocks=%s, water_logging=%s, highway=%s, water_bodies=%s, disability=%s, maintainance_required=%s, additional_requirements=%s where email=%s", (project_name, field_type, google_location, address, no_of_students, age, area, snake_prone, public_location, vandalism_prone, soil_condition, play_elements, underground_connections, electric_posts, trees, rocks, water_logging, highway, waterbodies, disability, maintainance_required, additional_requirements, email))
    disconnectDB(c)
    return True



# Update User/ Basically Create account
def create_user(email, password):
    c = connectDB()
    user_id = str(user_id)
    password = generate_password_hash(password)
    password = str(password, "utf-8")
    executeDB(c, "update user set password=%s, status=ongoing where email=%s", (password, email))
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
def request_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from user where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Fetch Single Request by Email
def request_by_email(email):
    c = connectDB()
    result = queryDB(c, "select * from user where email='"+email+"'")
    disconnectDB(c)
    return result


# Fetch all Requests
def request_list():
    c = connectDB()
    result = queryDB(c, "select * from user")
    disconnectDB(c)
    return result


# Fetch Image
def image_list_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from image where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Fetch Remarks
def remarks_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from remark where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Fetch Elements
def elements_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from element where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Fetch Has Elements
def has_elements_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from has_element where user_id=%s", (user_id, ))
    disconnectDB(c)
    return result


# Adding Stuff
# Add element
def add_element(element_name):
    c = connectDB()
    executeDB(c, "insert into element(element_id, element_name) values(default, %s)", (element_name, ))
    disconnectDB(c)
    return True


# Add image
def add_image(image_url, u_id):
    c = connectDB()
    u_id = str(u_id)
    executeDB(c, "insert into image(image_id, image_url, u_id) values(default, %s, %s)", (image_url, u_id))
    disconnectDB(c)
    return True


# Add remark
def add_remark(remarks, u_id):
    c = connectDB()
    u_id = str(u_id)
    executeDB(c, "insert into remark(remarks_id, remarks, u_id) values(default, %s, %s)", (remarks, u_id))
    disconnectDB(c)
    return True


# Add has_element
def add_has_element(e_id, u_id, quantity):
    c = connectDB()
    e_id = str(e_id)
    u_id = str(u_id)
    quantity = str(quantity)
    executeDB(c, "insert into has_element(e_id, u_id, quantity) values(%s, %s, %s)", (e_id, u_id, quantity))
    disconnectDB(c)
    return True
