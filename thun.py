import random
import matplotlib.pyplot as plt

run = 0

class card:
	def __init__(self, card):
		self.card = card
		
class deck:
	def __init__(self, stoways, drawOne, drawTwo):
		self.turn = 0
		self.hand = []
		self.thunPlayed = 0
		cards = 29
		normalCards = cards - stoways - drawOne - drawTwo
		self.deck = [card(0) for k in range(normalCards)]
		for k in range(stoways):
			self.deck.append(card(1))
		for k in range(4):
			self.deck.append(card(2))
		for k in range(drawOne):
			self.deck.append(card(4))
		for k in range(drawTwo):
			self.deck.append(card(5))
		self.start()
	
	def start(self):
		for k in range(3):
			self.drawCard()
	
	def shuffleCThun(self):
		self.deck.append(card(3))
	
	def drawCard(self):
		if (len(self.deck) > 0):
			card = random.choice(self.deck)
			self.deck.remove(card)
			self.hand.append(card)
	def playCard(self):
		currentMana = min(self.turn,10)
		global run
		while currentMana >= 2:
			thunCards = [k for k in self.hand if k.card == 2]
			stowaysCards = [k for k in self.hand if k.card == 1]
			cthunCards = [k for k in self.hand if k.card == 3]
			drawOneCards = [k for k in self.hand if k.card == 4]
			drawTwoCards = [k for k in self.hand if k.card == 5]
			### play cthun
			if len(cthunCards) > 0 and currentMana >= 10:
				return(True)
			###Play a thuncard
			elif len(thunCards) > 0 and currentMana >= 5:
				card = thunCards[0]
				self.hand.remove(card)
				self.thunPlayed +=1
				if (self.thunPlayed >= 4):
					self.shuffleCThun()
				currentMana -= 5
			###Play stowaways
			elif len(stowaysCards)>0 and currentMana >=5:
				card = stowaysCards[0]
				self.hand.remove(card)
				thunCardsDeck = [k for k in self.deck if k.card == 2]
				cthunCards = [k for k in self.deck if k.card == 3]
				for k in range(2):
					if len(cthunCards) > 0:
						self.hand.append(cthunCards[0])
						self.deck.remove(cthunCards[0])
						cthunCards.remove(cthunCards[0])
					if len(thunCardsDeck) > 0:
						self.hand.append(thunCardsDeck[0])
						self.deck.remove(thunCardsDeck[0])
						thunCardsDeck.remove(thunCardsDeck[0])
				currentMana -=5
			elif len(drawOneCards)>0 and currentMana >=2:
				card = drawOneCards[0]
				self.hand.remove(card)
				self.drawCard()
				currentMana -=2
			elif len(drawTwoCards)>0 and currentMana >=3:
				card = drawTwoCards[0]
				self.hand.remove(card)
				self.drawCard()
				self.drawCard()
				currentMana -=3
			else:
				return(False)
		return(False)
	def playTurn(self):
		self.turn +=1
		self.drawCard()
		ret = self.playCard()
		return(ret)
			
def simulatePlay(numStone, drawOne, drawTwo):
	simulation = deck(numStone, drawOne, drawTwo)
	temp = False
	while temp == False:
		temp = simulation.playTurn()
	return(simulation.turn)
	
def simulate(numSim, numStone, drawOne, drawTwo):
	turn = {}
	for k in range(32):
		turn[k] = 0
	global run
	run = 0
	while run < numSim:
		run += 1
		endTurn = simulatePlay(numStone, drawOne, drawTwo)
		if endTurn not in turn:
			turn[endTurn] = 0
		turn[endTurn] += 1
	return(turn)
	
def cumulative(list):
	ret = []
	cumSum = 0
	for k in range(len(list)):
		cumSum += list[k]
		ret.append(cumSum)
	return(ret)
	
def normalize(list):
	ret = []
	for k in list:
		ret.append((1.0*k)/sum(list))
	return(ret)

def plotWithStowaway(numSim, cummulative, drawOne, drawTwo, stowawayNumber):
	axisYTotal = []
	axisXTotal = []
	graphWidth = [0.8, 0.8, 0.8]
	graphAlpha = [1, 0.6, 0.4]
	graphFill = [True,True,False]
	graphHatch = ["O","",""]
	for stowaway in range(stowawayNumber+1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		if(cummulative):
			axisY = cumulative(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	for k in range(len(axisYTotal)):
		plt.bar(axisXTotal[k], axisYTotal[k], label = "number of stowaways: "+str(k), alpha = graphAlpha[k], width = graphWidth[k], fill = graphFill[k], hatch = graphHatch[k])
	if (cummulative):
		plt.axhline(y=0.5, color='k', linestyle='-')
	frame1 = plt.gca()
	plt.xlabel('turn')
	plt.ylabel('percent')
	plt.title("C'Thun turn\n drawOne: %s    drawTwo: %s" % (drawOne, drawTwo))
	plt.legend()
	plt.savefig("Stotawaway_D1_" + str(drawOne) +"_D2_" + str(drawTwo)+'.png')
	
def plotWithDrawOne(numSim, cummulative, stowaway, drawTwo, drawOneNumber = 2):
	axisYTotal = []
	axisXTotal = []
	graphWidth = [0.8, 0.8, 0.8]
	graphAlpha = [1, 0.6, 0.4]
	graphFill = [True,True,False]
	graphHatch = ["O","",""]
	for drawOne in range(drawOneNumber+1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		if(cummulative):
			axisY = cumulative(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	for k in range(len(axisYTotal)):
		plt.bar(axisXTotal[k], axisYTotal[k], label = "number of drawOne: "+str(k), alpha = graphAlpha[k], width = graphWidth[k], fill = graphFill[k], hatch = graphHatch[k])
	if (cummulative):
		plt.axhline(y=0.5, color='k', linestyle='-')
	frame1 = plt.gca()
	plt.xlabel('turn')
	plt.ylabel('percent')
	plt.title("C'Thun turn\n Stowaway: %s    drawTwo: %s" % (stowaway, drawTwo))
	plt.legend()
	plt.savefig("DrawOne_S1_" + str(drawOne) +"_D2_" + str(drawTwo)+'.png')
	
def plotWithDrawTwo(numSim, cummulative, stowaway, drawOne, drawTwoNumber = 2):
	axisYTotal = []
	axisXTotal = []
	graphWidth = [0.8, 0.8, 0.8]
	graphAlpha = [1, 0.6, 0.4]
	graphFill = [True,True,False]
	graphHatch = ["O","",""]
	for drawTwo in range(drawTwoNumber + 1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		if(cummulative):
			axisY = cumulative(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	for k in range(len(axisYTotal)):
		plt.bar(axisXTotal[k], axisYTotal[k], label = "number of drawTwo: "+str(k), alpha = graphAlpha[k], width = graphWidth[k], fill = graphFill[k], hatch = graphHatch[k])
	if (cummulative):
		plt.axhline(y=0.5, color='k', linestyle='-')
	frame1 = plt.gca()
	plt.xlabel('turn')
	plt.ylabel('percent')
	plt.title("C'Thun turn\n drawOne: %s    Stowaway: %s" % (stowaway, drawTwo))
	plt.legend()
	plt.savefig("DrawTwo_S1_" + str(drawOne) +"_D1_" + str(drawTwo)+'.png')

def SimulateWithParameters(numSim, cummulative, stowaway, drawOne, drawTwo, parameterToIterate):
	if parameterToIterate == 0:
		plotWithStowaway(numSim, cummulative, drawOne, drawTwo, stowaway)
	elif parameterToIterate == 1:
		plotWithDrawOne(numSim, cummulative, stowaway, drawTwo, drawOne)
	elif parameterToIterate == 2:
		plotWithDrawTwo(numSim, cummulative, stowaway, drawOne, drawTwo)


SimulateWithParameters(100000, True, 2, 2, 2, 0)
