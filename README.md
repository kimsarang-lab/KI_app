# 나의 갱년기 증상 체크 🌷

Streamlit 기반 한국어 증상 자가평가 데모. 제공된 이미지의 11문항과 가중치를 구현합니다. 진단 앱 또는 원문 KI와 동일한 검증 도구가 아닙니다.

## 기능

- 11개 문항의 4단계 응답(기본 미선택), 미응답 안내
- 가중치 합산(0~51점), 증상별 결과표
- Excel에서 열 수 있는 UTF-8 BOM CSV 다운로드
- 초기화, 모바일 접근, 별도 응답 DB 없음

## GitHub에 업로드 (웹에서)

1. ZIP을 먼저 압축 해제합니다. ZIP 자체를 올리면 배포할 수 없습니다.
2. https://github.com/new 에서 `menopause-check`라는 저장소를 만듭니다. 공개 여부는 본인이 선택합니다.
3. 저장소의 **uploading an existing file** 또는 **Add file → Upload files**를 선택합니다.
4. 압축 해제된 폴더 **안의 파일**을 올립니다. 저장소 첫 화면에 `app.py`, `scoring.py`, `requirements.txt`, `README.md`가 보여야 합니다.
5. **Commit changes**를 누릅니다.
6. `.streamlit`은 Mac Finder에서 숨김 폴더이므로 Command+Shift+. 으로 표시합니다. 업로드가 어려우면 GitHub의 **Add file → Create new file**에서 `.streamlit/config.toml`을 만들고 해당 파일 내용을 붙여넣습니다. 설정 파일이 없어도 기본 디자인으로 실행됩니다.

## Streamlit에 배포

1. https://share.streamlit.io 에 로그인하고 GitHub 계정을 연결합니다.
2. **Create app**에서 저장소 `kimsarang-lab/KI_app`, 브랜치 `main`, 실행 파일 `app.py`를 선택합니다.
3. **Advanced settings**에서 Python **3.12**을 선택합니다(검증 환경).
4. **Deploy**를 누르고 설치가 끝나면 생성된 앱 링크로 접속합니다.
5. 파일을 상위 폴더째 올렸다면 실행 파일 경로도 `menopause-check/app.py`로 지정해야 합니다. 루트 업로드를 권장합니다.

공식 안내: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 로컬 실행

Python 3.12 권장. 터미널에서 이 폴더로 이동한 후:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows 가상환경 활성화: `.venv\Scripts\activate`

## 점수와 해석

| 문항 | 가중치 |
|---|---:|
| 안면홍조 | 4 |
| 발한, 불면증, 신경질 | 각 2 |
| 우울증, 현기증(어지럼증), 피로감, 두통, 관절/근육통, 가슴두근거림, 질 건조감 | 각 1 |

없다=0, 약간=1, 보통=2, 심함=3. 총점은 각 응답 × 가중치의 합입니다.
이미지의 구간(5~10, 10~15, 15 이상)은 경계가 겹치고 5점 미만 설명이 없어 중증도 분류를 구현하지 않았습니다. 문항 명칭은 이미지를 따랐으며, '우울증' 응답 역시 해당 질환의 진단을 의미하지 않습니다. 이미지에 응답 기준 기간이 없어 임의의 회상 기간도 추가하지 않았습니다.

문항 출처: 사용자가 제공한 「나의 갱년기 지수는?」 이미지. 이미지에 인용된 제목은 *Comparative clinical evaluation of estrogenic preparations by the menopausal and amenorrheal indices*입니다. 이미지와 원문 도구의 일치 여부, 타당도, 이용 조건은 검증되지 않았습니다. 연구·임상 활용 전 도구 버전과 기준을 확인해야 합니다. 원본 이미지는 배포 패키지에 포함하지 않았습니다.

## 개인정보

응답은 계산을 위해 서버 세션에서 처리됩니다. 앱 코드에는 응답의 영구 저장, 사용자 식별정보 수집, 별도 분석 서비스 전송 기능이 없습니다. 다운로드한 CSV는 사용자가 관리합니다. 호스팅 서비스 자체의 로그·개인정보 정책은 별도 적용됩니다.

## 테스트

```bash
python -m unittest discover -s tests -v
```
