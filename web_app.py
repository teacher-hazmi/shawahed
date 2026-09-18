import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="بوابة شواهد الرقمية", page_icon="🎓", layout="centered")

st.markdown("""
<style>
.stTextInput align-items { direction: rtl !important; text-align: right !important; }
.st_label { text-align: right !important; direction: rtl !important; width: 100%; }
.stButton button { direction: rtl !important; }
div[data-baseweb="input"] { 
    direction: rtl !important; 
    text-align: right !important; 
    border: 2px solid #1E3A8A !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 25px; direction: rtl;">
<h1 style="text-align: right; color: white; font-family: 'Arial'; margin: 0; padding-right: 10px;">🎓 بوابة شواهد التعليمية</h1>
<p style="text-align: right; color: #E5E7EB; font-size: 16px; margin: 10px 10px 0 0; padding-right: 10px;">نظام الاستعلام الذكي عن بطاقات المتابعة والنتائج</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align: right; color: #4B5563; font-size: 15px; direction: rtl; font-weight: bold;">أعزائي أولياء الأمور، لتسهيل متابعة أبنائكم في مادة مهارات رقمية ومعرفة مستواهم يرجى كتابة السجل المدني في الأسفل:</p>', unsafe_allow_html=True)

@st.cache_data
def load_students_from_excel():
    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        id_col = None
        for col in df.columns:
            if "سجل" in str(col) or "مدني" in str(col) or "هوية" in str(col) or "ID" in str(col).upper():
                id_col = col
                break
        if id_col is None:
            return "error_col"
        db = {}
        for _, row in df.iterrows():
            val = str(row[id_col]).strip()
            sec_id = val.split('.')[0] if '.' in val else val
            db[sec_id] = {
                "name": row["اسم الطالب"],
                "class": row["الصف الدراسي"],
                "image_num": row["رقم الطالب"]
            }
        return db
    return {}

students_db = load_students_from_excel()

search_id = st.text_input("", placeholder="أدخل رقم السجل المدني هنا...", key="national_id_input")

if students_db == "error_col":
    st.error("⚠️ خطأ في ملف الإكسل: لم يتم العثور على عمود باسم 'السجل المدني'. يرجى التأكد من تسمية العمود في ملفك بدقة.")
elif search_id:
    search_id = search_id.strip()
    if search_id in students_db:
        student = students_db[search_id]
        st.success(f"🔹 تم التحقق بنجاح! مرحباً بولي أمر الطالب: {student['name']}")
        st.info(f"📋 الصف الدراسي: {student['class']}")
        image_name = f"student_{student['image_num']}.png"
        image_path = os.path.join("images", image_name) if os.path.exists("images") else image_name
        if os.path.exists(image_path) or os.path.exists(image_name):
            st.image(image_path if os.path.exists(image_path) else image_name, use_container_width=True)
        else:
            st.warning(f"⚠️ تم التحقق، ولكن لم يتم العثور على ملف الصورة: {image_name}")
    else:
        st.error("❌ رقم السجل المدني غير مسجل في النظام، يرجى التأكد من الرقم والمحاولة مجدداً.")
