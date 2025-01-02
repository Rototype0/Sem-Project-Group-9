from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import DeskUserProfile


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=20)
    height_cm = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=175)
    user_type = forms.ChoiceField(choices=DeskUserProfile.USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'age', 'height_cm' ,'user_type')
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        print("called save")
        user = super(RegisterUserForm, self).save(commit=commit)
        print("saved user")

        desk_user = DeskUserProfile.objects.get(user=User.objects.get(id=user.id))
        desk_user.age = self.cleaned_data['age']
        desk_user.height_cm=self.cleaned_data['height_cm']
        desk_user.user_type=self.cleaned_data['user_type']
        desk_user.save()
        return desk_user