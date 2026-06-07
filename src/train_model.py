import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as metrics
import sklearn as sk

def train_baseline_model(model_data):
    features = [
        "rank_diff",
        "age_diff",
        "h2h_diff",
        "h2h_matches",
        "surface",
        "best_of",
        "rank_points_diff",
        "form_diff",
        "elo_diff"
    ]

    target = "target"
    #rather than splitting data for training randomly doing it cronologically its more logical
    train_data = model_data[model_data["tourney_date"] < 20240101]
    test_data = model_data[model_data["tourney_date"] >= 20240101]

    scaler = StandardScaler()
    
    x_train = train_data[features].copy()
    y_train = train_data[target]

    x_test = test_data[features].copy()
    y_test= test_data[target]

    #convert string columns into numeric
    x_test= pd.get_dummies(x_test, columns=["surface"], drop_first=True)
    x_train = pd.get_dummies(x_train, columns=["surface"], drop_first=True)
    #That ensures the test set has the same columns as the training set.
    x_test = x_test.reindex(columns=x_train.columns, fill_value=0)

    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    #rf_model = sk.ensemble.RandomForestClassifier(n_estimators=100, random_state=1)
    #y_pred = model.predict(x_test)    
    model = sk.linear_model.LogisticRegression(max_iter=100000) 

    model.fit(x_train_scaled, y_train)
    
    
    y_pred = model.predict(x_test_scaled)
    accuracy = metrics.accuracy_score(y_test,y_pred)
    
    print("Baseline Logistic Regression with H2H, rank points difference and recent form")
    print("----------------------------")
    print(f"Accuracy: {accuracy*100:.4f}%")
    print()
    print("Confusion Matrix:")
    print(metrics.confusion_matrix(y_test, y_pred))
    print()
    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))

    return model