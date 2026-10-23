
import streamlit as st
import httpx
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NEXUS | AI Routing Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080b14;
    --panel: #101522;
    --border: #252d40;
    --muted: #8c97ad;
    --cyan: #61f3e3;
    --purple: #a78bfa;
}
.stApp {
    background: radial-gradient(ellipse at 80% 0%, #18213b 0%, #080b14 48%);
    color: #edf2ff;
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 {font-family: 'Space Grotesk', sans-serif !important;}
.block-container {padding-top: 2rem; max-width: 1440px;}
[data-testid="stSidebar"] {
    background: #0c101c;
    border-right: 1px solid #252d40;
}
[data-testid="stSidebar"] * {color: #e7ebf8;}
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #141b2b, #0e1320);
    border: 1px solid #29334a;
    border-radius: 16px;
    padding: 20px;
}
div[data-testid="stMetricLabel"] {color: #9ba8c0;}
div[data-testid="stMetricValue"] {color: #61f3e3;}
.stTextArea textarea {
    background: #0c1120 !important;
    color: #f4f7ff !important;
    border: 1px solid #35405b !important;
    border-radius: 14px !important;
}
.stButton button {
    background: linear-gradient(100deg, #7664f6, #4a9df8);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
}
.stButton button:hover {
    border: 1px solid #61f3e3;
    color: white;
}
.nexus-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 27px;
    font-weight: 700;
    letter-spacing: 2px;
}
.nexus-brand span {color: #61f3e3;}
.eyebrow {
    color: #61f3e3;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
}
.hero {
    background: linear-gradient(120deg, #171d34, #101625 60%, #14272e);
    border: 1px solid #303b55;
    border-radius: 22px;
    padding: 30px;
    margin: 10px 0 24px 0;
}
.hero h1 {font-size: 36px; margin: 8px 0;}
.hero p {color: #aab5cb; margin-bottom: 0;}
.panel {
    background: #101522;
    border: 1px solid #252d40;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
}
.small-muted {color: #9ba8c0; font-size: 13px;}
.pill {
    display: inline-block;
    color: #61f3e3;
    background: #12302f;
    padding: 5px 10px;
    border-radius: 30px;
    font-size: 12px;
}
hr {border-color: #252d40;}
</style>
""", unsafe_allow_html=True)


def fetch_analytics():
    try:
        r = httpx.get(f"{API_URL}/analytics", timeout=10)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError:
        return None


def generate(prompt):
    r = httpx.post(
        f"{API_URL}/chat",
        json={"prompt": prompt},
        timeout=240,
    )
    r.raise_for_status()
    return r.json()


with st.sidebar:
    st.markdown(
        '<div class="nexus-brand">NEX<span>U</span>S<span> ◈</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("AI ROUTING INTELLIGENCE")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Overview", "AI Playground", "Analytics", "About"],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    try:
        httpx.get(f"{API_URL}/", timeout=2).raise_for_status()
        st.markdown(
            '<span class="pill">● API ONLINE</span>',
            unsafe_allow_html=True,
        )
    except httpx.HTTPError:
        st.error("API offline — start the backend")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("LOCAL INFERENCE · OLLAMA")
    st.caption("NEXUS v1.0")

if page == "Overview":
    stats = fetch_analytics()

    st.markdown(
        '<div class="eyebrow">CONTROL CENTER / OVERVIEW</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">INTELLIGENT MODEL ORCHESTRATION</div>
      <h1>Make every AI request count.</h1>
      <p>Route requests, inspect decisions and understand inference costs
      from one workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    if stats is not None:
        a, b, c = st.columns(3)
        a.metric("TOTAL REQUESTS", stats["total_requests"])
        b.metric(
            "AVG. LATENCY",
            f'{stats["average_latency_seconds"]:.2f} s',
        )
        c.metric(
            "EST. API COST",
            f'${stats["total_estimated_api_cost_usd"]:.6f}',
        )
    else:
        st.warning("Cannot connect to the API. Start the FastAPI server.")

    st.markdown("### Your workspace")
    a, b = st.columns(2)
    with a:
        st.markdown("""
        <div class="panel">
          <div class="eyebrow">01 / PLAYGROUND</div>
          <h3>Prompt → Intelligence</h3>
          <p class="small-muted">Send a prompt and inspect the model's
          response, routing decision and performance.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Playground →", use_container_width=True):
            st.session_state["page_request"] = "AI Playground"
            st.rerun()
    with b:
        st.markdown("""
        <div class="panel">
          <div class="eyebrow">02 / OBSERVABILITY</div>
          <h3>Measure every request</h3>
          <p class="small-muted">Review aggregate latency, request volume
          and estimated API expenditure.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Analytics →", use_container_width=True):
            st.session_state["page_request"] = "Analytics"
            st.rerun()

elif page == "AI Playground":
    st.markdown(
        '<div class="eyebrow">WORKSPACE / PLAYGROUND</div>',
        unsafe_allow_html=True,
    )
    st.title("AI Playground")
    st.write("Describe your task. Your current router will choose a model.")

    examples = {
        "Custom prompt": "",
        "Java basics": "Explain Java arrays with one simple example.",
        "Code help": "Write a Java method to reverse a string.",
        "System design": "Design a scalable URL shortener and explain its trade-offs.",
    }

    choice = st.selectbox("QUICK START", list(examples.keys()))
    initial_prompt = examples[choice]

    with st.form("prompt_form"):
        prompt = st.text_area(
            "YOUR PROMPT",
            value=initial_prompt,
            placeholder="What would you like the AI to do?",
            height=170,
        )
        submitted = st.form_submit_button(
            "◈  Run AI",
            use_container_width=True,
        )

    if submitted:
        if not prompt.strip():
            st.warning("Enter a prompt first.")
        else:
            try:
                with st.spinner("Routing request and generating response..."):
                    data = generate(prompt)

                st.success("Request completed")
                st.markdown("### Generated response")
                st.markdown(data["response"])

                st.markdown("### Routing decision")
                x, y, z = st.columns(3)
                x.metric("TASK COMPLEXITY", data["complexity"].upper())
                y.metric("SELECTED MODEL", data["model"])
                z.metric("LATENCY", f'{data["latency_seconds"]:.2f} s')

                st.markdown(
                    f'<div class="panel"><div class="eyebrow">'
                    f'WHY THIS MODEL?</div><p>{data["reason"]}</p>'
                    f'<span class="pill">{data["provider"]}</span></div>',
                    unsafe_allow_html=True,
                )

                x, y, z = st.columns(3)
                x.metric("INPUT TOKEN ESTIMATE", data["input_tokens_estimated"])
                y.metric("OUTPUT TOKEN ESTIMATE", data["output_tokens_estimated"])
                z.metric("ESTIMATED API COST", f'${data["estimated_api_cost_usd"]:.6f}')

            except httpx.HTTPError as error:
                st.error(f"Request failed: {error}")

elif page == "Analytics":
    st.markdown(
        '<div class="eyebrow">OBSERVABILITY / METRICS</div>',
        unsafe_allow_html=True,
    )
    st.title("Request analytics")
    st.write("Aggregate measurements from your saved request logs.")

    if st.button("↻ Refresh metrics"):
        st.rerun()

    stats = fetch_analytics()
    if stats is None:
        st.error("Could not reach the backend API.")
    else:
        a, b, c = st.columns(3)
        a.metric("TOTAL REQUESTS", stats["total_requests"])
        b.metric("AVERAGE LATENCY", f'{stats["average_latency_seconds"]:.2f} s')
        c.metric("TOTAL ESTIMATED API COST", f'${stats["total_estimated_api_cost_usd"]:.6f}')

        st.markdown("### How to read these metrics")
        st.markdown("""
        - **Total requests:** requests recorded in the metrics log.
        - **Average latency:** mean recorded response time.
        - **Estimated API cost:** calculated provider API charges; local
          inference reports zero API charge, not zero electricity cost.
        """)
        st.info("Token counts are currently rough estimates, not tokenizer measurements.")

elif page == "About":
    st.markdown(
        '<div class="eyebrow">SYSTEM / ABOUT</div>',
        unsafe_allow_html=True,
    )
    st.title("Inside NEXUS")
    st.write("An experimental AI model routing and cost-observability project.")

    st.markdown("""
    <div class="panel">
      <h3>Current architecture</h3>
      <p>Streamlit interface → FastAPI backend → task classifier →
      Ollama local model → metrics logger.</p>
    </div>
    <div class="panel">
      <h3>Current capabilities</h3>
      <p>Rule-based complexity classification, local model inference,
      response latency tracking and estimated usage-cost reporting.</p>
    </div>
    <div class="panel">
      <h3>Next engineering milestone</h3>
      <p>Benchmark multiple distinct models, implement real model selection,
      and compare quality, latency and cost across requests.</p>
    </div>
    """, unsafe_allow_html=True)
