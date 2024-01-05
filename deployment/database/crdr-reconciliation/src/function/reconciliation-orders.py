import os
import sys
import logging
import pymysql
import json
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    client = boto3.client('rds')
    
    source_db_endpoint = event.get("source_db_endpoint")
    target_db_endpoint = event.get("target_db_endpoint")
    user_name = os.environ["user_name"]
    password = os.environ["password"]
    # user_name = event.get("user_name")
    # password = event.get("password")
    db_name = event.get("db_name")
    
    src_results = []
    target_results = []
    try:

        print("source db endpoint: " + str(source_db_endpoint))
        print("target db endpoint:" + str(target_db_endpoint))
        print("user:" + str(user_name))
        print("database:" + db_name)
        
        try:
            src_conn = pymysql.connect(host=source_db_endpoint, user=user_name, passwd=password, db=db_name, connect_timeout=5)

        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit(1)
        
        logger.info("SUCCESS: Connection to Source RDS for MySQL instance succeeded")
        
        try:
            target_conn = pymysql.connect(host= target_db_endpoint, user=user_name, passwd=password, db=db_name, connect_timeout=5)

        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit(1)
        
        logger.info("SUCCESS: Connection to Target RDS for MySQL instance succeeded")
        
        #get order ids from the fail-over DB in the DR region
        src_rows= read_from_db("CUSTOMER_ORDER", src_conn)
        if len(src_rows) > 0:
            for (id) in src_rows:
                print("Source order id:" + str(id))
                src_results.append(id)
        
        print("Total no of orders in restored snapshot :" + str(len(src_results)))
        
        #get order ids from the restored snapshot in the DR region
        target_rows= read_from_db("CUSTOMER_ORDER", target_conn)
        if len(target_rows) > 0:
            for (id) in target_rows:
                print("Target order id:" + str(id))
                target_results.append(id)
        print("Total no of orders in the fail-over DB in us-west-2:" + str(len(target_results)))
        
        
        final_results = []
        
        # find the diff of orders in the fail-over DB and the restored snapshot in the DR region
        diff = find_diff(src_results, target_results)
        
        cs_diff= ','.join([str(*i) for i in diff])
        
        if len(diff) > 0:
            for (id) in diff:
                final_results.append(read_all_orders_from_db(target_conn,id))

        print("Total no of orders that are not in the fail-over DB in us-west-2:" + str(len(final_results)))        
        target_conn.close()
        src_conn.close()
            
        return final_results
        
    except botocore.exceptions.ClientError as e:
        logger.error(e)
        raise

    return("reconcliation report generated!!!")

def read_all_orders_from_db(conn, id):
    try:
        id_val= str(*id)
        new_cursor = conn.cursor()
    
        # query = "SELECT co.id,co.email, co.firstName, co.lastName,coi.productId, coi.name, coi.price FROM CUSTOMER_ORDER co INNER JOIN CUSTOMER_ORDER_ITEM coi ON co.id = coi.order_id where co.id IN (\"" + id_val + "\")" 
        query = "SELECT * from CUSTOMER_ORDER where id=" + "\"" + id_val + "\""
        print("Printing query:" + query)
        new_cursor.execute(query)
        rows = new_cursor.fetchall()
        return rows
        
    except Exception as e:
        print(e)
        return None
    finally:
        new_cursor.close()
       
        
        
def read_from_db(table_name, conn):
    try:
      
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM " + table_name)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        

def find_diff(list1: [], list2: []) -> []:
    return list(set(list1).difference(list2))













