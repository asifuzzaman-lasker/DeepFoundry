import streamlit as st


def inject_theme():
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )
    css = r"""
    :root {
    --bg: #FFF8F3;
    --panel: #FFFFFF;
    --panel-accent: #F3E7D7;
    --text: #1F2A44;
    --muted: #5C6475;
    --primary: #2F6BAE;
    --primary-hover: #255C99;
    --header-orange: #F4B278;
    --header-blue: #3C86B8;
    --radius-lg: 18px;
    --radius-md: 12px;
    --shadow-soft: 0 2px 6px rgba(0,0,0,0.05);
    --shadow-strong: 0 8px 24px rgba(0,0,0,0.08);
    }

    /* Remove Streamlit header */
    [data-testid="stHeader"] {
        display: none;
    }

    /* Remove footer */
    [data-testid="stFooter"] {
        display: none;
    }

    /* Remove top padding */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 1rem;
    }

    /* App background */
    .stApp {
        background-color: #0E1117;  /* or #ffffff if light */
    }

    html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    .block-container { max-width: 1200px; padding-top: 4rem; padding-bottom: 3rem; }

    /* Headings */
    h1, h2, h3 { color: var(--text); font-weight: 700; letter-spacing: .2px; }

    /* Cards */
    .main-container {
    //background: var(--panel);
    //border-radius: var(--radius-lg);
    //box-shadow: var(--shadow-soft);
    //padding: 2rem 2.5rem;
    //margin-bottom: 2rem;
    //transition: box-shadow .2s ease, transform .2s ease;
    }
    .main-container:hover { box-shadow: var(--shadow-strong); transform: translateY(-2px); }

    .main-container :is(label, legend, h3, h4, p, span, small) {
    color: var(--text) !important;
    }

    /* Streamlit widget labels */
    label[data-testid="stWidgetLabel"],
    div[role="radiogroup"] label,
    div[role="group"] label,
    .stCheckbox > label,
    .stSlider label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextInput label {
    color: var(--text) !important;
    opacity: 1 !important;
    }

    /* BaseWeb controls (used by Streamlit) */
    [data-baseweb="slider"], 
    [data-baseweb="checkbox"], 
    [data-baseweb="input"],
    [data-baseweb="textarea"] {
    color: var(--text) !important;
    }

    /* Help/captions under widgets */
    .stCaption, .stMarkdown small {
    color: var(--muted) !important;
    }

    /* Keep disabled state *subtle* but readable */
    [aria-disabled="true"], [data-disabled="true"] {
    opacity: .85 !important;  /* was too faint; raise contrast */
    }
    .stSlider [aria-disabled="true"] [role="slider"] {
    box-shadow: none;
    border-color: #e5e7eb;
    }

    /* Slider track (you had these already; keeping for completeness) */
    .stSlider [data-baseweb="slider"] > div > div { background:#e6edf6; }
    .stSlider [data-baseweb="slider"] > div > div > div { background: var(--primary) !important; }

    .nested-container {
    //background: var(--panel-accent);
    //border-radius: var(--radius-md);
    //padding: 1.2rem 1.5rem;
    //margin-bottom: 1rem;
    //box-shadow: var(--shadow-soft);
    //height:100% !important;

    }

    /* Scope to the augmentation card only */
    .section-header:contains("Data Augmentation") + div[data-testid="stVerticalBlock"] 
    :is(label, legend, p, span, small) { color: var(--text) !important; }
    
    #select-dataset-folder{
    font-size:20px !important;
    font-weight:600 !important;
    }

    #train-test-split{
    font-size:20px !important;
    font-weight:600 !important;
    }
    #dataset-preview{
    font-size:20px !important;
    font-weight:600 !important;
    }

    #sample-classes{
    font-size:20px !important;
    font-weight:600 !important;
    }



    h3.className { font-size: 18px !important; }

    .selectedContainer {
        background: var(--panel-accent);
        background: var(--panel-accent);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-soft);


    }
    .stMetric {
        background: var(--panel-accent);;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-soft);
    padding: .6rem 1rem;
    }

    .classDistribution{
    //background: var(--panel-accent);
    //border-radius: var(--radius-md);
    //padding: 1rem 1.25rem;
    font-weight:600;
    //box-shadow: var(--shadow-soft);
    //text-align: center; /* for the heading */
    padding-bottom: 1.5rem;
    }
    .stMarkdown ul {
    list-style-type: none;
    margin: 5px;
    padding: 0;
    display: flex;
    }

    .stMarkdown ul li {
    margin: 0 10px;
    border-radius: var(--radius-md);
    border: 1px solid rgba(0,0,0,.1);
        padding: .4rem .8rem;
    }

    .stMarkdownContainer ul{
    width:25% !important;
    margin:0 auto !important;
    }

    .stMarkdownContainer ul li{
    width:25% !important;
    float:left;
    }

    /* Section headers (use these instead of plain <h2>) */
    .section-header {
    background: var(--header-orange);
    color: var(--text);
    font-weight: 700;
    font-size: 1.55rem;
    padding: .9rem 1.2rem;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 2px 4px rgba(0,0,0,.04);
    }
    .section-header.blue { background: var(--header-blue); color: #fff; }

    /* Info boxes */
    .info-container {
    //background: #E9F2FB;
    //border-left: 5px solid var(--primary);
    //border-radius: var(--radius-md);
    //padding: 1.3rem 1.5rem;
    //margin-bottom: 1.2rem;
    //box-shadow: var(--shadow-soft);
    }

    /* Buttons */
    .stButton > button{
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: var(--radius-md);
    padding: .6rem 1.1rem;
    font-weight: 600;
    box-shadow: 0 3px 6px rgba(47,107,174,.25);
    transition: background .18s ease, transform .15s ease;
    }
    .stButton > button:hover{ background: var(--primary-hover); transform: translateY(-1px); box-shadow: 0 6px 12px rgba(47,107,174,.3); }
    .stButton > button:active{ transform: translateY(0); }

    /* Inputs */
    .stTextInput > div > div > input{
    background:#fff; color:var(--text);
    border:1px solid rgba(0,0,0,.15)!important; border-radius: var(--radius-md)!important;
    padding:.6rem .8rem!important; box-shadow: inset 0 1px 1px rgba(0,0,0,.04);
    }
    .stTextInput > div > div > input:focus{
    border-color: var(--primary)!important;
    box-shadow: 0 0 0 3px rgba(47,107,174,.25)!important;
    }

    /* Metrics */
    [data-testid="stMetricValue"]{ color: var(--primary); font-weight: 700; }

    /* Progress/Sliders */
    .stProgress > div > div{ background:#E0E7F0; border-radius:999px; }
    .stProgress > div > div > div{ background:var(--primary)!important; }
    .stSlider [role="slider"]{ width:18px; height:18px; border:2px solid #fff; box-shadow:0 2px 6px rgba(0,0,0,.18); }
    .stSlider [data-baseweb="slider"]>div>div{ background:#e6edf6; }
    .stSlider [data-baseweb="slider"]>div>div>div{ background:var(--primary)!important; }

    /* Sample grid */
    .sample-grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:1rem; padding-top:1rem; }
    .sample-grid img{ width:100%; height:180px; object-fit:cover; border-radius:var(--radius-md); box-shadow:var(--shadow-soft); transition:transform .2s, box-shadow .2s; }
    .sample-grid img:hover{ transform:scale(1.02); box-shadow:var(--shadow-strong); }

    /* Sticky right column */
    .sticky{ position: sticky; top: 1rem; }

    /* Small helpers */
    .form-row{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
    .card-subtle{ background:#f8fafc; border:1px dashed rgba(31,42,68,.15); border-radius:12px; padding:.8rem 1rem; color:var(--muted); }

    /* Footer */
    footer, .reportview-container footer { display:none; }

    /* Disabled controls look intentional, not washed-out */
    [data-disabled="true"], .stSlider [aria-disabled="true"] {
    opacity: .55;
    cursor: not-allowed;
    }
    .stSlider [aria-disabled="true"] [role="slider"] {
    box-shadow: none;
    border-color: #f3f4f6;
    }
    .stCheckbox > label p { font-weight: 600; }
    /* Small spacing under checkbox titles */
    .stCheckbox { margin-bottom: .35rem; }

    /* Inline value chips above sliders */
    .value-chip {
    display:inline-block; font-weight:700; font-size:.9rem;
    padding:.15rem .45rem; border-radius:999px;
    background:#eaf2ff; color:#2F6BAE; border:1px solid rgba(47,107,174,.25);
    margin-bottom:.25rem;
    }
    .bknone{
    background:none !important;

    }
    .stElementContainer{
    border:none !important;
    background:none !important;
    }


    /*Asif ---- Classes line (count + pill chips) ---- */
    .classes-box{
    background: var(--panel-accent);
    border-radius: var(--radius-md);
    padding: 0.9rem 1rem;
    margin: 0.5rem 0 1rem;
    box-shadow: var(--shadow-soft);
    }

    .classes-header{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 0.6rem 0;
    font-weight: 700;
    color: var(--text);
    }

    .classes-badge{
    display: inline-block;
    min-width: 1.8rem;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: #fff;
    box-shadow: var(--shadow-soft);
    color: var(--primary);
    font-weight: 800;
    text-align: center;
    }

    .classes-list{
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 0.6rem;
    padding: 0;
    margin: 0;
    }

    .classes-item{
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: #fff;
    box-shadow: var(--shadow-soft);
    color: var(--text);
    font-weight: 600;
    line-height: 1.2;
    }
    /*Asif end ---- Classes line (count + pill chips) ---- */

    .classDistribution { padding: 1rem 1.25rem; border-radius: var(--radius-md); }
    .classDistribution ul.cd-list{
    list-style: none; margin: 0; padding: .4rem 0;
    display: flex; flex-wrap: wrap; gap: .5rem .75rem; justify-content: center;
    }
    .classDistribution ul.cd-list li{
    background: #fff; border-radius: 999px; padding: .25rem .6rem;
    box-shadow: var(--shadow-soft); font-weight: 600;
    }

    .count-blue{
    color: var(--primary);   /* your theme blue */
    font-weight: 700;
    }


    /* --- Blue section header variant --- */
    .section-header.blue{
    background: var(--header-blue);
    color: #fff;
    font-weight: 700;
    padding: 1rem 1.25rem;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 2px 4px rgba(0,0,0,.05);
    margin-top: 1.5rem;
    }

    /* --- Class name titles inside the Sample Classes section --- */
    .className{
    color: var(--primary);
    font-weight: 700;
    margin: 1rem 0 .5rem;
    }

    /* --- Image grid refinement --- */
    [data-testid="stImage"] img{
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    transition: transform .2s ease, box-shadow .2s ease;
    }

    [data-testid="stImage"] img:hover{
    transform: scale(1.03);
    box-shadow: var(--shadow-strong);
    }

    /* Blue section headers */
    .section-header.blue{
    background: var(--header-blue);
    color:#fff;
    font-weight:700;
    padding:1rem 1.25rem;
    border-radius:12px 12px 0 0;
    box-shadow:0 2px 4px rgba(0,0,0,.05);
    margin-top:1.25rem;
    }

    /* Spec chips under the selector */
    .spec-chip{
    display:inline-flex; flex-direction:column; gap:.15rem;
    background:#fff; border-radius:999px; padding:.45rem .9rem;
    box-shadow:var(--shadow-soft);
    border:1px solid rgba(0,0,0,.06);
    min-width:140px; text-align:center;
    }
    .spec-chip span{ color:var(--muted); font-weight:600; font-size:.85rem; }
    .spec-chip b{ color:var(--text); font-weight:800; }

    /* Description strip */
    .model-desc{
    margin-top:1rem;
    background:var(--panel-accent);
    border-left:6px solid var(--primary);
    border-radius:var(--radius-md);
    padding:.9rem 1rem;
    box-shadow:var(--shadow-soft);
    }

    /* Right panel info cards */
    .model-info-card{
    background:#fff;
    border-radius:var(--radius-md);
    box-shadow:var(--shadow-soft);
    padding:1rem 1.1rem;
    margin-bottom:1rem;
    border:1px solid rgba(0,0,0,.04);
    }
    .model-info-card h4{
    margin:.1rem 0 .5rem;
    font-size:1rem;
    color:var(--text);
    }
    .model-info-card p{ margin:.2rem 0; }

    /* Evaluation metric cards grid */
    .eval-metrics-grid{
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: .75rem;
    margin-bottom: .75rem;
    }
    .metric-card{
    background:#fff;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    padding:.75rem .9rem;
    border:1px solid rgba(0,0,0,.05);
    }
    .metric-card .label{
    color: var(--muted);
    font-weight:600;
    font-size:.9rem;
    margin-bottom:.25rem;
    }
    .metric-card .value{
    color: var(--primary);
    font-weight:800;
    font-size:1.15rem;
    }

    .summary-card{
    background:#fff;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    padding: .9rem 1rem;
    align-items:stretch;
    }
    .summary-card h4{
    margin:.1rem 0 .6rem;
    font-size:1rem;
    color: var(--text);
    }

    .stat-chip{
    display:inline-flex; flex-direction:column; gap:.15rem;
    min-width: 120px;
    }
    .stat-chip span{ color: var(--muted); font-weight:600; font-size:.85rem; }
    .stat-chip b{ color: var(--primary); font-weight:800; }

    .muted-line{ color: var(--muted); margin-top:.25rem; }

    /* ---------- Grad-CAM pair gallery polish ---------- */
    .pair-title{
    font-weight: 800;
    color: var(--text);
    margin: .25rem 0 .35rem;
    font-size: .95rem;
    opacity: .95;
    }
    .pair-title.grad{
    color: var(--primary);
    }
    .pair-caption{
    color: var(--muted);
    font-weight: 600;
    margin-top: .35rem;
    font-size: .95rem;
    }

    /* Nicer images: rounded + subtle shadow */
    [data-testid="stImage"] img{
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    }

    /* Keep rows tidy */
    .block-container .stColumns{
    margin-bottom: .5rem;
    }

    /* Titles & captions (you already have these, kept here for completeness) */
    .pair-title{
    font-weight: 800;
    color: var(--text);
    margin: .25rem 0 .35rem;
    font-size: .95rem;
    opacity: .95;
    }
    .pair-title.grad{ color: var(--primary); }
    .pair-caption{
    color: var(--muted);
    font-weight: 600;
    margin-top: .35rem;
    font-size: .95rem;
    }

    /* Image block wrapper so we can add highlight borders */
    .img-block{
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    padding: 4px;
    background: #fff;
    box-shadow: var(--shadow-soft);
    }
    .img-block.high{
    border-color: #22c55e;            /* green ring when >80% */
    box-shadow: 0 0 0 4px rgba(34,197,94,.35);
    }

    /* The image itself */
    .cam-img{
    width: 100%;
    height: auto;
    display: block;
    border-radius: calc(var(--radius-md) - 2px);
    }

    /* Row spacing */
    .block-container .stColumns{ margin-bottom: .5rem; }

    /* Card shell already matches your screenshot */
    .summary-card{
    background:#fff;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    padding: 1rem 1.1rem;
    }
    .summary-card h4{
    margin:.1rem 0 .9rem;
    font-size:1rem;
    color: var(--text);
    }

    /* Two-column key/value layout like your Model/Hyperparameters cards */
    .kv-grid{
    display:grid;
    grid-template-columns: 1fr 1fr;  /* two columns per row */
    gap: 1.0rem 2.2rem;              /* row / col gap */
    margin-bottom:.35rem;
    }
    .kv-item{}
    .kv-label{
    color: var(--muted);
    font-weight: 600;
    font-size: .95rem;
    margin-bottom:.15rem;
    }
    .kv-value{
    color: var(--primary);
    font-weight: 800;
    font-size: 1.05rem;
    }

    /* === Layout and section balance === */
    .image-card{
    background:#fff;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    padding: .8rem;
    text-align:center;
    }
    .img-meta{
    color: var(--muted);
    font-size:.9rem;
    margin-top:.6rem;
    text-align:left;
    }

    /* Prediction results + probability + gradcam cards */
    .card-subtitle{
    font-weight:700;
    font-size:2.1rem;
    color: var(--text);
    margin:.5rem 0 .6rem;
    }
    .result-card{
    background:#fff;
    border-radius: var(--radius-md);
    padding:.8rem 1rem;
    margin-bottom:.6rem;
    box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    }
    .result-card.success{ background:#E6F4EA; color:#0b6833; font-weight:600; }
    .result-card.highlight{
    background:#f9f6ef;
    text-align:center;
    }
    .result-card .big-text{
    color:var(--primary);
    font-size:1.8rem;
    font-weight:900;
    }

    /* Keep Grad-CAM images visually paired */
    .block-container .stColumns{ align-items:start; }

    /* Header: show both sides in one line (like your screenshot) */


    /* Cards */
    .image-card{
    background:#fff;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    padding:.6rem;
    }
    .img-meta{ color: var(--muted); font-size:.9rem; margin-top:.5rem; }

    .result-panel { }
    .pred-tag{
    background:#E6F4EA; color:#0b6833; border:1px solid rgba(0,0,0,.05);
    border-radius: var(--radius-md); padding:.55rem .8rem; margin:.3rem 0 .5rem;
    box-shadow: var(--shadow-soft);
    }
    .pred-tag.success b{ color:#0b6833; }

    .result-card{
    background:#fff; border-radius: var(--radius-md); padding:.8rem 1rem;
    margin:.55rem 0; box-shadow: var(--shadow-soft);
    border:1px solid rgba(0,0,0,.05);
    }
    .result-card.highlight{ background:#f3efe6; }
    .result-card .conf-label{ color:var(--muted); font-weight:700; margin-bottom:.25rem; }
    .result-card .big-text{ color:var(--primary); font-size:1.75rem; font-weight:900; }

    /* Subtitles */
    .card-subtitle{ font-weight:700; color:var(--text); margin:.6rem 0 .6rem; }
    .card-subtitle.mt{ margin-top: 1rem; }

    /* Horizontal probability bars */
    .hbar-row{
    display:grid; grid-template-columns: 140px 1fr 70px; gap:.6rem; align-items:center;
    margin:.4rem 0;
    }
    .hbar-label{ color: var(--text); font-weight:700; }
    .hbar{
    width:100%; height:14px; background:#e7edf6; border-radius:999px; overflow:hidden;
    border:1px solid rgba(0,0,0,.06);
    }
    .hbar-fill{
    height:100%; background: var(--primary);
    }
    .hbar-val{ text-align:right; font-weight:800; color: var(--primary); }

    /* Grad-CAM pair row spacing */
    .gradcam-row{ margin-top: 1rem; }

    /* Make both columns feel balanced in height */
    div[data-testid="column"] > div{ display:flex; flex-direction:column; }
    .predictionResult{
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--text);
    margin-bottom: 0.6rem;
    text-align: center;}

    .pair-title{
    font-weight: 800;
    color: var(--text);
    margin: .25rem 0 .35rem;
    font-size: 1.05rem;
    }
    .pair-title.grad{ color: var(--primary); }

    .img-block{
    border: 1px solid rgba(0,0,0,.06);
    border-radius: var(--radius-md);
    background: #fff;
    padding: 6px;
    box-shadow: var(--shadow-soft);
    }
    .img-block [data-testid="stImage"] img{
    border-radius: calc(var(--radius-md) - 2px);
    }

    .pair-caption{
    color: var(--muted);
    font-weight: 700;
    margin-top: .45rem;
    }

    .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: #0f172a;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 9999;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}

/* BRAND */
.navbar-brand {
    color: #38bdf8;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* MENU */
.navbar-menu {
    display: flex;
    gap: 1.5rem;
}

.navbar-menu a {
    color: #e5e7eb;
    text-decoration: none;
    font-size: 15px;
    font-weight: 500;
}

.navbar-menu a:hover {
    color: #38bdf8;
}

<div class="navbar">
    <div class="navbar-brand">DeepFoundry AI</div>
    <div class="navbar-menu">
        <a href="#train">Train</a>
        <a href="#evaluate">Evaluate</a>
        <a href="#inference">Inference</a>
        <a href="#about">About</a>
    </div>
</div>

    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_stepper(current):
    steps = [
        ("dataset", "Dataset"),
        ("model_&_hyperparameters", "Model"),
        ("training", "Training"),
        ("inference", "Inference"),
    ]

    st.markdown("""
    <style>
    .stepper {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1.5rem 0 2rem 0;
    }

    .step {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 14px;
        color: #94a3b8;
        background: #020617;
        border: 1px solid #1e293b;
    }

    .step.active {
        background: #38bdf8;
        color: #020617;
        border-color: #38bdf8;
    }

    .step.completed {
        background: #022c22;
        color: #34d399;
        border-color: #34d399;
    }

    .arrow {
        margin: 0 10px;
        font-size: 18px;
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

    html = '<div class="stepper">'
    for i, (key, label) in enumerate(steps):
        if key == current:
            cls = "step active"
            icon = "▶"
        elif steps.index((key, label)) < steps.index(next(s for s in steps if s[0] == current)):
            cls = "step completed"
            icon = "✔"
        else:
            cls = "step"
            icon = "○"

        html += f'<div class="{cls}">{icon} {label}</div>'
        if i < len(steps) - 1:
            html += '<div class="arrow">➜</div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_stepper_navbar1(current):
    steps = [
        ("dataset", "Dataset"),
        ("model_&_hyperparameters", "Model"),
        ("training", "Training"),
        ("inference", "Inference"),
    ]

    st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: linear-gradient( 90deg,  rgba(15, 23, 42, 0.8),  rgba(47, 107, 174, 0.8));
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        padding: 0 2rem;
        z-index: 9999;
        margin-bottom: 60px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    .brand {
        font-size: 20px;
        font-weight: 700;
        color: #38bdf8;
        padding-top: 0px;
        white-space: nowrap;
        justify-content: center;
    }

    .stepper-wrapper {
        display: flex;
        justify-content: center;
    }

    .stepper {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .step {
        padding: 10px 18px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid transparent;
        white-space: nowrap;
    }

    .step.completed {
        background: #022c22;
        color: #34d399;
        border-color: #34d399;
    }

    .step.active {
        background: #38bdf8;
        color: #020617;
        border-color: #38bdf8;
    }

    .step.upcoming {
        background: #020617;
        color: #94a3b8;
        border-color: #1e293b;
    }

    .arrow {
        color: #64748b;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    current_index = [s[0] for s in steps].index(current)

    html = """
    <div class="navbar">
        <div class="brand">🫁 DeepFoundry </div>
        <div class="stepper-wrapper">
            <div class="stepper">
    """

    for i, (key, label) in enumerate(steps):
        if i < current_index:
            cls, icon = "step completed", "✔"
        elif i == current_index:
            cls, icon = "step active", "▶"
        else:
            cls, icon = "step upcoming", "○"

        html += f'<div class="{cls}">{icon} {label}</div>'
        if i < len(steps) - 1:
            html += '<div class="arrow">➜</div>'

    html += """
            </div>
        </div>
        <div></div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_stepper_navbar(current):
    steps = [
        ("dataset", "Dataset"),
        ("model_&_hyperparameters", "Model"),
        ("training", "Training"),
        ("inference", "Inference"),
    ]

    st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: linear-gradient(90deg, #020617, #0f172a);
        display: grid;
        grid-template-columns: auto 1fr;
        padding: 0rem 2rem;
        z-index: 9999;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    .brand {
    
    font-size: 22px;
    font-weight: 600;
    color: #38bdf8;
    }

.center {
    display: flex;
    flex-direction: column;
    align-items: center;
}

    .title {
        font-size: 16px;
        font-weight: 800;
        color: #919191;
        align-items: left;
        padding-top: 16px;
    }


    .stepper {
        display: flex;
        align-items: left;
        gap: 14px;
        margin-top: 15px;
    }

    .step {
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid transparent;
    }

    .step.completed {
        background: #022c22;
        color: #34d399;
        border-color: #34d399;
    }

    .step.active {
        background: #38bdf8;
        color: #020617;
        border-color: #38bdf8;
    }

    .step.upcoming {
        background: #020617;
        color: #94a3b8;
        border-color: #1e293b;
    }

    .arrow {
        color: #64748b;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    current_index = [s[0] for s in steps].index(current)

    html = """
    <div class="navbar">
        <div class="brand">🫁 DeepFoundry</div>
        <div class="center">
            <div class="title">Clinical Imaging AI Pipeline: Design, Training, Evaluation & Inference</div>
            <div class="stepper">
    """

    for i, (key, label) in enumerate(steps):
        if i < current_index:
            cls, icon = "step completed", "✔"
        elif i == current_index:
            cls, icon = "step active", "▶"
        else:
            cls, icon = "step upcoming", "○"

        html += f'<div class="{cls}">{icon} {label}</div>'
        if i < len(steps) - 1:
            html += '<div class="arrow">➜</div>'

    html += """
            </div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)