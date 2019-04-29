# app/beerlog/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, SelectField, TextField
from wtforms.fields.html5 import DateField

from ..models.enums import OrganisationEnum, ProductEnum


class FilterForm(FlaskForm):
    """
    Form for filtering statistics list
    """

    user = TextField('User (n.ethz, RFID or AMIV User ID)')
    date_from = DateField('Start date')
    date_to = DateField('End date')
    organisation = SelectField('Organisation', choices=[(None, 'all'), *OrganisationEnum.choices()], coerce=OrganisationEnum.coerce)
    product = SelectField('Product', choices=[(None, 'all'), *ProductEnum.choices()], coerce=ProductEnum.coerce)
    submit = SubmitField('Filter')
