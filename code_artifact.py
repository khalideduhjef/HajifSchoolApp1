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

# تنسيقات CSS لتكبير الأزرار وجعلها بعرض متناسق ملء الصفحة مع ألوان فريدة
st.markdown("""
<style>
    /* اتجاه واجهة المستخدم من اليمين لليار */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* عنوان القائمة */
    .header-title {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* تكبير وتوسيع أزرار Streamlit لتأخذ العرض الكامل ومظهراً مميزاً */
    div.stButton > button {
        width: 100% !important;
        min-height: 60px !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 8px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.2) !important;
        opacity: 0.95 !important;
    }

    /* تخصيص ألوان الأزرار الـ 14 بشكل مميز */
    div[key="sec_1"] > button { background-color: #2563eb !important; }
    div[key="sec_2"] > button { background-color: #16a34a !important; }
    div[key="sec_3"] > button { background-color: #0d9488 !important; }
    div[key="sec_4"] > button { background-color: #ea580c !important; }
    div[key="sec_5"] > button { background-color: #9333ea !important; }
    div[key="sec_6"] > button { background-color: #dc2626 !important; }
    div[key="sec_7"] > button { background-color: #4f46e5 !important; }
    div[key="sec_8"] > button { background-color: #d97706 !important; }
    div[key="sec_9"] > button { background-color: #78350f !important; }
    div[key="sec_10"] > button { background-color: #0891b2 !important; }
    div[key="sec_11"] > button { background-color: #4b5563 !important; }
    div[key="sec_12"] > button { background-color: #db2777 !important; }
    div[key="sec_13"] > button { background-color: #1e3a8a !important; }
    div[key="sec_14"] > button { background-color: #059669 !important; }

    /* صندوق عرض محتوى القسم الحالي */
    .content-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# عنوان الأقسام
st.markdown('<div class="header-title">📌 الأقسام الرئيسية (انتقل إلى):</div>', unsafe_allow_html=True)

# قائمة الأقسام مع رموزها العريضة
sections = [
    {"id": "sec_1", "label": "💻 1. الواجهة الرئيسية والقرارات الذكية"},
    {"id": "sec_2", "label": "👨‍🎓 2. إدارة الطلبة (استيراد/تنزيل)"},
    {"id": "sec_3", "label": "👨‍🏫 3. إدارة المعلمين (استيراد/تنزيل)"},
    {"id": "sec_4", "label": "📋 4. إدارة الحضور والغياب"},
    {"id": "sec_5", "label": "📊 5. إدارة التحصيل الدراسي"},
    {"id": "sec_6", "label": "⭐ 6. السلوك والانضباط الطلابي"},
    {"id": "sec_7", "label": "📌 7. المهام والمتابعات المدرسية"},
    {"id": "sec_8", "label": "📅 8. الفعاليات والاجتماعات"},
    {"id": "sec_9", "label": "📦 9. إدارة المخزون والممتلكات"},
    {"id": "sec_10", "label": "📈 10. التقارير وتنزيل البيانات الشاملة"},
    {"id": "sec_11", "label": "📁 11. إدارة المستندات والأرشيف"},
    {"id": "sec_12", "label": "🌐 12. التواصل والخدمات الإلكترونية"},
    {"id": "sec_13", "label": "🔐 13. إدارة المستخدمين والصلاحيات"},
    {"id": "sec_14", "label": "💾 14. النسخ الاحتياطي واستعادة البيانات"}
]

# تقسيم الأقسام على شكل شبكة عريضة تمتد عبر كامل عرض الصفحة (3 أعمدة في كل صف)
cols = st.columns(3)

for idx, sec in enumerate(sections):
    col = cols[idx % 3]
    with col:
        if st.button(sec["label"], key=sec["id"]):
            st.session_state.selected_section = sec["label"]

st.divider()

# عرض محتوى القسم المحدد عند النقر عليه
st.markdown(f"""
<div class="content-box">
    <h3>تم الانتقال إلى:</h3>
    <h2 style="color: #2563eb; margin-top: 10px;">{st.session_state.selected_section}</h2>
    <p style="margin-top: 15px; color: #475569;">يمكنك الآن البدء في استخدام أدوات ووظائف هذا القسم.</p>
</div>
""", unsafe_allow_html=True)