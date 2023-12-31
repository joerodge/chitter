from dataclasses import dataclass
import re
import hashlib

@dataclass
class User:
    id: int
    name: str
    username: str
    email: str
    password: str

    def is_valid(self):
        if '' in [self.name, self.username, self.email, self.password]:
            return False
        if not re.match(r'^\w+$', self.username):
            return False
        if not re.match(r'^\w+(\.\w+)*@\w+(\.[a-z]+)+$', self.email):
            return False
        return True


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_user_by_id(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE id = %s', [user_id]
        )
        if rows:
            r = rows[0]
            return User(r['id'], r['name'], r['username'], r['email'], r['password'])

    def get_user_by_username(self, username):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE username = %s', [username]
        )
        if rows:
            r = rows[0]
            return User(r['id'], r['name'], r['username'], r['email'], r['password'])

    def create_user(self, user):
        binary_password = user.password.encode("utf-8")
        hashed_password = hashlib.sha256(binary_password).hexdigest()
        rows = self._connection.execute(
            "INSERT INTO users (name, username, email, password) " \
            "VALUES (%s, %s, %s, %s) RETURNING ID",
            [user.name, user.username, user.email, hashed_password]
        )
        return rows[0]['id']
    
    def get_all_users(self):
        rows = self._connection.execute("SELECT * FROM users")
        users = []
        for r in rows:
            user = User(r['id'], r['name'], r['username'], r['email'], r['password'])
            users.append(user)
        return users

    def check_user(self, user_to_check):
        """Checks a user against user repo to see if email or
        username already in use. Returns error strings if they are"""
        errors = []
        all_users = self.get_all_users()
        usernames = [user.username for user in all_users]
        emails = [user.email for user in all_users]
        if user_to_check.email in emails:
            errors.append(f'There is already an account registered to {user_to_check.email}')
        if user_to_check.username in usernames:
            errors.append(f'{user_to_check.username} already in use')
        return errors
    
    def check_password(self, username, password_attempt):
        binary_password_attempt = password_attempt.encode("utf-8")
        hashed_password_attempt = hashlib.sha256(binary_password_attempt).hexdigest()
        rows = self._connection.execute(
            'SELECT * FROM users WHERE username = %s AND password = %s',
            [username, hashed_password_attempt])
        return len(rows) > 0
