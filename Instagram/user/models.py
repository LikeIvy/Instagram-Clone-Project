from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    '''
        유저 프로필 사진
        유저 닉네임 => 화면에 표기되는 이름
        유저 이름 => 실제 사용자 이름
        유저 이메일 주소 => 회원가입 시 사용할 아이디
        유저 비밀번호 => 디폴트 쓰자
    '''
    email = models.EmailField(unique=True)    
    name = models.CharField(max_length=24)
    nickname = models.CharField(max_length=24, unique=True)
    profile_img = models.TextField() 

    USERNAME_FIELD = 'nickname' # 실제로 user를 선택하면 user의 어떤 필드를 사용할 것인지 정의

class Meta:
    db_table = "User"

