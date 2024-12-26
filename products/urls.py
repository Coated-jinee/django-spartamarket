from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),  # 제품 리스트 보기
    path('create/', views.product_create_view, name='product_create'),  # 제품 생성
    path('<int:pk>/', views.product_detail_view, name='product_detail'),  # 제품 상세 보기
    path('<int:pk>/edit/', views.product_edit_view, name='product_edit'),  # 제품 수정
    path('<int:pk>/delete/', views.product_delete_view, name='product_delete'),  # 제품 삭제
    path('<int:pk>/like/', views.product_like_view, name='product_like'),  # 제품 좋아요
]