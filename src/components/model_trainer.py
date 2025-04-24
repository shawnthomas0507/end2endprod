import os 
import sys 
from dataclasses import dataclass
from catboost import CatBoostRegressor

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")


class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig):
        self.model_trainer_config=model_trainer_config
    
    def initiate_model_trainer(self,train_array,test_array,preprocessor_path):

        try:
             X_train,y_train,X_test,y_test=train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]


             models={
                 "LinearRegression":LinearRegression(),
                 "DecisionTreeRegressor":DecisionTreeRegressor(),
                 "RandomForestRegressor":RandomForestRegressor(),
                 "GradientBoostingRegressor":GradientBoostingRegressor(),
                 "KNeighborsRegressor":KNeighborsRegressor(),
                 "XGBRegressor":XGBRegressor(),
                 "AdaBoostRegressor":AdaBoostRegressor(),
                 "CatBoostRegressor":CatBoostRegressor(verbose=False)
             }


             model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models=models)

             best_model_score=max(sorted(model_report.values()))

             best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

             best_model=models[best_model_name]

             if best_model_score<0.6:
                 raise CustomException("No best model found")
             

             save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
             )
             logging.info("Best model found")

             predicted=best_model.predict(X_test)
             r2=r2_score(y_test,predicted)
             print(r2)

        except Exception as e:
            raise CustomException(e,sys) from e

