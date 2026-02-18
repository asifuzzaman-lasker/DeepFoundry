import numpy as np

def confusion_matrix_from_preds(y_true, y_pred, num_classes):
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    return cm

def compute_metrics_from_cm(cm):
    total = cm.sum()
    correct = np.trace(cm)
    accuracy = correct / total if total else 0.0

    tp = np.diag(cm).astype(float)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp

    with np.errstate(divide='ignore', invalid='ignore'):
        precision_per_class = np.where(tp + fp > 0, tp / (tp + fp), 0.0)
        recall_per_class    = np.where(tp + fn > 0, tp / (tp + fn), 0.0)
        denom               = precision_per_class + recall_per_class
        f1_per_class        = np.where(denom > 0, 2 * precision_per_class * recall_per_class / denom, 0.0)

    precision_macro = float(np.mean(precision_per_class)) if len(tp) else 0.0
    recall_macro    = float(np.mean(recall_per_class)) if len(tp) else 0.0
    f1_macro        = float(np.mean(f1_per_class)) if len(tp) else 0.0

    row_marginals = cm.sum(axis=1)
    col_marginals = cm.sum(axis=0)
    s = float(total)
    c = float(correct)
    p_sq_sum = float(np.sum(col_marginals**2))
    t_sq_sum = float(np.sum(row_marginals**2))
    denom_mcc = np.sqrt((s*s - p_sq_sum) * (s*s - t_sq_sum))
    mcc = ((c * s) - float(np.sum(col_marginals * row_marginals))) / denom_mcc if denom_mcc > 0 else 0.0

    pe = float((row_marginals @ col_marginals) / (total * total)) if total else 0.0
    kappa = (accuracy - pe) / (1 - pe) if (1 - pe) > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "mcc": mcc,
        "kappa": kappa,
        "hamming_loss": (1.0 - accuracy),
    }

def log_loss_from_probs(Y_pred, y_true):
    eps = 1e-15
    N = len(y_true)
    p_true = Y_pred[np.arange(N), y_true]
    p_true = np.clip(p_true, eps, 1.0)
    return float(-np.mean(np.log(p_true))) if N > 0 else float('nan')

def roc_curve_auc_ovr(Y_pred, y_true, max_to_plot=10):
    k = Y_pred.shape[1]
    N = len(y_true)
    y_true_onehot = np.zeros((N, k), dtype=int)
    y_true_onehot[np.arange(N), y_true] = 1

    def roc_auc_binary(y_true_bin, y_score):
        order = np.argsort(-y_score)
        y_true_sorted = y_true_bin[order]
        P = y_true_sorted.sum()
        Nn = len(y_true_sorted) - P
        if P == 0 or Nn == 0:
            return (np.array([0, 1]), np.array([0, 1]), float('nan'))
        tp = np.cumsum(y_true_sorted)
        fp = np.cumsum(1 - y_true_sorted)
        tpr = tp / P
        fpr = fp / Nn
        fpr = np.concatenate(([0.0], fpr, [1.0]))
        tpr = np.concatenate(([0.0], tpr, [1.0]))
        auc = float(np.trapz(tpr, fpr))
        return (fpr, tpr, auc)

    order_by_freq = np.argsort(-np.bincount(y_true, minlength=k))
    return y_true_onehot, order_by_freq, roc_auc_binary
