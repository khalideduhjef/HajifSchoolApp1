import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة إدارة المدرسة الرقمية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تطبيق تنسيقات CSS احترافية لتصميم الواجهة (RTL, الألوان, البطاقات, الأزرار)
st.markdown("""
<style>
    /* اتجاه الصفحة من اليمين إلى اليسار */
    .stApp {
        direction: rtl;
        text-align: right;
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #ffffff;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }

    /* رأس الصفحة الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 25px 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);
    }

    /* بطاقات الإحصائيات (KPI Cards) */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-right: 5px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-title {
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
    }
    .metric-value {
        font-size: 26px;
        color: #0f172a;
        font-weight: 700;
        margin-top: 5px;
    }

    /* تنسيق أزرار الأقسام لتكون واسعة وتفاعلية */
    div.stButton > button {
        width: 100% !important;
        min-height: 50px !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #eff6ff !important;
        transform: translateY(-2px) !important;
    }

    /* الحاوية الرئيسية للمحتوى */
    .content-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🏫 برنامج المدرسة</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px; color: #94a3b8;'>نظام الإدارة المدرسية الذكي</p>", unsafe_allow_html=True)
    st.divider()

    selected_menu = st.radio(
        "القائمة الرئيسية",
        [
            "💻 لوحة التحكم الرئيسية",
            "👨‍🎓 إدارة الطلبة",
            "👨‍🏫 إدارة المعلمين",
            "📋 الحضور والغياب",
            "📊 التحصيل الدراسي",
            "⭐ السلوك والانضباط",
            "⚙️ الإعدادات والصلاحيات"
        ]
    )

# 4. الرأس العلوي (Header Banner)
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 28px;">مرحباً بك في نظام إدارة المدرسة الرقمي 👋</h1>
    <p style="margin-top: 8px; font-size: 15px; opacity: 0.9;">متابعة فورية للطلاب، الحضور، النتائج، والمهام الإدارية من مكان واحد.</p>
</div>
""", unsafe_allow_html=True)

# 5. عرض الإحصائيات السريعة (Quick Statistics)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card" style="border-color: #2563eb;">
        <div class="metric-title">إجمالي الطلاب 👨‍🎓</div>
        <div class="metric-value">1,240</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="border-color: #16a34a;">
        <div class="metric-title">الكادر التعليمي 👨‍🏫</div>
        <div class="metric-value">85</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="border-color: #ea580c;">
        <div class="metric-title">نسبة الحضور اليوم 📋</div>
        <div class="metric-value">96.8%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card" style="border-color: #9333ea;">
        <div class="metric-title">الفعاليات النشطة 📅</div>
        <div class="metric-value">12</div>
    </div>
    """, unsafe_allow_html=True)

st.write("") # مسافة فاصلة

# 6. الأقسام الرئيسية على شكل شبكة تفاعلية (Grid System)
st.subheader("📌 الأقسام السريعة")

sections = [
    {"id": "btn_1", "label": "💻 1. القرارات والتعاميم"},
    {"id": "btn_2", "label": "👨‍🎓 2. سجلات الطلاب"},
    {"id": "btn_3", "label": "👨‍🏫 3. جدول المعلمين"},
    {"id": "btn_4", "label": "📋 4. تسجيل الحضور"},
    {"id": "btn_5", "label": "📊 5. نتائج الامتحانات"},
    {"id": "btn_6", "label": "⭐ 6. المخالفات والتكريم"},
    {"id": "btn_7", "label": "📌 7. المهام المدرسية"},
    {"id": "btn_8", "label": "📅 8. جدول الفعاليات"},
    {"id": "btn_9", "label": "📦 9. العهد والمخزون"}
]

grid_cols = st.columns(3)
for idx, sec in enumerate(sections):
    with grid_cols[idx % 3]:
        if st.button(sec["label"], key=sec["id"]):
            st.toast(f"تم فتح: {sec['label']}")

st.divider()

# 7. قسم رسم بياني وجدول بيانات الطلاب (Dashboard Widgets)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 نسبة حضور الصفوف خلال الأسبوع")
    chart_data = pd.DataFrame(
        np.random.randint(90, 100, size=(5, 4)),
        columns=["الصف السابع", "الصف الثامن", "الصف التاسع", "الصف العاشر"]
    )
    st.line_chart(chart_data)

with col_right:
    st.subheader("📢 أحدث الإشعارات")
    st.info("📅 **اجتماع أولياء الأمور:** يوم الخميس القادم الساعة 10 صباحاً.")
    st.warning("⚠️ **تنبيه:** يرجى إدخال درجات المنتصف قبل نهاية الأسبوع.")
    st.success("🎉 **تكريم:** فوز المدرسة بالمركز الأول في المسابقة الثقافية.")

# 8. جدول تفاعلي للطلاب
st.subheader("📋 قائمة الطلاب الجدد")
data = {
    "رقم الطالب": [101, 102, 103, 104, 105],
    "اسم الطالب": ["أحمد العماني", "سعيد الحارثي", "فاطمة البلوشية", "خالد المعولي", "مريم الزدجالية"],
    "الصف": ["العاشر / 1", "العاشر / 2", "التاسع / 1", "التاسع / 3", "العاشر / 1"],
    "حالة الحضور": ["حاضر", "حاضر", "غائب", "حاضر", "حاضر"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)