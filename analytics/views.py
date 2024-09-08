from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..accounts.models import User, UserInterest, Person
from ..roadMap.models import Roadmap, Interest
from datetime import date


def __companyAnalytics(companyId, companyCity=None):
    """
    Company analytics: Charts with valuable information about user's roadmaps.
    Charts:
    1. Number of users that have the same interest as the company in the same city.
    2. Age range of users that have the same interest as the company in the same city as follows:
        Age < 18, 18 <= Age < 30, 30 <= Age < 50, Age >= 50.
    -- Suggested roadmaps based on company's interests.
    """
    def calculateAge(userId):
        today = date.today() #Today's date.
        person = Person.objects.get(idUser=userId)
        dob = person.dateOfBirth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            return 'U18'
        elif age < 30:
            return '18-30'
        elif age < 50:
            return '30-50'
        else:
            return 'O50'

    def collectData(companyInterests, relatedUsers):
        numOfUsersWithInterests = {} #Dict with the number of users that have the same interest as the company.
        numOfUsersPerAgePerInterest = {} #Dict with the number of users per age range that have the same interest as the company.
        ranges = {
            'U18': 0,
            '18-30': 0,
            '30-50': 0,
            'O50': 0
        }
        for user in relatedUsers:
            userInterests = set(UserInterest.objects.filter(idUser=user.id))
            commonInterests = companyInterests.intersection(userInterests)
            age = calculateAge(user.id)
            for interest in commonInterests:
                #Chart 1:
                if interest in numOfUsersWithInterests:
                    numOfUsersWithInterests[interest] += 1
                else:
                    numOfUsersWithInterests[interest] = 1

                #Chart 2:
                if interest in numOfUsersPerAgePerInterest:
                    numOfUsersPerAgePerInterest[interest][age] += 1
                else:
                    numOfUsersPerAgePerInterest[interest] = ranges
                    numOfUsersPerAgePerInterest[interest][age] += 1

        return numOfUsersWithInterests, numOfUsersPerAgePerInterest
    

    if not companyCity:
        companyCity = User.objects.get(id=companyId).city

    companyInterests = set(UserInterest.objects.filter(idUser=companyId))
    relatedUsers = User.objects.filter(city=companyCity)

    numOfUsersWithInterests, numOfUsersPerAgePerInterest = collectData(companyInterests, relatedUsers)

    #Hacer llamado a la funcion que crea los graficos.

    
        

def __personAnalytics(userId):
    #Suggested roadmaps based on person's interests.
    userInterests = UserInterest.objects.get(idUser=userId)
    suggestedRoadmaps = {}
    for userInterest in userInterests:
        roadmaps = list(Roadmap.objects.filter(idInterest=userInterest.idInterest))
        interest = Interest.objects.get(id=userInterest.idInterest).name
        if roadmaps:
            suggestedRoadmaps[interest] = roadmaps
        else:
            suggestedRoadmaps[interest] = None

    return suggestedRoadmaps

@login_required
def analytics(request):
    #TBF!!
    user = User.objects.get(username=request.user)
    if user.isCompany:
        return __companyAnalytics(user.id)
    else:
        suggestedRoadmaps = __personAnalytics(user.id)
        return render(request, 'personAnalytics.html', {'suggestedRoadmaps': suggestedRoadmaps})
