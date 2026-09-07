import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# قاعدة البيانات المربوطة بدقة (السجل المدني -> بيانات الطالب والبطاقة)
students_database = {
    "1170306805": {"name": "أحمد بن علي بن أحمد خواجي", "id": 1, "card_image": "student_1.png"},
    "1173444488": {"name": "المنذر بن ابراهيم بن أحمد بن نعمان", "id": 2, "card_image": "student_2.png"},
    "2392682916": {"name": "اياد هادي يحي علي", "id": 3, "card_image": "student_3.png"},
    "1175848421": {"name": "اياس بن ابراهيم بن حسين الامير", "id": 4, "card_image": "student_4.png"},
    "2401730763": {"name": "ايمن بن وحيد بن علي بن فقيه", "id": 5, "card_image": "student_5.png"},
    "1171842535": {"name": "جواد بن حسن حسين بن شولان", "id": 6, "card_image": "student_6.png"},
    "6054986601": {"name": "جواد خليل محمد البعداني", "id": 7, "card_image": "student_7.png"},
    "1173283431": {"name": "حازم بن عبده بن عايض بن صيادي", "id": 8, "card_image": "student_8.png"},
    "1167084365": {"name": "حافظ بن عبدالله بن علي بن شولان", "id": 9, "card_image": "student_9.png"},
    "1214683276": {"name": "حسن بن محسن بن حسن جمعان", "id": 10, "card_image": "student_10.png"},
    "1159694486": {"name": "خالد حسين محمد محزوم", "id": 11, "card_image": "student_11.png"},
    "2401728494": {"name": "رمزي محمد علي فقيه", "id": 12, "card_image": "student_12.png"},
    "1169574892": {"name": "ريان حسن موسى انصاري", "id": 13, "card_image": "student_13.png"},
    "1172460063": {"name": "ضيف الله بن ادريس بن احمد بن حسن جبريل بصيلي", "id": 14, "card_image": "student_14.png"},
    "1163976796": {"name": "طلال محمد جردي خبراني", "id": 15, "char_image": "student_15.png"},
    "1173719897": {"name": "عبدالحافظ رديف ناصر ريثي", "id": 16, "card_image": "student_16.png"},
    "1169588116": {"name": "عبدالرحمن احمد علي فقيه", "id": 17, "card_image": "student_17.png"},
    "1172872523": {"name": "عبدالرحمن محمد بن علي السلمى", "id": 18, "card_image": "student_18.png"},
    "1174862340": {"name": "عبدالله عطيه بن محمد نجمي", "id": 19, "card_image": "student_19.png"},
    "1174137776": {"name": "قصي يحى جبريل دريب", "id": 20, "card_image": "student_20.png"},
    "1177349022": {"name": "مؤيد عبدالله ابوشلعه دايلي", "id": 21, "card_image": "student_21.png"},
    "1173197995": {"name": "محمد حسن محمد فقيه", "id": 22, "card_image": "student_22.png"},
    "2419308123": {"name": "محمد يونس علي فقيه", "id": 23, "card_image": "student_23.png"},
    "1172665190": {"name": "مهند حسن علي شتيفي", "id": 24, "card_image": "student_24.png"},
    "1171720475": {"name": "موسى جابر علي ذماري", "id": 25, "card_image": "student_25.png"}
}

def check_access():
    national_id = entry_id.get().strip()
    if national_id in students_database:
        student = students_database[national_id]
        
        # تحديد مسار المجلد الحالي تلقائياً لضمان قراءة الصور بشكل صحيح في الماك
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, student['card_image'])
        
        success_msg = f"تم التحقق بنجاح!\n\nاسم الطالب: {student['name']}\nرقم الطالب: {student['id']}"
        messagebox.showinfo("بوابة شواهد - تم التحقق", success_msg)
        
        # محاولة فتح الصورة
        if os.path.exists(image_path):
            subprocess.run(["open", image_path])
        else:
            # إذا لم يجد امتداد .png يجرب البحث عن الامتداد الكبيرة .PNG أو العكس
            alt_path = image_path.replace(".png", ".PNG") if image_path.endswith(".png") else image_path.replace(".PNG", ".png")
            if os.path.exists(alt_path):
                subprocess.run(["open", alt_path])
            else:
                messagebox.showwarning("تنبيه", f"تم التحقق بنجاح، ولكن لم نجد الصورة بداخل المجلد.\nالمسار المتوقع:\n{image_path}")
    else:
        messagebox.showerror("خطأ في التحقق", "رقم السجل المدني غير صحيح أو غير مسجل!")

# إعداد واجهة البرنامج الرسومية
root = tk.Tk()
root.title("نظام شواهد - ماك")
root.geometry("450x250")
root.configure(bg="#f3f4f6")

label_title = tk.Label(root, text="بوابة متابعة الطالب - مدرسة أحمد بن حنبل", font=("Arial", 14, "bold"), bg="#f3f4f6", fg="#4b5563")
label_title.pack(pady=20)

label_prompt = tk.Label(root, text="الرجاء إدخال رقم السجل المدني للطالب للوصول للبطاقة:", font=("Arial", 11), bg="#f3f4f6", fg="#1f2937")
label_prompt.pack(pady=5)

entry_id = tk.Entry(root, font=("Arial", 12), width=25, justify='center')
entry_id.pack(pady=10)

btn_verify = tk.Button(root, text="التحقق وعرض البطاقة", font=("Arial", 11, "bold"), bg="#4f46e5", fg="black", width=20, command=check_access)
btn_verify.pack(pady=15)

root.mainloop()
