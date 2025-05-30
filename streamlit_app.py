import streamlit as st
import re
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64

# Page config
st.set_page_config(
    page_title="Sensory-Friendly Content Adapter",
    page_icon="🧠",
    layout="wide"
)

# Title and description
st.title("🧠 AI-Powered Sensory-Friendly Content Adapter")
st.markdown("*Automatically adapt content to reduce sensory overload*")

# Sidebar for sensitivity settings
st.sidebar.header("Sensory Preferences")
sensitivity_level = st.sidebar.select_slider(
    "Sensitivity Level",
    options=["Low", "Medium", "High"],
    value="Medium"
)

# Adaptation settings
text_simplify = st.sidebar.checkbox("Simplify Text", value=True)
reduce_colors = st.sidebar.checkbox("Reduce Color Intensity", value=True)
calm_palette = st.sidebar.checkbox("Apply Calm Color Palette", value=True)

# Main content area
tab1, tab2 = st.tabs(["📝 Text Adapter", "🎨 Image Adapter"])

# Tab 1: Text Adaptation
with tab1:
    st.header("Text Content Adaptation")
    
    input_text = st.text_area(
        "Paste your text here:",
        height=200,
        placeholder="Enter text that might be overwhelming or complex..."
    )
    
    if input_text:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Text")
            st.write(input_text)
        
        with col2:
            st.subheader("Adapted Text")
            
            # Simple AI-like text processing
            adapted_text = input_text
            
            if text_simplify:
                # Simplify sentences
                adapted_text = re.sub(r'[!]{2,}', '!', adapted_text)
                adapted_text = re.sub(r'[?]{2,}', '?', adapted_text)
                adapted_text = re.sub(r'[A-Z]{3,}', lambda m: m.group().capitalize(), adapted_text)
                
                # Break long sentences
                sentences = adapted_text.split('. ')
                short_sentences = []
                for sentence in sentences:
                    if len(sentence) > 100:
                        # Split long sentences at commas or conjunctions
                        parts = re.split(r'(, | and | but | or )', sentence)
                        short_sentences.extend([p.strip() for p in parts if p.strip() and p not in [', ', ' and ', ' but ', ' or ']])
                    else:
                        short_sentences.append(sentence)
                adapted_text = '. '.join(short_sentences)
            
            # Apply calm styling
            if calm_palette:
                st.markdown(
                    f'<div style="background-color: #f0f8f0; padding: 15px; border-radius: 10px; color: #2d5a2d; line-height: 1.8;">{adapted_text}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.write(adapted_text)

# Tab 2: Image Adaptation
with tab2:
    st.header("Image Content Adaptation")
    
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        # Load and display original image
        image = Image.open(uploaded_file)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("Adapted Image")
            
            # Apply adaptations based on sensitivity level
            adapted_image = image.copy()
            
            # Reduce brightness and contrast for high sensitivity
            if sensitivity_level == "High":
                enhancer = ImageEnhance.Brightness(adapted_image)
                adapted_image = enhancer.enhance(0.7)
                enhancer = ImageEnhance.Contrast(adapted_image)
                adapted_image = enhancer.enhance(0.6)
            elif sensitivity_level == "Medium":
                enhancer = ImageEnhance.Brightness(adapted_image)
                adapted_image = enhancer.enhance(0.85)
                enhancer = ImageEnhance.Contrast(adapted_image)
                adapted_image = enhancer.enhance(0.8)
            
            # Apply blur for overstimulating content
            if reduce_colors:
                adapted_image = adapted_image.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Reduce color saturation
            if calm_palette:
                enhancer = ImageEnhance.Color(adapted_image)
                adapted_image = enhancer.enhance(0.6)
            
            st.image(adapted_image, use_container_width=True)
            
            # Download button for adapted image
            buf = io.BytesIO()
            adapted_image.save(buf, format='PNG')
            btn = st.download_button(
                label="Download Adapted Image",
                data=buf.getvalue(),
                file_name="adapted_image.png",
                mime="image/png"
            )

# Footer with adaptation summary
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sensitivity Level", sensitivity_level)
with col2:
    st.metric("Active Adaptations", sum([text_simplify, reduce_colors, calm_palette]))
with col3:
    st.metric("Processing Mode", "Real-time")

# Info section
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    This AI-powered adapter helps reduce sensory overload by:
    
    **Text Adaptations:**
    - Simplifying complex sentences
    - Reducing excessive punctuation and caps
    - Breaking long paragraphs into smaller chunks
    
    **Visual Adaptations:**
    - Reducing brightness and contrast
    - Applying calming color palettes
    - Softening sharp visual elements
    
    **Future Features:**
    - Browser extension for real-time web adaptation
    - Integration with reading apps and e-books
    - Custom sensitivity profiles and learning
    
    *Perfect for individuals with autism, ADHD, sensory processing disorders, or anyone who prefers calmer digital experiences.*
    """)