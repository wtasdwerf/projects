import pprint
import requests

def get_deposit_products():
    # 본인의 API KEY 로 수정합니다.
    api_key = "b86152420296c641fed96a7608677733"
    url  = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        'auth' : api_key,
        'topFinGrpNo': '020000',
        'pageNo' : 1

    }
    # 응답을 json 형태로 변환
    response = requests.get(url, params = params).json()
    description = response["result"]["baseList"]
    
    return description

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_deposit_products()
    # prrint.prrint(): json 을 보기 좋은 형식으로 출력
    pprint.pprint(result)