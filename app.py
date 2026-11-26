import html

import streamlit as st

from src.similarity import calculate_similarity
from src.pdf_extractor import extract_text_from_pdf
from src.skill_extractor import extract_skills, compare_skills


st.set_page_config(
    page_title="ResumeMatch — the reality check",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #101110;
    --surface: #1b1d1b;
    --border: #343834;
    --text: #f0f0e9;
    --muted: #a5aaa2;
    --accent: #c6f36b;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.site-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 48px;
}

.brand {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.05em;
}

.brand span {
    color: var(--accent);
}

.nav-note {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
}

.eyebrow {
    font-family: 'DM Mono', monospace;
    color: var(--accent);
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}

.hero-title {
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 700;
    letter-spacing: -0.07em;
    line-height: 1.05;
    margin-bottom: 16px;
}

.hero-title span {
    color: var(--accent);
}

.hero-description {
    color: var(--muted);
    font-size: 1rem;
    margin-bottom: 42px;
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 28px;
    margin-bottom: 14px;
}

.section-heading {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin: 22px 0;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 22px;
    min-height: 140px;
}

.metric-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
}

.metric-number {
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.06em;
    margin-top: 14px;
}

.accent {
    color: var(--accent);
}

.skill-pill {
    display: inline-block;
    padding: 9px 13px;
    margin: 4px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
}

.found {
    color: var(--accent);
    border-color: #617b3d;
}

.missing {
    color: #f1b7a6;
    border-color: #76514a;
}

.cat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 24px;
    margin-top: 20px;
    text-align: center;
}

.cat-face {
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem;
    color: var(--accent);
    white-space: pre;
    line-height: 1.3;
}

.cat-caption {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    margin-top: 12px;
}

.footer-note {
    border-top: 1px solid var(--border);
    padding-top: 22px;
    margin-top: 60px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
}

.footer-note {
    border-top: 1px solid var(--border);
    padding-top: 22px;
    margin-top: 60px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    text-align: center;
    line-height: 1.8;
}

div[data-testid="stProgress"] > div > div {
    background-color: var(--accent);
}

div.stDownloadButton > button {
    background: var(--accent);
    color: #101110;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}

div.stDownloadButton > button:hover {
    background: #d7ff8c;
    color: #101110;
}

</style>
""", unsafe_allow_html=True)


def metric_card(label, value, highlight=False):
    color = "accent" if highlight else ""

    return f"""
    <div class="metric-card">
        <div class="metric-name">{html.escape(label)}</div>
        <div class="metric-number {color}">
            {html.escape(str(value))}
        </div>
    </div>
    """


def skill_badges(skills, kind):
    return "".join(
        f'<span class="skill-pill {kind}">'
        f'{html.escape(skill)}</span>'
        for skill in skills
    )


def cat_reaction(coverage):
    face = " /\\_/\\\\\n( o.o )\n > ^ <"

    if coverage >= 80:
        return face, "okay. you cooked."

    if coverage >= 50:
        return face, "not bad. the cat sees potential."

    return face, "the job description is doing too much."



st.markdown("""
<div class="site-nav">
    <div class="brand">resume<span>match</span>.</div>
    <div class="nav-note">the unofficial resume reality check</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="eyebrow">YOUR RESUME VS. THEIR WISHLIST</div>

<div class="hero-title">
    let's see if<br>
    <span>it's a match.</span>
</div>

<div class="hero-description">
    Drop your resume. Paste the job description.
    We'll handle the awkward comparison.
</div>
""", unsafe_allow_html=True)



left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### your resume")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    with st.expander("🔒 your resume is yours"):
        st.markdown(
            """
            no, the person who built this website isn't
            sitting somewhere reading your resume. 💀

            your file is used to generate your analysis,
            and doesn't intentionally save uploaded
            resumes or send them to the developer.

            the hosting platform may still process uploaded data.
            """
        )

with right:
    st.markdown("#### their wishlist")

    job_description = st.text_area(
        "Paste the job description",
        height=180,
        placeholder="knows everything. apparently capable of running the entire company alone."
    )


if uploaded_file is not None and job_description.strip():

    try:
        resume_text = extract_text_from_pdf(
            uploaded_file.getvalue()
        )

        if not resume_text or not resume_text.strip():
            st.warning(
                "No selectable text found. Try a text-based PDF."
            )
            st.stop()

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matching, missing, coverage = compare_skills(
            resume_skills,
            job_skills
        )

        with st.spinner("the cat is reviewing your application..."):
            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )

        st.divider()


        st.markdown(
            '<div class="section-label"> the results</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-heading">the numbers.</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                metric_card("resume skills", len(resume_skills)),
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                metric_card("matching skills", len(matching)),
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                metric_card("skill coverage", f"{coverage:.1f}%", True),
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                metric_card("AI similarity", f"{similarity_score:.3f}"),
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="section-label">SEMANTIC SIMILARITY</div>',
            unsafe_allow_html=True
        )

        st.progress(
            max(0.0, min(1.0, similarity_score))
        )

        with st.expander("what do these numbers mean?"):
            st.write(
                "**Skill coverage:** Percentage of detected job skills "
                "also found in your resume."
            )

            st.write(
                "**AI similarity:** Cosine similarity between your resume "
                "and the job description. It is not a hiring probability."
            )

        if not job_skills:
            st.info(
                "No skills from the current skill dictionary were "
                "detected in the job description."
            )


        st.markdown(
            '<div class="section-label"> the receipts</div>',
            unsafe_allow_html=True
        )

        skills_left, skills_right = st.columns(2, gap="large")

        with skills_left:
            st.markdown("### you've got these.")

            if matching:
                st.markdown(
                    skill_badges(matching, "found"),
                    unsafe_allow_html=True
                )
            else:
                st.info("No matching skills detected.")

        with skills_right:
            st.markdown("### they're asking for these.")

            if missing:
                st.markdown(
                    skill_badges(missing, "missing"),
                    unsafe_allow_html=True
                )
            else:
                st.success("No missing skills detected.")

        face, caption = cat_reaction(coverage)

        st.markdown(
            f"""
            <div class="cat-box">
                <div class="cat-face">{html.escape(face)}</div>
                <div class="cat-caption">{html.escape(caption)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        matching_text = (
            "\n".join(f"- {skill}" for skill in matching)
            if matching
            else "No matching skills detected."
        )

        missing_text = (
            "\n".join(f"- {skill}" for skill in missing)
            if missing
            else "No missing skills detected."
        )

        report = f"""RESUMEMATCH — ANALYSIS REPORT
================================

RESUME SKILLS: {len(resume_skills)}
MATCHING SKILLS: {len(matching)}
SKILL COVERAGE: {coverage:.1f}%
AI SIMILARITY: {similarity_score:.3f}

MATCHING SKILLS
---------------
{matching_text}

SKILLS NOT FOUND IN RESUME
--------------------------
{missing_text}

NOTES
-----
Skill coverage measures detected job skills
also found in the resume.

AI similarity measures text similarity.
It does not predict hiring outcomes.

Automated analysis may contain errors.

Generated by ResumeMatch AI.
"""

        st.markdown(
            '<div class="section-label">05 / keep the receipts</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            "↓ download your analysis",
            data=report,
            file_name="resumematch_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )

        with st.expander("view all detected skills"):
            a, b = st.columns(2)

            with a:
                st.markdown("**Resume skills**")
                st.write(", ".join(resume_skills) or "None detected")

            with b:
                st.markdown("**Job description skills**")
                st.write(", ".join(job_skills) or "None detected")

        with st.expander("view extracted resume text"):
            st.text_area(
                "Extracted text",
                resume_text,
                height=300
            )

    except Exception as error:
        st.error("Something broke. The cat is investigating.")
        st.exception(error)

else:
    st.caption(
        "Upload your resume and paste a job description to get started."
    )

st.markdown("""
<div class="footer-note">
    built with python, caffeine & questionable confidence.<br>
    the cat has seen worse resumes. probably.
</div>
""", unsafe_allow_html=True)