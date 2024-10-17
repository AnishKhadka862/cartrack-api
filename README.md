##Car Tracking REST API
###This is a REST API built with Flask for tracking cars and their accident histories. The API allows you to add, retrieve, and delete car records, including details about the cars, their locations, and any accidents they have been involved in.

##Features
###Cars Collection: Stores details about cars, including VIN, model, year, location, number of previous owners, and accident history.
###Accidents Collection: Stores accident details, including accident ID (AID), cars involved, date, location, and description.
###Pagination: Supports pagination of car records.

##CRUD Operations:
###Retrieve all car records or a specific car by VIN.
###Add new car records.
###Delete a car record by VIN.

##Technologies Used
###Flask: For building the API.
###MongoDB: For storing car and accident data.
###Flask-RESTful: For building the RESTful routes.
###webargs: For handling query parameters for pagination.

##API Endpoints
1. Get All Cars
GET /api/cars?count={}&startIndex={}
Retrieves all car records, with pagination options for count (number of results) and startIndex (starting page).
Example: GET /api/cars?count=5&startIndex=2
2. Get a Single Car by VIN
GET /api/car/<vin>
Retrieves a single car record by its VIN.
Example: GET /api/car/123ABC
3. Add a Car
POST /api/cars
Adds a new car record to the database.

##Example request body:
json
Copy code
{
  "VIN": "123ABC",
  "Modelname": "Tesla Model S",
  "Modelyear": "2020",
  "Location": {
    "City": "Palo Alto",
    "State": "California"
  },
  "previousownerscount": 3,
  "accidents": []
}
4. Delete a Car by VIN
DELETE /api/car/<vin>
Deletes a car record from the database by its VIN.
Example: DELETE /api/car/123ABC

##Setup and Running the API
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-repo/car-tracking-api.git
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Run the Flask App
bash
Copy code
python main.py
The app will be running at http://127.0.0.1:5000/.

4. MongoDB Setup
Make sure MongoDB is running on your local machine at mongodb://localhost:27017/, and it has a database named cartrack with collections cars and accidents.

Logging
Server logs are written to server.log, recording when any endpoint is accessed.
