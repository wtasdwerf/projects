from django.urls import path
from . import views

urlpatterns = [
    # 정기 예금 상품 목록
    path('test_data/', views.test_data),
    # 정기 예금 상품 목록
    path('save-deposit-products/', views.save_deposit_products),
    # 정기 예금 상품 목록 출력 / 삽입
    path('deposit-products/', views.deposit_products),
    # 특정 상품 옵션 리스트
    path('deposit-product-options/<str:fin_prdt_cd>', views.deposit_products_options),
    # 최고 금리가 가장 높은 금융상품, 해당 상품 옵션 리스트 출력
    path('deposit-products/top_rate/', views.top_rate),
]