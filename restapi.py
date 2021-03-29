from flask import Flask,request,Response
from pymongo import MongoClient
import json

app=Flask(__name__)

class RestAPI:
    def __init__(self,data):
        self.client = MongoClient('mongodb://docadmin:insent2021@cluster-insent.cluster-cippjt9vx3x1.us-west-2.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')
        db = data['Insent']
        collection_1 = data['User']
        cursor = self.client[db]
        self.collection_1=cursor[collection_1]
        self.data = data


    def find_one_document(self):
        documents=self.collection_1.find()
        return documents

@app.route('/user', methods=['GET'])
def mongo_read_one():
    data=request.json
    if data is None or data=={}:
        return Response(response=json.dumps({"Error":"Please provide data"}), status=400,mimetype='application/json')

    obj1=RestAPI(data)
    response = obj1.find_one_document()
    return Response(response=json.dumps(response),status=200,mimetype='application/json')


if __name__=='__main__':
    app.run(debug=True,port=5001,host='0.0.0.0')
