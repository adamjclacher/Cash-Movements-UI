from django.contrib import admin
from .models import Todo, clientAccount, cashMovementRequest, action

class TodoAdmin(admin.ModelAdmin):
	readonly_fields = ("created",)#make the date created variable show in db

# Register your models here.

admin.site.register(Todo, TodoAdmin)#show models in database
admin.site.register(clientAccount)
admin.site.register(cashMovementRequest)
admin.site.register(action)
