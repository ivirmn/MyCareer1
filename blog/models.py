from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from transliterate import translit


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - /{self.slug}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    not_show_create_date = models.BooleanField(null=True, default=False)
    show_edit_date = models.BooleanField(null=True, default=False)
    isPostHidden = models.BooleanField(null=True, default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    no_autopost = models.BooleanField(default=False, null=True, verbose_name="Не постить в соцсети")

    # type = models.ManyToField(Type, blank=true)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #    return reverse('post_detail', args=[str(Tag.slug), str(self.slug)])

    def get_absolute_url(self):
        if self.tags.all():
            return reverse('post_detail', args=[str(self.slug)])
        else:
            return reverse('post_list')

    def __str__(self):
        return f"{self.title} - /{self.slug}"


class PostType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - /{self.slug}"

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_page_hidden = models.BooleanField(null=True, default=False)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE, related_name='pages', null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return f"{self.title} - /{self.slug}"



