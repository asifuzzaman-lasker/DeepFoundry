MODEL_CONFIGS = {
    "VGG16":      {"input_shape": (224, 224, 3), "trainable_params": 14714688, "non_trainable_params": 0, "description": "16-layer deep network, good for transfer learning"},
    "VGG19":      {"input_shape": (224, 224, 3), "trainable_params": 20024384, "non_trainable_params": 0, "description": "Deeper version of VGG16"},
    "ResNet50":   {"input_shape": (224, 224, 3), "trainable_params": 23587712, "non_trainable_params": 53120, "description": "50-layer residual network, excellent for image classification"},
    "ResNet101":  {"input_shape": (224, 224, 3), "trainable_params": 42658176, "non_trainable_params": 90112, "description": "101-layer residual network"},
    "InceptionV3":{"input_shape": (299, 299, 3), "trainable_params": 21802784, "non_trainable_params": 48896, "description": "Efficient multi-scale feature extraction"},
    "EfficientNetB0":{"input_shape": (224, 224, 3), "trainable_params": 4049571, "non_trainable_params": 7794, "description": "Highly efficient, balanced model"},
    "EfficientNetB3":{"input_shape": (300, 300, 3), "trainable_params": 10783535, "non_trainable_params": 22674, "description": "Larger EfficientNet variant"},
    "MobileNetV2":{"input_shape": (224, 224, 3), "trainable_params": 2257984, "non_trainable_params": 3136, "description": "Lightweight model for mobile deployment"},
    "DenseNet121":{"input_shape": (224, 224, 3), "trainable_params": 7037504, "non_trainable_params": 31360, "description": "Dense connections between layers"},
    "Xception":   {"input_shape": (299, 299, 3), "trainable_params": 20861480, "non_trainable_params": 54144, "description": "Extreme version of Inception"},
}
OPTIMIZERS = ["Adam", "SGD", "RMSprop", "Adagrad", "Adadelta", "Adamax"]
