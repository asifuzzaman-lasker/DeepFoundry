import matplotlib.pyplot as plt

def plot_training_curves(history_dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#FFFFFF')

    ax1.plot(history_dict['epoch'], history_dict['accuracy'], label='Training Accuracy', linewidth=2)
    ax1.plot(history_dict['epoch'], history_dict['val_accuracy'], label='Validation Accuracy', linewidth=2)
    ax1.set_xlabel('Epoch'); ax1.set_ylabel('Accuracy'); ax1.set_title('Model Accuracy', fontweight='bold')
    ax1.legend(loc='lower right'); ax1.grid(True, alpha=0.25); ax1.set_facecolor('#FAFBFF')

    ax2.plot(history_dict['epoch'], history_dict['loss'], label='Training Loss', linewidth=2)
    ax2.plot(history_dict['epoch'], history_dict['val_loss'], label='Validation Loss', linewidth=2)
    ax2.set_xlabel('Epoch'); ax2.set_ylabel('Loss'); ax2.set_title('Model Loss', fontweight='bold')
    ax2.legend(loc='upper right'); ax2.grid(True, alpha=0.25); ax2.set_facecolor('#FAFBFF')

    plt.tight_layout()
    return fig
