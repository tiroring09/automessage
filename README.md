# 쇼피 메세지 자동화

[TOC]

## 사용법
### 1. 설치할 프로그램 목록
1. [python3.8](https://www.python.org/downloads/) `Windows x86-64 executable installer`

	설치시 `add python to path`에 체크하는게 편한 것 같다
2. [tesseract for window](https://github.com/UB-Mannheim/tesseract/wiki) `tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe`
3. [chrimedriver](https://chromedriver.chromium.org/downloads)

	로컬에 설치된 크롬버전과 맞아야 하는 것 같다.
4. [git](https://git-scm.com/) for windows

	소스코드 버전관리 목적
5. [vscode](https://code.visualstudio.com/)

	소스코드 편집기
6. [Typora](https://typora.io/) 마크다운 편집기 (선택)
7. `pip install -r requirements.txt`

	의존성 모듈 설치. 최초 1회 실행.

### 2. 환경변수 설정
`.env.example`의 형식을 참고하여 `.env`파일을 작성한다.
- `WORK_DIR`: 작업을 진행할 폴더의 절대경로. 이 폴더에는
	1. 촬영한 이미지 파일들
	2. 크로스체크할 엑셀파일 1개

	가 있어야 한다.
- `TARGET_NATION`: 메세지를 보낼 국가를 지정한다.

	`SG`, `PH`, `MY`, `ID`중 하나
- `TESSERACT_PATH`: 테서렉트가 설치된 경로

### 3. 전처리
`python src/preprocess.py`
- 작업폴더 아래 `preprocess`라는 폴더가 만들어진다.
- 사진으로부터 `order_id`를 인식하여 파일명으로 저장한다. (ex: `200000AA0000A0.jpg`)
- 여러장일 경우 숫자가 붙는다. (ex: `200000AA0000A0_2.jpg`)
- 전처리 결과 로그파일 생성된다. (ex: `log_1024_1555.txt`)
- 전처리에 실패한 사진파일들은 수작업으로 적절한 파일명으로 수정해야 한다.

### 4. 메세지 자동화
`python src/auto_message.py`

전처리 결과물을 가지고, 쇼피에 접속하여 `order_id`별로 지정된 메세지와 사진파일을 전송한다.

현재는 메세지 부분만 `auto_message.py`에서 직접 설정하도록 되어있다. 추후 업데이트 예정.

---
## WORKFLOW
### 1. 전처리
작업 디렉토리로부터 이미지 파일 순회

이미지에서 바코드를 읽는다 >> tracking code

엑셀에서 tcode로부터 order_id를 읽는다 (못찾는 경우, 이미지로부터 tcode를 잘못 읽은 것)

파일명을 order_id로 바꾼다

### 2. 메세지 자동화
selenium

파일명 순회하면서

브라우저 통해 웹페이지 접속 후, (로그인 등) order_id(파일명)로 채팅방 검색

채팅방 접속 후, 지정해둔 텍스트 붙여넣고 전송하기

## 가상환경 및 모듈관리는 기본

## 라이브러리(패키지) 검색
- zbar

	바코드 읽는 프로그램

	원래 파이썬 패키지가 아니라서 pip에서 래핑한 버전이 몇 개 있는 것 같다

	2009년 10월 업로드

	https://pypi.org/project/zbar/#description

- zbar-py

	이미지가 numpy array로 읽어와야 하는 것 같다.

	2016년 12월 업로드

	https://pypi.org/project/zbar-py/#description

- pyzbar

	numpy array뿐만 아니라 raw bytes 등 여러 형식 지원

	2016년부터 2019년까지 버전업그레이드

	https://pypi.org/project/pyzbar/#description
	
- pillow

	PIL 파이썬 이미지 라이브러리 후속 프로젝트 [위키 참고 링크](https://ko.wikipedia.org/wiki/Python_Imaging_Library)
	
- opencv

	opencv와 zbar를 함께 쓰는 경우가 많아 보임. 왜때문?!

	[opencv with zbar](https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/)

- pandas

	엑셀파일을 파이썬 내에서 손쉽게 다루기 위한 라이브러리

- xlrd

	엑셀파일 읽기위한 optional dependency라고 함

- selenium

	~~말해무엇하리~~

	크롬드라이버 버전충돌 에러가 있었는데, 로컬에 설치된 크롬과 웹드라이버의 버전을 체크해야 하는 것 같다.

	[참고: If you are using Chrome version 86, please download ChromeDriver 86.0.4240.22](https://chromedriver.chromium.org/downloads)

- python-decouple

	환경변수 불러오기

- pytesseract

	파이썬에서 테서렉트 이용가능하도록 하는 패키지

## image preprocessing library
바코드 이미지 전처리의 성능이 생각만큼 잘 안나와서 다른 도구를 찾아보았다.
opencv와 tesseract의 조합으로 많이 사용하는 것 같다.

PIL로 읽어오기도 하는 것 같고, 파일을 직접 끌어오기도 하는 것 같다.

아무튼 테서렉트는 약간 복잡한데, 로컬에서 엔진 설치 + python wrapper 패키지 설치

### 테서렉트 설치
https://github.com/tesseract-ocr/tesseract/wiki

https://github.com/UB-Mannheim/tesseract/wiki

https://pypi.org/project/pytesseract

> We don't provide an installer for Tesseract 4.1.0 because we think that the latest version 5.0.0-alpha is better for most Windows users in many aspects (functionality, speed, stability). Version 4.1 is only needed for people who develop software based on the Tesseract API and who need 100 % API compatibility with version 4.0.
>> 대충 4.1말고 5.0버전 쓰라는 뜻

그럼 pytesseract와 5.0이 잘 호환되는지 체크해야 할듯. 잘되겠지뭐.

(5.0 알파버전은 2020년 3월, pytesseract는 2020년 10월 업뎃)

## 환경변수 관리
`.env` 사용

## 참고자료
[쇼피 api](https://open.shopee.com/)

[파이썬 쇼피 api 패키지](https://pypi.org/project/shopee-api)