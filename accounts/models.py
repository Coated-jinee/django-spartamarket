from django.db import models
from django.contrib.auth.models import AbstractUser

# 프로필 이미지를 저장할 경로 설정 함수
def user_profile_image_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'

# 사용자 모델
class User(AbstractUser):
    # 프로필 이미지 필드
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)

    # 팔로우 관계 (비대칭)
    follows = models.ManyToManyField(
        'self',  # User 모델 간의 관계
        symmetrical=False,  # 비대칭 관계 (팔로우와 팔로잉 분리)
        related_name='followers',  # 역참조 이름: followers
        blank=True  # 비어 있을 수 있음
    )

    # 팔로워 수 계산
    @property
    def follower_count(self):
        return self.followers.count()

    # 팔로잉 수 계산
    @property
    def following_count(self):
        return self.follows.count()

    # 사용자 출력 형식
    def __str__(self):
        return self.username