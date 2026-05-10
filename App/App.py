import streamlit as st
import base64
import random
import time
import io
import re
import plotly.express as px
import pandas as pd

from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter

from streamlit_tags import st_tags
from PIL import Image

from Courses import (
    ds_course,
    web_course,
    android_course,
    uiux_course
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM UI ---------------- #

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI';
}

.main {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #4CAF50;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    background-color: #4CAF50;
    color: white;
}

.stProgress > div > div > div > div {
    background-color: #4CAF50;
}

</style>
""", unsafe_allow_html=True)

# ---------------- PDF READER ---------------- #

def pdf_reader(file):

    resource_manager = PDFResourceManager()

    fake_file_handle = io.StringIO()

    converter = TextConverter(
        resource_manager,
        fake_file_handle,
        laparams=LAParams()
    )

    page_interpreter = PDFPageInterpreter(
        resource_manager,
        converter
    )

    with open(file, 'rb') as fh:

        for page in PDFPage.get_pages(
            fh,
            caching=True,
            check_extractable=True
        ):

            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()

    return text

# ---------------- SHOW PDF ---------------- #

def show_pdf(file_path):

    with open(file_path, "rb") as f:

        base64_pdf = base64.b64encode(
            f.read()
        ).decode('utf-8')

    pdf_display = f"""
    <iframe
    src="data:application/pdf;base64,{base64_pdf}"
    width="100%"
    height="700"
    type="application/pdf">
    </iframe>
    """

    st.markdown(
        pdf_display,
        unsafe_allow_html=True
    )

# ---------------- COURSE RECOMMENDER ---------------- #

def course_recommender(course_list):

    st.subheader("🎓 Recommended Courses")

    random.shuffle(course_list)

    for c_name, c_link in course_list[:5]:

        st.markdown(
            f"✅ [{c_name}]({c_link})"
        )

# ---------------- MAIN APP ---------------- #

def run():

    # ---------------- SIDEBAR ---------------- #

    st.sidebar.markdown(
        """
        <h1 style='text-align:center; color:#4CAF50;'>
        🚀 AI Resume Analyzer
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    choice = st.sidebar.radio(

        "📌 Navigation",

        [

            "🏠 Home",
            "📄 Resume Analyzer",
            "👨‍💻 About Developers"

        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
        AI-Powered ATS Resume Screening System

        MCA Major Project
        RKDF University Bhopal
        """
    )

    st.sidebar.markdown("---")

    st.sidebar.success(
        "Developed using Python + Streamlit + AI"
    )

    # ---------------- HOME ---------------- #

    if choice == "🏠 Home":

        st.title(
            "AI-Powered ATS Resume Screening & Career Recommendation System"
        )

        st.markdown("---")

        st.subheader("📌 Project Overview")

        st.write("""

        This project analyzes resumes using
        Artificial Intelligence and ATS-based
        screening techniques.

        Features:

        ✅ ATS Resume Matching  
        ✅ AI Skill Detection  
        ✅ Resume Score Prediction  
        ✅ Career Recommendation  
        ✅ Skill Gap Analysis  
        ✅ AI Resume Summary  
        ✅ Resume Analytics  

        """)

        st.markdown("---")

        st.subheader("🛠 Technologies Used")

        st.write("""

        • Python  
        • Streamlit  
        • NLP  
        • Plotly  
        • PDFMiner  
        • AI-based Analysis  

        """)

        st.markdown("---")

        st.success(
            "Use sidebar navigation to explore the project."
        )

    # ---------------- RESUME ANALYZER ---------------- #

    elif choice == "📄 Resume Analyzer":

        st.title("📄 Resume Analyzer")

        act_name = st.text_input("👤 Name")

        act_mail = st.text_input("📧 Email")

        target_role = st.selectbox(

            "💼 Which role are you applying for?",

            [

                "Data Scientist",
                "Web Developer",
                "Cybersecurity Analyst",
                "Android Developer",
                "Cloud Engineer",
                "IT Support Engineer",
                "NOC Engineer",
                "Software Developer",
                "AI Engineer"

            ]
        )

        act_mob = st.text_input("📱 Mobile Number")

        pdf_file = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf"]
        )

        if pdf_file is not None:

            with st.spinner("Analyzing Resume..."):
                time.sleep(2)

            save_path = (
                "./Uploaded_Resumes/" +
                pdf_file.name
            )

            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            show_pdf(save_path)

            resume_text = pdf_reader(save_path)

            # ---------------- EMAIL ---------------- #

            email_match = re.findall(
                r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
                resume_text
            )

            email = (
                email_match[0]
                if email_match
                else act_mail
            )

            # ---------------- PHONE ---------------- #

            phone_patterns = [

                r'\+91[\s\-]?[6-9]\d{9}',
                r'91[\s\-]?[6-9]\d{9}',
                r'[6-9]\d{9}'

            ]

            phone = act_mob

            for pattern in phone_patterns:

                matches = re.findall(
                    pattern,
                    resume_text
                )

                if matches:

                    phone = matches[0]
                    break

            # ---------------- SKILLS ---------------- #

            skills_list = [

                "Python",
                "Java",
                "C",
                "C++",
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Node JS",
                "SQL",
                "MySQL",
                "MongoDB",
                "Machine Learning",
                "Deep Learning",
                "TensorFlow",
                "PyTorch",
                "Cybersecurity",
                "Ethical Hacking",
                "Kali Linux",
                "Wireshark",
                "Nmap",
                "Networking",
                "Windows",
                "Linux",
                "Technical Support",
                "IT Support",
                "NOC",
                "AWS",
                "Docker",
                "Kubernetes",
                "Android",
                "Flutter",
                "Firebase",
                "Git",
                "GitHub",
                "Power BI",
                "Tableau"

            ]

            detected_skills = []

            for skill in skills_list:

                if skill.lower() in resume_text.lower():

                    detected_skills.append(skill)

            detected_skills = list(set(detected_skills))

            # ---------------- ROLE SKILLS ---------------- #

            role_skills = {

                "Data Scientist": [
                    "Python",
                    "Machine Learning",
                    "TensorFlow"
                ],

                "Web Developer": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "React"
                ],

                "Cybersecurity Analyst": [
                    "Cybersecurity",
                    "Kali Linux",
                    "Wireshark"
                ],

                "Android Developer": [
                    "Android",
                    "Flutter",
                    "Firebase"
                ],

                "Cloud Engineer": [
                    "AWS",
                    "Docker",
                    "Kubernetes"
                ],

                "IT Support Engineer": [
                    "Windows",
                    "Networking",
                    "Technical Support"
                ],

                "NOC Engineer": [
                    "Networking",
                    "DNS",
                    "TCP/IP"
                ],

                "Software Developer": [
                    "Python",
                    "Java",
                    "SQL"
                ],

                "AI Engineer": [
                    "Python",
                    "Machine Learning",
                    "Deep Learning"
                ]
            }

            required_skills = role_skills[target_role]

            matched_skills = []
            missing_skills = []

            for skill in required_skills:

                if skill in detected_skills:

                    matched_skills.append(skill)

                else:

                    missing_skills.append(skill)

            role_match = int(

                (
                    len(matched_skills)
                    /
                    len(required_skills)
                ) * 100

            )

            # ---------------- SCORES ---------------- #

            resume_score = 40

            resume_score += len(detected_skills) * 3

            if "project" in resume_text.lower():
                resume_score += 15

            if "internship" in resume_text.lower():
                resume_score += 10

            if "github" in resume_text.lower():
                resume_score += 5

            if "linkedin" in resume_text.lower():
                resume_score += 5

            if resume_score > 100:
                resume_score = 100

            ats_score = role_match

            # ---------------- DISPLAY ---------------- #

            st.success("✅ Resume Successfully Analyzed")

            st.markdown("---")

            st.header("📋 Resume Information")

            col1, col2 = st.columns(2)

            with col1:

                st.info(f"👤 Name: {act_name}")

                st.info(f"📧 Email: {email}")

            with col2:

                st.info(f"📱 Mobile: {phone}")

                st.info(f"💼 Role: {target_role}")

            st.markdown("---")

            st.header("🛠 Detected Skills")

            st_tags(
                label='### Skills',
                text='Detected skills',
                value=detected_skills,
                key='skills'
            )

            st.markdown("---")

            st.header("🎯 ATS Compatibility")

            st.progress(ats_score)

            st.success(
                f"ATS Score: {ats_score}%"
            )

            st.markdown("---")

            st.header("📈 Resume Score")

            st.progress(resume_score)

            st.success(
                f"Resume Score: {resume_score}/100"
            )

            st.markdown("---")

            st.header("💼 Role Match Analysis")

            st.subheader("✅ Matched Skills")

            for skill in matched_skills:

                st.success(skill)

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.error(skill)

            else:

                st.success(
                    "No major missing skills detected."
                )

            st.markdown("---")

            st.header("🤖 AI Resume Summary")

            ai_summary = f"""

            Candidate is suitable for
            {target_role} roles.

            Strong skills detected:
            {', '.join(matched_skills)}

            Missing skills:
            {', '.join(missing_skills) if missing_skills else 'None'}

            """

            st.info(ai_summary)

            st.markdown("---")

            st.header("📊 Skill Analytics")

            graph_df = pd.DataFrame({

                "Category": [

                    "Detected Skills",
                    "Matched Skills",
                    "Missing Skills"

                ],

                "Count": [

                    len(detected_skills),
                    len(matched_skills),
                    len(missing_skills)

                ]
            })

            fig = px.pie(
                graph_df,
                names='Category',
                values='Count',
                title='Resume Skill Analysis'
            )

            st.plotly_chart(fig)

            st.markdown("---")

            # ---------------- COURSES ---------------- #

            if target_role == "Data Scientist":

                course_recommender(ds_course)

            elif target_role == "Web Developer":

                course_recommender(web_course)

            elif target_role == "Android Developer":

                course_recommender(android_course)

            elif target_role == "AI Engineer":

                course_recommender(ds_course)

            st.markdown("---")

            st.header("📌 Improvement Suggestions")

            if missing_skills:

                for skill in missing_skills:

                    st.warning(
                        f"Learn {skill}"
                    )

            else:

                st.success(
                    "Resume looks highly optimized."
                )

            st.balloons()

    # ---------------- ABOUT ---------------- #

    elif choice == "👨‍💻 About Developers":

        st.title("👨‍💻 About Developers")

        col1, col2 = st.columns(2)

        with col1:

            image1 = Image.open("photo1.jpg")

            st.image(image1, width=220)

            st.subheader("Gagan Bisen")

            st.write("""

            MCA Final Year Student

            RKDF University Bhopal

            Interests:
            • Cybersecurity
            • AI Projects
            • IT Support

            """)

        with col2:

            image2 = Image.open("photo2.jpg")

            st.image(image2, width=220)

            st.subheader("Huzaifa Khan")

            st.write("""

            MCA Final Year Student

            RKDF University Bhopal

            Interests:
            • AI
            • Web Development
            • UI/UX

            """)

        st.markdown("---")

        st.header("🚀 Project Features")

        st.markdown("""

        ✅ ATS Resume Matching  
        ✅ AI Skill Detection  
        ✅ Resume Validation  
        ✅ Resume Score Prediction  
        ✅ Career Recommendation  
        ✅ Skill Gap Analysis  
        ✅ AI Resume Summary  
        ✅ Skill Analytics Graph  

        """)

        st.success(
            "Developed using Python, Streamlit and AI concepts."
        )

# ---------------- RUN APP ---------------- #

run()