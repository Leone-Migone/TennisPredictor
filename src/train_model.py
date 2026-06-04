import pandas as pd

from sklearn.model_selection import train_test_split
import sklearn.linear_model as lm
import sklearn.metrics as metrics

def train_baseline_model(model_data):
    features = [
        "rank_diff",
        "age_diff",
        "h2h_diff",
        "h2h_matches",
        "surface",
        "best_of"
    ]

    target = "target"


    x = model_data[features].copy()
    y = model_data[target]

    #convert string columns into numeric
    x = pd.get_dummies(x, columns=["surface"], drop_first=True)

    x_train, x_test, y_train, y_test = train_test_split(
        x,y,test_size=0.2,random_state=1,stratify=y
    )

    model = lm.LogisticRegression(max_iter=1000)

    model.fit(x_train,y_train)
    y_pred = model.predict(x_test)
    accuracy = metrics.accuracy_score(y_test,y_pred)
    
    print("Baseline Logistic Regression with H2H features")
    print("----------------------------")
    print(f"Accuracy: {accuracy:.4f}")
    print()
    print("Confusion Matrix:")
    print(metrics.confusion_matrix(y_test, y_pred))
    print()
    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))

    return model