import os, pymysql, datetime
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)

__cursor = conn.cursor()

def close():
    __cursor.close()
    conn.close()
    
def get_score_by_day(year, month, day):
    sql = "SELECT name, level FROM problem WHERE repeatation = 0 AND YEAR(time) = %s AND MONTH(time) = %s AND DAY(time) = %s;"
    rows = __cursor.execute(sql, (year, month, day))
    return __cursor.fetchall()

def get_score_by_problem_and_period(start_time, end_time, problem_id):
    sql = "SELECT name, level FROM problem WHERE (time BETWEEN %s AND %s) AND problem = %s;"
    rows = __cursor.execute(sql, (start_time, end_time, problem_id))
    return __cursor.fetchall()

def get_event():
    sql = "SELECT * FROM event"
    rows = __cursor.execute(sql)
    return __cursor.fetchall()

def truncate_event():
    sql = "TRUNCATE TABLE event"
    rows =  __cursor.execute(sql)
    return rows

def add_event(description, start_time, end_time, problem_id):
    sql = "INSERT INTO (description, start_time, end_time, problem_id) VALUES (%s, %s, %s, %s)"
    rows = __cursor.execute(sql, (description, start_time, end_time, problem_id))
    return rows

def delete_event_by_id(id):
    sql = "DELETE FROM event WHERE id = %s"
    rows = __cursor.execute(sql, (id))
    return rows

def delete_event_by_description(description):
    sql = "DELETE FROM event WHERE description = %s"
    rows = __cursor.execute(sql, (description))
    return rows