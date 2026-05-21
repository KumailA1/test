import streamlit as st
import google.generativeai as genai
import re

# ==========================================
# 1. STREAMLIT CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="BRD Simulation",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Global CSS for Clean, Professional UI and Unified Buttons
st.markdown("""
    <style>
    /* Global Background and Fonts */
    .stApp {
        background-color: #FAFAFA;
        color: #2D3748;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Headers Styling */
    h1, h2, h3, h4 {
        color: #1A202C !important;
        font-weight: 700 !important;
    }
    
    /* Custom Clean Titles for Solution Document */
    .sol-title-1 { font-size: 24px; color: #1A202C; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #2B6CB0; padding-bottom: 5px; }
    .sol-title-2 { font-size: 18px; color: #2D3748; font-weight: bold; margin-top: 15px; margin-bottom: 8px; }
    
    /* Email Box Styling */
    .email-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* Unified Primary Buttons */
    div.stButton > button {
        background-color: #2B6CB0 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #3182CE !important;
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.2);
    }
    
    /* Navigation Bar */
    .nav-header {
        font-size: 14px;
        font-weight: 600;
        color: #718096;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 8px;
        margin-bottom: 24px;
    }
    
    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #FFFFFF;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #718096;
        z-index: 100;
    }
    .footer a {
        color: #2B6CB0;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
""", unsafe_allowed_unsafe_html=True)

# Top Navbar
st.markdown('<div class="nav-header">BRD Simulation</div>', unsafe_allowed_unsafe_html=True)

# Footer Definition
st.markdown(
    '<div class="footer">Built By <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank">Kumail Alhuwayji</a></div>', 
    unsafe_allowed_unsafe_html=True
)

# ==========================================
# 2. INITIALIZE SESSION STATE
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "problem_statement" not in st.session_state:
    st.session_state.problem_statement = ""
if "brd_overview" not in st.session_state:
    st.session_state.brd_overview = ""
if "brd_objectives" not in st.session_state:
    st.session_state.brd_objectives = ""
if "brd_in_scope" not in st.session_state:
    st.session_state.brd_in_scope = ""
if "brd_out_scope" not in st.session_state:
    st.session_state.brd_out_scope = ""
if "brd_biz_reqs" not in st.session_state:
    st.session_state.brd_biz_reqs = ""
if "brd_func_reqs" not in st.session_state:
    st.session_state.brd_func_reqs = ""
if "brd_criteria" not in st.session_state:
    st.session_state.brd_criteria = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "selected_stakeholder" not in st.session_state:
    st.session_state.selected_stakeholder = "Sarah Walid"

# Navigation Helper Functions
def go_next(): st.session_state.step += 1
def go_back(): st.session_state.step -= 1

# ==========================================
# 3. INITIALIZE GEMINI API & UTILS
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.warning("⚠️ API Key missing. Please configure GEMINI_API_KEY in Streamlit Secrets.")

def get_gemini_response(system_prompt, user_message, chat_history_list):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )
        formatted_contents = []
        for msg in chat_history_list:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append({"role": role, "parts": [msg["content"]]})
        
        formatted_contents.append({"role": "user", "parts": [user_message]})
        response = model.generate_content(formatted_contents)
        return response.text
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"

def clean_text_formatting(text):
    """Removes hash titles and stars for absolute text clean-up"""
    text = re.sub(r'#{1,6}\s*', '', text) 
    text = re.sub(r'\*{1,3}', '', text)    
    return text

# ==========================================
# 4. SIMULATION FLOW & SCREENS
# ==========================================

# ------------------------------------------
# STEP 1: Landing Page
# ------------------------------------------
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align: center; margin-top: 40px;'>Welcome to the BRD Simulation</h1>", unsafe_allowed_unsafe_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Experience a realistic Business Analysis scenario.</p>", unsafe_allowed_unsafe_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px; color: #718096; margin-bottom: 40px;'>Communicate with stakeholders, gather requirements, and create a professional BRD.</p>", unsafe_allowed_unsafe_html=True)
    
    st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin-bottom: 30px;'>", unsafe_allowed_unsafe_html=True)
    
    name_input = st.text_input("Enter Your Name", value=st.session_state.user_name, placeholder="Type your full name here...")
    
    st.markdown("<br>", unsafe_allowed_unsafe_html=True)
    if st.button("Start Simulation", use_container_width=True):
        if name_input.strip() == "":
            st.error("Please enter your name to proceed.")
        else:
            st.session_state.user_name = name_input
            go_next()

# ------------------------------------------
# STEP 2: Welcome Email
# ------------------------------------------
elif st.session_state.step == 2:
    st.subheader(f"Welcome, {st.session_state.user_name}")
    st.write("You are now working as a Business Analyst at SwiftDrop Logistics.")
    st.info("📅 Monday — 8:12 AM")
    st.write("You have received a new urgent email from the Operations Director.")
    
    if st.checkbox("✉️ Open Email", value=True):
        st.markdown(f"""
        <div class="email-container">
            <strong>From:</strong> Abdullah Salem — Operations Director<br>
            <strong>To:</strong> {st.session_state.user_name} — Business Analyst<br>
            <strong>Subject:</strong> Urgent Investigation Required — Delivery Delays
            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 12px 0;">
            <p>Good morning,</p>
            <p>Over the past three months, Veltra Logistics has experienced a noticeable increase in delayed deliveries across multiple cities. Customer complaints related to delivery delays have increased by 35%, and our average delivery delay has reached 28 minutes during peak hours.</p>
            <p>This issue is beginning to negatively affect customer satisfaction and overall operational performance. Recent customer satisfaction reports show a drop from 82% to 64%, and refund requests related to delayed orders are continuing to rise.</p>
            <p>At this stage, management would like a clearer understanding of:</p>
            <ul>
                <li>what is causing these delays,</li>
                <li>how current delivery operations are functioning,</li>
                <li>and what improvements may be required.</li>
            </ul>
            <p>You have been assigned to investigate the issue, communicate with the relevant stakeholders, and help identify potential business and operational requirements.</p>
            <p>The following stakeholders are available for discussion:</p>
            <ul>
                <li>Sarah Walid — Operations Manager</li>
                <li>Omar Khalid — Customer Support Lead</li>
                <li>Faisal Saad — Delivery Driver</li>
                <li>Naser Bader — CEO</li>
                <li>Reem Fahd — Customer</li>
            </ul>
            <p>Please begin your investigation as soon as possible.</p>
            <p>Regards,<br><strong>Abdullah Salem</strong><br>Operations Director<br>Veltra Logistics</p>
        </div>
        """, unsafe_allowed_unsafe_html=True)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 3: Before You Begin Disclaimer
# ------------------------------------------
elif st.session_state.step == 3:
    st.header("Before You Begin")
    st.warning("⚠️ Important System Behavior Notification")
    st.write("""
    This simulation does not currently save progress automatically. 
    If you refresh the page or leave the website, your work may be lost. 
    For the best experience, consider saving your notes or important responses externally while completing the simulation.
    """)
    
    st.markdown("<br><br>", unsafe_allowed_unsafe_html=True)
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 4: Write Problem Statement
# ------------------------------------------
elif st.session_state.step == 4:
    st.header("Write the Problem Statement")
    st.write("Based on the email and the available information, write a clear problem statement describing the business issue.")
    
    st.markdown("""
    *Consider:*
    - What is the problem?
    - Who is affected?
    - What is the business impact?
    """)
    
    prob_input = st.text_area("Problem Statement Input Box:", value=st.session_state.problem_statement, height=200, placeholder="Type your analysis of the problem here...")
    st.session_state.problem_statement = prob_input
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 5: Stakeholder Directory & Interviews
# ------------------------------------------
elif st.session_state.step == 5:
    st.header("Stakeholders Directory")
    st.write("The following stakeholders are available for discussion regarding the delivery delay issue.")
    
    # Directory mapping structure
    stakeholders_data = {
        "Sarah Walid": {"role": "Operations Manager", "resp": "Responsible for overseeing delivery operations and driver assignments."},
        "Omar Khalid": {"role": "Customer Support Lead", "resp": "Responsible for handling customer complaints and communication."},
        "Faisal Saad": {"role": "Delivery Driver", "resp": "Responsible for delivering orders and reporting field-related issues."},
        "Naser Bader": {"role": "CEO", "resp": "Responsible for overseeing business performance and strategic direction."},
        "Reem Fahd": {"role": "Customer", "resp": "Uses the delivery service and reports customer experience issues."}
    }
    
    # Render Directory Information UI Elements
    for s_name, details in stakeholders_data.items():
        st.markdown(f"**👤 {s_name}**")
        st.markdown(f"*{details['role']}*")
        st.markdown(details['resp'])
        st.markdown("---")
        
    st.subheader("💬 Start Interviewing Stakeholders")
    selected = st.selectbox("Select a Stakeholder to talk to:", list(stakeholders_data.keys()))
    st.session_state.selected_stakeholder = selected
    
    if selected not in st.session_state.chat_history:
        st.session_state.chat_history[selected] = []
        
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history[selected]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
    if user_msg := st.chat_input(f"Ask {selected} a question..."):
        with chat_container:
            with st.chat_message("user"):
                st.write(user_msg)
        st.session_state.chat_history[selected].append({"role": "user", "content": user_msg})
        
        # 100% COMPLETE AND UNALTERED PROMPTS FOR EACH STAKEHOLDER
        system_prompts = {
            "Sarah Walid": f"""You are Sarah Walid, the Operations Manager at Veltra Logistics.
Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Oversee daily delivery operations.
- Manage driver assignments and dispatching activities.
- Monitor operational efficiency and delivery performance.
- Identify bottlenecks in the delivery process.
Personality:
- Direct.
- Busy.
- Practical.
- Focused on operations, efficiency, and KPIs.
- Sometimes defensive when operations are blamed.
What You Know:
- Driver assignments are still handled manually in many cases.
- Peak hours create major pressure on dispatchers.
- Some delivery routes are not optimized.
- Drivers often call dispatchers to clarify assignments.
- There is limited real-time visibility into delivery status.
What You Do Not Know:
- Detailed customer emotions or complaint wording.
- Full financial impact.
- Technical system architecture.
- CEO-level strategic priorities.
Rules:
- You are addressing the Business Analyst whose name is {st.session_state.user_name}, use their name naturally in dialogue.
- Speak naturally like a real Operations Manager.
- Only discuss topics related to the delivery delay issue.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to delivery operations.
- Keep answers realistic, concise, and professional.""",

            "Omar Khalid": f"""You are Omar Khalid, the Customer Support Lead at Veltra Logistics.
Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Handle customer complaints and support escalations.
- Monitor repeated customer issues.
- Communicate customer pain points to internal teams.
- Track complaint trends and service quality issues.
Personality:
- Helpful.
- Friendly.
- Overwhelmed.
- Customer-focused.
- Concerned about repeated complaints.
What You Know:
- Customers complain mostly about late deliveries and lack of updates.
- Many customers contact support because they cannot track the real delivery status.
- Support agents often do not have accurate information from operations.
- Customers become frustrated when delivery time keeps changing.
- Refund requests related to delays are increasing.
What You Do Not Know:
- Detailed driver assignment process.
- Technical system limitations.
- Exact financial strategy.
- Full operational decision-making process.
Rules:
- You are addressing the Business Analyst whose name is {st.session_state.user_name}, use their name naturally in dialogue.
- Speak naturally like a real Customer Support Lead.
- Only discuss topics related to customer complaints and delivery delays.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to customer complaints and delivery delay issues.
- Keep answers realistic, concise, and professional.""",

            "Faisal Saad": f"""You are Faisal Saad, a Delivery Driver at Veltra Logistics.
Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Deliver customer orders.
- Follow assigned delivery routes.
- Report field-related issues.
- Communicate with dispatchers when there are route or order problems.
Personality:
- Honest.
- Practical.
- Straightforward.
- Field-focused.
- Sometimes frustrated because drivers are blamed for delays.
What You Know:
- Some routes are assigned without considering traffic or distance properly.
- Drivers sometimes receive unclear or late assignment updates.
- During peak hours, drivers wait for dispatch confirmation.
- The delivery app does not always show accurate order details.
- Drivers often need to call dispatchers manually.
What You Do Not Know:
- Company-level business objectives.
- Customer satisfaction reports.
- Detailed support complaint trends.
- Management strategy.
- Full system design.
Rules:
- You are addressing the Business Analyst whose name is {st.session_state.user_name}, use their name naturally in dialogue.
- Speak naturally like a real delivery driver.
- Use simple, practical language.
- Only discuss topics related to delivery work, routes, assignments, and field issues.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to delivery work and route issues.
- Keep answers realistic and concise.""",

            "Naser Bader": f"""You are Naser Bader, the CEO of Veltra Logistics.
Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Oversee business performance and strategic direction.
- Protect company reputation and customer trust.
- Ensure operational issues do not affect growth.
- Prioritize business goals and investment decisions.
Personality:
- Strategic.
- Concise.
- Business-focused.
- Concerned about reputation, revenue, and customer retention.
- Does not focus on small operational details.
What You Know:
- Delivery delays are damaging customer trust.
- Customer satisfaction dropped from 82% to 64%.
- Refund requests are increasing.
- The issue may affect upcoming expansion plans.
- Management wants measurable improvement.
What You Do Not Know:
- Detailed driver route problems.
- Daily dispatching process.
- Exact support team workflow.
- Technical details of the delivery app.
Rules:
- You are addressing the Business Analyst whose name is {st.session_state.user_name}, use their name naturally in dialogue.
- Speak naturally like a real CEO.
- Keep answers strategic and concise.
- Only discuss topics related to business impact, customer trust, performance, and strategy.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to the business impact of delivery delays.
- Avoid operational details unless the user asks at a high level.""",

            "Reem Fahd": f"""You are Reem Fahd, a customer of Veltra Logistics.
Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- You are not an employee.
- You use Veltra Logistics delivery services.
- You can only speak from your personal customer experience.
Personality:
- Honest.
- Emotional.
- Simple language.
- Frustrated because of repeated delays.
- Focused on communication, tracking, and reliability.
What You Know:
- Your last few deliveries arrived late.
- The tracking status was not clear.
- You did not receive early updates about delays.
- Customer support could not give a clear answer.
- You considered switching to another delivery provider.
What You Do Not Know:
- Internal operations.
- Driver assignment process.
- Company KPIs.
- Management strategy.
- Technical system details.
Rules:
- You are addressing the Business Analyst whose name is {st.session_state.user_name}, use their name naturally in dialogue.
- Speak naturally like a real customer.
- Use simple and emotional language.
- Only discuss your experience with delayed deliveries, tracking, communication, and support.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to your delivery experience.
- Keep answers realistic and concise."""
        }
        
        base_prompt = system_prompts[selected]
        ai_raw_response = get_gemini_response(base_prompt, user_msg, st.session_state.chat_history[selected][:-1])
        ai_clean_response = clean_text_formatting(ai_raw_response)
        
        with chat_container:
            with st.chat_message("assistant"):
                st.write(ai_clean_response)
        st.session_state.chat_history[selected].append({"role": "assistant", "content": ai_clean_response})

    st.markdown("<br><br>", unsafe_allowed_unsafe_html=True)
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue to Build BRD", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 6: Build the BRD Header
# ------------------------------------------
elif st.session_state.step == 6:
    st.header("Build the BRD")
    st.write("Based on the stakeholder interviews and the collected information, complete the following BRD sections.")
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 7: Section 1 — Project Overview
# ------------------------------------------
elif st.session_state.step == 7:
    st.subheader("Section 1 — Project Overview")
    st.write("Briefly describe the company, the problem, and the reason behind the project.")
    st.session_state.brd_overview = st.text_area("Your Input:", value=st.session_state.brd_overview, height=150)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 8: Section 2 — Business Objectives
# ------------------------------------------
elif st.session_state.step == 8:
    st.subheader("Section 2 — Business Objectives")
    st.write("Define the business goals the company wants to achieve.")
    st.session_state.brd_objectives = st.text_area("Your Input:", value=st.session_state.brd_objectives, height=150)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 9: Section 3 — Project Scope
# ------------------------------------------
elif st.session_state.step == 9:
    st.subheader("Section 3 — Project Scope")
    st.write("Define what features or parameters fall within or outside project parameters.")
    st.session_state.brd_in_scope = st.text_area("In Scope:", value=st.session_state.brd_in_scope, height=120)
    st.session_state.brd_out_scope = st.text_area("Out of Scope:", value=st.session_state.brd_out_scope, height=120)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 10: Section 4 — Requirements
# ------------------------------------------
elif st.session_state.step == 10:
    st.subheader("Section 4 — Business & Functional Requirements")
    st.session_state.brd_biz_reqs = st.text_area("Business Requirements:", value=st.session_state.brd_biz_reqs, height=120)
    st.session_state.brd_func_reqs = st.text_area("Functional Requirements:", value=st.session_state.brd_func_reqs, height=120)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Continue", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 11: Section 5 — Acceptance Criteria
# ------------------------------------------
elif st.session_state.step == 11:
    st.subheader("Section 5 — Acceptance Criteria")
    st.write("Define how the success of the solution will be measured.")
    st.session_state.brd_criteria = st.text_area("Your Input:", value=st.session_state.brd_criteria, height=150)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_back)
    with col2: st.button("Complete Simulation", on_click=go_next, use_container_width=True)

# ------------------------------------------
# STEP 12: Review and Feedback Engine
# ------------------------------------------
elif st.session_state.step == 12:
    st.header("BRD Review & Feedback")
    st.write("Processing your inputs... Here is a professional, supportive analysis of your requirement collection strategy:")
    
    feedback_prompt = f"""
    You are an expert Business Analysis Coach. Review the student inputs section by section.
    Your tone must be highly professional, polite, gentle, supportive, and encouraging. 
    Acknowledge strengths first, then provide guiding suggestions for improvement. 
    CRITICAL: Do not give the ready-made final answer. 
    Do not use markdown titles like ### or stars like *** or any hash # characters in your text output.
    
    Student Name: {st.session_state.user_name}
    
    Inputs to evaluate:
    - Problem Statement: {st.session_state.problem_statement}
    - Overview: {st.session_state.brd_overview}
    - Objectives: {st.session_state.brd_objectives}
    - In-Scope: {st.session_state.brd_in_scope}
    - Out-of-Scope: {st.session_state.brd_out_scope}
    - Business Requirements: {st.session_state.brd_biz_reqs}
    - Functional Requirements: {st.session_state.brd_func_reqs}
    - Acceptance Criteria: {st.session_state.brd_criteria}
    
    Format section by section using standard text and hyphens (-) for lists:
    Section Title
    Strengths:
    - point 1
    Suggestions:
    - point 1
    """
    
    with st.spinner("Analyzing document mapping... Please wait."):
        raw_feedback = get_gemini_response(feedback_prompt, "Evaluate my submission", [])
        clean_feedback = clean_text_formatting(raw_feedback)
        st.write(clean_feedback)
        
    st.markdown("---")
    
    if st.checkbox("📄 View One Possible Solution"):
        # CLEAN EXPLICIT SOLUTION FORMATTING (NO '#' OR '*')
        st.markdown("""
        <div class="sol-title-1">Sample BRD — Veltra Logistics Delivery Delay Project</div>
        
        <div class="sol-title-2">1. Project Overview</div>
        Veltra Logistics is a mid-sized delivery company operating across multiple cities. Over the past three months, the company has experienced a noticeable increase in delayed deliveries, particularly during peak hours. This issue has negatively affected customer satisfaction, increased refund requests, and created operational pressure across multiple departments.
        Management initiated this project to better understand the root causes of delivery delays and identify improvements that can enhance operational efficiency and customer experience.
        
        <div class="sol-title-2">2. Business Objectives</div>
        <p>- Reduce average delivery delays during peak hours.</p>
        <p>- Improve customer satisfaction related to delivery services.</p>
        <p>- Reduce delivery-related customer complaints and refund requests.</p>
        <p>- Improve communication between dispatchers, drivers, and customer support teams.</p>
        <p>- Increase visibility into delivery operations and order status.</p>
        
        <div class="sol-title-2">3. Project Scope</div>
        <p><strong>In Scope:</strong></p>
        <p>- Driver assignment process</p>
        <p>- Delivery tracking visibility</p>
        <p>- Dispatcher and driver communication</p>
        <p>- Customer delivery status updates</p>
        <p>- Customer support access to delivery information</p>
        <p>- Peak-hour delivery operations</p>
        
        <p><strong>Out of Scope:</strong></p>
        <p>- Payment systems</p>
        <p>- Warehouse inventory management</p>
        <p>- Marketing systems</p>
        <p>- HR and recruitment processes</p>
        <p>- Vendor management systems</p>
        
        <div class="sol-title-2">4. Business Requirements</div>
        <p>- The business requires improved visibility into delivery operations.</p>
        <p>- The business requires faster and more efficient driver assignment during peak hours.</p>
        <p>- The business requires better communication between operations and customer support teams.</p>
        <p>- The business requires improved customer communication regarding delivery status and delays.</p>
        <p>- The business requires reduction in delivery-related complaints and refund requests.</p>
        
        <div class="sol-title-2">5. Functional Requirements</div>
        <p>- The system should provide real-time delivery tracking.</p>
        <p>- The system should display updated estimated delivery times.</p>
        <p>- The system should notify customers when delays occur.</p>
        <p>- The system should allow dispatchers to assign drivers through a centralized platform.</p>
        <p>- The system should provide delivery status visibility for customer support agents.</p>
        <p>- The system should allow drivers to receive assignment updates in real time.</p>
        <p>- The system should generate operational reports related to delivery delays and peak-hour performance.</p>
        <p>- The system should allow dispatchers to monitor active deliveries through a dashboard.</p>
        
        <div class="sol-title-2">6. Acceptance Criteria</div>
        <p>- Average delivery delays are reduced by at least 30% within three months.</p>
        <p>- Customer satisfaction scores increase from 64% to at least 80%.</p>
        <p>- Delivery-related complaints decrease by at least 25%.</p>
        <p>- Customer support agents can access live delivery status information.</p>
        <p>- Drivers receive delivery assignments without manual communication delays.</p>
        <p>- Dispatchers can monitor delivery performance through a centralized dashboard.</p>
        
        <div class="sol-title-2">7. Proposed Solution Approach</div>
        One possible solution approach is implementing a centralized delivery management platform that supports automated driver assignment, real-time delivery tracking, and improved communication between operational teams.
        The proposed solution may include: automated route and driver assignment, real-time delivery tracking, customer delay notifications, dispatcher monitoring dashboard, and live delivery visibility for customer support teams. This solution aims to improve operational efficiency, reduce delivery delays, and enhance customer experience.
        
        <div class="sol-title-2">8. Expected Benefits</div>
        <p>- Improved delivery performance</p>
        <p>- Faster operational communication</p>
        <p>- Reduced customer frustration</p>
        <p>- Better delivery visibility</p>
        <p>- Increased customer trust and retention</p>
        <p>- Reduced refund requests and operational inefficiencies</p>
        
        <div class="sol-title-2">9. Important Note</div>
        This document represents one possible business analysis outcome based on the available stakeholder information and project context. Different analysis approaches may lead to alternative valid solutions depending on business priorities, operational constraints, and stakeholder needs.
        """, unsafe_allowed_unsafe_html=True)
        
    st.markdown("<br>", unsafe_allowed_unsafe_html=True)
    if st.button("End", use_container_width=True):
        st.session_state.step = 13
        st.rerun()

# ------------------------------------------
# STEP 13: Final Screen (Exit UI)
# ------------------------------------------
elif st.session_state.step == 13:
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>Thank You for Completing the Simulation</h2>", unsafe_allowed_unsafe_html=True)
    st.markdown("<p style='text-align: center;'>Thank you for participating in the BRD Simulation experience.</p>", unsafe_allowed_unsafe_html=True)
    st.markdown("<p style='text-align: center; font-size:14px; color:#718096;'>Your feedback can help improve future simulation experiences.</p>", unsafe_allowed_unsafe_html=True)
    
    st.markdown("<br>", unsafe_allowed_unsafe_html=True)
    
    st.markdown("""
        <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank" style="text-decoration: none;">
                <button style="background-color: #2B6CB0; color: white; border: none; border-radius: 6px; padding: 12px 30px; font-weight: 600; cursor: pointer;">
                    🔗 Connect on LinkedIn
                </button>
            </a>
            <p style="margin-top:15px; font-size:16px; font-weight:bold; color:#2D3748;">Kumail Alhuwayji</p>
        </div>
    """, unsafe_allowed_unsafe_html=True)
    
    st.markdown("<br><hr style='border:0; border-top:1px solid #E2E8F0;'><br>", unsafe_allowed_unsafe_html=True)
    if st.button("Restart New Simulation", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
