import streamlit as st
from deepfoundry.ui.style import inject_theme, render_stepper_navbar
from deepfoundry.ui.pages.dataset_page import show_dataset_page
from deepfoundry.ui.pages.model_page import show_model_page
from deepfoundry.ui.pages.training_page import show_training_page
from deepfoundry.ui.pages.inference_page import show_inference_page

st.set_page_config(page_title="Deep Learning Image Classifier", page_icon="🖼️", layout="wide")
inject_theme()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dataset'
if 'dataset_info' not in st.session_state:
    st.session_state.dataset_info = None
if 'dataset_path' not in st.session_state:
    st.session_state.dataset_path = None
if 'training_complete' not in st.session_state:
    st.session_state.training_complete = False
if 'training_history' not in st.session_state:
    st.session_state.training_history = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'tf_model' not in st.session_state:
    st.session_state.tf_model = None
if 'split_value' not in st.session_state:
    st.session_state.split_value = 80



render_stepper_navbar(st.session_state.current_page)


if st.session_state.current_page == 'dataset':
    show_dataset_page()
elif st.session_state.current_page == 'model_&_hyperparameters':
    show_model_page()
elif st.session_state.current_page == 'training':
    show_training_page()
elif st.session_state.current_page == 'inference':
    show_inference_page()

st.markdown('---')
st.markdown("""
<div style='text-align: center; color: #7FE4D3; padding: 1rem;'>
  <p>🖼️ Deep Learning Image Classifier | Built with Streamlit & TensorFlow/Keras</p>
  <p style='font-size: 0.9rem;'>💡 Note: This is a demonstration app. In production, integrate with actual TensorFlow/Keras models for real training.</p>
</div>
""", unsafe_allow_html=True)