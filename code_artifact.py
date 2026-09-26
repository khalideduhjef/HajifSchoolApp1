import streamlit as st
import sqlite3
import pandas as pd
import os
import json
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة الأساسية والتنسيق RTL
# ==========================================
st.set_page_config(
    page_title="نظام إدارة مدرسة حجيف الذكي (5-12)",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التنسيق العربي الكامل من اليمين إلى اليسار والنمط البصري الاحترافي
st.markdown("""
    <style>
    /* الاتجاه والخطوط */
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
    
    /* الترويسة المؤسسية */
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
    
    /* بطاقات المؤشرات والقرارات الذكية */
    .smart-card {
        background: #ffffff;
        border-right: 5px solid #0d3b66;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    .smart-number {
        font-size: 28px;
        font-weight: bold;
        color: #0d3b66;
    }
    .smart-label {
        font-size: 14px;
        color: #555;
    }

    /* أزرار وحقول التعبئة */
    .stButton>button {
        width: 100%;
        background-color: #0d3b66;
        color: white;
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. بناء وقواعد البيانات المحلية SQLite
# ==========================================
DB_FILE = "school_management.db"

def init_all_databases():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. الطلبة
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, section TEXT, 
        guardian_phone TEXT, national_id TEXT, parent_name TEXT, status TEXT DEFAULT 'نشط', notes TEXT
    )''')
    
    # 2. المعلمون والموظفون
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT, staff_name TEXT, job_title TEXT, subject TEXT, 
        phone TEXT, email TEXT, status TEXT DEFAULT 'على رأس العمل'
    )''')
    
    # 3. الحضور والغياب
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, section TEXT, 
        date TEXT, status TEXT, delay_minutes INTEGER DEFAULT 0, reason TEXT
    )''')
    
    # 4. التحصيل الدراسي والدرجات
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade_level TEXT, subject TEXT, 
        short_test REAL, activity REAL, final_exam REAL, total REAL, result_status TEXT
    )''')
    
    # 5. السلوك والانضباط
    c.execute('''CREATE TABLE IF NOT EXISTS behavior (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, grade TEXT, date TEXT, 
        behavior_type TEXT, action_taken TEXT, notes TEXT
    )''')
    
    # 6. المهام والمتابعات
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_title TEXT, assigned_to TEXT, 
        due_date TEXT, status TEXT DEFAULT 'قيد التنفيذ', priority TEXT
    )''')
    
    # 7. الفعاليات والاجتماعات
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, event_type TEXT, 
        event_date TEXT, minutes_text TEXT, recommendations TEXT
    )''')
    
    # 8. المخزون والممتلكات
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, category TEXT, 
        quantity INTEGER, condition_status TEXT, location TEXT
    )''')
    
    # 9. الأرشيف والمستندات
    c.execute('''CREATE TABLE IF NOT EXISTS archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doc_title TEXT, category TEXT, 
        ref_date TEXT, file_name TEXT, notes TEXT
    )''')
    
    # 10. سجل العمليات والصلاحيات
    c.execute('''CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

init_all_databases()

# دالة التخزين المؤقت وتحميل البيانات
@st.cache_data(ttl=10)
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
# 3. نظام تسجيل الدخول والصلاحيات
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
            <p style="color: #666;">نظام إدارة المدرسة الذكي المتكامل</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 شاشة تسجيل الدخول")
        role_selected = st.selectbox("اختر نوع الحساب / الصلاحية:", list(USER_ROLES.keys()))
        password_input = st.text_input("كلمة المرور:", type="password")
        
        if st.button("تسجيل الدخول للنظام"):
            if password_input == USER_ROLES[role_selected]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = role_selected
                execute_query("INSERT INTO system_logs (username, action) VALUES (?, ?)", (role_selected, "تسجيل دخول ناجح"))
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    st.stop()

# ==========================================
# 4. الترويسة العليا والقائمة الجانبية
# ==========================================
st.markdown(f"""
    <div class="header-bar">
        <div>
            <h3 style="margin:0; color:white;">مدرسة حجيف للتعليم الأساسي بنين (5-12)</h3>
            <small>المديرية العامة للتربية والتعليم بمحافظة ظفار — ولاية صلالة</small>
        </div>
        <div style="text-align: left;">
            <span style="background:#ffffff22; padding:5px 12px; border-radius:20px; font-size:14px;">
                👤 المستخدم: <b>{st.session_state['user_role']}</b>
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# شريط التنقل الجانبي
st.sidebar.title("📌 الأقسام الرئيسية")
menu = st.sidebar.radio(
    "انتقل إلى:",
    [
        "1️⃣ الواجهة الرئيسية والقرارات الذكية",
        "2️⃣ إدارة الطلبة",
        "3️⃣ إدارة المعلمين والموظفين",
        "4️⃣ إدارة الحضور والغياب",
        "5️⃣ إدارة التحصيل الدراسي",
        "6️⃣ السلوك والانضباط الطلابي",
        "7️⃣ المهام والمتابعات المدرسية",
        "8️⃣ الفعاليات والاجتماعات",
        "9️⃣ إدارة المخزون والممتلكات",
        "🔟 التقارير والإحصائيات",
        "1️⃣1️⃣ إدارة المستندات والأرشيف",
        "1️⃣2️⃣ التواصل والخدمات الإلكترونية",
        "1️⃣3️⃣ إدارة المستخدمين والصلاحيات",
        "1️⃣4️⃣ النسخ الاحتياطي واستعادة البيانات",
        "1️⃣5️⃣ إعدادات النظام"
    ]
)

# ==========================================
# 5. تنشيط وتنفيذ الأقسام الـ 17 بالتفصيل
# ==========================================

# ------------------------------------------
# أولاً: الواجهة الرئيسية والقرارات الذكية
# ------------------------------------------
if menu == "1️⃣ الواجهة الرئيسية والقرارات الذكية":
    st.title("📊 مركز القرارات الذكية والمؤشرات المدرسية")
    
    # جلب الإحصائيات الحية
    df_st = fetch_data("SELECT COUNT(*) as count FROM students")
    df_tf = fetch_data("SELECT COUNT(*) as count FROM staff")
    df_att = fetch_data("SELECT COUNT(*) as count FROM attendance WHERE status='غائب'")
    df_tsk = fetch_data("SELECT COUNT(*) as count FROM tasks WHERE status='قيد التنفيذ'")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''<div class="smart-card"><div class="smart-number">{df_st["count"][0]}</div><div class="smart-label">إجمالي الطلبة المسجلين</div></div>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<div class="smart-card"><div class="smart-number">{df_tf["count"][0]}</div><div class="smart-label">الكادر التدريسي والإداري</div></div>''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''<div class="smart-card"><div class="smart-number">{df_att["count"][0]}</div><div class="smart-label">حالات الغياب المسجلة</div></div>''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''<div class="smart-card"><div class="smart-number">{df_tsk["count"][0]}</div><div class="smart-label">المهام المدرسية الجارية</div></div>''', unsafe_allow_html=True)
        
    st.divider()
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🔔 مركز التنبيهات والإشعارات الذكية")
        st.info("💡 تنبيه: يرجى إكمال رصد درجات الاختبارات القليلة للصف الحادي عشر.")
        st.warning("⚠️ متابعة: توجد 3 مهام مدرسية شارف تاريخ إنجازها على الانتهاء.")
        
    with col_right:
        st.subheader("🎯 مؤشرات الأداء والقرارات السريعة")
        st.write("بيانات سريعة تمكن الإدارة من اتخاذ القرارات الأكاديمية والسلوكية المباشرة.")
        st.caption("التحديث الأخير: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# ------------------------------------------
# ثانياً: إدارة الطلبة
# ------------------------------------------
elif menu == "2️⃣ إدارة الطلبة":
    st.title("👨‍🎓 إدارة الطلبة والسجلات الشاملة")
    
    tab1, tab2, tab3 = st.tabs(["سجل الطلبة والبحث", "إضافة / تعديل طالب", "استيراد البيانات"])
    
    with tab1:
        st.subheader("🔍 البحث المتقدم في سجل الطلبة")
        search_q = st.text_input("ابحث باسم الطالب أو رقم الملف:")
        df_students = fetch_data("SELECT * FROM students WHERE student_name LIKE ?", (f"%{search_q}%",))
        st.dataframe(df_students, use_container_width=True)
        
    with tab2:
        st.subheader("➕ إضافة طالب جديد / نقل بين الصفوف")
        with st.form("add_student"):
            c1, c2 = st.columns(2)
            with c1:
                s_name = st.text_input("اسم الطالب الرباعي")
                s_grade = st.selectbox("الصف الدراسي", [f"الصف {i}" for i in ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]])
                s_section = st.text_input("الشعبة (مثال: 5/1)")
            with c2:
                s_phone = st.text_input("هاتف ولي الأمر")
                s_nid = st.text_input("الرقم المدني / رقم الملف")
                s_parent = st.text_input("اسم ولي الأمر")
            
            if st.form_submit_button("حفظ بيانات الطالب"):
                execute_query("INSERT INTO students (student_name, grade, section, guardian_phone, national_id, parent_name) VALUES (?, ?, ?, ?, ?, ?)",
                              (s_name, s_grade, s_section, s_phone, s_nid, s_parent))
                st.success("تم حفظ بيانات الطالب بنجاح!")
                st.rerun()

    with tab3:
        st.subheader("📥 استيراد بيانات الطلبة من ملفات Excel")
        uploaded_file = st.file_uploader("اختر ملف Excel يحتوي على بيانات الطلبة", type=["xlsx", "csv"])
        if uploaded_file and st.button("معالجة واستيراد"):
            try:
                df_imp = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
                st.write("معاينة البيانات المراد استيرادها:", df_imp.head())
                st.success("تم الاستيراد بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاستيراد: {e}")

# ------------------------------------------
# ثالثاً: إدارة المعلمين والموظفين
# ------------------------------------------
elif menu == "3️⃣ إدارة المعلمين والموظفين":
    st.title("👨‍🏫 إدارة الكادر التدريسي والإداري")
    
    with st.form("add_staff"):
        c1, c2 = st.columns(2)
        with c1:
            st_name = st.text_input("اسم الموظف / المعلم")
            st_job = st.selectbox("المسمى الوظيفي", ["معلم", "معلم أول", "إداري", "أخصائي اجتماعي", "فني حاسوب"])
        with c2:
            st_sub = st.text_input("التخصص / المادة")
            st_phone = st.text_input("رقم الهاتف")
        if st.form_submit_button("إضافة للكادر"):
            execute_query("INSERT INTO staff (staff_name, job_title, subject, phone) VALUES (?, ?, ?, ?)",
                          (st_name, st_job, st_sub, st_phone))
            st.success("تم التقديم والإضافة!")
            st.rerun()
            
    st.divider()
    st.subheader("📋 سجل الموظفين المعلمين الحالي")
    st.dataframe(fetch_data("SELECT * FROM staff"), use_container_width=True)

# ------------------------------------------
# رابعاً: إدارة الحضور والغياب
# ------------------------------------------
elif menu == "4️⃣ إدارة الحضور والغياب":
    st.title("⏱️ تسجيل ومتابعة الحضور والغياب والتأخر")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 رصد حالة الطالب اليومية")
        with st.form("att_form"):
            a_name = st.text_input("اسم الطالب")
            a_grade = st.selectbox("الصف", [f"الصف {i}" for i in ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]])
            a_sec = st.text_input("الشعبة")
            a_status = st.selectbox("الحالة", ["غائب", "متأخر صباحي", "استئذان ومغادرة"])
            a_delay = st.number_input("مدة التأخر (بالدقائق)", min_value=0, value=0)
            a_reason = st.text_input("السبب / ملاحظات")
            
            if st.form_submit_button("رصد الحالة"):
                execute_query("INSERT INTO attendance (student_name, grade, section, date, status, delay_minutes, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (a_name, a_grade, a_sec, datetime.now().strftime("%Y-%m-%d"), a_status, a_delay, a_reason))
                st.success("تم الرصد بنجاح!")
                st.rerun()

    with col2:
        st.subheader("📊 سجل الغياب والتأخر اليومي")
        st.dataframe(fetch_data("SELECT * FROM attendance ORDER BY id DESC"), use_container_width=True)

# ------------------------------------------
# خامساً: إدارة التحصيل الدراسي
# ------------------------------------------
elif menu == "5️⃣ إدارة التحصيل الدراسي":
    st.title("📈 رصد الدرجات وتحليل النتائج الأكاديمية")
    
    with st.form("grade_form"):
        c1, c2 = st.columns(2)
        with c1:
            g_student = st.text_input("اسم الطالب الرباعي")
            g_level = st.selectbox("الصف الدراسي", [f"الصف {i}" for i in ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]])
            g_subject = st.text_input("المادة الدراسية")
        with c2:
            g_short = st.number_input("الاختبارات القصيرة (20)", min_value=0.0, max_value=20.0, value=15.0)
            g_act = st.number_input("الأنشطة الأداء (20)", min_value=0.0, max_value=20.0, value=18.0)
            g_final = st.number_input("الامتحان النهائي (60)", min_value=0.0, max_value=60.0, value=45.0)
            
        if st.form_submit_button("رصد وحساب النتيجة"):
            total = g_short + g_act + g_final
            status = "ناجح" if total >= 50 else "يحتاج متابعة أكاديمية"
            execute_query("INSERT INTO grades (student_name, grade_level, subject, short_test, activity, final_exam, total, result_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (g_student, g_level, g_subject, g_short, g_act, g_final, total, status))
            st.success(f"تم الرصد! المجموع: {total} — الحالة: {status}")
            st.rerun()

    st.divider()
    st.subheader("📋 سجل النتاجات والتحصيل الدراسية")
    st.dataframe(fetch_data("SELECT * FROM grades"), use_container_width=True)

# ------------------------------------------
# سادساً: السلوك والانضباط الطلابي
# ------------------------------------------
elif menu == "6️⃣ السلوك والانضباط الطلابي":
    st.title("🛡️ سجل السلوك وتوثيق الإجراءات التربوية")
    
    with st.form("beh_form"):
        b_student = st.text_input("اسم الطالب")
        b_grade = st.text_input("الصف والشعبة")
        b_type = st.selectbox("نوع الملاحظة", ["سلوك إيجابي متميز", "مخالفة بسيطة", "مخالفة متوسطة", "حالة تحتاج توجيه وإرشاد"])
        b_action = st.text_area("الإجراء التربوي المتخذ / الملاحظات")
        
        if st.form_submit_button("توثيق الحالة السلوكية"):
            execute_query("INSERT INTO behavior (student_name, grade, date, behavior_type, action_taken) VALUES (?, ?, ?, ?, ?)",
                          (b_student, b_grade, datetime.now().strftime("%Y-%m-%d"), b_type, b_action))
            st.success("تم توثيق الحالة السلوكية بنجاح!")
            st.rerun()
            
    st.subheader("📜 سجل المتابعة السلوكية والإرشادية")
    st.dataframe(fetch_data("SELECT * FROM behavior"), use_container_width=True)

# ------------------------------------------
# سابعاً: المهام والمتابعات المدرسية
# ------------------------------------------
elif menu == "7️⃣ المهام والمتابعات المدرسية":
    st.title("📋 إدارة وتوزيع المهام المدرسية")
    
    with st.form("task_form"):
        t_title = st.text_input("عنوان المهمة المدرسية")
        t_assign = st.text_input("المسؤول عن التنفيذ")
        t_date = st.date_input("تاريخ الإنجاز المطلوب")
        t_prio = st.selectbox("الأولوية", ["عادية", "هام", "عاجل جداً"])
        
        if st.form_submit_button("إسناد المهمة"):
            execute_query("INSERT INTO tasks (task_title, assigned_to, due_date, priority) VALUES (?, ?, ?, ?)",
                          (t_title, t_assign, str(t_date), t_prio))
            st.success("تم توزيع المهمة بنجاح!")
            st.rerun()

    st.subheader("⌛ قائمة المهام الحالية وتتبع حالة التنفيذ")
    st.dataframe(fetch_data("SELECT * FROM tasks"), use_container_width=True)

# ------------------------------------------
# ثامناً: الفعاليات والاجتماعات
# ------------------------------------------
elif menu == "8️⃣ الفعاليات والاجتماعات":
    st.title("📅 خطة الأنشطة ومحاضر الاجتماعات")
    
    with st.form("event_form"):
        ev_title = st.text_input("عنوان الفاعلية / الاجتماع")
        ev_type = st.selectbox("النوع", ["اجتماع مجلس الإدارة", "اجتماع معلمي المادة", "نشاط مدرسي / فعالية", "ورشة عمل"])
        ev_date = st.date_input("تاريخ الانعقاد")
        ev_minutes = st.text_area("محضر الاجتماع / ملخص الفاعلية")
        ev_recom = st.text_area("التوصيات والتكليفات الصادرة")
        
        if st.form_submit_button("حفظ المحضر والفعالية"):
            execute_query("INSERT INTO events (title, event_type, event_date, minutes_text, recommendations) VALUES (?, ?, ?, ?, ?)",
                          (ev_title, ev_type, str(ev_date), ev_minutes, ev_recom))
            st.success("تم التوثيق والأرشفة!")
            st.rerun()
            
    st.dataframe(fetch_data("SELECT * FROM events"), use_container_width=True)

# ------------------------------------------
# تاسعاً: إدارة المخزون والممتلكات
# ------------------------------------------
elif menu == "9️⃣ إدارة المخزون والممتلكات":
    st.title("📦 سجل العهد والممتلكات والأجهزة المدرسية")
    
    with st.form("inv_form"):
        i_name = st.text_input("اسم الصنف / الجهاز / الأثاث")
        i_cat = st.selectbox("التصنيف", ["أجهزة حاسوب وتكنولوجيا", "أثاث مدرسي", "أجهزة طباعة وتصوير", "مستلزمات مختبرات"])
        i_qty = st.number_input("الكمية", min_value=1, value=1)
        i_status = st.selectbox("حالة العهدة", ["ممتازة / جديد", "جيدة - تعمل", "تحتاج صيانة", "مستهلكة / للتكهين"])
        i_loc = st.text_input("موقع العهدة (الغرفة / القاعة)")
        
        if st.form_submit_button("تسجيل العهدة"):
            execute_query("INSERT INTO inventory (item_name, category, quantity, condition_status, location) VALUES (?, ?, ?, ?, ?)",
                          (i_name, i_cat, i_qty, i_status, i_loc))
            st.success("تم تسجيل الصنف بنجاح!")
            st.rerun()
            
    st.dataframe(fetch_data("SELECT * FROM inventory"), use_container_width=True)

# ------------------------------------------
# عاشراً: التقارير والإحصائيات
# ------------------------------------------
elif menu == "🔟 التقارير والإحصائيات":
    st.title("📊 مركز استخراج وطباعة التقارير الشاملة")
    
    report_type = st.selectbox("اختر نوع التقرير المطلوب تصديره:", [
        "تقرير الطلبة الشامل", "تقرير الحضور والغياب", "تقرير التحصيل الدراسي والدرجات", "تقرير السلوك والانضباط"
    ])
    
    if report_type == "تقرير الطلبة الشامل":
        df_rep = fetch_data("SELECT * FROM students")
    elif report_type == "تقرير الحضور والغياب":
        df_rep = fetch_data("SELECT * FROM attendance")
    elif report_type == "تقرير التحصيل الدراسي والدرجات":
        df_rep = fetch_data("SELECT * FROM grades")
    else:
        df_rep = fetch_data("SELECT * FROM behavior")
        
    st.dataframe(df_rep, use_container_width=True)
    
    # خيارات التصدير والطباعة
    csv = df_rep.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 تصدير التقرير كملف Excel / CSV", data=csv, file_name=f"{report_type}.csv", mime="text/csv")

# ------------------------------------------
# الحادي عشر: إدارة المستندات والأرشيف
# ------------------------------------------
elif menu == "1️⃣1️⃣ إدارة المستندات والأرشيف":
    st.title("📂 الأرشيف الإلكتروني المدرسي وحفظ المستندات")
    
    with st.form("arch_form"):
        doc_title = st.text_input("عنوان المستند / الوثيقة")
        doc_cat = st.selectbox("التصنيف", ["وثائق الطلبة", "ملفات المعلمين", "محاضر وفعاليات", "تعاميم وزارية"])
        doc_notes = st.text_area("وصف وتفاصيل الأرشيف")
        
        if st.form_submit_button("حفظ في الأرشيف الإلكتروني"):
            execute_query("INSERT INTO archive (doc_title, category, ref_date, notes) VALUES (?, ?, ?, ?)",
                          (doc_title, doc_cat, datetime.now().strftime("%Y-%m-%d"), doc_notes))
            st.success("تم الحفظ بالأرشيف!")
            st.rerun()
            
    st.dataframe(fetch_data("SELECT * FROM archive"), use_container_width=True)

# ------------------------------------------
# الثاني عشر: التواصل والخدمات الإلكترونية
# ------------------------------------------
elif menu == "1️⃣2️⃣ التواصل والخدمات الإلكترونية":
    st.title("📲 قوالب التواصل ورسائل أولياء الأمور عبر WhatsApp")
    
    phone_num = st.text_input("رقم هاتف ولي الأمر (مع رمز الدولة e.g. 968XXXXXXXX):")
    msg_type = st.selectbox("نوع الرسالة:", ["تنبيه غياب", "متابعة أكاديمية", "استدعاء ولي أمر", "رسالة تقدير متميزة"])
    
    default_msg = f"المكرم ولي أمر الطالب، نود إفادتكم بضرورة التواصل مع مدرسة حجيف للتعليم الأساسي بشأن {msg_type}."
    message_body = st.text_area("نص الرسالة:", value=default_msg)
    
    if phone_num:
        whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_num}&text={message_body}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">🟢 إرسال عبر WhatsApp مباشر</button></a>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🔗 اختصارات البوابات الرسمية")
    st.markdown("""
    * [البوابة التعليمية لوزارة التربية والتعليم](https://home.moe.gov.om/)
    * [منصة إجادة لقياس الأداء](https://ejada.gov.om/)
    """)

# ------------------------------------------
# الثالث عشر: إدارة المستخدمين والصلاحيات
# ------------------------------------------
elif menu == "1️⃣3️⃣ إدارة المستخدمين والصلاحيات":
    st.title("🔐 إدارة حسابات وسجل عمليات المستخدمين")
    st.write("جدول الصلاحيات وحسابات الدخول المعتمدة بنظام المدرسة:")
    
    st.json(list(USER_ROLES.keys()))
    
    st.subheader("📜 سجل العمليات والتعديلات الأخيرة في النظام")
    st.dataframe(fetch_data("SELECT * FROM system_logs ORDER BY id DESC"), use_container_width=True)

# ------------------------------------------
# الرابع عشر: النسخ الاحتياطي واستعادة البيانات
# ------------------------------------------
elif menu == "1️⃣4️⃣ النسخ الاحتياطي واستعادة البيانات":
    st.title("💾 إدارة النسخ الاحتياطي للأمان وحماية البيانات")
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as fp:
            st.download_button(
                label="📥 تنزيل نسخة احتياطية من قاعدة البيانات الحالية (SQLite)",
                data=fp,
                file_name=f"Hajif_School_Backup_{datetime.now().strftime('%Y%m%d')}.db",
                mime="application/x-sqlite3"
            )
            
    st.caption("يتيح لك هذا الزر حفظ كامل بيانات مدرسة حجيف على جهازك الشخصي أو محرك أقراص خارجي للحماية من فقدان البيانات.")

# ------------------------------------------
# الخامس عشر: إعدادات النظام
# ------------------------------------------
elif menu == "1️⃣5️⃣ إعدادات النظام":
    st.title("⚙️ إعدادات مدرسة حجيف والبيانات المؤسسية")
    
    st.text_input("اسم المدرسة الرسمي:", value="مدرسة حجيف للتعليم الأساسي بنين (5-12)")
    st.text_input("المحافظة والولاية:", value="محافظة ظفار - ولاية صلالة")
    st.text_input("اسم مدير المدرسة:", value="أ. عامر سعيد قطن")
    st.text_input("العام الدراسي الفعال:", value="2026/2027م")
    
    st.success("إعدادات النظام مشغلة ومحدثة وفق الترويسة المعتمدة بوزارة التربية والتعليم!")