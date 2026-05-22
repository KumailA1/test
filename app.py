import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. Page Configuration & Global Layout Rules
# ==========================================
st.set_page_config(page_title="BRD Simulation", page_icon="💼", layout="wide")

def load_premium_ui_theme():
    st.markdown("""
        <style>
        /* Modern high-tech dark background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        
        /* Persistent Header Style */
        .global-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #6366f1;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            margin-bottom: 25px;
        }
        
        /* Unified Typographic Structure */
        h1, h2, h3 {
            color: #6366f1 !important;
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-weight: 700;
        }
        
        /* Unified Button Architecture */
        .stButton>button {
            background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px 22px !important;
            font-weight: bold !important;
            transition: all 0.25s ease-in-out !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(6, 182, 212, 0.5);
        }
        
        /* Form, text fields, and textarea inputs styling */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #1e293b !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #334155 !important;
        }
        
        /* Info alert cards box formatting */
        .stAlert {
            background-color: #1e293b !important;
            border-left: 5px solid #06b6d4 !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
        }
        
        /* Dynamic Sticky Footer */
        .global-footer {
            margin-top: 50px;
            padding-top: 15px;
            border-top: 1px solid rgba(51, 65, 85, 0.5);
            text-align: center;
            font-size: 0.9rem;
            color: #94a3b8;
        }
        .global-footer a {
            color: #06b6d4 !important;
            text-decoration: none;
            font-weight: bold;
        }
        .global-footer a:hover {
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

load_premium_ui_theme()

# Display Persistent Top-Left Label on All Screens
st.markdown('<div class="global-header">💼 BRD Simulation</div>', unsafe_allow_html=True)

# ==========================================
# 2. Custom UI Component Builders
# ==========================================

# Interactive Stakeholder Card Component
def display_stakeholder_card(name, role, description, avatar_seed):
    avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={avatar_seed}"
    st.markdown(f"""
        <div style="
            background: rgba(30, 41, 59, 0.7);
            border-radius: 14px;
            padding: 18px;
            border: 1px solid rgba(99, 102, 241, 0.15);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        ">
            <img src="{avatar_url}" style="width: 65px; height: 65px; border-radius: 50%; margin-right: 18px; border: 2px solid #06b6d4; background-color: #0f172a;">
            <div>
                <h4 style="margin: 0; color: #fff; font-family: 'Segoe UI'; font-size: 1.1rem;">{name}</h4>
                <p style="margin: 2px 0 6px 0; color: #06b6d4; font-size: 0.85rem; font-weight: 600;">{role}</p>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85rem; line-height: 1.4;">{description}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Premium Instant Messenger Chat Bubble Component
def display_chat_bubble(text, is_user=False):
    align = "flex-end" if is_user else "flex-start"
    bg_color = "#4f46e5" if is_user else "#1e293b"
    border_radius = "14px 14px 0px 14px" if is_user else "14px 14px 14px 0px"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: {align}; margin-bottom: 12px;">
            <div style="
                background-color: {bg_color};
                color: #ffffff;
                padding: 12px 16px;
                border-radius: {border_radius};
                max-width: 75%;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 0.95rem;
                line-height: 1.4;
            ">
                {text}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. Core State Infrastructure & API Init
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = "Analyst"
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

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {
        "Sarah Walid": [],
        "Omar Khalid": [],
        "Faisal Saad": [],
        "Naser Bader": [],
        "Reem Fahd": []
    }

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    pass

# Navigation Controllers
def go_forward(): st.session_state.page += 1
def go_backward(): st.session_state.page -= 1

# ==========================================
# 4. Simulation Stage View Engines
# ==========================================

# --- PAGE 1: Intro Splash Screen ---
if st.session_state.page == 1:
    st.title("Welcome to the BRD Simulation")
    st.write("Experience a realistic Business Analysis scenario. Communicate with stakeholders, gather requirements, and create a professional BRD.")
    
    name_input = st.text_input("Enter Your Name", placeholder="e.g., Ali")
    if name_input.strip():
        st.session_state.user_name = name_input.strip()
        
    st.write("")
    st.button("Start Simulation", on_click=go_forward)

# --- PAGE 2: Notification & Corporate Assignment ---
elif st.session_state.page == 2:
    st.title(f"Welcome, {st.session_state.user_name}")
    st.subheader("You are now working as a Business Analyst at SwiftDrop Logistics.")
    st.caption("Monday — 8:12 AM")
    
    st.info("📬 You have received a new urgent email from the Operations Director.")
    st.write("")
    st.button("Open Email", on_click=go_forward)

# --- PAGE 3: The Urgent Email Briefing ---
elif st.session_state.page == 3:
    st.subheader("📬 Corporate Inbox")
    
    st.markdown(f"""
    <div style="background-color: #1e293b; padding: 22px; border-radius: 12px; border-left: 5px solid #ef4444;">
        <p><strong>From:</strong> Abdullah Salem — Operations Director</p>
        <p><strong>To:</strong> {st.session_state.user_name} — Business Analyst</p>
        <p><strong>Subject:</strong> Urgent Investigation Required — Delivery Delays</p>
        <hr style="border-color: #334155; margin: 12px 0;">
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
            <li><strong>Sarah Walid</strong> — Operations Manager</li>
            <li><strong>Omar Khalid</strong> — Customer Support Lead</li>
            <li><strong>Faisal Saad</strong> — Delivery Driver</li>
            <li><strong>Naser Bader</strong> — CEO</li>
            <li><strong>Reem Fahd</strong> — Customer</li>
        </ul>
        <p>Please begin your investigation as soon as possible.</p>
        <p>Regards,<br><strong>Abdullah Salem</strong><br>Operations Director<br>Veltra Logistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 4: Volatile Memory Safeguard Warning ---
elif st.session_state.page == 4:
    st.title("Before You Begin")
    st.warning("""
    This simulation does not currently save progress automatically. 
    If you refresh the page or leave the website, your work may be lost. 
    For the best experience, consider saving your notes or important responses externally while completing the simulation.
    """)
    
    st.write("")
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 5: Problem Statement Ideation ---
elif st.session_state.page == 5:
    st.title("Write the Problem Statement")
    st.write("Based on the email and the available information, write a clear problem statement describing the business issue.")
    
    st.markdown("""
    *Consider:*
    * What is the problem?
    * Who is affected?
    * What is the business impact?
    """)
    
    st.session_state.problem_statement = st.text_area(
        "Problem Statement Workspace:",
        value=st.session_state.problem_statement,
        placeholder="Type here...",
        height=220
    )
    
    st.write("")
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 6: Stakeholder Directory Hub & Live Chat Interrogations ---
elif st.session_state.page == 6:
    st.title("Stakeholders Directory")
    st.write("The following stakeholders are available for discussion regarding the delivery delay issue.")
    
    # Render Directory List View Components
    display_stakeholder_card("Sarah Walid", "Operations Manager", "Responsible for overseeing delivery operations and driver assignments.", "Sarah")
    display_stakeholder_card("Omar Khalid", "Customer Support Lead", "Responsible for handling customer complaints and communication.", "Omar")
    display_stakeholder_card("Faisal Saad", "Delivery Driver", "Responsible for delivering orders and reporting field-related issues.", "Faisal")
    display_stakeholder_card("Naser Bader", "CEO", "Responsible for overseeing business performance and strategic direction.", "Naser")
    display_stakeholder_card("Reem Fahd", "Customer", "Uses the delivery service and reports customer experience issues.", "Reem")
    
    st.markdown("---")
    st.subheader("💬 Enter Live Elicitation Session")
    
    selected_target = st.selectbox(
        "Choose who you want to interview right now:",
        ["Sarah Walid", "Omar Khalid", "Faisal Saad", "Naser Bader", "Reem Fahd"]
    )
    
    # Explicit Persona Prompt Matrices
    prompts = {
        "Sarah Walid": """You are Sarah Walid, the Operations Manager at Veltra Logistics.

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
        
        "Omar Khalid": """You are Omar Khalid, the Customer Support Lead at Veltra Logistics.

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
        
        "Faisal Saad": """You are Faisal Saad, a Delivery Driver at Veltra Logistics.

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
        
        "Naser Bader": """You are Naser Bader, the CEO of Veltra Logistics.

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
        
        "Reem Fahd": """You are Reem Fahd, a customer of Veltra Logistics.

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
    
    # Active Dialog Render Area
    dialog_box = st.container()
    with dialog_box:
        for bubble in st.session_state.chat_histories[selected_target]:
            display_chat_bubble(bubble["text"], is_user=(bubble["role"] == "user"))
            
    prompt_input = st.chat_input(f"Send a message to {selected_target}...")
    if prompt_input:
        st.session_state.chat_histories[selected_target].append({"role": "user", "text": prompt_input})
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            context_string = f"{prompts[selected_target]}\n\nDialogue History:\n"
            for message_turn in st.session_state.chat_histories[selected_target]:
                context_string += f"{message_turn['role']}: {message_turn['text']}\n"
                
            runtime_output = model.generate_content(context_string)
            agent_text = runtime_output.text
        except Exception:
            agent_text = "I am currently reviewing the delivery constraints. Please outline your queries regarding our recent transit benchmarks."
            
        st.session_state.chat_histories[selected_target].append({"role": "model", "text": agent_text})
        st.rerun()
        
    st.write("")
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 7: BRD Documentation Entry Intro ---
elif st.session_state.page == 7:
    st.title("Build the BRD")
    st.write("Based on the stakeholder interviews and the collected information, complete the following BRD sections.")
    st.write("")
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 8: Section 1 — Project Overview ---
elif st.session_state.page == 8:
    st.title("Section 1 — Project Overview")
    st.write("Briefly describe the company, the problem, and the reason behind the project.")
    
    st.session_state.brd_overview = st.text_area("Overview Content Workspace:", value=st.session_state.brd_overview, placeholder="Type here...", height=250)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 9: Section 2 — Business Objectives ---
elif st.session_state.page == 9:
    st.title("Section 2 — Business Objectives")
    st.write("Define the business goals the company wants to achieve.")
    
    st.session_state.brd_objectives = st.text_area("Objectives Content Workspace:", value=st.session_state.brd_objectives, placeholder="Type here...", height=250)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 10: Section 3 — Project Scope (Split Inputs) ---
elif st.session_state.page == 10:
    st.title("Section 3 — Project Scope")
    
    st.write("**In Scope**")
    st.session_state.brd_in_scope = st.text_area("Define items inside scope boundaries:", value=st.session_state.brd_in_scope, placeholder="Type here...", height=150, key="in_scope")
    
    st.write("**Out of Scope**")
    st.session_state.brd_out_scope = st.text_area("Define items outside project constraints:", value=st.session_state.brd_out_scope, placeholder="Type here...", height=150, key="out_scope")
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 11: Section 4 — Business & Functional Requirements ---
elif st.session_state.page == 11:
    st.title("Section 4 — Business & Functional Requirements")
    
    st.write("**Business Requirements**")
    st.session_state.brd_biz_reqs = st.text_area("Enter high-level core business needs:", value=st.session_state.brd_biz_reqs, placeholder="Type here...", height=150, key="biz_reqs")
    
    st.write("**Functional Requirements**")
    st.session_state.brd_func_reqs = st.text_area("Enter technical systems capabilities required:", value=st.session_state.brd_func_reqs, placeholder="Type here...", height=150, key="func_reqs")
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Continue", on_click=go_forward)

# --- PAGE 12: Section 6 — Acceptance Criteria ---
elif st.session_state.page == 12:
    st.title("Section 6 — Acceptance Criteria")
    st.write("Define how the success of the solution will be measured.")
    
    st.session_state.brd_criteria = st.text_area("Acceptance Metrics Workspace:", value=st.session_state.brd_criteria, placeholder="Type here...", height=250)
    
    col1, col2 = st.columns([1, 4])
    with col1: st.button("Back", on_click=go_backward)
    with col2: st.button("Complete Simulation 🚀", on_click=go_forward)

# --- PAGE 13: Granular Feedback Engine & Best Practice Blueprint ---
elif st.session_state.page == 13:
    st.title("BRD Review & Feedback")
    st.balloons()
    
    composite_brd = f"""
    Problem Statement: {st.session_state.problem_statement}
    Project Overview: {st.session_state.brd_overview}
    Objectives: {st.session_state.brd_objectives}
    In Scope: {st.session_state.brd_in_scope} | Out Scope: {st.session_state.brd_out_scope}
    Business Reqs: {st.session_state.brd_biz_reqs} | Functional Reqs: {st.session_state.brd_func_reqs}
    Acceptance Criteria: {st.session_state.brd_criteria}
    """
    
    with st.spinner("Your Senior Coach is evaluating each section of your BRD..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            review_prompt = f"""
            You are an elite, highly supportive Senior Business Analyst Coach. 
            Evaluate the junior analyst's compiled BRD fields provided below.
            Your output MUST be entirely in professional English.
            Your evaluation tone must be: Professional, Gentle, Supportive, Encouraging, and Guiding.
            CRITICAL RULE: Do NOT give ready-made answers or rewritten solutions. Ask guiding questions instead.
            
            You must structure your feedback exactly in a 'Section by Section' format as follows:
            
            ### Problem Statement
            **Strengths**
            - [List strengths or acknowledge attempt]
            **Suggestions**
            - [List actionable improvements or considerations]
            
            ### Project Overview
            **Strengths**
            - ...
            **Suggestions**
            - ...
            
            [Repeat this exact structure for: Business Objectives, Project Scope, Requirements, and Acceptance Criteria].
            
            Data to review:
            {composite_brd}
            """
            analysis_output = model.generate_content(review_prompt)
            st.markdown(f"<div style='background-color: #1e293b; padding: 25px; border-radius: 14px; border: 1px solid #06b6d4;'>{analysis_output.text}</div>", unsafe_allow_html=True)
        except Exception:
            st.markdown("""
            <div style='background-color: #1e293b; padding: 20px; border-radius: 12px;'>
                <h3>Problem Statement</h3>
                <p><strong>Strengths:</strong> You targeted core metric changes accurately.</p>
                <p><strong>Suggestions:</strong> Consider adding details about the financial impacts of increased refunds.</p>
                <h3>Requirements Review</h3>
                <p><strong>Strengths:</strong> Good differentiation of roles.</p>
                <p><strong>Suggestions:</strong> Did you capture the route-optimization bottlenecks raised by Faisal during the field interview?</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    
    if "show_sample" not in st.session_state:
        st.session_state.show_sample = False
        
    if st.button("View One Possible Solution"):
        st.session_state.show_sample = True
        
    if st.session_state.show_sample:
        st.markdown("""
        <div style="background-color: #0f172a; padding: 25px; border-radius: 14px; border: 1px solid rgba(99,102,241,0.3); margin-top: 15px;">
        
        # Sample BRD — Veltra Logistics Delivery Delay Project

        ## 1. Project Overview
        Veltra Logistics is a mid-sized delivery company operating across multiple cities. Over the past three months, the company has experienced a noticeable increase in delayed deliveries, particularly during peak hours. This issue has negatively affected customer satisfaction, increased refund requests, and created operational pressure across multiple departments.
        Management initiated this project to better understand the root causes of delivery delays and identify improvements that can enhance operational efficiency and customer experience.

        ## 2. Business Objectives
        * Reduce average delivery delays during peak hours.
        * Improve customer satisfaction related to delivery services.
        * Reduce delivery-related customer complaints and refund requests.
        * Improve communication between dispatchers, drivers, and customer support teams.
        * Increase visibility into delivery operations and order status.

        ## 3. Project Scope
        ### In Scope
        * Driver assignment process
        * Delivery tracking visibility
        * Dispatcher and driver communication
        * Customer delivery status updates
        * Customer support access to delivery information
        * Peak-hour delivery operations
        ### Out of Scope
        * Payment systems
        * Warehouse inventory management
        * Marketing systems
        * HR and recruitment processes
        * Vendor management systems

        ## 4. Business Requirements
        * The business requires improved visibility into delivery operations.
        * The business requires faster and more efficient driver assignment during peak hours.
        * The business requires better communication between operations and customer support teams.
        * The business requires improved customer communication regarding delivery status and delays.
        * The business requires reduction in delivery-related complaints and refund requests.

        ## 5. Functional Requirements
        * The system should provide real-time delivery tracking.
        * The system should display updated estimated delivery times.
        * The system should notify customers when delays occur.
        * The system should allow dispatchers to assign drivers through a centralized platform.
        * The system should provide delivery status visibility for customer support agents.
        * The system should allow drivers to receive assignment updates in real time.
        * The system should generate operational reports related to delivery delays and peak-hour performance.
        * The system should allow dispatchers to monitor active deliveries through a dashboard.

        ## 6. Acceptance Criteria
        * Average delivery delays are reduced by at least 30% within three months.
        * Customer satisfaction scores increase from 64% to at least 80%.
        * Delivery-related complaints decrease by at least 25%.
        * Customer support agents can access live delivery status information.
        * Drivers receive delivery assignments without manual communication delays.
        * Dispatchers can monitor delivery performance through a centralized dashboard.

        ## 7. Proposed Solution Approach
        One possible solution approach is implementing a centralized delivery management platform that supports automated driver assignment, real-time delivery tracking, and improved communication between operational teams.
        The proposed solution may include:
        * Automated route and driver assignment
        * Real-time delivery tracking
        * Customer delay notifications
        * Dispatcher monitoring dashboard
        * Live delivery visibility for customer support teams
        This solution aims to improve operational efficiency, reduce delivery delays, and enhance customer experience.

        ## 8. Expected Benefits
        * Improved delivery performance
        * Faster operational communication
        * Reduced customer frustration
        * Better delivery visibility
        * Increased customer trust and retention
        * Reduced refund requests and operational inefficiencies

        ## 9. Important Note
        This document represents one possible business analysis outcome based on the available stakeholder information and project context. Different analysis approaches may lead to alternative valid solutions depending on business priorities, operational constraints, and stakeholder needs.
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.button("End", on_click=go_forward)

# --- PAGE 14: Closing Out & Networking ---
elif st.session_state.page == 14:
    st.title("Thank You for Completing the Simulation")
    st.write("Thank you for participating in the BRD Simulation experience.")
    
    st.write("")
    st.markdown("""
        <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank">
            <button style="
                background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
                color: white;
                border-radius: 10px;
                border: none;
                padding: 12px 24px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            ">
                🔗 Connect on LinkedIn
            </button>
        </a>
        <p style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 10px;">
            Your feedback can help improve future simulation experiences.
        </p>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Restart Simulation"):
        st.session_state.page = 1
        st.session_state.chat_histories = {k: [] for k in st.session_state.chat_histories}
        st.session_state.problem_statement = ""
        st.session_state.brd_overview = ""
        st.session_state.brd_objectives = ""
        st.session_state.brd_in_scope = ""
        st.session_state.brd_out_scope = ""
        st.session_state.brd_biz_reqs = ""
        st.session_state.brd_func_reqs = ""
        st.session_state.brd_criteria = ""
        st.session_state.show_sample = False
        st.rerun()

# ==========================================
# 5. Persistent Responsive Footer Elements
# ==========================================
st.markdown("""
    <div class="global-footer">
        Built By <a href="https://www.linkedin.com/in/kumail-alhuwayji" target="_blank">Kumail Alhuwayji</a>
    </div>
""", unsafe_allow_html=True)
