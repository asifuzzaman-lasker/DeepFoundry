import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import streamlit as st

def scan_dataset_folder(folder_path):
    dataset_info = {"total_images": 0, "classes": {}, "class_names": [], "sample_images": {}}
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

    if not os.path.isdir(folder_path):
        st.error("Invalid path. Please provide a valid directory path.")
        return None

    try:
        class_names = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
        if not class_names:
            st.warning("No subdirectories (classes) found in the provided folder.")
            return None

        dataset_info["class_names"] = sorted(class_names)

        for class_name in dataset_info["class_names"]:
            class_path = os.path.join(folder_path, class_name)
            image_files = [f for f in os.listdir(class_path) if f.lower().endswith(valid_extensions)]
            if image_files:
                dataset_info["classes"][class_name] = len(image_files)
                dataset_info["total_images"] += len(image_files)
                sample_paths = [os.path.join(class_path, img) for img in image_files[:5]]
                dataset_info["sample_images"][class_name] = sample_paths

        return dataset_info
    except Exception as e:
        st.error(f"An error occurred while scanning the folder: {e}")
        return None


def create_data_generators(folder_path, split_ratio, batch_size, img_size, augmentation_params):
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=augmentation_params.get('rotation_range', 0) if augmentation_params.get('rotation', False) else 0,
        width_shift_range=augmentation_params.get('shift_range', 0) if augmentation_params.get('shift', False) else 0,
        height_shift_range=augmentation_params.get('shift_range', 0) if augmentation_params.get('shift', False) else 0,
        shear_range=augmentation_params.get('shear_range', 0) if augmentation_params.get('shear', False) else 0,
        zoom_range=augmentation_params.get('zoom_range', 0) if augmentation_params.get('zoom', False) else 0,
        horizontal_flip=augmentation_params.get('horizontal_flip', False),
        vertical_flip=augmentation_params.get('vertical_flip', False),
        brightness_range=[1-augmentation_params.get('brightness_range', 0),
                          1+augmentation_params.get('brightness_range', 0)] if augmentation_params.get('brightness', False) else None,
        validation_split=1 - (split_ratio / 100)
    )

    val_datagen = ImageDataGenerator(rescale=1./255, validation_split=1 - (split_ratio / 100))

    train_generator = train_datagen.flow_from_directory(
        folder_path, target_size=img_size, batch_size=batch_size, class_mode='categorical',
        subset='training', shuffle=True
    )

    validation_generator = val_datagen.flow_from_directory(
        folder_path, target_size=img_size, batch_size=batch_size, class_mode='categorical',
        subset='validation', shuffle=False
    )
    return train_generator, validation_generator
