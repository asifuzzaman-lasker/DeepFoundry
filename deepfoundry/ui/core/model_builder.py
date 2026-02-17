from tensorflow.keras import models, layers
from tensorflow.keras.applications import (
    VGG16, VGG19, ResNet50, ResNet101, InceptionV3,
    EfficientNetB0, EfficientNetB3, MobileNetV2, DenseNet121, Xception
)
from tensorflow import keras

MODEL_DICT = {
    'VGG16': VGG16, 
    'VGG19': VGG19, 
    'ResNet50': ResNet50, 
    'ResNet101': ResNet101,
    'InceptionV3': InceptionV3, 
    'EfficientNetB0': EfficientNetB0, 
    'EfficientNetB3': EfficientNetB3,
    'MobileNetV2': MobileNetV2, 
    'DenseNet121': DenseNet121, 
    'Xception': Xception
}

def create_real_model(model_name, num_classes, input_shape, learning_rate, optimizer_name):
    base_model = MODEL_DICT[model_name](include_top=False, weights='imagenet', input_shape=input_shape)
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

    optimizer_map = {
        'Adam': keras.optimizers.Adam(learning_rate=learning_rate),
        'SGD': keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9),
        'RMSprop': keras.optimizers.RMSprop(learning_rate=learning_rate),
        'Adagrad': keras.optimizers.Adagrad(learning_rate=learning_rate),
        'Adadelta': keras.optimizers.Adadelta(learning_rate=learning_rate),
        'Adamax': keras.optimizers.Adamax(learning_rate=learning_rate)
    }

    model.compile(
        optimizer=optimizer_map.get(optimizer_name, keras.optimizers.Adam(learning_rate=learning_rate)),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
