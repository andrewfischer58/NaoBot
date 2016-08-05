from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.pollsapp
#check if faceImage is a collection of pollsapp. if exists, then drop

print(db.collection_names())        #Return a list of collections in 'pollsapp'
if ("faceImages" in db.collection_names()):     #Check if collection "faceImages" 
	collection = db['faceImages']
	print("Deleting: " + collection.name)
	collection.drop()  	


faceImage = [{"id":16,
      	 	 "name":"Lincoln"},
			 {"id":17,
      	 	 "name":"Chris"},
			 {"id":18,
      	 	 "name":"Yiran"},
			 {"id":19,
      	 	 "name":"Ning"},
			 {"id":20,
      	 	 "name":"Andrew"},
			 {"id":21,
      	 	 "name":"Jeff"},
			 {"id":22,
      	 	 "name":"Doctor Bai"},
			 {"id":23,
      	 	 "name":"Jin"}
			 ]
posts = db.faceImages
print("Inserting: "+posts.name)
post_id = posts.insert_many(faceImage).inserted_ids
print("Done Inserting. You have inserted:")
for doc in posts.find():
    print(doc)
