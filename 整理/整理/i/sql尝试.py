# I am trying to write a SQL query that retrieves all records from a table called 'employees' where the 'department' is 'Sales'. The query should also order the results by 'last_name' in ascending order.  I will be using sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import order_by, asc

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, department={self.department})>"

# Create an engine to connect to the database
engine = create_engine('sqlite:///employees.db')

# Create all tables
Base.metadata.create_all(engine)

# Create a session
session = Session(engine)

# Write the SQL query using sqlalchemy ORM
query = select(Employee).where(Employee.department == 'Sales').order_by(asc(Employee.last_name))
employees = session.execute(query).scalars().all()
for employee in employees:
    print(employee)
session.close()

