from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pollsapp

#loop to place info or input from subject

faceImage = {"SubjectID": 22,
      	 	 "firstname": 'Li',
			 "lastname": 'Bai'}
posts = db.faceImages
post_id = posts.insert_one(faceImage).inserted_id