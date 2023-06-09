from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = 'users_cr_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls,id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result = connectToMySQL(cls.db).query_db(query,{'id' : id})
        return cls(result[0])

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO users(first_name,last_name,email,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,NOW(),NOW())'
        results = connectToMySQL(cls.db).query_db(query,data)
        # print(results)
        return results

    @classmethod
    def update(cls,data):
        query = """
        UPDATE users 
        SET
        first_name=%(first_name)s,
        last_name=%(last_name)s,
        email=%(email)s,
        updated_at=NOW()
        WHERE id=%(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,id):
        query = """
        DELETE FROM users
        WHERE id=%(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,{'id' : id})
        return result

    @classmethod
    def unique_email(cls,data):
        query = """
        SELECT email FROM users
        """
        result = connectToMySQL(cls.db).query_db(query)
        emails = []
        for email in result:
            emails.append(email)
        for email in emails:
            if email['email'] == data:
                flash('Email in use')
                return True
        return result

    @staticmethod
    def user_vald(input):
        is_valid = True
        if not input['first_name']:
            flash('First Name is required')
            is_valid = False
        if not input['last_name']:
            flash('Last Name is required')
            is_valid = False
        if not EMAIL_REGEX.match(input['email']):
            flash('Email address is not valid')
            is_valid = False
        return is_valid