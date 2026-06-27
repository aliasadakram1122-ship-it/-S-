import streamlit as st
import google.generativeai as genai
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Page Configuration (Aap ke naam se)
st.set_page_config(page_title="[ᴀSᴀᴅㅤᴏҒҒɪᴄᴀʟ] - eBay VIP Generator", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a, #0284c7);
        color: white; font-weight: bold; border-radius: 12px;
        padding: 10px 24px; border: none; transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(2, 132, 199, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Main Website Header
st.title("🚀 [Apka Naam] - eBay VIP Listing Generator")
st.caption("Amazon link paste karein aur premium animated HTML code hasil karein.")

# Sidebar API Key
st.sidebar.header("🔑 Setup Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

theme_option = st.selectbox(
    "🎯 Select Product Category Theme:",
    ["Automotive / Hardware (Steel & Blue)", "Art & Craft / Tools (Terracotta & Gold)", "Skin Care / Beauty (Rosewood & Oat Gold)", "Medical / Pharmacy (Clinical Red & Gold)", "Pet Care (Velvet Purple & Gold)", "Garden / Organic (Forest Green & Lime)", "Hygiene / Household (Botanical Green & Aloe)"]
)

theme_colors = {
    "Automotive / Hardware (Steel & Blue)": {"brand": "#1e40af", "accent": "#94a3b8", "black": "#0f172a", "soft": "#f8fafc"},
    "Art & Craft / Tools (Terracotta & Gold)": {"brand": "#7c2d12", "accent": "#f59e0b", "black": "#0f172a", "soft": "#fffbeb"},
    "Skin Care / Beauty (Rosewood & Oat Gold)": {"brand": "#9f1239", "accent": "#fcd34d", "black": "#4c0519", "soft": "#fff1f2"},
    "Medical / Pharmacy (Clinical Red & Gold)": {"brand": "#991b1b", "accent": "#fbbf24", "black": "#450a0a", "soft": "#fef2f2"},
    "Pet Care (Velvet Purple & Gold)": {"brand": "#4c1d95", "accent": "#f59e0b", "black": "#2e1065", "soft": "#f5f3ff"},
    "Garden / Organic (Forest Green & Lime)": {"brand": "#166534", "accent": "#84cc16", "black": "#052e16", "soft": "#f7fee7"},
    "Hygiene / Household (Botanical Green & Aloe)": {"brand": "#14532d", "accent": "#4ade80", "black": "#052e16", "soft": "#f0fdf4"}
}

selected_colors = theme_colors[theme_option]

product_url = st.text_input("🔗 Paste Amazon Product URL here:")
product_data_to_process = ""

if product_url:
    match = re.search(r'amazon\.[a-z\.]+/(.*?)/dp/', product_url)
    if match:
        extracted_name = urllib.parse.unquote(match.group(1).replace('-', ' '))
        st.success(f"✅ Product Identified: **{extracted_name}**")
        product_data_to_process = extracted_name
    else:
        st.warning("⚠️ Could not read link format. Please try pasting the title manually.")
        product_data_to_process = st.text_input("📝 Type Product Title Manually:")

if st.button("✨ Generate VIP Listing Code"):
    if not api_key or not product_data_to_process:
        st.error("❌ Please provide API Key and Product Link!")
    else:
        with st.spinner("💎 Extrapolating premium data..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are a premium product copywriter. Product: "{product_data_to_process}".
                Generate an HTML eBay listing using these exact colors:
                --brand-color: {selected_colors['brand']};
                --accent-glow: {selected_colors['accent']};
                --premium-black: {selected_colors['black']};
                --soft-bg: {selected_colors['soft']};
                Structure: .hero-section, .product-intro (with 4 .hero-badge), .grid-layout (Core Performance & Benefits), .info-terminal (Specs), .usage-box (Pro Tip), .trust-bar, footer. ONLY output clean HTML text.
                """
                response = model.generate_content(prompt)
                generated_html = re.sub(r'^```html\s*|```$', '', response.text, flags=re.MULTILINE)
                
                st.success("🎉 Your VIP eBay Listing Code is Ready!")
                tab1, tab2 = st.tabs(["👀 Live Preview", "💻 Raw HTML Code"])
                with tab1:
                    st.components.v1.html(generated_html, height=1200, scrolling=True)
                with tab2:
                    st.text_area("Copy your code:", value=generated_html, height=600)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
