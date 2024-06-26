#!/usr/bin/python3
""" The User Model """

from models.base import Base, BaseModel
from models.category import Category
from models.expense import Expense
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """ Defining the User class """
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    salary = Column(Integer, default=0)
    categories = relationship("Category", backref="users",
                              cascade="all, delete, delete-orphan")

    def set_salary(self, value):
        """ Sets the salary for a User """
        if isinstance(value, int) and value > 0:
            setattr(self, 'salary', value)
            self.save()
        raise TypeError('Salary must be an Integer > 0')

    def details(self):
        """
        Returns a dictionary containing information about a user
        including a list of dictionaries with <category.name>.<category.id>
        as key and a list of expenses as the value pair
        """
        from models import storage
        categories = storage.all(Category)
        expenses = storage.all(Expense)
        user_dict = {}
        for key, value in self.__dict__.items():
            if key not in ["password", 'categories', '_sa_instance_state']:
                user_dict[key] = value
        user_dict['categories'] = []
        user_dict['expenses'] = []
        for category in categories.values():
            if category.user_id == self.id:
                user_dict["categories"].append(category.about())
                key = "{}.{}".format(category.name, category.id)
                new = {key: []}
                for expense in expenses.values():
                    if expense.category_id == category.id:
                        new[key].append(expense.about())
                user_dict["expenses"].append(new)
        return user_dict


def confirm_account(email, password):
    """ Confirms and retrieves a User account """
    from models import storage
    if email and password:
        user = storage.get_user(email)
        if user:
            pb = password.encode('utf-8')
            pwd_hash = md5()
            pwd_hash.update(pb)
            pwd = pwd_hash.hexdigest()
            if user.password == pwd:
                return user
            return None
    return None    


def check_string(string):
    """
    Checks a string for special characters

    Return: Bool
    """
    char_list =  ['!', '@', '#', '.', '$', '%', '^', '&',
                  '*', '(', ')', '/', '[', ']', '{', '}']
    for char in char_list:
        if char in string:
            return True
    return False
