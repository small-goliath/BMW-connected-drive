# BMW Connected Drive를 사용하여 차량을 원격으로 제어해보자

(ios기준) BMW Connected Drive API를 활용하여 차량을 원격으로 제어할 수 있는 FastAPI 서버입니다.

## 기능

아래와 같은 API를 제공합니다:

- **문 열기:** `POST /api/remote-control/doors`
- **문 잠그기:** `DELETE /api/remote-control/doors`
- **경적 울리기:** `POST /api/remote-control/horn`
- **에어컨 켜기:** `POST /api/remote-control/air-conditioning`
- **에어컨 끄기:** `DELETE /api/remote-control/air-conditioning`
- **충전 시작:** `POST /api/remote-control/charging`
- **충전 정지:** `DELETE /api/remote-control/charging`
- **목표 충전량(%):** `PATCH /api/remote-control/charging-settings`
- **충전 상태 조회:** `GET /api/status/charging`
- **문, 창문, 선루프 상태 조회:** `GET /api/status/doors-windows`

 ⚠️ 모든 api의 응답(body)는 siri가 읽을 문자열을 리턴합니다.

## 설치 및 실행 방법

### 1. 필수 요구사항

- Python 3.10 이상
- `.env` 파일
- `log.ini` 파일

### 2. .env 파일 설정

`.env` 파일에 아래 내용을 추가해야 합니다:

```
PROJECT_NAME=your_service_title
CAPCHA_TOKEN=your_captcha_token
USERNAME=your_bmw_username
PASSWORD=your_bmw_password
VIN_NUMBER=your_vehicle_vin
```

- **PROJECT_NAME**: 서버 이름
- **CAPCHA_TOKEN**: [CAPTCHA 토큰 생성 방법](https://bimmer-connected.readthedocs.io/en/stable/captcha.html) 참조
- **USERNAME**: mybmw 앱 계정 사용자명
- **PASSWORD**: mybmw 앱 계정 비밀번호
- **VIN_NUMBER**: 차대번호

### 3. log.ini 파일 설정

`log.ini` 파일에 logging 설정을 해야합니다;
(예시)
```
[loggers]
keys=root

[handlers]
keys=logfile,logconsole

[formatters]
keys=logformatter

[logger_root]
level=INFO
handlers=logfile, logconsole

[formatter_logformatter]
format=[%(asctime)s.%(msecs)03d] %(levelname)s [%(filename)s:%(lineno)d][%(thread)d] >> %(message)s

[handler_logfile]
class=handlers.TimedRotatingFileHandler
level=INFO
args=('../logs/mybmw.log','midnight')
formatter=logformatter

[handler_logconsole]
class=handlers.logging.StreamHandler
level=INFO
args=()
formatter=logformatter
```

### 4. 설치

```bash
git clone https://github.com/small-goliath/BMW-connected-drive.git
cd BMW-connected-drive
python -m venv .venv
source .venv/bin/activate  # Windows의 경우 `.venv\Scripts\activate`
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
tmux new -s mybmw
source .venv/bin/activate
cd app
uvicorn main:app --env-file ../.env --log-config ../log.ini
```

### 5. 서버 실행 확인

```bash
tmux ls
```

## 참고 자료

- [bimmer_connected GitHub 저장소](https://github.com/bimmerconnected/bimmer_connected?tab=readme-ov-file)
- [BMW CarData API 문서](https://bmw-cardata.bmwgroup.com/thirdparty/public/car-data/technical-configuration/api-documentation)
- [BMW API 참고 사이트](https://bmwapi.mihaiblaga.dev/)

## 주의 사항

- API를 사용하기 위해서는 BMW Connected Drive 계정과 CAPTCHA 토큰이 반드시 필요합니다. (최초 statup 시)
- CAPTCHA 토큰 생성 방법은 [문서](https://bimmer-connected.readthedocs.io/en/stable/captcha.html)를 참고하세요.

BMW API 서버를 활용하여 원격으로 차량을 제어해 보세요! 삶의 질이 더 올라갑니다!