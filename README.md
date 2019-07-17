Run the webapp:
docker image build --tag forecast:1.0 .

docker container run -d -p 5000:5000 --name forecast-1.0 forecast:1.0

Open browser at http://localhost:5000

To run the tests:
python test.py