from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from .models import DepositOptions, DepositProducts


# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

@api_view(['GET'])
def test_data(request):
    url = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo': 1
    }

    response = requests.get(url, params=params).json()

    return JsonResponse({'response':response})


@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    
    for li in response.get('result').get('baseList'):
            save_data1 = {
                "fin_prdt_cd": li.get("fin_prdt_cd"),
                "kor_co_nm": li.get("kor_co_nm"),
                "fin_prdt_nm": li.get("fin_prdt_nm"),
                "join_way": li.get("join_way"),
                "join_deny": li.get('join_deny'),
                "join_member": li.get('join_member'),
                "etc_note": li.get('etc_note'),
                "spcl_cnd": li.get("spcl_cnd"),
            }
            serializer = DepositProductsSerializer(data=save_data1, many=True)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except:
                pass
   
    for li in response.get('result').get('optionList'):
            product = DepositProducts.objects.get(fin_prdt_cd=li.get('fin_prdt_cd')),
            save_data2 = {
                'fin_prdt_cd' :li.get("fin_prdt_cd"),     # 금융 상품 코드
                'intr_rate_type_nm' :li.get("intr_rate_type_nm"),    # 저축 금리 유형명
                'intr_rate' :li.get("intr_rate") or -1,    # 저축 금리
                'intr_rate2': li.get("intr_rate2") or -1,    # 최고 우대 금리
                'save_trm': li.get("save_trm"),
            }
            serializer = DepositOptionsSerializer(data=save_data2, many=True)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product)
            except:
                pass
    

    # 저장완료 메세지
    return JsonResponse({ 'message': 'okay' })




@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse({ 'message' : 'success' })
        return JsonResponse({ 'message' : 'failed' })
    
    elif request.method == 'GET':
        deposit_products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products, many=True)
        return Response(serializer.data)





@api_view(['GET'])
def deposit_products_options(request, fin_prdt_cd):
    selected_option = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(selected_option, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def top_rate(request):
    option_list = DepositOptions.objects.all()
    top_rate_products_code = ""
    max_intr = -1
    for option in option_list:
        if top_rate_products_code == "":
            top_rate_products_code = option.fin_prdt_cd
            max_intr = option.intr_rate2
        else:
            if option.intr_rate2 > max_intr:
                top_rate_products_code = option.fin_prdt_cd
                max_intr = option.intr_rate2
    
    top_rate_option_list = DepositOptions.objects.filter(fin_prdt_cd=top_rate_products_code)
    top_rate_product = DepositProducts.objects.get(fin_prdt_cd=top_rate_products_code)
    
    top_rate_option_dict_list = []
    top_rate_product_dict = top_rate_product.__dict__
    top_rate_product_dict.pop('_state', None)
    
    for option in top_rate_option_list:
        option_dict = option.__dict__
        option_dict.pop('_state', None)
        top_rate_option_dict_list.append(option_dict)
    
    print(top_rate_product_dict)
    print(top_rate_option_dict_list)
    
    ret = {
        'deposit_product': top_rate_product_dict,
        'option': top_rate_option_dict_list,
    }
    
    return Response(ret)