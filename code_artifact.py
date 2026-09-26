import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

# مكتبات اختياريّة لمعالجة Word و PDF إن توفرت في البيئة
try:
    import docx
except ImportError:
    docx = None

try:
    import pypdf
except ImportError:
    pypdf = None

# ==========================================
# 1. إعدادات الصفحة الأساسية والتنسيق RTL
# ==========================================
st.set_page_config(
    page_title="نظام إدارة مدرسة حجيف الذكي (5-12)",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    html, body, [class*="st-"], [class*="css-"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    section[data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8f9fa;
    }
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .smart-card {
        background: #ffffff;
        border-right: 5px solid #0d3b66;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    .smart-number { font-size: 28px; font-weight: bold; color: #0d3b66; }
    .smart-label { font-size: 14px; color: #555; }
    .stButton>button { width: 100%; background-color: #0d3b66; color: white; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. بناء وقواعد البيانات المحلية SQLite
# ==========================================
DB_FILE = "school_management.db"

def init_all_databases():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, section TEXT, 
        guardian_phone TEXT, national_id TEXT, parent_name TEXT, status TEXT DEFAULT 'نشط', notes TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT, staff_name TEXT, job_title TEXT, subject TEXT, 
        phone TEXT, email TEXT, status TEXT DEFAULT 'على رأس العمل'
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, section TEXT, 
        date TEXT, status TEXT, delay_minutes INTEGER DEFAULT 0, reason TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade_level TEXT, subject TEXT, 
        short_test REAL, activity REAL, final_exam REAL, total REAL, result_status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS behavior (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, date TEXT, 
        behavior_type TEXT, action_taken TEXT, notes TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_title TEXT, assigned_to TEXT, 
        due_date TEXT, status TEXT DEFAULT 'قيد التنفيذ', priority TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, event_type TEXT, 
        event_date TEXT, minutes_text TEXT, recommendations TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, category TEXT, 
        quantity INTEGER, condition_status TEXT, location TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doc_title TEXT, category TEXT, 
        ref_date TEXT, file_name TEXT, notes TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_all_databases()

@st.cache_data(ttl=5)
def fetch_data(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()
    st.cache_data.clear()

# ==========================================
# 3. دالة الاستيراد الشاملة (Excel, Word, PDF)
# ==========================================
def parse_uploaded_file(uploaded_file):
    filename = uploaded_file.name.lower()
    records = []
    
    if filename.endswith(".xlsx") or filename.endswith(".xls") or filename.endswith(".csv"):
        df = pd.read_excel(uploaded_file) if (filename.endswith(".xlsx") or filename.endswith(".xls")) else pd.read_csv(uploaded_file)
        return df
        
    elif filename.endswith(".docx"):
        if docx is None:
            st.error("مكتبة python-docx غير مثبتة لتشغيل ملفات Word.")
            return None
        doc = docx.Document(uploaded_file)
        # محاولة قراءة الجداول في مستند Word
        for table in doc.tables:
            for row in table.rows[1:]: # يتخطى العناوين
                cols = [cell.text.strip() for cell in row.cells]
                if cols:
                    records.append(cols)
        if not records: # إذا لم تكن البيانات جدولاً، يقرأ الفقرات أسطراً
            for p in doc.paragraphs:
                if p.text.strip():
                    records.append([p.text.strip()])
        return pd.DataFrame(records)

    elif filename.endswith(".pdf"):
        if pypdf is None:
            st.error("مكتبة pypdf غير مثبتة لتشغيل ملفات PDF.")
            return None
        reader = pypdf.PdfReader(uploaded_file)
        text_lines = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                for line in t.split("\n"):
                    if line.strip():
                        text_lines.append([line.strip()])
        return pd.DataFrame(text_lines, columns=["السطر/الاسم المستخرج"])
    
    return None

# ==========================================
# 4. تسجيل الدخول والصلاحيات
# ==========================================
USER_ROLES = {
    "مدير المدرسة": "Hajif2026",
    "مساعد المدير": "Assistant2026",
    "المعلم": "Teacher2026",
    "الموظف الإداري": "Admin2026",
    "الأخصائي الاجتماعي": "Social2026"
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = ""

if not st.session_state["authenticated"]:
    st.markdown("""
        <div style="text-align: center; padding: 40px 10px;">
            <h1 style="color: #0d3b66;">🏫 مدرسة حجيف للتعليم الأساسي بنين (5-12)</h1>
            <h3>سلطنة عمان - محافظة ظفار - ولاية صلالة</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 تسجيل الدخول")
        role_selected = st.selectbox("اختر الصلاحية:", list(USER_ROLES.keys()))
        password_input = st.text_input("كلمة المرور:", type="password")
        if st.button("تسجيل الدخول"):
            if password_input == USER_ROLES[role_selected]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = role_selected
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    st.stop()

st.markdown(f"""
    <div class="header-bar">
        <div>
            <h3 style="margin:0; color:white;">مدرسة حجيف للتعليم الأساسي بنين (5-12)</h3>
            <small>محافظة ظفار — ولاية صلالة</small>
        </div>
        <div><span style="background:#ffffff22; padding:5px 12px; border-radius:20px;">👤 {st.session_state['user_role']}</span></div>
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي
st.sidebar.title("📌 الأقسام الرئيسية")
menu = st.sidebar.radio("انتقل إلى:", [
    "1️⃣ الواجهة الرئيسية والقرارات الذكية",
    "2️⃣ إدارة الطلبة (استيراد/تنزيل)",
    "3️⃣ إدارة المعلمين (استيراد/تنزيل)",
    "4️⃣ إدارة الحضور والغياب",
    "5️⃣ إدارة التحصيل الدراسي",
    "6️⃣ السلوك والانضباط الطلابي",
    "7️⃣ المهام والمتابعات المدرسية",
    "8️⃣ الفعاليات والاجتماعات",
    "9️⃣ إدارة المخزون والممتلكات",
    "🔟 التقارير وتنزيل البيانات الشاملة",
    "1️⃣1️⃣ إدارة المستندات والأرشيف",
    "1️⃣2️⃣ التواصل والخدمات الإلكترونية",
    "1️⃣3️⃣ إدارة المستخدمين والصلاحيات",
    "1️⃣4️⃣ النسخ الاحتياطي واستعادة البيانات",
    "1️⃣5️⃣ إعدادات النظام"
])

# ------------------------------------------
# 1. الواجهة الرئيسية
# ------------------------------------------
if menu == "1️⃣ الواجهة الرئيسية والقرارات الذكية":
    st.title("📊 مركز القرارات الذكية والمؤشرات المدرسية")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="smart-card"><div class="smart-number">{fetch_data("SELECT COUNT(*) as c FROM students")["c"][0]}</div><div class="smart-label">إجمالي الطلبة</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="smart-card"><div class="smart-number">{fetch_data("SELECT COUNT(*) as c FROM staff")["c"][0]}</div><div class="smart-label">الكادر التعليمي</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="smart-card"><div class="smart-number">{fetch_data("SELECT COUNT(*) as c FROM attendance WHERE status=\'غائب\'")["c"][0]}</div><div class="smart-label">حالات الغياب</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="smart-card"><div class="smart-number">{fetch_data("SELECT COUNT(*) as c FROM tasks WHERE status=\'قيد التنفيذ\'")["c"][0]}</div><div class="smart-label">مهام جارية</div></div>', unsafe_allow_html=True)

# ------------------------------------------
# 2. إدارة الطلبة
# ------------------------------------------
elif menu == "2️⃣ إدارة الطلبة (استيراد/تنزيل)":
    st.title("👨‍🎓 إدارة الطلبة واستيراد البيانات والتنزيل")
    
    tab1, tab2, tab3 = st.tabs(["📋 عرض البيانات والتنزيل", "➕ إضافة طالب يدوي", "📥 استيراد من (Excel / Word / PDF)"])
    
    with tab1:
        st.subheader("سجل الطلبة الحالي")
        df_st = fetch_data("SELECT * FROM students")
        st.dataframe(df_st, use_container_width=True)
        if not df_st.empty:
            csv = df_st.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تنزيل بيانات الطلبة (Excel / CSV)", data=csv, file_name="students_data.csv", mime="text/csv")
            
    with tab2:
        with st.form("add_st_form"):
            s_name = st.text_input("اسم الطالب الرباعي")
            s_grade = st.selectbox("الصف", [f"الصف {i}" for i in ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]])
            s_sec = st.text_input("الشعبة (مثال: 5/1)")
            s_phone = st.text_input("هاتف ولي الأمر")
            if st.form_submit_button("حفظ الطالب"):
                execute_query("INSERT INTO students (student_name, grade, section, guardian_phone) VALUES (?, ?, ?, ?)", (s_name, s_grade, s_sec, s_phone))
                st.success("تم الحفظ بنجاح!")
                st.rerun()

    with tab3:
        st.subheader("📥 استيراد قائمة الطلبة من ملف خارجي")
        up_file = st.file_uploader("اختر ملف (Excel, Word, أو PDF)", type=["xlsx", "xls", "csv", "docx", "pdf"])
        if up_file:
            parsed_df = parse_uploaded_file(up_file)
            if parsed_df is not None:
                st.write("🔍 معاينة البيانات المستخرجة من الملف:")
                st.dataframe(parsed_df, use_container_width=True)
                
                if st.button("حفظ هذه البيانات في سجل الطلبة"):
                    # إدخال تلقائي بسيط
                    for index, row in parsed_df.iterrows():
                        name_val = str(row.iloc[0]) if len(row) > 0 else "غير محدد"
                        grade_val = str(row.iloc[1]) if len(row) > 1 else "الصف الخامس"
                        execute_query("INSERT INTO students (student_name, grade) VALUES (?, ?)", (name_val, grade_val))
                    st.success("تم استيراد وحفظ كافة الطلبة بنجاح!")
                    st.rerun()

# ------------------------------------------
# 3. إدارة المعلمين
# ------------------------------------------
elif menu == "3️⃣ إدارة المعلمين (استيراد/تنزيل)":
    st.title("👨‍🏫 إدارة الكادر التعليمي واستيراد البيانات")
    
    tab1, tab2, tab3 = st.tabs(["📋 سجل المعلمين والتنزيل", "➕ إضافة معلم جديد", "📥 استيراد كادر من (Excel / Word / PDF)"])
    
    with tab1:
        df_tf = fetch_data("SELECT * FROM staff")
        st.dataframe(df_tf, use_container_width=True)
        if not df_tf.empty:
            csv_tf = df_tf.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تنزيل سجل المعلمين (Excel / CSV)", data=csv_tf, file_name="teachers_data.csv", mime="text/csv")

    with tab2:
        with st.form("add_tf"):
            t_name = st.text_input("اسم المعلم / الموظف")
            t_job = st.selectbox("المسمى الوظيفي", ["معلم", "معلم أول", "إداري", "أخصائي اجتماعي"])
            t_sub = st.text_input("التخصص / المادة")
            t_phone = st.text_input("رقم الهاتف")
            if st.form_submit_button("إضافة"):
                execute_query("INSERT INTO staff (staff_name, job_title, subject, phone) VALUES (?, ?, ?, ?)", (t_name, t_job, t_sub, t_phone))
                st.success("تم الحفظ!")
                st.rerun()

    with tab3:
        st.subheader("📥 استيراد كادر المعلمين")
        up_file = st.file_uploader("اختر ملف المعلمين (Excel, Word, PDF)", type=["xlsx", "xls", "csv", "docx", "pdf"], key="staff_file")
        if up_file:
            parsed_df = parse_uploaded_file(up_file)
            if parsed_df is not None:
                st.write("🔍 معاينة المحتوى المستخرج:")
                st.dataframe(parsed_df, use_container_width=True)
                if st.button("حفظ بيانات المعلمين"):
                    for index, row in parsed_df.iterrows():
                        name_val = str(row.iloc[0]) if len(row) > 0 else "غير محدد"
                        job_val = str(row.iloc[1]) if len(row) > 1 else "معلم"
                        execute_query("INSERT INTO staff (staff_name, job_title) VALUES (?, ?)", (name_val, job_val))
                    st.success("تم استيراد وحفظ المعلمين بنجاح!")
                    st.rerun()

# ------------------------------------------
# 4. باقي الأقسام التفاعلية
# ------------------------------------------
elif menu == "4️⃣ إدارة الحضور والغياب":
    st.title("⏱️ تسجيل ومتابعة الحضور والغياب")
    st.dataframe(fetch_data("SELECT * FROM attendance"), use_container_width=True)

elif menu == "5️⃣ إدارة التحصيل الدراسي":
    st.title("📈 رصد الدرجات وتحليل النتائج الأكاديمية")
    st.dataframe(fetch_data("SELECT * FROM grades"), use_container_width=True)

elif menu == "6️⃣ السلوك والانضباط الطلابي":
    st.title("🛡️ سجل السلوك والانضباط")
    st.dataframe(fetch_data("SELECT * FROM behavior"), use_container_width=True)

elif menu == "7️⃣ المهام والمتابعات المدرسية":
    st.title("📋 إدارة وتوزيع المهام المدرسية")
    st.dataframe(fetch_data("SELECT * FROM tasks"), use_container_width=True)

elif menu == "8️⃣ الفعاليات والاجتماعات":
    st.title("📅 الفعاليات ومحاضر الاجتماعات")
    st.dataframe(fetch_data("SELECT * FROM events"), use_container_width=True)

elif menu == "9️⃣ إدارة المخزون والممتلكات":
    st.title("📦 إدارة المخزون والممتلكات")
    st.dataframe(fetch_data("SELECT * FROM inventory"), use_container_width=True)

elif menu == "🔟 التقارير وتنزيل البيانات الشاملة":
    st.title("📊 مركز استخراج وتنزيل كافة البيانات")
    rep_choice = st.selectbox("اختر البيانات المراد تنزيلها:", ["بيانات الطلبة", "بيانات المعلمين", "سجل الحضور والغياب", "سجل الدرجات والتحصيل"])
    
    target_table = "students" if rep_choice == "بيانات الطلبة" else "staff" if rep_choice == "بيانات المعلمين" else "attendance" if rep_choice == "سجل الحضور والغياب" else "grades"
    df_export = fetch_data(f"SELECT * FROM {target_table}")
    
    st.dataframe(df_export, use_container_width=True)
    if not df_export.empty:
        csv_data = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button(f"📥 تنزيل {rep_choice} فوراً (ملف Excel/CSV)", data=csv_data, file_name=f"{target_table}_export.csv", mime="text/csv")

elif menu == "1️⃣1️⃣ إدارة المستندات والأرشيف":
    st.title("📂 الأرشيف الإلكتروني المدرسي")
    st.dataframe(fetch_data("SELECT * FROM archive"), use_container_width=True)

elif menu == "1️⃣2️⃣ التواصل والخدمات الإلكترونية":
    st.title("📲 التواصل السريع عبر WhatsApp")
    p_num = st.text_input("رقم هاتف ولي الأمر مع المفتاح (e.g. 968XXXXXXXX):")
    msg = st.text_area("نص الرسالة:", value="السلام عليكم، نود إفادتكم بمتابعة مستوى الطالب في مدرسة حجيف.")
    if p_num:
        st.markdown(f'<a href="https://api.whatsapp.com/send?phone={p_num}&text={msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">🟢 إرسال عبر WhatsApp</button></a>', unsafe_allow_html=True)

elif menu == "1️⃣3️⃣ إدارة المستخدمين والصلاحيات":
    st.title("🔐 الصلاحيات وسجل المستخدمين")
    st.json(USER_ROLES)

elif menu == "1️⃣4️⃣ النسخ الاحتياطي واستعادة البيانات":
    st.title("💾 النسخ الاحتياطي للأمان")
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as fp:
            st.download_button("📥 تنزيل قاعدة البيانات الحالية كاملة (SQLite)", data=fp, file_name="Hajif_Backup.db", mime="application/x-sqlite3")

elif menu == "1️⃣5️⃣ إعدادات النظام":
    st.title("⚙️ إعدادات مدرسة حجيف (5-12)")
    st.info("النظام جاهز ومعد وفق اشتراطات مدرسة حجيف للتعليم الأساسي - سلطنة عمان.")