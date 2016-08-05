from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pollsapp

#loop to place info or input from subject

faceImage = {"SubjectID": 23,
      	 	 "firstname": 'Jin',
			 "lastname": ''}
posts = db.faceImages
post_id = posts.insert_one(faceImage).inserted_id