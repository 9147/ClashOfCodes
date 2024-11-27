import openpyxl
from django.core.management.base import BaseCommand
from MainApp.models import Team, Problem
from datetime import datetime

class Command(BaseCommand):
    help = 'Generate Excel file of teams that have made submissions along with submission details'

    def handle(self, *args, **kwargs):
        # Get all teams that have made a submission
        submitted_problems = Problem.objects.select_related('team')

        # Create Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Teams with Submissions"

        # Add headers
        headers = [
            "Team ID", "Team Name", "Leader Name", "Leader Email", "Leader Contact",
            "Member 1", "Member 2", "Member 3", "City", "College", "State", "Country",
            "Submission Title", "Description", "Solution", "Domain", "Track", "Status","Solution File"
        ]
        sheet.append(headers)

        # Populate data
        for problem in submitted_problems:
            team = problem.team
            sheet.append([
                team.id, team.name, team.leader.first_name, team.leader.email, team.leader_contact,
                team.member1_name, team.member2_name, team.member3_name,
                team.city, team.college, team.state, team.country,
                problem.title, problem.description, problem.solution, problem.domain,
                problem.track, problem.status, problem.solution_pdf
            ])

        # Generate the file name with timestamp
        file_name = f"submitted_teams_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = f"./{file_name}"

        # Save the workbook
        workbook.save(file_path)
        self.stdout.write(self.style.SUCCESS(f"Excel file generated: {file_path}"))
