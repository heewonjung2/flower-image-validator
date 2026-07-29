import streamlit as st
from validator import validate_flower

st.set_page_config(
    page_title="Flower Image Validator",
    page_icon="🌸",
    layout="centered"
)

# ===========================
# CSS
# ===========================
st.markdown("""
<style>

/* 전체 여백 */
.main > div {
    padding-top: 2rem;
}

/* 제목 */
h1 {
    text-align: center;
    color: #2E7D32;
}

/* 캡션 */
[data-testid="stCaptionContainer"] {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    height: 3rem;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #4CAF50;
    color: white;
}

/* 텍스트 입력 */
.stTextArea textarea {
    border-radius: 12px;
}

/* 업로드 영역 */
[data-testid="stFileUploader"] {
    border: 2px dashed #B5D5C5;
    border-radius: 15px;
    padding: 15px;
}

/* Alert */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* 이미지 */
img {
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

# ===========================
# 제목
# ===========================
st.title("🌸 Flower Image Validator 🌸")

st.caption("프롬프트와 꽃 이미지를 비교하여 AI가 일치 여부를 판단합니다.")

# ===========================
# 입력
# ===========================
prompt = st.text_area(
    "꽃다발 프롬프트를 입력하세요.",
    placeholder="예) 분홍 장미와 흰 튤립으로 화사한 꽃다발"
)

uploaded_image = st.file_uploader(
    "이미지를 업로드하세요.",
    type=["png", "jpg", "jpeg"]
)

# ===========================
# 버튼 및 분석 로직
# ===========================
if st.button("검증하기"):

    if uploaded_image is None:
        st.warning("이미지를 업로드해주세요.")

    elif not prompt.strip():
        st.warning("꽃다발 프롬프트를 입력해주세요.")

    else:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(
                uploaded_image,
                caption="업로드한 이미지",
                width=250
            )

        try:
            with st.spinner("🌸 AI가 이미지를 분석하고 있습니다..."):
                result = validate_flower(
                    prompt,
                    uploaded_image
                )

            if result.get("match"):
                st.success("✅ 프롬프트 조건과 일치합니다!")
            else:
                st.error("❌ 프롬프트 조건과 일치하지 않습니다.")

            st.markdown("---")
            st.markdown("## 🌼 검증 결과")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.markdown("#### 🌼 꽃 종류")
                    st.markdown(
                        f"<h2 style='text-align:center; color:#2E7D32;'>{result.get('flower', '정보 없음')}</h2>",
                        unsafe_allow_html=True
                    )

            with col2:
                with st.container(border=True):
                    st.markdown("#### 🎨 꽃 색상")
                    st.markdown(
                        f"<h2 style='text-align:center; color:#D81B60;'>{result.get('color', '정보 없음')}</h2>",
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💬 판정 사유")

            st.markdown(f"""
            <div style="
                background:#F6FBFF;
                border-left:6px solid #4CAF50;
                padding:20px;
                border-radius:12px;
                line-height:1.8;
                font-size:16px;
                box-shadow:0 2px 5px rgba(0,0,0,0.05);
            ">
                {result.get("reason", "상세 이유가 제공되지 않았습니다.")}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("🔍 응답 원본 보기(JSON)"):
                st.json(result)

        except Exception as e:
            st.error(f"오류가 발생했습니다.\n\n{e}")