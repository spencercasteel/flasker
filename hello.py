from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# source virt/bin/activate
# deactivate

# export FLASK_APP=hello
# export FLASK_DEBUG=1
# flask run

# flask shell
# db.create_all()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    submit = SubmitField('Submit')

class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('has been updated successfully!')
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash('Error! Try Again!')
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash('user added successfully!')
    our_users = User.query.order_by(User.date_added)
    return render_template('add_user.html', 
            form=form,
            name=name,
            our_users=our_users)

@app.route('/')
def index():
    first_name = 'spencer'
    favorite_pizza = ['pepperoni', 'cheese', 'ham', 'bannana peppers', 41]

    return render_template('index.html', 
        first_name=first_name,
        favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):

    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfuly')
    return render_template('name.html',
        name = name,
        form = form)