# 유튜브 동영상 검색 관리 서비스 구현


## 1. 각 기능들을 구현하기 위한 view의 생성
- ChannelView : 선호하는 채널들의 리스트
- DetailView : 비디오 데이터를 youtube API키를 활용하여 동영상의 정보 추출, 동영상의 저장 및 저장 취소 기능 구현, 선호 채널 저장 구현
- HomeView : 기본 스타일
- LaterView : 나중에 볼 동영상들의 리스트
- SearchView : 비디오의 검색 및 axios를 활용한 상세페이지로의 비디오 데이터push

## 2. view들을 router, app.vue에 추가

## 3. 유튜브 동영상 홈 구현(SearchView)
  1. 유튜브 영상의 검색 
  input에서 검색 시 youtube_api_v3를 활용하여 youtube의 영상들을 클론 검색할 수 있는 웹사이트의 구현.
  - 위의 api를 활용하여 youtube의 영상 데이터를 input에 검색한 그대로 가져올 수 있었다. axios와 융합하여 get 메서드로 객체의 형태를 파악하여 필요한 데이터를 추출하였다.

  2. 검색한 영상의 push
  검색한 영상을 router를 활용하여 영상 상세페이지로 이동하는 함수를 구현

## 4. 영상 상세 페이지
  1. 영상의 정보 받아오기 
  searchview에서 건네받은 videoID를 활용하여 웹페이지 상에서 들어오는 객체의 구조를 다시 확인하여 상세정보를 출력하기 위해 임시로 저장할 currentVideo 변수를 선언. 해당 비디오의 상세정보(video)를 받은 뒤 동영상을 저장하기 위해 **saveVideoList**를 활용하여 json형태로 파싱

    - saveVideoList : 로컬 스토리지에 저장된 비디오의 정보
    - currentVideo : 현재 검색한 비디오의 정보

  2. 영상의 정보를 토대로 나중에 볼 영상들을 저장  

  - saveVideoList 내에서 video가 이미 저장된 경우(currentVideo, saveVideoList의 id를 대조),
  - saveVideoList의 길이가 0이 초과인 경우
  => 해당 상태를 isSave로 판단
  => 버튼의 text를 저장 취소 상태로 set(이미 나중에 볼 영상에 저장된 경우이므로)
  => 반대의 경우 동영상 저장 상태로 set

  - saveVideoList 내에서 video가 이미 저장된 경우(currentVideo, saveVideoList의 id를 대조),
  - saveVideoList의 길이가 0이 초과인 경우
  => 버튼의 text를 저장 취소 상태로 set

  addVideo 함수를 구현하여 동영상을 추가로 저장하는 함수를 구현
  - 비디오 리스트에 현재 비디오의 정보를 push() 메서드를 이용하여 추가.
  - 로컬 스토리지 내의 데이터를 json 데이터로 저장
  - isSave 상태를 true로 변환

  removeVideo 함수를 구현하여 동영상을 삭제하는 함수를 구현
  - 로컬 스토리지 내에서 데이터를 가져와 파싱한 뒤 videoIdx로 현재 비디오의 id와 로컬 내의 비디오의 id를 저장.
  - 로컬 스토리지에서 splice()메서드를 활용하여 삭제
  - 로컬 스토리지 내의 데이터를 setItem을 활용하여 다시 설정
  - isSave의 상태를 false로 전환

  3. 영상의 정보를 토대로 선호하는 채널들을 저장
    addChannel을 활용하여 선호하는 채널들을 저장
    - 현재 검색한 채널의 데이터 중 채널 정보(channelTitle)를 포함하고 있는 객체를 가져와서 saveChannelList에 push(append 개념)

  4. LaterView 와 ChannelView에서 나중에 볼 동영상 및 선호 채널을 출력
    1) LaterView 내에서 saveVideo 변수에 localStorage내에 저장된 데이터들을 json형태로 파싱하고 할당하여 데이터들을 그대로 출력

    2) ChannelView 내에서 saveChannelList 변수에 localStorage내에 저장된 데이터들을 json형태로 파싱하고 할당하여 데이터들을 그대로 출력