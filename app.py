import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. Page Configuration & Creative UI Theme (CSS)
# ==========================================
st.set_page_config(page_title="BRD Simulator - Veltra Logistics", page_icon="💼", layout="wide")

def load_creative_ui():
    st.markdown("""
        <style>
        /* Modern deep tech gradient background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        
        /* Modern typographic colors for headers */
        h1, h2, h3 {
            color: #6366f1 !important; /* Premium Indigo */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
        }
        
        /* Dynamic Button Styling with premium Hover Effects */
        .stButton>button {
            background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.6);
        }
        
        /* Premium container styling for alerts and status */
        .stAlert {
            background-color: #1e293b !important;
            border-left: 5px solid #06b6d4 !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
        }
        
        /* Sleek text inputs and textareas */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #1e293b !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #334155 !important;
        }
        
        /* Custom sleek scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

load_creative_ui()

# ==========================================
# 2. Custom UI Components (Cards & Chat Bubbles)
# ==========================================

# Modern Character Card Component
def display_character_card(name, role, avatar_seed, description):
    avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={avatar_seed}"
    st.markdown(f"""
        <div style="
            background: rgba(30, 41, 59, 0.7);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        ">
            <img src="{avatar_url}" style="width: 70px; height: 70px; border-radius: 50%; margin-right: 20px; border: 2px solid #06b6d4;">
            <div>
                <h4 style="margin: 0; color: #fff; font-family: 'Segoe UI';">{name}</h4>
                <p style="margin: 0; color: #06b6d4; font-size: 0.9em; font-weight: 600;">{role}</p>
                <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 0.85em; line-height: 1.4;">{description}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Elegant Chat Bubble Component
def custom_chat_bubble(text, is_user=False):
    align = "flex-end" if is_user else "flex-start"
    bg_color = "#4f46e5" if is_user else "#1e293b"
    border_radius = "15px 15px 0px 15px" if is_user else "15px 15px 15px 0px"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: {align}; margin-bottom: 12px;">
            <div style="
                background-color: {bg_color};
                color: #ffffff;
                padding: 12px 16px;
                border-radius: {border_radius};
                max-width: 75%;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                font-family: 'Segoe UI';
                direction: ltr;
            ">
                {text}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. Session State Management & API Configuration
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = 1

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {
        "Sarah Jenkins": [],
        "Faisal Al-Otaibi": [],
        "Ahmed Mansoor": [],
        "Khaled Al-Dossari": [],
        "Fatimah Al-Zahrani": []
    }

if "brd_draft" not in st.session_state:
    st.session_state.brd_draft = ""

# Securely configure the Gemini API
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.warning("⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Running in demo layout mode.")

# ==========================================
# 4. English Sidebar & Dynamic Progress Control
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #06b6d4;'>🧭 Navigation</h3>", unsafe_allow_html=True)
    
    # Track progress across 13 stages
    progress_percentage = int((st.session_state.page / 13) * 100)
    st.markdown(f"**Current Stage: {st.session_state.page} of 13**")
    st.progress(progress_percentage)
    
    st.markdown("---")
    
    st.write("📌 **Quick Jump To Milestones:**")
    if st.button("Introduction & Brief (P. 1-2)"): st.session_state.page = 1
    if st.button("Stakeholder Interviews (P. 3)"): st.session_state.page = 3
    if st.button("Draft the BRD (P. 12)"): st.session_state.page = 12
    if st.button("Expert AI Evaluation (P. 13)"): st.session_state.page = 13

# Helper navigation functions
def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

# ==========================================
# 5. The 13-Page Simulation Workflow
# ==========================================

# --- Page 1: Welcome & Corporate Context ---
if st.session_state.page == 1:
    st.title("💼 Business Requirements Document Simulator | BRD Challenge")
    st.subheader("Welcome to an immersive simulation for professional Business Analysts!")
    
    st.info("""
    **The Business Case:** You have just stepped into your role as a Business Analyst at **Veltra Logistics**, a premier supply chain and fulfillment provider.
    Recently, the company has hit a critical bottleneck impacting customer satisfaction scores: **severe delivery delays and massive overhead inefficiencies within the primary regional warehouses.**
    """)
    
    st.write("You will handle the complete analysis pipeline: reviewing the initial distress brief, managing dynamic client interviews, structuring the documentation, and receiving feedback from an elite Senior BA Coach.")
    st.button("Launch Simulation & Check Inbox 📥", on_click=next_page)

# --- Page 2: The Urgent Email Brief ---
elif st.session_state.page == 2:
    st.title("📥 Corporate Inbox - High Priority")
    
    st.markdown("""
    <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #ef4444;">
        <p><strong>From:</strong> Sarah Jenkins (Operations Manager)</p>
        <p><strong>To:</strong> Business Analysis Team</p>
        <p><strong>Subject:</strong> URGENT: Warehouse Bottlenecks & Delivery Delays</p>
        <hr style="border-color: #334155;">
        <p>Hi Team,</p>
        <p>The situation at our main Dammam distribution hub is becoming critical. We are experiencing massive sorting backlogs, and our manual checking processes are taking twice as long as expected. This delays truck dispatches, creating a cascading failure out to final consumer drop-offs.</p>
        <p>We need a robust, scalable technical solution (a smart Warehouse Management System - WMS) deployed promptly. Please schedule discovery interviews with the core stakeholders, synthesize their specific operational requirements, and compile the official BRD so we can initiate development.</p>
        <p>Best regards,<br><strong>Sarah Jenkins</strong><br>Operations Manager | Veltra Logistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1: st.button("Back", on_click=prev_page)
    with col2: st.button("Proceed to Conference Room for Discovery 👥", on_click=next_page)

# --- Pages 3 to 7: Interactive Client Interviews ---
elif 3 <= st.session_state.page <= 7:
    # Dictionary mapping each page to a specific stakeholder persona
    characters = {
        3: {"name": "Sarah Jenkins", "role": "Operations Manager", "seed": "Sarah", "desc": "Focuses strictly on overall center efficiency, reducing warehouse processing overhead, and optimizing throughput metrics.", "prompt": "You are Sarah Jenkins, the Operations Manager at Veltra Logistics. You are frustrated with manual sorting delays. Respond as a busy manager who wants clear dashboard reports and high-level metrics. Explain your operational pain points clearly. Do not provide direct code solutions."},
        4: {"name": "Faisal Al-Otaibi", "role": "Warehouse Supervisor", "seed": "Faisal", "desc": "Manages day-to-day floor operations, tracking inventory, staff assignments, shelf allocation, and dispatch zones.", "prompt": "You are Faisal Al-Otaibi, the Warehouse Supervisor. You manage the physical floor team. You complain about poor floor space utilization, missing items, and the lack of smart handheld barcode scanners. Speak in a realistic, on-the-ground corporate tone."},
        5: {"name": "Ahmed Mansoor", "role": "IT Director", "seed": "Ahmed", "desc": "Concerned with security baselines, infrastructure overhead, API reliability, and integration with the legacy ERP software.", "prompt": "You are Ahmed Mansoor, the IT Director. You worry about system integration overhead, strict data security, cloud hosting costs, and clean API documentation. Demand alignment with corporate IT standards."},
        6: {"name": "Khaled Al-Dossari", "role": "Procurement Specialist", "seed": "Khaled", "desc": "Evaluates financial boundaries, vendor SLAs, Return on Investment (ROI), and strict budget constraints.", "prompt": "You are Khaled Al-Dossari, the Procurement Specialist. Your main focus is budget limits, strict vendor Service Level Agreement (SLA) enforcement, licensing models, and long-term cost efficiency."},
        7: {"name": "Fatimah Al-Zahrani", "role": "Customer Success Lead", "seed": "Fatimah", "desc": "Represents client sentiment, tracks cancellation data, and calls for automated status updates and SMS tracking.", "prompt": "You are Fatimah Al-Zahrani, the Customer Success Lead. You are stressed due to a high volume of client complaints regarding late shipments. You demand automated customer notification systems and real-time package tracking."}
    }
    
    char_info = characters[st.session_state.page]
    st.title(f"🗣️ Live Interview Session: {char_info['name']}")
    
    # Render the custom card element
    display_character_card(char_info['name'], char_info['role'], char_info['seed'], char_info['desc'])
    
    # Active conversation container
    chat_area = st.container()
    with chat_area:
        for msg in st.session_state.chat_histories[char_info['name']]:
            custom_chat_bubble(msg["text"], is_user=(msg["role"] == "user"))
            
    # Interactive chat layout
    user_input = st.chat_input(f"Ask {char_info['name']} about their expectations, system constraints, or bottlenecks...")
    
    if user_input:
        st.session_state.chat_histories[char_info['name']].append({"role": "user", "text": user_input})
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            # Aggregate historical inputs for comprehensive LLM state
            full_prompt = f"{char_info['prompt']}\n\nInterview History:\n"
            for m in st.session_state.chat_histories[char_info['name']]:
                full_prompt += f"{m['role']}: {m['text']}\n"
            
            response = model.generate_content(full_prompt)
            ai_response = response.text
        except Exception:
            ai_response = f"Thank you for reaching out. As the {char_info['role']}, my focus is ensuring this implementation aligns with our department's milestones. Please verify your system's API configuration credentials."
            
        st.session_state.chat_histories[char_info['name']].append({"role": "character", "text": ai_response})
        st.rerun()

    st.write("")
    col1, col2 = st.columns(2)
    with col1: st.button("Previous Interview", on_click=prev_page)
    with col2: st.button("Save & Continue To Next Phase ➡️", on_click=next_page)

# --- Pages 8 to 11: Business Analysis & Modeling Stages ---
elif 8 <= st.session_state.page <= 11:
    page_titles = {
        8: "🔍 Elicitation Synthesis & Discovery Logs",
        9: "🎯 Project Scope Formulation & Objective Boundaries",
        10: "📊 Stakeholder Mapping & Influence Matrix",
        11: "⚡ Requirements Classification (Functional vs Non-Functional)"
    }
    st.title(page_titles[st.session_state.page])
    
    st.write("Synthesize and structure your discovery notes from your client sessions below to formulate your project documentation:")
    st.text_area("Analysis Workspace Area:", placeholder="Log professional analytical notes here...", height=250, key=f"notes_page_{st.session_state.page}")
    
    col1, col2 = st.columns(2)
    with col1: st.button("Back", on_click=prev_page)
    with col2: st.button("Next Phase", on_click=next_page)

# --- Page 12: Structuring the Official BRD ---
elif st.session_state.page == 12:
    st.title("📝 Business Requirements Document (BRD Template)")
    st.write("Compile your structural requirements findings into an industry-standard format. Your finalized text will be analyzed directly by our AI Coach:")
    
    brd_template = """1. Business Objective:
2. Stakeholder Requirements:
3. Functional Requirements:
4. Non-Functional Requirements:"""
    
    st.session_state.brd_draft = st.text_area(
        "Edit and compose your formal BRD draft here:", 
        value=st.session_state.brd_draft if st.session_state.brd_draft else brd_template,
        height=400
    )
    
    col1, col2 = st.columns(2)
    with col1: st.button("Back", on_click=prev_page)
    with col2: st.button("Submit Documentation for Expert Review 🚀", on_click=next_page)

# --- Page 13: Elite Mentorship Feedback & Celebration ---
elif st.session_state.page == 13:
    st.title("🏁 Senior Mentorship Review & Audit")
    
    # Celebrate the milestone instantly on loading completion!
    st.balloons()
    
    st.subheader("🤖 Senior Business Analyst Coach Feedback")
    st.write("The analytical model is validating your architecture against the exact constraints of Veltra Logistics:")
    
    if st.session_state.brd_draft.strip() == "" or "Business Objective" in st.session_state.brd_draft and len(st.session_state.brd_draft) < 150:
        st.warning("⚠️ The current document appears empty or incomplete. Please go back to Stage 12 and populate the template with detailed technical requirements to receive a quality critique.")
    else:
        with st.spinner("Analyzing document structure against stakeholder profiles..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                evaluation_prompt = f"""
                You are an encouraging, professional, and highly experienced Senior Business Analyst Coach.
                Review the following BRD draft written by a junior analyst for Veltra Logistics.
                Your evaluation MUST be completely in professional English using a friendly, elite mentoring tone.
                Acknowledge strong architectural definitions, and then use Socratic, constructive prompts to encourage deeper thinking. 
                (For example: Did they address Faisal's handheld scanning constraints? Ahmed's ERP integration requirement? Fatimah's automated notifications?). 
                Do NOT provide direct text rewrites; guide them on how to mature as an elite analyst.
                
                Document under audit:
                {st.session_state.brd_draft}
                """
                response = model.generate_content(evaluation_prompt)
                st.markdown(f"<div style='background-color: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #06b6d4;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception:
                st.markdown("""
                <div style='background-color: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #06b6d4;'>
                    <h4>Excellent Effort! (Simulation Framework Feedback)</h4>
                    <p>Your documentation structural alignment is highly accurate. To optimize this to a senior grade, analyze the systems data boundaries outlined by IT (Ahmed) regarding legacy software API hookups, alongside floor tracking hardware requested by Operations (Faisal). Exceptional delivery on project objectives!</p>
                </div>
                """, unsafe_allow_html=True)
                
    st.write("")
    if st.button("🔄 Restart Complete Simulation"):
        st.session_state.page = 1
        st.session_state.chat_histories = {k: [] for k in st.session_state.chat_histories}
        st.session_state.brd_draft = ""
        st.rerun()
