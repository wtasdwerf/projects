

# 1일차

1. 메인 페이지 작성(vue, django)
    
    [final_pjt_front](https://www.notion.so/final_pjt_front-88dfc5ff7d3640f8b73d9d5989f3b16e?pvs=21)
    
    [final_pjt_back](https://www.notion.so/final_pjt_back-07b66ca8bb864954aa7f04c4e74b7b2d?pvs=21)
    
2. 금융상품통합비교공시 api를 활용하여 예금,적금 데이터 GET
    1. 예금 데이터, 적금 데이터를 json으로 GET하여 models.py내에 작성된 모델을 기반으로 직렬화 수행. 
    2. 예금 데이터, 적금 데이터 중 unique value로 인해 get 과정에서 error가 발생하여, try-except 구문을 활용하여 error 발생 시 강제로 pass
    3. 예금, 적금을 DB에 저장
    
    ```python
    # requests 모듈을 활용하여 정기예금 상품 목록 데이터를 가져와 정기예금 
    # 상품 목록과 옵션 목록을 DB에 저장
    @api_view(['GET'])
    def save_products(request):
        api_key = settings.API_KEY
        deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1' 
        saving_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1' 
        
        # 정기 예금 상품 목록 및 옵션 목록 받기
        deposit_json = requests.get(deposit_url).json()
        saving_json = requests.get(saving_url).json()
        
        product_list = deposit_json.get('result').get('baseList')
        product_list.extend(saving_json.get('result').get('baseList'))
        
        option_list = deposit_json.get('result').get('optionList')
        option_list.extend(saving_json.get('result').get('optionList'))
        
        # 상품 목록 저장
        # 이 때 중복된 코드가 저장되지 않도록 try-except 사용
        for product in product_list:
            deposit_products = {
                'fin_prdt_cd': product.get('fin_prdt_cd'),
                'kor_co_nm': product.get('kor_co_nm'),
                'fin_prdt_nm': product.get('fin_prdt_nm'),
                'etc_note': product.get('etc_note'),
                'join_deny': product.get('join_deny'),
                'join_member': product.get('join_member'),
                'join_way': product.get('join_way'),
                'spcl_cnd': product.get('spcl_cnd'),
            }
            
            serializer = ProductsSerializer(data = deposit_products)
            
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except:
                pass
        
        # 옵션 목록 저장    
        # 이 때 중복된 코드가 저장되지 않도록 try-except 사용
        for option in option_list:
            product = Products.objects.get(fin_prdt_cd=option.get('fin_prdt_cd')),
            deposit_options = {
                'fin_prdt_cd': option.get('fin_prdt_cd'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'intr_rate': option.get('intr_rate') or -1,
                'intr_rate2': option.get('intr_rate2') or -1,
                'save_trm': option.get('save_trm'),
            }
            
            serializer = OptionsSerializer(data = deposit_options)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product)
            except:
                pass
        
        return JsonResponse({ 'message' : 'success' })
    ```
    

3. DB에 저장한 데이터를 vue에서 GET

1) 비동기 통신을 위해 axios를 활용하여 django 주소에서 가져온 데이터들을 다시 get

```jsx
// stores/products.js
// 전체 예금 상품 조회
  const getAllProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/products/`,
      // headers: {
      //   Authorization: `Token ${token.value}`
      // }
    })
      .then((res) => {
        console.log(res)
        products.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  return { getAllProducts, API_URL, products }
})
```

4. vue detail 페이지에서 선택한 상품 정보 출력

```jsx
<div>
    <h1>상품 리스트</h1>
    <div v-for="product in store.products" :key="product.id">
      <p>{{ product.kor_co_nm }}</p>
      <p>{{ product.fin_prdt_nm }}</p>
      <p>{{ product.join_way}}</p>
      <hr>
    </div>
    <p>{{ store.products }}</p>
  </div>

```

1. 고객이 검색한 은행과 db의 은행명을 대조하여 필터링
    1. 해당 view가 수행되는 순간 getAllProducts 수행
    2. productList에 모든 예적금 데이터를 담아줌
    3. 고객이 검색하지 않았을 경우 모든 상품을 출력
    4. 고객이 검색할 경우 store의 products의 모든 요소에 대해 indexOf() 메서드를 활용하여 고객이 검색한 단어와 store의 상품명을 비교하여 같은 경우의 상품들만 출력
        - indexOf() : javascript의 문자열 비교 함수로, 일치하는 경우가 없을시 -1을 반환
    

```jsx
// views/ProductListView.vue
		
<form @submit.prevent="searchByBank">
      <label for="search">은행명 : </label>
      <input type="text" v-model="query" id="search">
      <input type="submit" value="검색">
    </form>

import { onMounted, ref } from 'vue';
import { useProductStore } from '../stores/products';
import { useRouter } from 'vue-router';

const router = useRouter()
const store = useProductStore()
const query = ref(null)
const productList = ref([])

onMounted(() => {
  store.getAllProducts()
  productList.value = store.products
})

const goDetail = function (productId) {
  router.push({ name: 'product_detail', params: { id: productId } })
}

const searchByBank = function () {
  productList.value = []
  if(query.value === null) {
    productList.value = store.products
  }
  else {
    store.products.forEach(prod => {
      if(prod.kor_co_nm.indexOf(query.value) != -1) {
        productList.value.push(prod)
      }
    })
  }
}
```

1. 특정 상품 클릭 시 상세 정보 페이지로 전환
    1. onclick을 활용하여 상품명을 클릭 시 goDetail 함수를 통해 ProductDetailView로 이동하여 상품에 대한 더 자세한 정보를 확인 가능

```jsx
<template>
  <div>
    <h1>상품 리스트</h1>
    <form @submit.prevent="searchByBank">
      <label for="search">은행명 : </label>
      <input type="text" v-model="query" id="search">
      <input type="submit" value="검색">
    </form>

    <div v-for="product in productList" :key="product.id">
      <p>{{ product.kor_co_nm }}</p>
      <p @click="goDetail(product.id)">{{ product.fin_prdt_nm }}</p>
      <p>{{ product.join_way }}</p>
      <hr>
    </div>
  </div>
</template>

<script setup>
	const goDetail = function (productId) {
	  router.push({ name: 'product_detail', params: { id: productId } })
	}
</script>
```


<hr>

# 2일차

1. 회원가입
    
    ```python
    # final_pjt_back/bank_api
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('dj_rest_auth.urls')),
        path('products/', include('products.urls')),
        path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    ]
    ```
    
    bank_api url에서 유저들의 회원가입을 위한 url 작성
    
    해당 url 내에서 회원가입 진행 후 로그인 진행 시 drf로부터 토큰이 발급됨
    
2. 개인 컴퓨터로 node.js 설치 후 vue install 시도 시 환경변수 편집했음에도 불구하고 설치 안됨

- GPT
에러 메시지를 보니 **`esbuild`** 모듈이 설치되지 않은 것 같네요. **`npm ERR! code 1`**는 일반적으로 모듈 설치 과정에서 어떤 문제가 발생했다는 것을 의미합니다. 이런 문제들은 여러 가지 이유로 발생할 수 있어요. ⇒ 모듈 설치 과정에서 문제 발생하였으나 원인을 몰라 진행하지 못했음.

로그인, 로그아웃 및 여러 기능들을 vue에서 수행해야 했기 때문에 진전이 별로 없어 많이 아쉬웠다.

<hr>

# 3일차

1. 특정 상품 클릭 시 상세 정보 페이지로 전환, 상품 정보 출력
    1. productListView가 마운트될때 store에서 모든 제품을 가져옴
    2. 각 제품의 일부 정보를 화면상에 출력
    3. 제품 클릭시 제품의 상세정보 확인 가능
    4. 각 제품에 마우스를 갖다댈 시 색이 변하게 스타일 변경

```jsx
// views/ProductListView

<template>
  <div>
    <h1>상품 리스트</h1>
    <div class="input-group mb-3">
      <input type="text" class="query" placeholder="search query" aria-label="query" aria-describedby="search" v-model="query">
      <button class="btn btn-outline-secondary" type="button" id="search" @click="searchByBank">Search</button>
    </div>

    <ul class="list-group">
      <li class="list-group-item product-item" v-for="product in productList" :key="product.id" @click="goDetail(product.id)">
        <p>kor_co_nm : {{ product.kor_co_nm }}</p>
        <p>fin_prdt_nm : {{ product.fin_prdt_nm }}</p>
        <p>join_way : {{ product.join_way }}</p>
        <p>etc_note : {{ product.etc_note }}</p>
        <p>spcl_cnd : {{ product.spcl_cnd }}</p>
        <p>join_member : {{ product.spcl_cnd }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useProductStore } from '../stores/products';
import { useRouter } from 'vue-router';

const router = useRouter()
const store = useProductStore()
const query = ref(null)
const productList = ref([])

onMounted(() => {
  store.getAllProducts()
  productList.value = store.products
})

const goDetail = function (productId) {
  router.push({ name: 'product_detail', params: { id: productId } })
}

const searchByBank = function () {
  productList.value = [];
  if (!query.value || query.value.trim() === '') {
    productList.value = store.products;
  } else {
    store.products.forEach(prod => {
      if (prod.kor_co_nm.includes(query.value)) {
        productList.value.push(prod);
      }
    })
  }
}
</script>

<style scoped>
.product-item {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-family: 'Inter', 'Noto Sans KR', sans-serif; /* Inter 폰트 적용 */
}

.product-item:hover {
  background-color: rgb(95, 245, 208);
}
</style>

```

1. 회원 가입
    1. store의 signUp 함수에서 유저명과 비밀번호를 django 서버에 전달하여 db에 저장. 그리고 로그인 페이지로 이동시킴

```jsx
// views.SignUpView
<template>
  <div>
    <h1>회원 가입</h1>
    <form @submit.prevent="signUp">
      <div>
        <label for="username">username : </label>
        <input type="text" v-model.trim="username" id="username">
      </div>
      <div>
        <label for="password1">password : </label>
        <input type="password" v-model.trim="password1" id="password1">
      </div>
      <div>
        <label for="password2">password confirm : </label>
        <input type="password" v-model.trim="password2" id="password2">
      </div>
      <div>
        <input type="submit">
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProductStore } from '@/stores/products'

const store = useProductStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }
  store.signUp(payload)
}

</script>

<style scoped>

</style>
```

```jsx
const signUp = function (payload) {
    const { username, password1, password2 } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2,
      }
    })
      .then(response => {
        console.log(response)
        const password = password1
        login({username, password})
      })
      .catch(error => {
        console.log(error)
      })
  }
```

1. 회원 정보 수정
    1. v-model을 활용하여 고객이 입력창에 입력하는 데이터가 즉시 email, 성, 이름에 반영되게 설정
    2. 수정된 고객 정보들을 stores의 updateUserProfile을 활용하여 patch 메서드를 통해 django db에 반영시킴. 계정 정보 변경을 위해 토큰이 필요
    3. patch 메서드를 통해 수정 시 수정된 정보가 return 됨을 확인. 해당 정보를 화면 상에 출력하기 위해 회원 프로필에 고객이 수정한 데이터를 전달.

```jsx
// views/ProfileUpdateView
<template>
  <div>
    <form @submit.prevent="updateUserProfile">
      <p>username : {{ store.userObj.username }}</p>

      <div>
        <label for="email">e-mail : </label>
        <input type="text" id='email' v-model="email">
      </div>
      <div>
        <label for="first_name">성 : </label>
        <input type="text" id='first_name' v-model="first_name">
      </div>
      <div>
        <label for="last_name">이름 : </label>
        <input type="text" id='last_name' v-model="last_name">
      </div>

      <input type='submit' value="수정">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useProductStore } from '../stores/products';

const store = useProductStore()

const email = ref(store.userObj.email)
const first_name = ref(store.userObj.first_name)
const last_name = ref(store.userObj.last_name)

const updateUserProfile = function () {
  const payload = {
    email: email.value,
    first_name: first_name.value,
    last_name: last_name.value
  }
  store.updateUserProfile(payload)
}

</script>

<style scoped>

</style>
```

```jsx
const updateUserProfile = function (payload) {
    const { email, first_name, last_name } = payload
    axios({
      method: 'patch',
      url: `${API_URL}/accounts/user/`,
      data: {
        email,
        first_name,
        last_name,
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        router.push({ name: 'profile', params: { id: userObj.value.username }})
      })
      .catch(error => {
        console.log(error)
      })
  }
```

1. 로그인 / 로그아웃
    1. 회원가입과 동작원리는 비슷하며, 회원명과 비밀번호를 입력받는다.
    2. 해당 회원명, 비밀번호를 login 함수에 전달하여 post method로 회원명과 비밀번호를 django 서버에 전달
    3. 전달 이후 token 값을 받아와서 저장한 뒤 stores의 getUserProfile 함수를 수행하여 유저 정보를 추출하는 작업 수행
    4.  정보 추출 이후 메인 화면으로 이동

<hr>

# 4일차

# 회원을 DB에 저장하고 수정

이 코드는 Django의 기본 사용자 모델을 확장하여 사용자 정의 모델을 만들고, **`CustomAccountAdapter`** 클래스를 사용하여 사용자 생성 및 저장을 수정합니다.

- **User 모델**: 이 모델은 Django의 내장 **`AbstractUser`** 모델을 확장하여 사용자 정의 모델을 만듭니다. 추가된 필드로는 닉네임, 나이, 자산, 월급, 그리고 금융 상품 리스트를 저장하는 **`financial_products`** 필드가 있습니다.
- **CustomAccountAdapter 클래스**: 이 클래스는 **`DefaultAccountAdapter`**를 상속하고, 사용자 생성과 관련된 동작을 수정합니다. **`save_user`** 메서드는 사용자를 저장하기 위해 필요한 정보를 처리합니다. 이 메서드는 사용자가 입력한 데이터를 받아서 사용자 객체의 필드에 할당하고, 새로운 사용자를 저장합니다. 여기서는 추가된 사용자 필드들을 사용하여 **`User`** 모델을 업데이트하고 저장합니다. 예를 들어, 입력된 금융 상품은 기존의 리스트에 추가됩니다.

이 코드는 사용자 모델을 확장하여 추가 필드를 가진 사용자 객체를 만들고, 사용자를 생성할 때 사용자의 추가 정보를 적절히 저장하는 데 사용됩니다

```python
# final_pjt_back/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

# # Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    # 리스트 데이터 저장을 위해 list 형태로 저장
    financial_products = models.JSONField(default=list)
    # superuser fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        # 참고하여 새로운 필드들을 작성해줍니다.
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        age = data.get("age")
        money = data.get("money")
        salary = data.get("salary")
        financial_product = data.get("financial_products")

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if age:
            user.age = age
        if money:
            user.money = money
        if salary:
            user.salary = salary
        if financial_product:
            financial_products = user.financial_products.split(',')
            financial_products.append(financial_product)
            if len(financial_products) > 1:
                financial_products = ','.join(financial_products)
            user_field(user, "financial_products", financial_products)
        
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        
        if commit:
        # Ability not to commit makes it easier to derive from
        # this adapter by adding
            user.save()
        return user
```

- **CustomRegisterSerializer**: 이 시리얼라이저는 **`dj_rest_auth`**의 **`RegisterSerializer`**를 상속받아 사용자 등록에 사용됩니다. 여기에 추가적인 필드들을 정의하여 사용자의 회원가입 시에 추가 정보를 받을 수 있도록 합니다. 즉, 사용자가 이메일, 비밀번호, 닉네임, 나이, 자산, 월급, 금융 상품 등을 입력할 수 있게끔 커스텀한 것입니다. **`get_cleaned_data`** 메서드는 입력된 데이터를 정제하여 반환하고, **`save`** 메서드는 새로운 사용자를 생성하고 저장합니다.
- **UserSerializer**: 이 시리얼라이저는 **`User`** 모델을 기반으로 합니다. 사용자 모델에서 비밀번호를 제외한 모든 필드 데이터를 직렬화합니다. 이 시리얼라이저는 주로 사용자 정보를 시리얼화하여 API 엔드포인트를 통해 데이터를 반환하는 데 사용됩니다.

기능적으로 보면, **`CustomRegisterSerializer`**는 사용자 등록을 관리하고, **`UserSerializer`**는 사용자 모델의 정보를 시리얼화하여 API로 전달할 수 있도록 합니다.

```python
# accounts/serializers.py

from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

class CustomRegisterSerializer(RegisterSerializer):
# 추가할 필드들을 정의합니다.
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    financial_products = serializers.ListField(child=serializers.IntegerField(), required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', ''),
            'money': self.validated_data.get('money', ''),
            'salary': self.validated_data.get('salary', ''),
            'financial_products': self.validated_data.get('financial_products', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )
```

1. **user_profile 함수**: 이 함수는 사용자 프로필을 가져오거나 수정하는 데 사용됩니다. **`GET`** 요청을 받으면 해당 사용자의 프로필 정보를 시리얼라이즈하여 반환하고, **`POST`** 요청을 받으면 전달된 데이터로 사용자 정보를 업데이트합니다.
2. **add_cart 함수**: 이 함수는 사용자의 장바구니에 상품을 추가하는 데 사용됩니다. **`POST`** 요청을 받아 사용자가 소유한 **`financial_products`** 리스트에 제품 ID를 추가합니다.
3. **delete_cart 함수**: 이 함수는 사용자의 장바구니에서 상품을 제거하는 데 사용됩니다. **`POST`** 요청을 받아 제품 ID를 사용자의 **`financial_products`** 리스트에서 제거합니다.

모든 함수에서 **`@api_view`** 및 **`@permission_classes`** 데코레이터를 사용하여 요청의 유효성을 검사하고, **`UserSerializer`**를 사용하여 사용자 정보를 시리얼라이즈하여 응답합니다. 이 코드는 인증된 사용자가 요청을 보내야하며, 해당 사용자의 프로필 정보를 가져오거나 수정하고, 장바구니에 제품을 추가하거나 제거할 수 있는 기능을 제공합니다.

```python
# accounts/views.py

from .models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.nickname = request.data.get('nickname')
        user.age = request.data.get('age')
        user.money = request.data.get('money')
        user.salary = request.data.get('salary')
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart(request):
    productId = request.data.get('productId')
    user = request.user
    if user.financial_products is None:
        user.financial_products = []
        
    if productId not in user.financial_products:
        user.financial_products.append(productId)
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    productId = request.data.get('productId')
    user = request.user
    if user.financial_products is None:
        user.financial_products = []
        
    if productId in user.financial_products:
        user.financial_products.remove(productId)
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)
```

1. updateUserProfile**함수**: 이 함수는 사용자의 개인정보를 편집할 때 활용되는 함수이다. username(각 사용자의 id)을 기준으로 db에서 데이터를 불러온다.

```jsx
<script setup>
import { ref } from 'vue';
import { useProductStore } from '../stores/products';
import { useRoute } from 'vue-router';

const store = useProductStore()
const route = useRoute()

const email = ref(store.userObj.email)
const first_name = ref(store.userObj.first_name)
const last_name = ref(store.userObj.last_name)
const nickname = ref(store.userObj.nickname)
const age = ref(store.userObj.age)
const money = ref(store.userObj.money)
const salary = ref(store.userObj.salary)

const updateUserProfile = function () {
  const payload = {
    username: route.params.id,
    email: email.value,
    first_name: first_name.value,
    last_name: last_name.value,
    nickname: nickname.value,
    age: age.value,
    money: money.value,
    salary: salary.value
  }
  store.updateUserProfile(payload)
}
```

```jsx
const updateUserProfile = function (payload) {
    const { username, email, first_name, last_name, nickname, age, money, salary } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/${username}/`,
      data: {
        username, email, first_name, last_name, nickname, age, money, salary
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        router.push({ name: 'profile', params: { id: userObj.value.username }})
      })
      .catch(error => {
        console.log(error)
      })
  }
```

# 상품 찜해놓기/ 제거하기

1. **addCart 함수** : 이 함수는 고객 객체의 financial_products 리스트에 예적금 상품들을 추가합니다.  **`POST`** 요청을 받아 사용자가 소유한 **`financial_products`** 리스트에 제품 ID를 추가합니다.
2. **deleteCart 함수**: 이 함수는 사용자의 장바구니에서 상품을 제거하는 데 사용됩니다. **`POST`** 요청을 받아 사용자가 소유한 **`financial_products`** 리스트에서 제품 ID를 제거합니다.

```jsx
// final-pjt-front/views/ProductDetailView.vue

<script setup>
import { computed } from 'vue'
import { useProductStore } from '../stores/products';
import { useRoute } from 'vue-router';

const route = useRoute()
const store = useProductStore()
const product = store.getProductById(Number(route.params.id))
const isJoin = computed (() => {
  return store.userObj.financial_products.indexOf(product.id) != -1
})

const addCart = function () {
  store.addCart(Number(route.params.id))
}

const deleteCart = function () {
  store.deleteCart(Number(route.params.id))
}
</script>
```

```jsx
const addCart = function (productId) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/add_cart/`,
      data: {
        productId,
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        console.log(userObj.value.financial_products)
      })
      .catch(error => {
        console.log(error)
      })
  }

  const deleteCart = function (productId) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/delete_cart/`,
      data: {
        productId,
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        console.log(response)
      })
      .catch(error => {
        console.log(error)
      })
  }
```

# 가입 상품과 회원 정보 출력

1. **회원 정보 섹션**: 사용자의 기본 정보(아이디, 이메일, 이름, 닉네임, 나이, 자산, 월급)를 보여줍니다. 이메일이 비어있을 경우 "이메일을 입력해 주세요"라는 안내문이 표시됩니다. 사용자 정보 수정을 위한 버튼도 있어요.
2. **가입한 상품 목록 섹션**: 사용자가 가입한 상품 목록을 표시합니다. 이 부분은 **`joined-product`** 클래스로 스타일링되어 있고, 가입한 상품을 반복문을 통해 나열하고 있습니다.
3. **Vue 코드**: **`vue-router`**를 사용하여 다른 페이지로 이동하는 기능이 있습니다. **`goRecommend`** 함수는 추천 상품 페이지로 이동하고, **`goUserUpdate`** 함수는 회원 정보 수정 페이지로 이동합니다. 또한, 사용자의 장바구니에 있는 상품 목록을 가져와서 표시하는 로직이 있네요.
4. **CSS**: 스타일링 부분으로, **`container`**, **`button-group`**, **`btn`**, **`user-info`**, **`empty-email`**, **`update-button`**, **`joined-product`** 등의 클래스들을 사용하여 디자인을 정의하고 있습니다.

이 코드는 사용자의 정보를 보여주는 페이지로 보이는데, 회원 정보를 수정하거나 다른 기능을 제공하는 페이지인 것 같습니다.

<hr>

# 5일차

## 1. 상품 추천 알고리즘 구현

```jsx
// views/RecommendView.vue

<template>
  <div class="container">
    <div class="button-group">
      <a class="btn btn-primary" role="button" @click="goProfile">회원 정보</a>
      <a class="btn btn-disabled" role="button">추천 상품</a>
    </div>

    <h1>추천 상품 리스트</h1>
    <form @submit.prevent="getFilter" class="filter-form">
      <div class="radio-group">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest1" value="단리" v-model="interest">
          <label class="form-check-label" for="interest1">단리</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest2" value="복리" v-model="interest">
          <label class="form-check-label" for="interest2">복리</label>
        </div>
        <!-- <label><input type="radio" name="interest" value="단리" v-model="interest"> 단리</label>
        <label><input type="radio" name="interest" value="복리" v-model="interest"> 복리</label> -->
      </div>
      <div class="radio-group">
        <!-- <label><input type="radio" name="month" value="6" v-model="month"> 6개월</label>
        <label><input type="radio" name="month" value="12" v-model="month"> 12개월</label>
        <label><input type="radio" name="month" value="24" v-model="month"> 24개월</label>
        <label><input type="radio" name="month" value="36" v-model="month"> 36개월</label> -->
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month6" value="6" v-model="month">
          <label class="form-check-label" for="month6">6개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month12" value="12" v-model="month">
          <label class="form-check-label" for="month12">12개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month24" value="24" v-model="month">
          <label class="form-check-label" for="month24">24개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month36" value="36" v-model="month">
          <label class="form-check-label" for="month36">36개월</label>
        </div>
      </div>
      <button type="submit" class="btn-submit">Submit</button>
    </form>

    <ul class="list-group">
      <li class="list-group-item product-item" v-for="product in recommendList" :key="product.id" @click="goDetail(product.id)">
        <div class="product-info">
          <h3 class="bank-name">{{ product.kor_co_nm }}</h3>
          <p class="product-name">{{ product.fin_prdt_nm }}</p>
          <div class="details">
            <p class="detail">가입방법: {{ product.join_way }}</p>
            <!-- <p class="detail">참고사항: {{ product.etc_note }}</p>
            <p class="detail">특혜: {{ product.spcl_cnd }}</p>
            <p class="detail">가입 대상: {{ product.join_member }}</p> -->
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProductStore } from '../stores/products'
import { useRoute, useRouter } from 'vue-router';

const store = useProductStore()
const router = useRouter()
const route = useRoute()
const recommendList = ref([])

// 추천을 위해 사용할 값들
const interest = ref('')
const month = ref(0)

const goProfile = function () {
  router.push({ name: 'profile', params: {id: route.params.id } })
}

// 상품의 가입 제한 나이 범위 구하기
const getAgeInterval = function (product) {
  const str = product.join_member // 가입 제한
  const join_member = str.split(' ').join('') // 띄어쓰기 제거
  
  let minAge = 0
  let maxAge = 1000
  const len = join_member.length
  for(let i = 0; i < len; i++) {
    if(join_member[i] === '세') {
      if(i-1 >= 0 && 48 <= join_member[i-1].charCodeAt() && join_member[i-1].charCodeAt() <= 57) {
        let age = 0
        age += (i-2 >= 0 && 48 <= join_member[i-2].charCodeAt() && join_member[i-2].charCodeAt() <= 57) ? (join_member[i-2].charCodeAt()-48)*10 : 0
        age += join_member[i-1].charCodeAt()-48

        if(i+3 <= len && join_member.substring(i+1, i+3) === '이상') minAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '초과') minAge = age+1
        if(i+3 <= len && join_member.substring(i+1, i+3) === '이하') maxAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '미만') maxAge = age-1
        if(i+1 < len && join_member[i+1] === '~') minAge = age
        if(i-4 >= 0 && join_member.substring(i-4, i-1).indexOf('~') != -1) maxAge = age
      }
    }
  }

  return [minAge, maxAge]
}

// 상품들의 가입 제한 범위를 구해서 리스트에 모으기
const getAgeIntervalList = function () {
  const ret = [] // 반환할 배열
  for(let i = 0; i < store.products.length; i++) {
    const ageInterval = getAgeInterval(store.products[i]) // 나이 범위 추출
    ret.push(store.products[i].join_member, `${ageInterval[0]}~${ageInterval[1]}`) // 배열에 저장
    console.log(store.products[i].join_member + ' | ' + `${ageInterval[0]}~${ageInterval[1]}`) // 확인을 위해 콘솔에 출력
  }
}

const getFilter = function () {
  const filteredOptionList = []
  console.log(store.options)
  for(let i = 0; i < store.options.length; i++) {
    if(store.options[i].intr_rate_type_nm === interest.value && store.options[i].save_trm == month.value) {
      filteredOptionList.push({
        intr_rate: store.options[i].intr_rate,
        fin_prdt_cd: store.options[i].fin_prdt_cd,
      })
    }
  }

  filteredOptionList.sort(function(a, b) {
    return -a.intr_rate < -b.intr_rate
  })

  console.log(filteredOptionList)

  recommendList.value = []
  filteredOptionList.forEach(op => {
    if(recommendList.value.length < 10) {
      for(let i = 0; i < store.products.length; i++) {
        if(op.fin_prdt_cd === store.products[i].fin_prdt_cd) {
          const ageInterval = getAgeInterval(store.products[i])
          if(ageInterval[0] <= store.userObj.age && store.userObj.age <= ageInterval[1]) {
            recommendList.value.push(store.products[i])
          }
          break
        }
      }
    }
  })

  console.log(recommendList.value)
}

onMounted(() => {
  recommendList.value = []
  store.products.forEach(prod => {
    const ageInterval = getAgeInterval(prod)
    if(ageInterval[0] <= store.userObj.age && store.userObj.age <= ageInterval[1]) {
      recommendList.value.push(prod)
    }
  })
})

const goDetail = function (productId) {
  router.push({ name: 'product_detail', params: { id: productId } })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.btn {
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

/* 나머지 스타일은 그대로 유지 */

.filter-form {
  margin-bottom: 20px;
  margin-bottom: 40px;
  max-width: 800px;
  margin: 20px auto; /* 화면 중앙에 위치하도록 수정 */
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.radio-group {
  margin-bottom: 10px;

}

.btn-submit {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.product-item {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-family: 'Inter', 'Noto Sans KR', sans-serif;
}

.product-item:hover {
  background-color: rgb(95, 245, 208);
}

.radio-group {
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

.container {
  margin-left: 15px;
  margin-right: 15px;
}

.product-item {
  cursor: pointer;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  transition: background-color 0.3s;
}

.product-item:hover {
  background-color: rgb(95, 245, 208);
}

.product-info {
  color: #333;
}

.bank-name {
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 10px;
  font-family: 'Nanum Gothic', sans-serif;
}

.product-name {
  font-size: 18px;
  margin-bottom: 10px;
  font-family: 'Nanum Gothic', sans-serif;
}

.details {
  font-size: 16px;
}

.detail {
  margin-bottom: 5px;
  font-family: 'Nanum Gothic', sans-serif;
}

.query {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.btn-outline-secondary {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
</style>
```

### 1. 나이 기준 기본 필터링

1. 구현 방식: 로그인한 사람의 나이를 기준으로 가입 가능한 상품들을 기본적으로 필터링. getAgeInterval 함수에서 가입 제한 데이터를 통째로 가져옴. 
2. 모든 데이터에서 나이 뒤에‘세’라는 텍스트가 붙는 규칙을 발견. 
3. 모든 데이터에서 여백을 제거한 뒤 세를 발견 시, 세 앞의 두 개의 텍스트를 감지하는데, 해당 과정에서 charCodeAt()으로 나이에 해당하는 텍스트를 아스키 코드값으로 변환하여 아스키 코드표 내에서 0 ~9사이의 값들 사이에 있는지 판단. 성공 시 각 인덱스에 해당하는 숫자에 자릿수만큼 곱해주어 나이를 age에 추출.
4. 나이를 추출한 뒤 정확한 가입 범위를 판단하기 위해 이상, 초과, 이하, 미만이 포함되는 경우를 판단. substring 메서드로 가입 제한 데이터에서 이상, 초과, 이하, 미만이 포함되어있는지 판단. age 뒤에 이상 초과가 존재할 경우 추출한 age를 minAge로 설정, age 뒤에 이하, 미만이 존재할 경우 추출한 age를 maxAge로 설정한다.

```jsx
// views/RecommendView.vue

const getAgeInterval = function (product) {
  const str = product.join_member // 가입 제한
  const join_member = str.split(' ').join('') // 띄어쓰기 제거
  
  let minAge = 0
  let maxAge = 1000
  const len = join_member.length
  for(let i = 0; i < len; i++) {
    if(join_member[i] === '세') {
      if(i-1 >= 0 && 48 <= join_member[i-1].charCodeAt() && join_member[i-1].charCodeAt() <= 57) {
        let age = 0
        age += (i-2 >= 0 && 48 <= join_member[i-2].charCodeAt() && join_member[i-2].charCodeAt() <= 57) ? (join_member[i-2].charCodeAt()-48)*10 : 0
        age += join_member[i-1].charCodeAt()-48

        if(i+3 <= len && join_member.substring(i+1, i+3) === '이상') minAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '초과') minAge = age+1
        if(i+3 <= len && join_member.substring(i+1, i+3) === '이하') maxAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '미만') maxAge = age-1
        if(i+1 < len && join_member[i+1] === '~') minAge = age
        if(i-4 >= 0 && join_member.substring(i-4, i-1).indexOf('~') != -1) maxAge = age
      }
    }
  }

  return [minAge, maxAge]
}

// 상품들의 가입 제한 범위를 구해서 리스트에 모으기
const getAgeIntervalList = function () {
  const ret = [] // 반환할 배열
  for(let i = 0; i < store.products.length; i++) {
    const ageInterval = getAgeInterval(store.products[i]) // 나이 범위 추출
    ret.push(store.products[i].join_member, `${ageInterval[0]}~${ageInterval[1]}`) // 배열에 저장
    console.log(store.products[i].join_member + ' | ' + `${ageInterval[0]}~${ageInterval[1]}`) // 확인을 위해 콘솔에 출력
  }
}
```

### 2. 저축 이율과 가입 기간을 기준으로 필터링

1. 저축 이율과 가입 기간을 하나씩 선택할 수 있는 라디오버튼 그룹을 2개 생성.
2. v-model을 활용하여 상품의 데이터에서 추출한 저축 이율(store.options[i].intr_rate_type_nm)과 가입 기간(store.options[i].save_trm)을 라디오 버튼의 각 value와 비교하여, 같은 경우에만 필터링하여 화면에 표시

```jsx
// views/RecommendView.vue

<form @submit.prevent="getFilter" class="filter-form">
      <div class="radio-group">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest1" value="단리" v-model="interest">
          <label class="form-check-label" for="interest1">단리</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest2" value="복리" v-model="interest">
          <label class="form-check-label" for="interest2">복리</label>
        </div>
        <!-- <label><input type="radio" name="interest" value="단리" v-model="interest"> 단리</label>
        <label><input type="radio" name="interest" value="복리" v-model="interest"> 복리</label> -->
      </div>
      <div class="radio-group">
        <!-- <label><input type="radio" name="month" value="6" v-model="month"> 6개월</label>
        <label><input type="radio" name="month" value="12" v-model="month"> 12개월</label>
        <label><input type="radio" name="month" value="24" v-model="month"> 24개월</label>
        <label><input type="radio" name="month" value="36" v-model="month"> 36개월</label> -->
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month6" value="6" v-model="month">
          <label class="form-check-label" for="month6">6개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month12" value="12" v-model="month">
          <label class="form-check-label" for="month12">12개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month24" value="24" v-model="month">
          <label class="form-check-label" for="month24">24개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month36" value="36" v-model="month">
          <label class="form-check-label" for="month36">36개월</label>
        </div>
      </div>
      <button type="submit" class="btn-submit">Submit</button>
    </form>
```

```jsx
// views/RecommendView.vue

const getFilter = function () {
  const filteredOptionList = []
  console.log(store.options)
  for(let i = 0; i < store.options.length; i++) {
    if(store.options[i].intr_rate_type_nm === interest.value && store.options[i].save_trm == month.value) {
      filteredOptionList.push({
        intr_rate: store.options[i].intr_rate,
        fin_prdt_cd: store.options[i].fin_prdt_cd,
      })
    }
  }

  filteredOptionList.sort(function(a, b) {
    return -a.intr_rate < -b.intr_rate
  })

  console.log(filteredOptionList)

  recommendList.value = []
  filteredOptionList.forEach(op => {
    if(recommendList.value.length < 10) {
      for(let i = 0; i < store.products.length; i++) {
        if(op.fin_prdt_cd === store.products[i].fin_prdt_cd) {
          const ageInterval = getAgeInterval(store.products[i])
          if(ageInterval[0] <= store.userObj.age && store.userObj.age <= ageInterval[1]) {
            recommendList.value.push(store.products[i])
          }
          break
        }
      }
    }
  })

  console.log(recommendList.value)
}
```

## 2. UI 개선

1. 로그인 아이디, 비밀번호에 필요한 정보를 찾지 못할 시 alert를 활용하여 알림창 표시

```jsx
// stores/products.js

// 로그인
  const login = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/dj_rest_auth/login/`,
      data: {
        username, password,
      }
    })
      .then(response => {
        console.log(response.data)
        token.value = response.data.key
        client_name.value = username
        console.log(client_name.value)
        getUserProfile()
        getAllProducts()
        getAllOptions()
        router.push({ name: 'main' })
      })
      .catch(error => {
        window.alert('아이디와 비밀번호를 확인해주세요.')
        console.log(error)
      })
  }
```

1. 배경화면 설정
    1. 최상위 노드에서 background-image를 활용하여 배경화면을 설정하여 사용자 경험 개선. background-attachment: fixed 를 통해 배경화면이 스크롤에 상관없이 항상 고정됨

<hr>

# 6일차

## 1. 메인 페이지 작성

### final_pjt_front(vue)

- 로그인, 상품상세정보, 전체상품정보, 고객정보, 상품추천, 회원가입을 위한 함수를 작성하기 위해 view 생성
- 해당 view들을 모두 router에 추가
- 상품 정보를 활용하기 위한 product 컴포넌트 생성
- django내에서 예/적금 상품 데이터 GET을 위해 axios를 활용

### final_pjt_back(django)

- bank_api프로젝트 생성
- 고객의 계정 정보를 활용할 accounts app 생성
- 예/적금 상품정보를 활용할 products app 생성

---

## 2. 회원 관련 기능 구현

### 가입 기능

- back내의 bank_api url에서 유저들의 회원가입을 위한 url 작성. 해당 url 내에서 회원가입 진행 후 로그인 진행 시 drf로부터 토큰이 발급됨
- front의 SignUpView 내에서 유저명과 비밀번호를 django 서버에 전달하여 db에 저장. 그리고 로그인 페이지로 이동시킴

### 수정 기능

- v-model을 활용하여 고객이 입력창에 입력하는 데이터가 즉시 email, 성, 이름에 반영되게 설정
- 수정된 고객 정보들을 stores의 updateUserProfile을 활용하여 patch 메서드를 통해 django db에 반영시킴. 계정 정보 변경을 위해 토큰이 필요
- patch 메서드를 통해 수정 시 수정된 정보가 return 됨을 확인. 해당 정보를 화면 상에 출력하기 위해 회원 프로필에 고객이 수정한 데이터를 전달
- updateUserProfile**함수**: 이 함수는 사용자의 개인정보를 편집할 때 활용되는 함수이다. username(각 사용자의 id)을 기준으로 db에서 데이터를 불러온다.

### 로그인 / 로그아웃

- 회원가입과 동작원리는 비슷하며, 회원명과 비밀번호를 입력받는다.
- 해당 회원명, 비밀번호를 login 함수에 전달하여 post method로 회원명과 비밀번호를 django 서버에 전달
- 전달 이후 token 값을 받아와서 저장한 뒤 stores의 getUserProfile 함수를 수행하여 유저 정보를 추출하는 작업 수행
- 정보 추출 이후 메인 화면으로 이동

### ui

- 각 제품에 마우스를 갖다댈 시 색이 변하게 스타일 변경(product-item:hover)
- navbar 구현

---

## 3. 회원 정보 저장 및 수정

### 회원을 DB에 저장하고 수정

- 이 코드는 Django의 기본 사용자 모델을 확장하여 사용자 정의 모델을 만들고, **`CustomAccountAdapter`** 클래스를 사용하여 사용자 생성 및 저장을 수정합니다.

- **User 모델**: 이 모델은 Django의 내장 **`AbstractUser`** 모델을 확장하여 사용자 정의 모델을 만듭니다. 추가된 필드로는 닉네임, 나이, 자산, 월급, 그리고 금융 상품 리스트를 저장하는 **`financial_products`** 필드가 있습니다.

- **CustomAccountAdapter 클래스**: 이 클래스는 **`DefaultAccountAdapter`**를 상속하고, 사용자 생성과 관련된 동작을 수정합니다. **`save_user`** 메서드는 사용자를 저장하기 위해 필요한 정보를 처리합니다. 이 메서드는 사용자가 입력한 데이터를 받아서 사용자 객체의 필드에 할당하고, 새로운 사용자를 저장합니다. 여기서는 추가된 사용자 필드들을 사용하여 **`User`** 모델을 업데이트하고 저장합니다. 예를 들어, 입력된 금융 상품은 기존의 리스트에 추가됩니다.

이 코드는 사용자 모델을 확장하여 추가 필드를 가진 사용자 객체를 만들고, 사용자를 생성할 때 사용자의 추가 정보를 적절히 저장하는 데 사용됩니다

### 유저 데이터 직렬화

- **CustomRegisterSerializer**: 이 시리얼라이저는 **`dj_rest_auth`**의 **`RegisterSerializer`**를 상속받아 사용자 등록에 사용됩니다. 여기에 추가적인 필드들을 정의하여 사용자의 회원가입 시에 추가 정보를 받을 수 있도록 합니다. 즉, 사용자가 이메일, 비밀번호, 닉네임, 나이, 자산, 월급, 금융 상품 등을 입력할 수 있게끔 커스텀한 것입니다. **`get_cleaned_data`** 메서드는 입력된 데이터를 정제하여 반환하고, **`save`** 메서드는 새로운 사용자를 생성하고 저장합니다.
- **UserSerializer**: 이 시리얼라이저는 **`User`** 모델을 기반으로 합니다. 사용자 모델에서 비밀번호를 제외한 모든 필드 데이터를 직렬화합니다. 이 시리얼라이저는 주로 사용자 정보를 시리얼화하여 API 엔드포인트를 통해 데이터를 반환하는 데 사용됩니다.

### 유저의 관심 목록 추가/삭제

- **user_profile 함수**: 이 함수는 사용자 프로필을 가져오거나 수정하는 데 사용됩니다. **`GET`** 요청을 받으면 해당 사용자의 프로필 정보를 직렬화하여 반환하고, **`POST`** 요청을 받으면 전달된 데이터로 사용자 정보를 업데이트합니다.
- **add_cart 함수**: 이 함수는 사용자의 장바구니에 상품을 추가하는 데 사용됩니다. **`POST`** 요청을 받아 사용자가 소유한 **`financial_products`** 리스트에 제품 ID를 추가합니다.
- **delete_cart 함수**: 이 함수는 사용자의 장바구니에서 상품을 제거하는 데 사용됩니다. **`POST`** 요청을 받아 제품 ID를 사용자의 **`financial_products`** 리스트에서 제거합니다.

모든 함수에서 **`@api_view`** 및 **`@permission_classes`** 데코레이터를 사용하여 요청의 유효성을 검사하고, **`UserSerializer`**를 사용하여 사용자 정보를 시리얼라이즈하여 응답합니다. 이 코드는 인증된 사용자가 요청을 보내야하며, 해당 사용자의 프로필 정보를 가져오거나 수정하고, 장바구니에 제품을 추가하거나 제거할 수 있는 기능을 제공합니다.

### 가입 상품과 회원 정보 출력

이 코드는 사용자의 정보를 보여주는 페이지로 보이는데, 회원 정보를 수정하거나 가입한 상품을 확인하는 기능을 제공하는 페이지입니다.

- **회원 정보 섹션**: 사용자의 기본 정보(아이디, 이메일, 이름, 닉네임, 나이, 자산, 월급)를 보여줍니다. 이메일이 비어있을 경우 "이메일을 입력해 주세요"라는 안내문이 표시됩니다. 사용자 정보 수정을 위한 버튼도 있어요.
1. **가입한 상품 목록 섹션**: 사용자가 가입한 상품 목록을 표시합니다. 이 부분은 **`joined-product`** 클래스로 스타일링되어 있고, 가입한 상품을 반복문을 통해 나열하고 있습니다.
2. **Vue 코드**: **`vue-router`**를 사용하여 다른 페이지로 이동하는 기능이 있습니다. **`goRecommend`** 함수는 추천 상품 페이지로 이동하고, **`goUserUpdate`** 함수는 회원 정보 수정 페이지로 이동합니다. 또한, joinProductsList computed 함수에서 사용자의 장바구니에 있는 상품 목록과 전체 상품 목록의 id를 대조하여 일치할 시 가져와서 표시합니다.
3. **CSS**: 스타일링 부분으로, **`container`**, **`button-group`**, **`btn`**, **`user-info`**, **`empty-email`**, **`update-button`**, **`joined-product`** 등의 클래스들을 사용하여 디자인을 정의하고 있습니다.

---

## 4. 상품 추천 알고리즘

### 1. 나이 기준 기본 필터링

1. 구현 방식: 로그인한 사람의 나이를 기준으로 가입 가능한 상품들을 기본적으로 필터링. getAgeInterval 함수에서 가입 제한 데이터를 통째로 가져옴. 
2. 모든 데이터에서 나이 뒤에‘세’라는 텍스트가 붙는 규칙을 발견. 
3. 모든 데이터에서 여백을 제거한 뒤 세를 발견 시, 세 앞의 두 개의 텍스트를 감지하는데, 해당 과정에서 charCodeAt()으로 나이에 해당하는 텍스트를 아스키 코드값으로 변환하여 아스키 코드표 내에서 0 ~9사이의 값들 사이에 있는지 판단. 성공 시 각 인덱스에 해당하는 숫자에 자릿수만큼 곱해주어 나이를 age에 추출.
4. 나이를 추출한 뒤 정확한 가입 범위를 판단하기 위해 이상, 초과, 이하, 미만이 포함되는 경우를 판단. substring 메서드로 가입 제한 데이터에서 이상, 초과, 이하, 미만이 포함되어있는지 판단. age 뒤에 이상 초과가 존재할 경우 추출한 age를 minAge로 설정, age 뒤에 이하, 미만이 존재할 경우 추출한 age를 maxAge로 설정한다.

### 2. 저축 이율과 가입 기간을 기준으로 필터링

1. 저축 이율과 가입 기간을 하나씩 선택할 수 있는 라디오버튼 그룹을 2개 생성.
2. v-model을 활용하여 상품의 데이터에서 추출한 저축 이율(store.options[i].intr_rate_type_nm)과 가입 기간(store.options[i].save_trm)을 라디오 버튼의 각 value와 비교하여, 같은 경우에만 필터링하여 화면에 표시

### 유저의 관심 목록 추가/삭제

- **user_profile 함수**: 이 함수는 사용자 프로필을 가져오거나 수정하는 데 사용됩니다. **`GET`** 요청을 받으면 해당 사용자의 프로필 정보를 직렬화하여 반환하고, **`POST`** 요청을 받으면 전달된 데이터로 사용자 정보를 업데이트합니다.
- **add_cart 함수**: 이 함수는 사용자의 장바구니에 상품을 추가하는 데 사용됩니다. **`POST`** 요청을 받아 사용자가 소유한 **`financial_products`** 리스트에 제품 ID를 추가합니다.
- **delete_cart 함수**: 이 함수는 사용자의 장바구니에서 상품을 제거하는 데 사용됩니다. **`POST`** 요청을 받아 제품 ID를 사용자의 **`financial_products`** 리스트에서 제거합니다.

모든 함수에서 **`@api_view`** 및 **`@permission_classes`** 데코레이터를 사용하여 요청의 유효성을 검사하고, **`UserSerializer`**를 사용하여 사용자 정보를 시리얼라이즈하여 응답합니다. 이 코드는 인증된 사용자가 요청을 보내야하며, 해당 사용자의 프로필 정보를 가져오거나 수정하고, 장바구니에 제품을 추가하거나 제거할 수 있는 기능을 제공합니다.

### UI 개선

- 로그인 아이디, 비밀번호에 필요한 정보를 찾지 못할 시 alert를 활용하여 알림창 표시
- 배경화면 설정
    1. 최상위 노드에서 background-image를 활용하여 배경화면을 설정하여 사용자 경험 개선. background-attachment: fixed 를 통해 배경화면이 스크롤에 상관없이 항상 고정됨