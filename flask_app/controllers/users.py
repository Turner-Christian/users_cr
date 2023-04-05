from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    user = User.create(request.form)
    # print(user)
    print('-'*15)
    print(request.form)
    return redirect('/show/' + str(user))

@app.route('/show')
def show():
    users = User.get_all()
    return render_template('show.html', users=users)

@app.route('/show/<int:id>')
def show_one(id):
    user = User.get_one(id)
    return render_template('show_user.html', user=user)

@app.route('/edit/<int:id>')
def edit(id):
    user = User.get_one(id)
    return render_template('edit.html', user=user)

@app.route('/update', methods=['POST'])
def update():
    User.update(request.form)
    id = request.form['id']
    return redirect('/show/' + str(id))

@app.route('/delete/<int:id>')
def delete(id):
    user = User.get_one(id)
    return render_template('delete.html', user=user)

@app.route('/delete/confirmation', methods=['POST'])
def confirmation():
    if request.form['which_button'] == 'yes':
        print('YES')
        user = User.delete(request.form['id'])
        return redirect('/show')
    else:
        print('NO')
        return redirect('/show')