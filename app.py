import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import time
import json

st.set_page_config(page_title="MatchMatrix", layout="wide", page_icon=None)

# ----------------------------
# LIQUID GLASS / CLEAN UI CSS
# ----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    .main > div { padding: 2rem 1.5rem; }

    /* Glass card base */
    .glass {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.15);
    }

    .glass-accent {
        background: rgba(99, 102, 241, 0.15);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.1), inset 0 1px 0 rgba(255,255,255,0.1);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8));
        backdrop-filter: blur(10px);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.02em;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.25s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 1), rgba(139, 92, 246, 1));
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #a5b4fc;
    }
    div[data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSlider,
    section[data-testid="stSidebar"] p {
        color: rgba(255,255,255,0.85) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 9px;
        color: rgba(255,255,255,0.6);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.5rem 1.2rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.35) !important;
        color: white !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99,102,241,0.4) !important;
    }

    /* Inputs */
    .stTextInput input, .stSelectbox select, div[data-baseweb="select"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    .stTextInput input:focus {
        border-color: rgba(99,102,241,0.6) !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }

    /* Text areas */
    textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* Alert/info boxes */
    .stAlert {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }

    /* Typography */
    h1, h2, h3, h4 { color: white !important; }
    p, li, .stMarkdown { color: rgba(255,255,255,0.85) !important; }
    .stCaption { color: rgba(255,255,255,0.4) !important; }

    /* Match card */
    .match-card {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin: 0.75rem 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 4px 20px rgba(99,102,241,0.1);
    }

    /* API key badge */
    .api-status-connected {
        display: inline-block;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.4);
        color: #86efac;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .api-status-missing {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .ai-badge {
        display: inline-block;
        background: rgba(99,102,241,0.25);
        border: 1px solid rgba(99,102,241,0.4);
        color: #a5b4fc;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 600;
        margin-left: 6px;
        vertical-align: middle;
    }

    /* Toggle */
    .stToggle { color: rgba(255,255,255,0.85) !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# MOCK DATA
# ----------------------------
STUDENTS_CSV = """name,skills,preferences,free_text
Alice Chen,Python;Machine Learning;Data Viz,Robotics Lab;AI Research;Web Dev,"I love building ML models and visualising data. Python is my main language and I'd enjoy AI research."
Ben Okafor,Java;Web Dev;UI Design,Web Dev;Mobile Apps;AI Research,"I enjoy full-stack web development and designing clean user interfaces. Java is my strongest language."
Carla Diaz,Python;Robotics;C++,Robotics Lab;AI Research;Embedded Systems,"Robotics is my passion — I've built autonomous vehicles. Strong in Python and C++."
David Kim,Data Viz;SQL;Python,AI Research;Web Dev;Data Science,"I love turning raw data into insights. SQL and Python are my go-to tools for data science."
Emma Wilson,Mobile Apps;UI Design;Java,Mobile Apps;Web Dev;UI/UX,"I've shipped two Android apps and care deeply about UX and accessibility."
Farid Hassan,C++;Embedded Systems;Robotics,Embedded Systems;Robotics Lab;Hardware,"I enjoy low-level embedded programming on microcontrollers. Hardware projects excite me."
Grace Lee,Machine Learning;Python;SQL,AI Research;Data Science;Robotics Lab,"ML research is where I want to go — I've implemented NLP pipelines and love experimentation."
Henry Novak,Web Dev;UI Design;Mobile Apps,Web Dev;Mobile Apps;UI/UX,"I'm a frontend developer who can do mobile too. I care about responsive, beautiful interfaces."
Isla Murphy,Data Science;Python;SQL,Data Science;AI Research;Web Dev,"Data science is my focus — statistical analysis, Python, SQL. I'd love a project on real-world data."
Jamal Brooks,Robotics;C++;Hardware,Robotics Lab;Embedded Systems;Hardware,"I build robots. Hardware, embedded C++, sensor fusion — that's my world."
"""

PROJECTS_CSV = """title,required_skills,supervisor,capacity
Autonomous Robot Navigation,Robotics;C++;Embedded Systems,Dr. Patel,2
AI Research - NLP Models,Python;Machine Learning;Data Viz,Dr. Singh,2
Web Dev - Student Portal,Web Dev;UI Design;Java,Prof. Adams,3
Mobile Apps - Campus App,Mobile Apps;UI Design;Java,Prof. Adams,2
Data Science - Enrollment Trends,Data Science;SQL;Python,Dr. Lopez,2
Embedded Systems - IoT Sensors,Embedded Systems;C++;Hardware,Dr. Patel,1
"""

PROJECT_TYPE_MAP = {
    "Autonomous Robot Navigation": "Robotics Lab",
    "AI Research - NLP Models": "AI Research",
    "Web Dev - Student Portal": "Web Dev",
    "Mobile Apps - Campus App": "Mobile Apps",
    "Data Science - Enrollment Trends": "Data Science",
    "Embedded Systems - IoT Sensors": "Embedded Systems",
}

# ----------------------------
# HELPERS
# ----------------------------
def parse_tags(s):
    return set(x.strip() for x in str(s).split(";") if x.strip())

def load_default_data():
    students = pd.read_csv(StringIO(STUDENTS_CSV))
    projects = pd.read_csv(StringIO(PROJECTS_CSV))
    return students, projects

def skill_overlap_score(student_skills, project_skills):
    s = parse_tags(student_skills)
    p = parse_tags(project_skills)
    if not p:
        return 0.0
    return len(s & p) / len(p)

def preference_score(student_prefs, project_title):
    prefs = [x.strip() for x in str(student_prefs).split(";") if x.strip()]
    project_type = PROJECT_TYPE_MAP.get(project_title, project_title)
    if project_type in prefs:
        rank = prefs.index(project_type)
        return max(0.0, 1.0 - rank / len(prefs))
    return 0.0

def availability_score(project_capacity, current_load):
    if project_capacity <= 0:
        return 0.0
    return max(0.0, (project_capacity - current_load) / project_capacity)

def get_api_key():
    """Get API key from session state."""
    return st.session_state.get("anthropic_api_key", "").strip()

def has_api_key():
    return bool(get_api_key())

# ----------------------------
# SEMANTIC MATCHING
# ----------------------------
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer('all-MiniLM-L6-v2')
    except ImportError:
        return None

@st.cache_data(show_spinner=False)
def compute_semantic_matrix(_model, student_skills_list, project_skills_list, student_names, project_titles):
    try:
        import scipy.spatial.distance as dist
        student_emb = _model.encode(student_skills_list)
        project_emb = _model.encode(project_skills_list)
        similarity = 1 - dist.cdist(student_emb, project_emb, metric='cosine')
        return pd.DataFrame(similarity, index=student_names, columns=project_titles)
    except Exception:
        return None

def compute_match_matrix(students, projects, w_skill, w_pref, w_avail, loads, semantic_df=None):
    rows = []
    for _, srow in students.iterrows():
        for _, prow in projects.iterrows():
            if semantic_df is not None:
                sk = float(semantic_df.loc[srow["name"], prow["title"]])
            else:
                sk = skill_overlap_score(srow["skills"], prow["required_skills"])
            pr = preference_score(srow["preferences"], prow["title"])
            av = availability_score(prow["capacity"], loads.get(prow["title"], 0))
            score = w_skill * sk + w_pref * pr + w_avail * av
            rows.append({
                "student": srow["name"],
                "project": prow["title"],
                "skill_score": round(sk, 3),
                "preference_score": round(pr, 3),
                "availability_score": round(av, 3),
                "match_score": round(score, 3),
            })
    return pd.DataFrame(rows)

# ----------------------------
# GALE-SHAPLEY
# ----------------------------
def build_student_prefs(matrix_df, project_titles):
    prefs = {}
    for student in matrix_df["student"].unique():
        sub = matrix_df[matrix_df["student"] == student].sort_values("match_score", ascending=False)
        prefs[student] = sub["project"].tolist()
    return prefs

def build_supervisor_prefs(matrix_df, students_list):
    prefs = {}
    for project in matrix_df["project"].unique():
        sub = matrix_df[matrix_df["project"] == project].sort_values("match_score", ascending=False)
        prefs[project] = sub["student"].tolist()
    return prefs

def gale_shapley(student_prefs, supervisor_prefs, capacities):
    free_students = list(student_prefs.keys())
    next_proposal = {s: 0 for s in free_students}
    project_slots = {p: [] for p in supervisor_prefs}
    student_match = {}
    proj_rank = {
        proj: {stu: idx for idx, stu in enumerate(supervisor_prefs[proj])}
        for proj in supervisor_prefs
    }
    while free_students:
        s = free_students.pop(0)
        s_prefs = student_prefs[s]
        if next_proposal[s] >= len(s_prefs):
            student_match[s] = "UNASSIGNED"
            continue
        proj = s_prefs[next_proposal[s]]
        next_proposal[s] += 1
        cap = capacities.get(proj, 1)
        if len(project_slots[proj]) < cap:
            project_slots[proj].append(s)
            student_match[s] = proj
        else:
            current = project_slots[proj]
            worst = max(current, key=lambda x: proj_rank[proj].get(x, 9999))
            if proj_rank[proj].get(s, 9999) < proj_rank[proj].get(worst, 9999):
                current.remove(worst)
                current.append(s)
                student_match[s] = proj
                student_match[worst] = None
                free_students.append(worst)
            else:
                free_students.append(s)
    return student_match

def run_gale_shapley(matrix_df, projects):
    capacities = dict(zip(projects["title"], projects["capacity"]))
    all_projects = projects["title"].tolist()
    all_students = matrix_df["student"].unique().tolist()
    student_prefs = build_student_prefs(matrix_df, all_projects)
    supervisor_prefs = build_supervisor_prefs(matrix_df, all_students)
    return gale_shapley(student_prefs, supervisor_prefs, capacities)

# ----------------------------
# GREEDY MATCHING
# ----------------------------
def greedy_assign(matrix_df, projects, fairness):
    capacities = dict(zip(projects["title"], projects["capacity"]))
    remaining = capacities.copy()
    assigned = {}
    assignment_log = []
    df = matrix_df.copy()
    popularity = df.groupby("project")["match_score"].mean().to_dict()
    max_pop = max(popularity.values()) if popularity else 1
    df["adj_score"] = df.apply(
        lambda r: r["match_score"] - fairness * 0.3 * (popularity.get(r["project"], 0) / max_pop),
        axis=1
    )
    df = df.sort_values("adj_score", ascending=False)
    for _, row in df.iterrows():
        student, project = row["student"], row["project"]
        if student in assigned:
            continue
        if remaining.get(project, 0) > 0:
            assigned[student] = project
            remaining[project] -= 1
            assignment_log.append({
                "student": student, "project": project,
                "match_score": row["match_score"], "adj_score": round(row["adj_score"], 3),
            })
    for student in matrix_df["student"].unique():
        if student not in assigned:
            assignment_log.append({
                "student": student, "project": "UNASSIGNED",
                "match_score": 0.0, "adj_score": 0.0,
            })
    return pd.DataFrame(assignment_log), remaining

# ----------------------------
# HUNGARIAN SMART RESOLVE
# ----------------------------
def smart_resolve(unassigned_students, available_projects, match_score_matrix):
    try:
        from scipy.optimize import linear_sum_assignment
    except ImportError:
        return {}
    if not unassigned_students or not available_projects:
        return {}
    valid_students = [s for s in unassigned_students if s in match_score_matrix.index]
    valid_projects = [p for p in available_projects if p in match_score_matrix.columns]
    if not valid_students or not valid_projects:
        return {}
    sub = match_score_matrix.loc[valid_students, valid_projects]
    cost = -sub.values
    row_ind, col_ind = linear_sum_assignment(cost)
    return {valid_students[i]: valid_projects[j] for i, j in zip(row_ind, col_ind)}

# ----------------------------
# LLM CALLS (Claude API)
# Uses API key from session state
# ----------------------------
def llm_explain_match(student_name, student_skills, student_free_text, project_title,
                       project_skills, skill_score, pref_score, avail_score,
                       supervisor_qa=None):
    """Generate a personalised match explanation using Claude."""
    import requests
    api_key = get_api_key()
    if not api_key:
        return None

    qa_section = ""
    if supervisor_qa:
        qa_section = f"\nAdditional supervisor questions and student answers:\n{supervisor_qa}\n"

    prompt = f"""You are a friendly academic advisor explaining why a student was matched to a project.

Student: {student_name}
Student skills: {student_skills}
Student's own statement: "{student_free_text}"{qa_section}
Matched project: {project_title}
Project required skills: {project_skills}
Match score breakdown: skill alignment={skill_score:.2f}, preference match={pref_score:.2f}, availability={avail_score:.2f}

Write 2-3 friendly sentences explaining why this match makes sense. Reference specific skills and the student's interests. Be encouraging and specific. Do not use bullet points. Do not include any numerical scores or percentages."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 250,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=20
        )
        data = response.json()
        if "content" in data:
            return data["content"][0]["text"].strip()
        return None
    except Exception:
        return None

def llm_extract_preferences(free_text, project_titles):
    """Use Claude to rank projects from a free-text statement."""
    import requests
    api_key = get_api_key()
    if not api_key:
        return project_titles

    prompt = f"""Given this student's statement: "{free_text}"
The available projects are: {', '.join(project_titles)}
Return a JSON array of project titles ranked from most to least suitable for this student.
Output ONLY valid JSON, no other text. Example: ["Project A", "Project B", "Project C"]"""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        text = data["content"][0]["text"].strip()
        ranked = json.loads(text)
        return ranked
    except Exception:
        return project_titles

def llm_score_qa_answers(student_name, questions_answers, project_title, project_skills):
    """Use Claude to score a student's answers to supervisor questions and return a numeric bonus score 0-1."""
    import requests
    api_key = get_api_key()
    if not api_key:
        return 0.0

    qa_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in questions_answers.items()])
    prompt = f"""You are evaluating how well a student's answers to supervisor questions align with a project.

Project: {project_title}
Project required skills: {project_skills}
Student: {student_name}

Supervisor questions and student answers:
{qa_text}

Rate the overall fit of this student for the project based ONLY on their answers.
Respond with ONLY a JSON object like: {{"score": 0.75, "rationale": "brief reason"}}
Score must be between 0.0 and 1.0. Output ONLY valid JSON."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 150,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        result = json.loads(data["content"][0]["text"].strip())
        return float(result.get("score", 0.0)), result.get("rationale", "")
    except Exception:
        return 0.0, ""

# ----------------------------
# RULE-BASED FALLBACK EXPLANATION
# ----------------------------
def explain_match_rule_based(student_row, project_row, score_row):
    skills_overlap = parse_tags(student_row["skills"]) & parse_tags(project_row["required_skills"])
    prefs = [x.strip() for x in str(student_row["preferences"]).split(";") if x.strip()]
    project_type = PROJECT_TYPE_MAP.get(project_row["title"], project_row["title"])
    if project_type in prefs:
        rank = prefs.index(project_type) + 1
        rank_text = f"this was among your top preferences"
    else:
        rank_text = "this project matched well on skills and availability"
    skill_text = ", ".join(skills_overlap) if skills_overlap else "relevant technical areas"
    return (
        f"You were matched with **{project_row['title']}** (supervisor: {project_row['supervisor']}). "
        f"Your skills in **{skill_text}** aligned with this project's requirements, "
        f"and {rank_text}."
    )

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "students" not in st.session_state:
    s, p = load_default_data()
    st.session_state.students = s
    st.session_state.projects = p

for key in ["assignments", "matrix", "semantic_df", "llm_explanations", "ai_prefs"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "use_semantic" not in st.session_state:
    st.session_state.use_semantic = False
if "use_gale_shapley" not in st.session_state:
    st.session_state.use_gale_shapley = True
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = ""
# Supervisor custom questions: dict {project_title: [question strings]}
if "supervisor_questions" not in st.session_state:
    st.session_state.supervisor_questions = {}
# Student answers: dict {student_name: {project_title: {question: answer}}}
if "student_answers" not in st.session_state:
    st.session_state.student_answers = {}

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.markdown("## MatchMatrix")
st.sidebar.markdown("---")

# --- API KEY SECTION ---
st.sidebar.markdown("### Anthropic API Key")
api_key_input = st.sidebar.text_input(
    "Enter your API key",
    value=st.session_state.anthropic_api_key,
    type="password",
    placeholder="sk-ant-...",
    help="Your Anthropic API key is stored only in this session and never persisted to disk."
)
if api_key_input != st.session_state.anthropic_api_key:
    st.session_state.anthropic_api_key = api_key_input

if has_api_key():
    st.sidebar.markdown('<span class="api-status-connected">Connected</span>', unsafe_allow_html=True)
    st.sidebar.caption("Claude AI features are active.")
else:
    st.sidebar.markdown('<span class="api-status-missing">Not Connected</span>', unsafe_allow_html=True)
    st.sidebar.caption("Add your key to enable AI explanations and question scoring.")

st.sidebar.markdown("---")

st.sidebar.markdown("### 1. Data Input")
data_mode = st.sidebar.radio("Data source", ["Use sample data", "Upload CSVs"], label_visibility="collapsed")

if data_mode == "Upload CSVs":
    st.sidebar.markdown("**Students CSV** — columns: `name, skills, preferences, free_text`")
    students_file = st.sidebar.file_uploader("Upload Students CSV", type="csv", key="students_csv")
    st.sidebar.markdown("**Projects CSV** — columns: `title, required_skills, supervisor, capacity`")
    projects_file = st.sidebar.file_uploader("Upload Projects CSV", type="csv", key="projects_csv")
    if students_file:
        st.session_state.students = pd.read_csv(students_file)
    if projects_file:
        st.session_state.projects = pd.read_csv(projects_file)
else:
    s, p = load_default_data()
    st.session_state.students = s
    st.session_state.projects = p

st.sidebar.markdown("### 2. AI Features")
use_semantic = st.sidebar.toggle(
    "Semantic skill matching",
    value=False,
    help="Uses sentence-transformers to understand skill synonyms. Falls back to keyword matching if unavailable."
)
use_gs = st.sidebar.toggle(
    "Gale-Shapley stable matching",
    value=True,
    help="Two-sided stable matching algorithm. When OFF, uses greedy assignment."
)
use_llm_explain = st.sidebar.toggle(
    "AI match explanations (Claude)",
    value=False,
    help="Generate personalised explanations using Claude AI. Requires API key above."
)
use_qa_scoring = st.sidebar.toggle(
    "Score supervisor questions with Claude",
    value=False,
    help="When supervisors add custom questions, Claude scores student answers to improve matching."
)

st.sidebar.markdown("### 3. Scoring Weights")
w_skill = st.sidebar.slider("Skill overlap weight", 0.0, 1.0, 0.5, 0.05)
w_pref = st.sidebar.slider("Student preference weight", 0.0, 1.0, 0.3, 0.05)
w_avail = st.sidebar.slider("Availability weight", 0.0, 1.0, 0.2, 0.05)
total_w = w_skill + w_pref + w_avail or 1
w_skill, w_pref, w_avail = w_skill/total_w, w_pref/total_w, w_avail/total_w
st.sidebar.caption(f"Normalised: Skill {w_skill:.2f} | Pref {w_pref:.2f} | Avail {w_avail:.2f}")

if not use_gs:
    st.sidebar.markdown("### 4. Fairness (Greedy mode)")
    fairness = st.sidebar.slider("Top choice vs Equal distribution", 0.0, 1.0, 0.3, 0.05)
else:
    fairness = 0.3

run_button = st.sidebar.button("Run Matching", use_container_width=True)

with st.sidebar.expander("Responsible AI & Fairness"):
    st.markdown("""
**Appropriate data?** Only skills, preferences, and optional free-text — no protected attributes.

**Exclusion risks?** All scores visible to staff. Staff can override any decision.

**Accountability?** Every match traces to weighted score components. Staff have final approval.

**Support learning?** AI explanations help students understand outcomes without exposing raw numbers.

**Pre-implementation checks?** Pilot with a small cohort, measure satisfaction, allow opt-out.
    """)

# ----------------------------
# MAIN HEADER
# ----------------------------
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.25rem;">
        MatchMatrix
    </h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 1rem; margin: 0;">
        AI-assisted project allocation — fair, transparent, data-driven
    </p>
</div>
""", unsafe_allow_html=True)

# Status badges
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
with col_b1:
    method = "Semantic NLP" if use_semantic else "Keyword"
    st.markdown(f'<div class="glass" style="padding:0.75rem 1rem; text-align:center;"><span style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.08em;">Skill Matching</span><br><strong style="font-size:0.9rem;">{method}</strong></div>', unsafe_allow_html=True)
with col_b2:
    algo = "Gale-Shapley" if use_gs else "Greedy"
    st.markdown(f'<div class="glass" style="padding:0.75rem 1rem; text-align:center;"><span style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.08em;">Algorithm</span><br><strong style="font-size:0.9rem;">{algo}</strong></div>', unsafe_allow_html=True)
with col_b3:
    exp = "Claude AI" if (use_llm_explain and has_api_key()) else "Rule-based"
    st.markdown(f'<div class="glass" style="padding:0.75rem 1rem; text-align:center;"><span style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.08em;">Explanations</span><br><strong style="font-size:0.9rem;">{exp}</strong></div>', unsafe_allow_html=True)
with col_b4:
    qa_status = "Active" if (use_qa_scoring and has_api_key()) else "Off"
    st.markdown(f'<div class="glass" style="padding:0.75rem 1rem; text-align:center;"><span style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.08em;">Q&A Scoring</span><br><strong style="font-size:0.9rem;">{qa_status}</strong></div>', unsafe_allow_html=True)

st.divider()

tab_admin, tab_supervisor_q, tab_student, tab_data = st.tabs([
    "Admin View", "Supervisor Questions", "Student View", "Data Tables"
])

# ----------------------------
# DATA TAB
# ----------------------------
with tab_data:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Students")
        st.dataframe(st.session_state.students, use_container_width=True)
    with col2:
        st.subheader("Projects")
        st.dataframe(st.session_state.projects, use_container_width=True)

# ----------------------------
# SUPERVISOR QUESTIONS TAB
# ----------------------------
with tab_supervisor_q:
    st.subheader("Supervisor Custom Questions")
    st.markdown("""
Staff can add bespoke questions for each project. Students answer these when viewing their matches.
When Claude scoring is enabled, answers are evaluated by Claude to produce a richer match score.
Questions are shown to students without revealing any numerical scores.
    """)

    projects_df = st.session_state.projects
    for _, proj_row in projects_df.iterrows():
        proj_title = proj_row["title"]
        with st.expander(f"{proj_title}  —  {proj_row['supervisor']}"):
            current_questions = st.session_state.supervisor_questions.get(proj_title, [])

            st.markdown(f"**Current questions ({len(current_questions)}):**")
            questions_to_keep = []
            for i, q in enumerate(current_questions):
                col_q, col_del = st.columns([5, 1])
                with col_q:
                    st.markdown(f"{i+1}. {q}")
                with col_del:
                    if st.button("Remove", key=f"del_q_{proj_title}_{i}"):
                        pass  # will be filtered below
                    else:
                        questions_to_keep.append(q)
            st.session_state.supervisor_questions[proj_title] = questions_to_keep

            st.markdown("**Add a new question:**")
            new_q = st.text_input(
                "Question text",
                key=f"new_q_{proj_title}",
                placeholder="e.g. What experience do you have with sensor fusion?",
                label_visibility="collapsed"
            )
            if st.button("Add Question", key=f"add_q_{proj_title}"):
                if new_q.strip():
                    current = st.session_state.supervisor_questions.get(proj_title, [])
                    current.append(new_q.strip())
                    st.session_state.supervisor_questions[proj_title] = current
                    st.rerun()

    total_q = sum(len(v) for v in st.session_state.supervisor_questions.values())
    if total_q:
        st.info(f"{total_q} question(s) configured across {sum(1 for v in st.session_state.supervisor_questions.values() if v)} project(s).")

# ----------------------------
# RUN MATCHING
# ----------------------------
if run_button:
    students = st.session_state.students
    projects = st.session_state.projects

    with st.spinner("Computing match scores..."):
        semantic_df = None
        if use_semantic:
            model = load_embedding_model()
            if model is not None:
                student_skills_list = students["skills"].astype(str).tolist()
                project_skills_list = projects["required_skills"].astype(str).tolist()
                semantic_df = compute_semantic_matrix(
                    model,
                    tuple(student_skills_list), tuple(project_skills_list),
                    tuple(students["name"].tolist()), tuple(projects["title"].tolist())
                )
                st.session_state.semantic_df = semantic_df
            else:
                st.toast("sentence-transformers not installed — using keyword matching")

        matrix = compute_match_matrix(students, projects, w_skill, w_pref, w_avail, {}, semantic_df)

        # Apply Claude QA bonus scores if enabled and API key present
        if use_qa_scoring and has_api_key():
            bonus_rows = []
            for _, srow in students.iterrows():
                student_answers = st.session_state.student_answers.get(srow["name"], {})
                for _, prow in projects.iterrows():
                    proj_questions = st.session_state.supervisor_questions.get(prow["title"], [])
                    proj_answers = student_answers.get(prow["title"], {})
                    if proj_questions and proj_answers:
                        qa_pairs = {q: proj_answers.get(q, "") for q in proj_questions if proj_answers.get(q)}
                        if qa_pairs:
                            score, _ = llm_score_qa_answers(srow["name"], qa_pairs, prow["title"], prow["required_skills"])
                            bonus_rows.append({"student": srow["name"], "project": prow["title"], "qa_bonus": score * 0.2})

            if bonus_rows:
                bonus_df = pd.DataFrame(bonus_rows)
                matrix = matrix.merge(bonus_df, on=["student", "project"], how="left")
                matrix["qa_bonus"] = matrix["qa_bonus"].fillna(0)
                matrix["match_score"] = (matrix["match_score"] + matrix["qa_bonus"]).clip(upper=1.0).round(3)

        st.session_state.matrix = matrix

    if use_gs:
        with st.spinner("Running Gale-Shapley stable matching..."):
            time.sleep(0.3)
            gs_result = run_gale_shapley(matrix, projects)
            assignment_log = []
            for student, project in gs_result.items():
                proj_name = project if project else "UNASSIGNED"
                score_rows = matrix[(matrix["student"] == student) & (matrix["project"] == proj_name)]
                score_val = score_rows["match_score"].values[0] if len(score_rows) else 0.0
                assignment_log.append({
                    "student": student, "project": proj_name,
                    "match_score": score_val, "adj_score": score_val,
                })
            assigned_names = {r["student"] for r in assignment_log}
            for s_name in matrix["student"].unique():
                if s_name not in assigned_names:
                    assignment_log.append({
                        "student": s_name, "project": "UNASSIGNED",
                        "match_score": 0.0, "adj_score": 0.0,
                    })
            assignments = pd.DataFrame(assignment_log)
            cap_dict = dict(zip(projects["title"], projects["capacity"]))
            used = assignments[assignments["project"] != "UNASSIGNED"]["project"].value_counts().to_dict()
            remaining_capacity = {p: cap_dict[p] - used.get(p, 0) for p in cap_dict}
    else:
        with st.spinner("Running greedy matching..."):
            assignments, remaining_capacity = greedy_assign(matrix, projects, fairness)

    st.session_state.assignments = assignments
    st.session_state.remaining_capacity = remaining_capacity
    st.session_state.llm_explanations = {}
    st.toast("Matching complete.")

# ----------------------------
# ADMIN TAB
# ----------------------------
with tab_admin:
    if st.session_state.matrix is None:
        st.info("Configure weights and click **Run Matching** in the sidebar to generate results.")
    else:
        students = st.session_state.students
        projects = st.session_state.projects
        matrix = st.session_state.matrix
        assignments = st.session_state.assignments

        total_s = len(students)
        assigned_count = (assignments["project"] != "UNASSIGNED").sum()
        avg_score = assignments[assignments["project"] != "UNASSIGNED"]["match_score"].mean()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Students", total_s)
        m2.metric("Assigned", assigned_count)
        m3.metric("Unassigned", total_s - assigned_count)
        m4.metric("Avg Match Score", f"{avg_score:.2f}")

        st.divider()

        st.subheader("Match Score Heatmap")
        st.caption("Brighter = stronger match. All scores are visible to staff for full transparency.")
        pivot = matrix.pivot(index="student", columns="project", values="match_score")
        fig = px.imshow(
            pivot, color_continuous_scale="Viridis", aspect="auto",
            labels=dict(color="Match Score"),
        )
        fig.update_layout(
            height=420, margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("Score Breakdown — Assigned Students")
        assigned_names = assignments[assignments["project"] != "UNASSIGNED"]["student"].tolist()
        assigned_matrix = matrix[matrix["student"].isin(assigned_names)]
        assigned_merged = assigned_matrix.merge(assignments[["student", "project"]], on=["student", "project"])
        if not assigned_merged.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name="Skill", x=assigned_merged["student"], y=assigned_merged["skill_score"], marker_color="#6366f1"))
            fig2.add_trace(go.Bar(name="Preference", x=assigned_merged["student"], y=assigned_merged["preference_score"], marker_color="#22c55e"))
            fig2.add_trace(go.Bar(name="Availability", x=assigned_merged["student"], y=assigned_merged["availability_score"], marker_color="#f59e0b"))
            fig2.update_layout(
                barmode="stack", height=320, margin=dict(l=10, r=10, t=30, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="rgba(255,255,255,0.8)"
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        st.subheader("Suggested Assignments")
        st.caption("Scores visible to staff only. Students see qualitative explanations.")

        projects_list = projects["title"].tolist() + ["UNASSIGNED"]
        edited_rows = []
        for _, row in assignments.iterrows():
            c1, c2, c3 = st.columns([2, 3, 2])
            with c1:
                st.markdown(f"**{row['student']}**")
            with c2:
                idx = projects_list.index(row["project"]) if row["project"] in projects_list else len(projects_list)-1
                new_project = st.selectbox(
                    f"Project for {row['student']}", options=projects_list,
                    index=idx, key=f"override_{row['student']}", label_visibility="collapsed",
                )
            with c3:
                if new_project != "UNASSIGNED":
                    score_row = matrix[(matrix["student"] == row["student"]) & (matrix["project"] == new_project)]
                    score_val = score_row["match_score"].values[0] if len(score_row) else 0.0
                else:
                    score_val = 0.0
                st.metric("Match Score", f"{score_val:.2f}")
            edited_rows.append({"student": row["student"], "project": new_project, "match_score": score_val})

        edited_df = pd.DataFrame(edited_rows)
        st.divider()

        unassigned = edited_df[edited_df["project"] == "UNASSIGNED"]["student"].tolist()
        cap_counts = edited_df[edited_df["project"] != "UNASSIGNED"]["project"].value_counts().to_dict()
        capacities_dict = dict(zip(projects["title"], projects["capacity"]))
        available_projects = [p for p, cap in capacities_dict.items() if cap_counts.get(p, 0) < cap]

        if unassigned:
            col_res1, col_res2 = st.columns([2, 4])
            with col_res1:
                if st.button("Smart Resolve (Hungarian)", use_container_width=True,
                             help="Assigns unassigned students using the Hungarian optimal assignment algorithm."):
                    pivot_all = matrix.pivot(index="student", columns="project", values="match_score").fillna(0)
                    new_assignments = smart_resolve(unassigned, available_projects, pivot_all)
                    if new_assignments:
                        for i, row in edited_df.iterrows():
                            if row["student"] in new_assignments:
                                proj = new_assignments[row["student"]]
                                score_val = matrix[(matrix["student"] == row["student"]) & (matrix["project"] == proj)]["match_score"].values
                                edited_df.at[i, "project"] = proj
                                edited_df.at[i, "match_score"] = float(score_val[0]) if len(score_val) else 0.0
                        avg_new = np.mean([edited_df.loc[edited_df["student"] == s, "match_score"].values[0] for s in new_assignments])
                        st.success(f"Resolved {len(new_assignments)} student(s) — average score: {avg_new:.2f}")
                        assignments_updated = assignments.copy()
                        for i, row in assignments_updated.iterrows():
                            if row["student"] in new_assignments:
                                assignments_updated.at[i, "project"] = new_assignments[row["student"]]
                        st.session_state.assignments = assignments_updated
                        st.rerun()
                    else:
                        st.warning("No available project slots to resolve remaining students.")
            with col_res2:
                st.info(f"{len(unassigned)} student(s) unassigned. Click Smart Resolve to automatically place them.")

        st.subheader("Conflict Check")
        capacities = dict(zip(projects["title"], projects["capacity"]))
        load_counts = edited_df[edited_df["project"] != "UNASSIGNED"]["project"].value_counts().to_dict()
        conflicts = []
        for proj, cap in capacities.items():
            load = load_counts.get(proj, 0)
            if load > cap:
                conflicts.append(f"**{proj}** is overloaded: {load}/{cap} slots.")
        unassigned_count = (edited_df["project"] == "UNASSIGNED").sum()
        if unassigned_count > 0:
            conflicts.append(f"**{unassigned_count}** student(s) unassigned.")
        low_score = edited_df[(edited_df["project"] != "UNASSIGNED") & (edited_df["match_score"] < 0.3)]
        for _, r in low_score.iterrows():
            conflicts.append(f"**{r['student']}** has a low match score for **{r['project']}** — consider a manual review.")
        if conflicts:
            for c in conflicts:
                st.warning(c)
        else:
            st.success("No conflicts detected. All assignments are within capacity and reasonably matched.")

        st.divider()
        st.subheader("Final Match Table")
        st.dataframe(edited_df, use_container_width=True)
        csv_data = edited_df.to_csv(index=False)
        st.download_button("Export Final Matches (CSV)", data=csv_data,
                           file_name="matchmatrix_results.csv", mime="text/csv")
        st.session_state.final_assignments = edited_df

# ----------------------------
# STUDENT VIEW TAB
# Note: match scores are NEVER shown to students.
# Only qualitative explanations and project fit context.
# ----------------------------
with tab_student:
    if st.session_state.matrix is None:
        st.info("Matching has not been run yet. Please check back with your supervisor.")
    else:
        students = st.session_state.students
        projects = st.session_state.projects
        matrix = st.session_state.matrix
        final_assignments = st.session_state.get("final_assignments", st.session_state.assignments)

        selected_student = st.selectbox("Select student (simulating login)", students["name"].tolist())
        student_row = students[students["name"] == selected_student].iloc[0]
        assign_row = final_assignments[final_assignments["student"] == selected_student]

        st.markdown(f"### Welcome, {selected_student}")

        if assign_row.empty or assign_row.iloc[0]["project"] == "UNASSIGNED":
            st.warning("You have not been assigned to a project yet. Please speak with your supervisor.")
        else:
            project_title = assign_row.iloc[0]["project"]
            project_row = projects[projects["title"] == project_title].iloc[0]
            score_row = matrix[(matrix["student"] == selected_student) & (matrix["project"] == project_title)].iloc[0]

            # --- Supervisor Q&A Section (before explanation) ---
            proj_questions = st.session_state.supervisor_questions.get(project_title, [])
            if proj_questions:
                st.markdown('<div class="glass-accent">', unsafe_allow_html=True)
                st.markdown(f"**Your supervisor has a few questions for you about {project_title}:**")
                student_qa = st.session_state.student_answers.get(selected_student, {})
                proj_qa = student_qa.get(project_title, {})
                answers = {}
                for q in proj_questions:
                    ans = st.text_area(q, value=proj_qa.get(q, ""), key=f"qa_{selected_student}_{project_title}_{q}")
                    answers[q] = ans
                if st.button("Submit Answers", key=f"submit_qa_{selected_student}"):
                    if selected_student not in st.session_state.student_answers:
                        st.session_state.student_answers[selected_student] = {}
                    st.session_state.student_answers[selected_student][project_title] = answers
                    st.success("Your answers have been saved.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            # --- Match explanation (no scores shown) ---
            if use_llm_explain and has_api_key():
                cache_key = f"{selected_student}_{project_title}"
                if st.session_state.llm_explanations is None:
                    st.session_state.llm_explanations = {}
                if cache_key not in st.session_state.llm_explanations:
                    with st.spinner("Generating your personalised match summary..."):
                        student_answers_text = ""
                        all_answers = st.session_state.student_answers.get(selected_student, {}).get(project_title, {})
                        if all_answers:
                            student_answers_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in all_answers.items() if a])
                        free_text = student_row.get("free_text", "")
                        explanation = llm_explain_match(
                            selected_student, student_row["skills"], free_text,
                            project_title, project_row["required_skills"],
                            score_row["skill_score"], score_row["preference_score"],
                            score_row["availability_score"],
                            supervisor_qa=student_answers_text if student_answers_text else None
                        )
                        st.session_state.llm_explanations[cache_key] = explanation

                cached = st.session_state.llm_explanations.get(cache_key)
                if cached:
                    st.markdown(f'<div class="match-card"><strong>Your Match</strong> <span class="ai-badge">Claude</span><br><br>{project_title}<br><em style="color:rgba(255,255,255,0.5)">Supervisor: {project_row["supervisor"]}</em><br><br>{cached}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="match-card">{explain_match_rule_based(student_row, project_row, score_row)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="match-card">{explain_match_rule_based(student_row, project_row, score_row)}</div>', unsafe_allow_html=True)

            # --- Top project suggestions (no scores shown to students) ---
            st.markdown("#### Your top project matches")
            st.caption("Listed in order of fit — based on your skills and preferences.")
            student_scores = matrix[matrix["student"] == selected_student].sort_values("match_score", ascending=False).head(3)
            labels = ["Best match", "Strong match", "Good match"]
            for i, (_, r) in enumerate(student_scores.iterrows()):
                assigned_label = " — your current placement" if r["project"] == project_title else ""
                proj_sup = projects[projects["title"] == r["project"]]["supervisor"].values
                sup_text = f" ({proj_sup[0]})" if len(proj_sup) else ""
                st.markdown(f"**{labels[i]}:** {r['project']}{sup_text}{assigned_label}")

            # --- LLM preference extraction ---
            if use_llm_explain and has_api_key() and "free_text" in student_row and str(student_row["free_text"]).strip():
                with st.expander("What does your profile suggest?"):
                    free_text = str(student_row["free_text"])
                    st.markdown(f"*Your statement:* \"{free_text}\"")
                    with st.spinner("Analysing your interests..."):
                        ai_ranked = llm_extract_preferences(free_text, projects["title"].tolist())
                    st.markdown("**Based on your interests, these projects could suit you:**")
                    for i, proj in enumerate(ai_ranked[:4], 1):
                        st.markdown(f"{i}. {proj}")

st.divider()
st.caption("MatchMatrix — Built with Streamlit — Gale-Shapley + Hungarian optimisation + Claude AI")
