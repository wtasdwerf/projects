# 03_pjt

<br>

## 웹 페이지의 구성

```css
/* navbar */
.navbar {
  position: fixed;
  top :0;
  left :0;
  right :0;
  justify-content: space-between;
  }

.navbar img {
  height: 50px;
  width: 120px;
  object-fit:fill;
}

.navbar-nav {
  display: flex;
  align-items: end;
}

.collapse{
  justify-content: end;
}
```
1. navbar의 구현
> 네비게이션 바를 구현하면서 가장 까다로웠던 점은 요소들의 정렬과 이미지의 크기 맞춤 삽입이였다.
> 요소의 우측 정렬은 navbar-nav 클래스 내에서 **align-items**를 end로 설정하여 해결하였고,  
> 이미지의 크기 맞춤 삽입은 크기를 직접 조정해준 뒤, **object-fill**을 fill로 채워 해결하였다.  

<br><br>

```css
/* header */
@media screen and (min-width: 1400px) {
  .header{
    display: flex;
    top: 0;
    align-items: center;
    justify-content: center;
  }

  .carousel{
    width: 1320px;
  }
}
```

1. header
> 헤더에서는 carousel을 활용했는데, 이미지들을 넣어주고 미디어쿼리를 활용하여 너비가 1400px 이상이 될때 헤더 클래스의 display를 flex로 설정하고 top을 0으로 설정하여 위에 여백이 없게 했고, 그리고 **align-items**와 **justify-content**를 center로 설정하여 사진들이 천장에 붙은 채로 중앙에 나타나게 구현했다. 그리고 carousel 클래스를 너비를 1320으로 고정시켰다.

<br>

2. section
  
```css
    .text-center{
    padding-top: 5%;
    padding-bottom:5%;
    }

    .section {
    display : flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-bottom:5%;
    }

    .sectioncontainer {
    width: 70%;
    height:70%;
    }

```

> section 부분은 제목에 padding을 주어 위와 아래 간격을 화면 비율에 비례하게 주었고, section의 display를 flex로 설정하고 축을 90도 회전시켜 세로로 정렬시켰다. 

3. main

```css
.main {
  display : flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-body {
  width: 100%;
}

.aside {
  padding-top:5%;
  display : flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-bottom:5%;
  width: 100%;
}

.row {
  width: 100%;
  display : flex;
  align-items: center;
  justify-content: center;
}

.list-group {
  width: 100%;
  height: 15%;
}
```
> section 부분은 제목에 padding을 주어 위와 아래 간격을 화면 비율에 비례하게 주었고, section의 display를 flex로 설정하고 축을 90도 회전시켜 세로로 정렬시켰다. 그리고 화면의 크기에 따라 col을 다르게 설정하였다.

<br></br>

4. community
> 이 부분은 자력으로 해결하지 못해 아쉬웠다.
> 카드 그리드를 활용하여 해결하려 하였으나 
> 화면상에 보이지 않게 설정하는 **d-none**의 존재를 
> 몰라 많이 당황스러웠다. d-none, d-flex, d-lg-none 등 내가 전혀 사용하지 않았던 표현들이 나와서 아마 고민했어도 시간이 많이 오래 걸렸거나 해결하지 못했을거라 생각하여 프로님의 답안을 참조하여 이해하였다.

<br></br>

5. footer
> 이 부분은 fixed-bottom을 활용하여 화면 최하단에 고정시켰고, display를 flex 설정하고 justify content 와 align items 를 활용하여 중앙에 텍스트를 위치시켰다.