from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from django.db import transaction
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Ensure database tables are fully cleared before repopulating
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()

            # Create users
            users = [
                User(username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
                User(username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
                User(username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
                User(username='crashoverride', email='crashoverride@hmhigh.edu', password='crashoverridepassword'),
                User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
            ]

            # Add a check to avoid duplicate entries
            for user in users:
                if User.objects.filter(email=user.email).exists():
                    continue
                user.save()

            # Ensure users are saved before adding them to teams
            for user in users:
                user.save()

            # Create teams
            team1 = Team(name='Blue Team')
            team2 = Team(name='Gold Team')
            team1.save()
            team2.save()

            # Update team members after saving users
            team1.members.set(users[:3])
            team2.members.set(users[3:])

            # Create activities
            activities = [
                Activity(user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
                Activity(user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
                Activity(user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
                Activity(user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
                Activity(user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
            ]
            Activity.objects.bulk_create(activities)

            # Create leaderboard entries
            leaderboard_entries = [
                Leaderboard(user=users[0], score=100),
                Leaderboard(user=users[1], score=90),
                Leaderboard(user=users[2], score=95),
                Leaderboard(user=users[3], score=85),
                Leaderboard(user=users[4], score=80),
            ]
            Leaderboard.objects.bulk_create(leaderboard_entries)

            # Create workouts
            workouts = [
                Workout(name='Cycling Training', description='Training for a road cycling event'),
                Workout(name='Crossfit', description='Training for a crossfit competition'),
                Workout(name='Running Training', description='Training for a marathon'),
                Workout(name='Strength Training', description='Training for strength'),
                Workout(name='Swimming Training', description='Training for a swimming competition'),
            ]
            Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the SQLite database with test data.'))
