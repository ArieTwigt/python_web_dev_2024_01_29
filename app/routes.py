from flask import render_template, request, url_for, redirect, flash
from sqlalchemy.exc import IntegrityError
from app import app, db
from app.forms import PredictionRequestForm
from app.models import PredictionRequest

from app.utils.import_weather_data import import_weather_by_city
from app.utils.conversion_functions import convert_dict_to_df

# initial route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    # create form object
    form = PredictionRequestForm()

    # if we do a POST request
    if request.method == 'POST':

        # validate the form
        if form.validate_on_submit():
            # get the data from the form
            data = request.form

            # create a new prediction request object: <TODO> add username
            selected_country_code = data['country_code']
            selected_city = data['city']
            prediction_request = PredictionRequest(username="test",
                                                country_code=selected_country_code,
                                                city=selected_city)
            


            # save the new prediction request object        
            try:
                db.session.add(prediction_request)
                db.session.commit()
                flash(f'Saved prediction request for country code: <b>{selected_country_code}</b> and city: <b>{selected_city}</b>', 'alert alert-success')
            except IntegrityError:
                db.session.rollback()
                flash(f'The prediction combination for country: <b>{selected_country_code}</b> and city: <b>{selected_city}</b>', 'alert alert-danger')
        else:
            flash(f'Wrong', 'alert alert-danger')
            return render_template('index.html', form=form)
    
        # return to the template
        return redirect(url_for('index'))
    
    # regular GET request
    return render_template('index.html', form=form)


# route for generating a prediction
@app.route('/get_weather_data', methods=['GET', 'POST'])
def get_weather_data():
    # hardcoded country code and city
    country_code = 'NL'
    city = 'Amsterdam'

    # import the weather data
    predictions_dict = import_weather_by_city(city, country_code)

    # create form object
    form = PredictionRequestForm()

    # return the data to the page
    return render_template('index.html', predictions_dict=predictions_dict
                            , form=form)