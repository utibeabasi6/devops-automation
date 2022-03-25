from flask import Flask, request
from twilio.rest import Client 
import os
import logging


account_sid =  os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token) 

logger = logging.getLogger()
app = Flask(__name__)

@app.post("/")
def send_whatsapp_message():
    alert = request.json
    logger.warning(alert)
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=f'There are some alerts😱: This is real',      
                              to='whatsapp:+2349030809169' 
                          ) 
    return {"sent": True}

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)