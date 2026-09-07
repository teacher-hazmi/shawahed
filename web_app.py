import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية للموقع
st.set_page_config(page_title="بوابة شواهد الرقمية", page_icon="🎓", layout="centered")

# إضافة كود تنسيقي لجعل واجهة الموقع تدعم اللغة العربية من اليمين لليسار بالكامل
st.markdown("""
    <style>
        .stTextInput align-items { direction: rtl !important; text-align: right !important; }
        div[data-baseweb="input"] { direction: rtl !important; text-align: right !important; }
        p, label { text-align: right !important; direction: rtl !important; width: 100%; }
        .stButton button { direction: rtl !important; }
    </style>
""", unsafe_allow_html=True)

# 2. تصميم الترويسة العلوية باللون الأزرق الملكي
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 25px; direction: rtl;'>
        <h1 style='text-align: right; color: white; font-family: "Arial"; margin: 0; padding-right: 10px;'>🎓 بوابة شواهد التعليمية</h1>
        <p style='text-align: right; color: #E5E7EB; font-size: 16px; margin: 10px 0 0 0; padding-right: 10px;'>مدرسة أحمد بن حنبل - نظام الاستعلام الذكي عن بطاقات المتابعة</p>
    </div>
""", unsafe_allow_html=True)

# العبارة الترحيبية الدقيقة والمخصصة بناءً على طلبك
st.markdown("<p style='text-align: right; color: #4B5563; font-size: 15px; direction: rtl; font-weight: bold;'>اعزائي اولياء الأمور لتسهيل متابعة ابناءكم في مادة مهارات رقمية ومعرفة مستواهم يرجي كتابة السجل المدني في الاسفل</p>", unsafe_allow_html=True)

# 3. دالة ذكية لقراءة ملف الإكسل المرفوع مباشرة في السيرفر
@st.cache_data
def load_students_from_excel():
    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file, dtype={"السجل المدني": str})
        db = {}
        for _, row in df.iterrows():
            sec_id = str(row["السجل المدني"]).strip()
            db[sec_id] = {
                "name": row["اسم الطالب"],
                "class": row["الصف"],
                "card_image": f"student_{int(row['رقم الصورة'])}.png"
            }
        return db
    return {}

students_database = load_students_from_excel()

# 4. تصميم صندوق الدخول والاستعلام المحاذي لليمن
if not students_database:
    st.error("⚠️ لم يتم العثور على قاعدة البيانات الشاملة للطلاب 'students_data.xlsx' في السيرفر.")
else:
    with st.container():
        st.markdown("<div style='background-color: #F3F4F6; padding: 25px; border-radius: 8px; border: 1px solid #E5E7EB; direction: rtl; text-align: right;'>", unsafe_allow_html=True)
        
        # خانة إدخال السجل المدني
        national_id = st.text_input("🔑 رقم السجل المدني للطالب:", max_chars=10)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("") 
        
        # زر الاستعلام
        submit_button = st.button("🔍 عرض بطاقة المتابعة والنتائج", type="primary", use_container_width=True)

    # 5. معالجة الضغط وعرض النتائج
    if submit_button:
        search_id = national_id.strip()
        if search_id in students_database:
            student = students_database[search_id]
            
            st.markdown(f"<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)
            st.success(f"✨ تم التحقق بنجاح! مرحباً بولي أمر الطالب: **{student['name']}**")
            st.info(f"📋 **الصف الدراسي:** {student['class']}")
            st.markdown(f"</div>", unsafe_allow_html=True)
            
            # تحديد مسار الصورة داخل السيرفر مباشرة بشكل صحيح ومغلق
            image_path = student['card_image']
            
            if os.path.exists(image_path):
                st.image(image_path, caption=f"البطاقة الرسمية للطالب: {student['name']}", use_column_width=True)
            else:
                st.warning(f"⚠️ تم التحقق من السجل، ولكن لم يتم العثور على ملف الصورة: {student['card_image']} بداخل السيرفر.")
        else:
            st.markdown(f"<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)
            st.error("❌ عذراً، رقم السجل المدني غير صحيح أو غير مسجل في النظام الدراسي للعام الحالي!")
            st.markdown(f"</div>", unsafe_allow_html=True)
