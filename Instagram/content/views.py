from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from uuid import uuid4
import os
from Instagram.settings import MEDIA_ROOT

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # select * from content_feed;(쿼리셋)

        return render(request, 'Instagram/main.html', context=dict(feeds=feed_list)) # context로 데이터를 넣어줄 때는 항상 dict형태로 넣어줘야 한다.(실제로는 json형식으로 넣어야 하나 dict랑 호환이 되기 때문에)


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
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')
    
        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0) # 피드를 새로 만듦(DB에 추가)

        return Response(status=200)