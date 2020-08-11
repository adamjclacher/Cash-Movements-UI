from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
	title = models.CharField(max_length=100)
	memo = models.TextField(blank=True)#can be blank
	created = models.DateTimeField(auto_now_add=True)#any time someone makes a new instance of this object, the date is automatically generated
	datecompleted = models.DateTimeField(null=True, blank=True)#has to be null for time
	important = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.title

class clientAccount(models.Model):
	provider = models.CharField(max_length=20, default="")
	accountNumber = models.CharField(max_length=20, default="")
	accountName = models.CharField(max_length=200, default="")
	currency = models.CharField(max_length=20, default="")
	sortCodeABACA = models.CharField(max_length=50, default="", blank=True)
	bankAccountNumber = models.CharField(max_length=50, default="", blank=True)
	IBAN = models.CharField(max_length=200, default="", blank=True)
	SWIFT = models.CharField(max_length=200, default="", blank=True)
	presentOnDrive = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete = models.CASCADE, default="")
	dateVerified = models.DateTimeField(null=True, blank=True)


	def __str__(self):
		return self.IBAN + " | " + str(self.completed)#This Defines in Django how Items are Named

class cashMovementRequest(models.Model):
	dateRequested = models.DateTimeField(auto_now_add=True)
	withdrawlOrDeposit = models.CharField(max_length=20, default="")
	amount = models.CharField(max_length=20, default="")
	currency = models.CharField(max_length=3, default="")
	provider = models.CharField(max_length=20, default="")
	accountNumber = models.CharField(max_length=20, default="")
	accountName = models.CharField(max_length=200, default="")
	narrative = models.CharField(max_length=200, default="", blank=True)
	sortCodeABACA = models.CharField(max_length=50, default="", blank=True)
	bankAccountNumber = models.CharField(max_length=50, default="", blank=True)
	IBAN = models.CharField(max_length=200, default="", blank=True)
	Notifications = models.CharField(max_length=200, default="", blank=True)
	asuraInternalNarrative = models.CharField(max_length=200, default="", blank=True)
	asuraPaymentIDLloyds = models.CharField(max_length=200, default="", blank=True)
	asuraPaymentIDProvider = models.CharField(max_length=200, default="", blank=True)
	dateCompleted = models.DateTimeField(null=True, blank=True)
	completed = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete = models.CASCADE, default="")
	userCompleted = models.CharField(max_length=50, default="")
	cancellationMessage = models.CharField(max_length=999, default="", blank=True)

	def __str__(self):
		return self.IBAN + " | " + str(self.accountName)

class action(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default="")
	created = models.DateTimeField(null=True, blank=True)
	description = models.CharField(max_length=200, default="")

	def __str__(self):
		return str(self.user) + " | " + str(self.created)
