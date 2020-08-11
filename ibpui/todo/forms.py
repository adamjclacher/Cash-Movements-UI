from django.forms import ModelForm
from django import forms
from .models import Todo, clientAccount, cashMovementRequest #imports the Todo model from models.py

class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ["title", "memo", "important"]

class ListForm(forms.ModelForm):
	class Meta:
		model = clientAccount
		fields = ["provider", "accountNumber", "accountName", "currency", "sortCodeABACA", "bankAccountNumber", "IBAN", "SWIFT", "completed", "presentOnDrive"]

class cashMovementRequestForm(forms.ModelForm):
	class Meta:
		model = cashMovementRequest
		fields = ["withdrawlOrDeposit", "amount", "currency", "accountNumber", "accountName", "narrative", "sortCodeABACA", "bankAccountNumber", "IBAN", "Notifications", "asuraInternalNarrative", "asuraPaymentIDLloyds", "asuraPaymentIDProvider", "dateCompleted", "provider", "cancellationMessage"]

class deleteCashMovementRequestForm(forms.ModelForm):
	class Meta:
		model = cashMovementRequest
		fields = ["cancellationMessage"]
