from pymongo import MongoClient

#client = MongoClient('localhost', 27017, username='v1ume_user', password='@V1um3pWd!!', authSource='viume')
client = MongoClient('193.203.167.201', 27017, username='v1ume_user', password='@V1um3pWd!!', authSource='viume')
db = client['viume']
