import os
import streamlit as st
from PIL import Image
from deepfoundry.core.data_loader import scan_dataset_folder

def show_dataset_page():
    st.markdown('<div class="main-container"><div class="section-header">Dataset Configuration</div>', unsafe_allow_html=True)

    st.markdown('<div class="nested-container ">', unsafe_allow_html=True)
    st.markdown("<h3>Select Dataset Folder</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        folder_path = st.text_input(
            "Enter the path to your dataset folder",
            placeholder="e.g., C:/Users/YourUser/Desktop/dataset",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Load Dataset", use_container_width=True):
            if folder_path:
                info = scan_dataset_folder(folder_path)
                if info:
                    st.session_state.dataset_info = info
                    st.session_state.dataset_path = folder_path
                    st.success("Dataset loaded successfully!")
            else:
                st.warning("Please enter a folder path.")
    st.caption("📌 Select a folder with subfolders for each class (e.g., folder/class1/, folder/class2/).")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Train–Test Split</div>', unsafe_allow_html=True)
    st.markdown('<div class="nested-container">', unsafe_allow_html=True)
    split_value = st.slider("Train–Test Split", 0, 100, st.session_state.get('split_value', 80), label_visibility="collapsed")
    st.session_state.split_value = split_value
    c1, c2 = st.columns(2)
    with c1: st.metric("Training", f"{split_value}%")
    with c2: st.metric("Testing", f"{100 - split_value}%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Dataset Preview</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-container">', unsafe_allow_html=True)
    info = st.session_state.get('dataset_info')
    if info:
        total_images = info['total_images']
        train_count = int(total_images * (split_value / 100))
        test_count = total_images - train_count
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Total Images", total_images)
        with c2: st.metric("Train Images", train_count)
        with c3: st.metric("Test Images", test_count)

        classes = info["class_names"]
        cls_count = len(classes)
        chips_html = "".join(
            f'<li class="pill"><span class="name">{name}</span>: '
            f'<span class="count-blue">{cnt} images</span></li>'
            for name, cnt in info["classes"].items()
        )
        st.markdown(
            f"""
            <div class="classes-box">
                <div class="classes-header">
                    <span>Classes</span>
                    <span class="classes-badge">{cls_count}</span>
                </div>
                <ul class="classes-list">{chips_html}</ul>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.info("👆 Enter a dataset folder path and click **Load Dataset** to see the preview.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header blue">Sample Classes</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    if info and info['sample_images']:
        for class_name, image_paths in info['sample_images'].items():
            st.markdown(f"<h3 class='className'>📂 {class_name.capitalize()}</h3>", unsafe_allow_html=True)
            img_cols = st.columns(5)
            for i, col in enumerate(img_cols):
                if i < len(image_paths):
                    try:
                        image = Image.open(image_paths[i])
                        col.image(image, caption=os.path.basename(image_paths[i]), use_container_width=True)
                    except Exception:
                        col.error("Failed to load image")
    else:
        st.info("👆 Load a dataset to view sample images from each class.")
    st.markdown('</div>', unsafe_allow_html=True)

    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("Next: Model & Hyperparameters →", type="primary", use_container_width=True):
            if st.session_state.get('dataset_info'):
                st.session_state.current_page = 'model_&_hyperparameters'
                st.rerun()
            else:
                st.error("Please load a dataset first!")
