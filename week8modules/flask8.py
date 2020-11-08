#!flask/bin/python
from flask import Flask, jsonify, abort, request
import pandas as pd
import sqlalchemy as sqla



app = Flask(__name__)

# Task 
#Make a simple flask server with one, get endpoint /flask_app/.
#a) Make it write Hello World.

@app.route('/flask_app/')
def index():
    return "Hello, World from flask server! This is Allan"

# Task a) /api/showAll

@app.route('/api/showAll', methods=['GET'])
def get_all():
    return showAllDB().to_html()



def showAllDB():
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@db/db"
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)

    result_df = pd.read_sql('select * from People', con=engine)
    return result_df


# Task b) /api/employee/<string: firstName>/<string: lastName>


@app.route('/api/employee/<string:firstName>/<string:lastName>', methods=['GET'])
def get_person(firstName, lastName):
    return get_person(firstName, lastName).to_html()


def get_person(firstName, lastName):
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@db/db"
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)

    result_df = pd.read_sql(
        con=engine,
        sql = "SELECT * FROM People WHERE `First Name`='{}' AND `Last Name`='{}'".format(firstName, lastName))
    return result_df

#Task c) /api/employee/add

@app.route('/api/employee/add', methods=['POST'])
def create_person():
    if not request.json:
        abort(400)
    return addperson(request).to_html(), 201

def addperson(request):
    person = {
        "First Name": request.json['First Name'],
        "Last Name": request.json['Last Name'],
        "Gender": request.json['Gender'],
        "Age": request.json['Age'],
        "Email": request.json['Email'],
        "Phone": request.json['Phone'],
        "Occupation": request.json['Occupation'],
        "Salary": request.json['Salary']
    }
    df = pd.json_normalize(person)
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@db/db"
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)

    df.to_sql(
        "People",
        engine,
        if_exists="append",
        dtype={col_name: sqla.types.NVARCHAR(length=255) for col_name in df}
    )
    return showAllDB()


#Task d) /api/employee/delete

@app.route('/api/employee/delete', methods=['DELETE'])
def delete_person():
    if not request.json:
            abort(400)
    return deleteperson(request).to_html(), 201


def deleteperson(request):
    index = request.json['ID']
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@db/db"
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)

    conn = engine.connect()
    try:
        conn.execute("DELETE FROM People WHERE `index`='{}'".format(index))
    except:
        raise 
    return showAllDB()


#Task e) /api/employee/update
@app.route('/api/employee/update', methods=['PUT'])
def update_person():
    if not request.json:
        abort(400)
    return updateperson(request).to_html(), 201


def updateperson(request):
    SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@db/db'
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    conn = engine.connect()
    try:
        conn.execute("UPDATE People SET `First Name`='{}', `Last Name`='{}', Gender='{}', Age='{}', Email='{}', Phone='{}', Occupation='{}', Salary='{}' WHERE `index`='{}'".format(
            request.json['First Name'], request.json['Last Name'], request.json['Gender'], request.json['Age'], request.json['Email'], request.json['Phone'], request.json['Occupation'], request.json['Salary'], request.json['Index']))
    except:
        raise

    return showAllDB()


if __name__ == '__main__':
    app.run(debug=True)