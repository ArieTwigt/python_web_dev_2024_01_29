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
    # get the saved prediction requests
    prediction_requests = PredictionRequest.query.all()


    # create form object
    form = PredictionRequestForm()

    # if we do a POST request
    if request.method == 'POST':

        # validate the form
        if form.validate_on_submit():
            # get the data from the form
            data = request.form

            # create a new prediction request object: <TODO> add username
            selected_country_code = data['country_code'].upper()
            selected_city = data['city'].lower().capitalize()
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
            return render_template('index.html', form=form, prediction_requests=prediction_requests)
    
        # return to the template
        return redirect(url_for('index'))
    
    # regular GET request
    return render_template('index.html', form=form, prediction_requests=prediction_requests)


# route for generating a prediction
@app.route('/get_weather_data', methods=['POST'])
def get_weather_data():
    # get the id
    prediction_id = request.form.get('prediction_id')

    # get the prediction request object
    prediction_request = PredictionRequest.query.get(prediction_id)

    # get the city and country code
    city = prediction_request.city
    country_code = prediction_request.country_code

    # import the weather data
    predictions_dict = import_weather_by_city(city, country_code)

    # create form object
    form = PredictionRequestForm()

    # get the saved prediction requests
    prediction_requests = PredictionRequest.query.all()

    # return the data to the page
    return render_template('index.html', predictions_dict=predictions_dict
                            ,form=form,
                            selected_city=city,
                            selected_country_code=country_code,
                            prediction_requests=prediction_requests)


# edit an existing prediction request
@app.route('/edit_prediction_request/<id>', methods=['GET', 'POST'])
def edit_prediction_request(id):

    # get the prediction request object
    prediction_request = PredictionRequest.query.get(id)

    # create form object
    form = PredictionRequestForm(obj=prediction_request)

    if request.method == 'POST':

        if form.validate_on_submit():
            # Update and save the edited data
            prediction_request.country_code = form.country_code.data
            prediction_request.city = form.city.data

            # save the new prediction request object
            db.session.commit()
            flash('Prediction request updated successfully', 'success')

            # redirect to index
            return redirect(url_for('index'))
        else:
            flash('Something went wrong', 'danger')
            return render_template('edit_prediction_request.html', 
                                    prediction_request=prediction_request,
                                    form=form)

    # return the data to the page
    return render_template('edit_prediction_request.html', 
                            prediction_request=prediction_request,
                            form=form)


# delete an existing prediction request
@app.route('/delete_prediction_request/<id>', methods=['GET', 'POST'])
def delete_prediction_request(id):
    
        # get the prediction request object
        prediction_request = PredictionRequest.query.get(id)
    
        # create form object
        form = PredictionRequestForm(obj=prediction_request)
    
        # delete the prediction request
        db.session.delete(prediction_request)
        db.session.commit()
        flash('Prediction request deleted successfully', 'secondary')

        # redirect to index
        return redirect(url_for('index'))
