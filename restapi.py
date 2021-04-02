from flask import Flask, Response, request, jsonify, json
from pymongo import MongoClient
import os

app = Flask(__name__)

# establishing connection to mongodb
client = MongoClient("mongodb+srv://" + os.environ['username'] + ":" + os.environ['password'] + "@cluster0.nkw8r.mongodb.net/insent?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
Collection = input("Enter the Collection name you want to access : Users | Visitors | Conversation ")


class MongoAPI:

    def __init__(self, data):
        self.client = client
        cursor = self.client['insent']
        self.collection = cursor[Collection]
        self.data = data

    def read_all(self):
        documents = self.collection.find({}, {'_id': 0})
        if documents is None or documents == {}:
            output = "No data is present in collection to find"
        else:
            output = []
            for data in documents:
                output.append(data)
        return output

    def read_one(self, data):
        documents = self.collection.find_one(data, {"_id": 0})
        if documents is None or documents == {}:
            output = "No data is present in collection to find"
        else:
            output = jsonify(documents)
        return output

    def write(self, data):
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        if response.modified_count > 0:
            output = {'Status': 'Successfully Updated'}
        else:
            output = {"Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        if response.deleted_count > 0:
            output = {'Status': 'Successfully Deleted Document'}
        else:
            output = {"Document not found."}
        return output

    def aggregate(self, data):
        filt = self.data['Filter']
        response = self.collection.aggregate([{"$match": filt}])
        output = [{item: data[item] for item in data if item != '_id'} for data in response]
        return output


@app.route('/find_all', methods=['GET'])  # API for finding all document
def mongo_read_all():
    obj1 = MongoAPI()
    response = obj1.read_all()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# API for finding one document
@app.route('/find_one', methods=['GET'])
def mongo_read_one():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read_one(data)
    return response


# API for inserting document
@app.route('/insert', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# API for updating document
@app.route('/update', methods=['PUT'])
def mongo_update():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide required data"}),
                        status=400,
                        mimetype='application/json')
    if 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide Filter to update the data"}),
                        status=400,
                        mimetype='application/json')
    if 'DataToBeUpdated' not in data:
        return Response(response=json.dumps({"Error": "Please provide Filter to update the data"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.update(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# API for deleting document
@app.route('/delete', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide required data"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# API for aggregation
@app.route('/aggregate', methods=['GET'])
def mongo_aggregate():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide required data"}),
                        status=400,
                        mimetype='application/json')
    if 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide Filter to aggregate the document"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPIVisitor(data)
    response = obj1.aggregate(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
