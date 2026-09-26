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

# --- 2. تهيئة قاعدة البيانات والتخزين المؤقت ---
def init_db():
    conn = sqlite3.connect("school_management.db")
    cursor = conn.cursor()
    
    # جدول حوكمة الطباعة الورقية للمراحل (5-12)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paper_printing_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT NOT NULL,
            role_type TEXT NOT NULL,
            pages_count INTEGER NOT NULL,
            target_grade TEXT NOT NULL,
            target_section TEXT,
            print_reason TEXT NOT NULL,
            print_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # جدول بيانات الطلاب
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

# --- 3. نظام حماية ودخول النظام بكلمة مرور ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 نظام إدارة مدرسة حجيف للتعليم الأساسي (5-12)")
    st.caption("سلطنة عمان - محافظة ظفار - ولاية صلالة | بإدارة أ. عامر سعيد قطن")
    st.markdown("---")
    
    password_input = st.text_input("أدخل كلمة المرور الخاصة بالإدارة للدخول:", type="password")
    if st.button("تسجيل الدخول للنظام"):
        if password_input == "Hajif2026":
            st.session_state["authenticated"] = True
            st.success("تم التحقق بنجاح! جاري تحويلك...")
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة! يرجى المحاولة مرة أخرى.")
    st.stop()

# --- 4. القائمة الجانبية المعتمدة ---
st.sidebar.title("🏫 مدرسة حجيف (5-12)")
st.sidebar.caption("المديرية العامة للتربية والتعليم بمحافظة ظفار")
st.sidebar.info("مدير المدرسة: أ. عامر سعيد قطن")

menu = st.sidebar.radio(
    "التنقل المباشر:",
    ["اللوحة الرئيسية", "حركة وحوكمة الطباعة", "التقرير الشهري المفصل", "سجل الطلاب والمراحل", "المنصات الوزارية"]
)

# --- 5. محتوى أقسام البرنامج ---

# أ. اللوحة الرئيسية
if menu == "اللوحة الرئيسية":
    st.title("📊 لوحة المؤشرات الإحصائية العامة")
    st.caption("مدرسة حجيف للتعليم الأساسي بنين (5-12) - ولاية صلالة")
    st.markdown("---")
    
    df_print = load_printing_data()
    total_pages = df_print["pages_count"].sum() if not df_print.empty else 0
    total_requests = len(df_print) if not df_print.empty else 0
    estimated_cost = total_pages * 0.015  # بالريال العماني
    
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الورق المطبوع", f"{total_pages} ورقة")
    col2.metric("إجمالي طلبات الطباعة", f"{total_requests} طلب")
    col3.metric("التكلفة التقديرية (OMR)", f"{estimated_cost:.3f} ر.ع")
    
    st.divider()
    st.markdown("### 🏛️ الترويسة المؤسسية الرسمية")
    st.info("سلطنة عمان | وزارة التربية والتعليم | المديرية العامة للتربية والتعليم بمحافظة ظفار | مدرسة حجيف للتعليم الأساسي بنين (5-12)")

# ب. حركة وحوكمة الطباعة
elif menu == "حركة وحوكمة الطباعة":
    st.title("🖨️ تسجيل وحوكمة عمليات الطباعة")
    st.write("استمارة تسجيل استهلاك الأوراق والطباعة المربوطة بالفصول والمراحل الدراسية.")
    
    with st.form("print_form"):
        col1, col2 = st.columns(2)
        with col1:
            staff_name = st.text_input("اسم المعلم / الإداري")
            role_type = st.selectbox("الصفة الوظيفية", ["معلم", "إداري", "رئيس قسم", "أخصائي"])
            pages_count = st.number_input("عدد الأوراق المطلوبة", min_value=1, value=10)
        with col2:
            target_grade = st.selectbox("المرحلة الدراسية", [
                "عام / إداري", 
                "الصف الخامس", "الصف السادس", "الصف السابع", "الصف الثامن", 
                "الصف التاسع", "الصف العاشر", "الصف الحادي عشر", "الصف الثاني عشر"
            ])
            target_section = st.text_input("الفصل الدراسي (مثال: 5/1)")
            print_reason = st.selectbox("سبب الطباعة", ["اختبار قصير", "ورقة عمل", "أنشطة إثرائية", "سجلات إدارية", "امتحانات نهائية"])
            
        submitted = st.form_submit_button("حفظ وحوكمة الطلب")
        
        if submitted:
            if staff_name.strip() == "":
                st.error("يرجى إدخال اسم المعلم أو الإداري.")
            else:
                conn = sqlite3.connect("school_management.db")
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO paper_printing_logs (staff_name, role_type, pages_count, target_grade, target_section, print_reason, print_date)
                    VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
                ''', (staff_name, role_type, pages_count, target_grade, target_section, print_reason))
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.success("تم تسجيل عملية الطباعة بنجاح وحفظها في قاعدة البيانات!")
                st.rerun()

    st.divider()
    st.subheader("📋 سجل الطباعة العام")
    st.dataframe(load_printing_data(), use_container_width=True)

# ج. التقرير الشهري المفصل
elif menu == "التقرير الشهري المفصل":
    st.title("📅 التقرير الشهري المعتمد لاستهلاك الورق")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_year = st.selectbox("اختر السنة", [2026, 2027, 2028], index=0)
    with col_f2:
        months_dict = {
            "يناير (1)": "01", "فبراير (2)": "02", "مارس (3)": "03", "أبريل (4)": "04",
            "مايو (5)": "05", "يونيو (6)": "06", "يوليو (7)": "07", "أغسطس (8)": "08",
            "سبتمبر (9)": "09", "أكتوبر (10)": "10", "نوفمبر (11)": "11", "ديسمبر (12)": "12"
        }
        selected_month_name = st.selectbox("اختر الشهر", list(months_dict.keys()))
    
    target_date = f"{selected_year}-{months_dict[selected_month_name]}"
    
    conn = sqlite3.connect("school_management.db")
    df_m = pd.read_sql_query(f"SELECT * FROM paper_printing_logs WHERE print_date LIKE '{target_date}%'", conn)
    conn.close()
    
    if not df_m.empty:
        total_m_pages = df_m['pages_count'].sum()
        st.success(f"إجمالي استهلاك الشهر المحدد ({selected_month_name}): **{total_m_pages}** ورقة.")
        st.dataframe(df_m, use_container_width=True)
        
        csv_data = df_m.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل التقرير الشهري بصيغة CSV/Excel",
            data=csv_data,
            file_name=f"Hajif_Report_{target_date}.csv",
            mime="text/csv"
        )
    else:
        st.info("لا توجد أي سجلات طباعة مسجلة خلال هذا الشهر المحدد.")

# د. سجل الطلاب والمراحل
elif menu == "سجل الطلاب والمراحل":
    st.title("👨‍🎓 إدارة بيانات الطلاب والمراحل (5-12)")
    st.write("قسم مخصص لحصر وتتبع طلاب مدرسة حجيف موزعين على الفصول والمراحل الدراسية.")

# هـ. المنصات الوزارية
elif menu == "المنصات الوزارية":
    st.title("🌐 الروابط والمنصات الوزارية الرسمية")
    st.markdown("""
    * 🔗 [البوابة التعليمية لوزارة التربية والتعليم](https://home.moe.gov.om/)
    * 🔗 [منصة إجادة لقياس الأداء المؤسسي والفردي](https://ejada.gov.om/)
    """)

# --- 6. زر النسخ الاحتياطي لقاعدة البيانات ---
st.sidebar.divider()
if os.path.exists("school_management.db"):
    with open("school_management.db", "rb") as fp:
        st.sidebar.download_button(
            label="💾 تحميل نسخة احتياطية من البيانات",
            data=fp,
            file_name="Hajif_School_Backup.db",
            mime="application/x-sqlite3"
        )