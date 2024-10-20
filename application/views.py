from profile.models import User
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from .models import Application, Comment, Attachment, Attachment_comment
from django.contrib.admin.views.decorators import staff_member_required
from telegram import Bot
import pika
from minio import Minio
from Help_dasks import settings
from .serializers import ApplicationSerializer, default, AttachmentSerializer, Attachment_commentSerializer, CommentSerializer
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


#Представления для сериализаторов



class ApplicationView(APIView):
   def post(self, request, format=None):
       print(request.user)
       if request.user.is_authenticated:
           team = request.data.get('subject')
           text = request.data.get('description')
           id = request.data.get('id')
           user = User.objects.get(id=id)
           name = user.username
           application_serializer = ApplicationSerializer(data={
               'team': team,
               'text': text,
               'created_by': id,
           })
           if application_serializer.is_valid():
               application_serializer.save()
               for f in request.FILES.getlist('files'):
                   Attachment.objects.create(
                      name="",
                      application=application_serializer.instance,
                      image=f)
               return Response((application_serializer.data, {'name': name}), status=status.HTTP_201_CREATED)
           else:
               return Response(application_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       else:
           return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def application_details_api(request, id):
    print(request.user)
    apples = get_object_or_404(Application, id=id)
    user_app = User.objects.get(id=apples.created_by.id)
    attachment = Attachment.objects.filter(application=id)
    attachment_comment = Attachment_comment.objects.filter(comment__application__id=id)
    comments = Comment.objects.filter(application=id).exclude(attachment_comment__isnull=False)

    comment_serializer = CommentSerializer(comments, many=True)
    application_serializer = default(apples, user_app.username)
    attachment_serializer = AttachmentSerializer(attachment, many=True)
    attachment_comment_serializer = Attachment_commentSerializer(attachment_comment, many=True)

    return Response({
       'application': application_serializer,
       'attachment': attachment_serializer.data,
       'comment': comment_serializer.data,
       'attachment_comment': attachment_comment_serializer.data,
    })


@api_view(['GET'])
@permission_classes((permissions.DjangoModelPermissionsOrAnonReadOnly,))
def applications_list_api(request):
   #get_messages()
   if request.user.is_staff:
       applications = Application.objects.all()
   else:
       applications = Application.objects.filter(created_by=request.user_id)
   attachment = Attachment.objects.all()
   comment = Comment
   context = {'attachment': attachment, 'applications': applications, 'comment': comment}
   return JsonResponse(context)


class Applicationst(viewsets.ModelViewSet):
   serializer_class = ApplicationSerializer

   def get_queryset(self):
       id = self.request.POST['id']
       user = User.objects.get(id=id)
       if user.is_staff:
           return Application.objects.all()
       else:
           return Application.objects.filter(Q(created_by=user))


@api_view(['POST'])
def create_comment_api(request, id):
   com_count = 0
   application = Application.objects.get(id=id)
   comments = Comment.objects.filter(application=application.id)
   for com in comments:
       if com.name_id != 1:
           com_count += 1
   if request.method == 'POST':
       apples = application
       user_id = request.POST['user_id']
       name = User.objects.get(id=user_id)
       body = request.POST['content']
       obj = Comment.objects.create(
           application=apples,
           name=name,
           body=body,
       )
       print('comment create')
       for f in request.FILES.getlist('files'):
           att = Attachment_comment.objects.create(
               name="",
               comment=obj,
               image=f)
           a = True
#       if com_count == 0:
#           if request.FILES:
#               if application.telegram:
#                   bot_send_photo(
#                       name=f'static/{att.image}',
#                       chat_id=application.chat_id,
#                       message_id=application.messages_id,
#                       caption=f'Заявка {application.id} : {body}')
#               if application.mail:
#                   message = {"message": [{"text": obj.body}, {'to': obj.name},
#                                          {'attachment': f'static/{att.image}'}],
#                              "replay to message": [{"text": application.text}, {"to": application.name}]}
#                   rabbit_send_message(message)
#           else:
#               if application.telegram:
#                   send_message_by_id(
#                       chat_id=application.chat_id,
#                       message_id=int(application.messages_id),
#                       text=f'Заявка {application.id} : {body}')
#               if application.mail:
#                   message = {"message": [{"text": obj.body}, {'to': obj.name}, {'attachment': 'null'}],
#                              "replay to message": [{"text": application.text}, {"to": application.name}]}
#                   #rabbit_send_message(message)
#       else:
#           for com in Comment.objects.filter(application=application.id):
#               blank = True
#               if com.telegram and com.chat_id == application.chat_id:
#                   if att:
#                       if application.telegram:
#                           bot_send_photo(
#                               name=f'static/{att.image}',
#                               chat_id=application.chat_id,
#                               message_id=int(com.messages_id),
#                               caption=f'Заявка {application.id} : {body}')
#                       if application.mail:
#                           message = {"message": [{"text": obj.body}, {'to': obj.name},
#                                                  {'attachment': f'static/{att.image}'}],
#                                      "replay to message": [{"text": com.text}, {"to": com.name}]}
#                           #rabbit_send_message(message)
#                   else:
#                       if application.telegram:
#                           mes_id = int(com.messages_id)
#                           send_message_by_id(
#                               chat_id=application.chat_id,
#                               message_id=mes_id,
#                               text=f'Заявка {application.id} : {body}')
#                           blank = False
#                       if application.mail:
#                           message = {"message": [{"text": obj.body}, {'to': obj.name}, {'attachment': 'null'}],
#                                      "replay to message": [{"text": com.text}, {"to": com.name}]}
#                           #rabbit_send_message(message)
#                           blank = False
#                       if not blank:
 #                          break
       return JsonResponse({'status': 'success', 'message': 'Comment added successfully'})
   else:
       return JsonResponse({'status': 'error', 'message': 'Invalid request'})





class CommentsView(APIView):
   def get(self, request, id):
       comments = Comment.objects.filter(application=id).exclude(attachment_comment__isnull=False)
       serializer = CommentSerializer(comments, many=True)
       return Response(serializer.data)



@staff_member_required
def status_close_view(request, id):
    try:
        obj = Application.objects.get(id=id)
        obj.status = "Close"
        obj.save()
        return redirect('/app/applications_list/')
    except Application.DoesNotExist:
        return redirect('/app/applications_list/')


def send_message_by_id(chat_id, text, message_id):
    bot = Bot(token=settings.BOT_TOKEN)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_to_message_id=message_id)


def bot_send_photo(name, chat_id, message_id, caption):
    bot = Bot(token=settings.BOT_TOKEN)
    minioClient = Minio(
        settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=False)
    data = minioClient.get_object(bucket_name='telegram', object_name=name)
    photo = data.read()
    bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption,
        reply_to_message_id=message_id)


def rabbit_send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='hello',
                          routing_key='hello',
                          body=message)
    connection.close()


def get_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    method_frame, header_frame, body = channel.basic_get(queue='hello')

    if method_frame:
        taem = body['theme']
        groups = 'mail'
        text = change_text(body['message'])
        priority = 'нет'
        mail = True
        name = body['to']
        attachment = body['attachment'[0]]
        created_by = 3
        if body['Application']:
            obj = Application.objects.create(
                taem=taem,
                groups=groups,
                text=text,
                priority=priority,
                mail=mail,
                created_by=created_by,
                name=name)
            if attachment:
                file_name = f'static/telegram{attachment["fileName"]}'
                Attachment.objects.create(
                    image=file_name,
                    application_id=obj.id)
        else:
            applications = Application.objects.all()
            for application in applications:
                if application.team == taem:
                    obj = Comment.objects.create(
                        taem=taem,
                        body=text,
                        application_id=application.id,
                        name_id=3,
                        name=created_by,
                        mail=mail)
        print(body)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        connection.close()


def change_text(text):
    n_index = text.find("\n")
    r_index = text.find("\r")

    fist_part = text[:n_index]
    second_part = text[r_index:]

    final_part = second_part.split("\r", 1)[0]

    result = final_part + final_part
    return result
