

class Particle:
	all = []
	id_next = 0
	def __init__(self, x, y):
		self.id = Particle.id_next
		Particle.id_next += 1
		self.x = x
		self.y = y
		self.prev_x = x
		self.prev_y = y
		Particle.all.append(self)
	
	def getId(self):
		return self.id

	def getXCoor(self):
		return self.x

	def getYCoor(self):
		return self.y

	def getXVelocity(self):
		return self.x - self.prev_x
	
	def getYVelocity(self):
		return self.y - self.prev_y
	
	def getNextXCoor(self):
		return 2*self.x - self.prev_x
	
	def getNextYCoor(self):
		return 2*self.y - self.prev_y
	
	def setXCoor(self, x):
		self.x = x

	def setYCoor(self, y):
		self.y = y

	def moveTo(self, coors):
		self.x = coors[0]
		self.y = coors[1]
	
	def resetPrevCoors(self):
		self.prev_x = self.x
		self.prev_y = self.y

	def getDensity(self):
		return None
	
	def getColour(self):
		return None
	
	def getState(self):
		# 0 = Gas; 1 = Liquid; 2 = Solid
		return None

class Border(Particle):
	all = []
	def __init__(self, x, y):
		super().__init__(x, y)
		Border.all.append(Particle.all.pop()) # Remove border from computation
	
	def getDensity(self):
		return 999999999
	
	def getColour(self):
		return "black"
	
	def getState(self):
		return None

class Sand(Particle):
	def getDensity(self):
		return 20
	
	def getColour(self):
		return "orange"

	def getState(self):
		return 2

class Water(Particle):
	def getDensity(self):
		return 10
	
	def getColour(self):
		return "blue"
	
	def getState(self):
		return 1

class Air(Particle):
	def getDensity(self):
		return 5
	
	def getColour(self):
		return "SkyBlue2"
	
	def getState(self):
		return 0

class Mercury(Particle):
	def getDensity(self):
		return 30
	
	def getColour(self):
		return "silver"
	
	def getState(self):
		return 1