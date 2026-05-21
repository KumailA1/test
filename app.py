import streamlit as st
import google.generativeai as genai

# -------------------------------------------------------------
# 1. PAGE CONFIGURATION & GLOBAL STYLES
# -------------------------------------------------------------
st.set_page_config(page_title="BRD Simulation", page_icon="💼", layout="centered")

# Secure API Key Configuration via Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif st.sidebar.text_input("Gemini API Key", type="password"):
    genai.configure(api_key=st.sidebar.text_input("Gemini API Key", type="password"))
else:
    st.warning("Please add your Gemini API Key in Streamlit Secrets to run the app.")

# Enforcing Unified Button Colors, Layout Spacing, and Sidebar/Footer Identity
st.markdown("""
    <style>
    /* Global App Custom Alignment */
    .reportview-container .main .block-container { padding-top: 1.5rem; }
    
    /* Top Left Header Branding */
    .top-left-header {
        position: fixed;
        top: 40px;
        left: 20px;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
        color: #1E3A8A;
        font-size: 14px;
        z-index: 999;
    }
    
    /* Unified Button Styling */
    div.stButton > button:first-child {
        background-color: #1E3A8A !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 0.5rem 2rem !important;
        font-size: 16px !important;
        border: none !important;
        width: auto !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #3B82F6 !important;
        color: white !important;
    }
    
    /* Footer Styling */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F3F4F6;
        color: #4B5563;
        text-align: center;
        padding: 8px;
        font-family: sans-serif;
        font-size: 13px;
        border-top: 1px solid #E5E7EB;
        z-index: 999;
    }
    .custom-footer a {
        color: #1E3A8A;
        text-decoration: none;
        font-weight: bold;
    }
    .custom-footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="top-left-header">BRD Simulation</div>
    <div class="custom-footer">Built By <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank">Kumail Alhuwayji</a></div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "problem_statement" not in st.session_state:
    st.session_state.problem_statement = ""
if "brd_overview" not in st.session_state:
    st.session_state.brd_overview = ""
if "business_objectives" not in st.session_state:
    st.session_state.business_objectives = ""
if "scope_in" not in st.session_state:
    st.session_state.scope_in = ""
if "scope_out" not in st.session_state:
    st.session_state.scope_out = ""
if "business_reqs" not in st.session_state:
    st.session_state.business_reqs = ""
if "functional_reqs" not in st.session_state:
    st.session_state.functional_reqs = ""
if "acceptance_criteria" not in st.session_state:
    st.session_state.acceptance_criteria = ""

# Persistent chat histories for individual stakeholders
if "chat_sarah" not in st.session_state: st.session_state.chat_sarah = []
if "chat_omar" not in st.session_state: st.session_state.chat_omar = []
if "chat_faisal" not in st.session_state: st.session_state.chat_faisal = []
if "chat_naser" not in st.session_state: st.session_state.chat_naser = []
if "chat_reem" not in st.session_state: st.session_state.chat_reem = []

# Navigation Helpers
def go_to(target_step):
    st.session_state.step = target_step
    st.rerun()

# -------------------------------------------------------------
# PAGE 1: WELCOME SCREEN
# -------------------------------------------------------------
if st.session_state.step == 1:
    st.markdown("<div style='text-align: center; margin-top: 5rem;'>", unsafe_allow_html=True)
    st.title("Welcome to the BRD Simulation")
    st.write("Experience a realistic Business Analysis scenario.")
    st.write("Communicate with stakeholders, gather requirements, and create a professional BRD.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    name_input = st.text_input("Enter Your Name", value=st.session_state.user_name)
    
    if st.button("Start Simulation"):
        if name_input.strip() == "":
            st.error("Please enter your name to proceed.")
        else:
            st.session_state.user_name = name_input
            go_to(2)

# -------------------------------------------------------------
# PAGE 2: URGENT EMAIL NOTIFICATION
# -------------------------------------------------------------
elif st.session_state.step == 2:
    st.title(f"Welcome, {st.session_state.user_name}")
    st.write("You are now working as a Business Analyst at SwiftDrop Logistics.")
    st.info("Monday — 8:12 AM\n\nYou have received a new urgent email from the Operations Director.")
    
    if st.button("Open Email"):
        go_to(3)

# -------------------------------------------------------------
# PAGE 3: THE EMAIL CONTENT & SYSTEM DETAILS
# -------------------------------------------------------------
elif st.session_state.step == 3:
    st.subheader("📬 Inbox — Urgent Investigation Required")
    
    email_box = f"""
    <div style="background-color: white; padding: 20px; border: 1px solid #D1D5DB; border-radius: 6px; font-family: monospace; line-height: 1.5; color: #1F2937;">
    <b>From:</b> Abdullah Salem — Operations Director<br>
    <b>To:</b> {st.session_state.user_name} — Business Analyst<br>
    <b>Subject:</b> Urgent Investigation Required — Delivery Delays<br>
    <hr style="border-top: 1px solid #D1D5DB;">
    Good morning,<br><br>
    Over the past three months, Veltra Logistics has experienced a noticeable increase in delayed deliveries across multiple cities. Customer complaints related to delivery delays have increased by 35%, and our average delivery delay has reached 28 minutes during peak hours.<br><br>
    This issue is beginning to negatively affect customer satisfaction and overall operational performance. Recent customer satisfaction reports show a drop from 82% to 64%, and refund requests related to delayed orders are continuing to rise.<br><br>
    At this stage, management would like a clearer understanding of:<br>
    * what is causing these delays,<br>
    * how current delivery operations are functioning,<br>
    * and what improvements may be required.<br><br>
    You have been assigned to investigate the issue, communicate with the relevant stakeholders, and help identify potential business and operational requirements.<br><br>
    The following stakeholders are available for discussion:<br>
    - Sarah Walid — Operations Manager<br>
    - Omar Khalid — Customer Support Lead<br>
    - Faisal Saad — Delivery Driver<br>
    - Naser Bader — CEO<br>
    - Reem Fahd — Customer<br><br>
    Please begin your investigation as soon as possible.<br><br>
    Regards,<br>
    Abdullah Salem<br>
    Operations Director<br>
    Veltra Logistics
    </div>
    """
    st.markdown(email_box, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Continue"):
        go_to(4)

# -------------------------------------------------------------
# PAGE 4: BEFORE YOU BEGIN WARNING
# -------------------------------------------------------------
elif st.session_state.step == 4:
    st.title("Before You Begin")
    st.warning("""
    This simulation does not currently save progress automatically. 
    If you refresh the page or leave the website, your work may be lost. 
    For the best experience, consider saving your notes or important responses externally while completing the simulation.
    """)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(3)
    with col2:
        if st.button("Continue"): go_to(5)

# -------------------------------------------------------------
# PAGE 5: DRAFT PROBLEM STATEMENT
# -------------------------------------------------------------
elif st.session_state.step == 5:
    st.title("Write the Problem Statement")
    st.write("Based on the email and the available information, write a clear problem statement describing the business issue.")
    st.info("Consider:\n- What is the problem?\n- Who is affected?\n- What is the business impact?")
    
    prob_input = st.text_area("Problem Statement Workspace:", value=st.session_state.problem_statement, height=200)
    st.session_state.problem_statement = prob_input
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(4)
    with col2:
        if st.button("Continue"): go_to(6)

# -------------------------------------------------------------
# PAGE 6: STAKEHOLDER INTERVIEWS (THE CHAT ROOMS)
# -------------------------------------------------------------
elif st.session_state.step == 6:
    st.title("Stakeholders Directory")
    st.write("The following stakeholders are available for discussion regarding the delivery delay issue. Click on their names to open the chat.")
    
    tab_sarah, tab_omar, tab_faisal, tab_naser, tab_reem = st.tabs([
        "Sarah (Ops)", "Omar (Support)", "Faisal (Driver)", "Naser (CEO)", "Reem (Customer)"
    ])
    
    # ------------------ TAB: SARAH WALID ------------------
    with tab_sarah:
        st.subheader("Sarah Walid — Operations Manager")
        st.write("<b>Responsibilities:</b> Responsible for overseeing delivery operations and driver assignments.", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_sarah:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Sarah Walid...", key="input_sarah"):
            st.session_state.chat_sarah.append({"role": "user", "content": prompt})
            st.rerun()
            
        if st.session_state.chat_sarah and st.session_state.chat_sarah[-1]["role"] == "user":
            with st.spinner("Sarah is typing..."):
                try:
                    sarah_prompt = """You are Sarah Walid, the Operations Manager at Veltra Logistics.
Project Context: Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Oversee daily delivery operations.
- Manage driver assignments and dispatching activities.
- Monitor operational efficiency and delivery performance.
- Identify bottlenecks in the delivery process.
Personality: Direct. Busy. Practical. Focused on operations, efficiency, and KPIs. Sometimes defensive when operations are blamed.
What You Know:
- Driver assignments are still handled manually in many cases.
- Peak hours create major pressure on dispatchers.
- Some delivery routes are not optimized.
- Drivers often call dispatchers to clarify assignments.
- There is limited real-time visibility into delivery status.
What You Do Not Know: Detailed customer emotions or complaint wording. Full financial impact. Technical system architecture. CEO-level strategic priorities.
Rules:
- Speak naturally like a real Operations Manager.
- Only discuss topics related to the delivery delay issue.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to delivery operations.
- Keep answers realistic, concise, and professional."""
                    model = genai.GenerativeModel("gemini-pro")
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_sarah])
                    response = model.generate_content(f"{sarah_prompt}\n\nConversation History:\n{chat_history_str}")
                    st.session_state.chat_sarah.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # ------------------ TAB: OMAR KHALID ------------------
    with tab_omar:
        st.subheader("Omar Khalid — Customer Support Lead")
        st.write("<b>Responsibilities:</b> Responsible for handling customer complaints and communication.", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_omar:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Omar Khalid...", key="input_omar"):
            st.session_state.chat_omar.append({"role": "user", "content": prompt})
            st.rerun()
            
        if st.session_state.chat_omar and st.session_state.chat_omar[-1]["role"] == "user":
            with st.spinner("Omar is typing..."):
                try:
                    omar_prompt = """You are Omar Khalid, the Customer Support Lead at Veltra Logistics.
Project Context: Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Handle customer complaints and support escalations.
- Monitor repeated customer issues.
- Communicate customer pain points to internal teams.
- Track complaint trends and service quality issues.
Personality: Helpful. Friendly. Overwhelmed. Customer-focused. Concerned about repeated complaints.
What You Know:
- Customers complain mostly about late deliveries and lack of updates.
- Many customers contact support because they cannot track the real delivery status.
- Support agents often do not have accurate information from operations.
- Customers become frustrated when delivery time keeps changing.
- Refund requests related to delays are increasing.
What You Do Not Know: Detailed driver assignment process. Technical system limitations. Exact financial strategy. Full operational decision-making process.
Rules:
- Speak naturally like a real Customer Support Lead.
- Only discuss topics related to customer complaints and delivery delays.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect the conversation back to customer complaints and delivery delay issues.
- Keep answers realistic, concise, and professional."""
                    model = genai.GenerativeModel("gemini-pro")
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_omar])
                    response = model.generate_content(f"{omar_prompt}\n\nConversation History:\n{chat_history_str}")
                    st.session_state.chat_omar.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # ------------------ TAB: FAISAL SAAD ------------------
    with tab_faisal:
        st.subheader("Faisal Saad — Delivery Driver")
        st.write("<b>Responsibilities:</b> Responsible for delivering orders and reporting field-related issues.", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_faisal:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Faisal Saad...", key="input_faisal"):
            st.session_state.chat_faisal.append({"role": "user", "content": prompt})
            st.rerun()
            
        if st.session_state.chat_faisal and st.session_state.chat_faisal[-1]["role"] == "user":
            with st.spinner("Faisal is typing..."):
                try:
                    faisal_prompt = """You are Faisal Saad, a Delivery Driver at Veltra Logistics.
Project Context: Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Deliver customer orders.
- Follow assigned delivery routes.
- Report field-related issues.
- Communicate with dispatchers when there are route or order problems.
Personality: Honest. Practical. Straightforward. Field-focused. Sometimes frustrated because drivers are blamed for delays.
What You Know:
- Some routes are assigned without considering traffic or distance properly.
- Drivers sometimes receive unclear or late assignment updates.
- During peak hours, drivers wait for dispatch confirmation.
- The delivery app does not always show accurate order details.
- Drivers often need to call dispatchers manually.
What You Do Not Know: Company-level business objectives. Customer satisfaction reports. Detailed support complaint trends. Management strategy. Full system design.
Rules:
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
- Keep answers realistic and concise."""
                    model = genai.GenerativeModel("gemini-pro")
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_faisal])
                    response = model.generate_content(f"{faisal_prompt}\n\nConversation History:\n{chat_history_str}")
                    st.session_state.chat_faisal.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # ------------------ TAB: NASER BADER ------------------
    with tab_naser:
        st.subheader("Naser Bader — CEO")
        st.write("<b>Responsibilities:</b> Responsible for overseeing business performance and strategic direction.", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_naser:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Naser Bader...", key="input_naser"):
            st.session_state.chat_naser.append({"role": "user", "content": prompt})
            st.rerun()
            
        if st.session_state.chat_naser and st.session_state.chat_naser[-1]["role"] == "user":
            with st.spinner("Naser is typing..."):
                try:
                    naser_prompt = """You are Naser Bader, the CEO of Veltra Logistics.
Project Context: Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- Oversee business performance and strategic direction.
- Protect company reputation and customer trust.
- Ensure operational issues do not affect growth.
- Prioritize business goals and investment decisions.
Personality: Strategic. Concise. Business-focused. Concerned about reputation, revenue, and customer retention. Does not focus on small operational details.
What You Know:
- Delivery delays are damaging customer trust.
- Customer satisfaction dropped from 82% to 64%.
- Refund requests are increasing.
- The issue may affect upcoming expansion plans.
- Management wants measurable improvement.
What You Do Not Know: Detailed driver route problems. Daily dispatching process. Exact support team workflow. Technical details of the delivery app.
Rules:
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
- Avoid operational details unless the user asks at a high level."""
                    model = genai.GenerativeModel("gemini-pro")
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_naser])
                    response = model.generate_content(f"{naser_prompt}\n\nConversation History:\n{chat_history_str}")
                    st.session_state.chat_naser.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # ------------------ TAB: REEM FAHD ------------------
    with tab_reem:
        st.subheader("Reem Fahd — Customer")
        st.write("<b>Responsibilities:</b> Uses the delivery service and reports customer experience issues.", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_reem:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Reem Fahd...", key="input_reem"):
            st.session_state.chat_reem.append({"role": "user", "content": prompt})
            st.rerun()
            
        if st.session_state.chat_reem and st.session_state.chat_reem[-1]["role"] == "user":
            with st.spinner("Reem is typing..."):
                try:
                    reem_prompt = """You are Reem Fahd, a customer of Veltra Logistics.
Project Context: Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.
Your Responsibilities:
- You are not an employee.
- You use Veltra Logistics delivery services.
- You can only speak from your personal customer experience.
Personality: Honest. Emotional. Simple language. Frustrated because of repeated delays. Focused on communication, tracking, and reliability.
What You Know:
- Your last few deliveries arrived late.
- The tracking status was not clear.
- You did not receive early updates about delays.
- Customer support could not give a clear answer.
- You considered switching to another delivery provider.
What You Do Not Know: Internal operations. Driver assignment process. Company KPIs. Management strategy. Technical system details.
Rules:
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
                    model = genai.GenerativeModel("gemini-pro")
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_reem])
                    response = model.generate_content(f"{reem_prompt}\n\nConversation History:\n{chat_history_str}")
                    st.session_state.chat_reem.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(5)
    with col2:
        if st.button("Continue to BRD Building"): go_to(7)

# -------------------------------------------------------------
# PAGE 7: BUILD THE BRD INSTRUCTIONS SCREEN
# -------------------------------------------------------------
elif st.session_state.step == 7:
    st.title("Build the BRD")
    st.write("Based on the stakeholder interviews and the collected information, complete the following BRD sections.")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(6)
    with col2:
        if st.button("Continue"): go_to(8)

# -------------------------------------------------------------
# PAGE 8: SECTION 1 - PROJECT OVERVIEW
# -------------------------------------------------------------
elif st.session_state.step == 8:
    st.title("Section 1 — Project Overview")
    st.write("Briefly describe the company, the problem, and the reason behind the project.")
    
    ov_in = st.text_area("Overview Text:", value=st.session_state.brd_overview, height=200)
    st.session_state.brd_overview = ov_in
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(7)
    with col2:
        if st.button("Continue"): go_to(9)

# -------------------------------------------------------------
# PAGE 9: SECTION 2 - BUSINESS OBJECTIVES
# -------------------------------------------------------------
elif st.session_state.step == 9:
    st.title("Section 2 — Business Objectives")
    st.write("Define the business goals the company wants to achieve.")
    
    obj_in = st.text_area("Objectives Text:", value=st.session_state.business_objectives, height=200)
    st.session_state.business_objectives = obj_in
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(8)
    with col2:
        if st.button("Continue"): go_to(10)

# -------------------------------------------------------------
# PAGE 10: SECTION 3 - PROJECT SCOPE (IN/OUT)
# -------------------------------------------------------------
elif st.session_state.step == 10:
    st.title("Section 3 — Project Scope")
    
    st.write("In Scope")
    sc_in = st.text_area("What is included inside this phase:", value=st.session_state.scope_in, height=150, key="in_scope_input")
    st.session_state.scope_in = sc_in
    
    st.write("Out of Scope")
    sc_out = st.text_area("What is explicitly excluded from this phase:", value=st.session_state.scope_out, height=150, key="out_scope_input")
    st.session_state.scope_out = sc_out
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(9)
    with col2:
        if st.button("Continue"): go_to(11)

# -------------------------------------------------------------
# PAGE 11: SECTION 4 - BUSINESS & FUNCTIONAL REQUIREMENTS
# -------------------------------------------------------------
elif st.session_state.step == 11:
    st.title("Section 4 — Business & Functional Requirements")
    
    st.write("Business Requirements")
    br_in = st.text_area("Core high-level needs of the enterprise:", value=st.session_state.business_reqs, height=150, key="br_input")
    st.session_state.business_reqs = br_in
    
    st.write("Functional Requirements")
    fr_in = st.text_area("System features needed to satisfy business requirements:", value=st.session_state.functional_reqs, height=150, key="fr_input")
    st.session_state.functional_reqs = fr_in
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(10)
    with col2:
        if st.button("Continue"): go_to(12)

# -------------------------------------------------------------
# PAGE 12: SECTION 5 - ACCEPTANCE CRITERIA
# -------------------------------------------------------------
elif st.session_state.step == 12:
    st.title("Section 5 — Acceptance Criteria")
    st.write("Define how the success of the solution will be measured.")
    
    ac_in = st.text_area("Acceptance Criteria Metrics:", value=st.session_state.acceptance_criteria, height=200)
    st.session_state.acceptance_criteria = ac_in
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"): go_to(11)
    with col2:
        if st.button("Complete Simulation"): go_to(13)

# -------------------------------------------------------------
# PAGE 13: EVALUATION & ANALYSIS REPORT
# -------------------------------------------------------------
elif st.session_state.step == 13:
    st.title("BRD Review & Feedback")
    st.write("Processing analysis via the AI Business Analysis Coach...")
    
    if "final_coaching_report" not in st.session_state:
        with st.spinner("Evaluating your documentation section-by-section..."):
            try:
                eval_prompt = f"""
                You are an expert Business Analysis Coach evaluating a candidate's completed BRD entries.
                Your tone must be highly professional, polite, gentle, supportive, and encouraging. 
                Evaluate the user's entries based on the Veltra Logistics delivery delay case study.
                
                CRITICAL INSTRUCTION: Analyze the text section by section. For each section, list out clear points for 'Strengths' followed by clear points for 'Suggestions'. Do not provide full ready-made answers, guide them on what to improve.
                
                CRITICAL FORMATTING INSTRUCTIONS:
                - Output everything strictly in English.
                - Use plain layout and standard hyphens (-) for bullet items.
                - ABSOLUTELY DO NOT use any markdown characters like '#' titles or text styling markers like '**' or '*' anywhere.
                
                User Data to Check:
                - Problem Statement: {st.session_state.problem_statement}
                - Project Overview: {st.session_state.brd_overview}
                - Business Objectives: {st.session_state.business_objectives}
                - Project Scope (In/Out): In: {st.session_state.scope_in} | Out: {st.session_state.scope_out}
                - Requirements: Business: {st.session_state.business_reqs} | Functional: {st.session_state.functional_reqs}
                - Acceptance Criteria: {st.session_state.acceptance_criteria}
                """
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(eval_prompt)
                st.session_state.final_coaching_report = response.text
            except Exception as e:
                st.session_state.final_coaching_report = f"Coaching engine encountered an error: {e}"
                
    st.markdown(f"""
        <div style='background-color: #F3F4F6; padding: 20px; border-radius: 8px; font-family: sans-serif; white-space: pre-wrap; line-height: 1.6; color: #1F2937;'>
        {st.session_state.final_coaching_report}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("View One Possible Solution"):
        go_to(14)

# -------------------------------------------------------------
# PAGE 14: ONE POSSIBLE SOLUTION VIEW
# -------------------------------------------------------------
elif st.session_state.step == 14:
    st.title("Sample BRD — Veltra Logistics Delivery Delay Project")
    
    sample_document = """
    <div style='background-color: white; border: 1px solid #D1D5DB; padding: 25px; border-radius: 8px; font-family: Arial, sans-serif; line-height: 1.6; color: #1F2937;'>
    
    <h3>1. Project Overview</h3>
    Veltra Logistics is a mid-sized delivery company operating across multiple cities. Over the past three months, the company has experienced a noticeable increase in delayed deliveries, particularly during peak hours. This issue has negatively affected customer satisfaction, increased refund requests, and created operational pressure across multiple departments.<br><br>
    Management initiated this project to better understand the root causes of delivery delays and identify improvements that can enhance operational efficiency and customer experience.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>2. Business Objectives</h3>
    - Reduce average delivery delays during peak hours.<br>
    - Improve customer satisfaction related to delivery services.<br>
    - Reduce delivery-related customer complaints and refund requests.<br>
    - Improve communication between dispatchers, drivers, and customer support teams.<br>
    - Increase visibility into delivery operations and order status.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>3. Project Scope</h3>
    <b>In Scope</b><br>
    - Driver assignment process<br>
    - Delivery tracking visibility<br>
    - Dispatcher and driver communication<br>
    - Customer delivery status updates<br>
    - Customer support access to delivery information<br>
    - Peak-hour delivery operations<br><br>
    <b>Out of Scope</b><br>
    - Payment systems<br>
    - Warehouse inventory management<br>
    - Marketing systems<br>
    - HR and recruitment processes<br>
    - Vendor management systems
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>4. Business Requirements</h3>
    - The business requires improved visibility into delivery operations.<br>
    - The business requires faster and more efficient driver assignment during peak hours.<br>
    - The business requires better communication between operations and customer support teams.<br>
    - The business requires improved customer communication regarding delivery status and delays.<br>
    - The business requires reduction in delivery-related complaints and refund requests.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>5. Functional Requirements</h3>
    - The system should provide real-time delivery tracking.<br>
    - The system should display updated estimated delivery times.<br>
    - The system should notify customers when delays occur.<br>
    - The system should allow dispatchers to assign drivers through a centralized platform.<br>
    - The system should provide delivery status visibility for customer support agents.<br>
    - The system should allow drivers to receive assignment updates in real time.<br>
    - The system should generate operational reports related to delivery delays and peak-hour performance.<br>
    - The system should allow dispatchers to monitor active deliveries through a dashboard.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>6. Acceptance Criteria</h3>
    - Average delivery delays are reduced by at least 30% within three months.<br>
    - Customer satisfaction scores increase from 64% to at least 80%.<br>
    - Delivery-related complaints decrease by at least 25%.<br>
    - Customer support agents can access live delivery status information.<br>
    - Drivers receive delivery assignments without manual communication delays.<br>
    - Dispatchers can monitor delivery performance through a centralized dashboard.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>7. Proposed Solution Approach</h3>
    One possible solution approach is implementing a centralized delivery management platform that supports automated driver assignment, real-time delivery tracking, and improved communication between operational teams.<br><br>
    The proposed solution may include:<br>
    - Automated route and driver assignment<br>
    - Real-time delivery tracking<br>
    - Customer delay notifications<br>
    - Dispatcher monitoring dashboard<br>
    - Live delivery visibility for customer support teams<br><br>
    This solution aims to improve operational efficiency, reduce delivery delays, and enhance customer experience.
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>8. Expected Benefits</h3>
    - Improved delivery performance<br>
    - Faster operational communication<br>
    - Reduced customer frustration<br>
    - Better delivery visibility<br>
    - Increased customer trust and retention<br>
    - Reduced refund requests and operational inefficiencies
    <hr style='border-top: 1px solid #E5E7EB;'>
    
    <h3>9. Important Note</h3>
    This document represents one possible business analysis outcome based on the available stakeholder information and project context. Different analysis approaches may lead to alternative valid solutions depending on business priorities, operational constraints, and stakeholder needs.
    </div>
    """
    st.markdown(sample_document, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("End"):
        go_to(15)

# -------------------------------------------------------------
# PAGE 15: FINAL THANK YOU
# -------------------------------------------------------------
elif st.session_state.step == 15:
    st.markdown("<div style='text-align: center; margin-top: 5rem;'>", unsafe_allow_html=True)
    st.title("Thank You for Completing the Simulation")
    st.write("Thank you for participating in the BRD Simulation experience.")
    st.write("Your feedback can help improve future simulation experiences.")
    st.write("If you have any suggestions, feedback, or ideas for future simulations, feel free to connect with me on LinkedIn.")
    
    # Large Beautiful LinkedIn Button Action Block
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank" style="text-decoration: none;">
            <button style="background-color: #1E3A8A; color: white; border-radius: 6px; padding: 0.6rem 2.5rem; font-size: 16px; border: none; cursor: pointer; font-weight: bold;">
                Connect on LinkedIn
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><b>Kumail Alhuwayji</b>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Restart Simulation"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        go_to(1)
