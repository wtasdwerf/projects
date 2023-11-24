from django.urls import path
from . import views

urlpatterns = [
    # 정기 예금 상품 목록
    path('save-products/', views.save_products),
    # 정기 예금 상품 목록 출력 / 삽입
    path('products/', views.products),
    path('options/', views.options),
    # 특정 상품 옵션 리스트
    path('product-options/<str:fin_prdt_cd>', views.products_options),
    # 최고 금리가 가장 높은 금융상품, 해당 상품 옵션 리스트 출력
    path('products/top_rate/', views.top_rate),
]