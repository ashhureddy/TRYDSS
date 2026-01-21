#==============================================================================
# STREAMLIT UI FOR DSS EXTRACTOR
#==============================================================================
# Description: Web interface for DSS Extractor with NRCellDU Grouping
# Brand: MASTEC
# Developer: AKSHATHA KALLUR
#==============================================================================

import streamlit as st
import pandas as pd
import io
import os
import sys
from datetime import datetime
import zipfile
from contextlib import redirect_stdout

# Import all features
from config import Config
from feature1 import Feature1
from feature2 import Feature2
from feature3 import Feature3
from feature4 import Feature4
from feature5 import Feature5
from feature6 import Feature6

# Page configuration
st.set_page_config(
    page_title="DSS Extractor | MASTEC",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .brand-name {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #F8FAFC;
        padding: 0.5rem;
        text-align: center;
        font-size: 0.85rem;
        color: #64748B;
        border-top: 1px solid #E2E8F0;
        z-index: 999;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .log-box {
        background-color: #1E293B;
        color: #E2E8F0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 60px;
    }
    .success-box {
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="brand-name">MASTEC</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">📡 DSS VALUE Extractor Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automate template filling for DSS </div>', unsafe_allow_html=True)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []
if 'generated_files' not in st.session_state:
    st.session_state.generated_files = []

class StreamCapture:
    """Capture print statements to display in log window"""
    def __init__(self):
        self.logs = []
    
    def write(self, text):
        if text.strip():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.logs.append(f"[{timestamp}] {text.strip()}")
            st.session_state.log_messages.append(f"[{timestamp}] {text.strip()}")
    
    def flush(self):
        pass

def process_excel_file(uploaded_file):
    """Process the uploaded Excel file through all features"""
    
    try:
        # Save uploaded file temporarily
        temp_file_path = "temp_upload.xlsx"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Initialize config
        config = Config()
        config.excel_file_path = temp_file_path
        
        # Capture all print outputs
        stream_capture = StreamCapture()
        
        with redirect_stdout(stream_capture):
            # Feature 1: DSS Extraction
            print("🔵 FEATURE 1: DSS Value Extraction")
            feature1 = Feature1(config)
            filtered_df = feature1.execute()
            
            if filtered_df is None or len(filtered_df) == 0:
                print("⚠️ No DSS values found")
                return None
            
            print(f"✅ Feature 1 Complete")
            print("")
            
            # Feature 2: NRCellDU Grouping
            print("🔵 FEATURE 2: NRCellDU Grouping")
            feature2 = Feature2(config, filtered_df)
            dss_variables = feature2.execute()
            print(f"✅ Feature 2 Complete")
            print("")
            
            # Feature 3: JSON Cleaning
            print("🔵 FEATURE 3: JSON Cleaning")
            feature3 = Feature3(config, dss_variables)
            cleaned_variables = feature3.execute()
            print(f"✅ Feature 3 Complete")
            print("")
            
            # Feature 4: JSON Population
            print("🔵 FEATURE 4: Data Population")
            feature4 = Feature4(config, cleaned_variables)
            populated_variables = feature4.execute()
            print(f"✅ Feature 4 Complete")
            print("")
            
            # Feature 5: Placeholder Mapping
            print("🔵 FEATURE 5: Placeholder Mapping")
            feature5 = Feature5(config, populated_variables)
            mapped_variables = feature5.execute()
            print(f"✅ Feature 5 Complete")
            print("")
            
            # Feature 6: Template Generation
            print("🔵 FEATURE 6: Template Generation")
            feature6 = Feature6(config, mapped_variables)
            generated_files = feature6.execute()
            print(f"✅ Feature 6 Complete")
            print("")
            
            print("🎉 All processing complete!")
        
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return generated_files
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print(f"Details: {traceback.format_exc()}")
        return None

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Excel File")
    
    uploaded_file = st.file_uploader(
        "Choose your Excel file",
        type=['xlsx', 'xls'],
        help="Upload the Excel file containing 5G network configuration data"
    )
    
    if uploaded_file is not None:
        st.markdown('<div class="info-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        
        # Process button appears after upload
        if st.button("🚀 Start Processing", key="process_btn"):
            st.session_state.log_messages = []
            st.session_state.processed = False
            st.session_state.generated_files = []
            
            with st.spinner("⏳ Processing... Please wait..."):
                generated_files = process_excel_file(uploaded_file)
                
                if generated_files and len(generated_files) > 0:
                    st.session_state.generated_files = generated_files
                    st.session_state.processed = True
                    st.success("✅ Processing completed successfully!")
                else:
                    st.error("❌ Processing failed. Check the log for details.")

with col2:
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Upload** your Excel file
    2. Click **Start Processing**
    3. Wait for completion
    4. **Download** generated files
    
    **Note:** Template files must be in the `templates/` folder on the server.
    """)

# Download section - ONLY NOTEPAD FILES
if st.session_state.processed and st.session_state.generated_files:
    st.markdown("---")
    st.markdown("### 📥 Download Generated Files")
    
    # Individual file downloads
    cols = st.columns(min(len(st.session_state.generated_files), 3))
    
    for idx, file_info in enumerate(st.session_state.generated_files):
        col_idx = idx % 3
        
        with cols[col_idx]:
            file_path = file_info['output_file']
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                st.download_button(
                    label=f"📄 {file_info['variable_name']}",
                    data=file_content,
                    file_name=os.path.basename(file_path),
                    mime="text/plain",
                    key=f"download_{idx}"
                )
    
    # Download all as ZIP
    if len(st.session_state.generated_files) > 1:
        st.markdown("---")
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in st.session_state.generated_files:
                file_path = file_info['output_file']
                if os.path.exists(file_path):
                    zip_file.write(file_path, os.path.basename(file_path))
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="📦 Download All Files (ZIP)",
            data=zip_buffer,
            file_name=f"dss_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )

# Log window
st.markdown("---")
st.markdown("### 📊 Processing Log")

if st.session_state.log_messages:
    log_content = "\n".join(st.session_state.log_messages)
    st.markdown(f'<div class="log-box">{log_content}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="log-box">Waiting for file upload...</div>', unsafe_allow_html=True)

# Footer
st.markdown(f'''
    <div class="footer">
        Made by <strong>AKSHATHA KALLUR</strong> | Powered by <strong>MASTEC</strong> | © {datetime.now().year}
    </div>
''', unsafe_allow_html=True)


