# from rest_framework import serializers
# from MyCareer.models import Vacancy
#
# class VacancySerializer(serializers.ModelSerializer):
#     employer = serializers.PrimaryKeyRelatedField(
#         read_only=True,
#         default=serializers.CurrentUserDefault(),
#     )
#
#     class Meta:
#         model = Vacancy
#         fields = ['title', 'short_description', 'main_description', 'salary', 'main_image', 'additional_images', 'employer']
