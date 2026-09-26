import streamlit as st

# 1. تهيئة الصفحة وضبط الإعدادات لتكون بعرض واسع
st.set_page_config(
    page_title="برنامج المدرسة",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إدارة حالة القسم المحدد
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "1. الواجهة الرئيسية والقرارات الذكية"

# 3. إدراج تنسيقات CSS لدعم الاتجاه العربي والتصميم الواسع للأزرار
st.markdown("""
<style>
    /* ضبط اتجاه الصفحة بالكامل من اليمين لليسار */
    .stApp {
        direction: rtl;
        text-align: right;
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* العنوان الرئيسي */
    .header-title {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 20px;
    }

    /* جعل الأزرار واسعة وممتدة بعرض الخلية */
    div.stButton > button {
        width: 100% !important;
        min-height: 55px !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
        margin-bottom: 5px !important;
    }

    /* تغيير لون الزر عند الوقوف عليه */
    div.stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #eff6ff !important;
    }

    /* صندوق عرض محتوى القسم الحالي */
    .content-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-right: 5px solid #2563eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 4. شريط القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("🏫 برنامج المدرسة")
    st.caption("نظام الإدارة المدرسية الرقمي")
    st.divider()
    st.write("📌 **الإجراءات السريعة**")
    if st.button("🔄 إعادة تحميل الصفحة"):
        st.rerun()

# 5. عنوان الواجهة الرئيسية
st.markdown('<div class="header-title">📌 الأقسام الرئيسية (انتقل إلى):</div>', unsafe_allow_html=True)

# 6. قائمة الأقسام الـ 14
sections = [
    {"id": "s1", "name": "💻 1. الواجهة الرئيسية والقرارات الذكية"},
    {"id": "s2", "name": "👨‍🎓 2. إدارة الطلبة (استيراد/تنزيل)"},
    {"id": "s3", "name": "👨‍🏫 3. إدارة المعلمين (استيراد/تنزيل)"},
    {"id": "s4", "name": "📋 4. إدارة الحضور والغياب"},
    {"id": "s5", "name": "📊 5. إدارة التحصيل الدراسي"},
    {"id": "s6", "name": "⭐ 6. السلوك والانضباط الطلابي"},
    {"id": "s7", "name": "📌 7. المهام والمتابعات المدرسية"},
    {"id": "s8", "name": "📅 8. الفعاليات والاجتماعات"},
    {"id": "s9", "name": "📦 9. إدارة المخزون والممتلكات"},
    {"id": "s10", "name": "📈 10. التقارير وتنزيل البيانات الشاملة"},
    {"id": "s11", "name": "📁 11. إدارة المستندات والأرشيف"},
    {"id": "s12", "name": "🌐 12. التواصل والخدمات الإلكترونية"},
    {"id": "s13", "name": "🔐 13. إدارة المستخدمين والصلاحيات"},
    {"id": "s14", "name": "💾 14. النسخ الاحتياطي واستعادة البيانات"}
]

# 7. توزيع الأزرار على 3 أعمدة
cols = st.columns(3)

for idx, item in enumerate(sections):
    with cols[idx % 3]:
        if st.button(item["name"], key=item["id"]):
            st.session_state.selected_section = item["name"]

st.divider()

# 8. عرض القسم النشط المختار عند الضغط على أي زر
st.markdown(f"""
<div class="content-card">
    <h4 style="margin:0; color:#64748b;">أنت الآن في قسم:</h4>
    <h2 style="margin-top:5px; color:#2563eb;">{st.session_state.selected_section}</h2>
</div>
""", unsafe_allow_html=True)