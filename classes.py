class Game:
    def __init__(self, homeTeamId=None, homeTeamName=None, awayTeamId=None, awayTeamName=None, score=None, competitionName=None, competitionId=None, location=None):
        self.homeTeamId = homeTeamId
        self.homeTeamName = homeTeamName
        self.awayTeamId = awayTeamId
        self.awayTeamName = awayTeamName
        self.score = score
        self.competitionName = competitionName
        self.competitionId = competitionId
        self.location = location

class Club:
    def __init__(self, clubName, logoUrl, website=None, facebook=None, twitter=None, instagram=None, locationAddress=None, locationDescription=None, locationLat=None, locationLong=None, sourceUrl=None, sourceName=None):
        self.name=clubName,
        self.logoUrl=logoUrl,
        self.website=website,
        self.facebook=facebook,
        self.twitter=twitter,
        self.instagram=instagram,
        self.locationDescription=locationDescription,
        self.locationAddress=locationAddress,
        self.locationLat=locationLat,
        self.locationLong=locationLong,
        self.sourceUrl = sourceUrl,
        self.sourceName = sourceName,

class Event:
    def __init__(self, name, category=None, dateStart=None, dateEnd=None, dateText=None, location=None, address=None, description=None, sourceUrl=None, sourceName=None):
        self.name = name
        self.category = category
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.dateText = dateText
        self.location = location
        self.address = address
        self.description = description
        self.sourceUrl = sourceUrl
        self.sourceName = sourceName