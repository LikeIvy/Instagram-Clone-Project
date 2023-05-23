from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed


# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # select * from content_feed;(쿼리셋)

        return render(request, 'Instagram/main.html', context=dict(feeds=feed_list)) # context로 데이터를 넣어줄 때는 항상 dict형태로 넣어줘야 한다.(실제로는 json형식으로 넣어야 하나 dict랑 호환이 되기 때문에)
