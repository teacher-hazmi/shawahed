import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية للموقع
st.set_page_config(page_title="بوابة شواهد الرقمية", page_icon="🎓", layout="centered")

st.markdown("""
<style>
/* ضبط محاذاة كل نصوص المتصفح والمخرجات لتكون من اليمين لليسار */
.stMarkdown p, p, h1, h3, div { text-align: right !important; direction: rtl !important; }

/* إخفاء تلميحات الإدخال المزعجة */
div[data-testid="InputInstruction"] { display: none !important; }

/* برواز ملفت وتوهج جذاب على جملة أعزائي أولياء الأمور */
.welcome-box {
    border: 2px dashed #FF5722 !important;
    background-color: #FFF3E0 !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin-bottom: 25px !important;
    box-shadow: 0px 4px 10px rgba(255, 87, 34, 0.1) !important;
}

/* إجبار النص الداخلي لخانة السجل على الاستقرار يميناً */
input { text-align: right !important; direction: rtl !important; }
input::placeholder { text-align: right !important; direction: rtl !important; color: #4A5568 !important; font-weight: bold !important; }

div[data-testid="stTextInput"] { width: 65% !important; margin-right: 0 !important; margin-left: auto !important; }
div[data-baseweb="input"] { border: 2.5px solid #1E3A8A !important; border-radius: 8px !important; background-color: #FFFFFF !important; }

/* تنسيق زر البحث الفعال */
div.stButton > button:first-child {
    background-color: #3B82F6 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 8px 25px !important;
    border: none !important;
    margin-top: 10px !important;
    box-shadow: 0px 4px 10px rgba(59, 130, 246, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# 2. تصميم الترويسة الشاملة لطلباتك الفخمة
st.markdown("""
<div style="background: linear-gradient(135deg, #1E3A8A, #2563EB); padding: 25px; border-radius: 12px; margin-bottom: 30px; direction: rtl; text-align: right;">
<h1 style="color: white; font-family: 'Arial'; margin: 0; font-size: 26px; font-weight: bold;">🎓 بوابة الشواهد الرقمية</h1>
<p style="color: #93C5FD; font-size: 15px; margin: 6px 0 0 0; font-weight: bold;">📊 ومتابعة الطلاب في مهامهم الأدائية والتحريرية</p>
<h3 style="color: #34D399; font-family: 'Arial'; margin: 12px 0 0 0; font-size: 18px; font-weight: bold;">🖥️ مادة المهارات الرقمية - للمعلم طارق الحازمي</h3>
<p style="color: #FBBF24; font-size: 15px; margin: 10px 0 0 0; font-weight: bold;">🏫 ابتدائية أحمد بن حنبل & متوسطة الشقيري</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome-box">
<p style="color: #D84315; font-size: 16px; font-weight: bold; margin: 0; line-height: 1.6;">
📢 أعزائي أولياء الأمور، لتسهيل متابعة أبنائكم في مادة مهارات رقمية ومعرفة مستواهم يرجى كتابة السجل المدني في الأسفل:
</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_students_from_excel():
    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        id_col, name_col, class_col, num_col, link_col = None, None, None, None, None
        for col in df.columns:
            col_str = str(col).strip()
            if "سجل" in col_str or "مدني" in col_str or "هوية" in col_str: id_col = col
            elif "اسم" in col_str or "طالب" in col_str:
                if "رقم" not in col_str: name_col = col
            elif "صف" in col_str or "فصل" in col_str or "مرحل" in col_str: class_col = col
            elif "رابط" in col_str or "شواهد" in col_str: link_col = col
            elif "رقم" in col_str or "تسلسل" in col_str or "صورة" in col_str:
                if "سجل" not in col_str and "مدني" not in col_str: num_col = col
        if id_col is None or name_col is None: return "error_col"
        db = {}
        for _, row in df.iterrows():
            val = str(row[id_col]).strip()
            sec_id = val[:-2] if val.endswith('.0') else val
            s_link = str(row[link_col]).strip() if link_col and pd.notna(row[link_col]) else "#"
            db[sec_id] = {
                "name": str(row[name_col]).strip(), 
                "class": str(row[class_col]).strip() if class_col else "المرحلة الدراسية", 
                "image_num": int(float(row[num_col])) if num_col else 0, 
                "link": s_link
            }
        return db
    return {}

students_db = load_students_from_excel()

search_id = st.text_input("", placeholder="🔍 أدخل رقم السجل المدني هنا للبحث...", key="national_id_ultimate_final_excel_v15")
btn_search = st.button("🔍 ابدأ الاستعلام والبحث")

if students_db == "error_col":
    st.error("⚠️ خطأ في ملف الإكسل: لم نتمكن من التعرف على أعمدة البيانات الأساسية.")
elif btn_search or search_id:
    if search_id:
        search_id = search_id.strip()
        if search_id in students_db:
            student = students_db[search_id]
            st.success(f"🔹 تم التحقق بنجاح! مرحباً بولي أمر الطالب: {student['name']}")
            st.info(f"📋 الصف الدراسي: {student['class']}")
            
            # زر الانتقال المباشر للرابط الفعلي المأخوذ من عمود الإكسل الجديد
            if student['link'] != "#":
                st.markdown(f"""
                <div style="text-align: right; margin-top: 15px; margin-bottom: 15px;">
                <a href="{student['link']}" target="_blank" style="background-color: #10B981; color: white; padding: 12px 22px; text-decoration: none; font-weight: bold; border-radius: 8px; box-shadow: 0px 4px 10px rgba(16, 185, 129, 0.3); display: inline-block;">
                🔗 اضغط هنا للانتقال المباشر لشواهد الطالب (محتوى الباركود)
                </a>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ هذا الطالب مسجل، ولكن لم يتم إضافة 'رابط الشواهد' الخاص به في ملف الإكسل بعد.")
            
            image_name = f"student_{student['image_num']}.png"
            image_path = os.path.join("images", image_name) if os.path.exists("images") else image_name
            if os.path.exists(image_path) or os.path.exists(image_name):
                st.image(image_path if os.path.exists(image_path) else image_name, use_container_width=True)
