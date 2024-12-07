from django.shortcuts import render
from .models import DemoUser, CurrentFoodCheck
from django.http import JsonResponse
import json

def home(request):
    if request.method == 'POST':
        # Handle form submission
        data = json.loads(request.body)
        unique_code = data.get('unique_code')
        try:
            demo_user = DemoUser.objects.get(unique_code=unique_code)
            # check what is the current food status
            current_food_check = CurrentFoodCheck.objects.first()
            current_food = current_food_check.current_food
            # check if the user has access to the current food by checking the corresponding field in the DemoUser model
            has_access = getattr(demo_user, current_food)
            if has_access:
                # check if the current food is already completed
                is_completed = getattr(demo_user, f"{current_food}_completed")
                if is_completed:
                    return JsonResponse({'error': f'{current_food} already marked as completed for {demo_user.name}'}, status=400)
                # change the status of the current food to completed
                setattr(demo_user, f"{current_food}_completed", True)
                demo_user.save()
                return JsonResponse({'success': f'{current_food} marked as completed for {demo_user.name}'})
            else:
                return JsonResponse({'error': 'User doesnt have access to this food'}, status=403)
        except DemoUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return render(request, 'QRcode/home.html')
