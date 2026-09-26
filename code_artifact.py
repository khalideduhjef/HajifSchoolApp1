import streamlit as st

# ضبط إعدادات الصفحة لتكون بعرض كامل
st.set_page_config(
    page_title="الأقسام الرئيسية",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إدارة حالة التنقل بين الأقسام
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "1. الواجهة الرئيسية والقرارات الذكية"

# تنسيقات CSS مخصصة وضمان وضوح النص واتجاه الصفحة
st.markdown("""
<style>
    /* إعداد اتجاه الصفحة بالكامل من اليمين للياسار */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* عنوان القائمة الرئيسي */
    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: #1e293b;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* تحسين شكل وحجم أزرار Streamlit لجعلها واسعة ومقروءة */
    div.stButton > button {
        width: 100% !important;
        min-height: 55px !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1e293b !important; /* لون النص أسود داكن لضمان الوضوح */
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* تأثير تحريك المؤشر فوق الأزرار */
    div.stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #eff6ff !important;
        transform: translateY(-2px) !important;
    }

    /* صندوق عرض محتوى القسم النشط */
    .content-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #2563eb;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-top: 25px;
    }
</style>
""", unsafe_allow_html=True)

# عنوان الأقسام
st.markdown('<div class="header-title">📌 الأقسام الرئيسية (انتقل إلى):</div>', unsafe_allow_html=True)

# قائمة الأقسام مع رموزها وأسمائها
sections = [
    {"id": "btn_1", "label": "💻 1. الواجهة الرئيسية والقرارات الذكية"},
    {"id": "btn_2", "label": "👨‍🎓 2. إدارة الطلبة (استيراد/تنزيل)"},
    {"id": "btn_3", "label": "👨‍🏫 3. إدارة المعلمين (استيراد/تنزيل)"},
    {"id": "btn_4", "label": "📋 4. إدارة الحضور والغياب"},
    {"id": "btn_5", "label": "📊 5. إدارة التحصيل الدراسي"},
    {"id": "btn_6", "label": "⭐ 6. السلوك والانضباط الطلابي"},
    {"id": "btn_7", "label": "📌 7. المهام والمتابعات المدرسية"},
    {"id": "btn_8", "label": "📅 8. الفعاليات والاجتماعات"},
    {"id": "btn_9", "label": "📦 9. إدارة المخزون والممتلكات"},
    {"id": "btn_10", "label": "📈 10. التقارير وتنزيل البيانات الشاملة"},
    {"id": "btn_11", "label": "📁 11. إدارة المستندات والأرشيف"},
    {"id": "btn_12", "label": "🌐 12. التواصل والخدمات الإلكترونية"},
    {"id": "btn_13", "label": "🔐 13. إدارة المستخدمين والصلاحيات"},
    {"id": "btn_14", "label": "💾 14. النسخ الاحتياطي واستعادة البيانات"}
]

# توزيع الأقسام على 3 أعمدة بعرض الصفحة
cols = st.columns(3)

for idx, sec in enumerate(sections):
    col = cols[idx % 3]
    with col:
        if st.button(sec["label"], key=sec["id"]):
            st.session_state.selected_section = sec["label"]

st.divider()

# عرض القسم المختار وتفاعله عند النقر
st.markdown(f"""
<div class="content-box">
    <h3 style="margin: 0; color: #64748b; font-size: 16px;">القسم الحالي:</h3>
    <h2 style="color: #2563eb; margin-top: 8px; font-size: 22px;">{st.session_state.selected_section}</h2>
</div>
""", unsafe_allow_html=True)