from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pollsapp



faceImage = {"SubjectID":23,
      	 	 "firstname": 'Lincoln',
			 "lastname": 'David'}
posts = db.faceImages
post_id = posts.insert_one(faceImage).inserted_id