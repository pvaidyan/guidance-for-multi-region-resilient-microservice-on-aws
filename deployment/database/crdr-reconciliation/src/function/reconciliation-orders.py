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
    
    source_db_arn = event.get("source_db_arn")
    target_db_arn = event.get("target_db_arn")
    user_name = event.get("user_name")
    password = event.get("password")
    db_name = event.get("db_name")
    
    src_results = []
    target_results = []
    try:

        print("source db: " + source_db_arn)
        print("target db:" + target_db_arn)
        print("user:" + str(user_name))
        print("database:" + db_name)
        
        try:
            src_conn = pymysql.connect(host=source_db_arn, user=user_name, passwd=password, db=db_name, connect_timeout=5)

        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit(1)
        
        logger.info("SUCCESS: Connection to Source RDS for MySQL instance succeeded")
        
        try:
            target_conn = pymysql.connect(host= target_db_arn, user=user_name, passwd=password, db=db_name, connect_timeout=5)

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
        
        print("Total no of orders in fail-over DB:" + str(len(src_results)))
        
        #get order ids from the restored snapshot in the DR region
        target_rows= read_from_db("CUSTOMER_ORDER", target_conn)
        if len(target_rows) > 0:
            for (id) in target_rows:
                print("Target order id:" + str(id))
                target_results.append(id)
        print("Total no of orders in the restored snapshot:" + str(len(target_results)))
        
        # find the 
        diff = find_diff(src_results, target_results)
        return diff
        
    except botocore.exceptions.ClientError as e:
        logger.error(e)
        raise

    return("reconcliation done!!!")

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
        conn.close()

def find_diff(list1: [], list2: []) -> []:
    return list(set(list1).difference(list2))













