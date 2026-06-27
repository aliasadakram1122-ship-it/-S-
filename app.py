import streamlit as st
import google.generativeai as genai
import re
import urllib.parse

st.set_page_config(page_title="Asad Official - eBay VIP Generator", page_icon="🚀", layout="wide")

st.title("🚀 Asad Official - eBay VIP Listing Generator")
st.caption("Amazon link paste karein aur premium animated HTML code hasil karein.")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ API Key not found! Please add it in Streamlit Settings -> Secrets.")
    st.stop()

theme_option = st.selectbox("🎯 Select Category Theme:", ["Automotive / Hardware", "Art & Craft / Tools", "Skin Care / Beauty", "Medical / Pharmacy", "Pet Care", "Garden / Organic", "Hygiene / Household"])

theme_colors = {
    "Automotive / Hardware": {"brand": "#1e40af", "accent": "#94a3b8", "black": "#0f172a", "soft": "#f8fafc"},
    "Art & Craft / Tools": {"brand": "#7c2d12", "accent": "#f59e0b", "black": "#0f172a", "soft": "#fffbeb"},
    "Skin Care / Beauty": {"brand": "#9f1239", "accent": "#fcd34d", "black": "#4c0519", "soft": "#fff1f2"},
    "Medical / Pharmacy": {"brand": "#991b1b", "accent": "#fbbf24", "black": "#450a0a", "soft": "#fef2f2"},
    "Pet Care": {"brand": "#4c1d95", "accent": "#f59e0b", "black": "#2e1065", "soft": "#f5f3ff"},
    "Garden / Organic": {"brand": "#166534", "accent": "#84cc16", "black": "#052e16", "soft": "#f7fee7"},
    "Hygiene / Household": {"brand": "#14532d", "accent": "#4ade80", "black": "#052e16", "soft": "#f0fdf4"}
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
        product_data_to_process = st.text_input("📝 Type Product Title Manually:")

if st.button("✨ Generate VIP Listing Code"):
    if product_data_to_process:
        with st.spinner("💎 Extrapolating premium data and scanning available AI models..."):
            try:
                genai.configure(api_key=api_key)
                
                # --- AUTO-DETECT WORKING MODEL ---
                working_model_name = None
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        working_model_name = m.name
                        break # Jo pehla chalne wala model mil jaye, usay select kar lo
                
                if not working_model_name:
                    st.error("❌ Google ka koi bhi text model is waqt available nahi hai!")
                    st.stop()
                
                # --- RUN AI WITH DETECTED MODEL ---
                model = genai.GenerativeModel(working_model_name) 
                
                prompt = f"Write eBay HTML for '{product_data_to_process}'. Colors: --brand-color: {selected_colors['brand']}; --accent-glow: {selected_colors['accent']}; --premium-black: {selected_colors['black']}; --soft-bg: {selected_colors['soft']}; Use .hero-section, .product-intro, .grid-layout, .info-terminal, .usage-box, .trust-bar. Return ONLY HTML."
                
                response = model.generate_content(prompt)
                generated_html = re.sub(r'^```html\s*|```$', '', response.text, flags=re.MULTILINE)
                
                st.success(f"🎉 VIP eBay Listing Code is Ready! (Model used: {working_model_name})")
                st.components.v1.html(generated_html, height=1200, scrolling=True)
                st.text_area("Copy your code:", value=generated_html, height=600)
            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")
