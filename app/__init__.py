from flask import Flask, request, jsonify, Blueprint, send_from_directory
import pandas as pd
import datetime
import dateutil.relativedelta
import os

from instance.config import app_config

def create_app(config_name):
    app = Flask(__name__, static_folder='../frontend/build')
    app.config.from_object(app_config[config_name])

    @app.route('/data', methods=['GET'])
    def get_corn_data():
        data_type = request.args.get('data_type')
        
        try:
            months = int(request.args.get('months'))
        except ValueError:
            response = jsonify({'error':'Months must be a number'})
            response.status_code = 400
            return response

        if months < 0:
            response = jsonify({'error':'Negative months'})
            response.status_code = 400
            return response

        if data_type == 'corn':
            filename = 'CORN.csv'
        elif data_type == 'ndaq':
            filename = 'NDAQ.csv'
        elif data_type == 'uga':
            filename = 'UGA.csv'
        else:
            response = jsonify({'error':'Unknown data type'})
            response.status_code = 400
            return response

        df = pd.read_csv(app.config.get('DATA_LOCATION') + filename, sep=',')
        
        max_date = datetime.datetime.strptime(df['Date'].max(), '%Y-%m-%d')
        start_date = max_date - dateutil.relativedelta.relativedelta(months=months)

        data = df.loc[df['Date'] >= str(start_date)]
        data = data.to_json(orient='records')
        
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')

        response.data = data
        response.status_code = 200
        return response

    @app.route('/predict', methods=['GET'])
    def get_prediction():
        uga_df = pd.read_csv(app.config.get('DATA_LOCATION') + 'UGA.csv', sep=',')
        corn_df = pd.read_csv(app.config.get('DATA_LOCATION') + 'CORN.csv', sep=',')
        ndaq_df = pd.read_csv(app.config.get('DATA_LOCATION') + 'NDAQ.csv', sep=',')

        uga_last_3_days = uga_df.sort_values(by=['Date']).iloc[-3:]
        corn_last_3_days = corn_df.sort_values(by=['Date']).iloc[-3:]
        ndaq_last_3_days = ndaq_df.sort_values(by=['Date']).iloc[-3:]

        uga_mean = float(uga_last_3_days['Close'].mean())
        corn_mean = float(corn_last_3_days['Close'].mean())
        ndaq_mean = float(ndaq_last_3_days['Close'].mean())

        uga_prediction_date = datetime.datetime.strptime(uga_df['Date'].max(), '%Y-%m-%d') + dateutil.relativedelta.relativedelta(days=1)
        corn_prediction_date = datetime.datetime.strptime(corn_df['Date'].max(), '%Y-%m-%d') + dateutil.relativedelta.relativedelta(days=1)
        ndaq_prediction_date = datetime.datetime.strptime(ndaq_df['Date'].max(), '%Y-%m-%d') + dateutil.relativedelta.relativedelta(days=1)

        response = jsonify({
            'UGA': {
                'mean': uga_mean, 
                'date': uga_prediction_date.isoformat()
            }, 
            'CORN': {
                'mean': corn_mean, 
                'date': corn_prediction_date.isoformat()
            }, 
            'NDAQ': {
                'mean': ndaq_mean, 
                'date': ndaq_prediction_date.isoformat()
            }
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 200
        return response

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != '':
            return send_from_directory('../frontend/build', path)
        else:
            return send_from_directory('../frontend/build', 'index.html')

    return app