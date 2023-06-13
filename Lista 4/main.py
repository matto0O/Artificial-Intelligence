import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

"""
Data preparing functions
"""
def no_preparing(training, validation):
    return training, validation

def normalization(training, validation):
    normalizer = Normalizer()
    return normalizer.fit_transform(training), normalizer.transform(validation)

def pca_prep(training, validation):
    pca = PCA()
    return pca.fit_transform(training), pca.transform(validation)

"""
Classifying method
"""

def classify(xt, xv, yt, yv, prep_list):
    var_smoothing_range = range(0, 11)
    dtc_range = range(2, 11)            # for max_depth and min_samples_split
    dtc_mixed_range = range(2,6)        # same but for using both at once
    
    models = []
    results = []

    for vs in var_smoothing_range:
        value = f"1e-{vs}"
        models.append((GaussianNB(var_smoothing=eval(value)), f"GNB vs={value}", 1))

    for md in dtc_range:
        models.append((DecisionTreeClassifier(max_depth=md, random_state=10), f"DTC md={md}", 2))

    for mss in dtc_range:
        models.append((DecisionTreeClassifier(min_samples_split=mss, random_state=10), f"DTC mss={mss}", 3))

    for mixed_md in dtc_mixed_range:
        for mixed_mss in dtc_mixed_range:
            models.append((DecisionTreeClassifier(max_depth=mixed_md, min_samples_split=mixed_mss, random_state=10), f"DTC md={mixed_md} mss={mixed_mss}", 4))

    for prep in prep_list:
        xt, xv = prep(xt, xv)
        part_results = []
        for model, model_name, model_group in models:
            model_copy = model
            model_copy.fit(xt, yt)
            y_pred_val = model_copy.predict(xv)
            accuracy = accuracy_score(yv, y_pred_val)
            precision = precision_score(yv, y_pred_val, average='weighted', zero_division=1)
            recall = recall_score(yv, y_pred_val, average='weighted', zero_division=1)
            f1 = f1_score(yv, y_pred_val, average='weighted', zero_division=1)
            part_results.append([model_name, prep.__name__, model_group, confusion_matrix(yv, y_pred_val), accuracy.round(3), precision.round(3), recall.round(3), f1.round(3)])
        results += part_results

        f1_values = tuple(map(lambda x: x[-1],part_results))
        labels = tuple(map(lambda x: x[0],part_results))
        y_pos = np.arange(len(part_results))
        
        plt.figure(figsize=(10,5))
        plt.bar(y_pos,f1_values)
        plt.xticks(y_pos, labels, rotation=90)
        plt.xlabel("Model")
        plt.ylabel("F1 score")
        plt.ylim(0.25, 0.65)
        plt.title(prep.__name__)
        plt.show()

    ordered_models = tuple(sorted(results, key=lambda x: x[-1], reverse=True))
    for i in range(1, 5):
        best_in_group = tuple(filter(lambda x: x[2]==i, ordered_models))[0]
        best_in_group_matrix = best_in_group[3]
        sns.heatmap(best_in_group_matrix, annot=True, cbar=False, linewidths=0.5)
        plt.title(f"Confusion matrix - {best_in_group[0]} {best_in_group[1]}")
        plt.show()

    results = tuple(map(lambda x: x[:2]+x[4:], results))

    df = pd.DataFrame(results, columns=["Model", "Preparation", "Accuracy", "Precision", "Recall", "F1-Score"])
    df.to_csv(R"Lista 4\results.csv", index=False)

if __name__=="__main__":
    column_names = ['Id', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type']
    data = pd.read_csv("Lista 4\glass.data", names=column_names)
    data.describe()
    X = data.drop(['Id', 'Type'], axis=1)
    y = data['Type']

    train_x, validation_x, train_y, validation_y = train_test_split(X, y, test_size=0.8)

    data_preparation = [no_preparing, normalization, pca_prep]

    classify(train_x, validation_x, train_y, validation_y, data_preparation)
    