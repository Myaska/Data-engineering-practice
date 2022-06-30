### App for 'data-engineering-take-home'
#### Before run this app you should create: 
- AWS SQS Queue
- send message in the following JSON compatible format:\
[\
  {\
    "user_id": "value1",\
    "app_version": "value2",\
    "device_type": "value3",\
    "ip": "value4",\
    "locale": "value5",\
    "device_id": "value6"\
  }\
]
- create Postgres database
- create table in the database according this defenition: 

CREATE TABLE IF NOT EXISTS user_logins(\
    user_id             varchar(128),\
    device_type         varchar(32),\
    masked_ip           varchar(256),\
    masked_device_id    varchar(256),\
    locale              varchar(32),\
    app_version         varchar(32),\
    create_date         date);

#### To run the app execute the following commands: 
- tested im Python 3.9.12
- pip install -r requirements.txt
- set up app parameters in params.yaml
- sh run_app.sh 

#### To improve this app I would suggest:
- instead of sending message with the data to SQS Queue, put JSON file to S3 bucket and send S3 path to the queue
- store username and password in the Secret Manager
- customize function processing message_processing for different JSON payload
