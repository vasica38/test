# REST API
Make sure you have a new virtual env and install requirements.txt


To build the database run `python build_database.py`

To run the application simply run in terminal `python main.py`

Now you can create a request to create a worker using cURL

`curl -X POST \
  http://127.0.0.1:5000/workers \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 08850a64-1268-301f-efb1-0569dd747006' \
  -d '{
	"name" : "test1"
}'`

to create a shift for that worker 
`curl -X POST \
  http://127.0.0.1:5000/shifts \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 84f595e7-ff13-d06a-9700-a5db9381d825' \
  -d '{
	"date" : "18/08/20 08:00:00",
	"worker_name" : "test1"
}'`


To run unit tests `python tests.py`
