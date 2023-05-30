from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User
from uuid import uuid4
import os
from Instagram.settings import MEDIA_ROOT

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_object_list = Feed.objects.all().order_by('-id') # select * from content_feed;(쿼리셋)
        feed_list = []
        
        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=feed.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))

            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_img,
                                  nickname=user.nickname,
                                  reply_list=reply_list
                                  ))

        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        return render(request, 'Instagram/main.html', context=dict(feeds=feed_list, user=user)) # context로 데이터를 넣어줄 때는 항상 dict형태로 넣어줘야 한다.(실제로는 json형식으로 넣어야 하나 dict랑 호환이 되기 때문에)


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file'] # 파일을 불러오고

        uuid_name = uuid4().hex # 랜덤하게 글자를 만들어줌
        save_path = os.path.join(MEDIA_ROOT, uuid_name) # 즉, 프로젝트 경로/미디어/uud4로 생성된 이름으로 저장된다  => ./media/uuid4

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)
    
        Feed.objects.create(image=image, content=content, email=email, like_count=0) # 피드를 새로 만듦(DB에 추가)

        return Response(status=200)
    

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')
        return render(request, 'content/profile.html', context=dict(user=user))
    


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)
