import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية للموقع
st.set_page_config(page_title="بوابة شواهد الرقمية", page_icon="🎓", layout="centered")

# إضافة كود تنسيقي لجعل واجهة الموقع تدعم اللغة العربية بالكامل وتبرز خانة السجل المدني
st.markdown("""
<style>
/* دعم اللغة العربية والمحاذاة لليمين */
.stTextInput align-items { direction: rtl !important; text-align: right !important; }
.st_label { text-align: right !important; direction: rtl !important; width: 100%; }
.stButton button { direction: rtl !important; }

/* تمييز خانة السجل المدني لتصبح واضحة وبارزة جداً لأولياء الأمور */
div[data-baseweb="input"] { 
    direction: rtl !important; 
    text-align: right !important; 
    border: 2px solid #1E3A8A !important;   /* إطار كحلي عريض وفخم */
    border-radius: 8px !important;         /* انحناء أنيق للحواف */
    background-color: #FFFFFF !important;   /* فرض خلفية بيضاء ناصعة مكان الكتابة */
}
</style>
""", unsafe_allow_html=True)

# 2. تصميم الترويسة العلوية باللون الأزرق الملكي الفخم
st.markdown("""
<div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 25px; direction: rtl;">
<h1 style="text-align: right; color: white; font-family: 'Arial'; margin: 0; padding-right: 10px;">🎓 بوابة شواهد Educational Portal</h1>
<p style="text-align: right; color: #E5E7EB; font-size: 16px; margin: 10px 10px 0 0; padding-right: 10px;">نظام الاستعلام الذكي عن بطاقات المتابعة والنتائج</p>
</div>
""", unsafe_allow_html=True)

# العبارة الترحيبية
st.markdown('<p style="text-align: right; color: #4B5563; font-size: 15px; direction: rtl; font-weight: bold;">أعزائي أولياء الأمور، لتسهيل متابعة أبنائكم في مادة مهارات رقمية ومعرفة مستواهم يرجى كتابة السجل المدني في الأسفل:</p>', unsafe_allow_html=True)

# 3. دالة ذكية خارقة لقراءة ملف إكسل وتفادي أخطاء أسماء الأعمدة بالكامل
@st.cache_data
def load_students_from_excel():
    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        
        # البحث الذكي عن الأعمدة بناءً على الكلمات المفتاحية لتفادي المسافات والأخطاء الإملائية
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
                    
        # حل احتياطي لو لم يجد عمود رقم الطالب صراحة
        if num_col is None and name_col is not None:
            num_col = df.columns[-1] # افترض العمود الأخير
            
        if id_col is None or name_col is None:
            return "error_col"
            
        db = {}
        for _, row in df.iterrows():
            val = str(row[id_col]).strip()
            sec_id = val.split('.')[0] if '.' in val else val
            
            # جلب البيانات بأمان وتفادي غياب أي عمود
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

# خانة إدخال السجل المدني النظيفة والواضحة
search_id = st.text_input("", placeholder="أدخل رقم السجل المدني هنا...", key="national_id_input")

if students_db == "error_col":
    st.error("⚠️ خطأ في ملف الإكسل: لم نتمكن من التعرف على أعمدة البيانات الأساسية (السجل أو الاسم). يرجى مراجعة الجدول.")
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
