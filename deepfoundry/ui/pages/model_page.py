import streamlit as st
from deepfoundry.constants import MODEL_CONFIGS, OPTIMIZERS

def show_model_page():
    if not st.session_state.get('dataset_info'):
        st.error("⚠️ Please configure dataset first!")
        if st.button("← Go to Dataset Configuration"):
            st.session_state.current_page = 'dataset'; st.rerun()
        return

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="section-header blue">🧠 Model Selection</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        selected_model = st.selectbox("Choose a pre-trained model", list(MODEL_CONFIGS.keys()), index=0)
        st.session_state.selected_model = selected_model
        mi = MODEL_CONFIGS[selected_model]

        specs = st.columns(3)
        with specs[0]: st.markdown(f"<div class='spec-chip'><span>Input</span><b>{mi['input_shape']}</b></div>", unsafe_allow_html=True)
        with specs[1]: st.markdown(f"<div class='spec-chip'><span>Trainable</span><b>{mi['trainable_params']:,}</b></div>", unsafe_allow_html=True)
        with specs[2]:
            total_params = mi['trainable_params'] + mi.get('non_trainable_params', 0)
            st.markdown(f"<div class='spec-chip'><span>Total</span><b>{total_params:,}</b></div>", unsafe_allow_html=True)
        st.markdown(f"""<div class="model-desc"><strong>Description:</strong> {mi['description']}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">⚙️ Hyperparameters</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            epochs = st.number_input("Number of Epochs", min_value=1, max_value=200, value=10)
            learning_rate = st.number_input("Learning Rate", min_value=0.00001, max_value=1.0, value=0.001, format="%.5f")
            optimizer = st.selectbox("Optimizer", OPTIMIZERS)
        with col2:
            img_height = st.number_input("Image Height", min_value=32, max_value=512, value=mi['input_shape'][0])
            img_width  = st.number_input("Image Width",  min_value=32, max_value=512, value=mi['input_shape'][1])
            batch_size = st.number_input("Batch Size",   min_value=1, max_value=256, value=32)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">🔄 Data Augmentation</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            rotation = st.checkbox("Rotation", value=True, key="aug_rotation")
            rotation_range = st.slider("Rotation Range", 0, 180, 20, disabled=not rotation, key="aug_rotation_range")
        with c2:
            zoom = st.checkbox("Zoom", value=True, key="aug_zoom")
            zoom_range = st.slider("Zoom Range", 0.0, 1.0, 0.2, disabled=not zoom, key="aug_zoom_range")
        with c3:
            shear = st.checkbox("Shear", value=False, key="aug_shear")
            shear_range = st.slider("Shear Range", 0.0, 1.0, 0.2, disabled=not shear, key="aug_shear_range")
        with c4:
            shift = st.checkbox("Width/Height Shift", value=True, key="aug_shift")
            shift_range = st.slider("Shift Range", 0.0, 1.0, 0.2, disabled=not shift, key="aug_shift_range")

        d1, d2, d3, d4 = st.columns(4)
        with d1:
            horizontal_flip = st.checkbox("Horizontal Flip", value=True, key="aug_hflip")
            st.caption("Flip left-right at random.")
        with d2:
            vertical_flip = st.checkbox("Vertical Flip", value=False, key="aug_vflip")
            st.caption("Flip top-bottom at random.")
        with d3:
            brightness = st.checkbox("Brightness", value=True, key="aug_brightness")
            brightness_range = st.slider("Brightness Range", 0.0, 2.0, 0.2, disabled=not brightness, key="aug_brightness_range")
        with d4:
            st.markdown('<div class="card-subtle">Tip: Start light. Too-strong aug can hurt validation accuracy.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="section-header blue">📊 Model Info</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        model_info = mi
        num_classes = len(st.session_state.dataset_info['class_names'])
        total_params = model_info['trainable_params'] + model_info.get('non_trainable_params', 0)
        st.markdown(
            f"""
            <div class="model-info-card">
              <h4>Architecture</h4>
              <p><strong>Model:</strong> {st.session_state.selected_model}</p>
              <p><strong>Input Shape:</strong> {model_info['input_shape']}</p>
              <p><strong>Output Classes:</strong> {num_classes}</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="model-info-card">
              <h4>Parameters</h4>
              <p><strong>Trainable:</strong> {model_info['trainable_params']:,}</p>
              <p><strong>Non-trainable:</strong> {model_info.get('non_trainable_params', 0):,}</p>
              <p><strong>Total:</strong> {total_params:,}</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="model-info-card">
              <h4>Training Config</h4>
              <p><strong>Epochs:</strong> {epochs}</p>
              <p><strong>Batch Size:</strong> {batch_size}</p>
              <p><strong>Learning Rate:</strong> {learning_rate}</p>
              <p><strong>Optimizer:</strong> {optimizer}</p>
              <p><strong>Image Size:</strong> {img_height}×{img_width}</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    btn_cols = st.columns([1, 1, 1])
    with btn_cols[0]:
        if st.button("← Back to Dataset", use_container_width=True):
            st.session_state.current_page = 'dataset'; st.rerun()
    with btn_cols[2]:
        if st.button("Next: Training →", type="primary", use_container_width=True):
            st.session_state.hyperparameters = {
                'epochs': epochs,
                'learning_rate': learning_rate,
                'optimizer': optimizer,
                'batch_size': batch_size,
                'img_size': (img_height, img_width)
            }
            st.session_state.augmentation_params = {
                'rotation': rotation, 'rotation_range': rotation_range,
                'zoom': zoom, 'zoom_range': zoom_range,
                'shear': shear, 'shear_range': shear_range,
                'shift': shift, 'shift_range': shift_range,
                'horizontal_flip': horizontal_flip, 'vertical_flip': vertical_flip,
                'brightness': brightness, 'brightness_range': brightness_range
            }
            st.session_state.current_page = 'training'
            st.rerun()
