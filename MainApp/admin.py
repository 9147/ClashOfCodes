from django.contrib import admin
from .models import Team, UserToken, submissiontime, contact, Problem, ladingPage, ReferralCode, Payment

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name','city','college','state','country']
    sortable_by = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name','city','college']
    search_fields = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name','city','college']
    list_filter = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name','city','college']

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'token_created_at']
    sortable_by = ['user', 'token', 'token_created_at']
    search_fields = ['user', 'token', 'token_created_at']
    list_filter = ['user', 'token', 'token_created_at']

@admin.register(submissiontime)
class submissiontimeAdmin(admin.ModelAdmin):
    list_display = ['tag', 'submission_time']
    sortable_by = ['tag', 'submission_time']
    search_fields = ['tag', 'submission_time']
    list_filter = ['tag', 'submission_time']


@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    list_display = ['email', 'message','action']
    sortable_by = ['email', 'message','action']
    search_fields = ['email', 'message','action']
    list_filter = ['email', 'message','action']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'team', 'description', 'solution','solution_pdf','domain','track']
    sortable_by = ['title', 'team', 'description', 'solution','solution_pdf','domain','track']
    search_fields = ['title', 'team', 'description', 'solution','solution_pdf','domain','track']
    list_filter = ['title', 'team', 'description', 'solution','solution_pdf','domain','track']

@admin.register(ladingPage)
class landingPageAdmin(admin.ModelAdmin):
    list_display = ['user','is_set']
    sortable_by = ['user','is_set']
    search_fields = ['user','is_set']
    list_filter = ['user','is_set']

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'college']
    sortable_by = ['code', 'college']
    search_fields = ['code', 'college']
    list_filter = ['code', 'college']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount','utr_number','payment_screenshot','posted_date','payment_status']
    sortable_by = ['posted_date','payment_status']


