from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.db.models import DateTimeField
from django.dispatch import receiver

class CareerCenter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


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
    #user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=255)
    firstname = models.TextField(null=True, max_length=100)
    surname = models.TextField(null=True, max_length=100)
    patronymic = models.TextField(null=True, max_length=100)
    vk_id = models.DecimalField(null=True, max_digits=12, decimal_places=0)
    phonenumber = models.DecimalField(null=True, max_digits=11, decimal_places=0)
    other_contacts = models.TextField(null=True, max_length=100)
    have_whatsapp = models.BooleanField(null=True, default=False)
    have_telegram = models.BooleanField(null=True, default=False)
    have_viber = models.BooleanField(null=True, default=False)
    is_staff = models.BooleanField(null=True, default=False)
    is_employer = models.BooleanField(null=True, default=False)
    company = models.CharField(null=True, max_length=255, blank=True)
    faculty = models.CharField(null=True, max_length=255, blank=True)
    course = models.DecimalField(null=True, max_digits=1, decimal_places=0)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Vacancy(models.Model):
    employer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    career_center = models.ForeignKey(
        CareerCenter,
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    main_description = models.TextField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    main_image = models.ImageField(upload_to='vacancy_images')
    additional_images = models.ManyToManyField('AdditionalImage', blank=True)

    def __str__(self):
        return self.title


class AdditionalImage(models.Model):
    image = models.ImageField(upload_to='additional_images')

    def __str__(self):
        return self.image.name


class Messenger(models.Model):
    career_centers = models.ManyToManyField(
        CareerCenter,
        related_name='messengers'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    # Additional fields related to the messenger

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()

    def __str__(self):
        return self.message


class Demand(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    reason = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    have_whatsapp = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='have_wa'
    )
    have_viber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='have_vb'
    )
    have_telegram = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='have_tg'
    )
    faculty = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='fac'
    )
    target = models.TextField()
    stage = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reason

class Counter(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)

    class Meta:
        verbose_name_plural = 'Counter'


@receiver(post_save, sender=Demand)
def update_counter(sender, instance, created, **kwargs):
    if created:
        counter, _ = Counter.objects.get_or_create(pk=1)
        counter.count += 1
        counter.save()