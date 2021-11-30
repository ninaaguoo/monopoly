from cmu_112_graphics import *
import math, random

def playMonopoly():
    (rows, cols, cellSize) = gameDimensions()
    width = cols * cellSize                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    height = rows * cellSize 
    runApp(width = width, height = height)

class Player(object):
    def __init__(self, number):
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.number = number
        self.balance = 1500
        self.properties = []
        self.col = 0
        self.row = 10
        self.color = colors[number]
        self.numHouses = 0
        self.numHotels = 0
        self.cards = []
        self.inJail = False
        self.rr = []
    
    #use method to get positions 
    def getPosition(self):
        return (self.row, self.col)
    
    def getProperties(self):
        return self.properties
    
    def getBalance(self):
        return self.balance
    
    def getColor(self):
        return self.color

    def changeBalance(self, money):
        self.balance += money

    def addProperties(self, prop):
        self.properties.append(prop)

    def isHouseLegal(self):
        colors = {"brown": 2,
                "light blue": 3,
                "magenta": 3,
                "orange": 3,
                "red": 3,
                "green": 3,
                "yellow": 3,
                "blue": 2}

        playerColors = {"brown" : 0,
            "light blue" : 0,
            "magenta": 0,
            "orange": 0,
            "red": 0,
            "green": 0,
            "yellow": 0,
            "blue": 0}

        for prop in self.properties:
            for color in colors:
                if prop.color == color:
                    playerColors[color] += 1
                if playerColors[color] == colors[color]:
                    return (True, color)
        else:
            return (False, None)

    def isHotelLegal(self):
        colors = {"brown": [MEDITERRANEANAVENUE, BALTICAVENUE],
                "light blue": [ORIENTALAVENUE, VERMONTAVENUE, CONNECTICUTAVENUE],
                "magenta": [STCHARLESPLACE, STATESAVENUE, VIRGINIAAVENUE],
                "orange": [STJAMESPLACE, TENNESSEEAVENUE, NEWYORKAVENUE],
                "red": [KENTUCKYAVENUE, INDIANAAVENUE, ILLINOISAVENUE],
                "yellow": [ATLANTICAVENUE, VENTNORAVENUE, MARVINGARDENS],
                "green": [PACIFICAVENUE, NORTHCAROLINAAVENUE, PENNSYLVANIAAVENUE],
                "blue": [PARKPLACE, BOARDWALK]}
        count = 0
        for color in colors:
            for prop in colors[color]:
                if prop.numHouses == 4:
                    count += 1
            if count == len(colors[color]):
                return (True, color)
        return (False, None)
    
    def assets(self):
        result = 0
        for prop in self.properties:
            if prop.numHouses > 0:
                result += (50 * prop.numHouses)
            if prop.numHotels > 0:
                result += (100 % prop.numHotels)
            if prop.isMortgage == True:
                result += (0.5 * prop.price)
            elif prop.isMortgage == False:
                result += prop.price
        for rr in self.rr:
            if rr.isMortgage == True:
                result += (0.5 * rr.price)
            elif rr.isMortgage == False:
                result += rr.price
        return result + self.balance
    
    def movePosition(self, row, col):
        self.row = row
        self.col = col

    def move(self, num):
        for i in range(num):
            if self.col == 0:                     
                if self.row == 0:
                    self.col += 1
                else:
                    self.row -= 1
            elif self.row == 0:
                if self.col == 10:
                    self.row += 1
                else:
                    self.col += 1
            elif self.col == 10:
                if self.row == 10:
                    self.col -= 1
                else:
                    self.row += 1
            elif self.row == 10:
                if self.col == 0:
                    self.row -= 1
                else:
                    self.col -= 1
        return (self.row, self.col)

    def ifPassedGo(self, num):
        currRow = self.row
        currCol = self.col
        for i in range(num):
            if currCol == 0:                     
                if currRow == 0:
                    currCol += 1
                    self.onGo(currRow, currCol)
                else:
                    currRow -= 1
                    self.onGo(currRow, currCol)
            elif currRow == 0:
                if currCol == 10:
                    currRow += 1
                    self.onGo(currRow, currCol)
                else:
                    currCol += 1
                    self.onGo(currRow, currCol)
            elif currCol == 10:
                if currRow == 10:
                    currCol -= 1
                    self.onGo(currRow, currCol)
                else:
                    currRow += 1
                    self.onGo(currRow, currCol)
            elif currRow == 10:
                if currCol == 0:
                    currRow -= 1
                    self.onGo(currRow, currCol)
                else:
                    currCol -= 1
                    self.onGo(currRow, currCol)
    
    def onGo(self, currRow, currCol):
        if currRow == 10 and currCol == 0:
            self.changeBalance(200)
        else: 
            pass

class Property(object):
    def __init__(self, name, price, baseRent, row, col, color,
                houseHotelPrice, oneRent, twoRent, threeRent, fourRent, 
                hotelRent, mortgage, isUtility = False, isRail = False):   
        self.name = name
        self.price = price
        self.baseRent = baseRent
        self.row = row
        self.col = col
        self.numHouses = 0
        self.numHotels = 0
        self.color = color
        self.owner = None
        self.isMortgage = False
        self.oneRent = oneRent
        self.twoRent = twoRent
        self.threeRent = threeRent
        self.fourRent = fourRent
        self.hotelRent = hotelRent
        self.isMortgage = False

        if isUtility == True:
            self.isUtility = True

        if isRail == True:
            self.isRail = True

    def getPrice(self):
        return self.price

    def getOwner(self):
        return self.owner

    def getBaseRent(self):
        return self.baseRent

    def changeOwner(self, newOwner):
        self.owner = newOwner
    
    def getColorPriceAndName(self):
        return (self.color, self.price, self.name)

    def getLocation(self):
        return (self.row, self.col)
    
    def rentForOneHouse(self):
        self.baseRent = self.oneRent

    def rentForTwoHouses(self):
        self.baseRent = self.twoRent

    def rentForThreeHouses(self):
        self.baseRent = self.threeRent

    def rentForFourHouses(self):
        self.baseRent = self.fourRent

    def rentForHotel(self):
        self.baseRent = self.hotelRent

MEDITERRANEANAVENUE = Property("MEDITERRANEAN AVENUE", 60, 2, 9, 0, "brown", 50, 10, 30, 90, 160, 250, 30)
BALTICAVENUE = Property("BALTIC AVENUE", 60, 8, 7, 0, "brown", 50, 20, 60, 180, 320, 450, 30)
ORIENTALAVENUE = Property("ORIENTAL AVENUE", 100, 6, 4, 0, "light blue", 50, 30, 90, 270, 400, 550, 50)
VERMONTAVENUE = Property("VERMONT AVENUE", 100, 6, 2, 0, "light blue", 50, 30, 90, 270, 400, 550, 50)
CONNECTICUTAVENUE = Property("CONNECTICUT AVENUE", 120, 8, 1, 0, "light blue", 50, 40, 100, 300, 450, 600, 60)
STCHARLESPLACE = Property("ST CHARLES PLACE", 140, 10, 0, 1, "magenta", 100, 50, 150, 450, 625, 750, 70)
STATESAVENUE = Property("STATES AVENUE", 140, 10, 0, 3, "magenta", 100, 50, 150, 450, 625, 750, 70)
VIRGINIAAVENUE = Property("VIRGINIA AVENUE", 160, 12, 0, 4, "magenta", 100, 60, 180, 500, 700, 900, 80)
STJAMESPLACE = Property("ST JAMES PLACE", 180, 14, 0, 6, "orange", 100, 70, 200, 550, 750, 950, 90)
TENNESSEEAVENUE = Property("TENNESSEE AVENUE", 180, 14, 0, 8, "orange", 100, 70, 200, 550, 750, 950, 90)
NEWYORKAVENUE = Property("NEW YORK AVENUE", 200, 16, 0, 9, "orange", 100, 80, 220, 600, 800, 1000, 100)
KENTUCKYAVENUE = Property("KENTUCKY AVENUE", 220, 18, 1, 10, "red", 150, 90, 250, 700, 875, 1050, 110)
INDIANAAVENUE = Property("INDIANA AVENUE", 220, 18, 3, 10, "red", 150, 90, 250, 700, 875, 1050, 110)
ILLINOISAVENUE = Property("ILLINOIS AVENUE", 240, 20, 4, 10, "red", 150, 100, 300, 750, 925, 1150, 120)
ATLANTICAVENUE = Property("ATLANTIC AVENUE", 260, 22, 6, 10, "yellow", 150, 110, 330, 800, 975, 1150, 130)
VENTNORAVENUE = Property("VENTNOR AVENUE", 260, 22, 7, 10, "yellow", 150, 110, 330, 800, 975, 1150, 130)
MARVINGARDENS = Property("MARVIN GARDENS", 280, 24, 9, 10, "yellow", 150, 120, 360, 850, 1025, 1200, 140)
PACIFICAVENUE = Property("PACIFIC AVENUE", 300, 26, 10, 9, "green", 200, 130, 390, 900, 1100, 1275, 150)
NORTHCAROLINAAVENUE = Property("NORTH CAROLINA AVENUE", 300, 26, 10, 8, "green", 200, 130, 390, 900, 1100, 1275, 150)
PENNSYLVANIAAVENUE = Property("PENNSYLVANIA AVENUE", 320, 28, 10, 6, "green", 200, 150, 450, 1000, 1200, 1400, 160)
PARKPLACE = Property("PARK PLACE", 350, 35, 10, 3, "blue", 200, 175, 500, 1100, 1300, 1500, 175)
BOARDWALK = Property("BOARDWALK", 400, 50, 10, 1, "blue", 200, 200, 600, 1400, 1700, 2000, 200)

class Tile(object):
    def __init__(self, name, isChance, isCC, isGo, isJail, isFreeParking, row, col):
        self.isChance = isChance
        self.isCC = isCC
        self.isGo = isGo
        self.isJail = isJail
        self.isFreeParking = isFreeParking
        self.row = row
        self.col = col
    
    def getLocation(self):
        return (self.row, self.col)

GO = Tile("GO", False, False, True, False, False, 10, 0)
COMMUNITYCHEST1 = Tile("COMMUNITY CHEST", False, True, False, False, False, 8, 0)
INCOMETAX = Tile("INCOME TAX", False, False, False, False, False, 6, 0)
CHANCE1 = Tile("CHANCE", True, False, False, False, False, 3, 0)
COMMUNITYCHEST2 = Tile("COMMUNITY CHEST", False, True, False, False, False, 0, 7)
FREEPARKING = Tile("FREE PARKING", False, False, False, False, True, 0, 10)
CHANCE2 = Tile("CHANCE", True, False, False, False, False, 2, 10)
GOTOJAIL = Tile("GO TO JAIL", False, False, False, True, False, 10, 10)
COMMUNITYCHEST3 = Tile("COMMUNITY CHEST", False, True, False, False, False, 10, 7)
CHANCE3 = Tile("CHANCE", True, False, False, False, False, 10, 4)
LUXURYTAX = Tile("LUXURY TAX", False, False, False, False, False, 8, 10)

class Railroad(object):
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        self.price = 200
        self.mortgage = 100
        self.isMortgage = False
        self.owner = None
        

    def changeBaseRent(self, num):
        if num == 2:
            self.baseRent = 50
        elif num == 3:
            self.baseRent = 100
        elif num == 4:
            self.baseRent = 200
    
    def getLocation(self):
        return self.row, self.col
    
    def changeOwner(self, owner):
        self.owner = owner
  
READINGRAILROAD = Railroad("READING RAILROAD", 5, 0)
PENNSYLVANIARAILROAD = Railroad("PENNSYLVANIA RAILROAD", 0, 5)
BANDORAILROAD = Railroad("B&O RAILROAD", 5, 10)
SHORTLINE = Railroad("SHORT LINE", 10, 5)

def gameDimensions():
    rows = 11
    cols = 11
    cellSize = 70
    return (rows, cols, cellSize)

def appStarted(app):
    app.tiles = [GO, COMMUNITYCHEST1, INCOMETAX, CHANCE1, COMMUNITYCHEST2, FREEPARKING,
                CHANCE2, GOTOJAIL, COMMUNITYCHEST3, CHANCE3, LUXURYTAX]
    (rows, cols, cellSize) = gameDimensions()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.width = app.cols * app.cellSize 
    app.height = app.rows * app.cellSize 
    app.dice1 = -1
    app.dice2 = -1
    app.dicetotal = app.dice1 + app.dice2
    app.hasDiceRolled = False
    app.askPlayerAboutOwnedPropertyMode = False
    app.askPlayerAboutUnownedPropertyMode = False
    app.playerCanNowBuyHouses = False
    app.isProperty = False
    app.yourOwnProperty = False
    app.isTile = False
    app.isRR = False
    app.buyingHouses = False
    app.winner = None
    app.doesPlayerWantToStopBuyingHouses = False
    app.deleted = []
    app.name = ''  #number of players input
    app.numHouses = ''
    app.screen = "startScreen" #entire screen
    app.players = []
    app.display = "disappear" #message screen
    app.info = "disappear" #stats screen
    app.propertyCheckMode = False  #if it is or isnt a property
    app.askPlayerAboutOwnedPropertyMode = False  #what to do when on someone else's property
    app.askPlayerAboutUnownedPropertyMode = False   #what to do when on nobody's property
    app.playerCanNowBuyHotels = False
    app.askPlayerAboutMortgage = False
    app.askHowManyHouses = False
    app.askAboutLuxuryTax = False
    app.askAboutIncomeTax = False
    app.askPlayerAboutUnownedRR = False
    app.askPlayerAboutOwnedRR = False
    app.properties = [KENTUCKYAVENUE, INDIANAAVENUE, ILLINOISAVENUE,
    ATLANTICAVENUE, VENTNORAVENUE, MARVINGARDENS, PACIFICAVENUE, 
    NORTHCAROLINAAVENUE, PENNSYLVANIAAVENUE, PARKPLACE, 
    BOARDWALK, MEDITERRANEANAVENUE, BALTICAVENUE, ORIENTALAVENUE,
    VERMONTAVENUE, CONNECTICUTAVENUE, STCHARLESPLACE,
    STATESAVENUE, VIRGINIAAVENUE, STJAMESPLACE, TENNESSEEAVENUE, NEWYORKAVENUE]
    app.turn = 0
    app.message = ""
    app.numHousesInt = 0
    app.rrs = []
    app.chance = ["ADVANCE TO GO", "Advance to Illinois Ave.", "Advance to St. Charles Place.", 
                    "Bank pays you dividend of $50.",
    "Get out of Jail Free.", "Go to Jail.", "Make general repairs on all your property: For each house pay $25, For each hotel pay $100.",
    "Pay poor tax of $15", "Take a trip to Reading Railroad.", "Take a walk on the Boardwalk.", "You have been elected Chairman of the Board. Pay each player $50.",
    "Your building and loan matures. Receive $150.", "You have won a crossword competition. Collect $100."]
    app.cc = ["Advance to Go.", "Bank error in your favor. Collect $200.",
                "Doctor's fees. Pay $50.", "From sale of stock you get $50.",
                "Get Out of Jail Free.", "Go to Jail.",
                "Grand Opera Night. Collect $50 from every player for opening night seats.", 
                "Holiday Fund matures. Receive $100.",
                "Income tax refund. Collect $20.",
                "It is {It's} your birthday. Collect $10 from every player.",
                "Life insurance matures – Collect $100.", "Hospital Fees. Pay $50.",
                "School fees. Pay $50.", "Receive $25 consultancy fee.",
                "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
                "You have won second prize in a beauty contest. Collect $10.",
                "You inherit $100."]    
    
def keyPressed(app, event):
    if event.key.isdigit() and app.screen == "userNumber":
        if len(event.key) == 1 and 0 < int(event.key) <= 6:
            app.name += event.key
        return
    elif event.key.isdigit() and app.askHowManyHouses == True:
        if len(event.key) == 1:
            app.numHouses += event.key
    elif event.key == "Delete" and len(app.name) >= 1 and app.screen == "userNumber":
        app.name = app.name[:-1]
    elif event.key == "Delete" and len(app.numHouses) >= 1 and app.askHowManyHouses == True:
        app.numHouses = app.numHouses[:-1]
                
    elif event.key == "Space" and app.screen == "board":
        diceRoll(app)
        #if property:
            #change display state
            #in check property state
            #check condition for draw depending on display state
            #
    else:
        return

def checkWinner(app):
    remaining = []
    curr = 0
    currPlayer = ""
    best = -1
    for player in app.players:
        if player not in app.deleted:
            remaining.append(player)
    print(remaining)
    for player in remaining:
        currPlayer = player
        curr = player.assets()
        if curr > best:
            app.winner = currPlayer.number
            best = curr
    print(app.winner)
    

def mousePressed(app, event):
    while app.turn in app.deleted:
        if (int(app.name) - len(app.deleted)) == int(app.name) - 1:
            checkWinner(app)
        else:
            app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
        
    #clicking start to get to number of user input screen
    if (app.width//2 - 30 < event.x < app.width//2 + 30 and 
        app.height * 3//5 - 30 < event.y < app.height * 3//5 + 30):
        app.screen = "userNumber"
    (x2, y2, x3, y3) = getCellBounds(app, 1, 9)

    #toggle between showing stats and not showing stats
    if x3 - 15 < event.x < x3 - 5 and y2 + 5 < event.y < y2 + 15 and app.info == "disappear" and app.screen == "board":
        app.info = "appear"
    elif x3 - 15 < event.x < x3 - 5 and y2 + 5 < event.y < y2 + 15 and app.info == "appear" and app.screen == "board":
        app.info = "disappear"
    (x0, y0, x1, y1) = getCellBounds(app, 5, 5) #dice location on board

    #clicking next to get to board screen
    if (app.screen == "userNumber" and app.width * 3//5 - 10 < event.x 
            < app.width *3//5 + 10 and app.height*3.01/5 - 10 < event.y 
            < app.height *3.01/5 + 10):
        app.screen = "board"
        createPlayers(app)  #create player instances
    
    #buying houses
    if app.playerCanNowBuyHouses == True:
        (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
        if (x0 - 60 < event.x < x0 - 40 and y0 + 40 < event.y < y0 + 60) and app.isProperty == True: #click yes
            app.doesPlayerWantToStopBuyingHouses = True
            app.buyingHouses = True
        elif (x0 + 110 < event.x < x0 + 130 and y0 + 40 < event.y < y0 + 60) and app.isProperty == True: #click no
            app.display = "disappear"
            app.turn = (app.turn + 1) % int(app.name)

    if app.buyingHouses == True:
        (boolean, color) = app.players[app.turn].isHouseLegal()
        for prop in app.players[app.turn].properties:
            if prop.color == color:
                (row, col) = prop.row, prop.col
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                if x0 < event.x < x1 and y0 < event.y < y1: #clicking on that property
                    if prop.numHouses < 4:
                        prop.numHouses += 1
                        if prop.numHouses == 1:
                            prop.rentForOneHouse()
                        elif prop.numHouses == 2:
                            prop.rentForTwoHouses()
                        elif prop.numHouses == 3:
                            prop.rentForThreeHouses()
                        elif prop.numHouses == 4:
                            prop.rentForFourHouses()
                        app.players[app.turn].numHouses += 1
                        app.players[app.turn].changeBalance(-50) #draw properties
                        ifPlayerBankrupt(app)

    if app.doesPlayerWantToStopBuyingHouses == True:
        (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
        if app.width//2 - 10 < event.x < app.width//2 + 10 and y0 + 40 < event.y < y0 + 60: #DONE
            app.playerCanNowBuyHouses = False
            app.buyingHouses = False
            app.turn = (app.turn + 1) % int(app.name)

    #if can buy hotels
    if app.playerCanNowBuyHotels == True:
        (boolean, color) = app.players[app.turn].isHotelLegal()
        for prop in app.players[app.turn].properties:
            if prop.color == color:
                (row, col) = prop.row, prop.col
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                if x0 < event.x < x1 and y0 < event.y < y1: #click property to buy hotels
                    if prop.numHotels == 0:
                        prop.numHotels += 1
                        if prop.numHotels == 1:
                            prop.rentForHotel()
                        app.players[app.turn].numHotels += 1
                        prop.numHouses -= 4 #lose houses to get hotel
                        app.players[app.turn].numHouses -= 4
                        app.players[app.turn].changeBalance(-50)

    #no i will not buy houses
    if app.playerCanNowBuyHouses == True and x0 + 110 < event.x < x0 + 130 and y0 + 40 < event.y < y0 + 60:
        app.playerCanNowBuyHouses = False

    #landed on unowned property  
    if app.askPlayerAboutUnownedPropertyMode == True: #if it's an unowned property do u want to buy
        (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if (x1 + 90 < event.x < x1 + 110 and y2 + 20 < event.y < y1 + 40) and app.isProperty == True: #click yes
            (boolean, prop) = isProperty(app)
            price = prop.price
            app.players[app.turn].changeBalance(-price)
            ifPlayerBankrupt(app)
            if app.turn in app.deleted: pass
            else:
                prop.changeOwner(app.players[app.turn].number)
                app.players[app.turn].addProperties(prop)
                (boolean2, color) = app.players[app.turn].isHouseLegal()
                if boolean2 == True:
                    app.playerCanNowBuyHouses = True
                    app.boom = f'player {app.turn} can buy houses! do you want to buy a house for {color} properties?'
                (boolean3, color) = app.players[app.turn].isHotelLegal()
                if boolean3 == True:
                    app.playerCanNowBuyHotels = True
                    app.boom = f'player {app.turn} can buy hotels! do you want to buy a hotel for {color} properties?'
                    #if yes:
                        #pick which ones
                app.display = "disappear"
                app.turn = (app.turn + 1) % int(app.name)
        elif (x2 - 110 < event.x < x2 - 90 and y2 + 20 < event.y < y2 + 40) and app.isProperty == True: #no
            app.display = "disappear"
            app.turn = (app.turn + 1) % int(app.name)
        app.askPlayerAboutOwnedPropertyMode = False

    #landed on owned property
    elif app.askPlayerAboutOwnedPropertyMode == True: #if property already has an owner
        (boolean, prop) = isProperty(app)
        price = prop.price
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if app.width//2 - 10 < event.x < app.width//2 + 10 and y2 + 10 < event.y < y2 + 30 and prop.isMortgage == False: #OK
                app.players[app.turn].changeBalance(-price)
                ifPlayerBankrupt(app)
                app.players[prop.owner].changeBalance(price)
                if app.players[app.turn].getBalance() < 0: #go into debt after buying property
                    app.boom = f'You do not have enough money to pay for {prop.name}. You can mortgage a property.'
                    app.askPlayerAboutMortgage = True
                else: #not in debt after buying property
                    app.display = "disappear"
        app.turn = (app.turn + 1)%int(app.name)
    
    elif app.yourOwnProperty == True:
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        (boolean, prop) = isProperty(app)
        if app.width//2 - 10 < event.x < app.width//2 + 10 and y2 + 10 < event.y < y2 + 30: #OK
            app.display = "disappear"

    #mortgage time
    elif app.askPlayerAboutMortgage == True: #if player wants to mortgage property
        for prop in app.players[app.turn].properties:
            if prop.numHouses == 0: #unimproved property
                (x0, y0, x1, y1) = getCellBounds(app, prop.row, prop.col)
                if x0 < event.x < x1 and y0 < event.y < y1: #click on property
                    app.players[app.turn].changeBalance(prop.mortgage)
                    prop.isMortgage = True
            else: #improved property
                app.message  = "You have to sell houses/hotels before mortgaging."
                for i in range(len(prop.numHouses)):
                    app.players[app.turn].numHouses -= 1
                    prop.numHouses -= 1
                    app.players[app.turn].changeBalance(25)
                app.players[app.turn].changeBalance(prop.mortgage)
                prop.isMortgage = True
        app.turn = (app.turn + 1)%int(app.name)

    
#########TILES#####################################################################
    
    #landed on income tax
    if app.askAboutIncomeTax == True:
        while app.turn in app.deleted:
            if (int(app.name) - len(app.deleted)) == int(app.name) - 1:
                checkWinner(app)
            else:
                app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
        app.message = "You must pay income tax. You can either pay $200 (yes) or 10 percent of your total assets (no).", "You have ten seconds to decide."
        (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if (x1 + 90 < event.x < x1 + 110 and y2 + 20 < event.y < y1 + 40): #click yes
            app.players[app.turn].changeBalance(-200)
            ifPlayerBankrupt(app)
    (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
    if app.width//2 - 10 < event.x < app.width//2 + 10 and y2 + 10 < event.y < y2 + 30 and app.isTile == True:
            app.turn = (app.turn + 1) % int(app.name)
            app.display = "disappear"
            app.isTile = False

    #landed on luxury tax
    elif app.askAboutLuxuryTax == True:
        app.isTile = True
        app.display = "appear"
        app.message = "You must pay luxury tax of $75 to the bank."
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if app.width//2 - 10 < event.x < app.width//2 + 10 and y2 + 10 < event.y < y2 + 30 and app.isTile == True: #OK
            app.display = "disapppear"
            app.players[app.turn].changeBalance(-75) 
            ifPlayerBankrupt(app)
            app.askAboutLuxuryTax = False
        app.turn = (app.turn + 1) % int(app.name)

########RAILROADS##################################################################

    if app.askPlayerAboutUnownedRR == True:
        (boolean, rr) = isRR(app)
        app.display = "appear"
        app.message = f'You have landed on an unowned railroad. Would you like to buy {rr.name} for ${rr.price}.'
        (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if (x1 + 90 < event.x < x1 + 110 and y2 + 20 < event.y < y1 + 40) and app.isRR == True: #yes
            app.players[app.turn].railroads.append(rr)
            app.players[app.turn].changeBalance(-rr.price)
            ifPlayerBankrupt(app)
            rr.changeBaseRent(len(app.players[app.turn].railroads))
            rr.changeOwner(app.turn)
        elif (x2 - 110 < event.x < x2 - 90 and y2 + 20 < event.y < y2 + 40) and app.isRR == True: #no
            app.display = "disappear"
        app.turn = (app.turn + 1) % int(app.name)
    
    if app.askPlayerAboutOwnedRR == True:
        (boolean, rr) = isRR(app)
        app.display = "appear"
        app.message = f"You have landed on player {rr.owner}'s railroad. You have to pay them ${rr.rent}."
        (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
        if app.width//2 - 10 < event.x < app.width//2 + 10 and y2 + 10 < event.y < y2 + 30 and app.isRR == True: #OK
            app.players[app.turn].changeBalance(-rr.rent)
            ifPlayerBankrupt(app)
            app.players[rr.owner].changeBalance(rr.rent)
        app.turn = (app.turn + 1)%int(app.name)

def isProperty(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    for prop in app.properties:
        rowprop, colprop = prop.getLocation()
        rowplay = app.players[app.turn].row
        colplay = app.players[app.turn].col
        if rowplay == rowprop and colplay == colprop: 
            app.isProperty = True
            app.isTile = False
            app.isRR = False
            return True, prop
    return False, None

def isTile(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    for tile in app.tiles:
        rowtile, coltile = tile.getLocation()
        rowplay, colplay = app.players[app.turn].row, app.players[app.turn].col
        if rowplay == rowtile and colplay == coltile:
            app.isTile = True
            app.isProperty = False
            app.isRR = False
            return True, tile
    return False, None

def isRR(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    for rr in app.rrs:
        rowrr, colrr = rr.getLocation()
        rowplay, colplay = app.players[app.turn].row, app.players[app.turn].col
        if rowplay == rowrr and colplay == colrr:
            app.isRR = True
            app.isTile = False
            app.isProperty = False
            return True, rr
    return False, None

def diceRoll(app):
    while app.turn in app.deleted:
        if (int(app.name) - len(app.deleted)) == int(app.name) - 1:
            checkWinner(app)
        else:
            app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    if app.players[app.turn].inJail == True:
        app.dice1 = random.randint(1, 6)
        app.dice2 = random.randint(1, 6)
        app.dicetotal = app.dice1 + app.dice2
        if app.dice1 == app.dice2:
            app.players[app.turn].move(app.dicetotal)
            app.players[app.turn].inJail = False
        elif "Get out of Jail Free." in app.players[app.turn].cards:
            app.players[app.turn].move(app.dicetotal)
            app.players[app.turn].inJail = False
        #elif paying a fine on either of next two turns:
            #move
    elif app.display == "disappear" and app.players[app.turn].inJail == False:
        app.hasDiceRolled = True
        app.dice1 = random.randint(1, 6)
        app.dice2 = random.randint(1, 6)
        app.dicetotal = app.dice1 + app.dice2
        if app.dice1 == app.dice2:
            app.dicetotal += 1
        app.players[app.turn].ifPassedGo(app.dicetotal)
        app.players[app.turn].move(app.dicetotal)
        app.propertyCheckMode = True
        (boolean, prop) = isProperty(app)
        if boolean == True: #player is on property
            app.display = "appear"
            price = prop.getPrice()
            owner = prop.getOwner()
            name = prop.name
            if owner == None: #no one owns property
                app.message = f'hi player {app.turn}, {name} is an unowned property would u like to buy it for ${price}?'
                app.askPlayerAboutUnownedPropertyMode = True
                app.askPlayerAboutOwnedPropertyMode = False
                app.yourOwnProperty = False
            elif owner != app.turn: #property is owned by someone
                app.askPlayerAboutOwnedPropertyMode = True
                app.askPlayerAboutUnownedPropertyMode = False
                app.yourOwnProperty = False
                rent = prop.getBaseRent()
                app.message = f'this is a property owned by player {owner}. You have to pay player {owner} ${rent}.'
                if app.players[app.turn].getBalance() >= rent: #has enough money to pay rent
                    ifPlayerBankrupt(app)
                    app.players[app.turn].changeBalance(-rent)
                    app.players[owner].changeBalance(+rent)
            elif owner == app.turn: 
                app.askPlayerAboutOwnedPropertyMode = False
                app.askPlayerAboutUnownedPropertyMode = False
                app.yourOwnProperty = True
                app.message = f'this is your own property'
        else: #not a property but a tile
            (boolean2, tile) = isTile(app)
            if boolean2 == True: #it's a tile!
                app.display = "appear"
                if tile == GO:
                    app.players[app.turn].changeBalance(200)
                    app.message = f'You have landed on GO.'
                elif tile == COMMUNITYCHEST1 or tile == COMMUNITYCHEST2 or tile == COMMUNITYCHEST3:
                    message = communityChest(app)
                    app.message = f'You have landed on a community chest tile! {message}'
                elif tile == CHANCE1 or tile == CHANCE2 or tile == CHANCE3:
                    message = chance(app)
                    app.message = f'You have landed on a chance tile! {message}'
                elif tile == GOTOJAIL:
                    if "Get out of Jail Free." in app.players[app.turn].cards:
                        app.message = "You do not need to go to jail."
                        pass
                    else:
                        app.message = "You are going to jail!"
                        app.players[app.turn].movePosition(0, 0)
                        app.players[app.turn].inJail = True
                    #stay there until pay fee
                elif tile == FREEPARKING:
                    app.message = "You are on free parking. Nothing happens."
                elif tile == INCOMETAX:
                    app.message = "You have landed on income tax."
                    app.incomeTaxTimer = "start"
                    app.askAboutIncomeTax = True
                elif tile == LUXURYTAX:
                    app.message = "You have landed on luxury tax."
                    app.askAboutLuxuryTax = True
            else: #it's a rr
                (boolean, rr) = isRR(app)
                if boolean == True:
                    app.display = "appear"
                    price = rr.price
                    owner = rr.owner
                    if owner == None: #no one owns rr
                        app.message = f'hi player {app.turn}, {name} is an unowned railroad would u like to buy it for ${price}?'
                        app.askPlayerAboutUnownedRRMode = True
                    elif owner == app.turn: 
                        app.message = "this is your own railroad."
                        pass #this is my rr
                    elif owner != app.turn: #property is owned by someone
                        app.askPlayerAboutOwnedRRMode = True
                        app.askPlayerAboutUnownedRRMode = False
                        rent = rr.getBaseRent()
                        app.message = f'this is a railroad owned by player {owner}. You have to pay player {owner} ${rent}.'
                        if app.players[app.turn].getBalance() >= rent: #has enough money to pay rent
                            ifPlayerBankrupt(app)
                            app.players[app.turn].changeBalance(-rent)
                            app.players[owner].changeBalance(+rent)
                        else:
                            pass
                            #mortage
                        

def ifPlayerBankrupt(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    if app.players[app.turn].balance < 0:
        for prop in app.players[app.turn].properties:
            prop.changeOwner(None)
        app.deleted.append(app.turn)
        app.players.pop(app.turn)
        checkWinner(app)
        return True
    return False
        
def communityChest(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    i = random.randint(0, len(app.cc) - 1)
    stuff = app.cc[i]
    if stuff == "Advance to Go.":
        app.players[app.turn].movePosition(10, 0)
        app.players[app.turn].changeBalance(200)
    elif stuff == "Bank error in your favor. Collect $200.":
        app.players[app.turn].changeBalance(200)
    elif stuff == "From sale of stock you get $50.":
         app.players[app.turn].changeBalance(50)
    elif stuff == "Get Out of Jail Free.":
        app.players[app.turn].cards.append(stuff)
    elif stuff == "Go to Jail.":
        if "Get out of Jail Free." in app.players[app.turn].cards:
            pass
        else:
            app.players[app.turn].movePosition(0, 0)
            app.players[app.turn].inJail = True
    elif stuff == "Grand Opera Night. Collect $50 from every player for opening night seats.":
        for player in app.players:
            if player != app.players[app.turn]:
                player.changeBalance(-50)
                ifPlayerBankrupt(app)
        app.players[app.turn].changeBalance(50 * (len(app.players) - 1))
    elif stuff == "Holiday Fund matures. Receive $100.":
        app.players[app.turn].changeBalance(100)
    elif stuff == "Income tax refund. Collect $20.":
        app.players[app.turn].changeBalance(20)
    elif stuff == "It is your birthday. Collect $10 from every player.":
        for player in app.players:
            if player != app.players[app.turn]:
                player.changeBalance(-10)
                ifPlayerBankrupt(app)
        app.players[app.turn].changeBalance(10 * (len(app.players) - 1))
    elif stuff == "Life insurance matures – Collect $100.":
        app.players[app.turn].changeBalance(100)
    elif stuff == "Hospital Fees. Pay $50.":
        app.players[app.turn].changeBalance(-50)
        ifPlayerBankrupt(app)
    elif stuff == "School fees. Pay $50.":
        app.players[app.turn].changeBalance(-50)
        ifPlayerBankrupt(app)
    elif stuff == "Receive $25 consultancy fee.":
        app.players[app.turn].changeBalance(25)
    elif stuff == "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.":
        if app.players[app.turn].numHouses > 0:
            for house in app.players[app.turn].numHouses:
                app.players[app.turn].changeBalance(-40)
                ifPlayerBankrupt(app)
        else:
            pass
        if app.players[app.turn].numHotels > 0:
            for hotel in app.players[app.turn].numHotels:
                app.players[app.turn].changeBalance(-115)
                ifPlayerBankrupt(app)
        else:
            pass
    elif stuff == "You have won second prize in a beauty contest. Collect $10.":
         app.players[app.turn].changeBalance(-10)
         ifPlayerBankrupt(app)
    elif stuff == "You inherit $100.":
        app.players[app.turn].changeBalance(100)
    return stuff

def chance(app):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    i = random.randint(0, len(app.chance) - 1)
    stuff = app.chance[i]
    if stuff == "ADVANCE TO GO":
        app.players[app.turn].movePosition(10, 0)
        app.players[app.turn].changeBalance(200)
    elif stuff == "Advance to Illinois Ave.":
        ifPassedGo(app, app.players[app.turn].row, app.players[app.turn].col, 4, 10)
        app.players[app.turn].movePosition(4, 10)
    elif stuff == "Advance to St. Charles Place.":
        ifPassedGo(app, app.players[app.turn].row, app.players[app.turn].col, 0, 1)
        app.players[app.turn].movePosition(0, 1)
    elif stuff == "Bank pays you dividend of $50.":
        app.players[app.turn].changeBalance(50)
    elif stuff == "Get out of Jail Free.":
        #keep in deck may use later
        app.players[app.turn].cards.append(stuff)
    elif stuff == "Go To Jail.":
        if "Get out of Jail Free." in app.players[app.turn.cards]:
            pass
        else:
            app.players[app.turn].movePosition(0, 0)
            app.players[app.turn].inJail = True
    elif stuff == "Make general repairs on all your property: For each house pay $25, For each hotel pay $100.":
        for i in range(app.players[app.turn].numHouses):
            app.players[app.turn].changeBalance(-25)
            ifPlayerBankrupt(app)
        for j in range(app.players[app.turn].numHotels):
            app.players[app.turn].changeBalance(-100)
            ifPlayerBankrupt(app)
    elif stuff == "Pay poor tax of $15": 
        app.players[app.turn].changeBalance(-15)
        ifPlayerBankrupt(app)
    elif stuff == "Take a trip to Reading Railroad.":
        ifPassedGo(app, app.players[app.turn].row, app.players[app.turn].col, 5, 0)
        app.players[app.turn].movePosition(5, 0)
    elif stuff == "Take a walk on the Boardwalk.":
        ifPassedGo(app, app.players[app.turn].row, app.players[app.turn].col, 10, 1)
        app.players[app.turn].movePosition(10, 1)
    elif stuff == "You have been elected Chairman of the Board. Pay each player $50.":
        app.players[app.turn].changeBalance(-(50 * len(app.players) - 1))
        ifPlayerBankrupt(app)
        for player in app.players:
            if player != app.players[app.turn]:
                player.changeBalance(50)
    elif stuff == "Your building and loan matures. Collect $150.":
        app.players[app.turn].changeBalance(150)
    elif stuff == "You have won a crossword competition. Collect $100.":
        app.players[app.turn].changeBalance(100)
    return stuff

def ifPassedGo(app, startRow, startCol, finalRow, finalCol):
    while app.turn in app.deleted:
        app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    currRow = startRow
    currCol = startCol
    while currRow != finalRow and currCol != finalCol:
        if currCol == 0:                     
            if currRow == 0:
                currCol += 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
            else:
                currRow -= 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
        elif currRow == 0:
            if currCol == 10:
                currRow += 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
            else:
                currCol += 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
        elif currCol == 10:
            if currRow == 10:
                currCol -= 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
            else:
                currRow += 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
        elif currRow == 10:
            if currCol == 0:
                currRow -= 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)
            else:
                currCol -= 1
                if onGo(currRow, currCol):
                    app.players[app.turn].changeBalance(200)

def onGo(currRow, currCol):
    if currRow == GO.row and currCol == GO.col:
        return True
    else:
        return False

def createPlayers(app):
    for i in range(int(app.name)):
        app.players.append(Player(i))

#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width 
    gridHeight = app.height
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

def redrawAll(app, canvas):
    if app.winner != None:
        drawWinner(app, canvas)
    if app.winner == None:
        if app.screen == "startScreen":
            drawStartScreen(app, canvas)
        if app.screen == "userNumber":
            drawUserNumber(app, canvas)
        if app.screen == "board":
            drawCell(app, canvas)
            drawProperties(app, canvas)
            drawPlayer(app, canvas)
            drawDiceRoll(app, canvas)
            drawInfo(app, canvas)
        if app.display == "appear" and app.askPlayerAboutUnownedPropertyMode == True:
            drawUnownedMessages(app, canvas)
        elif app.display == "appear" and app.askPlayerAboutOwnedPropertyMode == True:
            drawOwnedMessages(app, canvas)
        elif app.display == "appear" and app.yourOwnProperty == True:
            drawYourOwnProperty(app, canvas)
        if app.info == "appear":
            drawStats(app, canvas)
        if app.playerCanNowBuyHouses == True and app.isTile == False:
            drawAskToBuyHouse(app, canvas)
        if app.display == "appear" and app.isTile == True:
            #and app.players[app.turn].inJail == False 
            #and app.askPlayerAboutUnownedPropertyMode == False 
            #and app.askPlayerAboutOwnedPropertyMode == False):
            drawTileMessages(app, canvas)
        
def drawWinner(app, canvas):
    (x0, y0, x1, y1) = getCellBounds(app, 4, 0)
    (x2, y2, x3, y3) = getCellBounds(app, 6, 9)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width//2, y2, text = f'player {app.winner} has won! Game Over!',
                        font = "Arial 30 bold", fill = "yellow")

def drawTileMessages(app, canvas):
    (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
    (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
    canvas.create_rectangle(x0, y0, x3, y3, outline = "black", fill = "white")
    canvas.create_text(app.width//2, y2 - 20, text = app.message)
    canvas.create_text(app.width//2, y2 + 20, text = "OK", fill = "black")

def drawStartScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = "MONOPOLY", 
                        fill = "black", font = "Arial 40")
    canvas.create_text(app.width//2, app.height*3//5, text = "START", 
                        fill = "black")
    canvas.create_rectangle(app.width//2 - 30, app.height*3//5 - 30, 
                            app.width//2 + 30, app.height*3//5 + 30,
                            outline = "black")

def drawAskToBuyHouse(app, canvas): #do u want to buy houses?
    newImg = PhotoImage(file = 'boom.png')
    (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
    canvas.create_image(x0 + 30, y0 + 10, image = newImg)
    canvas.create_text(x0 + 50, y0 - 10, text = app.boom, fill = "black", 
                        font = "Arial 20 bold", width = 300)
    if app.playerCanNowBuyHouses == True and app.buyingHouses == False:
        canvas.create_text(x0 - 50, y0 + 50, text = "YES", fill = "black", 
                        font = "Arial 20 bold")
        canvas.create_text(x0 + 120, y0 + 50, text = "NO", fill = "black",
                        font = "Arial 20 bold")

    elif app.doesPlayerWantToStopBuyingHouses == True and app.buyingHouses == True:
        (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
        canvas.create_text(app.width//2, y0 + 50, text = "DONE", fill = "black",
                            font = "Arial 20 bold")
    
    
def drawUnownedMessages(app, canvas): #what happens after moving
    (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
    (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
    canvas.create_rectangle(x0, y0, x3, y3, outline = "black", fill = "white")
    canvas.create_text(app.width//2, y2 - 20, text = app.message)
    canvas.create_text(x1 + 100, y2 + 30, text = "YES")
    canvas.create_text(x2 - 100, y2 + 30, text = "NO")

def drawOwnedMessages(app, canvas):
    (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
    (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
    canvas.create_rectangle(x0, y0, x3, y3, outline = "black", fill = "white")
    canvas.create_text(app.width//2, y2 - 20, text = app.message)
    canvas.create_text(app.width//2, y2 + 20, text = "OK", fill = "black")

def drawYourOwnProperty(app, canvas):
    (x0, y0, x1, y1) = getCellBounds(app, 8, 1)
    (x2, y2, x3, y3) = getCellBounds(app, 9, 9)
    canvas.create_rectangle(x0, y0, x3, y3, outline = "black", fill = "white")
    canvas.create_text(app.width//2, y2 - 20, text = app.message)
    canvas.create_text(app.width//2, y2 + 20, text = "OK", fill = "black")

def drawUserNumber(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
                        text = "how many players are playing? (max 6)")
    canvas.create_text(app.width//2, app.height * 3//5, text = app.name)
    canvas.create_text(app.width//2, app.height * 3.01/5, text = "_")
    if len(app.name) == 1:
        canvas.create_text(app.width*3//5, app.height * 3.01/5, text = "next")

def drawDiceRoll(app, canvas):
    if app.hasDiceRolled == False:
        (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
        canvas.create_oval(x0, y0 - 5, x1, y1 - 5, fill = "white")
        canvas.create_text(x1//1.08, y1//1.1, text = "hit space to roll", 
                            fill = "black", font = "Arial 10 bold", width = 35)
    else:
        (x0, y0, x1, y1) = getCellBounds(app, 5, 5)
        canvas.create_oval(x0, y0 - 5, x1, y1 - 5, fill = "black")
        canvas.create_text(x1//1.09, y1//1.1, text = app.dicetotal, 
                            fill = "white", font = "Arial 30 bold")

def drawStats(app, canvas):
    while app.turn in app.deleted:
        if (int(app.name) - len(app.deleted)) == int(app.name) - 1:
            checkWinner(app)
        else:
            app.turn = (app.turn + 1) %(int(app.name) - len(app.deleted))
    (x0, y0, x1, y1) = getCellBounds(app, 1, 6)
    (x2, x3, x4, y4) = getCellBounds(app, 5, 9)
    canvas.create_rectangle(x0 + 50, y0 + 50, x4 - 10, y4, fill = "white", 
                            width = 4)
    canvas.create_text(x0 + 165, y0 + 70, 
                        text = f"PLAYER {app.turn}'s BALANCE:", 
                        font = "Arial 12 bold")
    canvas.create_text(x0 + 165, y0 + 90, text = f'${app.players[app.turn].balance}',
                        font = "Arial 12")
    canvas.create_text(x0 + 140, y0 + 120, text = "PROPERTIES:",
                        font = "Arial 12 bold")
    canvas.create_text(x0 + 240, y0 + 120, text = "RENT:", font = "Arial 12 bold")
    if len(app.players[app.turn].properties) < 1:
        canvas.create_text(x0 + 140, y0 + 140, text = "None", font = "Arial 12")
    else:
        for i in range(len(app.players[app.turn].properties)):
            prop = app.players[app.turn].properties[i]
            canvas.create_text(x0 + 133, y0 + 140 + 20*(i), 
                                text = prop.name, font = "Arial 12")
            canvas.create_oval(x0 + 210, y0 + 134 + 20*(i), x0 + 220,
                                y0 + 144 + 20*(i), 
                                fill = f'{prop.color}')
            canvas.create_text(x0 + 240, y0 + 140 + 20*(i), text = f'${prop.baseRent}', font = "Arial 12")

def drawPlayer(app, canvas): 
    for player in app.players:
        (row, col) = player.getPosition()
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        color = player.getColor()
        canvas.create_oval(x0, y0, x1, y1, fill = color)
   
def drawInfo(app, canvas):
    newImg = PhotoImage(file = 'info.png')
    (x0, y0, x1, y1) = getCellBounds(app, 1, 9)
    canvas.create_image(x1 - 10, y0 + 10, image = newImg)

def drawCell(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0 = app.cellSize * col
            y0 = app.cellSize * row
            x1 = x0 + app.cellSize
            y1 = y0 + app.cellSize
            canvas.create_rectangle(x0, y0, x1, y1, fill = "#BFDBAE",
                                    width = 3)
    newImg = PhotoImage(file = 'Webp.net-resizeimage (1).png')
    canvas.create_image(app.width//2, app.height//2, image = newImg)

def drawProperties(app, canvas):
    (x1, y1, x2, y2) = getCellBounds(app, 0, 1)
    color, price, name = STCHARLESPLACE.getColorPriceAndName()
    canvas.create_rectangle(x1, y1 + 50, x2, y2, fill = color, width = 3)
    canvas.create_text(x2 - x1//2, y1 + 35, text = name,
                        width = 53, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x1 + 38, y1 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if STCHARLESPLACE.numHouses > 0:
        for i in range(STCHARLESPLACE.numHouses): 
            canvas.create_rectangle(x1 + 18*i, y1 + 50, x1 + 15 + 18*i, y2,
                                    fill = "green") 
    elif STCHARLESPLACE.numHotels == 1:
        canvas.create_rectangle(x1 + 20, y1 + 50, x2 - 20, y2, fill = "red")

    (x3, y3, x4, y4) = getCellBounds(app, 0, 3)
    color, price, name = STATESAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x3, y3 + 50, x4, y4, fill = color, width = 3)
    canvas.create_text(x4 - x3//6, y3 + 35, text = name,
                        width = 53, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x3 + 38, y3 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if STATESAVENUE.numHouses > 0:
        for i in range(STATESAVENUE.numHouses): 
            canvas.create_rectangle(x3 + 18*i, y3 + 50, x3 + 15 + 18*i, y4,
                                    fill = "green") 
    elif STATESAVENUE.numHotels == 1:
        canvas.create_rectangle(x3 + 20, y3 + 50, x4 - 20, y4, fill = "red")

    (x5, y5, x6, y6) = getCellBounds(app, 0, 4)
    color, price, name = VIRGINIAAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x5, y5 + 50, x6, y6, fill = color, width = 3)
    canvas.create_text(x6 - x5//8, y5 + 35, text = name,
                        width = 53, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x5 + 38, y5 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if VIRGINIAAVENUE.numHouses > 0:
        for i in range(VIRGINIAAVENUE.numHouses): 
            canvas.create_rectangle(x5 + 18*i, y5 + 50, x5 + 15 + 18*i, y6,
                                    fill = "green") 
    elif VIRGINIAAVENUE.numHotels == 1:
        canvas.create_rectangle(x5 + 20, y5+ 50, x6 - 20, y6, fill = "red")
    (x7, y7, x8, y8) = getCellBounds(app, 0, 6)
    color, price, name = STJAMESPLACE.getColorPriceAndName()
    canvas.create_rectangle(x7, y7 + 50, x8, y8, fill = color, width = 3)
    canvas.create_text(x8 - x7//12, y7 + 35, text = name,
                        width = 53, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x7 + 38, y7 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if STJAMESPLACE.numHouses > 0:
        for i in range(STJAMESPLACE.numHouses): 
            canvas.create_rectangle(x7 + 18*i, y7 + 50, x7 + 15 + 18*i, y8,
                                    fill = "green") 
    elif STJAMESPLACE.numHotels == 1:
        canvas.create_rectangle(x7 + 20, y7 + 50, x8 - 20, y8, fill = "red")
    (x0, y0, x1, y1) = getCellBounds(app, 0, 7)
    newImg = PhotoImage(file = 'cc1.png')
    canvas.create_image(x0 + 35, y0 + 25, image = newImg)
    canvas.create_text(x0 + 35, y0 + 55, text = "COMMUNITY", 
                        font = "Arial 8", angle = 180, width = 50)
    canvas.create_text(x1 - 33, y0 + 45, text = "CHEST",
                        font = "Arial 8", angle = 180, width = 50)
    (x9, y9, x10, y10) = getCellBounds(app, 0, 8)
    color, price, name = TENNESSEEAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x9, y9 + 50, x10, y10, fill = color, width = 3)
    canvas.create_text(x10 - x9//15, y9 + 35, text = name,
                        width = 53, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x9 + 38, y9 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if TENNESSEEAVENUE.numHouses > 0:
        for i in range(TENNESSEEAVENUE.numHouses): 
            canvas.create_rectangle(x9 + 18*i, y9 + 50, x9 + 15 + 18*i, y10,
                                    fill = "green") 
    elif TENNESSEEAVENUE.numHotels == 1:
        canvas.create_rectangle(x9 + 20, y9 + 50, x10 - 20, y10, fill = "red")
    (x10, y10, x11, y11) = getCellBounds(app, 0, 9)
    color, price, name = NEWYORKAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x10, y10 + 50, x11, y11, fill = color, width = 3)
    canvas.create_text(x11 - x10//17, y10 + 35, text = name,
                        width = 70, angle = 180, 
                        font = "Arial 8")
    canvas.create_text(x10 + 38, y10 + 12, text = f'${price}', angle = 180, 
                        font = "Arial 7")
    if NEWYORKAVENUE.numHouses > 0:
        for i in range(NEWYORKAVENUE.numHouses): 
            canvas.create_rectangle(x10 + 18*i, y10 + 50, x10 + 15 + 18*i, y11,
                                    fill = "green") 
    elif NEWYORKAVENUE.numHotels == 1:
        canvas.create_rectangle(x10 + 20, y10 + 50, x11 - 20, y11, fill = "red")
    (x12, y12, x13, y13) = getCellBounds(app, 1, 10)
    color, price, name = KENTUCKYAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x12, y12, x12 + 20, y13, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y12 + 35, text = name,
                        width = 70, angle = 90, 
                        font = "Arial 8")   
    canvas.create_text(x13 - 12, y12 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if KENTUCKYAVENUE.numHouses > 0:
        for i in range(KENTUCKYAVENUE.numHouses): 
            canvas.create_rectangle(x12, y12 + 18*i, x12 + 20 , y12 + 15 + 18*i,
                                    fill = "green") 
    elif KENTUCKYAVENUE.numHotels == 1:
        canvas.create_rectangle(x12, y12 + 20, x12 + 20, y13 - 20, fill = "red")
    (x0, y0, x1, y1) = getCellBounds(app, 2, 10)
    newImg = PhotoImage(file = 'chance2.png')
    canvas.create_image(x1 - 30, y0 + 37, image = newImg)
    canvas.create_text(x0 + 8, y0 + 37, text = "CHANCE", 
                        font = "Arial 8", angle = 90, width = 50)
    (x12, y14, x13, y15) = getCellBounds(app, 3, 10)
    color, price, name = INDIANAAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x12, y14, x12 + 20, y15, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y14 + 35, text = name,
                        width = 60, angle = 90, 
                        font = "Arial 8") 
    canvas.create_text(x13 - 12, y14 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if INDIANAAVENUE.numHouses > 0:
        for i in range(INDIANAAVENUE.numHouses): 
            canvas.create_rectangle(x12, y14 + 18*i, x12 + 20 , y14 + 15 + 18*i,
                                    fill = "green") 
    elif INDIANAAVENUE.numHotels == 1:
        canvas.create_rectangle(x12, y14 + 20, x12 + 20, y15 - 20, fill = "red")
    (x12, y15, x13, y16) = getCellBounds(app, 4, 10)
    color, price, name = ILLINOISAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x12, y15, x12 + 20, y16, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y15 + 35, text = name,
                        width = 60, angle = 90, 
                        font = "Arial 8") 
    canvas.create_text(x13 - 12, y15 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if ILLINOISAVENUE.numHouses > 0:
        for i in range(ILLINOISAVENUE.numHouses): 
            canvas.create_rectangle(x12, y15 + 18*i, x12 + 20 , y15 + 15 + 18*i,
                                    fill = "green") 
    elif ILLINOISAVENUE.numHotels == 1:
        canvas.create_rectangle(x12, y15 + 20, x12 + 20, y16 - 20, fill = "red")
    (x12, y17, x13, y18) = getCellBounds(app, 6, 10)
    color, price, name = ATLANTICAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x12, y17, x12 + 20, y18, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y17 + 35, text = name,
                        width = 60, angle = 90, 
                        font = "Arial 8") 
    canvas.create_text(x13 - 12, y17 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if ATLANTICAVENUE.numHouses > 0:
        for i in range(ATLANTICAVENUE.numHouses): 
            canvas.create_rectangle(x12, y17 + 18*i, x12 + 20 , y17 + 15 + 18*i,
                                    fill = "green") 
    elif ATLANTICAVENUE.numHotels == 1:
        canvas.create_rectangle(x12, y17 + 20, x12 + 20, y18 - 20, fill = "red")
    (x12, y18, x13, y19) = getCellBounds(app, 7, 10)
    color, price, name = VENTNORAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x12, y18, x12 + 20, y19, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y18 + 35, text = name,
                        width = 70, angle = 90, 
                        font = "Arial 8") 
    canvas.create_text(x13 - 12, y18 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if VENTNORAVENUE.numHouses > 0:
        for i in range(VENTNORAVENUE.numHouses): 
            canvas.create_rectangle(x12, y18 + 18*i, x12 + 20 , y18 + 15 + 18*i,
                                    fill = "green") 
    elif VENTNORAVENUE.numHotels == 1:
        canvas.create_rectangle(x12, y18 + 20, x12 + 20, y19 - 20, fill = "red")
    (x12, y20, x13, y21) = getCellBounds(app, 9, 10)
    color, price, name = MARVINGARDENS.getColorPriceAndName()
    canvas.create_rectangle(x12, y20, x12 + 20, y21, fill = color, width = 3)
    canvas.create_text(x13 - x12//20, y20 + 35, text = name,
                        width = 60, angle = 90, 
                        font = "Arial 8") 
    canvas.create_text(x13 - 12, y20 + 35, text = f'${price}', angle = 90,
                        font = "Arial 7")
    if MARVINGARDENS.numHouses > 0:
        for i in range(MARVINGARDENS.numHouses): 
            canvas.create_rectangle(x12, y20 + 18*i, x12 + 20 , y20 + 15 + 18*i,
                                    fill = "green") 
    elif MARVINGARDENS.numHotels == 1:
        canvas.create_rectangle(x12, y20 + 20, x12 + 20, y21 - 20, fill = "red")
    (x14, y22, x15, y23) = getCellBounds(app, 10, 9)
    color, price, name = PACIFICAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x14, y22, x15, y22 + 20, fill = color, width = 3)
    canvas.create_text(x14 + 35, (y22 + y23)//2, 
                        text = name,
                        width = 70, font = "Arial 8") 
    if PACIFICAVENUE.numHouses > 0:
        for i in range(PACIFICAVENUE.numHouses): 
            canvas.create_rectangle(x14 + 18*i, y22, x14 + 15 + 18*i , y22 + 20,
                                    fill = "green") 
    elif PACIFICAVENUE.numHotels == 1:
        canvas.create_rectangle(x14 + 20, y22, x15 - 20, y22 + 20, fill = "red")
    canvas.create_text(x14 + 35, y23 - 12, text = f'${price}', font = "Arial 7")
    (x16, y22, x14, y23) = getCellBounds(app, 10, 8)
    color, price, name = NORTHCAROLINAAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x16, y22, x14, y22 + 20, fill = color, width = 3)
    canvas.create_text(x16 + 35, (y22 + y23)/2, 
                        text = name,
                        width = 65, font = "Arial 7") 
    if NORTHCAROLINAAVENUE.numHouses > 0:
        for i in range(NORTHCAROLINAAVENUE.numHouses): 
            canvas.create_rectangle(x16 + 18*i, y22, x16 + 15 + 18*i , y22 + 20,
                                    fill = "green") 
    elif NORTHCAROLINAAVENUE.numHotels == 1:
        canvas.create_rectangle(x16 + 20, y22, x14 - 20, y22 + 20, fill = "red")
    canvas.create_text(x16 + 35, y23 - 12, text = f'${price}', font = "Arial 7")
    (x0, y0, x1, y1) = getCellBounds(app, 10, 7)
    newImg = PhotoImage(file = 'cc2.png')
    canvas.create_image(x0 + 35, y1 - 25, image = newImg)
    canvas.create_text(x0 + 35, y0 + 15, text = "COMMUNITY", 
                        font = "Arial 8", width = 50)
    canvas.create_text(x1 - 33, y0 + 25, text = "CHEST",
                        font = "Arial 8", width = 50)
    (x17, y22, x18, y23) = getCellBounds(app, 10, 6)
    color, price, name = PENNSYLVANIAAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x17, y22, x18, y22 + 20, fill = color, width = 3)
    canvas.create_text(x17 + 35, (y22 + y23)//2, 
                        text = name,
                        width = 70, font = "Arial 8") 
    if PENNSYLVANIAAVENUE.numHouses > 0:
        for i in range(PENNSYLVANIAAVENUE.numHouses): 
            canvas.create_rectangle(x17 + 18*i, y22, x17 + 15 + 18*i , y22 + 20,
                                    fill = "green") 
    elif PENNSYLVANIAAVENUE.numHotels == 1:
        canvas.create_rectangle(x17 + 20, y22, x18 - 20, y22 + 20, fill = "red")
    canvas.create_text(x17 + 35, y23 - 12, text = f'${price}', font = "Arial 7")
    (x0, y0, x1, y1) = getCellBounds(app, 10, 5)
    newImg = PhotoImage(file = 'rr1.png')
    canvas.create_image(x1 - 38, y0 + 40, image = newImg)
    canvas.create_text(x0 + 35, y0 + 10, text = "SHORT", 
                        font = "Arial 7", width = 50)
    canvas.create_text(x0 + 35, y0 + 20, text = "LINE", 
                        font = "Arial 7", width = 50)
    #price
    (x0, y0, x1, y1) = getCellBounds(app, 10, 4)
    newImg = PhotoImage(file = 'chance3.png')
    canvas.create_image(x0 + 37, y1- 30, image = newImg)
    canvas.create_text(x0 + 37, y0 + 8, text = "CHANCE", 
                        font = "Arial 8", width = 50)
    (x19, y22, x20, y23) = getCellBounds(app, 10, 3)
    color, price, name = PARKPLACE.getColorPriceAndName()
    canvas.create_rectangle(x19, y22, x20, y22 + 20, fill = color, width = 3)
    canvas.create_text(x19 + 35, (y22 + y23)//2, 
                        text = name,
                        width = 70, font = "Arial 8") 
    canvas.create_text(x19 + 35, y23 - 12, text = f'${price}', font = "Arial 7")
    if PARKPLACE.numHouses > 0:
        for i in range(PARKPLACE.numHouses): 
            canvas.create_rectangle(x19 + 18*i, y22, x19 + 15 + 18*i , y22 + 20,
                                    fill = "green") 
    elif PARKPLACE.numHotels == 1:
        canvas.create_rectangle(x19 + 20, y22, x20 - 20, y22 + 20, fill = "red")
    (x21, y22, x22, y23) = getCellBounds(app, 10, 1)
    color, price, name = BOARDWALK.getColorPriceAndName()
    canvas.create_rectangle(x21, y22, x22, y22 + 20, fill = color, width = 3)
    canvas.create_text(x21 + 35, (y22 + y23)//2, 
                        text = name,
                        width = 70, font = "Arial 8") 
    canvas.create_text(x21 + 35, y23 - 12, text = f'${price}', font = "Arial 7")
    if BOARDWALK.numHouses > 0:
        for i in range(BOARDWALK.numHouses): 
            canvas.create_rectangle(x21 + 18*i, y22, x21 + 15 + 18*i , y22 + 20,
                                    fill = "green") 
    elif BOARDWALK.numHotels == 1:
        canvas.create_rectangle(x21 + 20, y22, x22 - 20, y22 + 20, fill = "red")
    (xgo0, ygo0, xgo1, ygo1) = getCellBounds(app, 10, 0)
    canvas.create_text(xgo1 - 45, ygo1 - 45, 
                        text = "Collect $200 as you pass go", 
                        width = 40, angle = 45, font = "Helvetica 5")
    canvas.create_text(xgo1 - 30, ygo1 - 27, text = "GO", 
                        width = 60, angle = 45, font = "Helvetica 34 bold")
    (x23, y24, x24, y25) = getCellBounds(app, 9, 0)
    color, price, name = MEDITERRANEANAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x23 + 50, y24, x24, y25, fill = color, width = 3)
    canvas.create_text(x23 + 35, (y24 + y25)//2, 
                        text = name, angle = 270,
                        width = 70, font = "Arial 7")
    canvas.create_text(x23 + 10, y24 + 35, text = f'${price}', angle = 270,
                        font = "Arial 7") 
    if MEDITERRANEANAVENUE.numHouses > 0:
        for i in range(MEDITERRANEANAVENUE.numHouses): 
            canvas.create_rectangle(x23 + 50, y24 + 18*i, x24, y24 + 15 + 18*i,
                                    fill = "green")
    elif MEDITERRANEANAVENUE.numHotels == 1:
        canvas.create_rectangle(x23 + 50, y24 + 20, x24, y25 - 20, fill = "red")
    (xcc0, ycc0, xcc1, ycc1) = getCellBounds(app, 8, 0)
    newImg = PhotoImage(file = 'cc.png')
    canvas.create_image(xcc0 + 25, ycc0 + 35, image = newImg)
    canvas.create_text(xcc1 - 15, ycc0 + 37, text = "COMMUNITY", 
                        font = "Arial 8", angle = 270, width = 50)
    canvas.create_text(xcc1 - 25, ycc0 + 33, text = "CHEST",
                        font = "Arial 8", angle = 270, width = 50)
    (x25, y24, x26, y25) = getCellBounds(app, 7, 0)
    color, price, name = BALTICAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x25 + 50, y24, x26, y25, fill = color, width = 3)
    canvas.create_text(x25 + 40, (y24 + y25)//2, 
                        text = name, angle = 270,
                        width = 70, font = "Arial 8") 
    canvas.create_text(x25 + 10, y24 + 35, text = f'${price}', angle = 270,
                        font = "Arial 7") 
    if BALTICAVENUE.numHouses > 0:
        for i in range(BALTICAVENUE.numHouses): 
            canvas.create_rectangle(x25 + 50, y24 + 18*i, x26, y24 + 15 + 18*i,
                                    fill = "green")
    elif BALTICAVENUE.numHotels == 1:
        canvas.create_rectangle(x25 + 50, y24 + 20, x26, y25 - 20, fill = "red")
    x0, y0, x1, y1 = getCellBounds(app, 6, 0)
    canvas.create_text(x0 + 58, y0 + 35, text = "INCOME", angle = 270, 
                        font = "Arial 11", width = 70)
    canvas.create_text(x0 + 46, y0 + 35, text = "TAX", angle = 270, 
                        font = "Arial 11", width = 70)  
    canvas.create_text(x0 + 15, y0 + 35, text = "PAY $200", angle = 270, 
                        font = "Arial 8")                  
    (x27, y24, x28, y25) = getCellBounds(app, 4, 0)
    color, price, name = ORIENTALAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x27 + 50, y24, x28, y25, fill = color, 
                            width = 2.5)
    canvas.create_text(x27 + 35, (y24 + y25)//2, 
                        text = name, angle = 270,
                        width = 60, font = "Arial 8") 
    canvas.create_text(x27 + 10, y24 + 35, text = f'${price}', angle = 270,
                        font = "Arial 7") 
    if ORIENTALAVENUE.numHouses > 0:
        for i in range(ORIENTALAVENUE.numHouses): 
            canvas.create_rectangle(x27 + 50, y24 + 18*i, x28, y24 + 15 + 18*i,
                                    fill = "green")
    elif ORIENTALAVENUE.numHotels == 1:
        canvas.create_rectangle(x27 + 50, y24 + 20, x28, y25 - 20, fill = "red")
    (x0, y0, x1, y1) = getCellBounds(app, 3, 0)
    newImg = PhotoImage(file = 'chance1.png')
    canvas.create_image(x0 + 30, y0 + 37, image = newImg)
    canvas.create_text(x1 - 8, y0 + 37, text = "CHANCE", 
                        font = "Arial 8", angle = 270, width = 50)
    (x29, y24, x30, y25) = getCellBounds(app, 2, 0)
    color, price, name = VERMONTAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x29 + 50, y24, x30, y25, fill = color, 
                            width = 3)
    canvas.create_text(x29 + 35, (y24 + y25)//2, 
                        text = name, angle = 270,
                        width = 70, font = "Arial 8") 
    canvas.create_text(x29 + 10, y24 + 35, text = f'${price}', angle = 270,
                        font = "Arial 7") 
    if VERMONTAVENUE.numHouses > 0:
        for i in range(VERMONTAVENUE.numHouses): 
            canvas.create_rectangle(x29 + 50, y24 + 18*i, x30, y24 + 15 + 18*i,
                                    fill = "green")
    elif VERMONTAVENUE.numHotels == 1:
        canvas.create_rectangle(x29 + 50, y24 + 20, x30, y25 - 20, fill = "red")
    (x29, y24, x30, y25) = getCellBounds(app, 1, 0)
    color, price, name = CONNECTICUTAVENUE.getColorPriceAndName()
    canvas.create_rectangle(x29 + 50, y24, x30, y25, fill = color, 
                            width = 3)
    canvas.create_text(x29 + 35, (y24 + y25)//2, 
                        text = name, angle = 270,
                        width = 70, font = "Arial 8") 
    canvas.create_text(x29 + 10, y24 + 35, text = f'${price}', angle = 270,
                        font = "Arial 7") 
    if CONNECTICUTAVENUE.numHouses > 0:
        for i in range(CONNECTICUTAVENUE.numHouses): 
            canvas.create_rectangle(x29 + 50, y24 + 18*i, x30, y24 + 15 + 18*i,
                                    fill = "green")
    elif CONNECTICUTAVENUE.numHotels == 1:
        canvas.create_rectangle(x29 + 50, y24 + 20, x30, y25 - 20, fill = "red")
    (x0, y0, x1, y1) = getCellBounds(app, 5, 0)
    canvas.create_text(x0 + 60, y0 + 35, text = "READING RAILROAD", angle = 270,
                        font = "Arial 7", width = 70)
    newImg = PhotoImage(file = 'readr.png')
    canvas.create_image(x0 + 30, y0 + 35, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 0, 5)
    canvas.create_text(x0 + 35, y0 + 60, text = "PENNSYLVANIA RAILROAD", angle = 180,
                        font = "Arial 7", width = 70)
    newImg = PhotoImage(file = 'pennr.png')
    canvas.create_image(x0 + 35, y0 + 30, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 5, 10)
    canvas.create_text(x0 + 10, y0 + 35, text = "B&O RAILROAD", angle = 90,
                        font = "Arial 7", width = 70)
    newImg = PhotoImage(file = 'bo.png')
    canvas.create_image(x0 + 35, y0 + 35, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 10, 2)
    canvas.create_text(x0 + 35, y0 + 10, text = "LUXURY TAX", font = "Arial 9", 
    width = 70)
    newImg = PhotoImage(file = 'lt.png')
    canvas.create_image(x0 + 35, y0 + 45, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 10, 10)
    canvas.create_text(x0 + 35, y0 + 10, text = "GO TO JAIL", font = "Arial 9", 
    width = 70)
    newImg = PhotoImage(file = 'gojail.png')
    canvas.create_image(x0 + 35, y0 + 45, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 0, 10)
    canvas.create_text(x0 + 35, y0 + 10, text = "FREE PARKING", font = "Arial 8", 
    width = 70)
    newImg = PhotoImage(file = 'free.png')
    canvas.create_image(x0 + 35, y0 + 42, image = newImg)
    (x0, y0, x1, y1) = getCellBounds(app, 0, 0)
    newImg = PhotoImage(file = 'jail.png')
    canvas.create_image(x0 + 35, y0 + 35, image = newImg)
playMonopoly()


