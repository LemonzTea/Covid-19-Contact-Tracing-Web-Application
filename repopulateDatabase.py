### WARNING: ONLY USE THIS IF YOU WANT A CLEAN RESET ON THE DATABASE
###          THIS Will drop all tables and re-create them using a fresh slate
###          ANY CHANGES MADE AFTER INITIAL SETUP WILL BE LOST

# TO REPOPULATE THE DATABASE 
#   1. Copy all classes from entities.py and replace the classes below
#   2. type the following command in command prompt
#      >>> python repopulateDatabase.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randrange, randint, uniform
from datetime import datetime, timedelta

app = Flask(__name__)

# Database Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

# -------------------------------------------------
#               Editable Settings
# -------------------------------------------------
# Location History Settings
CHANCE_TO_GO_OUT = 33          # In percentage (33%)
MIN_LOCATION_VISITED = 1        # No of location
MAX_LOCATION_VISITED = 3        # No of location

# Infection Setting
POPULATION_PERCENTAGE_CONFIRMED_INFECTED_DAILY = 0.01	  # In percentage (0.01%)


# COPIES OF ALL ENTITY BELOW. COPY ALL CLASS ENTITY FROM ENTITIES.PY BEFORE RUNNING CODE
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Get all business records
    @staticmethod
    def getAllBusiness():
        return Business.query.all()

    # Get business ID from business name
    @staticmethod
    def getID(name):
        result = Business.query.filter_by(name=name).first()

        # Id no result is found
        if result is None:
            return None
        
        # If result is found
        return result.id
    
class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    businessID = db.Column(db.String(10), db.ForeignKey('business.id'), nullable=False)
    locationName = db.Column(db.String(100), unique=True, nullable=False)

    # Get all location records
    @staticmethod
    def getAllLocation():
        return Location.query.all()

    # Get location ID from location name
    @staticmethod
    def getID(name):
        result = Location.query.filter_by(locationName=name).first()

        # Id no result is found
        if result is None:
            return None
        
        # If result is found
        return result.id
    
    # Get location ID from location name
    @staticmethod
    def getName(id):
        result = Location.query.filter_by(id=id).first()

        # Id no result is found
        if result is None:
            return None
        
        # If result is found
        return result.locationName

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    accountActive = db.Column(db.Boolean, default=True)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC, password):
        # Verify the user by their NRIC and password
        result = User.query.filter_by(NRIC=NRIC,password=password).first()
        # select * from user where TABLE COLUMN = 'NRIC_VALUE' AND TABLE COLUMN = 'password value' limit 1;

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

    # Check if user exists, returns True/False
    @staticmethod
    def getAccountStatus(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()
        return result.accountActive

    # Search for a user
    @staticmethod
    def getAllUser():
        return User.query.all()
    
    # Check if a NRIC exist in the database
    @staticmethod
    def hasRecord(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

class BusinessUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    businessID = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = BusinessUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True
    
    @staticmethod
    def getUsers(businessName):
        userQuery = BusinessUser.query\
                                .join(User, User.NRIC==BusinessUser.NRIC)\
                                .join(Business, Business.id==BusinessUser.businessID)\
                                .filter(User.NRIC==BusinessUser.NRIC)\
                                .filter(BusinessUser.businessID==Business.getID(businessName))\
                                .all()
        return userQuery   

class HealthStaffUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    licenseNo = db.Column(db.Integer, unique=True, nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = HealthStaffUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

class OrganisationUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    organisationID = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = OrganisationUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sent_by = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
    sent_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    alert_type = db.Column(db.String(100), nullable=False)
    recipient_NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False,)
    message = db.Column(db.Text, nullable=False)
    read_on = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean, default=False)

    @staticmethod
    def addRecord(sent_by, alert_type, recipient_NRIC, message):
        record = Alert(sent_by=sent_by, alert_type=alert_type,
                       recipient_NRIC=recipient_NRIC,
                       message=message)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def getUserAlert(NRIC):
        result = Alert.query.filter_by(recipient_NRIC=NRIC)
        
        if result is not None:
            return result
        else:
            return "no alerts"
    
    @staticmethod
    def updateRecord(id):
        record = Alert.query.filter_by(id=id)\
                            .update({Alert.is_read: True,
                                    Alert.read_on: datetime.now()})
        print(record)
        db.session.commit()
        return record

class LocationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
    location_visited = db.Column(db.Integer, db.ForeignKey('location.id'), autoincrement=True)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def getLocationHistory(NRIC):
        results = LocationHistory.query\
                                .filter_by(NRIC=NRIC)\
                                .order_by(LocationHistory.time_in.desc())\
                                .all()
        # If no result is found
        if results is None:
            return None

        # If result is found
        return results

    @staticmethod
    def getLocationHistory(NRIC, date):
        results = LocationHistory.query\
                                .filter_by(NRIC=NRIC)\
                                .filter(LocationHistory.time_in >= date)\
                                .filter(LocationHistory.time_out < (date + timedelta(1)))\
                                .order_by(LocationHistory.time_in.desc())\
                                .all()
        # If no result is found
        if results is None:
            return None

        # If result is found
        formatted_result = []
        for result in results:
            formatted_result.append(result.location_visited)

        return formatted_result

class InfectedPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
    infected_on = db.Column(db.DateTime, nullable=False)
    
    @staticmethod
    def getAllRecords():
        earliest_date = datetime.date.today() - datetime.timedelta(days=28)
        result = InfectedPeople.query\
                                .filter_by(infected_on > earliest_date)\
                                .order_by(infected_on.desc())\
                                .all()
        return result

    # Get the NRIC of everyone affect since 14 days before date provided
    @staticmethod
    def getCurrentlyInfected(date):
        earliest_date = date - timedelta(days=14)
        results = InfectedPeople.query\
                               .filter(InfectedPeople.infected_on >= earliest_date)\
                               .filter(InfectedPeople.infected_on < (date + timedelta(1)))\
                               .order_by(InfectedPeople.infected_on.desc())\
                               .all()

        # Return if no results
        if results is None:
            return None

        # Return list of NRIC
        allInfected = []
        for result in results:
            allInfected.append(result.NRIC)
        return allInfected
        

    


# Code to create and populate data

#16 ^ 3  = 4096 unique names / accounts
firstName = ['Addison', 'Bowie', 'Carter', 'Drew', 'Eden', 'Finn', 'Gabriel', 'Hayden', 'Jamie', 'Jules', 'Ripley', 'Skylar', 'Ashton', 'Caelan', 'Flynn', 'Kaden']
middleName = ['Angel', 'Asa', 'Bay', 'Blue', 'Cameron', 'Gray', 'Lee', 'Quinn', 'Rue', 'Tate', 'Banks', 'Quince', 'Finley', 'Shea', 'Pace', 'James']
lastName = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Wilson', 'Taylor', 'Moore', 'White', 'Anderson', 'Rodriguez', 'Lopez', 'Walker']
gender = ['M', 'F']

businessID = range(1, 11)
businessName = ['Bapple', 'Amazone', 'Fishbook', 'Boogle', 'McRonald\'s', '7-Melon', 'Sunbucks', 'Blokeswagon', 'Cola Coca', 'Borgar King']
branchLocation = ['Ang Mo Kio', 'Bishan', 'Choa Chu Kang', 'Woodlands', 'Punggol', 'Tampines', 'Pasir Ris', 'Yishun', 'Jurong', 'Sengkang']


# Drop all existing tables
db.drop_all()
print('All tables have been dropped')

# Recreate all tables again
db.create_all()
print('All tables have been created')

# Create BUSINESS record
for business in businessName:
    newBusiness = Business(name=business)
    db.session.add(newBusiness)
print('All business entity has been created')

# Create ORGANISATION record
newOrganisation = Organisation(name='Ministry of Health')
db.session.add(newOrganisation)
print('All organisation enity created')

# Create USER record
# All users types are added to this database, before randomly deciding if this user
# is a public, business, health staff, organisation user
count = 0
licenseNo = 10000000

# Generate Users ()
for x in firstName:
    for y in middleName:
        for z in lastName:
            count += 1

            # Generate NRIC
            NRIC = 'S'+ '{:04d}'.format(count)

            # Generate a random usertype
            mobile = 90000000 + count
            random_gender = randint(0,len(gender)-1)

            # Add User
            newUser = User(NRIC=NRIC,
                           password=NRIC,
                           firstName=x, 
                           middleName=y, 
                           lastName=z, 
                           mobile=mobile, 
                           gender=gender[random_gender])
            db.session.add(newUser)
            print('User added. {} new users added.'.format(count), end =' ')


            if count < 1000:
                print('Account type: Public')

            # Generate a business user
            elif 1000 <= count < 2000:
                random_businessID = randint(1,len(businessID))
                newBusinessUser = BusinessUser(NRIC=NRIC, businessID=random_businessID)
                db.session.add(newBusinessUser)
                print('Account type: Business')

            # Generate a health user
            elif 2000 <= count < 3000:
                licenseNo += 1
                newHealthStaffUser = HealthStaffUser(NRIC=NRIC, licenseNo=licenseNo)
                db.session.add(newHealthStaffUser)
                print('Account type: Health Staff')

            # Generate a organisation user
            else:
                newOrganisationUser = OrganisationUser(NRIC=NRIC, organisationID=1)
                db.session.add(newOrganisationUser)
                print('Account type: Organisation')


# Generate Locations (100 Locations)
count = 1
allLocations = {}
for business in businessName:
    for branch in branchLocation:
        locationName = '{} - {} Branch'.format(business, branch)
        allLocations[count] = locationName
        newLocation = Location(businessID=count, locationName=locationName)
        db.session.add(newLocation)
        print('Location entity has been created - {}'.format(locationName))
    count += 1



# Variable Setup
totalNumberOfUsers = range(1, 4097)
numOfDays = range(31, -1, -1)
today = datetime.now()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)


# Generate Location History
noOfRecords = 0
for i in numOfDays:
    for userID in totalNumberOfUsers:
        NRIC = 'S'+ '{:04d}'.format(userID)
        # Random chance to visit location
        chance = randint(0, 100)

        # if user goes out
        if chance <= CHANCE_TO_GO_OUT:

            # Randomly generate number of place visited
            numOfLocationVisited = randint(MIN_LOCATION_VISITED, MAX_LOCATION_VISITED)
            locationVisited = []

            # Add all location visited
            for location in range(numOfLocationVisited):
                visitLocation = randint(1, 100)
                while visitLocation in locationVisited:
                    visitLocation = randint(1, 100)
                locationVisited.append(visitLocation)

            # Add to location history
            for location in locationVisited:
                time_in = today - timedelta(i)
                time_in_hour = randint(0, 21)
                time_in_min = randint(0, 59)
                time_in = time_in.replace(hour=time_in_hour, minute=time_in_min)
                time_out = time_in.replace(hour=time_in_hour + randint(0, 2), minute=randint(0, 59))

                newLocationRecord = LocationHistory(NRIC=NRIC, location_visited=location, time_in=time_in , time_out=time_out)
                db.session.add(newLocationRecord)
                noOfRecords += 1
                print('Location History Record on {}. Total Location history Record = {}'.format(time_in, noOfRecords))

# Generate Infected Record
noOfRecords = 0
for i in numOfDays:
    for userID in totalNumberOfUsers:            
        NRIC = 'S'+ '{:04d}'.format(userID)
        # Random chance to visit location
        chance = uniform(0.00, 100.00)

        #if user is infected
        if chance <= POPULATION_PERCENTAGE_CONFIRMED_INFECTED_DAILY:
            infected_on = visited_on = today - timedelta(i)
            newinfectedRecord = InfectedPeople(NRIC=NRIC, infected_on=infected_on)
            db.session.add(newinfectedRecord)
            noOfRecords += 1
            print('Infected History Recorded on {}. Total Infected Individual Record = {}'.format(infected_on, noOfRecords))

# Commit Records
db.session.commit()
print('All entries committed to database')
