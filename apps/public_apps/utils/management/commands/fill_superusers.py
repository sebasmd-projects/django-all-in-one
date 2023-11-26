import json
import os
from getpass import getpass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create, add, delete, or remove superusers from JSON and/or database'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--add',
            action='store_true',
            help='Add a new superuser to the JSON file'
        )
        parser.add_argument(
            '-ac',
            '--addcreate',
            action='store_true',
            help='Add a new superuser to the JSON file and DB'
        )
        parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            help='Delete an existing superuser from JSON file'
        )
        parser.add_argument(
            '-dr',
            '--deleteremove',
            action='store_true',
            help='Delete an existing superuser from JSON file and DB'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        super_users_file = os.path.join(
            settings.BASE_DIR, "apps", "public_apps", "utils", "data", "super_users.json"
        )

        if options['add'] or options['addcreate']:
            user_exists = False

            username = input('Enter username: ')
            email = input('Enter email: ')
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            password = getpass('Enter password: ')
            confirm_password = getpass('Confirm password: ')

            while password != confirm_password:
                self.stdout.write(
                    self.style.WARNING(
                        'Password does not match!'
                    )
                )
                password = getpass('Enter password:')
                confirm_password = getpass('Confirm password:')

            try:
                with open(super_users_file, 'r') as json_file:
                    existing_users = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_users = []

            for user_data in existing_users:
                if user_data["username"] == username or user_data["email"] == email:
                    user_exists = True
                    break

            if not user_exists:
                existing_users.append({
                    "username": username,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password
                })

                with open(super_users_file, 'w') as json_file:
                    json.dump(existing_users, json_file, indent=4)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Superuser {username} added to json'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'Superuser {username} could not be added to json'
                    )
                )

            if options['addcreate']:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superuser {username} created in DB'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Superuser {username} could not be created in DB'
                        )
                    )

        elif options['delete'] or options['deleteremove']:
            username_or_email = input('Enter username or email to delete: ')

            user_exists = False

            try:
                with open(super_users_file, 'r') as json_file:
                    existing_users = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_users = []

            for user_data in existing_users:
                if ('@' in username_or_email and user_data["email"] == username_or_email) or (user_data["username"] == username_or_email):
                    existing_users.remove(user_data)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superuser {
                                username_or_email} removed from JSON file'
                        )
                    )
                    with open(super_users_file, 'w') as json_file:
                        json.dump(existing_users, json_file, indent=4)
                    user_exists = True
                    break

            if not user_exists:
                self.stdout.write(
                    self.style.ERROR(
                        f'Superuser {
                            username_or_email} does not exist in JSON file'
                    )
                )

            if options['deleteremove']:
                # TODO: Error; Delete superuser in DB (django.db.utils.ProgrammingError: no existe la relación «apps_tenant_alarm»                LINE 1: ...time", "apps_tenant_alarm"."creator_user_id" FROM "apps_tena...)

                try:
                    if '@' in username_or_email:
                        user = User.objects.get(
                            email=username_or_email
                        )
                    else:
                        user = User.objects.get(
                            username=username_or_email
                        )
                    user.delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superuser {username_or_email} removed from DB'
                        )
                    )
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Superuser {
                                username_or_email} does not exist in DB'
                        )
                    )

        else:
            try:
                with open(super_users_file, 'r') as json_file:
                    existing_users = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_users = []

            for user_data in existing_users:
                username = user_data["username"]
                email = user_data["email"]
                first_name = user_data["first_name"]
                last_name = user_data["last_name"]
                password = user_data["password"]

                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superuser {username} created from JSON: Email: "{
                                email}", Nombre: "{first_name} {last_name}"'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Superuser {
                                username} already exists in the database'
                        )
                    )
