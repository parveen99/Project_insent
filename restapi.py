from flask import Flask, Response, request, jsonify, json
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("mongodb+srv://sameena:sameena@cluster0.nkw8r.mongodb.net/insent?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")


class MongoAPIUser:
    def __init__(self, data):
        self.client = MongoClient("mongodb+srv://sameena:sameena@cluster0.nkw8r.mongodb.net/insent?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        cursor = self.client['insent']
        self.collection = cursor['Users']
        self.data = data

    def read_user(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write_user(self, data):
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update_user(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

class MongoAPIVisitor:
    def __init__(self, data):
        self.client = MongoClient("mongodb+srv://sameena:sameena@cluster0.nkw8r.mongodb.net/insent?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        cursor = self.client['insent']
        self.collection = cursor['Visitors']
        self.data = data

    def read_visitor(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write_visitor(self, data):
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output
    
    def update_visitor(self, data):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output
    
@app.route('/read_user', methods=['GET'])
def mongo_read_user():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.read_user()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_visitor', methods=['GET'])
def mongo_read_visitor():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.read_visitor()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/insert_user', methods=['POST'])
def mongo_write_user():
    data = request.json
    obj1 = MongoAPIUser(data)
    response = obj1.write_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/insert_visitor', methods=['POST'])
def mongo_write_visitor():
    data = request.json
    obj1 = MongoAPIVisitor(data)
    response = obj1.write_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/update_user', methods=['PUT'])
def mongo_update_user():
    data = request.json
    obj1 = MongoAPIUser(data)
    response = obj1.update_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/update_visitor', methods=['PUT'])
def mongo_update_visitor():
    data = request.json
    obj1 = MongoAPIVisitor(data)
    response = obj1.update_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
