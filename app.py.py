import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="نظام إدارة مدرسة حجيف (5-12)",
    page_icon="🏫",
    layout="wide"
)

# --- 2. نظام التخزين المؤقت وقاعدة البيانات ---
def init_db():
    conn = sqlite3.connect("school_management.db")
    cursor = conn.cursor()
    
    # جدول حوكمة الطباعة المرتبط بالفصول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paper_printing_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT NOT NULL,
            role_type TEXT NOT NULL,
            pages_count INTEGER NOT NULL,
            target_grade TEXT,
            target_section TEXT,
            print_reason TEXT NOT NULL,
            print_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # جدول الطلاب والفصول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            grade_level TEXT NOT NULL,
            class_section TEXT NOT NULL,
            student_phone TEXT,
            registration_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@st.cache_data(ttl=60)
def load_printing_data():
    conn = sqlite3.connect("school_management.db")
    df = pd.read_sql_query("SELECT * FROM paper_printing_logs ORDER BY id DESC", conn)
    conn.close()
    return df

# --- 3. شاشة حماية ودخول النظام ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 نظام إدارة مدرسة حجيف للتعليم الأساسي (5-12)")
    st.subheader("محافظة ظفار - ولاية صلالة | إدارة أ. عامر سعيد قطن")
    
    password_input = st.text_input("أدخل كلمة المرور لدخول النظام:", type="password")
    if st.button("تسجيل الدخول"):
        if password_input == "Hajif2026":  # كلمة المرور الافتراضية
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")
    st.stop()

# --- 4. القائمة الجانبية والترويسة ---
st.sidebar.title("🏫 مدرسة حجيف (5-12)")
st.sidebar.caption("سلطنة عمان - محافظة ظفار - ولاية صلالة")
st.sidebar.info("مدير المدرسة: أ. عامر سعيد قطن")

menu = st.sidebar.radio(
    "التنقل السريع:",
    ["اللوحة الرئيسية", "حركة وحوكمة الطباعة", "التقرير الشهري المفصل", "سجل الطلاب والفصول", "المنصات الوزارية"]
)

# --- 5. محتوى الأقسام ---

# أ. اللوحة الرئيسية
if menu == "اللوحة الرئيسية":
    st.title("📊 لوحة المؤشرات الإحصائية العامة")
    st.markdown("---")
    
    df_print = load_printing_data()
    total_pages = df_print["pages_count"].sum() if not df_print.empty else 0
    total_requests = len(df_print) if not df_print.empty else 0
    estimated_cost = total_pages * 0.015  # بالريال العماني
    
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الورق المطبوع", f"{total_pages} ورقة")
    col2.metric("عدد عمليات الطباعة", f"{total_requests} عملية")
    col3.metric("التكلفة التقديرية", f"{estimated_cost:.3f} OMR")
    
    st.divider()
    st.markdown("### 🏛️ الترويسة المؤسسية المعتمدة")
    st.write("سلطنة عمان - وزارة التربية والتعليم - المديرية العامة للتربية والتعليم بمحافظة ظفار - مدرسة حجيف للتعليم الأساسي بنين (5-12)")

# ب. حوكمة الطباعة
elif menu == "حركة وحوكمة الطباعة":
    st.title("🖨️ تسجيل وحوكمة عمليات الطباعة")
    
    with st.form("print_form"):
        col1, col2 = st.columns(2)
        with col1:
            staff_name = st.text_input("اسم المعلم / الإداري")
            role_type = st.selectbox("الصفة", ["معلم", "إداري", "رئيس قسم"])
            pages_count = st.number_input("عدد الأوراق المطلوبة", min_value=1, value=10)
        with col2:
            target_grade = st.selectbox("المرحلة الدراسية", ["إداري / عام", "الصف الخامس", "الصف السادس", "الصف السابع", "الصف الثامن", "الصف التاسع", "الصف العاشر", "الصف الحادي عشر", "الصف الثاني عشر"])
            target_section = st.text_input("الفصل الدراسي (مثال: 5/1)")
            print_reason = st.selectbox("سبب الطباعة", ["اختبار قصير", "ورقة عمل", "أنشطة إثرائية", "سجلات إدارية"])
            
        submitted = st.form_submit_button("حفظ وحوكمة الطلب")
        
        if submitted:
            conn = sqlite3.connect("school_management.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO paper_printing_logs (staff_name, role_type, pages_count, target_grade, target_section, print_reason, print_date)
                VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
            ''', (staff_name, role_type, pages_count, target_grade, target_section, print_reason))
            conn.commit()
            conn.close()
            st.cache_data.clear()
            st.success("تم تسجيل عملية الطباعة بنجاح!")
            st.rerun()

    st.divider()
    st.subheader("📋 سجل الطباعة المعتمد")
    st.dataframe(load_printing_data(), use_container_width=True)

# ج. التقرير الشهري المفصل
elif menu == "التقرير الشهري المفصل":
    st.title("📅 التقرير الشهري لاستهلاك الورق")
    
    selected_year = st.selectbox("السنة", [2026, 2027], index=0)
    months_dict = {"يناير (1)": "01", "فبراير (2)": "02", "مارس (3)": "03", "أبريل (4)": "04", "مايو (5)": "05", "يونيو (6)": "06", "يوليو (7)": "07", "أغسطس (8)": "08", "سبتمبر (9)": "09", "أكتوبر (10)": "10", "نوفمبر (11)": "11", "ديسمبر (12)": "12"}
    selected_month_name = st.selectbox("الشهر", list(months_dict.keys()))
    
    target_date = f"{selected_year}-{months_dict[selected_month_name]}"
    
    conn = sqlite3.connect("school_management.db")
    df_m = pd.read_sql_query(f"SELECT * FROM paper_printing_logs WHERE print_date LIKE '{target_date}%'", conn)
    conn.close()
    
    if not df_m.empty:
        st.write(f"إجمالي استهلاك هذا الشهر: **{df_m['pages_count'].sum()}** ورقة.")
        st.dataframe(df_m, use_container_width=True)
        
        # تحميل CSV
        csv = df_m.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل التقرير كملف Excel/CSV", data=csv, file_name=f"Report_{target_date}.csv", mime="text/csv")
    else:
        st.info("لا توجد سجلات لهذا الشهر المحدد.")

# د. سجل الطلاب
elif menu == "سجل الطلاب والفصول":
    st.title("👨‍🎓 إدارة الطلاب والمراحل (5-12)")
    st.write("قسم خاص بتسجيل ومتابعة طلاب المدرسة وحفط فصولهم.")

# هـ. المنصات الوزارية
elif menu == "المنصات الوزارية":
    st.title("🌐 الروابط والمنصات الرسمية")
    st.markdown("""
    * [البوابة التعليمية لوزارة التربية والتعليم](https://home.moe.gov.om/)
    * [منصة إجادة لقياس الأداء](https://ejada.gov.om/)
    """)

# زر النسخ الاحتياطي في أسفل القائمة الجانبية
st.sidebar.divider()
if os.path.exists("school_management.db"):
    with open("school_management.db", "rb") as fp:
        st.sidebar.download_button(
            label="💾 تنزيل نسخة احتياطية للبيانات",
            data=fp,
            file_name="Hajif_School_Backup.db",
            mime="application/x-sqlite3"
        )