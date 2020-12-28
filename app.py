from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SECRET_KEY'] = 'sEcReTkEy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dan/Desktop/HackingProject/sqlite3/database.db'
Bootstrap(app)
db = SQLAlchemy(app)





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))




class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('remember me')




class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])




@app.route('/', methods=['POST', 'GET'])##begins with page with two buttons "student" or "teacher"
def index2():
    return render_template('test.html')




@app.route('/studentLogin', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return render_template("dashboard.html")
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('studentLogin.html', form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>UserAddedToDataBase</h1>'

    return render_template("signup.html", form=form)



@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)