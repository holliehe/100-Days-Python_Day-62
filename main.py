from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
#app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    open = TimeField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close = TimeField('Closing TIme e.g. 5:30PM', validators=[DataRequired()])
    coffee_rate = SelectField('Coffee Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi_rate = SelectField('Wifi Strength Rating', choices=['✘️', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_availability = SelectField('Power Socket Availability', choices=['✘️', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    cafe_form = CafeForm()
    if cafe_form.validate_on_submit():
        print("True")
        data_to_write = [cafe_form.cafe.data, cafe_form.url.data, cafe_form.open.data, cafe_form.close.data,
                         cafe_form.coffee_rate.data, cafe_form.wifi_rate.data, cafe_form.power_availability.data]
        with open('cafe-data.csv', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.write('\n')
            csv_writer.writerow(data_to_write)
        print("successfully written.")
        cafe_form = CafeForm(formdata=None)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=cafe_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
