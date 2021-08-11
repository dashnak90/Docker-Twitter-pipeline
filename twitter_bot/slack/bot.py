import time
import requests
from sqlalchemy import create_engine

time.sleep(10)

pg = create_engine('postgresql://user:pass123@postgresdb:5432/dbname', echo=True)


webhook_url = 'webhook_url'

while True:
	
    select=pg.execute("SELECT * FROM tweets ORDER BY date DESC LIMIT 1;")
    for i in select.fetchall():
        msg=i[0]		
        user=i[1]		
        date=i[2]
        count=i[4]    
        score=i[5]
        photo=i[3]        
		
    fin_msg=f"*LATEST :snake:PYTHON:snake: TWEET*\n:watch:{date}\n:mega: {msg}\n:dart: Sentiment score : {score}\n:soon: Next tweet will come in 15 seconds..."
	

    data4 = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": fin_msg 
			},
			"accessory": {
				"type": "image",
				"image_url": photo,
				"alt_text": "twitter"}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "image",
					"image_url": photo,
					"alt_text": 'photo'
				},
				{
					"type": "mrkdwn",
					"text": f"*{user}* with *{count} followers* has just tweeted this message."
				}
			]
		}
	]
}



    requests.post(url=webhook_url, json = data4)
    time.sleep(15)

