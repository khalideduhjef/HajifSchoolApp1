import streamlit as st
import sqlite3
import pandas as pd
import os

# --- 1. إعدادات الصفحة والتصميم الأساسي ---
st.set_page_config(
    page_title="نظام إدارة مدرسة حجيف - ولاية صلالة",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. تخصيص الواجهة لتطابق الترويسة والألوان والاتجاه العربي (RTL) ---
st.markdown("""
    <style>
    /* تطبيق الاتجاه العربي والخطوط */
    html, body, [class*="st-"], [class*="css-"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8f9fa;
    }
    
    /* الترويسة الرسمية العليا */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        padding: 10px 20px;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .header-title {
        text-align: center;
        font-weight: bold;
        color: #0d3b66;
    }
    
    /* البطاقات الإحصائية الرسمية (KPI Cards) */
    .metric-card-blue {
        background: linear-gradient(135deg, #0d3b66 0%, #1d4ed8 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-number {
        font-size: 32px;
        font-weight: bold;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 16px;
        opacity: 0.9;
    }
    
    /* أزرار التسجيل والجداول */
    .stButton>button {
        width: 100%;
        background-color: #0d3b66;
        color: white;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. إنشاء قاعدة البيانات والجداول ---
def init_db():
    conn = sqlite3.connect("school_management.db")
    cursor = conn.cursor()
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

@st.cache_data(ttl=60)
def load_student_data():
    conn = sqlite3.connect("school_management.db")
    df = pd.read_sql_query("SELECT * FROM students ORDER BY id DESC", conn)
    conn.close()
    return df

# --- 4. شاشة دخول النظام الحصري ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1 style="color: #0d3b66;">🔒 نظام إدارة مدرسة حجيف للتعليم الأساسي (5-12)</h1>
            <h3>محافظة ظفار - ولاية صلالة | إدارة أ. عامر سعيد قطن</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("أدخل كلمة المرور لدخول النظام:", type="password")
        if st.button("تسجيل الدخول"):
            if password_input == "Hajif2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    st.stop()

# --- 5. الترويسة الرسمية للعرض (شعار الوزارة والرؤية) ---
st.markdown("""
    <div class="header-container">
        <div>
            <strong style="font-size: 18px; color: #0d3b66;">وزارة التربية والتعليم</strong><br/>
            <span style="font-size: 13px; color: #555;">Ministry of Education</span>
        </div>
        <div class="header-title">
            <h2 style="margin:0; color:#0d3b66;">نظام إدارة مدرسة حجيف - ولاية صلالة</h2>
            <span style="font-size: 14px; color:#666;">مدرسة حجيف للتعليم الأساسي بنين (5-12)</span>
        </div>
        <div>
            <strong style="font-size: 18px; color: #0d3b66;">رؤية عمان 2040</strong><br/>
            <span style="font-size: 13px; color: #555;">OMAN VISION 2040</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 6. القائمة الجانبية (شريط التنقل) ---
st.sidebar.title("📌 القائمة الرئيسية")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "انتقل إلى:",
    [
        "🏠 الرئيسية",
        "🖨️ حوكمة الطباعة",
        "📋 سجل الزيارات الإشرافية",
        "👨‍🎓 بيانات الطلاب",
        "👨‍🏫 بيانات المعلمين",
        "🌐 المنصات الوزارية"
    ]
)

# --- 7. محتوى الأقسام الشامل ---

df_print = load_printing_data()
df_students = load_student_data()

total_pages = df_print["pages_count"].sum() if not df_print.empty else 0
total_print_requests = len(df_print) if not df_print.empty else 0
total_students = len(df_students) if not df_students.empty else 2254  # الرقم التقديري من التصميم

# أ. الشاشة الرئيسية (تطابق بطاقات وجداول الصورة)
if menu == "🏠 الرئيسية":
    # 3 بطاقات علوية متناسقة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card-blue">
                <div class="metric-label">إدارة بيانات الطلاب والمعلمين</div>
                <div class="metric-number">{total_students:,}</div>
                <div style="font-size:12px;">بيانات الطلاب</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="metric-card-blue">
                <div class="metric-label">تقارير الفصول والمراحل (5-12)</div>
                <div class="metric-number">7,300</div>
                <div style="font-size:12px;">تقارير الفصول و (5-12)</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="metric-card-blue">
                <div class="metric-label">إحصائيات الطباعة الشهرية</div>
                <div class="metric-number">{total_pages if total_pages > 0 else 108}</div>
                <div style="font-size:12px;">إحصائيات الطباعة</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # قسم توفير الورق الرقمي والجداول
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("توفير الورق الرقمي (OMR)")
        st.info("توفير الورق الرقمي: **125.00 OMR**")
        st.write("إحصائية الحصة والطباعة الرقمية لسنة 2026")
        
        # جدول حوكمة الطباعة السريع
        st.markdown("##### حوكمة الطباعة حسب الصفوف")
        if not df_print.empty:
            st.dataframe(df_print[["staff_name", "target_grade", "pages_count", "print_reason"]].head(5), use_container_width=True)
        else:
            sample_data = pd.DataFrame({
                "عدد الطلاب": ["مدرسة حجيف للتعليم الأساسي بنين", "مدرسة حجيف للتعليم الأساسي بنين", "مدرسة حجيف للتعليم الأساسي بنين"],
                "إنجازات الطباعة": [22, 13, 28],
                "التعليم": ["Oman", "Oman", "Oman"]
            })
            st.dataframe(sample_data, use_container_width=True)

    with c2:
        st.subheader("إدارة بيانات الطلاب والمعلمين")
        st.write("بيانات مدرسة حجيف للتعليم الأساسي بنين (5-12)")
        
        if not df_students.empty:
            st.dataframe(df_students.head(5), use_container_width=True)
        else:
            sample_students = pd.DataFrame({
                "بيانات الطلاب": ["مدرسة حجيف للتعليم الأساسي بنين (5-12)", "مدرسة حجيف بنين"],
                "الدافعية": ["الإنتاج", "سلسلة ممتازة"],
                "الطلاب": [30, 25],
                "التمهيد": ["المعلمين", "البصمية"]
            })
            st.dataframe(sample_students, use_container_width=True)

# ب. حوكمة الطباعة
elif menu == "🖨️ حوكمة الطباعة":
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

# ج. بيانات الطلاب
elif menu == "👨‍🎓 بيانات الطلاب":
    st.title("👨‍🎓 إضافة وإدارة بيانات الطلاب")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("اسم الطالب الثلاثي")
            s_grade = st.selectbox("الصف الدراسي", ["الصف الخامس", "الصف السادس", "الصف السابع", "الصف الثامن", "الصف التاسع", "الصف العاشر", "الصف الحادي عشر", "الصف الثاني عشر"])
        with col2:
            s_section = st.text_input("الفصل (مثال: 5/1)")
            s_phone = st.text_input("رقم هاتف ولي الأمر")
            
        s_submit = st.form_submit_button("تسجيل الطالب")
        if s_submit:
            conn = sqlite3.connect("school_management.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (student_name, grade_level, class_section, student_phone)
                VALUES (?, ?, ?, ?)
            ''', (s_name, s_grade, s_section, s_phone))
            conn.commit()
            conn.close()
            st.cache_data.clear()
            st.success("تم تسجيل الطالب بنجاح!")
            st.rerun()

    st.divider()
    st.dataframe(load_student_data(), use_container_width=True)

# د. الأقسام الأخرى
elif menu == "📋 سجل الزيارات الإشرافية":
    st.title("📋 سجل الزيارات الإشرافية والتقييم")
    st.info("قسم متابعة الزيارات الإشرافية للإدارة والمهتمين.")

elif menu == "👨‍🏫 بيانات المعلمين":
    st.title("👨‍🏫 سجل وإدارة بيانات الكادر التدريسي")
    st.write("قائمة المعلمين والتخصصات بمدرسة حجيف للتعليم الأساسي.")

elif menu == "🌐 المنصات الوزارية":
    st.title("🌐 الروابط والمنصات الرسمية")
    st.markdown("""
    * [البوابة التعليمية لوزارة التربية والتعليم](https://home.moe.gov.om/)
    * [منصة إجادة لقياس الأداء](https://ejada.gov.om/)
    """)

# زر النسخ الاحتياطي بالأسفل
st.sidebar.divider()
if os.path.exists("school_management.db"):
    with open("school_management.db", "rb") as fp:
        st.sidebar.download_button(
            label="💾 تنزيل نسخة احتياطية للبيانات",
            data=fp,
            file_name="Hajif_School_Backup.db",
            mime="application/x-sqlite3"
        )