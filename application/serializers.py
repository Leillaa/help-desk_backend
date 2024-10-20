from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Q
from Help_dasks import settings
from .models import Application, Attachment, Attachment_comment, Comment
import json


def default(obj, name):
    return {
        'groups': obj.groups,
        'team': obj.team,
        'text': obj.text,
        'created_by': obj.created_by.id,
        'created': obj.created.strftime("%Y-%m-%d %H:%M:%S"),
        'status': obj.status,
        'messages_id': obj.messages_id,
        'priority': obj.priority,
        'chat_id': obj.chat_id,
        'telegram': obj.telegram,
        'mail': obj.mail,
        'name': name,
    }

class AttachmentSerializer(serializers.ModelSerializer):
    application = serializers.StringRelatedField()

    class Meta:
       model = Attachment
       fields = ['name', 'application', 'image']



class CommentSerializer(serializers.ModelSerializer):
   application_id = serializers.PrimaryKeyRelatedField(source='application', read_only=True)
   username = serializers.CharField(source='name.username', read_only=True)

   class Meta:
       model = Comment
       fields = ['id', 'application_id', 'username', 'name', 'body', 'messages_id', 'telegram', 'created', 'chat_id', 'mail']


class Attachment_commentSerializer(serializers.ModelSerializer):
   comment = CommentSerializer(read_only=True)

   class Meta:
       model = Attachment_comment
       fields = ['name', 'comment', 'image']

   def to_representation(self, instance):
       representation = super().to_representation(instance)
       representation['image'].replace("http://minio:9000/", "http://127.0.0.1:9000/")
       #representation = a.replace("http://minio:9000/", "http://127.0.0.1:9000/")
       return representation


class ApplicationSerializer(serializers.ModelSerializer):
   comment_count = serializers.SerializerMethodField()

   class Meta:
       model = Application
       fields = ['id', 'groups', 'team', 'text', 'created_by', 'created', 'updated', 'status', 'messages_id', 'priority', 'chat_id', 'telegram', 'mail', 'name', 'comment_count']

   def get_comment_count(self, obj):
       return obj.comment_set.count()

