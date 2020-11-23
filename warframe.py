from urllib.request import Request, urlopen
from html.parser import HTMLParser


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

#overframe = Overframe()

#print(overframe.prettyPrint("warframes"))
