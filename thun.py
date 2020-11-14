import random
import matplotlib.pyplot as plt

run = 0

class card:
	def __init__(self, card, nextTurn = False):
		self.card = card
		self.nextTurn = nextTurn
		
class deck:
	def __init__(self, stoways, drawOne, drawTwo):
		self.turn = 0
		self.hand = []
		self.thunPlayed = 0
		cards = 29
		normalCards = cards - stoways - drawOne - drawTwo
		self.deck = [card(0) for k in range(normalCards)]
		self.drawStartTurn = 0
		for k in range(stoways):
			self.deck.append(card(1))
		for k in range(drawOne):
			if (k < number_Of_Draw_One_CardsImmediatly):
				self.deck.append(card(4))
			else:
				self.deck.append(card(4, True))
		for k in range(drawTwo):
			if (k < number_Of_Draw_Two_CardsImmediatly):
				self.deck.append(card(5))
			else:
				self.deck.append(card(5,True))
		self.start()
		for k in range(4):
			self.deck.append(card(2))
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
	
		global run
		global chancePlayingOtherThanDraw
		
		for k in range(self.drawStartTurn):
			self.drawCard()
		self.drawStartTurn = 0
		
		currentMana = min(self.turn,10)

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
			elif len(drawTwoCards)>0 and currentMana >=3:
				card = drawTwoCards[0]
				self.hand.remove(card)
				if ( not card.nextTurn):
					self.drawCard()
					self.drawCard()
				else:
					self.drawStartTurn +=2
				currentMana -=3
			elif len(drawOneCards)>0 and currentMana >=2:
				card = drawOneCards[0]
				self.hand.remove(card)
				if (not card.nextTurn):	
					self.drawCard()
				else:
					self.drawStartTurn +=1
				currentMana -=2
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
	
def plot(axisXTotal, axisYTotal, labels, cummulative, title, numberIterate, saveName):
	graphWidth = [0.95 for k in range(numberIterate+1)]
	graphAlpha = [1-((0.2*k)) for k in range(numberIterate+1)]
	graphFill = [(lambda k:True if k in range(numberIterate) else False)(k) for k in range(numberIterate+1)]
	graphHatch = [(lambda k: "O" if k in [0] else "")(k) for k in range(numberIterate+1)]
	if (cummulative):
		axisYTotal = [cumulative(k) for k in axisYTotal]
		plt.axhline(y=0.5, color='k', linestyle='-')
	for k in range(len(axisYTotal)):
		plt.bar(axisXTotal[k], axisYTotal[k], label = labels[k], alpha = graphAlpha[k], width = graphWidth[k], fill = graphFill[k], hatch = graphHatch[k])
	plt.xlabel('turn')
	plt.ylabel('percent')
	plt.legend()
	plt.title(title)
	plt.savefig(saveName)
	
def plotWithStowaway(numSim, cummulative, drawOne, drawTwo, stowawayNumber = 2, startNumber = 0):
	axisYTotal = []
	axisXTotal = []
	for stowaway in range(startNumber, startNumber+stowawayNumber + 1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	labels = [("number of stowaways: "+str(k + startNumber)) for k in range(len(axisYTotal))]
	title = "C'Thun turn\n drawOne: %s    drawTwo: %s" % (drawOne, drawTwo)
	saveName = ("Stowaway_D1_" + str(drawOne) +"_D2_" + str(drawTwo)+'.png')
	plot(axisXTotal, axisYTotal, labels, cummulative, title, stowawayNumber, saveName)
	
def plotWithDrawOne(numSim, cummulative, stowaway, drawTwo, drawOneNumber = 2, startNumber = 0):
	axisYTotal = []
	axisXTotal = []
	for drawOne in range(startNumber, startNumber+drawOneNumber + 1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	labels = [("number of drawOne: "+str(k + startNumber)) for k in range(len(axisYTotal))]
	title = "C'Thun turn\n Stowaway: %s    drawTwo: %s" % (stowaway, drawTwo)
	saveName = "DrawOne_S1_" + str(stowaway) +"_D2_" + str(drawTwo)+'.png'
	plot(axisXTotal, axisYTotal, labels, cummulative, title, drawOneNumber, saveName)
	
def plotWithDrawTwo(numSim, cummulative, stowaway, drawOne, drawTwoNumber = 2, startNumber = 0):
	axisYTotal = []
	axisXTotal = []
	for drawTwo in range(startNumber, startNumber+drawTwoNumber + 1):
		temp = simulate(numSim, stowaway, drawOne, drawTwo)
		keys = [k for k in temp.keys()]
		keys.sort()
		axisX = [k for k in keys]
		axisY = [temp[k] for k in axisX]
		axisY = normalize(axisY)
		axisYTotal.append([k for k in axisY])
		axisXTotal.append([k for k in axisX])
	labels = [("number of drawTwo: "+str(k + startNumber)) for k in range(len(axisYTotal))]
	title = "C'Thun turn\n drawOne: %s    Stowaway: %s" % (drawOne, stowaway)
	saveName = "DrawTwo_S1_" + str(stowaway) +"_D1_" + str(drawOne)+'.png'
	plot(axisXTotal, axisYTotal, labels, cummulative, title, drawTwoNumber, saveName)

def SimulateWithParameters(numSim, cummulative, stowaway, drawOne, drawTwo, parameterToIterate, startNumber):
	if parameterToIterate == 0:
		plotWithStowaway(numSim, cummulative, drawOne, drawTwo, stowaway, startNumber)
	elif parameterToIterate == 1:
		plotWithDrawOne(numSim, cummulative, stowaway, drawTwo, drawOne, startNumber)
	elif parameterToIterate == 2:
		plotWithDrawTwo(numSim, cummulative, stowaway, drawOne, drawTwo, startNumber)


number_Of_Draw_One_CardsImmediatly = 4
number_Of_Draw_Two_CardsImmediatly = 2

SimulateWithParameters(10000, False, 2, 2, 4, 1, 4)
