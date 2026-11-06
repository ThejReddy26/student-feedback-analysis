import mysql.connector
from mysql.connector import Error

def get_connection(config):
    return mysql.connector.connect(
        host=config["MYSQL_HOST"],
        user=config["MYSQL_USER"],
        password=config["MYSQL_PASSWORD"],
        database=config["MYSQL_DATABASE"]
    )

def init_db(config):
    # The database itself must first be created by running database/schema.sql.
    try:
        conn = get_connection(config)
        conn.close()
    except Error as exc:
        raise RuntimeError(
            "Cannot connect to MySQL. Check that MySQL is running and "
            "your .env settings match database/schema.sql."
        ) from exc

def get_courses(config):
    conn = get_connection(config)
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT course_id, course_name, faculty_name FROM courses ORDER BY course_name")
        return cur.fetchall()
    finally:
        conn.close()

def get_questions(config):
    conn = get_connection(config)
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT question_id, question_text FROM feedback_questions WHERE active=TRUE ORDER BY question_id")
        return cur.fetchall()
    finally:
        conn.close()

def save_feedback(config, course_id, answers, comment):
    conn = get_connection(config)
    try:
        cur = conn.cursor()
        for question_id, rating in answers:
            cur.execute(
                """INSERT INTO feedback
                   (course_id, question_id, rating, comment_optional)
                   VALUES (%s, %s, %s, %s)""",
                (course_id, question_id, rating, comment or None)
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def fetch_feedback_rows(config):
    conn = get_connection(config)
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT c.course_name, q.question_text, f.rating, f.submitted_at
            FROM feedback f
            JOIN courses c ON c.course_id=f.course_id
            JOIN feedback_questions q ON q.question_id=f.question_id
            ORDER BY c.course_name, q.question_id
        """)
        return cur.fetchall()
    finally:
        conn.close()
