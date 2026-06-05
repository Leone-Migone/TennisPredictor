import pandas as pd

from sklearn.model_selection import train_test_split
import sklearn as sk 
import sklearn.metrics as metrics

def train_baseline_model(model_data):
    features = [
        "rank_diff",
        "age_diff",
        "h2h_diff",
        "h2h_matches",
        "surface",
        "best_of",
        "rank_points_diff"
    ]

    target = "target"
    #rather than splitting data for training randomly doing it cronologically its more logical
    train_data = model_data[model_data["tourney_date"] < 20220101]
    test_data = model_data[model_data["tourney_date"] >= 20220101]

    x_train = train_data[features].copy()
    y_train = train_data[target]

    x_test = test_data[features].copy()
    y_test= test_data[target]

    #convert string columns into numeric
    x_test= pd.get_dummies(x_test, columns=["surface"], drop_first=True)
    x_train = pd.get_dummies(x_train, columns=["surface"], drop_first=True)
    #That ensures the test set has the same columns as the training set.
    x_test = x_test.reindex(columns=x_train.columns, fill_value=0)
    #rf_model = sk.ensemble.RandomForestClassifier(n_estimators=100, random_state=1)
    #rf_model.fit(x_train, y_train)
    #y_pred = rf_model.predict(x_test)    
    model = sk.linear_model.LogisticRegression(max_iter=1000)

    model.fit(x_train,y_train)
    y_pred = model.predict(x_test)
    accuracy = metrics.accuracy_score(y_test,y_pred)
    
    print("Baseline Logistic Regression with H2H and rank points difference")
    print("----------------------------")
    print(f"Accuracy: {accuracy*100:.4f}%")
    print()
    print("Confusion Matrix:")
    print(metrics.confusion_matrix(y_test, y_pred))
    print()
    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))

    return model