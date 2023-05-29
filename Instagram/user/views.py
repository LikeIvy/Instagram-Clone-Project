from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from Instagram.settings import MEDIA_ROOT
from uuid import uuid4
import os

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html') # Join이란 함수 실행 시 GET으로 호출했을 때 user폴더의 template join.html을 보여줘라
    
    def post(self, request):
         # TODO 회원가입
         email = request.data.get('email', None)
         nickname = request.data.get('nickname', None)
         name = request.data.get('name', None)
         password = request.data.get('password', None)

         User.objects.create(email = email, 
                             name = name,
                             nickname = nickname, 
                             password = make_password(password),
                             profile_img = "default_profile.jpg")
         
         return Response(status = 200)




class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # TODO 회원가입
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email = email).first()

        if user is None:
            return Response(status = 400, data=dict(message='회원정보가 잘못되었습니다.')) # 회원정보가 있든 없든 동일하게 잘못된 회원정보라고 안내하는것이 바람직하다.(해킹방지)
        
        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status = 200)
        else:
            return Response(status = 400, data=dict(message='회원정보가 잘못되었습니다.'))



class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')
    

class Uploadprofile(APIView):
    def post(self, request):
        file = request.FILES['file'] 
        email = request.data.get('email')

        uuid_name = uuid4().hex 
        save_path = os.path.join(MEDIA_ROOT, uuid_name) 

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        profile_image = uuid_name
        
        
        user = User.objects.filter(email=email).first()

        user.profile_img = profile_image

        user.save()
    
        return Response(status=200)