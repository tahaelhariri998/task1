from markupsafe import escape
from flask import Flask
from flask import url_for
from flask import request
import json 
import pandas as pd

app = Flask(__name__)


import sqlite3
from sqlite3 import Error
db_file="Database\\orders\\Master_of_lists_v2(1).db"
@app.route("/messages/<campaign_id>/<vector_id>/<message_id>/", methods = ['GET'])
def fetchMessage(campaign_id,vector_id,message_id):
    response_object = dict()
    try:
        global conn
        conn = sqlite3.connect(db_file,check_same_thread=False)
    except Error as e:
        return e
    campaign_id=escape(campaign_id)
    vector_id=escape(vector_id)
    message_id=escape(message_id)
    cur = conn.cursor()
    sqlquery='select  name from Vectors where id="{vector_id}" and campaign_id="{campaign_id}"'.format(vector_id=vector_id,campaign_id=campaign_id)
    cur.execute(sqlquery)
    name=cur.fetchall()
    newname="_".join(name[0][0].split("-"))
    sqlquery='select  * from {newname} where id={message_id}'.format(newname=newname,message_id=message_id)
    cur.execute(sqlquery)
    messages=cur.fetchall()
    keys=["id","campaign_id","vector_id","text","reaction","status","type","posted_by","replies"]
    tempdict=dict()
    s=len(messages[0][1].split(","))
    tempdict=""
    response_object=dict()
    while s>=0:
        s=s-1
        if  tempdict=="":
            tempdict={"id": messages[0][1].split(",")[s],
                      "text": messages[0][2].split("||")[s], 
                      "reaction": messages[0][3].split(",")[s], 
                      "status": messages[0][4].split(",")[s],
                      "type":'reply',
                      "posted_by":messages[0][6].split(",")[s]}
        else:
            if s==0:
                
                response_object[keys[0]]=message_id
                response_object[keys[1]]=campaign_id
                response_object[keys[2]]=vector_id
                response_object[keys[3]]=messages[0][2].split("||")[s]
                response_object[keys[4]]=messages[0][3].split(",")[s]
                response_object[keys[5]]=messages[0][4].split(",")[s]
                response_object[keys[6]]="message"
                response_object[keys[7]]=messages[0][6].split(",")[s]
                response_object[keys[8]]=[tempdict]
            else:
                dic={ "id": messages[0][1].split(",")[s],
                          "text": messages[0][2].split("||")[s], 
                          "reaction": messages[0][3].split(",")[s], 
                          "status": messages[0][4].split(",")[s],
                          "type":'reply',
                          "posted_by":messages[0][6].split(",")[s],
                          "replies": [tempdict]}
                tempdict=dic
            
    
            
            
            
            
            
            
    json_object = json.dumps(response_object, indent = 4) 
           
    conn.close()
    return json_object