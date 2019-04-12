from config import dbcreds
import mysql.connector

# Open new db connection
db = mysql.connector.connect(host=dbcreds["host"], user=dbcreds["user"],
                             password=dbcreds["pswd"], database=dbcreds["db"])

# Define new cursor to work with db
cursor = db.cursor()


def get_users():
    """Fetch all users' telegram id's from database
    Return:
        users: list – list of users' telegram id's
    """
    users = []
    cursor.execute("SELECT tg_id FROM users")
    for user in cursor.fetchall():
        users.append(user[0])
    return users


def add_user(user_id):
    """Add user to database
    Args:
        user_id: str – user id in telegram
    Return:
        True – if succeeded
        False – if failed
    """
    try:
        cursor.execute(
            "INSERT INTO users (tg_id, status) VALUES (%s, 0)", (user_id,))
        db.commit()
        return True
    except:
        return False


def get_user_status(user_id):
    """Get current user's status"""
    try:
        cursor.execute("SELECT status FROM users WHERE tg_id=%s", (user_id,))
        status = cursor.fetchone()
        return status[0]
    except:
        return None


def set_user_status(user_id, status):
    try:
        cursor.execute(
            "UPDATE users SET status=%s WHERE tg_id=%s", (status, user_id,))
        db.commit()
        return True
    except:
        return False
