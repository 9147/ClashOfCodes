from MainApp.models import Team, Payment
from QRcode.models import DemoUser



def assign_food_access(demo_user, access_dict):
    """
    Assign food access permissions to the user based on the provided dictionary.
    """
    demo_user.lunch1 = access_dict.get('lunch1', False)
    demo_user.dinner = access_dict.get('dinner', False)
    demo_user.breakfast = access_dict.get('breakfast', False) or demo_user.dinner
    demo_user.lunch2 = access_dict.get('lunch2', False)
    demo_user.save()

def create_demo_users():
    # Step 1: Add team members with completed payments
    for team in Team.objects.all():
        leader_payment = Payment.objects.filter(user=team.leader, payment_status="accepted").exists()
        if leader_payment:
            members = [team.leader.username, team.member1_name, team.member2_name, team.member3_name]
            for member in members:
                demo_user, created = DemoUser.objects.get_or_create(name=member, role='Team Member', team_name=team.name)
                # Assign default food access
                assign_food_access(demo_user, {'lunch1': True, 'dinner': True, 'lunch2': False})

    # Step 2: Add volunteers and judges from a sheet
    import csv
    with open('volunteers_judges.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            role = row['role']  # Ensure 'role' is either 'Volunteer' or 'Judge'
            demo_user, created = DemoUser.objects.get_or_create(name=name, role=role)
            # Assign default food access for volunteers and judges
            assign_food_access(demo_user, {'lunch1': True, 'dinner': False, 'lunch2': True})

    print("Demo users created and food access assigned successfully!")
