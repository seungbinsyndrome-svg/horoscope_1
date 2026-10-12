import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# 한글 폰트 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def get_user_inputs():
  st.title("토정비결 기반 오늘의 운세")
  st.write("생년월일시분초와 띠를 입력하여 오늘의 운세를 확인하세요.")

  st.subheader("출생 정보 입력")
  col1, col2, col3 = st.columns(3)
  with col1:
    birth_year = st.number_input(
        "출생 연도", min_value=1900, max_value=2026, value=2000
    )
  with col2:
    birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=1)
  with col3:
    birth_day = st.number_input("출생 일", min_value=1, max_value=31, value=1)

  col4, col5, col6 = st.columns(3)
  with col4:
    birth_hour = st.number_input("출생 시", min_value=0, max_value=23, value=0)
  with col5:
    birth_minute = st.number_input("출생 분", min_value=0, max_value=59, value=0)
  with col6:
    birth_second = st.number_input("출생 초", min_value=0, max_value=59, value=0)

  zodiac_list = [
      "쥐",
      "소",
      "호랑이",
      "토끼",
      "용",
      "뱀",
      "말",
      "양",
      "원숭이",
      "닭",
      "개",
      "돼지",
  ]
  zodiac = st.selectbox("띠 선택", zodiac_list)

  return (
      birth_year,
      birth_month,
      birth_day,
      birth_hour,
      birth_minute,
      birth_second,
      zodiac,
  )


def calculate_tojeongbigyeol(year, month, day, hour, minute, second, zodiac):
  today = datetime.date.today()
  seed_val = (
      year
      + month
      * 31
      + day
      + hour
      + minute
      + second
      + hash(zodiac)
      + today.toordinal()
  )
  np.random.seed(seed_val % (2**32))

  fortunes = [
      (
          "상반기에 노력한 결실이 하반기에 크게 나타나는 운세입니다."
          " 조급해하지 말고 꾸준히 나아가십시오."
      ),
      (
          "주변 사람과의 협력이 중요한 하루입니다. 혼자서 해결하기 어려운"
          " 일은 조언을 구하는 것이 좋습니다."
      ),
      (
          "뜻밖의 재물이나 기회가 찾아올 수 있는 안정적인 하루입니다. 다만"
          " 지출에 주의를 기울이십시오."
      ),
      (
          "작은 장애물이 있을 수 있으나 지혜롭게 극복할 수 있는 힘이 있습니다."
          " 차분하게 대처하십시오."
      ),
      (
          "새로운 도전이나 계획을 시작하기 좋은 날입니다. 결단력을 가지고"
          " 행동으로 옮기십시오."
      ),
  ]

  selected_fortune = np.random.choice(fortunes)

  scores = {
      "종합운": int(np.random.randint(70, 100)),
      "재물운": int(np.random.randint(65, 100)),
      "사업/학업운": int(np.random.randint(65, 100)),
      "건강운": int(np.random.randint(70, 100)),
  }

  return selected_fortune, scores


def generate_fortune_image(scores):
  categories = list(scores.keys())
  values = list(scores.values())

  fig, ax = plt.subplots(figsize=(6, 4))
  bars = ax.bar(
      categories, values, color=["#4A90E2", "#50E3C2", "#F5A623", "#E94E77"]
  )
  ax.set_ylim(0, 100)
  ax.set_ylabel("점수")
  ax.set_title("부문별 오늘의 운세 지수")

  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height}점",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

  plt.tight_layout()
  return fig


def display_results(fortune_text, fig):
  st.subheader("오늘의 운세 결과")
  st.write("---")

  st.markdown("### 텍스트 운세")
  st.write(fortune_text)

  st.markdown("### 운세 그래프")
  st.pyplot(fig)


def main():
  (
      birth_year,
      birth_month,
      birth_day,
      birth_hour,
      birth_minute,
      birth_second,
      zodiac,
  ) = get_user_inputs()

  if st.button("오늘의 운세 확인하기"):
    fortune_text, scores = calculate_tojeongbigyeol(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        zodiac,
    )
    fig = generate_fortune_image(scores)
    display_results(fortune_text, fig)


if __name__ == "__main__":
  main()