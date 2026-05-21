import streamlit as st
import google.generativeai as genai

# ضبط إعدادات الصفحة
st.set_page_config(page_title="محاكي مقابلات محلل الأعمال", page_icon="💼", layout="centered")

# تأمين جلب مفتاح الـ API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif st.sidebar.text_input("Gemini API Key", type="password"):
    genai.configure(api_key=st.sidebar.text_input("Gemini API Key", type="password"))
else:
    st.warning("الرجاء إضافة مفتاح الـ API في الـ Secrets لتشغيل التطبيق.")

# تنسيق واجهة المستخدم مخصص وإخفاء الأزرار المزعجة
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #1E3A8A; color: white; border-radius: 8px; padding: 0.5rem 2rem; font-size: 16px;
    }
    div.stButton > button:first-child:hover { background-color: #3B82F6; border-color: #3B82F6; }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة الجلسة (Session State) لتنقل مرن بين الخطوات
if "step" not in st.session_state:
    st.session_state.step = 1
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# دالة مساعدة للانتقال بين الصفحات
def next_step():
    st.session_state.step += 1
def prev_step():
    st.session_state.step -= 1

# عنوان التطبيق الرئيسي
st.title("💼 محاكي مقابلات متطلبات أعمال الـ BRD")
st.write("مرحباً بك في المحاكي الذكي. هنا ستخوض تجربة مقابلة حية لجمع المتطلبات وصياغتها بأسلوب احترافي ورشيق.")

# -------------------------------------------------------------
# الخطوة 1: اختيار السيناريو
# -------------------------------------------------------------
if st.session_state.step == 1:
    st.header("الخطوة 1: اختر سيناريو المشروع")
    st.write("اختر أحد المشاريع التالية لتبدأ محاكاة جمع المتطلبات مع العميل:")
    
    scenario = st.selectbox("المشاريع المتاحة:", [
        "نظام إدارة المخزون والمستودعات الذكي لتجارة التجزئة",
        "تطبيق الخدمات الطبية المنزلية والرعاية الصحية",
        "منصة التعليم الرقمي التفاعلية للشركات"
    ])
    st.session_state.scenario = scenario
    
    if st.button("ابدأ المحاكاة الآن"):
        next_step()

# -------------------------------------------------------------
# الخطوات من 2 إلى 6: أسئلة المحاكاة التفاعلية
# -------------------------------------------------------------
elif 2 <= st.session_state.step <= 6:
    current_q = st.session_state.step - 1
    st.header(f"المحاكاة - السؤال {current_q} من 5")
    st.subheader(f"المشروع الحالي: {st.session_state.scenario}")
    
    # تحديد نص السؤال بناءً على الخطوة الحالية لحفظ التركيز
    prompts_questions = {
        2: "أهلاً بك، أنا صاحب المشروع. نواجه حالياً مشاكل تشغيلية وتأخير واضح في وتيرة العمل اليومية، وضياع للبيانات الأساسية. كيف يمكنك مساعدتنا في صياغة 'بيان المشكلة' (Problem Statement) بدقة؟ وما هي زوايا الألم الأساسية التي يجب أن نركز عليها برأيك؟",
        3: "جميل جداً. بناءً على رؤيتك للمشكلة، كيف ترى 'النظرة العامة للمشروع' (Project Overview)؟ وما هو الوصف الشامل والشكل النهائي للحل البرمجي الذي تطمح لتصميمه ومشاركته معنا ومع أصحاب المصلحة؟",
        4: "الآن لنتحدث عن لغة الأرقام والتأثير الفعلي. ما هي 'أهداف العمل الأساسية' (Business Objectives) التي يسعى هذا النظام لتحقيقها؟ وكيف نضمن أنها أهداف ذكية ومحددة يمكن قياس نجاحها بعد الإطلاق؟",
        5: "هناك نقطة حساسة دائماً تسبب الخلاف؛ وهي الحدود. ما هو 'نطاق المشروع' (Project Scope)؟ حدد لي بوضوح ما الذي سيكون مشمولاً داخل هذا النظام (In-Scope) وما هي الميزات أو المتطلبات المستبعدة تماماً في هذه المرحلة (Out-of-Scope)؟",
        6: "ممتاز، وصلنا لأهم جزء يحتاجه الفريق التقني. ما هي 'المتطلبات الوظيفية والمعايير الأساسية لقبول النظام' (Functional Requirements & Acceptance Criteria)؟ اذكر لي أهم السيناريوهات والخصائص التي بدونها لا يعتبر النظام ناجحاً."
    }
    
    # عرض سؤال الـ AI
    st.info(prompts_questions[st.session_state.step])
    
    # استقبال إجابة المستخدم لحفظها
    user_keys = {2: "problem_statement", 3: "brd_overview", 4: "business_objectives", 5: "project_scope", 6: "functional_requirements"}
    current_key = user_keys[st.session_state.step]
    
    if current_key not in st.session_state:
        st.session_state[current_key] = ""
        
    user_input = st.text_area("اكتب إجابتك وصياغتك هنا:", value=st.session_state[current_key], height=200)
    st.session_state[current_key] = user_input
    
    # أزرار التنقل بين خطوات الأسئلة
    col1, col2 = st.columns(2)
    with col1:
        if st.button("السابق"):
            prev_step()
    with col2:
        if st.button("التالي"):
            if user_input.strip() == "":
                st.error("الرجاء كتابة إجابتك أو مسودتك قبل الانتقال للخطوة التالية لضمان الحصول على تقييم دقيق.")
            else:
                next_step()

# -------------------------------------------------------------
# الخطوة 7: مراجعة المستند وتوليد التقييم النهائي بالـ AI
# -------------------------------------------------------------
elif st.session_state.step == 7:
    st.header("الخطوة الأخيرة: مراجعة وثيقة المتطلبات والتقييم")
    st.write("راجع الصياغة التي قمت بكتابتها خلال المحاكاة قبل إرسالها إلى مدرب الذكاء الاصطناعي لتحليلها وتصحيحها:")
    
    # عرض ملخص إجابات المستخدم للمراجعة
    with st.expander("📝 عرض مسودة المتطلبات الخاصة بك"):
        st.subheader("1. بيان المشكلة (Problem Statement)")
        st.write(st.session_state.problem_statement)
        st.subheader("2. نظرة عامة على المشروع (Project Overview)")
        st.write(st.session_state.brd_overview)
        st.subheader("3. أهداف العمل (Business Objectives)")
        st.write(st.session_state.business_objectives)
        st.subheader("4. نطاق المشروع (Project Scope)")
        st.write(st.session_state.project_scope)
        st.subheader("5. المتطلبات الوظيفية ومعايير القبول")
        st.write(st.session_state.functional_requirements)
        
    if st.button("إرسال الوثيقة للتقييم والتصحيح بالـ AI"):
        with st.spinner("يقوم مدرب تحليل الأعمال الآن بفحص وثيقتك وصياغة نصائح مخصصة لك... الرجاء الانتظار"):
            try:
                # صياغة الـ System Prompt لضبط النبرة اللطيفة والتنسيق النظيف بالشرطات
                evaluation_prompt = f"""
                You are an expert Business Analysis Coach training a junior Business Analyst. 
                Your tone must be highly professional, polite, gentle, supportive, and encouraging. 
                Analyze the user's drafted sections for the scenario: '{st.session_state.scenario}'.
                
                For each section below, provide clear, constructive feedback. 
                Acknowledge strengths first, then provide guiding suggestions for improvement. 
                CRITICAL: Do not give the ready-made final answer. Let them improve it themselves.
                
                CRITICAL FORMATTING RULES:
                - Output everything directly in Arabic.
                - Use ONLY standard plain text and hyphens (-) for list items.
                - DO NOT use any markdown styling headers like '#' or text decorations like '**' or '*' anywhere in your response.
                
                Inputs to evaluate:
                - Problem Statement: {st.session_state.problem_statement}
                - Project Overview: {st.session_state.brd_overview}
                - Business Objectives: {st.session_state.business_objectives}
                - Project Scope: {st.session_state.project_scope}
                - Functional Requirements & Acceptance Criteria: {st.session_state.functional_requirements}
                """
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(evaluation_prompt)
                st.session_state.evaluation_results = response.text
                st.session_state.step = 8
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم الافتراضي للذكاء الاصطناعي: {e}")

    if st.button("تعديل الإجابات"):
        st.session_state.step = 6
        st.rerun()

# -------------------------------------------------------------
# الخطوة 8: عرض التقييم النهائي النظيف واللطيف
# -------------------------------------------------------------
elif st.session_state.step == 8:
    st.header("🎯 تقييم وتوجيهات مدرب الذكاء الاصطناعي")
    st.write("إليك تحليل شامل ومحدد لصياغتك ومجهودك، مع نصائح تطويرية ودعم مباشر لقدراتك:")
    
    # إخفاء الرموز المزعجة عبر الـ CSS وعرض النص نظيفاً تماماً
    st.markdown(f"""
        <div style='background-color: #F3F4F6; padding: 20px; border-radius: 10px; font-family: sans-serif; line-height: 1.6; white-space: pre-wrap;'>
        {st.session_state.evaluation_results}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("إعادة خوض محاكاة جديدة"):
        # تصفير الجلسة تماماً للبدء من جديد
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
