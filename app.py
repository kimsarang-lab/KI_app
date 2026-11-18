import csv
import io
import streamlit as st
from scoring import SYMPTOMS, LEVELS, MAX_SCORE, calculate

st.set_page_config(page_title='나의 갱년기 증상 체크', page_icon='🌷', layout='centered')
st.markdown('''<style>
.block-container {max-width:760px; padding-top:2.5rem;}
h1 {letter-spacing:-.06em;}
.hero {background:linear-gradient(115deg,#fff0f1,#fff5e9); padding:24px; border-radius:22px; margin-bottom:22px; color:#722e42;}
.hero small {letter-spacing:.13em; font-weight:600;}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><small>MY WELLNESS CHECK</small><h1>나의 갱년기 증상 체크</h1><p>몸과 마음의 변화를 차분하게 살펴보세요.</p></div>', unsafe_allow_html=True)
st.write('각 증상에 대해 현재 느끼는 정도를 선택해주세요. 총 11문항입니다.')
st.caption('제공된 이미지의 문항·가중치를 구현한 참고용 앱입니다. 갱년기 여부를 진단하지 않습니다.')

def clear():
    for i in range(len(SYMPTOMS)):
        st.session_state.pop(f'q{i}', None)
    st.session_state.pop('result', None)

st.button('처음부터 다시 하기', on_click=clear)
with st.form('symptoms'):
    answers = []
    for i, (symptom, weight) in enumerate(SYMPTOMS):
        answers.append(st.radio(f'{i+1}. {symptom}', range(4),
                                format_func=lambda value: LEVELS[value],
                                index=None, horizontal=True, key=f'q{i}'))
    submitted = st.form_submit_button('나의 점수 확인하기', type='primary', use_container_width=True)

if submitted:
    st.session_state.pop('result', None)
    if None in answers:
        missing = [str(i+1) for i, a in enumerate(answers) if a is None]
        st.warning('아직 선택하지 않은 문항이 있어요: ' + ', '.join(missing) + '번')
    else:
        st.session_state.result = list(answers)

if 'result' in st.session_state:
    result = st.session_state.result
    total = calculate(result)
    st.divider()
    st.subheader('나의 체크 결과')
    st.metric('가중치 적용 총점', f'{total}점', help=f'각 응답 점수(0~3)에 가중치를 곱한 합계입니다. 범위: 0~{MAX_SCORE}점.')
    st.caption('마지막으로 ‘나의 점수 확인하기’를 누른 응답의 결과입니다. 응답을 바꾸면 버튼을 다시 눌러주세요.')
    st.info('이 점수만으로 갱년기 여부나 증상의 원인을 판단할 수 없습니다. 증상이 불편하거나 지속된다면 의료진과 상담해주세요.')
    rows = [{'증상': name, '응답': LEVELS[a], '응답 점수': a, '가중치': w, '반영 점수': a*w}
            for (name, w), a in zip(SYMPTOMS, result)]
    with st.expander('증상별 점수 보기', expanded=True):
        st.dataframe(rows, hide_index=True, use_container_width=True)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['항목', '응답', '응답 점수', '가중치', '반영 점수'])
    for row in rows:
        writer.writerow(row.values())
    writer.writerow(['합계', '', '', '', total])
    writer.writerow(['안내', '제공 이미지 기반 참고용 점수; 진단 및 중증도 분류에 사용하지 않음'])
    st.download_button('결과 내려받기 (CSV)', output.getvalue().encode('utf-8-sig'),
                       'menopause_check_result.csv', 'text/csv')

with st.expander('평가 기준과 개인정보 안내'):
    st.write('응답은 없다 0점, 약간 1점, 보통 2점, 심함 3점입니다. 안면홍조 ×4, 발한·불면증·신경질 ×2, 나머지 문항 ×1을 적용합니다. 총점 범위는 0~51점입니다.')
    st.write('제공 이미지의 중증도 구간은 10점·15점의 경계가 겹치고 5점 미만의 해석이 없습니다. 원문 도구와 분류 기준을 확인하기 전까지 경증·중등도·중증 판정은 제공하지 않습니다. 원문 Kupperman Index와 동일한 검증 도구라는 의미가 아닙니다.')
    st.write('이 앱은 이름·연락처를 요청하지 않으며, 응답을 별도 파일이나 데이터베이스에 저장하지 않습니다. 계산을 위해 응답은 Streamlit 서버의 현재 세션에서 처리됩니다. 다운로드한 결과는 사용자의 기기에 저장됩니다.')
    st.caption('문항 출처: 사용자가 제공한 「나의 갱년기 지수는?」 이미지. 이미지에 기재된 참고문헌 제목: Comparative clinical evaluation of estrogenic preparations by the menopausal and amenorrheal indices. 본 앱의 문항 구성과 원문 간 일치 여부는 검증되지 않았습니다.')
