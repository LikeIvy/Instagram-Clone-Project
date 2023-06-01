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
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')
        
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
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_img,
                                  nickname=user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))

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
    
        Feed.objects.create(image=image, content=content, email=email) # 피드를 새로 만듦(DB에 추가)

        return Response(status=200)
    


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')
        
        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True)) # value_list와 flat을 true로 준 후 list로 감싸주면 object가 리스트로 나옴
        like_feed_list = Feed.objects.filter(id__in=like_list) # id__in => Feed에 있는 아이디중 like_list(피드 아이디 리스트를 포함하고 있는 애들만 걸린다)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list, like_feed_list=like_feed_list, bookmark_feed_list=bookmark_feed_list, user=user))
    


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)
    


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border': 
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)
    


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)

        if bookmark_text == 'bookmark_border': 
            is_marked = True
        else:
            is_marked = False

        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)
