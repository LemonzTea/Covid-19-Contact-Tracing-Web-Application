from ..entity.User import User
from ..entity.InfectedPeople import InfectedPeople
import datetime
# import itertools


class HealthStaffUser_ContactTracingController:
	def __init__(self):
		self.INFECTION_TIME = 14 	# Considered as infected for _ days

	# get infected people NRIC for the past 14 days
	def getInfectedPeopleNRIC(self, date):

		# Creates a InfectedPeople object
		infectedPeople = InfectedPeople()

		currentTime = datetime.datetime.today()
		enteredDate = datetime.datetime.strptime(date, '%Y-%m-%d')

		daysAgo = (currentTime - enteredDate).days

		# Gets the NRIC list of infected individuals
		NRICList = infectedPeople.getInfectedPeople(daysAgo,self.INFECTION_TIME)

		# return list of unique NRIC
		return list(set(NRICList))
    

	def getPatientDetails(self, NRICList):
		""" 
		Returns a 2D string array containing the following information.

		[x][0] - NRIC
		[x][1] - First Name
		[x][2] - Middle Name
		[x][3] - Last Name
		[x][4] - Mobile Number
		[x][5] - Gender
		[x][6] - Infected On

		"""
		# Creates a InfectedPeople object
		infectedPeople = InfectedPeople()

		result = []

		for NRIC in NRICList:

			# List to store patient detail
			userInfo = []

			# Get user information
			tempUser = User(NRIC)

			# Get user last infection date
			infectedOnString = infectedPeople.getLastInfectedDate(NRIC)
			infectedOnDateTime = datetime.datetime.strptime(infectedOnString, '%Y-%m-%d %H:%M:%S')
			infectedOnFormatted = infectedOnDateTime.strftime("%d/%m/%Y")

			# Append data to array
			userInfo.append(NRIC)
			userInfo.append(tempUser.getFirstName())
			userInfo.append(tempUser.getMiddleName())
			userInfo.append(tempUser.getLastName())
			userInfo.append(tempUser.getMobile())
			userInfo.append(tempUser.getGender())
			userInfo.append(infectedOnFormatted)

			result.append(userInfo)

		sorted(result, key=lambda e: (e[6], e[0]))
		
		#return users detail list
		return result

			
	