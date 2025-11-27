import streamlit as st
import time
import shutil
import os
import stat
from pathlib import Path

# Import Lazarus Engine
from scanner import scan_repository
from dependency_manager import update_dependencies
from security_patcher import patch_security
from code_modernizer import modernize_codebase

# --- CONFIGURATION ---
st.set_page_config(page_title="Lazarus AI", page_icon="💀", layout="wide", initial_sidebar_state="collapsed")

# --- THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; background-image: radial-gradient(circle at center, #1a0000 0%, #000000 100%); color: #d0d0d0; font-family: 'Consolas', monospace; }
    h1 { color: #ff0000; text-shadow: 0 0 15px #8a0000; text-transform: uppercase; }
    h3 { border-bottom: 1px solid #330000; color: #e0e0e0; }
    .stMetricValue { color: #ff3333 !important; text-shadow: 0 0 5px #550000; }
    .stButton button { background-color: #1a0000; color: #cc0000; border: 1px solid #cc0000; transition: all 0.2s; }
    .stButton button:hover { background-color: #cc0000; color: #000; box-shadow: 0 0 20px #cc0000; }
    div[data-testid="stExpander"] { background-color: #0a0a0a; border: 1px solid #330000; }
    .blood-pulse { animation: blood-pulse 2s infinite; }
    @keyframes blood-pulse { 0% {box-shadow: inset 0 0 0 0 rgba(138,0,0,0);} 50% {box-shadow: inset 0 0 100px 50px rgba(138,0,0,0.5);} 100% {box-shadow: inset 0 0 0 0 rgba(138,0,0,0);} }
    </style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'report' not in st.session_state: st.session_state.report = None
if 'local_path' not in st.session_state: st.session_state.local_path = None
if 'resurrection_done' not in st.session_state: st.session_state.resurrection_done = False
if 'results' not in st.session_state: st.session_state.results = {}

# --- HEADER ---
c1, c2 = st.columns([1, 6])
c1.markdown("<div style='font-size: 4rem; text-align: center;'>🩸</div>", unsafe_allow_html=True)
c2.markdown("# LAZARUS AI\n`STATUS: HUNTING` | `TARGET: DEAD CODE`")
st.markdown("---")

# --- INPUT ---
col1, col2 = st.columns([4, 1])
repo_url = col1.text_input("TARGET REPO", placeholder="https://github.com/user/dead-project", label_visibility="collapsed")
if col2.button("INITIATE SCAN", use_container_width=True) and repo_url:
    with st.status(">> HUNTING...", expanded=True):
        if st.session_state.local_path and Path(st.session_state.local_path).exists():
            try:
                shutil.rmtree(st.session_state.local_path, ignore_errors=True)
            except: pass
        st.session_state.report = scan_repository(repo_url, cleanup=False)
        st.session_state.local_path = st.session_state.report['local_path']
        st.session_state.resurrection_done = False
        st.rerun()

# --- DEATH REPORT ---
if st.session_state.report and not st.session_state.resurrection_done:
    r = st.session_state.report
    st.markdown("### /// AUTOPSY RESULTS")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SUBJECT", r['project_name'])
    c2.metric("DECAY", f"{100 - r['resurrection_score']}%")
    c3.metric("DEPENDENCIES", r['dependency_health']['total'])
    c4.metric("CRITICAL", r['dependency_health']['outdated'])
    
    if st.button("🩸 PERFORM BLOOD RITUAL (RESURRECT)", type="primary"):
        path = st.session_state.local_path
        prog = st.progress(0)
        
        # 1. Dependencies
        with st.status(">> INJECTING ADRENALINE...", expanded=True):
            dep_res = update_dependencies(path, r['dependency_health']['details'])
        prog.progress(33)
        
        # 2. Security
        with st.status(">> CAUTERIZING WOUNDS...", expanded=True):
            sec_res = patch_security(path)
        prog.progress(66)
        
        # 3. Modernization
        with st.status(">> MUTATING DNA...", expanded=True):
            mod_res = modernize_codebase(path)
        prog.progress(100)

        # Save Results
        st.session_state.results = {
            "dependencies": dep_res,
            "security": sec_res,
            "modernization": mod_res
        }
        st.session_state.resurrection_done = True
        time.sleep(1)
        st.rerun()

# --- SUCCESS INTERFACE (REPORT & DOWNLOAD) ---
if st.session_state.resurrection_done:
    st.markdown("""<script>window.parent.document.querySelector(".stApp").classList.add("blood-pulse");</script>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #1a0000; border: 2px solid #ff0000; padding: 20px; text-align: center;">
        <h1 style="margin:0;">RITUAL COMPLETE</h1>
    </div>
    """, unsafe_allow_html=True)
    
    res = st.session_state.results
    
    # --- REPORT SECTION ---
    st.markdown("### 📝 RESURRECTION REPORT (BEFORE vs AFTER)")
    
    col_A, col_B = st.columns(2)
    
    with col_A:
        st.info("💀 BEFORE")
        st.write(f"**Outdated Deps:** {st.session_state.report['dependency_health']['outdated']}")
        st.write(f"**Vulnerabilities:** UNKNOWN (Likely Critical)")
        st.write(f"**Syntax:** LEGACY (var, console.log)")
    
    with col_B:
        st.success("🩸 AFTER")
        st.write(f"**Updated:** {len(res['dependencies']['success'])} Packages")
        st.write(f"**Security:** {res['security']['fixed']} Patched")
        st.write(f"**Modernized:** {res['modernization']['files_changed']} Files Refactored")

    with st.expander("🔎 VIEW DETAILED CHANGE LOG"):
        st.markdown("#### 🧬 Files Modernized")
        st.write(res['modernization']['file_names'])
        st.markdown("#### 📦 Dependencies Forced")
        st.write(res['dependencies']['success'])

    st.markdown("---")

    # --- DOWNLOAD SECTION ---
    st.markdown("### 💾 EXPORT PROJECT")
    
    # Create Zip
    zip_path = shutil.make_archive(f"{st.session_state.local_path}_export", 'zip', st.session_state.local_path)
    
    with open(zip_path, "rb") as f:
        st.download_button(
            label="⬇️ DOWNLOAD RESURRECTED PROJECT (.ZIP)",
            data=f,
            file_name="lazarus_resurrection.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        
    if st.button("<< START NEW RITUAL"):
        st.session_state.report = None
        st.session_state.resurrection_done = False
        st.rerun()