from flask import Flask,render_template,redirect,session,request
from user import User
app = Flask(__name__)
app.secret_key = 'root'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    User.create(request.form)
    return redirect('/show')

@app.route('/show')
def show():
    users = User.get_all()
    print(users)
    return render_template('show.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)