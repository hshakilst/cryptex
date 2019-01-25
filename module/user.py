#!/usr/bin/python
class User(object):
    def __init__(self, name='', department='', position='', id='', email=''):
        self.name = name
        self.department = department
        self.position = position
        self.id = id
        self.email = email
    
    def __hash__(self):
        return hash((self.name, self.department, self.position, self.id, self.email))

    def __eq__(self, other):
        return self.name, self.department, self.position, self.id, self.email == other.name, other.department, other.position, other.id, other.email

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def set_name(self, name):
        self.name = name

    def set_department(self, department):
        self.department = department

    def set_position(self, position):
        self.position = position

    def set_id(self, id):
        self.id = id

    def set_email(self, email):
        self.email = email

    def get_name(self):
        return self.name

    def get_department(self):
        return self.department

    def get_position(self):
        return self.position

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email
