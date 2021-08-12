from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
import pandas as pd
import csv

COFFEE_CHOICE = [('0', '✘'), ('1', '☕'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕')]
WIFI_CHOICE = [('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')]
POWER_CHOICE = [('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField('Location URL', validators=[url()])
    open_time = StringField('Open time', validators=[DataRequired()])
    close_time = StringField('Close_time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating', choices=COFFEE_CHOICE, validators=[DataRequired()])
    wifi_rating = SelectField('WIFI rating', choices=WIFI_CHOICE, validators=[DataRequired()])
    power_outlet_rating = SelectField('Power outlet rating', choices=POWER_CHOICE, validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("/Users/nadun/PycharmProjects/Day-62-coffee-and-wifi/cafe-data.csv", mode="a", encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location_url.data},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    data = pd.read_csv("/Users/nadun/PycharmProjects/Day-62-coffee-and-wifi/cafe-data.csv")
    list_of_rows = []
    # loop through each row and record specific data
    for index, row in data.iterrows():
        each_row = (
            row['Cafe Name'], row['Location'], row['Open'], row['Close'], row['Coffee'], row['Wifi'], row['Power'])
        list_of_rows.append(each_row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
