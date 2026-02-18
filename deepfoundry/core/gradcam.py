import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf

def _last_conv_layer(model):
    for layer in reversed(model.layers):
        try:
            if len(layer.output_shape) == 4:
                return layer.name
        except Exception:
            continue
    return None

def compute_gradcam_tf(model, pil_img, class_index, target_size=(224, 224), target_layer_name=None):
    if model is None:
        return None
    try:
        img = pil_img.convert("RGB").resize(target_size, Image.LANCZOS)
        arr = np.asarray(img).astype("float32") / 255.0
        arr = np.expand_dims(arr, axis=0)

        last_conv_name = target_layer_name or _last_conv_layer(model)
        if not last_conv_name:
            return None
        conv_layer = model.get_layer(last_conv_name)
        grad_model = tf.keras.models.Model([model.inputs], [conv_layer.output, model.output])

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(arr)
            if class_index is None:
                class_index = int(tf.argmax(predictions[0]))
            class_channel = predictions[:, class_index]

        grads = tape.gradient(class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-12)
        return heatmap.numpy()
    except Exception:
        return None

def compute_gradcam_fallback(pil_img, target_size=(224, 224)):
    gray = np.asarray(pil_img.convert("L").resize(target_size, Image.LANCZOS), dtype=np.float32) / 255.0
    gy, gx = np.gradient(gray)
    mag = np.sqrt(gx * gx + gy * gy)
    mag = (mag - mag.min()) / (mag.max() - mag.min() + 1e-12)
    return mag

def overlay_heatmap_on_image(pil_img, heatmap, alpha=0.35):
    if heatmap is None:
        return pil_img
    heatmap = np.uint8(255 * np.clip(heatmap, 0, 1))
    cmap = plt.get_cmap("jet")
    colored = cmap(heatmap)[..., :3]
    colored = np.uint8(colored * 255)
    heat_img = Image.fromarray(colored).resize(pil_img.size, Image.BILINEAR)
    overlay = Image.blend(pil_img.convert("RGB"), heat_img.convert("RGB"), alpha)
    return overlay
