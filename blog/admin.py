from django.contrib import admin
#from django.contrib.gis import forms

from .models import *
from mptt.admin import MPTTModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'created_at', 'updated_at', 'isPostHidden')
    filter_horizontal = ('tags',)

class PostPage(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'created_at', 'updated_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Page, PostPage)
admin.site.register(Tag)
admin.site.register(PostType)

#class PostAdminForm(forms.ModelForm):
   # content = forms.CharField(widget=CKEditorUploadingWidget())
   # class Meta:
   #     model = Post
    #    fields = '__all__'