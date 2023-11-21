from xgboost import XGBRegressor
import warnings
warnings.simplefilter(action="ignore")
class Modeler(object):

    @classmethod
    def checkpoint(self,strategy):
        if strategy.isai == True:
            simulation = strategy.retrieve_model_data()
            model = XGBRegressor(booster="dart",learning_rate=1)
            training_data = simulation[(simulation["date"]>strategy.model_start) & (simulation["date"]<strategy.model_end)]
            prediction_data = simulation[(simulation["date"]>strategy.backtest_start) & (simulation["date"]<strategy.backtest_end)]
            model.fit(training_data[strategy.factors],training_data["y"])
            prediction_data["prediction"] = model.predict(prediction_data[strategy.factors])
            strategy.drop_simulation()
            strategy.store_simulation(prediction_data.drop(strategy.factors,axis=1).drop("y",axis=1))
        else:
            simulation = strategy.retrieve_model_data()
            strategy.drop_simulation()
            strategy.store_simulation(simulation)