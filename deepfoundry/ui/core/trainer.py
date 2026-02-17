import time
import streamlit as st
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, Callback

class StreamlitCallback(Callback):
    def __init__(self, progress_bar, status_text, log_container, total_epochs):
        super().__init__()
        self.progress_bar = progress_bar
        self.status_text = status_text
        self.log_container = log_container
        self.total_epochs = total_epochs
        self.logs_list = []

    def on_epoch_end(self, epoch, logs=None):
        progress = 0.2 + (0.8 * (epoch + 1) / self.total_epochs)
        self.progress_bar.progress(progress)
        logs = logs or {}
        log_msg = (
            f"Epoch {epoch+1}/{self.total_epochs} - "
            f"Loss: {logs.get('loss', 0):.4f}, "
            f"Acc: {logs.get('accuracy', 0):.4f}, "
            f"Val Loss: {logs.get('val_loss', 0):.4f}, "
            f"Val Acc: {logs.get('val_accuracy', 0):.4f}"
        )
        self.logs_list.append(log_msg)
        self.status_text.text(f"Training... Epoch {epoch+1}/{self.total_epochs}")
        self.log_container.text_area("Training Logs", "\n".join(self.logs_list[-10:]), height=200)

def train(model, train_gen, val_gen, epochs, ui_hooks=True):
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7),
    ]
    start = time.time()
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=callbacks, verbose=0)
    duration = time.time() - start
    return history, duration
