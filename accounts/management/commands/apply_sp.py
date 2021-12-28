"""
Apply Story Points Command
"""

import json
import sys

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Q

from accounts.models import Sprint, StoryPoint, CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('data.json', "r") as f:
            obj = json.loads(f.read())
            date = obj['date']
            sprint = Sprint.objects.latest()
            print(sprint)
            if not sprint:
                sys.stdout.write("*** Please setup sprint date.\n")
                return
            for item in obj['data']:
                username = item['user']
                user = CustomUser.objects.get(username=username)
                try:
                    StoryPoint.objects.create(user=user,
                                              sprint=sprint,
                                              date=date,
                                              sp=item['sp'])
                except IntegrityError as e:
                    StoryPoint.objects.filter(Q(user=user) &
                                              Q(date=date)).delete()
                    StoryPoint.objects.create(user=user,
                                              sprint=sprint,
                                              date=date,
                                              sp=item['sp'])
