import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def classify(xt, xv, yt, yv, prep_list):
    var_smoothing_range = range(0, 11)
    dtc_range = range(2, 11)            # for max_depth and min_samples_split
    dtc_mixed_range = range(2,6)        # same but for using both at once
    
    models = []
    results = []

    for vs in var_smoothing_range:
        value = f"1e-{vs}"
        models.append((GaussianNB(var_smoothing=eval(value)), f"GNB var_smoothing={value}"))

    for md in dtc_range:
        models.append((DecisionTreeClassifier(max_depth=md), f"DTC max_depth={md}"))
        models.append((DecisionTreeClassifier(min_samples_split=md), f"DTC min_samples_split={md}"))

    for mixed_md in dtc_mixed_range:
        for mixed_mss in dtc_mixed_range:
            models.append((DecisionTreeClassifier(max_depth=mixed_md, min_samples_split=mixed_mss), f"DTC max_depth={mixed_md} min_samples_split={mixed_mss}"))

    for prep in prep_list:
        xt, xv = prep(xt, xv)
        for model, model_name in models:
            model.fit(xt, yt)
            y_pred_val = model.predict(xv)
            accuracy = accuracy_score(yv, y_pred_val)
            precision = precision_score(yv, y_pred_val, average='weighted', zero_division=1)
            recall = recall_score(yv, y_pred_val, average='weighted', zero_division=1)
            f1 = f1_score(yv, y_pred_val, average='weighted', zero_division=1)
            results.append([f"{model_name} {prep.__name__}", "%.3f" % accuracy, "%.3f" % precision, "%.3f" % recall, "%.3f" % f1])

            # print(classification_report(yv, y_pred_val, zero_division=1))
            # cm = confusion_matrix(yv, y_pred_val)
            # print("Macierz pomyłek:")
            # for row in cm:
            #     print(row)
            # print("\n--------------------------------------\n")

    df = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall", "F1-Score"])
    df.to_csv(R"Lista 4\results.csv", index=False)


def no_processing(training, validation):
    return training, validation

def normalization(training, validation):
    normalizer = Normalizer()
    return normalizer.fit_transform(training), normalizer.transform(validation)

def pca_prep(training, validation):
    pca = PCA()
    return pca.fit_transform(training), pca.transform(validation)

if __name__=="__main__":
    column_names = ['Id', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type']
    data = pd.read_csv("Lista 4\glass.data", names=column_names)
    data.describe()
    X = data.drop(['Id', 'Type'], axis=1)
    y = data['Type']

    train_x, validation_x, train_y, validation_y = train_test_split(X, y, test_size=0.8)

    data_preparation = [no_processing, normalization, pca_prep]

    classify(train_x, validation_x, train_y, validation_y, data_preparation)
    