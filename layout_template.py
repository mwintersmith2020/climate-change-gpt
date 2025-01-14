# layout_template.py
import functions
import streamlit as st
from PIL import Image

BOOK_IMAGE = Image.open("img/ca-voter-guide.png")

def sidebar_template():
    # Sidebar
    # st.sidebar.title("Navigation")
    # st.sidebar.write("This is a shared sidebar for all pages.")
    st.sidebar.image(BOOK_IMAGE)
    st.sidebar.markdown("---")

    #st.sidebar.page_link("pages/user-agent.py", label="<User Agent>")
    #st.sidebar.markdown("---")
    st.sidebar.page_link("app.py", label="Voter Summary")
    st.sidebar.page_link("pages/trust-o-meter.py", label="Trust-O-Meter")
    st.sidebar.page_link("pages/winners-and-losers.py", label="Winners & Losers")
    st.sidebar.page_link("pages/show-me-the-money.py", label="Show Me The Money!")
    
    st.sidebar.page_link("pages/trojan-horses.py", label="Trojan Horses")
    st.sidebar.page_link("pages/election-gpt.py", label="Election-GPT")

    st.sidebar.markdown("---")

    if st.sidebar.button("About me..."):
        show_about_me_dialog()

    if not functions.USER_NAME:
        user_intro_form()

@st.dialog("Tell us about yourself")
def user_intro_form():
    # Create a form for name (required) and email (optional)
    with st.form("user_info_form", clear_on_submit=False):
        st.write("Please tell us about yourself:")
        
        # Required field for name
        name = st.text_input("Name", placeholder="What is your name", max_chars=50)
        
        # Optional field for email
        email = st.text_input("Email (optional, if you want project updates...)", placeholder="Enter your email", max_chars=100)

        # Submit button to process the form
        submit = st.form_submit_button("Submit")

        # Validate that name is required
        if submit:
            if not name:
                st.error("Name is required!")
            else:
                st.success(f"Thank you, {name}!")
                functions.USER_NAME = name
                if email:
                    st.info(f"We'll contact you at {email}")

@st.dialog("About this app's author...", width="large")
def show_about_me_dialog():
    text_content = """
Freelance AI/ML researcher & strategist with a specialization in LLMs and possessing the following **hard** skills:

* **Machine Learning & Deep Learning Expertise:**
*Solid understanding ML algorithms (supervised, unsupervised, reinforcement learning), deep learning frameworks (TensorFlow, PyTorch), and model evaluation techniques.*

* **Natural Language Processing (NLP):** 
*Knowledge of NLP techniques (transformers, embeddings, BERT, GPT models), text preprocessing, and understanding of large language models (LLMs).*

* **Data Engineering:**
*Skilled in data wrangling, data pipelines, ETL processes, and working with structured and unstructured data (SQL, NoSQL databases, data lakes).*

* **Cloud Computing:**
***Google Certified Professional Cloud Architect*** with expertise in cloud platforms GCP, AWS and Digital Ocean for deploying AI/ML solutions, managing compute resources, and containerization (Kubernetes, Docker).*

* **Model Deployment and Scalability:** 
*Knowledge of MLOps for deploying models into production environments using APIs, handling scaling issues and monitoring model performance.*

* **Software Engineering:** 
*Considerable proficiency with programming languages (Python, Java, Go, Javascript), version control (Git) and the software development lifecycle best-practices (Agile, CI/CD).*

* **High-Performance Computing (HPC):** Understanding of GPU/TPU acceleration, distributed training, parallel processing and the tradeoffs needed to speed up model training.

* **Experimentation and Prototyping:** Proven ability to design and run experiments to test hypotheses quickly, using tools like Jupyter notebooks and rapid prototyping frameworks such as Flask, Gradio and others.

* **AI Ethics and Compliance:** Decades of experience in regulated industries, with knowledge of ethical AI practices, regulatory requirements and an understanding of how to build responsible AI systems (bias mitigation, fairness and transparency).

* **Statistical Analysis & Data Science:** Strong grounding in probability, statistics, and the mathematical foundations of AI, including hypothesis testing, statistical modeling, and experiment design.    
----
    """
    st.subheader("Mark Wintersmith", divider="gray")

    st.markdown(text_content)
    st.markdown("*A.I.* is **really** ***cool***.  Follow me on [LinkedIn](https://www.linkedin.com/in/markwintersmith/) ")

# <audio controls>
#   <source src="your-audio-file.m4a" type="audio/mp4">
# </audio>
