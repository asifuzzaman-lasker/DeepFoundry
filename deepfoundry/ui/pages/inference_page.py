import base64
from io import BytesIO
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from deepfoundry.constants import MODEL_CONFIGS
from deepfoundry.core.gradcam import compute_gradcam_tf, compute_gradcam_fallback, overlay_heatmap_on_image

def _get_model_input_size():
    sel = st.session_state.selected_model
    if sel and sel in MODEL_CONFIGS:
        h, w = MODEL_CONFIGS[sel]["input_shape"][:2]
        return (h, w)
    return (224, 224)

def _predict_probabilities(pil_img):
    classes = st.session_state.dataset_info["class_names"]
    K = len(classes)
    model = st.session_state.get("tf_model", None)
    target_size = _get_model_input_size()

    if model is not None:
        img = pil_img.convert("RGB").resize(target_size, Image.LANCZOS)
        arr = np.asarray(img).astype("float32") / 255.0
        arr = np.expand_dims(arr, axis=0)
        probs = model.predict(arr, verbose=0)[0]
        probs = np.asarray(probs, dtype=np.float32)
        s = probs.sum()
        if s <= 0 or s > 1.5:
            probs = np.exp(probs - probs.max()); probs = probs / probs.sum()
    else:
        probs = np.random.dirichlet(np.ones(K))
    return probs, int(np.argmax(probs))

def _gradcam_for_image(pil_img, class_index):
    model = st.session_state.get("tf_model", None)
    target_size = _get_model_input_size()
    heat = compute_gradcam_tf(model, pil_img, class_index, target_size=target_size)
    if heat is None:
        heat = compute_gradcam_fallback(pil_img, target_size=target_size)
    return heat

def _pil_to_b64(pil_img):
    buf = BytesIO(); pil_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def _render_img_block(pil_img, is_high_conf=False, title=None, caption=None):
    b64 = _pil_to_b64(pil_img)
    high_cls = " high" if is_high_conf else ""
    title_html = f"<div class='pair-title{' grad' if title=='Grad-CAM' else ''}'>{title}</div>" if title else ""
    cap_html = f"<div class='pair-caption'>{caption}</div>" if caption else ""
    st.markdown(
        f"""
        {title_html}
        <div class="img-block{high_cls}">
           <img class="cam-img" src="data:image/png;base64,{b64}" />
        </div>
        {cap_html}
        """, unsafe_allow_html=True
    )

def show_inference_page():
    if not st.session_state.get('training_complete'):
        st.error("⚠️ Please complete training first!")
        if st.button("← Go to Training"):
            st.session_state.current_page = 'training'; st.rerun()
        return

    st.markdown('<div class="section-header blue">🔍 Model Inference & Testing</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    inference_mode = st.radio("Select Inference Mode", ["Single Image Prediction", "Batch Image Prediction"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if inference_mode == "Single Image Prediction":
        st.markdown("<div class='section-header'>🖼️ Uploaded Image</div>", unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'bmp'], key="single_upl")
        if uploaded_file is not None:
            if "single_pred_done" not in st.session_state:
                st.session_state.single_pred_done = False
            if st.session_state.get("single_last_name") != uploaded_file.name:
                st.session_state.single_pred_done = False
                st.session_state.single_last_name = uploaded_file.name

            left, right = st.columns([1.2, 1])
            with left:
                pil_img = Image.open(uploaded_file).convert("RGB")
                st.markdown("<div class='image-card'>", unsafe_allow_html=True)
                st.image(pil_img, use_container_width=True)
                st.markdown(
                    f"""
                    <div class='img-meta'>
                    <b>Filename:</b> {uploaded_file.name}<br>
                    <b>Size:</b> {pil_img.size}<br>
                    <b>Mode:</b> {pil_img.mode}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                prob_area = st.container()

            with right:
                st.markdown("<div class='result-panel'><span class='predictionResult'>🧠 Prediction Results</span>", unsafe_allow_html=True)
                go = st.button("🧪  Predict", use_container_width=True, type="primary")
                if go: st.session_state.single_pred_done = True
                pred_box = st.empty(); conf_box = st.empty(); prob_title = st.empty(); table_hold = st.empty()
                st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.single_pred_done:
                with st.spinner("Analyzing image..."):
                    probs, pred_idx = _predict_probabilities(pil_img)
                    classes = st.session_state.dataset_info["class_names"]
                    pred_class = classes[pred_idx]; confidence = float(probs[pred_idx])

                    pred_box.markdown(f"<div class='pred-tag success'>Predicted Class: <b>{pred_class}</b></div>", unsafe_allow_html=True)
                    conf_box.markdown(
                        f"""
                        <div class='result-card highlight'>
                           <div class='conf-label'>Confidence:</div>
                           <div class='big-text'>{confidence:.2%}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )

                    prob_df = pd.DataFrame({"Class": classes, "Probability": probs}).sort_values("Probability", ascending=False).reset_index(drop=True)
                    prob_title.markdown("<h4 class='card-subtitle'>📋 Detailed Probabilities</h4>", unsafe_allow_html=True)
                    table_hold.dataframe(prob_df.style.format({"Probability": "{:.2%}"}), use_container_width=True, height=220)

                    with prob_area:
                        st.markdown("<h4 class='card-subtitle mt'>📊 Class Probabilities</h4>", unsafe_allow_html=True)
                        for cls, p in zip(classes, probs):
                            st.markdown(
                                f"""
                                <div class="hbar-row">
                                  <div class="hbar-label">{cls}:</div>
                                  <div class="hbar"><div class="hbar-fill" style="width:{p*100:.2f}%"></div></div>
                                  <div class="hbar-val">{p*100:.2f}%</div>
                                </div>
                                """, unsafe_allow_html=True
                            )

                    st.markdown("<div class='gradcam-row'>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("<div class='pair-title'>Original</div>", unsafe_allow_html=True)
                        st.markdown("<div class='img-block'>", unsafe_allow_html=True)
                        st.image(pil_img, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='pair-caption'><b>{uploaded_file.name}</b></div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown("<div class='pair-title grad'>Grad-CAM</div>", unsafe_allow_html=True)
                        heatmap = _gradcam_for_image(pil_img, pred_idx)
                        overlay = overlay_heatmap_on_image(pil_img, heatmap, alpha=0.35)
                        st.markdown("<div class='img-block'>", unsafe_allow_html=True)
                        st.image(overlay, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='pair-caption'><b>{pred_class}</b> — {confidence:.2%}</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Upload an image to get predictions")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown('<div class="section-header">📤 Upload Multiple Images for Batch Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Choose images...", type=['png', 'jpg', 'jpeg', 'bmp'], accept_multiple_files=True)
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} images uploaded")
            if st.button("🔮 Predict All", use_container_width=True, type="primary"):
                st.markdown("### Batch Prediction Results")
                progress_bar = st.progress(0)
                classes = st.session_state.dataset_info['class_names']
                results = []
                for idx, uf in enumerate(uploaded_files):
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                    pil = Image.open(uf).convert("RGB")
                    probs, pred_idx = _predict_probabilities(pil)
                    pred_class = classes[pred_idx]; confidence = float(probs[pred_idx])
                    heatmap = _gradcam_for_image(pil, pred_idx)
                    overlay = overlay_heatmap_on_image(pil, heatmap, alpha=0.35)
                    results.append({"Image": uf.name, "Predicted Class": pred_class, "Confidence": confidence, "Overlay": overlay, "Original": pil})

                results_df = pd.DataFrame([{"Image": r["Image"], "Predicted Class": r["Predicted Class"], "Confidence": r["Confidence"]} for r in results])
                st.dataframe(results_df.style.format({'Confidence':'{:.2%}'}), use_container_width=True)

                st.markdown("### 📊 Prediction Summary")
                csm1, csm2, csm3 = st.columns(3)
                with csm1: st.metric("Total Images", len(results))
                with csm2: st.metric("Average Confidence", f"{float(results_df['Confidence'].mean()):.2%}")
                with csm3: st.metric("High Confidence (>80%)", int((results_df['Confidence'] > 0.8).sum()))

                st.markdown("### 📈 Predicted Class Distribution")
                class_counts = results_df['Predicted Class'].value_counts()
                st.bar_chart(class_counts)

                st.markdown("### 🔥 Grad-CAM Gallery (Original ↔ Grad-CAM)")
                pairs_per_row = 2; cols_per_row = 4
                for i in range(0, len(results), pairs_per_row):
                    cols = st.columns(cols_per_row)
                    for pair_offset in range(pairs_per_row):
                        j = i + pair_offset
                        if j >= len(results): break
                        r = results[j]; is_high = float(r["Confidence"]) > 0.80
                        with cols[pair_offset * 2]:
                            _render_img_block(r["Original"], is_high_conf=is_high, title="Original", caption=f"<b>{r['Image']}</b>")
                        with cols[pair_offset * 2 + 1]:
                            _render_img_block(r["Overlay"], is_high_conf=is_high, title="Grad-CAM", caption=f"<b>{r['Predicted Class']}</b> — {r['Confidence']:.2%}")
        else:
            st.info("👆 Upload multiple images for batch prediction")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Model Performance Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    left, right = st.columns(2)
    history = st.session_state.training_history
    with left:
        best_train_acc = max(history['accuracy']); best_val_acc = max(history['val_accuracy'])
        final_train_ls = history['loss'][-1]; final_val_ls = history['val_loss'][-1]
        st.markdown(
            f"""
            <div class="summary-card"><h4>Training Performance</h4>
              <div class="kv-grid">
                 <div class="kv-item"><div class="kv-label">Best Train Acc</div><div class="kv-value">{best_train_acc:.2%}</div></div>
                 <div class="kv-item"><div class="kv-label">Best Val Acc</div><div class="kv-value">{best_val_acc:.2%}</div></div>
              </div>
              <div class="kv-grid">
                 <div class="kv-item"><div class="kv-label">Final Train Loss</div><div class="kv-value">{final_train_ls:.4f}</div></div>
                 <div class="kv-item"><div class="kv-label">Final Val Loss</div><div class="kv-value">{final_val_ls:.4f}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    with right:
        sel = st.session_state.selected_model; epochs = st.session_state.hyperparameters['epochs']
        train_time = st.session_state.training_time; n_classes = len(st.session_state.dataset_info['class_names'])
        st.markdown(
            f"""
            <div class="summary-card"><h4>Model Configuration</h4>
              <div class="kv-grid">
                <div class="kv-item"><div class="kv-label">Model</div><div class="kv-value">{sel}</div></div>
                <div class="kv-item"><div class="kv-label">Epochs</div><div class="kv-value">{epochs}</div></div>
              </div>
              <div class="kv-grid">
                <div class="kv-item"><div class="kv-label">Training Time</div><div class="kv-value">{train_time:.2f}s</div></div>
                <div class="kv-item"><div class="kv-label">Classes</div><div class="kv-value">{n_classes}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">💾 Export & Download</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Download Model (.h5)", use_container_width=True):
            st.info("💡 This demo button indicates model download. Use the Save Model action above to export.")
    with col2:
        history_df = pd.DataFrame(st.session_state.training_history)
        csv = history_df.to_csv(index=False)
        st.download_button("📥 Download Training History (CSV)", data=csv, file_name="training_history.csv", mime="text/csv", use_container_width=True)
    with col3:
        from deepfoundry.core.plotting import plot_training_curves
        fig = plot_training_curves(st.session_state.training_history)
        buf = BytesIO(); fig.savefig(buf, format='png', dpi=300, bbox_inches='tight'); buf.seek(0)
        st.download_button("📥 Download Training Plots (PNG)", data=buf, file_name="training_plots.png", mime="image/png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    btn_cols = st.columns([1, 1, 1])
    with btn_cols[0]:
        if st.button("← Back to Training", use_container_width=True):
            st.session_state.current_page = 'training'; st.rerun()
    with btn_cols[1]:
        if st.button("🔄 New Training Session", use_container_width=True):
            st.session_state.training_complete = False
            st.session_state.training_history = None
            st.session_state.current_page = 'dataset'; st.rerun()
