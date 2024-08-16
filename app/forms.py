from django import forms
from django.contrib.auth.models import User

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

class RemoveUserForm(forms.Form):
    username = forms.CharField(max_length=150)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

from django import forms
from .models import Level, Question

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['name', 'difficulty']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['level', 'question_text', 'correct_answer', 'option_1', 'option_2', 'option_3', 'option_4']
