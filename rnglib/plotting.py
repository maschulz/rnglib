from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve


def plot_roc(data):
    """
    plot receiver operating characteristic

    :param data: [(predictions, classes, name), ... ]
    """
    plt.figure()
    lw = 2

    for predictions, classes, name in data:
        fpr, tpr, thresholds = roc_curve(classes, predictions)
        roc_auc = roc_auc_score(classes, predictions)

        plt.plot(fpr, tpr,
                 lw=lw, label='%s (area = %0.3f)' % (name, roc_auc))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()
