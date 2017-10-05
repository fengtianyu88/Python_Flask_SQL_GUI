from os import getenv
from flask import Flask, request
from flask import render_template
import mysql.connector as sql

app = Flask(__name__)
sql_server_database = 'classes1718'
sql_server_user = 'root'
sql_server_host = 'localhost'
sql_server_pw = 'password'


@app.route('/' )
def start():
     return render_template('index.html')

@app.route('/view')
def viewData():
    classes_DB = sql.connect(user=sql_server_user, password= sql_server_pw, host=sql_server_host, database=sql_server_database)
    classes_DB_agent = classes_DB.cursor()
    classes_DB_agent.execute("SELECT * FROM students")
    data = []
    for id, fname, lname, classperiod in classes_DB_agent:
        data.append({'id':id, 'fname':fname, 'lname':lname, 'classperiod':classperiod})
    classes_DB_agent.close()
    classes_DB.close()
    return render_template('view.html', data = data)

@app.route('/add', methods=['GET', 'POST'])
def addData():
    if request.method == 'POST':
        classes_DB = sql.connect(user=sql_server_user, password=sql_server_pw, host=sql_server_host, database=sql_server_database)
        classes_DB_agent = classes_DB.cursor()
        insertion = "INSERT students VALUES (" + \
                    request.form['id'] + \
                    ", '" + request.form['fname'] + "', '" + \
                    request.form['lname'] + "', " + \
                    request.form['period'] +");"
        classes_DB_agent.execute(insertion)

        query = "SELECT * FROM students WHERE ID=" + request.form['id']
        classes_DB.commit()
        classes_DB_agent.execute(query)
        confirmation = {'hasData': True}
        for id, fname, lname, classperiod in classes_DB_agent:
            confirmation.update({'id': id, 'fname': fname, 'lname': lname, 'classperiod': classperiod})
        classes_DB_agent.close()
        classes_DB.close()
    else:
        confirmation = {'hasData':False}

    return render_template('addStudent.html', data = confirmation )

@app.route('/edit', methods=['GET', 'POST'])
def editData():
    if request.method == 'POST' and 'secondSubmit' in request.form:

        # this will update the student record and retrive the information
        classes_DB = sql.connect(user=sql_server_user, password=sql_server_pw, host=sql_server_host, database=sql_server_database)
        classes_DB_agent = classes_DB.cursor()
        update = "UPDATE students set "
        update += "firstname = '" + request.form['fname'] + "', "
        update += "lastname = '" + request.form['lname'] + "', "
        update += "classperiod = " + request.form['period']
        print('point 4')
        update += " WHERE id = " + request.form['id2']
        update += ";"
        classes_DB_agent.execute(update)
        classes_DB.commit()
        query = "SELECT * FROM students WHERE id= " + request.form['id2']
        classes_DB_agent.execute(query)

        for id, fname, lname, classperiod in classes_DB_agent:
            data = {'confirm': True, 'hasData': True, 'id': id, 'fname': fname, 'lname': lname,
                    'classperiod': classperiod}
        classes_DB_agent.close()
        classes_DB.close()

    elif request.method == 'POST' and 'firstSubmit' in request.form:
        # this code will retrive and return current info
        classes_DB = sql.connect(user=sql_server_user, password=sql_server_pw, host=sql_server_host, database=sql_server_database)
        classes_DB_agent = classes_DB.cursor()
        query = "SELECT * FROM students WHERE id= " + request.form['id']
        classes_DB_agent.execute(query)

        for id, fname, lname, classperiod in classes_DB_agent:
            data = {'confirm': False, 'hasData': True, 'id': id, 'fname': fname, 'lname': lname,
                    'classperiod': classperiod}
        classes_DB_agent.close()
        classes_DB.close()
    else:
        data= {'hasData': False, 'confirm':False}

    return render_template('editStudent.html', data = data)

@app.route('/delete', methods= ['GET', 'POST'])
def deleteData():
    if request.method == 'POST' and 'secondSubmit' in request.form:

        # this will update the student record and retrive the information
        classes_DB = sql.connect(user=sql_server_user, password=sql_server_pw, host=sql_server_host, database=sql_server_database)
        classes_DB_agent = classes_DB.cursor()
        delete = "DELETE FROM students WHERE id=" + request.form['id2'] + ";"
        classes_DB_agent.execute(delete)
        classes_DB.commit()
        data = {'confirm': True, 'hasData': True,}
        classes_DB_agent.close()
        classes_DB.close()

    elif request.method == 'POST' and 'firstSubmit' in request.form:
        # this code will retrive and return current info
        classes_DB = sql.connect(user=sql_server_user, password=sql_server_pw, host=sql_server_host, database=sql_server_database)
        classes_DB_agent = classes_DB.cursor()
        query = "SELECT * FROM students WHERE id= " + request.form['id']
        classes_DB_agent.execute(query)

        for id, fname, lname, classperiod in classes_DB_agent:
            data = {'confirm': False, 'hasData': True, 'id': id, 'fname': fname, 'lname': lname,
                    'classperiod': classperiod}
        classes_DB_agent.close()
        classes_DB.close()
    else:
        data = {'hasData': False, 'confirm': False}
    return render_template('deleteStudent.html', data = data)

#depreciated
@app.route('/process',  methods=['POST'])
def sayhello():

    user = {'fname': request.form['fname'], 'lname': request.form['lname']}
    print(user)
    return render_template('process.html', user = user)

@app.route('/getData',  methods=['POST'])
def getData():
    classes_DB = sql.connect(user=sql_server_user, password= sql_server_pw, host=sql_server_host, database=sql_server_database)
    classes_DB_agent = classes_DB.cursor()
    query = "SELECT * FROM students"
    searchID = request.form['id']
    searchFName = request.form['fname']
    searchLName = request.form['lname']
    searchPeriod = request.form['period']
    first = True
    if searchID !='' or searchFName !='' or searchLName !='' or searchPeriod !='':
        query += " WHERE "
    if searchID !='':
        first = False
        query += " ID=" + searchID
    if searchFName !='':
        if not first:
            query+= " AND "
        first = False
        query += " firstname='" + searchFName + "'"
    if searchLName !='':
        if not first:
            query += " AND "
        first = False
        query += " lastname='" + searchLName + "'"
    if searchPeriod !='':
        if not first:
            query += " AND "
        first = False
        query += " classperiod=" + searchPeriod
    classes_DB_agent.execute(query)
    data = []
    for id, fname, lname, classperiod in classes_DB_agent:
        data.append({'id': id, 'fname': fname, 'lname': lname, 'classperiod': classperiod})

    classes_DB_agent.close()
    classes_DB.close()
    return render_template('dataTable.html', data = data)


if __name__ == '__main__':
    app.run()

app.run(host=getenv('IP', '0.0.0.0'),port=int(getenv('PORT', 8080)))

