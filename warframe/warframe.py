from urllib.request import Request, urlopen
from html.parser import HTMLParser
from Levenshtein import distance
from json import loads

class Parser(HTMLParser):

    tier="N/A"
    previous="N/A"
    tierMap=[]
    currLink="N/A"

    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if("arsenal" in value):
                self.currLink=Overframe.baseOverframe+value
                #print("Encountered a start tag:", value)

    def handle_data(self, data):
        if( self.tier != "Done"):
            if( "Tier -" in data ):
                self.tier=self.previous
            elif ("Social Media" in data):
                self.tier="Done"
            elif (self.tier != "N/A"):
                if(data == "S"):
                    #print( self.tier + " " + self.previous)
                    self.tierMap.append((self.tier,self.previous,self.currLink))
            self.previous=data

    def finish(self):
        self.tier="N/A"
        self.previous="N/A"
        self.currLink="N/A"
        temp = self.tierMap
        self.tierMap=[]
        return temp



class Overframe:
    baseOverframe="https://overframe.gg"
    warframes=[]
    primaries=[]
    secondaries=[]
    melee=[]

    def __init__(self):
        rawWarframe=self.getData("/tier-list/warframes/")
        parser = Parser()
        parser.feed(rawWarframe)
        self.warframes=parser.finish()
        rawPrimaries=self.getData("/tier-list/primary-weapons/")
        parser.feed(rawPrimaries)
        self.primaries=parser.finish()
        rawSecondaries=self.getData("/tier-list/secondary-weapons/")
        parser.feed(rawSecondaries)
        self.secondaries=parser.finish()
        rawMelee=self.getData("/tier-list/melee-weapons/")
        parser.feed(rawMelee)
        self.melee=parser.finish()

    def prettyPrint(self,data):
            msg = ''
            if data.startswith("warframe"):
                    print("Processing warframe ranks")
                    prevTier="N/A"
                    for item in self.warframes :
                            if( item[0] != prevTier):
                                    prevTier=item[0]
                                    msg += '\n===== {} Tier =====\n{}'.format(item[0], item[1])
                            else :
                                    msg += ', {}'.format(item[1])
            elif data.startswith("primary"):
                    print("Processing primary weapon ranks")
                    prevTier="N/A"
                    for item in self.primaries :
                            if( item[0] != prevTier):
                                    prevTier=item[0]
                                    msg += '\n===== {} Tier =====\n{}'.format(item[0], item[1])
                            else :
                                    msg += ', {}'.format(item[1])
            elif data.startswith("secondary"):
                    print("Processing secondary weapon ranks")
                    prevTier="N/A"
                    for item in self.secondaries :
                            if( item[0] != prevTier):
                                    prevTier=item[0]
                                    msg += '\n===== {} Tier =====\n{}'.format(item[0], item[1])
                            else :
                                    msg += ', {}'.format(item[1])
            elif data.startswith("melee"):
                    print("Processing melee weapon ranks")
                    prevTier="N/A"
                    for item in self.melee :
                            if( item[0] != prevTier):
                                    prevTier=item[0]
                                    msg += '\n===== {} Tier =====\n{}'.format(item[0], item[1])
                            else :
                                    msg += ', {}'.format(item[1])
            else :
                    print("Processing rank: ", data)
                    tempList= self.warframes + self.primaries + self.secondaries + self.melee
                    for item in tempList:
                            if item[1].lower() == data.lower():
                                    msg = '{} is Tier {}'.format(item[1],item[0])
            return msg

    def getLink(self,data):
            msg = ''
            tempList= self.warframes + self.primaries + self.secondaries + self.melee
            for item in tempList:
                if item[1].lower() == data.lower():
                    msg = '{}'.format(item[2])
            return msg

    def getData(self,endpoint):
        req = Request(self.baseOverframe + endpoint , headers={'User-Agent': 'Mozilla/5.0'})
        mybytes = urlopen(req).read()
        return mybytes.decode("utf8")

class Warframe:
    overframe = Overframe()
    warframeApi = 'http://content.warframe.com/dynamic/worldState.php'

    #functions
    def getPriceURL(self,item):
        line = 'https://api.warframe.market/v1/items/' + item.replace(' ', '_').lower() + '/statistics'
        return line

    def getJson(self,url):
        request = Request(url)
        response = urlopen(request)
        jsonData = loads(response.read().decode('utf-8'))
        return jsonData

    def handleMessageWrapper(self,message,author):
        splitMessage = message.split(' ',2)
        subCommand = splitMessage[1]

        if subCommand.startswith('!help'):
            return self.handleMessageHelp(author)
        elif subCommand.startswith('!price'):
            return self.handleMessagePrice(splitMessage)
        elif subCommand.startswith('!wiki'):
            return self.handleMessageWiki(splitMessage)
        elif subCommand.startswith('!rank'):
            return self.overframe.prettyPrint(splitMessage[2].strip())
        elif subCommand.startswith('!build'):
            return self.overframe.getLink(splitMessage[2].strip())

    #Get the help response
    def handleMessageHelp(self,author):
        msg = '{} These are the Warframe commands:\n'
        msg += '!warframe !help : Gets all warframe commands.\n'
        msg += '!warframe !price (item): Pulls the median price from the market.)\n'
        msg += '!warframe !wiki (item): Gets the wiki page for a requested object.\n'
        msg += '!warframe !build (item): Gets the overframe.gg build page for a requested object.\n'
        msg += '!warframe !rank (item): Gets the overframe.gg rank info for a requested object. Use warframes,primary weapons, secondary weapons, or melee weapons for the entire group\n'
        return msg.format(author)

    def handleMessagePrice(self,splitMessage):
        if len(splitMessage) >= 3:
            request = splitMessage[2]
            jsonData = self.getJson(self.getPriceURL(request))
            newmsg = ''
            median = 0
            for item in jsonData['payload']['statistics_closed']['90days']:
                median = item['median']
            return '{} has a median price of {}.'.format(request, median)

    def handleMessageWiki(self, splitMessage):
        if len(splitMessage) >= 3:
            base = 'https://warframe.fandom.com/wiki/'
            filepath = 'warframe_items.txt'
            request = splitMessage[2]

            #uses levenshtein distance to determine the closes item
            #still needs work
            minDist = 1000
            minPhrase = 'Error'
            with open(filepath) as fp:
                line = fp.readline()
                while line:
                    currDistance = distance(request, line)
                    if currDistance < minDist :
                        minDist = currDistance
                        minPhrase = line
                    line = fp.readline()
            minPhrase = minPhrase.replace(' ', '_')
            return "{}".format(base+minPhrase)


#warframe = Warframe()
#print(warframe.handleMessageWrapper("!warframe !price reaper prime blade", "@Jake"))
