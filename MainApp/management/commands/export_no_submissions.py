import openpyxl
from django.core.management.base import BaseCommand
from MainApp.models import Team, Problem
from datetime import datetime

class Command(BaseCommand):
    help = 'Generate Excel file of teams with no submissions'

    def handle(self, *args, **kwargs):
        # Get all teams that have not made a submission
        submitted_teams = Problem.objects.values_list('team_id', flat=True)
        no_submission_teams = Team.objects.exclude(id__in=submitted_teams)

        # Create Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Teams Without Submissions"

        # Add headers
        headers = [
            "Team ID", "Team Name", "Leader Name","Leader Email", "Leader Contact", 
            "Member 1", "Member 2", "Member 3", "City", "College", "State", "Country"
        ]
        sheet.append(headers)

        # Populate data
        for team in no_submission_teams:
            sheet.append([
                team.id, team.name, team.leader.first_name,team.leader.username, team.leader_contact,
                team.member1_name, team.member2_name, team.member3_name,
                team.city, team.college, team.state, team.country
            ])

        # Generate the file name with timestamp
        file_name = f"no_submission_teams_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = f"./{file_name}"

        # Save the workbook
        workbook.save(file_path)
        self.stdout.write(self.style.SUCCESS(f"Excel file generated: {file_path}"))
