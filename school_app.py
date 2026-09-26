import streamlit as st

# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="نظام إدارة المدرسة الذكي",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS - تصميم عربي RTL احترافي
# =========================================================

st.markdown("""
<style>

    /* =========================
       الصفحة الرئيسية
       ========================= */

    .stApp {
        direction: rtl;
        background: #f5f7fb;
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
    }

    /* إخفاء عناصر Streamlit غير الضرورية */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* =========================
       الشريط الجانبي
       ========================= */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-left: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 20px;
    }

    .sidebar-logo {
        text-align: center;
        padding: 10px 5px 20px 5px;
    }

    .sidebar-logo .school-icon {
        font-size: 48px;
        margin-bottom: 8px;
    }

    .sidebar-logo h2 {
        color: #172554;
        font-size: 19px;
        margin: 0;
        font-weight: 800;
    }

    .sidebar-logo p {
        color: #64748b;
        font-size: 13px;
        margin-top: 6px;
    }

    /* =========================
       العنوان الرئيسي
       ========================= */

    .top-header {
        background: #ffffff;
        padding: 22px 28px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
        margin-bottom: 22px;
    }

    .top-header h1 {
        margin: 0;
        color: #172554;
        font-size: 28px;
        font-weight: 800;
    }

    .top-header p {
        margin: 7px 0 0 0;
        color: #64748b;
        font-size: 14px;
    }

    /* =========================
       أزرار القائمة الجانبية
       ========================= */

    section[data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        min-height: 48px;
        border: none !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: #334155 !important;
        text-align: right !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: all 0.2s ease;
        justify-content: flex-start !important;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: #eff6ff !important;
        color: #2563eb !important;
        transform: translateX(-2px);
    }

    /* الزر النشط في الشريط الجانبي */
    section[data-testid="stSidebar"] div.stButton > button.active-nav-btn,
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: #eff6ff !important;
        color: #2563eb !important;
        font-weight: 800 !important;
        border-right: 4px solid #2563eb !important;
    }

    /* =========================
       بطاقات الأقسام (الشبكة الرئيسية)
       ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
    }

    .card-icon {
        font-size: 34px;
        text-align: center;
        margin-bottom: 6px;
    }

    .card-title {
        text-align: center;
        font-weight: 800;
        font-size: 15px;
        color: #1e293b;
        min-height: 42px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        color: #2563eb !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        border-color: #3b82f6 !important;
        background: #eff6ff !important;
        color: #1d4ed8 !important;
    }

    /* =========================
       القسم النشط
       ========================= */

    .active-section {
        background: linear-gradient(
            135deg,
            #eff6ff 0%,
            #ffffff 100%
        );
        border: 1px solid #bfdbfe;
        border-right: 6px solid #2563eb;
        border-radius: 18px;
        padding: 25px 28px;
        margin-top: 20px;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
    }

    .active-section .small-title {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 5px;
    }

    .active-section .section-title {
        color: #1d4ed8;
        font-size: 24px;
        font-weight: 800;
        margin: 0;
    }

    .active-section .description {
        color: #64748b;
        margin-top: 10px;
        font-size: 14px;
    }

    /* =========================
       بطاقات الإحصائيات
       ========================= */

    .stat-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }

    .stat-icon {
        font-size: 28px;
        margin-bottom: 7px;
    }

    .stat-number {
        font-size: 25px;
        font-weight: 800;
        color: #172554;
    }

    .stat-title {
        color: #64748b;
        font-size: 13px;
        margin-top: 5px;
    }

    /* =========================
       عناوين الأقسام
       ========================= */

    .section-heading {
        color: #172554;
        font-size: 21px;
        font-weight: 800;
        margin: 25px 0 15px 0;
    }

    /* =========================
       الجوال
       ========================= */

    @media (max-width: 900px) {

        .top-header h1 {
            font-size: 22px;
        }

        .active-section .section-title {
            font-size: 20px;
        }
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# بيانات الأقسام
# =========================================================

SECTIONS = [
    {"id": "dashboard", "icon": "🏠", "title": "الواجهة الرئيسية والقرارات الذكية",
     "description": "لوحة التحكم والإحصائيات والتنبيهات والمؤشرات المدرسية."},
    {"id": "students", "icon": "👨‍🎓", "title": "إدارة الطلبة",
     "description": "بيانات الطلبة والاستيراد والبحث والملفات والسجلات."},
    {"id": "teachers", "icon": "👨‍🏫", "title": "إدارة المعلمين والموظفين",
     "description": "بيانات المعلمين والموظفين والتخصصات والملفات."},
    {"id": "attendance", "icon": "📋", "title": "إدارة الحضور والغياب",
     "description": "الحضور والغياب والتأخر والاستئذان والتقارير."},
    {"id": "grades", "icon": "📊", "title": "إدارة التحصيل الدراسي",
     "description": "الدرجات والنتائج والتحليل الأكاديمي."},
    {"id": "behavior", "icon": "⭐", "title": "السلوك والانضباط الطلابي",
     "description": "المتابعة السلوكية والإرشاد والحالات الطلابية."},
    {"id": "tasks", "icon": "📝", "title": "المهام والمتابعات المدرسية",
     "description": "المهام والتكليفات والمواعيد والمتابعة."},
    {"id": "events", "icon": "📅", "title": "الفعاليات والاجتماعات",
     "description": "الفعاليات والاجتماعات والمحاضر والتوصيات."},
    {"id": "inventory", "icon": "📦", "title": "إدارة المخزون والممتلكات",
     "description": "العهد والأجهزة والممتلكات والمخزون."},
    {"id": "reports", "icon": "📈", "title": "التقارير والإحصائيات",
     "description": "التقارير والطباعة والتصدير والإحصائيات."},
    {"id": "documents", "icon": "📁", "title": "إدارة المستندات والأرشيف",
     "description": "الأرشيف الإلكتروني والمستندات والملفات."},
    {"id": "services", "icon": "🌐", "title": "التواصل والخدمات الإلكترونية",
     "description": "الرسائل والخدمات والبوابات الإلكترونية."},
    {"id": "users", "icon": "🔐", "title": "إدارة المستخدمين والصلاحيات",
     "description": "المستخدمون والأدوار والصلاحيات وسجل العمليات."},
    {"id": "backup", "icon": "💾", "title": "النسخ الاحتياطي واستعادة البيانات",
     "description": "حماية البيانات والنسخ الاحتياطي والاستعادة."},
]

SECTIONS_BY_ID = {s["id"]: s for s in SECTIONS}


# =========================================================
# حالة التطبيق
# =========================================================

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "dashboard"


# =========================================================
# دالة تغيير القسم
# ملاحظة مهمة: هذه الدالة تُستدعى عبر on_click، وليس بعد
# استدعاء st.button داخل شرط if. هذا هو الإصلاح الأساسي:
# استخدام on_click يضمن تحديث الحالة *قبل* أن تُعيد Streamlit
# رسم الصفحة، بينما نمط "if st.button(): ... ; st.rerun()"
# قد يحتاج نقرة إضافية ليظهر أثره فعلياً.
# =========================================================

def select_section(section_id: str):
    st.session_state.selected_section = section_id


# =========================================================
# الشريط الجانبي
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        <div class="school-icon">🏫</div>
        <h2>نظام إدارة المدرسة</h2>
        <p>النظام المدرسي الذكي</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📚 الأقسام الرئيسية")

    for section in SECTIONS:
        is_active = st.session_state.selected_section == section["id"]
        st.button(
            f"{section['icon']}  {section['title']}",
            key=f"side_{section['id']}",
            on_click=select_section,
            args=(section["id"],),
            type="primary" if is_active else "secondary",
            use_container_width=True,
        )

    st.divider()
    st.caption("نظام إدارة المدرسة الذكي")
    st.caption("الإصدار 1.0")


# =========================================================
# رأس الصفحة
# =========================================================

st.markdown("""
<div class="top-header">
    <h1>🏫 نظام إدارة المدرسة الذكي</h1>
    <p>مدرسة حجيف للتعليم الأساسي بنين من 5 إلى 12</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# الإحصائيات
# =========================================================

stat_cards = [
    ("👨‍🎓", "0", "إجمالي الطلبة"),
    ("👨‍🏫", "0", "المعلمون والموظفون"),
    ("📋", "0%", "نسبة الحضور"),
    ("⚠️", "0", "تنبيهات تحتاج متابعة"),
]

cols = st.columns(4)
for col, (icon, number, title) in zip(cols, stat_cards):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-number">{number}</div>
            <div class="stat-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# عنوان الأقسام
# =========================================================

st.markdown('<div class="section-heading">📌 الأقسام الرئيسية</div>', unsafe_allow_html=True)


# =========================================================
# بطاقات الأقسام (الشبكة)
# كل بطاقة الآن حاوية (container) بحدود، تعرض الأيقونة والعنوان
# كنص/HTML، ثم زر صغير واضح أسفلها للتنقل. هذا يفصل بين العرض
# المرئي (HTML) وبين عنصر التفاعل الفعلي (st.button)، فلا تختلط
# مشاكل تنسيق النص متعدد الأسطر داخل زر Streamlit مع منطق النقر.
# =========================================================

grid_cols = st.columns(3, gap="large")

for index, section in enumerate(SECTIONS):
    with grid_cols[index % 3]:
        with st.container(border=True):
            st.markdown(f"""
                <div class="card-icon">{section['icon']}</div>
                <div class="card-title">{section['title']}</div>
            """, unsafe_allow_html=True)

            is_active = st.session_state.selected_section == section["id"]
            st.button(
                "القسم الحالي ✓" if is_active else "فتح القسم",
                key=f"main_{section['id']}",
                on_click=select_section,
                args=(section["id"],),
                type="primary" if is_active else "secondary",
                use_container_width=True,
            )


# =========================================================
# القسم النشط
# =========================================================

active = SECTIONS_BY_ID.get(st.session_state.selected_section, SECTIONS[0])

st.markdown(f"""
<div class="active-section">
    <div class="small-title">القسم الحالي</div>
    <div class="section-title">{active["icon"]} {active["title"]}</div>
    <div class="description">{active["description"]}</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# محتوى مؤقت للقسم
# =========================================================

PLACEHOLDER_TEXT = {
    "dashboard": "لوحة التحكم الرئيسية جاهزة لربطها بقاعدة بيانات المدرسة وعرض المؤشرات والإحصائيات الفعلية.",
    "students": "هنا سيتم وضع نظام إدارة الطلبة: إضافة، تعديل، بحث، استيراد، أرشفة، ملف الطالب وغيرها.",
    "teachers": "هنا سيتم وضع إدارة المعلمين والموظفين والصلاحيات والبيانات الوظيفية.",
    "attendance": "هنا سيتم وضع تسجيل الحضور والغياب والتأخر والاستئذان والتقارير.",
    "grades": "هنا سيتم وضع الدرجات والتحصيل الدراسي وتحليل النتائج.",
    "behavior": "هنا سيتم وضع نظام السلوك والانضباط والإرشاد الطلابي.",
    "tasks": "هنا سيتم وضع المهام والتكليفات والمتابعات المدرسية.",
    "events": "هنا سيتم وضع الفعاليات والاجتماعات والمحاضر والتوصيات.",
    "inventory": "هنا سيتم وضع إدارة المخزون والممتلكات والعهد.",
    "reports": "هنا سيتم وضع التقارير والإحصائيات والتصدير والطباعة.",
    "documents": "هنا سيتم وضع الأرشيف الإلكتروني وإدارة المستندات.",
    "services": "هنا سيتم وضع الخدمات الإلكترونية وقوالب التواصل والبوابات الرسمية.",
    "users": "هنا سيتم وضع المستخدمين والأدوار والصلاحيات وسجل العمليات.",
    "backup": "هنا سيتم وضع النسخ الاحتياطي واستعادة بيانات المدرسة.",
}

st.info(PLACEHOLDER_TEXT.get(active["id"], ""))


# =========================================================
# التذييل
# =========================================================

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#94a3b8; font-size:12px;">
        نظام إدارة المدرسة الذكي © 2026
    </div>
    """,
    unsafe_allow_html=True
)
