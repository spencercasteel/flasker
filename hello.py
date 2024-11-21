from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# source virt/bin/activate
# deactivate

# export FLASK_APP=hello
# export FLASK_DEBUG=1
# flask run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Password'

class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


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