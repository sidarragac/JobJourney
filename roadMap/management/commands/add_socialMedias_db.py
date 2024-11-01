from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import SocialMedia
import json

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        json_file_path = 'roadMap/management/commands/socialMedias.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            socialMedias = json.load(file)
        
        for i in range(3):
            socialMedia = socialMedias[i]
            exist = SocialMedia.objects.filter(name=socialMedia['name']).first()
            if not exist:
                SocialMedia.objects.create(name=socialMedia['name'])
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded social medias from socialMedias.json'))