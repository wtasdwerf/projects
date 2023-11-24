##  정기 예금 상품 목록 db 저장
  > api로 전달받은 데이터를 db에 저장하는 도중 외래키를 포함하고 있는 객체를 product에 담아주고, 해당 product를 serializer.save(product=product)에 담아주어 해결

## 전체 정기예금 상품 목록 출력
  > 조회, 수정 요청을 받는 경우로 나누어 직렬화하여 유효성 검사를 한 이후 db에 저장하였다.

## 정기예금 상품 추가하기
  > 옵션 내에 있는 객체들 중 filter를 통해 fin_prdt_cd가 일치하는 경우만을 직렬화하여 json 파일로 출력하는 과정이였다.


## 특정 상품의 옵션 리스트 출력
  > 옵션 내에 있는 객체들 중 filter를 통해 fin_prdt_cd가 일치하는 경우만을 직렬화하여 json 파일로 출력하는 과정이였다.


## 금리가 가장 높은 상품의 정보 출력  
> 옵션 내에 있는 모든 객체를 가져와서 해당 객체 내에서 top_rate_products_code가 비어있는 경우를  고려하여 코드를 구현하였다. 그리고 금리가 가장 높은 옵션들을 top_rate_option_list로 filter를 통해 객체들을 가져오고, 해당 옵션을 통해 금리가 높은 상품을 top_rate_product에 담아서 가져왔다. 그 후, top_rate_option_list를 순회하며 dict_list에 하나씩 추가하고 해당 리스트 내의 요소들을 모두 출력한다.