import utils 
import yaml

def main(sqs_url, table_name, dbname, user_name, password):   
    
    '''  This is a main driver function   '''
 
    
    postgre_data = utils.message_processing(sqs_url)       
    conn, cursor = utils.connection(dbname, user_name, password)
    utils.put_data_to_db(conn, cursor, postgre_data, table_name)

if __name__ == "__main__":         
    with open('params.yaml') as f:        
        params = yaml.load(f, Loader=yaml.FullLoader)

    main(params['sqs_url'], 
         params['table_name'], 
         params['dbname'], 
         params['user_name'], 
         params['password'])
    