from email.policy import default
from operator import contains
from random import choices
from typing import Container
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,RadioField
from wtforms.validators import DataRequired

class InfoForm(FlaskForm):
    app_type = SelectField(u'Application Type',choices=['HPC','Non HPC'])
    resource = RadioField(u'Resources',choices=['CPU','GPU'],default='CPU')
    cpu = SelectField(u'CPU Core',choices=[1,2,4,6,8,16,32,64])
    gpu = SelectField(u'GPU',choices=[1,2,4,6,8,16,32,64])
    ram = IntegerField(u'RAM (GB)', validators=[DataRequired()])
    memory = IntegerField(u'Disk (GB)', validators=[DataRequired()])
    no_of_container = IntegerField(u'Number of container', validators=[DataRequired()])
