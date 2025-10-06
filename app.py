import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import graphviz

# ตั้งค่า Streamlit page
st.set_page_config(page_title="ระบบแนะนำท่องเที่ยว 🌴", layout="wide")

# Sidebar เมนู
menu_choice = st.sidebar.selectbox("🌟 เลือกเมนู", ["หน้าหลัก", "แบบทดสอบเลือกการตัดสินใจ"])

# --- หน้าหลัก ---
if menu_choice == "หน้าหลัก":
    st.markdown("""
        <h1 style='text-align: center; color: #FF6F61;'>🏠 ยินดีต้อนรับสู่ระบบแนะนำท่องเที่ยว</h1>
        <p style='text-align: center; font-size:18px; color:#555;'>ค้นหาสถานที่ท่องเที่ยวที่เหมาะกับคุณตามงบประมาณและความชอบ</p>
        """, unsafe_allow_html=True)

# --- แบบทดสอบเลือกการตัดสินใจ ---
elif menu_choice == "แบบทดสอบเลือกการตัดสินใจ":
    st.markdown("<h1 style='text-align: center; color: #FF6F61;'>📝 แบบทดสอบเลือกการท่องเที่ยว</h1>", unsafe_allow_html=True)
    st.write("กรอกข้อมูลของคุณด้านข้าง แล้วกดปุ่มเพื่อดูคำแนะนำ")

    st.sidebar.header("กรอกข้อมูลของคุณที่นี่")
    budget_choice = st.sidebar.radio(
        "1. งบประมาณของคุณ", 
        ["ต่ำ (<5000)", "ปานกลาง (5000-15000)", "สูง (>15000)"], key="budget"
    )
    prefer = st.sidebar.radio(
        "2. คุณชอบบรรยากาศแบบไหน", 
        ["ทะเล", "ภูเขา", "วัฒนธรรม", "ยอดนิยม", "ธรรมชาติ"], key="prefer"
    )

    # กำหนดงบเป็นตัวเลข
    if budget_choice == "ต่ำ (<5000)":
        budget = 5000
    elif budget_choice == "ปานกลาง (5000-15000)":
        budget = 12000
    else:
        budget = 20000

    # ฐานข้อมูลสถานที่
    destinations = [
        {"จังหวัด": "ชลบุรี", "สถานที่": "เกาะล้าน", "ประเภท": "ทะเล", "ค่าใช้จ่ายต่อวัน": 1500},
        {"จังหวัด": "กระบี่", "สถานที่": "อ่าวนาง", "ประเภท": "ทะเล", "ค่าใช้จ่ายต่อวัน": 2500},
        {"จังหวัด": "ภูเก็ต", "สถานที่": "หาดป่าตอง", "ประเภท": "ทะเล", "ค่าใช้จ่ายต่อวัน": 4000},
        {"จังหวัด": "เชียงใหม่", "สถานที่": "ดอยอินทนนท์", "ประเภท": "ภูเขา", "ค่าใช้จ่ายต่อวัน": 2000},
        {"จังหวัด": "เชียงใหม่", "สถานที่": "ถนนนิมมาน", "ประเภท": "ยอดนิยม", "ค่าใช้จ่ายต่อวัน": 2500},
        {"จังหวัด": "นครราชสีมา", "สถานที่": "เขาใหญ่", "ประเภท": "ธรรมชาติ", "ค่าใช้จ่ายต่อวัน": 1800},
        {"จังหวัด": "พระนครศรีอยุธยา", "สถานที่": "วัดไชยวัฒนาราม", "ประเภท": "วัฒนธรรม", "ค่าใช้จ่ายต่อวัน": 1200},
        {"จังหวัด": "สุโขทัย", "สถานที่": "อุทยานประวัติศาสตร์สุโขทัย", "ประเภท": "วัฒนธรรม", "ค่าใช้จ่ายต่อวัน": 1600},
        {"จังหวัด": "กรุงเทพฯ", "สถานที่": "ถนนข้าวสาร", "ประเภท": "ยอดนิยม", "ค่าใช้จ่ายต่อวัน": 2000},
    ]

    # --- เลือกสถานที่ที่อยากเที่ยวหลายแห่ง ---
    filtered_destinations = [d for d in destinations if d["ประเภท"] == prefer]
    location_options = [d["สถานที่"] for d in filtered_destinations]
    selected_locations = st.sidebar.multiselect(
        "3. เลือกสถานที่ที่อยากเที่ยว (เลือกได้หลายแห่ง)", location_options
    )

    if st.sidebar.button("🎯 แสดงผลการแนะนำ"):
        if not selected_locations:
            st.warning("❌ โปรดเลือกสถานที่อย่างน้อย 1 แห่ง")
        else:
            # รวมข้อมูลสถานที่ที่เลือก
            results = []
            for d in filtered_destinations:
                if d["สถานที่"] in selected_locations:
                    max_days = budget // d["ค่าใช้จ่ายต่อวัน"]
                    results.append({
                        "จังหวัด": d["จังหวัด"],
                        "สถานที่": d["สถานที่"],
                        "ค่าใช้จ่ายต่อวัน": d["ค่าใช้จ่ายต่อวัน"],
                        "สามารถเที่ยวได้ (วัน)": max_days
                    })

            df_results = pd.DataFrame(results)

            # --- แนะนำสถานที่เพิ่มเติมในจังหวัดเดียวกัน ---
            selected_provinces = df_results["จังหวัด"].unique()
            extra_recommendations = [
                d for d in filtered_destinations
                if d["จังหวัด"] in selected_provinces and d["สถานที่"] not in selected_locations
            ]
            df_extra = pd.DataFrame(extra_recommendations)

            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown("### 🗺️ ตารางสรุป")
                fig_table = go.Figure(data=[go.Table(
                    header=dict(values=list(df_results.columns),
                                fill_color='paleturquoise',
                                align='left'),
                    cells=dict(values=[df_results[col] for col in df_results.columns],
                               fill_color='lavender',
                               align='left'))
                ])
                st.plotly_chart(fig_table, use_container_width=True)

                if not df_extra.empty:
                    st.markdown("### 🌟 แนะนำสถานที่เพิ่มเติมในจังหวัดเดียวกัน")
                    fig_extra = go.Figure(data=[go.Table(
                        header=dict(values=list(df_extra.keys()),
                                    fill_color='lightgreen',
                                    align='left'),
                        cells=dict(values=[df_extra[col] for col in df_extra.columns],
                                   fill_color='honeydew',
                                   align='left'))
                    ])
                    st.plotly_chart(fig_extra, use_container_width=True)

            with col2:
                st.markdown("### 📊 จำนวนวันท่องเที่ยว")
                fig = px.bar(
                    df_results,
                    x="สถานที่",
                    y="สามารถเที่ยวได้ (วัน)",
                    color="จังหวัด",
                    text="สามารถเที่ยวได้ (วัน)",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(
                    plot_bgcolor="#FFF7F0",
                    paper_bgcolor="#FFF7F0",
                    title_font_color="#FF6F61"
                )
                st.plotly_chart(fig, use_container_width=True)

            # กราฟเส้นทางการตัดสินใจ
            st.markdown("### 🌐 เส้นทางการตัดสินใจ")
            dot = graphviz.Digraph(format='png')
            dot.attr(bgcolor='#FFF7F0')
            dot.node("A", f"💰 งบประมาณ\n({budget_choice})", style='filled', color='#FFCCCB')
            dot.node("B", f"💖 ความชอบ\n({prefer})", style='filled', color='#FFD580')
            dot.node("C", f"📍 สถานที่เลือก\n({', '.join(selected_locations)})", style='filled', color='#A0E7E5')
            dot.node("D", f"🏝️ ผลลัพธ์: {len(df_results)} สถานที่", style='filled', color='#B4F8C8')
            dot.edges(["AB", "BC", "CD"])
            st.graphviz_chart(dot)
