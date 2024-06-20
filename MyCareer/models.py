from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.sites import requests
from django.db import models
from django.db.models.signals import post_save
from django.db.models import DateTimeField
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import requests
import random
import string
# class CareerCenter(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.name


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=255)
    firstname = models.TextField(null=True, max_length=100)
    surname = models.TextField(null=True, max_length=100)
    patronymic = models.TextField(null=True, max_length=100)
    vk_id = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=0)
    phonenumber = models.CharField(null=True, max_length=11)
    telegram_id = models.TextField(null=True, blank=True, max_length=100)
    telegram_code = models.CharField(null=True, blank=True, max_length=100)
    other_contacts = models.TextField(blank=True, null=True, max_length=100)
    have_whatsapp = models.BooleanField(null=True, default=False)
    have_telegram = models.BooleanField(null=True, default=False)
    have_viber = models.BooleanField(null=True, default=False)
    is_staff = models.BooleanField(blank=True, null=True, default=False)
    faculty = models.CharField(null=True, max_length=255, blank=True)
    course = models.DecimalField(blank=True, null=True, max_digits=1, decimal_places=0)
    direction = models.CharField(null=True, max_length=255, blank=True)
    recordbook = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=0)
    is_ended_study = models.BooleanField(null=True, default=False)
    year_of_ending = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=0)
    is_active = models.BooleanField(default=True) # добавлено поле is_active
    objects = UserProfileManager()
    agreed_for_email_bulletins = models.BooleanField(null=True, default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_telegram_code(self):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.telegram_code = code
        self.save()
        return code
    def __str__(self):
        return self.email


# class Vacancy(models.Model):
#     employer = models.ForeignKey(
#         UserProfile,
#         on_delete=models.CASCADE,
#         related_name='vacancies'
#     )
#     career_center = models.ForeignKey(
#         CareerCenter,
#         on_delete=models.CASCADE,
#         related_name='vacancies',
#         null=True
#     )
#     title = models.CharField(max_length=100)
#     short_description = models.TextField()
#     main_description = models.TextField()
#     salary = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
#     main_image = models.ImageField(upload_to='vacancy_images')
#     additional_images = models.ManyToManyField('AdditionalImage', blank=True)
#
#     def __str__(self):
#         return self.title


# class AdditionalImage(models.Model):
#     image = models.ImageField(upload_to='additional_images')
#
#     def __str__(self):
#         return self.image.name


# class Messenger(models.Model):
#     career_centers = models.ManyToManyField(
#         CareerCenter,
#         related_name='messengers'
#     )
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
#     # Additional fields related to the messenger
#
#     def __str__(self):
#         return self.name


# class Message(models.Model):
#     sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
#     message = models.TextField()
#
#     def __str__(self):
#         return self.message


class Demand(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='demands', blank=True,
                                     null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #date_updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    isArchived = models.BooleanField(blank=True, null=True)
    target = models.TextField()
    stage = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.target

    def save(self, *args, **kwargs):
        is_stage_changed = False
        if self.pk:
            original_instance = Demand.objects.get(pk=self.pk)
            if original_instance.stage != self.stage:
                is_stage_changed = True

        if not self.pk:
            user_profile = self.user_profile
            if user_profile:
                self.have_whatsapp = user_profile.have_whatsapp
                self.have_viber = user_profile.have_viber
                self.have_telegram = user_profile.have_telegram
                self.phonenumber = user_profile
                self.faculty = user_profile.faculty

        super().save(*args, **kwargs)

        if is_stage_changed:
            # отправка сообщения в лс пользователю с id 1837265180
            chat_id = 1837265180
            token = "7159365270:AAGh8r8XColkr4gPXXeAb4wwXvuIpT1ksqo"
            message_text = f"Здравствуйте! Ваша заявка '{self.target}' от '{self.date_created}' изменила статус на '{self.stage}'"
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": message_text}

            # создание объекта PreparedRequest
            req = requests.Request('POST', url, data=data).prepare()

            # вывод в консоль деталей запроса
            print(f"Sending Telegram message:")
            print(f"URL: {req.url}")
            print(f"Headers: {req.headers}")
            print(f"Body: {req.body}")

            response = requests.post(url, data=data)
            if response.status_code != 200:
                print(f"Error sending Telegram message: {response.text}")
            else:
                print(f"Success: {response.text}")

# class Counter(models.Model):
#     count = models.IntegerField(default=0)
#
#     def __str__(self):
#         return str(self.count)
#
#     class Meta:
#         verbose_name_plural = 'Counter'
#
#
# @receiver(post_save, sender=Demand)
# def update_counter(sender, instance, created, **kwargs):
#     counter, _ = Counter.objects.get_or_create(pk=1)
#     counter.count = Demand.objects.count()
#     counter.save()

from django.db import models


# class Survey(models.Model):
#     title = models.CharField(max_length=255)
#     short_description = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     description_after_passing = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title


# class Question(models.Model):
#     survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
#     text = models.TextField()
#     is_mandatory = models.BooleanField(null=True, default=True)
#
#     # Добавим поле, которое будет указывать на тип вопроса (текстовый, один выбор, множественный выбор)
#     QUESTION_TYPES = [
#         ('text', 'Текстовый вопрос'),
#         ('single_choice', 'Выбор одного варианта'),
#         ('multiple_choice', 'Выбор нескольких вариантов'),
#     ]
#     question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='text')
#
#     def __str__(self):
#         return self.text


# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     answer_choices = models.JSONField(blank=True, null=True)
#     date_answered = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Answer to '{self.question.text}' by {self.user_profile.email}"

 #   from django.db import models

# class Faculty(models.Model):
#         name = models.CharField(max_length=100)
#
#         def __str__(self):
#             return self.name


# class StudyDirection(models.Model):
#     name = models.CharField(max_length=100)
#
#     # Добавляем поле для служебного флага
#     # EDUCATION_LEVEL_CHOICES = (
#     #     ('Бакалавриат', 'Бакалавриат'),
#     #     ('Магистратура', 'Магистратура'),
#     #     ('Специалитет', 'Специалитет'),
#     # )
#     # education_level = models.CharField(
#     #     max_length=20,
#     #     choices=EDUCATION_LEVEL_CHOICES,
#     #     default='Бакалавриат',
#     # )
#
#     # Связываем направление с факультетом
#     faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


