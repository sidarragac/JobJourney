from django.core.management.base import BaseCommand
from roadMap.models import Interest
import os
import json





class Command(BaseCommand):
    help = 'Load movies from movies_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        json_file_path = 'roadMap/management/commands/interests.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            interests = json.load(file)
        
        for i in range(14):
            interest = interests[i]
            exist = Interest.objects.filter(name=interest['name']).first()
            if not exist:
                Interest.objects.create(name=interest['name'], description=interest['description'])
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded interests from interests.json'))
        
