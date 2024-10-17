from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api, abort
import pymongo
from datetime import datetime
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)
api = Api(app)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["cartrack"]

####################################
## Collections: cars, accidents
## cars
##      {
##        VIN: "123ABC", Modelname: "Tesla Model S", Modelyear: "2020",
##        Location: {City: Palo Alto, State: California},
##        previousownerscount: 3, accidents:
##        [
##           {
##             AID: 1, Carsinvolved: ["123ABC", "321CBA"], Date: 12/05/2021,
##             Location: {City: San Francisco, State: California},
##             Description: "Minor fender bender near Golden Gate Bridge"
##           },
##           {
##             AID: 2, Carsinvolved: ["123ABC"], Date: 08/15/2022,
##             Location: {City: Oakland, State: California},
##             Description: "Hit a pole in bad weather, no major injuries"
##           }
##        ]
##      }
## Accidents (AccidentID, Carsinvolved, Time, Location, Description)
## {
##     AID: 1, Carsinvolved: ["123ABC", "321CBA"], Date: 12/05/2021,
##     Location: {City: San Francisco, State: California},
##     Description: "Minor fender bender near Golden Gate Bridge"
##  }


## www.myfirstrestapi.com/api/...?count={}&startIndex={}
##
##
## count = number of results
## startIndex = paging system
####################################

def log(msg):
    '''writes the message in the server.log files. messages include entering/exiting any url methods'''
    with open("server.log", 'a') as f:
        f.write(msg + ' ' + str(datetime.now()) + '\n')
    return

def get_data(collection, filters, count, startIndex):
    '''returns the paginated data and the total count of documents in the given collection'''
    numskips = (startIndex - 1) * count
    print (numskips)
    return list(mydb[collection].find(filters, {"_id":0}).skip(numskips).limit(count)), mydb[collection].count_documents({})

def post_data(collection, data):
    '''adds data to the given collection'''
    mydb[collection].insert_one(data)
    return

def delete_data(collection, filters):
    '''deletes data from the given collection by applying the given filters and returns the count of deleted items'''
    return mydb[collection].delete_many(filters).deleted_count

    
def get_urls(temp_url, count, startIndex, total_count):
    '''returns the url for previous, and next page''' 
    prevPage = temp_url.format(count, startIndex - 1) if startIndex > 1 else None
    nextPage = temp_url.format(count, startIndex + 1) if total_count > count * startIndex else None
    return prevPage, nextPage

def verify_vin(vin):
    '''checks if the given VIN is valid'''
    try:
        return len(vin) == 6
    except:
        return False

## parsing args for pagination
index_args = {'count':fields.Integer(validate=lambda val: val > 0, missing=10), 'startIndex':fields.Integer(validate=lambda val: val > 0, missing=1)}

class Cars(Resource):
    def __init__(self):
        super().__init__()
        self.temp_url = "http://127.0.0.1:5000/api/cars?count={}&startIndex={}"  ##template url for this resource
    
    @use_args(index_args, location="query")
    def get(self, args):
        log(" ==> Cars.get called")
        count, startIndex = args['count'], args['startIndex']
        cars, total_count = get_data("cars", {}, count, startIndex)
        prevPage, nextPage = get_urls(self.temp_url, count, startIndex, total_count)
        log(" <== Cars.get returned")
        return make_response(jsonify({"success": True, "prevPage": prevPage,
                                      "nextPage": nextPage, "data": cars}), 200)

    def post(self):
        data =  eval(request.data.decode())
        vin = data['VIN']
        print (vin)
        car, _ = get_data("cars", {"VIN": vin}, count=1, startIndex=1)
        if len(car) == 0:   # given vin not in the record
            post_data("cars", data)
            data.pop("_id") # removing the _id field because it's not JSON serializable
            return make_response(jsonify({"success": True, "data": data}))
        return make_response(jsonify({"success": False, "message": "VIN already exists"}))
            
        

class Car(Resource):
    def __init__(self):
        super().__init__()
        self.temp_url = "http://127.0.0.1:5000/api/cars/{vin}"  ##template url for this resource
        
    def get(self, vin):
        log(" ==> Car.get called")
        if not verify_vin(vin):
            return make_response(jsonify({"success": False, "message": "VIN not valid"}), 400)  ##Bad request
        car, _ = get_data("cars", {"VIN": vin}, 0, 1)  ## grab all the records
        if len(car) == 0:
            return make_response(jsonify({"success": False, "message": "No car found"}), 404)
        log(" <== Cars.get returned")
        return make_response(jsonify({"success": True, "data":car}), 200)
        
    def delete(self, vin):
        log(" ==> Car.delete called")
        if not verify_vin(vin):
            return make_response(jsonify({"success": False, "message": "VIN not valid"}), 400)  ##Bad request 
        delete_count = delete_data("cars", {"VIN": vin})
        if delete_count == 0:
            return make_response(jsonify({"success": False, "message": "No car found"}), 404)
        log(" <== Car.delete returned")
        return make_response('', 204)
        
        
api.add_resource(Cars, '/api/cars')
api.add_resource(Car, '/api/car/<vin>')


if __name__ == '__main__':
    app.run(debug=True)
