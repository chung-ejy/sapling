from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, SGDRegressor, RidgeCV
import pandas as pd
import xgboost as xgb
from xgboost.sklearn import XGBClassifier, XGBRegressor
from catboost import CatBoostRegressor, CatBoostClassifier

import warnings
warnings.filterwarnings(action='ignore')

## Modeling standardizer
class Modeler(object):

    ## standardizes predicting regardless of model, asks for clearly stated factors
    @classmethod
    def predict(self,models,prediction_set,factors):
        factors = [x for x in factors if x != "y" and x != "ticker"]
        for row in models.iterrows():
            try:
                model = row[1]["model"]
                api = row[1]["api"]
                score = row[1]["score"]
                prediction_set[f"{api}_prediction"] = model.predict(prediction_set[factors])
                prediction_set[f"{api}_score"] = score 
            except Exception as e:
                print(str(e))
        prediction_cols = [x for x in prediction_set.columns if "prediction" in x]
        score_cols = [x for x in prediction_set.columns if "score" in x]
        prediction_set["prediction"] = [sum([row[1][x] for x in prediction_cols]) / len(prediction_cols) for row in prediction_set.iterrows()]
        return prediction_set.drop(prediction_cols,axis=1).drop(score_cols,axis=1)

    ## regression standardizer and aggregator, aggregates different modeling apis
    @classmethod
    def regression(self,data):
        results = []
        results.append(self.sk_regression(data))
        results.append(self.xgb_regression(data))
        results.append(self.cat_regression(data))
        df = pd.DataFrame(results)
        df["model_type"] = "regression"
        return df
    
    @classmethod
    def xgb_regression(self,data):
        try:
            params = {
                    "booster":["gbtree","gblinear","dart"]
                      ,"learning_rate":[0.1,0.5,1]
                      }
            X_train, X_test, y_train, y_test = self.shuffle_split(data)
            gs = GridSearchCV(XGBRegressor(objective="reg:squarederror",verbosity = 0),param_grid=params,scoring="r2")
            gs.fit(X_train,y_train)
            predictions = gs.predict(X_test)
            score = r2_score(predictions,y_test)
            model = gs.best_estimator_
            return {"api":"xgb","model":model,"score":score}
        except Exception as e:
            print(str(e))
            return {"api":"xgb","model":str(e),"score":-99999}
    
    @classmethod
    def cat_regression(self,data):
        try:
            params = {"boosting_type":[
                                        "Ordered",
                                        "Plain"
                                        ]}
            X_train, X_test, y_train, y_test = self.shuffle_split(data)
            gs = GridSearchCV(CatBoostRegressor(iterations=100,verbose=False,early_stopping_rounds=3),param_grid=params,scoring="r2")
            gs.fit(X_train,y_train)
            predictions = gs.predict(X_test)
            score = r2_score(predictions,y_test)
            model = gs.best_estimator_
            return {"api":"cat","model":model,"score":score}
        except Exception as e:
            print(str(e))
            return {"api":"cat","model":str(e),"score":-99999}
            
    @classmethod
    def sk_regression(self,data):
        stuff = {
            "sgd" : {"model":SGDRegressor(fit_intercept=True),"params":{"loss":["squared_loss","huber"]
                                                            ,"learning_rate":["constant","optimal","adaptive"]
                                                            ,"alpha" : [0.01, 0.1, 0.2, 0.5, 1]}},
            "r" : {"model":RidgeCV(alphas=[0.01, 0.1, 0.2, 0.5, 1],fit_intercept=True),"params":{}},
            "lr" : {"model":LinearRegression(fit_intercept=True),"params":{"fit_intercept":[True,False]}}
        }
        X_train, X_test, y_train, y_test = self.shuffle_split(data)
        results = []
        for regressor in stuff:
            try:
                model = stuff[regressor]["model"]
                model.fit(X_train,y_train)
                y_pred = model.predict(X_test)
                score = r2_score(y_test,y_pred)
                result = {"api":"skl","model":model,"score":score}
                results.append(result)
            except Exception as e:
                print(str(e))
                results.append({"api":"skl","model":str(e),"score":-99999})
        return pd.DataFrame(results).sort_values("score",ascending=False).iloc[0].to_dict()
    
    @classmethod
    def shuffle_split(self,data):
        X_test = data["X"].iloc[::4]
        X_train = data["X"].drop(index=[x for x in range(0,data["X"].index.size,4)])
        y_test = data["y"].iloc[::4]
        y_train = data["y"].drop(index=[x for x in range(0,data["y"].index.size,4)])
        return [X_train, X_test, y_train, y_test]