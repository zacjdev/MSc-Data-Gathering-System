class Game:
    def __init__(self, hash, homeTeamName=None, awayTeamName=None, score=None, dateStart=None, competitionName=None, competitionId=None, location=None, sourceUrl=None, sourceName=None, sport=None):
        self.homeTeamName = homeTeamName
        self.awayTeamName = awayTeamName
        self.score = score
        self.competitionName = competitionName
        self.competitionId = competitionId
        self.dateStart = dateStart
        self.location = location
        self.sport = sport
        self.sourceUrl = sourceUrl
        self.sourceName = sourceName
        self.hash = hash

    def to_dict(self):
        return {
            "homeTeamName": self.homeTeamName,
            "awayTeamName": self.awayTeamName,
            "score": self.score,
            "competitionName": self.competitionName,
            "dateStart": self.dateStart,
            "competitionId": self.competitionId,
            "location": self.location,
            "sourceUrl": self.sourceUrl,
            "sourceName": self.sourceName,
            "sport": self.sport,
            "hash": self.hash  
        }

class Club:
    def __init__(self, hash, clubName, clubCode=None, location=None, logoUrl=None, website=None, facebook=None, twitter=None, instagram=None, sourceUrl=None, sourceName=None, sport=None):
        self.name = clubName
        self.clubCode = clubCode
        self.logoUrl = logoUrl
        self.website = website
        self.facebook = facebook
        self.twitter = twitter
        self.location = location
        self.instagram = instagram
        self.sourceUrl = sourceUrl
        self.sourceName = sourceName
        self.sport = sport
        self.hash = hash

    def to_dict(self):
        return {
            "name": self.name,
            "logoUrl": self.logoUrl,
            "website": self.website,
            "facebook": self.facebook,
            "location": self.location,
            "twitter": self.twitter,
            "instagram": self.instagram,
            "sourceUrl": self.sourceUrl,
            "sourceName": self.sourceName,
            "sport": self.sport,
            "hash": self.hash
        }

class Event:
    def __init__(self, hash, name, category=None, dateStart=None, dateEnd=None, dateText=None, location=None, description=None, sourceUrl=None, sourceName=None, sport=None):
        self.name = name
        self.category = category
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.dateText = dateText
        self.description = description
        self.location = location
        self.sourceUrl = sourceUrl
        self.sourceName = sourceName
        self.sport = sport
        self.hash = hash

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "dateStart": self.dateStart,
            "dateEnd": self.dateEnd,
            "dateText": self.dateText,
            "location": self.location,
            "description": self.description,
            "sourceUrl": self.sourceUrl,
            "sourceName": self.sourceName,
            "sport": self.sport,
            "hash": self.hash
        }
    
class Location:
    def __init__(self, description=None, address=None, lat=None, long=None, generatedCoords=False):
        self.description = description
        self.address = address
        self.lat = lat
        self.long = long
        self.generatedCoords = generatedCoords

    def to_dict(self):
        return {
            "description": self.description,
            "address": self.address,
            "lat": self.lat,
            "long": self.long,
            "generatedCoords": self.generatedCoords
        }