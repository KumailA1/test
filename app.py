import streamlit as st
from google import genai

# =========================================================
# BRD Simulation MVP
# Tech: Streamlit + Gemini API
# Secret required in Streamlit Secrets:
# GEMINI_API_KEY = "your_api_key_here"
# =========================================================

APP_TITLE = "BRD Simulation"
AUTHOR_NAME = "Ali Alali"
LINKEDIN_URL = "https://www.linkedin.com/"
MODEL_NAME = "gemini-2.5-flash"

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📄",
    layout="wide",
)

# -----------------------------
# Basic Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main { background-color: #ffffff; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }
    .top-title { font-size: 22px; font-weight: 700; color: #1f2937; }
    .footer { position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; color: #6b7280; font-size: 13px; }
    .footer a { color: #2563eb; text-decoration: none; }
    .card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 18px; margin-bottom: 14px; background: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
    .muted { color: #6b7280; }
    .small { font-size: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header / Footer
# -----------------------------
def render_header():
    st.markdown(f'<div class="top-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.divider()


def render_footer():
    st.markdown(
        f'<div class="footer">Created by <a href="{LINKEDIN_URL}" target="_blank">{AUTHOR_NAME}</a></div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Gemini Client
# -----------------------------
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
        st.stop()
    return genai.Client(api_key=api_key)


def call_gemini(prompt: str, temperature: float = 0.4) -> str:
    client = get_client()
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": 450,
            },
        )
        return response.text.strip() if response.text else "I could not generate a response."
    except Exception as e:
        return f"Error while contacting Gemini: {e}"

# -----------------------------
# Session State
# -----------------------------
def init_state():
    defaults = {
        "step": "welcome",
        "user_name": "",
        "problem_statement": "",
        "brd": {
            "overview": "",
            "objectives": "",
            "scope_in": "",
            "scope_out": "",
            "business_requirements": "",
            "functional_requirements": "",
            "acceptance_criteria": "",
        },
        "review": "",
        "chats": {},
        "completed_interviews": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

# -----------------------------
# Data
# -----------------------------
EMAIL_TEXT = """
From: Abdullah Salem — Operations Director  
To: {name} — Business Analyst  
Subject: Urgent Investigation Required — Delivery Delays

Good morning,

Over the past three months, Veltra Logistics has experienced a noticeable increase in delayed deliveries across multiple cities. Customer complaints related to delivery delays have increased by 35%, and our average delivery delay has reached 28 minutes during peak hours.

This issue is beginning to negatively affect customer satisfaction and overall operational performance. Recent customer satisfaction reports show a drop from 82% to 64%, and refund requests related to delayed orders are continuing to rise.

At this stage, management would like a clearer understanding of:
- what is causing these delays,
- how current delivery operations are functioning,
- and what improvements may be required.

You have been assigned to investigate the issue, communicate with the relevant stakeholders, and help identify potential business and operational requirements.

The following stakeholders are available for discussion:
- Sarah Walid — Operations Manager
- Omar Khalid — Customer Support Lead
- Faisal Saad — Delivery Driver
- Naser Bader — CEO
- Reem Fahd — Customer

Please begin your investigation as soon as possible.

Regards,  
Abdullah Salem  
Operations Director  
Veltra Logistics
"""

STAKEHOLDERS = {
    "Sarah Walid": {
        "role": "Operations Manager",
        "responsibility": "Responsible for overseeing delivery operations and driver assignments.",
        "prompt": """
You are Sarah Walid, the Operations Manager at Veltra Logistics.

Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.

Your Responsibilities:
- Oversee daily delivery operations.
- Manage driver assignments and dispatching activities.
- Monitor operational efficiency and delivery performance.
- Identify bottlenecks in the delivery process.

Personality:
- Direct, busy, practical, KPI-focused.
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
- Keep answers realistic, concise, and professional.
""",
    },
    "Omar Khalid": {
        "role": "Customer Support Lead",
        "responsibility": "Responsible for handling customer complaints and communication.",
        "prompt": """
You are Omar Khalid, the Customer Support Lead at Veltra Logistics.

Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.

Your Responsibilities:
- Handle customer complaints and support escalations.
- Monitor repeated customer issues.
- Communicate customer pain points to internal teams.
- Track complaint trends and service quality issues.

Personality:
- Helpful, friendly, overwhelmed, customer-focused.
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
- If the user asks unrelated questions, politely redirect back to customer complaints and delivery delay issues.
- Keep answers realistic, concise, and professional.
""",
    },
    "Faisal Saad": {
        "role": "Delivery Driver",
        "responsibility": "Responsible for delivering orders and reporting field-related issues.",
        "prompt": """
You are Faisal Saad, a Delivery Driver at Veltra Logistics.

Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.

Your Responsibilities:
- Deliver customer orders.
- Follow assigned delivery routes.
- Report field-related issues.
- Communicate with dispatchers when there are route or order problems.

Personality:
- Honest, practical, straightforward, field-focused.
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
- Only discuss delivery work, routes, assignments, and field issues.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect back to delivery work and route issues.
- Keep answers realistic and concise.
""",
    },
    "Naser Bader": {
        "role": "CEO",
        "responsibility": "Responsible for overseeing business performance and strategic direction.",
        "prompt": """
You are Naser Bader, the CEO of Veltra Logistics.

Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.

Your Responsibilities:
- Oversee business performance and strategic direction.
- Protect company reputation and customer trust.
- Ensure operational issues do not affect growth.
- Prioritize business goals and investment decisions.

Personality:
- Strategic, concise, business-focused.
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
- Only discuss business impact, customer trust, performance, and strategy.
- Do not provide ready-made business requirements.
- Do not directly suggest a complete solution.
- Do not say “the system shall”.
- Do not break character.
- Do not mention that you are an AI.
- Share information gradually based on the quality of the user's questions.
- If the user asks unrelated questions, politely redirect back to the business impact of delivery delays.
- Avoid operational details unless asked at a high level.
""",
    },
    "Reem Fahd": {
        "role": "Customer",
        "responsibility": "Uses the delivery service and reports customer experience issues.",
        "prompt": """
You are Reem Fahd, a customer of Veltra Logistics.

Project Context:
Veltra Logistics is experiencing increased delivery delays across multiple cities. Customer complaints related to delivery delays increased by 35%, the average delay reached 28 minutes during peak hours, and customer satisfaction dropped from 82% to 64%.

Your Responsibilities:
- You are not an employee.
- You use Veltra Logistics delivery services.
- You can only speak from your personal customer experience.

Personality:
- Honest, emotional, simple language.
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
- If the user asks unrelated questions, politely redirect back to your delivery experience.
- Keep answers realistic and concise.
""",
    },
}

SAMPLE_BRD = """
# Sample BRD — Veltra Logistics Delivery Delay Project

This is one possible BRD submission. It is not the only correct answer.

## 1. Project Overview

Veltra Logistics is a mid-sized delivery company operating across multiple cities. Over the past three months, the company has experienced a noticeable increase in delayed deliveries, especially during peak hours. This issue has affected customer satisfaction, increased refund requests, and created pressure on operations, drivers, and customer support teams.

The purpose of this project is to investigate the causes of delivery delays and identify business and system requirements that can improve delivery performance, communication, and customer visibility.

## 2. Business Objectives

- Reduce average delivery delays during peak hours.
- Improve customer satisfaction related to delivery services.
- Reduce delivery-related customer complaints and refund requests.
- Improve communication between dispatchers, drivers, and customer support teams.
- Increase visibility into delivery operations and order status.

## 3. Project Scope

### In Scope
- Driver assignment process
- Delivery tracking visibility
- Dispatcher and driver communication
- Customer delivery status updates
- Customer support access to delivery information
- Peak-hour delivery operations

### Out of Scope
- Payment systems
- Warehouse inventory management
- Marketing systems
- HR and recruitment processes
- Vendor management systems

## 4. Business Requirements

- The business requires improved visibility into delivery operations.
- The business requires faster and more efficient driver assignment during peak hours.
- The business requires better communication between operations and customer support teams.
- The business requires improved customer communication regarding delivery status and delays.
- The business requires reduced delivery-related complaints and refund requests.

## 5. Functional Requirements

- The system should provide real-time delivery tracking.
- The system should display updated estimated delivery times.
- The system should notify customers when delivery delays occur.
- The system should allow dispatchers to assign drivers through a centralized platform.
- The system should provide delivery status visibility for customer support agents.
- The system should allow drivers to receive assignment updates in real time.
- The system should generate operational reports related to delivery delays and peak-hour performance.
- The system should allow dispatchers to monitor active deliveries through a dashboard.

## 6. Acceptance Criteria

- Average delivery delays are reduced by at least 30% within three months.
- Customer satisfaction increases from 64% to at least 80%.
- Delivery-related complaints decrease by at least 25%.
- Customer support agents can access live delivery status information.
- Drivers receive delivery assignments without manual communication delays.
- Dispatchers can monitor active delivery performance through a centralized dashboard.
"""

# -----------------------------
# Helper Functions
# -----------------------------
def go(step: str):
    st.session_state.step = step
    st.rerun()


def reset_simulation():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def build_review_prompt() -> str:
    brd = st.session_state.brd
    return f"""
You are a supportive Senior Business Analyst reviewing a beginner-to-intermediate Business Analyst's BRD work.

Important rules:
- Review only what the user wrote.
- Do not review stakeholder interviews.
- Be kind, encouraging, professional, and constructive.
- Do not provide a full corrected answer.
- Do not write the solution for the user.
- Give feedback section by section.
- Use this format for each section:
  ✅ Strengths
  ⚠ Suggestions
- Avoid harsh words like wrong, bad, or incorrect.
- Keep the review concise but useful.

User Submission:

Problem Statement:
{st.session_state.problem_statement}

Project Overview:
{brd['overview']}

Business Objectives:
{brd['objectives']}

In Scope:
{brd['scope_in']}

Out of Scope:
{brd['scope_out']}

Business Requirements:
{brd['business_requirements']}

Functional Requirements:
{brd['functional_requirements']}

Acceptance Criteria:
{brd['acceptance_criteria']}
"""


def build_chat_prompt(stakeholder_name: str, user_message: str) -> str:
    stakeholder = STAKEHOLDERS[stakeholder_name]
    history = st.session_state.chats.get(stakeholder_name, [])[-8:]
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    return f"""
{stakeholder['prompt']}

Conversation History:
{history_text}

Current User Question:
{user_message}

Respond as {stakeholder_name}. Keep the answer natural and not too long.
"""

# -----------------------------
# Screens
# -----------------------------
def screen_welcome():
    st.title("Welcome to the BRD Simulation")
    st.write("Experience a realistic Business Analysis scenario. Communicate with stakeholders, gather information, and create a professional BRD.")
    name = st.text_input("Enter your name", value=st.session_state.user_name)
    if st.button("Start Simulation", type="primary"):
        if not name.strip():
            st.warning("Please enter your name to start.")
        else:
            st.session_state.user_name = name.strip()
            go("intro")


def screen_intro():
    st.title(f"Welcome, {st.session_state.user_name}")
    st.write("You are now working as a Business Analyst at Veltra Logistics.")
    st.info("Monday — 8:12 AM\n\nYou have received a new urgent email from the Operations Director.")
    if st.button("Open Email", type="primary"):
        go("email")


def screen_email():
    st.title("Incoming Email")
    st.markdown(EMAIL_TEXT.format(name=st.session_state.user_name))
    if st.button("Continue", type="primary"):
        go("notice")


def screen_notice():
    st.title("Before You Begin")
    st.warning("This simulation does not currently save progress automatically. If you refresh the page or leave the website, your work may be lost.")
    st.write("For the best experience, consider saving your notes or important responses externally while completing the simulation.")
    if st.button("Continue Simulation", type="primary"):
        go("problem")


def screen_problem():
    st.title("Write the Problem Statement")
    st.write("Based on the email and the available information, write a clear problem statement describing the business issue.")
    st.markdown("""
**Consider:**
- What is the problem?
- Who is affected?
- What is the business impact?
""")
    st.session_state.problem_statement = st.text_area(
        "Problem Statement",
        value=st.session_state.problem_statement,
        height=180,
    )
    if st.button("Continue", type="primary"):
        go("directory")


def screen_directory():
    st.title("Stakeholders Directory")
    st.write("The following stakeholders are available for discussion regarding the delivery delay issue.")

    for name, data in STAKEHOLDERS.items():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(name)
                st.write(f"**{data['role']}**")
                st.write(data["responsibility"])
                if name in st.session_state.completed_interviews:
                    st.success("Interview completed")
            with col2:
                if st.button("Start Interview", key=f"interview_{name}"):
                    st.session_state.active_stakeholder = name
                    go("chat")

    st.divider()
    if st.button("Continue to BRD", type="primary"):
        go("brd")


def screen_chat():
    name = st.session_state.active_stakeholder
    data = STAKEHOLDERS[name]

    st.title(f"Interview: {name}")
    st.caption(f"{data['role']} — {data['responsibility']}")

    if name not in st.session_state.chats:
        st.session_state.chats[name] = []

    for msg in st.session_state.chats[name]:
        with st.chat_message("user" if msg["role"] == "User" else "assistant"):
            st.write(msg["content"])

    user_message = st.chat_input("Ask your interview question...")
    if user_message:
        st.session_state.chats[name].append({"role": "User", "content": user_message})
        prompt = build_chat_prompt(name, user_message)
        answer = call_gemini(prompt, temperature=0.5)
        st.session_state.chats[name].append({"role": name, "content": answer})
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mark Interview Completed"):
            st.session_state.completed_interviews.add(name)
            go("directory")
    with col2:
        if st.button("Back to Stakeholders"):
            go("directory")


def screen_brd():
    st.title("Build the BRD")
    st.write("Based on the stakeholder interviews and the collected information, complete the following BRD sections.")

    brd = st.session_state.brd

    brd["overview"] = st.text_area("1. Project Overview", value=brd["overview"], height=150)
    brd["objectives"] = st.text_area("2. Business Objectives", value=brd["objectives"], height=150)

    st.subheader("3. Project Scope")
    brd["scope_in"] = st.text_area("In Scope", value=brd["scope_in"], height=120)
    brd["scope_out"] = st.text_area("Out of Scope", value=brd["scope_out"], height=120)

    st.subheader("4. Business & Functional Requirements")
    brd["business_requirements"] = st.text_area("Business Requirements", value=brd["business_requirements"], height=150)
    brd["functional_requirements"] = st.text_area("Functional Requirements", value=brd["functional_requirements"], height=180)

    brd["acceptance_criteria"] = st.text_area("5. Acceptance Criteria", value=brd["acceptance_criteria"], height=150)

    if st.button("Submit BRD for Review", type="primary"):
        with st.spinner("Reviewing your BRD..."):
            st.session_state.review = call_gemini(build_review_prompt(), temperature=0.3)
        go("review")


def screen_review():
    st.title("BRD Review & Feedback")
    st.markdown(st.session_state.review)

    st.divider()
    if st.button("View Sample BRD", type="primary"):
        go("sample")


def screen_sample():
    st.title("Sample BRD")
    st.info("This is one possible BRD submission. It is not the only correct answer.")
    st.markdown(SAMPLE_BRD)

    st.divider()
    if st.button("Finish Simulation", type="primary"):
        go("final")


def screen_final():
    st.title("Thank You for Completing the Simulation")
    st.write("Thank you for participating in the BRD Simulation experience.")
    st.write("If you have any suggestions, feedback, or ideas for future simulations, feel free to connect with me on LinkedIn.")
    st.link_button("Connect on LinkedIn", LINKEDIN_URL)

    st.divider()
    if st.button("Restart Simulation"):
        reset_simulation()

# -----------------------------
# Router
# -----------------------------
render_header()

step = st.session_state.step
if step == "welcome":
    screen_welcome()
elif step == "intro":
    screen_intro()
elif step == "email":
    screen_email()
elif step == "notice":
    screen_notice()
elif step == "problem":
    screen_problem()
elif step == "directory":
    screen_directory()
elif step == "chat":
    screen_chat()
elif step == "brd":
    screen_brd()
elif step == "review":
    screen_review()
elif step == "sample":
    screen_sample()
elif step == "final":
    screen_final()
else:
    screen_welcome()

render_footer()

# Sidebar controls
with st.sidebar:
    st.subheader("Simulation Menu")
    if st.button("Restart"):
        reset_simulation()
    st.caption("Progress is saved only during the current session.")
