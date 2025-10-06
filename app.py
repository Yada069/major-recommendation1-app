import streamlit as st
import graphviz
import pandas as pd
import numpy as np
import plotly.express as px

# --- ตั้งค่าพื้นฐานของหน้าเว็บ ---
st.set_page_config(page_title="แนะนำสถานที่ท่องเที่ยว", page_icon="🌍", layout="wide")

# --- เมนูหลักด้านซ้าย ---
st.sidebar.title("เมนูหลัก")
menu_choice = st.sidebar.selectbox(
    "เลือกเมนูที่ต้องการ:",
    ("Dashboard สรุปผล", "ให้ความรู้แต่ละจังหวัด", "แบบทดสอบเลือกการตัดสินใจ")
)

# ------------------------------
# 1. Dashboard
# ------------------------------
if menu_choice == "Dashboard สรุปผล":
    st.title("📊 Dashboard สรุปผล")
    st.write("ภาพรวมข้อมูลจากการจำลองนักท่องเที่ยว 500 คนที่เข้ามาทำแบบทดสอบ")

    # --- สร้างข้อมูลจำลอง ---
    @st.cache_data
    def create_mock_data():
        num_tourists = 500
        provinces = [
            "ภูเก็ต", "เชียงใหม่", "กรุงเทพฯ", "ชลบุรี", "กระบี่",
            "สุราษฎร์ธานี", "อุบลราชธานี", "นครราชสีมา", "พระนครศรีอยุธยา", "กาญจนบุรี",
            "สุโขทัย", "เพชรบุรี", "ตรัง", "แม่ฮ่องสอน", "ขอนแก่น"
        ]
        types = ["ทะเล", "ภูเขา", "วัฒนธรรม", "ยอดนิยม", "ธรรมชาติ"]
        data = {
            'จังหวัด': np.random.choice(provinces, num_tourists),
            'ประเภทสถานที่': np.random.choice(types, num_tourists)
        }
        df = pd.DataFrame(data)
        return df

    df = create_mock_data()

    # --- กราฟสรุปจังหวัด ---
    st.header("จังหวัดที่ถูกแนะนำมากที่สุด")
    province_counts = df['จังหวัด'].value_counts().reset_index()
    province_counts.columns = ['จังหวัด', 'จำนวนนักท่องเที่ยว']

    fig_bar = px.bar(province_counts,
                     x='จังหวัด',
                     y='จำนวนนักท่องเที่ยว',
                     title="จำนวนการแนะนำจังหวัด",
                     color='จังหวัด',
                     text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- กราฟประเภทสถานที่ ---
    st.header("ประเภทสถานที่ท่องเที่ยวที่นิยม")
    fig_pie = px.pie(df, names='ประเภทสถานที่', title='สัดส่วนประเภทสถานที่')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.header("ตารางข้อมูลดิบ")
    st.dataframe(df)


# ------------------------------
# 2. ข้อมูลแต่ละจังหวัด
# ------------------------------
elif menu_choice == "ให้ความรู้แต่ละจังหวัด":
    st.title("📚 ข้อมูลจังหวัดท่องเที่ยว")
    st.write("ทำความรู้จักกับจังหวัดท่องเที่ยวยอดนิยมของไทย")

    st.header("🌴 ภูเก็ต")
    st.write("- หาดป่าตอง, หาดกะตะ, เกาะพีพี (ประเภท: ทะเล)")

    st.header("⛰️ เชียงใหม่")
    st.write("- ดอยสุเทพ, ดอยอินทนนท์, ถนนนิมมาน (ประเภท: ภูเขา + วัฒนธรรม)")

    st.header("🏙️ กรุงเทพฯ")
    st.write("- วัดพระแก้ว, พระบรมมหาราชวัง, ถนนข้าวสาร (ประเภท: วัฒนธรรม + ยอดนิยม)")

    st.header("🌊 ชลบุรี")
    st.write("- พัทยา, เกาะล้าน, สวนสัตว์เปิดเขาเขียว (ประเภท: ทะเล + ยอดนิยม)")

    st.header("🏖️ กระบี่")
    st.write("- อ่าวนาง, ทะเลแหวก, เกาะพีพี (ประเภท: ทะเล)")

    st.header("🌅 สุราษฎร์ธานี")
    st.write("- เกาะสมุย, เกาะพะงัน, เขาสก (ประเภท: ทะเล + ธรรมชาติ)")

    st.header("🌄 นครราชสีมา")
    st.write("- เขาใหญ่, ปราสาทหินพิมาย (ประเภท: ธรรมชาติ + วัฒนธรรม)")

    st.header("🏯 พระนครศรีอยุธยา")
    st.write("- อุทยานประวัติศาสตร์อยุธยา, วัดไชยวัฒนาราม (ประเภท: วัฒนธรรม)")

    st.header("🌉 กาญจนบุรี")
    st.write("- สะพานข้ามแม่น้ำแคว, น้ำตกเอราวัณ (ประเภท: ธรรมชาติ + วัฒนธรรม)")

    st.header("🏜️ อุบลราชธานี")
    st.write("- ผาแต้ม, สามพันโบก (ประเภท: ธรรมชาติ)")

    st.header("🏛️ สุโขทัย")
    st.write("- อุทยานประวัติศาสตร์สุโขทัย (ประเภท: วัฒนธรรม)")

    st.header("🌊 เพชรบุรี")
    st.write("- ชะอำ, เขาวัง (ประเภท: ทะเล + วัฒนธรรม)")

    st.header("🏝️ ตรัง")
    st.write("- เกาะกระดาน, เกาะมุก (ประเภท: ทะเล)")

    st.header("🌄 แม่ฮ่องสอน")
    st.write("- ปาย, ถ้ำปลา (ประเภท: ภูเขา + ธรรมชาติ)")

    st.header("🦖 ขอนแก่น")
    st.write("- บึงแก่นนคร, พิพิธภัณฑ์ไดโนเสาร์ภูเวียง (ประเภท: ธรรมชาติ + วัฒนธรรม)")


# ------------------------------
# 3. แบบทดสอบเลือกการตัดสินใจ
# ------------------------------
elif menu_choice == "แบบทดสอบเลือกการตัดสินใจ":
    st.title("📝 แบบทดสอบเลือกการท่องเที่ยว")
    st.write("เลือกความชอบของคุณ แล้วกดปุ่มเพื่อดูคำแนะนำ")

    st.sidebar.header("กรอกข้อมูลของคุณที่นี่")
    budget = st.sidebar.radio("1. งบประมาณของคุณ", ["ต่ำ (<5000)", "ปานกลาง (5000-15000)", "สูง (>15000)"], key="budget")
    prefer = st.sidebar.radio("2. คุณชอบบรรยากาศแบบไหน", ["ทะเล", "ภูเขา", "วัฒนธรรม", "ยอดนิยม", "ธรรมชาติ"], key="prefer")
    season = st.sidebar.radio("3. ช่วงเวลาเดินทาง", ["หน้าร้อน", "หน้าหนาว", "หน้าฝน"], key="season")

    if st.sidebar.button("แสดงผลการแนะนำ"):
        result_province = ""
        result_spot = ""
        result_type = prefer

        # Logic การแนะนำเบื้องต้น
        if prefer == "ทะเล":
            if budget == "ต่ำ (<5000)":
                result_province, result_spot = "ชลบุรี", "เกาะล้าน"
            elif budget == "ปานกลาง (5000-15000)":
                result_province, result_spot = "กระบี่", "อ่าวนาง"
            else:
                result_province, result_spot = "ภูเก็ต", "หาดป่าตอง"
        elif prefer == "ภูเขา":
            result_province, result_spot = "เชียงใหม่", "ดอยอินทนนท์"
        elif prefer == "วัฒนธรรม":
            result_province, result_spot = "สุโขทัย", "อุทยานประวัติศาสตร์สุโขทัย"
        elif prefer == "ธรรมชาติ":
            result_province, result_spot = "นครราชสีมา", "เขาใหญ่"
        else: # ยอดนิยม
            result_province, result_spot = "กรุงเทพฯ", "ถนนข้าวสาร"

        # แสดงผลลัพธ์
        st.success(f"จังหวัดที่แนะนำสำหรับคุณคือ: **{result_province}**")
        st.info(f"สถานที่ท่องเที่ยวที่เหมาะสม: {result_spot} ({result_type})")

                # แสดงกราฟเส้นทางการตัดสินใจ
        dot = graphviz.Digraph()

        # เพิ่ม Node พร้อมแสดงค่าที่เลือก
        dot.node("A", f"งบประมาณ\n({budget})")
        dot.node("B", f"ความชอบ\n({prefer})")
        dot.node("C", f"ฤดูกาล\n({season})")
        dot.node("D", f"ผลลัพธ์:\n{result_province} - {result_spot} ({result_type})")

        # สร้างเส้นเชื่อม
        dot.edges(["AB", "BC", "CD"])

        st.graphviz_chart(dot)

