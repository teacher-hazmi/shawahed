import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية للموقع
st.set_page_config(page_title="بوابة شواهد الرقمية", page_icon="🎓", layout="centered")

# إضافة كود تنسيقي محدث وقوي جداً لتدمير الكاش القديم قسرياً وتثبيت الخانة في اليمين
st.markdown("""
<style>
/* ضبط محاذاة النصوص بالكامل جهة اليمين */
.stMarkdown p, p { text-align: right !important; direction: rtl !important; }

/* 🔥 تثبيت وإجبار خانة السجل المدني بالكامل لتكون جهة اليمين غصب عن الكاش */
div[data-testid="stTextInput"] {
    width: 60% !important;
    margin-right: 0 !important;
    margin-left: auto !important;
    float: right !important; /* فرض التوجيه جهة اليمين */
}

/* تمييز خانة السجل المدني لتظهر واضحة جداً بألوان زاهية وبارزة */
div[data-baseweb="input"] { 
    direction: rtl !important; 
    text-align: right !important; 
    border: 3px solid #FF5722 !important;   /* إطار برتقالي زاهي وملفت للانتباه */
    border-radius: 10px !important; 
    background-color: #FFFFFF !important; 
    box-shadow: 0px 4px 12px rgba(255, 87, 34, 0.2) !important; /* توهج زاهي وملفت */
}

input::placeholder {
    color: #4A5568 !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 2. تصميم الترويسة العلوية بألوان زاهية ومشرقة (تدمج شعار المدارس والمادة صراحة)
st.markdown("""
<div style="background: linear-gradient(135deg, #1E3A8A, #3B82F6); padding: 25px; border-radius: 12px; margin-bottom: 30px; direction: rtl; text-align: right; box-shadow: 0px 4px 15px rgba(59, 130, 246, 0.2);">
<h1 style="color: white; font-family: 'Arial'; margin: 0; padding-right: 5px; font-size: 26px;">🎓 بوابة شواهد الرقمية</h1>
<h3 style="color: #FDE047; font-family: 'Arial'; margin: 8px 5px 0 0; font-size: 18px; font-weight: bold;">📚 مادة المهارات الرقمية</h3>
<p style="color: #E5E7EB; font-size: 15px; margin: 10px 5px 0 0; font-weight: 500;">🏫 ابتدائية أحمد بن حنبل & متوسطة الشقيري</p>
</div>
""", unsafe_allow_html=True)

# العبارة الترحيبية الدقيقة والمخصصة
st.markdown('<p style="color: #1F2937; font-size: 16px; font-weight: bold; margin-bottom: 15px;">أعزائي أولياء الأمور، لتسهيل متابعة أبنائكم في مادة مهارات رقمية ومعرفة مستواهم يرجى كتابة السجل المدني في الأسفل:</p>', unsafe_allow_html=True)

# 3. دالة ذكية مرنة لقراءة ملف إكسل وتفادي أخطاء أسماء الأعمدة
@st.cache_data
def load_students_from_excel():
    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        
        id_col, name_col, class_col, num_col = None, None, None, None
        for col in df.columns:
            col_str = str(col).strip()
            if "سجل" in col_str or "مدني" in col_str or "هوية" in col_str or "ID" in col_str.upper():
                id_col = col
            elif "اسم" in col_str or "طالب" in col_str or "NAME" in col_str.upper():
                if "رقم" not in col_str and "NUM" not in col_str.upper():
                    name_col = col
            elif "صف" in col_str or "فصل" in col_str or "درج" in col_str or "CLASS" in col_str.upper() or "GRADE" in col_str.upper():
                class_col = col
            elif "رقم" in col_str or "تسلسل" in col_str or "NUM" in col_str.upper():
                if "سجل" not in col_str and "مدني" not in col_str:
                    num_col = col
                    
        if num_col is None and name_col is not None:
            num_col = df.columns[-1]
            
        if id_col is None or name_col is None:
            return "error_col"
            
        db = {}
        for _, row in df.iterrows():
            val = str(row[id_col]).strip()
            sec_id = val[:-2] if val.endswith('.0') else val
            
            s_name = str(row[name_col]).strip() if name_col else "طالب"
            s_class = str(row[class_col]).strip() if class_col else "المرحلة المتوسطة"
            try:
                s_num = int(float(row[num_col])) if num_col else 0
            except:
                s_num = 0
                
            db[sec_id] = {
                "name": s_name,
                "class": s_class,
                "image_num": s_num
            }
        return db
    return {}

students_db = load_students_from_excel()

# 💡 تغيير المفتاح (key) قسرياً لتدمير كاش المتصفح القديم فوراً
search_id = st.text_input("", placeholder="🔍 أدخل رقم السجل المدني هنا لفتح البطاقة...", key="national_id_new_burst_v2")

if students_db == "error_col":
    st.error("⚠️ خطأ في ملف الإكسل: لم نتمكن من التعرف على أعمدة البيانات الأساسية (السجل أو الاسم).")
elif search_id:
    search_id = search_id.strip()
    if search_id in students_db:
        student = students_db[search_id]
        st.success(f"🔹 تم التحقق بنجاح! مرحباً بولي أمر الطالب: {student['name']}")
        st.info(f"📋 الصف الدراسي: {student['class']}")
        
        # عرض صورة بطاقة الطالب
        image_name = f"student_{student['image_num']}.png"
        image_path = os.path.join("images", image_name) if os.path.exists("images") else image_name
        
        if os.path.exists(image_path) or os.path.exists(image_name):
            st.image(image_path if os.path.exists(image_path) else image_name, use_container_width=True)
        else:
            st.warning(f"⚠️ تم التحقق، ولكن لم يتم العثور على ملف الصورة: {image_name}")
    else:
        st.error("❌ رقم السجل المدني غير مسجل في النظام، يرجى التأكد من الرقم والمحاولة مجدداً.")
