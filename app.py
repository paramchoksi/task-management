from flask import Flask, render_template, request, redirect
from Database import *
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/index/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        email = email.lower()
        # Split email with @ and pick first value. Eg- newparamchoksi@gmail.com => newparamchoki
        table_name = email.split('@')[0]
        username = None

        """Fetching users data (username, email, pass) from login table"""
        users_data = getDataFromTable(createDatabaseConnection(), '*', 'login')
        for user_data in users_data:
            if email in user_data and password in user_data:
                username = user_data[0]
                break
            elif user_data == users_data[-1]:
                print("Your email and password not matched")
                return render_template('index.html')
            else:
                continue

        """Fetching all tables from database"""
        all_users_tables = getAllTables(createDatabaseConnection())
        for table in all_users_tables:
            if table_name in table:
                print("Welcome {}".format(username))
                allToDo = getDataFromTable(createDatabaseConnection(), '*', table_name)
                return render_template('home.html', username=username, table_name=table_name, allToDo=allToDo)

        print("{0} Your database table is not created..!!".format(username))

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        passwd = request.form['password']

        email = email.lower()
        username = username.lower()
        # If user enter "Param Choksi". There should not be space between name for userTable name in MySql.
        # username = username.split(' ')
        # username = '_'.join(username)
        # username "Param Choksi" will convert it into "Param_Choksi" for a userTable creation.

        table_name = email.split('@')[0]
        createUserTodoTable(table_name)
        all_users_tables = getAllTables(createDatabaseConnection())
        for table in all_users_tables:
            if table_name in table:
                insert_query = """INSERT INTO LOGIN VALUES ("{0}", "{1}", "{2}")""".format(username, email, passwd)
                executeQuery(createDatabaseConnection(), insert_query)
                break

    return render_template('signup.html')


@app.route('/index/home/<string:username>/<string:table_name>', methods=['GET', 'POST'])
def home(username, table_name):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0:
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            insert_query = """INSERT INTO {0}(title, description, time) VALUES("{1}", "{2}", "{3}")""".format(table_name,
                                                                                            title, desc, formatted_date)
            executeQuery(createDatabaseConnection(), insert_query)
            print("Data submitted to the database..!!")
            allToDo = getDataFromTable(createDatabaseConnection(), '*', table_name)
            return render_template('home.html', username=username, table_name=table_name, allToDo=allToDo)
        else:
            allToDo = getDataFromTable(createDatabaseConnection(), '*', table_name)
            return render_template('home.html', username=username, table_name=table_name, allToDo=allToDo)

    return render_template('home.html', username=username)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index/home/<string:username>/<string:table_name>/update/<int:sno>', methods=['GET', 'POST'])
def update(username, table_name, sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        updateUserTodo(createDatabaseConnection(), table_name, title, desc, formatted_date, sno)

        allToDo = getDataFromTable(createDatabaseConnection(), '*', table_name)
        return render_template('home.html', username=username, table_name=table_name, allToDo=allToDo)

    todo = getUserTodo(createDatabaseConnection(), table_name, sno)
    return render_template('update.html', username=username, table_name=table_name, sno=sno, todo=todo[0])


@app.route('/index/home/<string:username>/<string:table_name>/delete/<int:sno>')
def delete(username, table_name, sno):
    delete_query = "DELETE FROM {0} WHERE sno = {1}".format(table_name, sno)
    executeQuery(createDatabaseConnection(), delete_query)
    print("Your row is successfully deleted")
    # Reset/rearrange the indexing after delete a row from the database
    executeQuery(createDatabaseConnection(), "ALTER TABLE {} DROP sno".format(table_name))
    executeQuery(createDatabaseConnection(), "ALTER TABLE {} AUTO_INCREMENT = 1".format(table_name))
    executeQuery(createDatabaseConnection(),
                 "ALTER TABLE {} ADD sno int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST".format(table_name))

    # return redirect('/index/home/<string:username>/<string:table_name>')
    allToDo = getDataFromTable(createDatabaseConnection(), '*', table_name)
    return render_template('home.html', username=username, table_name=table_name, allToDo=allToDo)


if __name__ == '__main__':
    app.run(debug=True)
