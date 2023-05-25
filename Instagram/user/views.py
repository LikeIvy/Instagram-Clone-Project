from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html') # Join이란 함수 실행 시 GET으로 호출했을 때 user폴더의 template join.html을 보여줘라
    
    def post(self, request):
         # TODO 회원가입
         pass


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # TODO 회원가입
        pass