from django.core.management.base import BaseCommand
from MainApp.models import Team, Problem
import openpyxl
from datetime import datetime


class Command(BaseCommand):
    help = 'Generate Excel file of all team members from teams with completed payments'

    def handle(self, *args, **kwargs):
        # Fetch all teams whose leaders have completed payment
        teams_with_payments =  Problem.objects.select_related('team').filter(status='Accepted')

        # Create Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Paid Teams Members"

        # Add headers
        headers = ["Team Name", "Member Name"]
        sheet.append(headers)

        # Populate data
        for team in teams_with_payments:
            team = team.team
            payment = getattr(team.leader, 'payment', None)
            if not payment :
                continue
            # Add team leader
            sheet.append([team.name, team.leader.first_name])
            # Add team members
            if team.member1_name:
                sheet.append([team.name, team.member1_name])
            if team.member2_name:
                sheet.append([team.name, team.member2_name])
            if team.member3_name and team.member3_name != "" and team.member3_name != None and team.member3_name != "None" and team.member3_name != "none" and team.member3_name != "NONE" and team.member3_name != "null" and team.member3_name != "NULL" and team.member3_name != "Null" and team.member3_name != "nil" and team.member3_name != "NIL" and team.member3_name != "Nil" and team.member3_name != "." and team.member3_name !="_":
                sheet.append([team.name, team.member3_name])

        # Generate the file name with timestamp
        file_name = f"team_members_paid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = f"./{file_name}"

        # Save the workbook
        workbook.save(file_path)
        self.stdout.write(self.style.SUCCESS(f"Excel file generated: {file_path}"))