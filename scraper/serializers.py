from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Article

class ArticleSerializer(ModelSerializer):
    date = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M:%S')