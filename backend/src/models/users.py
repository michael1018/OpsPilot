# src/database/models/users.py
from sqlalchemy import Column, String, Integer, Date
from database.orm import ModelBase, AuditMixin, DeletedMixin, RemarkMixin
from sqlalchemy.inspection import inspect
from datetime import date, datetime

class Users(ModelBase, AuditMixin, DeletedMixin, RemarkMixin):
    """
    Users table for testing
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False, unique=True, comment='Name, unique identifier')
    age = Column(Integer, comment='Age')
    password = Column(String(32), comment='Password')
    birthdate = Column(Date, comment='Birthday')
    sex = Column(Integer, comment='Gender 1=Male,2=Female')
    status_code = Column(String(10), comment='Status code, references dictionary')

    def to_dict(self) -> dict:
        data = {}

        for column in inspect(self).mapper.column_attrs:
            key = column.key

            if key == "password":
                continue

            value = getattr(self, key)

            if isinstance(value, (date, datetime)):
                value = value.isoformat()

            data[key] = value

        return data