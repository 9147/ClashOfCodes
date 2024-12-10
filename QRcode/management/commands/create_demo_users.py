from QRcode.models import DemoUser
import openpyxl
from django.db import transaction
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate the DemoUser model with data from the given Excel file.'

    def add_arguments(self, parser):
        # Add the base_url argument (this is the parameter that you will pass)
        parser.add_argument('--reset', type=bool, help='Reset all the completed flags to False')

    def handle(self, *args, **kwargs):
            
        """
        Populate the DemoUser model with data from the given Excel file.
        :param file_path: Path to the Excel file.
        """

        # rest all options is flagged as False or true defalut is false
        reset = kwargs.get('reset', False) 

        try:
            # Load the Excel workbook
            file_path = "DemoUsers.xlsx"
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Skip the header row
            rows = list(sheet.iter_rows(values_only=True))[1:]

            # Start a database transaction
            with transaction.atomic():
                for row in rows:
                    user_id, team_name, member_name, role , lunch1, dinner, breakfast, lunch2 = row
                    
                    # Create or update the DemoUser
                    demo_user, created = DemoUser.objects.update_or_create(
                        id=user_id,
                        defaults={
                            'name': member_name,
                            'team_name': team_name if team_name else None,
                            'role': role,
                            'lunch1': lunch1,
                            'dinner': dinner,
                            'breakfast': breakfast,
                            'lunch2': lunch2,
                            
                        }

                    )
                    # set lunch_completed, dinner_completed, breakfast_completed, lunch2_completed to false  if reset was true
                    if reset:
                        demo_user.lunch1_completed = False
                        demo_user.dinner_completed = False
                        demo_user.breakfast_completed = False
                        demo_user.lunch2_completed = False
                        demo_user.save()
                    print(f"{'Created' if created else 'Updated'} DemoUser: {demo_user.name} ({demo_user.id})")
            
            print("DemoUser data successfully populated.")
        except Exception as e:
            print(f"Error populating DemoUser data: {e}")
