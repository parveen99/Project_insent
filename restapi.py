from flask import Flask, Response, request, jsonify, json
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# establishing connection to mongodb
client = MongoClient(
    "mongodb+srv://sameena:sameena@cluster0.nkw8r.mongodb.net/insent?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

class MongoAPIUser:
    def __init__(self, data):
        self.client = client
        cursor = self.client['insent']
        self.collection = cursor['Users']
        self.data = data

    def read_user(self):
        documents = self.collection.find({},{'_id':0})
        output=[]
        for data in documents:
            output.append(data)
        return output

    def read_user_find_one(self, data):
        documents = self.collection.find_one(data, {"_id": 0})
        output = jsonify(documents)
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
        if response.modified_count > 0:
            output = {'Status': 'Successfully Updated'}
        else:
            output = {"Nothing was updated."}
        return output

    def delete_user(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        if response.deleted_count > 0:
            output = {'Status': 'Successfully Deleted Document'}
        else:
            output = {"Document not found."}
        return output

    def aggregate_find_user(self, data):
        filt = self.data['Filter']
        response = self.collection.aggregate([{"$match": filt}])
        output = [{item: data[item] for item in data if item != '_id'} for data in response]
        return output

class MongoAPIVisitor:
    def __init__(self, data):
        self.client = client
        cursor = self.client['insent']
        self.collection = cursor['Visitors']
        self.data = data

    def read_visitor(self):
        documents = self.collection.find({}, {'_id': 0})
        output = []
        for data in documents:
            output.append(data)

    def read_visitor_find_one(self, data):
        documents = self.collection.find_one(data, {"_id": 0})
        output = jsonify(documents)
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
        if response.modified_count > 0:
            output = {'Status': 'Successfully Updated Document'}
        else:
            output = {"Nothing was updated."}
        return output

    def delete_visitor(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        if response.deleted_count > 0:
            output = {'Status': 'Successfully Deleted Document'}
        else:
            output = {"Document not found."}
        return output

    def aggregate_find_visitor(self, data):
        filt = self.data['Filter']
        response = self.collection.aggregate([{"$match": filt}])
        output = [{item: data[item] for item in data if item != '_id'} for data in response]
        return output

class MongoAPIConversation:
    def __init__(self, data):
        self.client = client
        cursor = self.client['insent']
        self.collection = cursor['Conversation']
        self.data = data

    def read_conversation(self):
        documents = self.collection.find({},{'_id':0})
        output=[]
        for data in documents:
            output.append(data)
        return output

    def write_conversation(self, data):
        filt = self.data['name']
        filter = {"name": filt}
        response = self.collection.aggregate([{"$match": filter}])
        output = [{item: data[item] for item in data if item != '_id'} for data in response]
        if (len(output) == 0):
            response = self.collection.insert_one(data)
            output_response = {'Status': 'Successfully Inserted',
                               'Document_ID': str(response.inserted_id)}
            return output_response
        else:
            self.collection.update(filt, {"$push": {"logs": data['logs']}})
            output_response = {'Status': 'Successfully pushed'}
            return output_response

@app.route('/read_user', methods=['GET'])
def mongo_read_user():
    data = request.json
    obj1 = MongoAPIUser(data)
    response = obj1.read_user()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_visitor', methods=['GET'])
def mongo_read_visitor():
    data = request.json
    obj1 = MongoAPIVisitor(data)
    response = obj1.read_visitor()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_conversation', methods=['GET'])
def mongo_read_conversation():
    data = request.json
    obj1 = MongoAPIConversation(data)
    response = obj1.read_conversation()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_user_find_one', methods=['GET'])
def mongo_read_one_user():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.read_user_find_one(data)
    return response

@app.route('/read_visitor_find_one', methods=['GET'])
def mongo_read_one_visitor():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.read_visitor_find_one(data)
    return response

@app.route('/insert_user', methods=['POST'])
def mongo_write_user():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.write_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/insert_visitor', methods=['POST'])
def mongo_write_visitor():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.write_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/insert_conversation', methods=['POST'])
def conversation_insert():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIConversation(data)
    response = obj1.write_conversation(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/update_user', methods=['PUT'])
def mongo_update_user():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.update_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/update_visitor', methods=['PUT'])
def mongo_update_visitor():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.update_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/delete_user', methods=['DELETE'])
def mongo_delete_user():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.delete_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/delete_visitor', methods=['DELETE'])
def mongo_delete_visitor():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.delete_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_user_find_aggregate', methods=['GET'])
def mongo_read_user_aggregate():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIUser(data)
    response = obj1.aggregate_find_user(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/read_visitor_find_aggregate', methods=['GET'])
def mongo_read_visitor_aggregate():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.aggregate_find_visitor(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
