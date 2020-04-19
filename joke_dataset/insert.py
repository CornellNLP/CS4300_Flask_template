import psycopg2
import json

try:
   connection = psycopg2.connect(
                                  host="localhost",
                                  port="5432",
                                  database="hahadata")
   cursor = connection.cursor()
   with open ('./final.json') as f: 
       data = json.load(f)
       string = "\'" + json.dumps(data) + "\'"
       postgres_insert_query = "Insert into jokes (text, score, categories) select text, score, categories from json_populate_recordset(null::jokes, " + string + ");"
   cursor.execute(postgres_insert_query)

   connection.commit()
   count = cursor.rowcount
   print (count, "Records inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")