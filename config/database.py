from pymongo import MongoClient

mongoDbUrl="mongodb+srv://gokuhulk234:a4sivdEq0gCifmnE@cluster0.y5w9ppw.mongodb.net/autism_spectrum?retryWrites=true&w=majority"
port=8000
client = MongoClient(mongoDbUrl, port)
db = client["autism_spectrum"]

