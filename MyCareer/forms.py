from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Vacancy, Demand
from django.contrib.auth import get_user_model


class UserProfileForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    is_employer = forms.BooleanField(required=False)
    company = forms.CharField(required=False)
    faculty = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'is_employer', 'company', 'faculty')


class UserProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    is_employer = forms.BooleanField(required=False)
    company = forms.CharField(required=False)
    faculty = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'avatar', 'is_employer', 'company', 'faculty')


class VacancyForm(forms.ModelForm):
    User = get_user_model()
    employer: ModelChoiceField = forms.ModelChoiceField(queryset=User.objects.filter(is_employer=True))
    career_center_id = forms.IntegerField()

    class Meta:
        model = Vacancy
        fields = (
            'employer', 'career_center_id', 'title', 'short_description', 'main_description', 'salary', 'main_image',
            'additional_images')


class EmployerRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    is_employer = forms.BooleanField(required=False)
    company = forms.CharField(required=True)
    faculty = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'is_employer', 'company', 'faculty')


class ApplicantRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    is_employer = forms.BooleanField(required=False)
    company = forms.CharField(required=False)
    faculty = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'is_employer', 'company', 'faculty')


# class AddDemandForm
class DemandForm(forms.ModelForm):
    have_whatsapp = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    have_viber = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    have_telegram = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Demand
        fields = ['reason', 'salary', 'have_whatsapp', 'have_viber', 'have_telegram', 'faculty', 'target', 'stage', 'result']


class AddDemandView(FormView):
    template_name = 'add_demand.html'
    form_class = DemandForm
    success_url = '/add_demand/'  # Укажите URL, на который будет перенаправлен пользователь после успешного сохранения формы

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

