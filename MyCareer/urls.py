"""MyCareer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from api import views
from api.views import export_demands_csv, export_active_demands_csv, export_inactive_demands_csv,update_demand, delete_demand, error_403, error_500, error_502, archive_demand, register_user
from django.contrib.auth.views import LoginView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from api.urls import *

from blog.views import *
from social_api.views import *
from rest_framework import routers
#from django_rest_passwordreset import views as rest_passwordreset_views

handler403 = 'api.views.error_403'
handler500 = 'api.views.error_500'
handler502 = 'api.views.error_502'

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('alldemands/', admin.site.urls),
   # path('add_demand/', views.AddDemandView.as_view(), name='add_demand'),
    path('create-demand/', views.create_demand, name='create_demand'),
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    #path('testtemplate.html', views.test_template, name='testtemplate'),
    path('registration/', views.register_user, name='register'),
    path('my-demands/', views.my_demands, name='my-demands'),
    #path('vacancy_form.html', views.VacancyCreateView.as_view(), name='create_vacancy'),
   # path('vacancytest.html', views.vacancy_list, name='vacancy_list'),
    path('profile', views.see_user_profile, name='profile'),
    # path('profile/update/', update_profile, name='update_profile'),
    path('export-demands-csv/', views.export_demands_csv, name='export_demands_csv'),
    path('export-active-demands-csv/', views.export_active_demands_csv, name='export_active_demands_csv'),
    path('export-inactive-demands-csv/', views.export_inactive_demands_csv, name='export_inactive_demands_csv'),
    #path('export-demands-excel/', ExportDemandsExcelView.as_view(), name='export_demands_excel'),
    path('editprofile.html', views.edit_user_profile, name='editprofile'),
   # path('vacancy/<int:vacancy_id>/', vacancy_detail, name='vacancy_detail'),
   # path('regtest.html', views.create_user_profile, name='create_profile'),
   # path('test_profile.html', views.see_user_profile, name='see_user_profile'),
   # path('test-messenger.html', messenger_test, name='messenger_test'),
   # path('send-message/', views.send_message, name='send_message'),
   # path('registration-plug.html/', views.registration_plug, name='registration_plug'),
   # path('messenger-test.html/', views.messenger_test, name='messenger_test'),
   # path('employer-registration.html', views.employer_registration, name='employer_registration'),
   # path('applicant-registration.html', views.applicant_registration, name='applicant_registration'),
    path('about-us', views.about_us, name='about_us'),
    path('for-student', views.for_student, name='for_student'),
    path('for-employer', views.for_employer, name='for_employer'),
    path('contacts', views.contacts, name='contacts'),
   # path('send-message/', views.send_message, name='send_message'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('admin-test', views.admin_test, name='admintest'),
    #path('test-search.html', job_search, name='search_test'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('demand-interface/', views.demand_interface, name='demand_interface'),
    path('admin-help/', views.admin_help, name='admin_help'),
    path('update-demand/<int:demand_id>/', update_demand, name='update_demand'),
    path('delete-demand/<int:demand_id>/', delete_demand, name='delete_demand'),
    path('archive-demand/<int:demand_id>/', views.archive_demand, name='archive_demand'),
   # path('surveys/', views.surveys, name='surveys'),
   # path('survey/<int:survey_id>/', views.take_survey, name='take_survey'),
    #path('create-survey/', views.create_survey, name='create_survey'),
   # path('edit-survey/<int:survey_id>/', views.edit_survey, name='edit_survey'),
    path('survey-master/', views.survey_master, name='survey_master'),
   # path('edit-survey/<int:survey_id>/delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
   # path('take-survey/<int:survey_id>/', views.take_survey, name='take_survey'),
    path('article-editor/', views.article_editor, name='article_editor'),
    path('tos/', views.tos, name='tos'),
    path('survey/', include('survey.urls')),
    #path('survey/<int:survey_id>/answers/', views.survey_answers, name='survey_answers'),
   # path('survey/<int:survey_id>/answers/<int:user_id>/', views.user_answers, name='user_answers'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('social_api/', include('social_api.urls')),
    #path('post/<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
        #include blog paths
    path('', include('blog.urls')),
    path('', include('survey_helper.urls')),
    path('api/', include('api.urls')),
  #  path('password_reset/', rest_passwordreset_views.PasswordResetView.as_view(), name='password_reset'),
   # path('password_reset/confirm/<uidb64>/<token>/', rest_passwordreset_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]