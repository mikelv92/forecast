import unittest
import json
from app import create_app
import os

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    def test_get_corn_data(self):
        path = self.app.config.get('DATA_LOCATION')
        with open(path + 'CORN.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2013-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
            f.write('2018-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
        res = self.client().get('/data?data_type=corn&months=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('[{"Date":"2018-12-10","Open":31.83,"High":32.049999,"Low":31.4,"Close":31.780001,"Adj Close":31.780001,"Volume":27700}]'))
        

    def test_2_records(self):
        path = self.app.config.get('DATA_LOCATION')
        with open(path + 'CORN.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2018-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
            f.write('2018-12-11,32,32,31,31,31,27700\n')

        res = self.client().get('/data?data_type=corn&months=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            json.loads(res.data), 
            json.loads(
                '[ ' \
                '{"Date":"2018-12-10","Open":31.83,"High":32.049999,"Low":31.4,"Close":31.780001,"Adj Close":31.780001,"Volume":27700},' \
                '{"Date":"2018-12-11","Open":32,"High":32,"Low":31,"Close":31,"Adj Close":31,"Volume":27700}' \
                ']'
            )
        )
        
    def test_negative_months(self):
        res = self.client().get('/data?data_type=corn&months=-1')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data), json.loads('{"error": "Negative months"}'))

    def test_empty_months(self):
        res = self.client().get('/data?data_type=corn&months=')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data), json.loads('{"error": "Months must be a number"}'))
        
    def test_get_ndaq_data(self):
        path = self.app.config.get('DATA_LOCATION')
        with open(path + 'NDAQ.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2013-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
            f.write('2018-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
        res = self.client().get('/data?data_type=ndaq&months=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('[{"Date": "2018-12-10","Open":31.83,"High":32.049999,"Low":31.4,"Close":31.780001,"Adj Close":31.780001,"Volume":27700}]'))

    def test_unknown_data_type(self):
        res = self.client().get('/data?data_type=new_data_type&months=1')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data), json.loads('{"error": "Unknown data type"}'))

    def test_get_uga_data(self):
        path = self.app.config.get('DATA_LOCATION')
        with open(path + 'UGA.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2013-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
            f.write('2018-12-10,31.830000,32.049999,31.400000,31.780001,31.780001,27700\n')
        res = self.client().get('/data?data_type=uga&months=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('[{"Date":"2018-12-10","Open":31.83,"High":32.049999,"Low":31.4,"Close":31.780001,"Adj Close":31.780001,"Volume":27700}]'))

    def test_predictions(self):
        path = self.app.config.get('DATA_LOCATION')
        with open(path + 'UGA.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2018-12-06,24.760000,25.280001,24.280001,25.180000,25.180000,70600\n')
            f.write('2018-12-07,26.100000,26.530001,25.770000,25.809999,25.809999,30400\n')
            f.write('2018-12-10,25.350000,25.600000,24.719999,24.809999,24.809999,29400\n')
        with open(path + 'CORN.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2018-12-06,16.350000,16.400000,16.219999,16.360001,16.360001,35800\n')
            f.write('2018-12-07,16.400000,16.469999,16.379999,16.450001,16.450001,124200\n')
            f.write('2018-12-10,16.370001,16.469999,16.360001,16.379999,16.379999,25800\n')
        with open(path + 'NDAQ.csv', 'w+') as f:
            f.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
            f.write('2018-12-06,89.610001,90.190002,88.739998,89.889999,89.889999,1720400\n')
            f.write('2018-12-07,89.949997,90.110001,87.169998,87.360001,87.360001,1167400\n')
            f.write('2018-12-10,87.360001,87.360001,85.110001,87.099998,87.099998,1033500\n')

        res = self.client().get('/predict')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)

        self.assertTrue(data['NDAQ'])
        self.assertTrue(data['CORN'])
        self.assertTrue(data['UGA'])
        self.assertEqual(data['NDAQ']['mean'], 88.11666600000001)
        self.assertEqual(data['UGA']['mean'], 25.266665999999997)
        self.assertEqual(data['CORN']['mean'], 16.396666999999997)

    def tearDown(self):
        path = self.app.config.get('DATA_LOCATION')
        if os.path.exists(path + 'CORN.csv'):
            os.remove(path + 'CORN.csv')
        if os.path.exists(path + 'UGA.csv'):
            os.remove(path + 'UGA.csv')
        if os.path.exists(path + 'NDAQ.csv'):
            os.remove(path + 'NDAQ.csv')
        return

if __name__ == '__main__':
    unittest.main()