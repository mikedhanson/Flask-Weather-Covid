import requests
import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import COVID19Py
#from wtforms import SelectField

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

weatherAPIToken = os.getenv('WeatherAPIToken')

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid={ weatherAPIToken }'
    r = requests.get(url).json()
    return r


@app.route('/')
def index_get():
    cities = City.query.all()
    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')

    if not new_city:
        err_msg = 'Cant find blank value'

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = f'Cant find { new_city }'
        else:
            err_msg = f'{ new_city } already exists!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash(f'{ new_city } added succesfully!')

    return redirect(url_for('index_get'))


@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))


@app.route('/covid', methods=['GET', 'POST'])
def covid_index():
    covid_data = []
    covid19 = COVID19Py.COVID19(data_source="jhu")
    all_data = covid19.getAll()
    covid_loc = get_country_list()

    item_selected = request.form.get('country_select')
    #print(f'item selected: {item_selected}')

    if item_selected:
        index = get_country_byIndex(item_selected)
        country_name = all_data['locations'][index]['country']
        country_pop = all_data['locations'][index]['country_population']
        country_coord = all_data['locations'][index]['coordinates']
        country_lastUpdated = all_data['locations'][index]['last_updated']

        output_confirmed = all_data['locations'][index]['latest']['confirmed']
        output_deaths = all_data['locations'][index]['latest']['deaths']
        output_recovered = all_data['locations'][index]['latest']['recovered']

    else:

        country_name = 'World'
        country_pop = '7.8 Billion'
        country_coord = 'Not Applicable'
        country_lastUpdated = 'Now'

        output_confirmed = all_data['latest']['confirmed']
        output_deaths = all_data['latest']['deaths']
        output_recovered = all_data['latest']['recovered']

    covidtable = {
        'countryName': country_name,
        'confirmed': output_confirmed,
        'deaths': output_deaths,
        'recovered': output_recovered,
        'population': country_pop,
        'coordinates': country_coord,
        'last_updated': country_lastUpdated,

    }
    covid_data.append(covidtable)

    return render_template('covid.html', covid_data=covid_data, covid_locations=covid_loc)


def get_country_list():
    covid19 = COVID19Py.COVID19(data_source="jhu")
    all_data = covid19.getAll()
    location_data = all_data['locations']

    covid_data_locations = []
    for index in range(len(location_data)):
        country = location_data[index]['country']
        if country not in covid_data_locations:
            covid_data_locations.append(country)
    # for dic in location_data:
    #     #print(f'dic is {dic}')
    #     for key in dic:
    #         pass
            #print(f'key is {key}')
            #print(dic[key])

    return covid_data_locations


def get_country_byIndex(country):

    location_data = COVID19Py.COVID19(data_source="jhu").getAll()['locations']
    #covid_country_id = []

    for index in range(len(location_data)):
        c = location_data[index]['country']
        if country == c:
            val = index

    return val


def get_covid_data():
    covid_data = []
    covid19 = COVID19Py.COVID19(data_source="jhu")
    all_data = covid19.getAll()
    latest_confirmed = all_data['latest']['confirmed']
    latest_deaths = all_data['latest']['deaths']
    latest_recovered = all_data['latest']['recovered']

    covidtable = {
        'confirmed': latest_confirmed,
        'deaths': latest_deaths,
        'recovered': latest_recovered,
    }
    covid_data.append(covidtable)
    return covid_data


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


app.run(host='0.0.0.0', port=5000)
