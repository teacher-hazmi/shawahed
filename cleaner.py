import os
import pandas as pd

def clean_and_merge_all_grades():
    output_file = "students_data.xlsx"
    
    # قائمة الملفات الجديدة والأسماء المرتبطة بها
    noor_files = [
        {"file": "noor_1m.xlsx", "default_class": "أول متوسط"},
        {"file": "noor_2m.xlsx", "default_class": "ثاني متوسط"},
        {"file": "noor_3m.xlsx", "default_class": "ثالث متوسط"}
    ]
    
    print("=== نظام شواهد: جاري فحص ودمج جميع المراحل المضافة تلقائياً ===")
    
    # قراءة البيانات السابقة لصف سادس أ إن وجدت للحفاظ عليها وتكملة الترقيم
    if os.path.exists(output_file):
        try:
            final_df = pd.read_excel(output_file)
            print(f"[i] تم العثور على قاعدة البيانات السابقة (سادس أ).")
        except:
            final_df = pd.DataFrame(columns=["السجل المدني", "اسم الطالب", "الصف", "رقم الصورة"])
    else:
        final_df = pd.DataFrame(columns=["السجل المدني", "اسم الطالب", "الصف", "رقم الصورة"])

    # معالجة كل ملف من الملفات الثلاثة الجديدة تلقائياً
    for file_info in noor_files:
        file_name = file_info["file"]
        def_class = file_info["default_class"]
        
        if not os.path.exists(file_name):
            print(f"[!] تنبيه: الملف '{file_name}' ليس موجوداً في المجلد حالياً، تم تجاوزه.")
            continue
            
        print(f"\n📂 جاري تنظيف واستخراج الطلاب من ملف: {file_name}...")
        
        try:
            df = pd.read_excel(file_name)
            ids = []
            names = []
            classes = []
            current_detected_class = def_class
            
            for index, row in df.iterrows():
                row_str = [str(x).strip() for x in row.values if pd.notna(x)]
                
                # التقاط اسم الفصل الدقيق (مثل أول متوسط أ أو ب) إذا ورد في السطر
                for item in row_str:
                    if "متوسط" in item or "ابتدائي" in item:
                        current_detected_class = item
                
                for item in row_str:
                    if item.isdigit() and len(item) == 10 and (item.startswith('1') or item.startswith('2') or item.startswith('6')):
                        current_id = item
                        for val in row.values:
                            if pd.notna(val) and isinstance(val, str) and len(val) > 10 and "وزارة" not in val and "الإدارة" not in val:
                                if val.strip() not in names and current_id not in ids:
                                    # التأكد أن الطالب غير مكرر في قاعدة البيانات العامة
                                    if final_df.empty or current_id not in final_df["السجل المدني"].astype(str).values:
                                        ids.append(current_id)
                                        names.append(val.strip())
                                        classes.append(current_detected_class)

            if len(ids) > 0:
                # حساب رقم بداية الصور الجديد بناءً على آخر رقم موجود في الجدول الشامل
                start_img_num = 1 if final_df.empty else int(final_df["رقم الصورة"].max()) + 1
                
                # إنشاء جدول للملف الحالي
                new_df = pd.DataFrame({
                    "السجل المدني": ids,
                    "اسم الطالب": names,
                    "الصف": classes,
                    "رقم الصورة": range(start_img_num, start_img_num + len(ids))
                })
                
                # دمج الجدول الجديد مع الجدول الرئيسي الشامل
                final_df = pd.concat([final_df, new_df], ignore_index=True)
                print(f"[✓] تم استخراج {len(ids)} طالب بنجاح. ترقيم صورهم يبدأ من: {start_img_num} إلى {start_img_num + len(ids) - 1}")
            else:
                print(f"[i] لم يتم العثور على طلاب جدد أو البيانات مضافة مسبقاً في هذا الملف.")
                
        except Exception as e:
            print(f"[×] حدث خطأ أثناء قراءة {file_name}: {e}")
            
    # حفظ قاعدة البيانات الشاملة المحدثة لكل الفصول والمراحل الدراسيّة
    final_df.to_excel(output_file, index=False)
    print("\n==================================================")
    print("🎉 مبروك الانتهاء من الدمج الشامل لجميع المراحل الدراسية!")
    print(f"[✓] إجمالي عدد الطلاب المسجلين في نظام موقعك الآن: {len(final_df)} طالب.")
    print("==================================================")

if __name__ == "__main__":
    clean_and_merge_all_grades()

