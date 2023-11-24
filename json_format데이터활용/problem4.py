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
    # 금융회사명, 금융상품명, 금리정보(큰 틀)
    big_list = []

    for base in response["result"]["baseList"]:
        big_dict = {}
        # fin_prdt_cd를 기반으로 optionList에서 데이터를 추출할 변수
        temp = [base["fin_prdt_cd"]]
        # 금리정보(저축 금리, 저축 기간, 저축금리유형, 저축 금리 유형명, 최고 우대금리)
        new_list = []
        for option in response["result"]["optionList"]:
            if option["fin_prdt_cd"] in temp:
                new_dict = {}
                new_dict['저축 금리'] = option["intr_rate"]
                new_dict['저축 기간'] = option['save_trm']
                new_dict['저축금리유형'] = option["intr_rate_type"]
                new_dict['저축금리유형명'] = option["intr_rate_type_nm"]
                new_dict['최고 우대금리'] = option["intr_rate2"]
                # '금융상품코드' : response["result"]["optionList"][i]["fin_prdt_cd"],
                # '저축 금리' : response["result"]["optionList"]["intr_rate"],
                # '저축 기간' : response["result"]["optionList"]['save_trm'],
                # '저축금리유형' : response["result"]["optionList"]["intr_rate_type"],
                # '저축금리유형명' : response["result"]["optionList"]["intr_rate_type_nm"],
                # '최고 우대금리' : response["result"]["optionList"]["intr_rate2"],
                new_list.append(new_dict)

        big_dict['금리정보'] = new_list
        big_dict['금융회사명'] = base["kor_co_nm"]
        big_dict['금융상품명'] = base["fin_prdt_nm"]

        big_list.append(big_dict)

    return big_list

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_deposit_products()
    # prrint.prrint(): json 을 보기 좋은 형식으로 출력
    pprint.pprint(result)