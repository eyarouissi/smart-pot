# using python 3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from data import PLANTS

app = Flask(__name__)
# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Enter the name of the plant to check its planning for the week', validators=[Required()])
    submit = SubmitField('Submit')

# define functions to be used by the routes (just one here)

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        name = row["Common_Name"]
        names.append(name)
    return sorted(names)

# all Flask routes below

# two decorators using the same function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    names = get_names(PLANTS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    water_needs = ""
    Climate_Zones=""
    Light_Needs=""
    Soil_Type=""
    Maintenance=""
    if form.validate_on_submit():
        name = form.name.data
        if name in names:
            for row in PLANTS:
                if name==row["Common_Name"]:
                    row_wanted=row
                    water_needs=row["Water_Needs"]
                    Climate_Zones=row["Climate_Zones"]
                    Light_Needs=row["Light_Needs"]
                    Soil_Type=row["Soil_Type"]
                    Maintenance=row["Maintenance"]
                message = "Here is what your plant really needs :" 
                msg_water = "water_needs:" + water_needs
                
            # empty the form field
                form.name.data = ""
        else:
            message = "The plant that you entered is not in our database."
    # notice that we don't need to pass name or names to the template
    return render_template('index.html', form=form, message=message,water_needs=water_needs,Climate_Zones=Climate_Zones,Light_Needs=Light_Needs,Soil_Type=Soil_Type,Maintenance=Maintenance)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
