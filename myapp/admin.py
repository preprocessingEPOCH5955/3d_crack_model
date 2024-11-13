from django.contrib import admin


from .models import *


@admin.register(Signup_form)
class Signup_formAdmin(admin.ModelAdmin):
    list_display  = ["firstname","lastname","email","password",'project_name',]

@admin.register(project_data)
class project_admin(admin.ModelAdmin):
    list_display = [f.name for f in project_data._meta.fields]
# admin.site.register(Signup_form,Signup_formAdmin)
# class admin_project_creation(admin.ModelAdmin):
#     list_display  = ["project_piccture","project_name","User_name","user_password","user"]
# admin.site.register(project_create_by_admin,admin_project_creation)
# @admin.register(project_data)
# class padmin(admin.ModelAdmin):
#     list_display = [f.name for f in project_data._meta.fields]