
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")


# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("aggregated_state_results.csv")
    return df


df = load_data()

# عنوان الصفحة
st.title("🗳 محاكاة الانتخابات الرئاسية الأمريكية (2008 - 2024)")

# اختيار الولاية
states = df['state_name'].unique()
selected_state = st.selectbox("اختر ولاية لعرض نتائجها:", sorted(states))

# تصفية البيانات حسب الولاية المختارة
state_data = df[df['state_name'] == selected_state]

# ✅ 1. رسم توزيع الأصوات عبر السنوات
fig_votes = px.bar(
    state_data,
    x='year', y='votes',
    color='party', barmode='group',
    title=f"توزيع الأصوات في {selected_state} من 2008 إلى 2024"
)
st.plotly_chart(fig_votes, use_container_width=True)

# ✅ 2. تغيّر تصويت الناخبين (swing)
pivot = state_data.pivot(index='year', columns='party', values='votes').fillna(0)
pivot['dem_change'] = pivot['dem'].diff()
pivot['gop_change'] = pivot['gop'].diff()

fig_swing = px.bar(
    pivot.reset_index(),
    x='year', y=['dem_change', 'gop_change'],
    barmode='group',
    title="تغيرات التصويت عبر الانتخابات"
)
st.plotly_chart(fig_swing, use_container_width=True)

# ✅ 3. الانحراف المعياري
std_dev = state_data.groupby('party')['votes'].std().reset_index()
fig_std = px.bar(std_dev, x='party', y='votes', title="الانحراف المعياري للأصوات")
st.plotly_chart(fig_std, use_container_width=True)

# ✅ 4. توقع نتائج 2028
latest = pivot.iloc[-1]  # بيانات 2024
avg_change = pivot[['dem_change', 'gop_change']].mean()

pred_dem = latest['dem'] + avg_change['dem_change']
pred_gop = latest['gop'] + avg_change['gop_change']

winner = "الديمقراطي" if pred_dem > pred_gop else "الجمهوري"
st.markdown(f"### 🧠 التوقع لانتخابات 2028 في {selected_state}: *{winner}*")

# ✅ 5. عرض خريطة المحاكاة الانتخابية
st.markdown("### 🗺 خريطة المحاكاة الانتخابية")
st.image("us_map.gif", caption="محاكاة نتائج الانتخابات حسب الولاية", use_container_width=True)

# ✅ 6. عرض شريط الفوز لكل حزب
st.markdown("### 📊 عدد مرات فوز الحزب في المحاكاة")
st.image("election_bars.gif", caption="نتائج محاكاة الفوز حسب الحزب", use_container_width=True)
