import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="الأقسام الرئيسية",
    layout="wide",
    initial_sidebar_state="expanded"
)

# بناء تنسيق الـ CSS والأقسام داخل st.markdown
st.markdown("""
<style>
    /* إعداد اتجاه الصفحة للغة العربية */
    .main {
        direction: rtl;
        text-align: right;
    }

    /* عنوان القائمة */
    .header-title {
        font-size: 22px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* الحاوية الرئيسية للعرض الأفقي */
    .sections-container {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap; /* يتيح انتقال الأزرار للسطر التالي حسب حجم الشاشة */
        gap: 12px;
        align-items: center;
        justify-content: flex-start;
        direction: rtl;
        margin-bottom: 25px;
    }

    /* تصميم بطاقة/زر القسم */
    .section-card {
        display: inline-flex;
        align-items: center;
        padding: 10px 18px;
        border-radius: 25px; /* حواف دائرية أنيقة */
        color: #ffffff !important;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        cursor: pointer;
        user-select: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        white-space: nowrap; /* إبقاء عنوان القسم في سطر واحد داخل الزر */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-decoration: none !important;
    }

    /* تأثير تحريك البطاقات عند التأشير عليها */
    .section-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
        color: #ffffff !important;
    }

    /* تنسيق أيقونة القسم */
    .section-card .icon {
        margin-left: 8px; /* مسافة بين الأيقونة والنص */
        font-size: 18px;
        line-height: 1;
    }

    /* ألوان مخصصة زاهية ومتناسقة لكل قسم بناءً على نوعه */
    .card-blue     { background-color: #2563eb; } /* 1. الواجهة والقرارات */
    .card-green    { background-color: #16a34a; } /* 2. إدارة الطلبة */
    .card-teal     { background-color: #0d9488; } /* 3. إدارة المعلمين */
    .card-orange   { background-color: #ea580c; } /* 4. الحضور والغياب */
    .card-purple   { background-color: #9333ea; } /* 5. التحصيل الدراسي */
    .card-red      { background-color: #dc2626; } /* 6. السلوك والانضباط */
    .card-indigo   { background-color: #4f46e5; } /* 7. المهام والمتابعات */
    .card-amber    { background-color: #d97706; } /* 8. الفعاليات والاجتماعات */
    .card-brown    { background-color: #78350f; } /* 9. إدارة المخزون */
    .card-cyan     { background-color: #0891b2; } /* 10. التقارير الشاملة */
    .card-gray     { background-color: #4b5563; } /* 11. المستندات والأرشيف */
    .card-pink     { background-color: #db2777; } /* 12. التواصل والخدمات */
    .card-darkblue { background-color: #1e3a8a; } /* 13. المستخدمون والصلاحيات */
    .card-emerald  { background-color: #059669; } /* 14. النسخ الاحتياطي */
</style>

<!-- عنوان الأقسام -->
<div class="header-title">
  <span>📌</span> الأقسام الرئيسية (انتقل إلى):
</div>

<!-- شبكة الخانات والأزرار الأفقية -->
<div class="sections-container">
  
  <div class="section-card card-blue">
    <span class="icon">💻</span>
    <span class="title">1. الواجهة الرئيسية والقرارات الذكية</span>
  </div>

  <div class="section-card card-green">
    <span class="icon">👨‍🎓</span>
    <span class="title">2. إدارة الطلبة (استيراد/تنزيل)</span>
  </div>

  <div class="section-card card-teal">
    <span class="icon">👨‍🏫</span>
    <span class="title">3. إدارة المعلمين (استيراد/تنزيل)</span>
  </div>

  <div class="section-card card-orange">
    <span class="icon">📋</span>
    <span class="title">4. إدارة الحضور والغياب</span>
  </div>

  <div class="section-card card-purple">
    <span class="icon">📊</span>
    <span class="title">5. إدارة التحصيل الدراسي</span>
  </div>

  <div class="section-card card-red">
    <span class="icon">⭐</span>
    <span class="title">6. السلوك والانضباط الطلابي</span>
  </div>

  <div class="section-card card-indigo">
    <span class="icon">📌</span>
    <span class="title">7. المهام والمتابعات المدرسية</span>
  </div>

  <div class="section-card card-amber">
    <span class="icon">📅</span>
    <span class="title">8. الفعاليات والاجتماعات</span>
  </div>

  <div class="section-card card-brown">
    <span class="icon">📦</span>
    <span class="title">9. إدارة المخزون والممتلكات</span>
  </div>

  <div class="section-card card-cyan">
    <span class="icon">📈</span>
    <span class="title">10. التقارير وتنزيل البيانات الشاملة</span>
  </div>

  <div class="section-card card-gray">
    <span class="icon">📁</span>
    <span class="title">11. إدارة المستندات والأرشيف</span>
  </div>

  <div class="section-card card-pink">
    <span class="icon">🌐</span>
    <span class="title">12. التواصل والخدمات الإلكترونية</span>
  </div>

  <div class="section-card card-darkblue">
    <span class="icon">🔐</span>
    <span class="title">13. إدارة المستخدمين والصلاحيات</span>
  </div>

  <div class="section-card card-emerald">
    <span class="icon">💾</span>
    <span class="title">14. النسخ الاحتياطي واستعادة البيانات</span>
  </div>

</div>
""", unsafe_allow_html=True)