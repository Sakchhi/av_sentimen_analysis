import pickle

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB


def get_predictions(train_data, train_labels, test_data):
    mnb_model = MultinomialNB()
    mnb_model.fit(train_data, train_labels)
    predictions = mnb_model.predict(test_data)

    pickle.dump(mnb_model, open('models/20200115_mnb_bow_v0.4.pickle', 'wb'))
    return predictions


if __name__ == '__main__':
    df_bow = pd.read_csv('Data/train/bag_of_words_v0.4.csv')
    df_train = pd.read_csv('Data/train/train.csv')
    # X_train, X_val, y_train, y_val = train_test_split(df_bow, df_train.label, test_size=0.2)

    negative_label_indices = df_train[df_train.label == 0].index
    sample_size = sum(df_train.label == 1)
    random_indices = np.random.choice(negative_label_indices, sample_size, replace=False)
    negative_sample = df_bow.loc[random_indices]
    negative_label_sample = df_train.loc[random_indices]

    y_pred = get_predictions(df_bow, df_train.label, df_bow)

    accuracy_score = metrics.accuracy_score(df_train.label, y_pred)
    print(accuracy_score)

    cm = metrics.confusion_matrix(df_train.label, y_pred)
    tp, fn, fp, tn = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
    print("FPR = {}".format(fp / (fp + tn)))
    print("TPR = {}".format(tp / (tp + fn)))

    f1 = metrics.f1_score(df_train.label, y_pred)
    print("F1 Score = {}".format(f1))
