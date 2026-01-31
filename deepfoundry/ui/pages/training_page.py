import io
import time
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import tensorflow as tf

from deepfoundry.constants import MODEL_CONFIGS
from deepfoundry.core.data_loader import create_data_generators
from deepfoundry.core.model_builder import create_real_model
from deepfoundry.core.plotting import plot_training_curves
from deepfoundry.core.metrics import (
    confusion_matrix_from_preds, compute_metrics_from_cm, log_loss_from_probs, roc_curve_auc_ovr
)

def show_training_page():
    if not st.session_state.get('dataset_info') or not st.session_state.get('selected_model'):
        st.error("⚠️ Please configure dataset and model first!")
        if st.button("← Go to Model Configuration"):
            st.session_state.current_page = 'model_&_hyperparameters'; st.rerun()
        return

    info = st.session_state.dataset_info
    hp = st.session_state.hyperparameters
    st.markdown('<div class="section-header blue">📋 Training Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="summary-card">
             <h4>Dataset</h4>
             <div class="stat-chip"><span>Total Images</span><b>{info['total_images']}</b></div>
             <div class="stat-chip"><span>Classes</span><b>{len(info['class_names'])}</b></div>
             <div class="muted-line">Top classes: {', '.join(info['class_names'][:3])}...</div>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        params = MODEL_CONFIGS[st.session_state.selected_model]
        st.markdown(
            f"""
            <div class="summary-card">
             <h4>Model</h4>
             <div class="stat-chip"><span>Architecture</span><b>{st.session_state.selected_model}</b></div>
             <div class="stat-chip"><span>Params</span><b>{params['trainable_params']:,}</b></div>
             <div class="stat-chip"><span>Input</span><b>{params['input_shape'][:2]}</b></div>
            </div>
            """, unsafe_allow_html=True)
    with c3:
        st.markdown(
            f"""
            <div class="summary-card">
             <h4>Hyperparameters</h4>
             <div class="stat-chip"><span>Epochs</span><b>{hp['epochs']}</b></div>
             <div class="stat-chip"><span>Batch Size</span><b>{hp['batch_size']}</b></div>
             <div class="stat-chip"><span>LR</span><b>{hp['learning_rate']}</b></div>
             <div class="stat-chip"><span>Optimizer</span><b>{hp['optimizer']}</b></div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    if not st.session_state.training_complete:
        if st.button("🔴 START TRAINING", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.empty()
            try:
                status_text.text("📁 Loading dataset...")
                train_gen, val_gen = create_data_generators(
                    folder_path=st.session_state.dataset_path,
                    split_ratio=st.session_state.split_value,
                    batch_size=hp['batch_size'],
                    img_size=hp['img_size'],
                    augmentation_params=st.session_state.augmentation_params
                )
                st.session_state.val_generator = val_gen
                progress_bar.progress(0.1)

                status_text.text("🏗️ Building model architecture...")
                model = create_real_model(
                    model_name=st.session_state.selected_model,
                    num_classes=len(info['class_names']),
                    input_shape=MODEL_CONFIGS[st.session_state.selected_model]['input_shape'],
                    learning_rate=hp['learning_rate'],
                    optimizer_name=hp['optimizer']
                )
                st.session_state.tf_model = model
                st.session_state.class_indices = train_gen.class_indices
                progress_bar.progress(0.2)

                class StreamlitCallback(tf.keras.callbacks.Callback):
                    def __init__(self, pb, stx, logc, total):
                        super().__init__()
                        self.pb, self.stx, self.logc, self.total = pb, stx, logc, total
                        self.logs_list = []
                    def on_epoch_end(self, epoch, logs=None):
                        logs = logs or {}
                        progress = 0.2 + (0.8 * (epoch + 1) / self.total)
                        self.pb.progress(progress)
                        msg = (f"Epoch {epoch+1}/{self.total} - Loss: {logs.get('loss',0):.4f}, "
                               f"Acc: {logs.get('accuracy',0):.4f}, Val Loss: {logs.get('val_loss',0):.4f}, "
                               f"Val Acc: {logs.get('val_accuracy',0):.4f}")
                        self.logs_list.append(msg)
                        self.stx.text(f"Training... Epoch {epoch+1}/{self.total}")
                        self.logc.text_area("Training Logs", "\n".join(self.logs_list[-10:]), height=200)

                callbacks_list = [
                    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
                    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7),
                    StreamlitCallback(progress_bar, status_text, log_container, hp['epochs'])
                ]

                status_text.text("🚀 Training started...")
                start_time = time.time()
                history = model.fit(train_gen, validation_data=val_gen, epochs=hp['epochs'], callbacks=callbacks_list, verbose=0)
                training_time = time.time() - start_time

                st.session_state.training_history = {
                    'epoch': list(range(1, len(history.history['loss']) + 1)),
                    'loss': history.history['loss'],
                    'accuracy': history.history['accuracy'],
                    'val_loss': history.history['val_loss'],
                    'val_accuracy': history.history['val_accuracy']
                }
                st.session_state.training_time = training_time
                st.session_state.training_complete = True

                progress_bar.progress(1.0)
                st.success(f"✅ Training completed in {training_time:.2f} seconds!")
                st.balloons()
                st.rerun()

            except Exception as e:
                st.error(f"❌ Training failed: {str(e)}")
                st.exception(e)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.training_complete:
        history = st.session_state.training_history
        st.markdown('<div class="section-header">📈 Training Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Training Time", f"{st.session_state.training_time:.2f}s")
        with m2: st.metric("Final Train Accuracy", f"{history['accuracy'][-1]:.2%}")
        with m3: st.metric("Final Val Accuracy", f"{history['val_accuracy'][-1]:.2%}")
        with m4: st.metric("Final Val Loss", f"{history['val_loss'][-1]:.4f}")
        fig_curves = plot_training_curves(history)
        st.pyplot(fig_curves)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">🧭 Evaluation Details</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        val_gen = st.session_state.get("val_generator")
        model   = st.session_state.get("tf_model")
        if val_gen is None or model is None:
            st.error("Validation generator or model not found. Please (re)run training.")
        else:
            Y_pred = model.predict(val_gen, verbose=0)
            y_pred_classes = np.argmax(Y_pred, axis=1)
            y_true_classes = val_gen.classes
            class_labels = list(val_gen.class_indices.keys())
            k = len(class_labels); N = len(y_true_classes)

            cm = confusion_matrix_from_preds(y_true_classes, y_pred_classes, k)
            left, right = st.columns([1, 1])
            with left:
                st.markdown("#### Confusion Matrix")
                fig_cm, ax = plt.subplots(figsize=(7, 6))
                im = ax.imshow(cm, cmap="Blues", vmin=0); ax.set_aspect('equal')
                ax.set_xticks(range(k)); ax.set_yticks(range(k))
                ax.set_xticklabels(class_labels, rotation=45, ha='right'); ax.set_yticklabels(class_labels)
                ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title("Confusion Matrix")
                max_val = cm.max() if cm.size else 0
                thresh = max_val / 2.0 if max_val > 0 else 0.5
                for i in range(k):
                    for j in range(k):
                        val = cm[i, j]
                        ax.text(j, i, str(val), ha='center', va='center',
                                fontsize=9, color=("white" if val > thresh else "black"))
                cbar = fig_cm.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.ax.set_ylabel("Count", rotation=270, labelpad=12)
                st.pyplot(fig_cm); plt.close(fig_cm)

            with right:
                st.markdown("#### 📊 Evaluation Results")
                metrics = compute_metrics_from_cm(cm)
                ll = log_loss_from_probs(Y_pred, y_true_classes)
                st.markdown(
                    f"""
                    <div class="eval-metrics-grid">
                      <div class="metric-card"><div class="label">Accuracy</div><div class="value">{metrics['accuracy']:.2%}</div></div>
                      <div class="metric-card"><div class="label">Precision (macro)</div><div class="value">{metrics['precision_macro']:.2%}</div></div>
                      <div class="metric-card"><div class="label">Recall (macro)</div><div class="value">{metrics['recall_macro']:.2%}</div></div>
                      <div class="metric-card"><div class="label">F1-score (macro)</div><div class="value">{metrics['f1_macro']:.2%}</div></div>
                      <div class="metric-card"><div class="label">Cohen’s κ</div><div class="value">{metrics['kappa']:.3f}</div></div>
                      <div class="metric-card"><div class="label">MCC</div><div class="value">{metrics['mcc']:.3f}</div></div>
                      <div class="metric-card"><div class="label">Hamming Loss</div><div class="value">{metrics['hamming_loss']:.3f}</div></div>
                      <div class="metric-card"><div class="label">Log Loss</div><div class="value">{ll:.3f}</div></div>
                    </div>
                    """, unsafe_allow_html=True
                )

            left2, right2 = st.columns([1, 1])
            with left2:
                st.markdown("#### 📋 Epoch-wise Training Logs")
                df = pd.DataFrame(history)
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Download Logs CSV", data=csv, file_name="training_history.csv", mime="text/csv", use_container_width=True)
            with right2:
                st.markdown("#### ROC–AUC (One-vs-Rest)")
                if k < 2:
                    st.info("ROC curves require at least 2 classes.")
                else:
                    y_onehot, order_by_freq, roc_auc_binary = roc_curve_auc_ovr(Y_pred, y_true_classes)
                    max_to_plot = min(k, 10)
                    fig_roc, axr = plt.subplots(figsize=(7.5, 6))
                    aucs = []
                    for ci in order_by_freq[:max_to_plot]:
                        fpr, tpr, auc_c = roc_auc_binary(y_onehot[:, ci], Y_pred[:, ci])
                        aucs.append(auc_c)
                        label = f"{class_labels[ci]} (AUC={auc_c:.2f})" if auc_c == auc_c else f"{class_labels[ci]} (AUC=NA)"
                        axr.plot(fpr, tpr, label=label, linewidth=1.8)
                    macro_auc = float(np.nanmean(aucs)) if len(aucs) else float('nan')
                    axr.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
                    title = f"ROC–AUC (macro≈{macro_auc:.2f})" if macro_auc == macro_auc else "ROC–AUC"
                    axr.set_title(title); axr.set_xlabel("False Positive Rate"); axr.set_ylabel("True Positive Rate")
                    axr.set_xlim(0, 1); axr.set_ylim(0, 1); axr.grid(True, alpha=.25)
                    axr.legend(loc="lower right", fontsize=9, frameon=True, bbox_to_anchor=(1.02, 0.5), framealpha=0.9, borderaxespad=0.8)
                    st.pyplot(fig_roc); plt.close(fig_roc)

        st.markdown('<div class="section-header">💾 Save Model</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            model_name = st.text_input("Model Name", value=f"{st.session_state.selected_model}_model")
        with c2:
            if st.button("Save Model (.h5)", use_container_width=True):
                st.session_state.tf_model.save(f"{model_name}.h5")
                st.success(f"✅ Model saved as {model_name}.h5")
        st.markdown('</div>', unsafe_allow_html=True)

        btn_cols = st.columns([1, 1, 1])
        with btn_cols[0]:
            if st.button("← Back to Model", use_container_width=True):
                st.session_state.current_page = 'model_&_hyperparameters'; st.rerun()
        with btn_cols[2]:
            if st.button("Next: Inference →", use_container_width=True, type="primary"):
                st.session_state.current_page = 'inference'; st.rerun()
