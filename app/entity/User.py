from ...dbConfig import dbConnect, dbDisconnect

class User:
	# Constructor for user
	def __init__(self, NRIC):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Select User from database and populate instance variables
		result = db.execute("""SELECT NRIC, password, firstName,
									  middleName, lastName, mobile, gender,
									  accountActive, accountType
							   FROM user 
							   WHERE NRIC = (?)""", (NRIC,)).fetchone()

		# If a result is returned, populate object with data
		if result is not None:
			# Initialise instance variables for this object
			self.__NRIC = NRIC
			self.__password = result[1]
			self.__firstName = result[2]
			self.__middleName = result[3]
			self.__lastName = result[4]
			self.__mobile = result[5]
			self.__gender = result[6]
			self.__accountActive = result[7]
			self.__accountType = result[8]
		else:
			self.__NRIC = None
			self.__password = None
			self.__firstName = None
			self.__middleName = None
			self.__lastName = None
			self.__mobile = None
			self.__gender = None
			self.__accountActive = None
			self.__accountType = None

		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Methods
	def getNRIC(self):
		"""Returns the NRIC of the user"""
		return self.__NRIC

	def getPassword(self):
		"""Returns the Password of the user"""
		return self.__password

	def getFirstName(self):
		"""Returns the first name of the user"""
		return self.__firstName
	
	def getMiddleName(self):
		"""Returns the middle name of the user"""
		return self.__middleName

	def getLastName(self):
		"""Returns the last name of the user"""
		return self.__lastName

	def getMobile(self):
		"""Returns the mobile number of the user as an int"""
		return int(self.__mobile)
	
	def getGender(self):
		"""Returns the gender of the user"""
		return self.__mobile
	
	def getAccountActive(self):
		"""Returns True if account is active"""
		return bool(self.__accountActive)
	
	def getAccountType(self):
		"""Returns the accountType of the user"""
		return self.__accountType

	# Mutator Methods
	def updatePassword(self, password):
		""" 
		Updates the password of the user. 
		Returns True if updated successfully
		Returns False if update failed
		"""

		# Update the object's recorded password"
		self.__password = password

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the password for the user
		db.execute("""UPDATE user
					  SET password = (?)
					  WHERE NRIC = (?)""", (password, self.__NRIC))
		
		# Commit the update to the database
		connection.commit()
		
		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False	

	def updateMobile(self, mobile):
		""" 
		Updates the mobile number of the user
		Returns True if updated successfully
		Returns False if update failed
		"""

		# Update the object's recorded mobile number"
		self.__mobile = mobile

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the mobile number for the user
		db.execute("""UPDATE user
					  SET mobile = (?)
					  WHERE NRIC = (?)""", (mobile, self.__NRIC))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False

	def updateAccountActive(self, accountActive):
		"""
		Updates account status of the user.
		Returns True if updated successfully
		Returns False if update failed
		"""

		# Update the object's recorded account status"
		self.__accountActive = accountActive

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the account status for the user
		db.execute("""UPDATE user
					  SET accountActive = (?)
					  WHERE NRIC = (?)""", (accountActive, self.__NRIC))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False
	
	# Other Methods
	def verifyLoginDetails(self, NRIC, password):
		""" 
		Verify the login details against retrieved data from database
		Returns True if verified successfully
		Returns False if verification does not match
		"""
		if self.__NRIC == NRIC and self.__password == password:
			return True
		return False

	def verifyPassword(self, password):
		""" 
		Verify the password against retrieved data from database
		Returns True if verified successfully
		Returns False if verification does not match
		"""
		return self.__password == password