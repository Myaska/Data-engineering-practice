import boto3
import json
import gocept.pseudonymize
import psycopg2

sqs = boto3.client('sqs')

def message_processing(sqs_url):

    '''This fuction parses messages from the queue'''
    
    postgre_data = []
    attributes = sqs.get_queue_attributes(
        QueueUrl=sqs_url,
        AttributeNames=[
            'ApproximateNumberOfMessages'])
    date = attributes['ResponseMetadata']['HTTPHeaders']['date']
    number = int(attributes['Attributes']['ApproximateNumberOfMessages'])    
        
    for msg in range(number):
        get_message = sqs.receive_message(
                            QueueUrl=sqs_url)
        
        try:                   
            for message in get_message['Messages']:
        
                msg_body = json.loads(message['Body'])
                receipt_handle = message['ReceiptHandle']
            
                sqs.delete_message(QueueUrl=sqs_url,
                                   ReceiptHandle=receipt_handle)
            
                masked_device_id = gocept.pseudonymize.text(msg_body['device_id'], 'secret')
                masked_ip = gocept.pseudonymize.text(msg_body['ip'], 'secret')
                msg_body['masked_device_id'] = masked_device_id
                msg_body['masked_ip'] = masked_ip
                msg_body['create_date'] = date
                msg_body.pop('device_id')
                msg_body.pop('ip')
                
                postgre_data.append(msg_body)                    
        except:
            print('No messages was found')
 
    return postgre_data


def connection(dbname, user_name, password):
    
    '''This fuction connects to the PostgresSQL DB '''
    
    conn = psycopg2.connect("dbname={0} user={1} password={2}".format(dbname, user_name, password))
    cursor = conn.cursor()

    return conn, cursor

def put_data_to_db(conn, cursor, postgre_data, table_name):
    
    '''This fuction iserts data to the table'''
    
    for user in postgre_data:
        placeholders = ', '.join(['%s'] * len(user))
        columns = ', '.join(user.keys())
        
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
        cursor.execute(sql, list(user.values()))
        conn.commit()
        