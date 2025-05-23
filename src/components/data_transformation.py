import sys 
from dataclasses import dataclass
import os 
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging  
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig):
        self.data_transformation_config=data_transformation_config


    def get_data_transformer_object(self):
        try:
            numerical_columns=["writing score","reading score"]
            categorical_columns=[
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course"
            ]

            numerical_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])

            cat_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("onehotencoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ])


            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipeline",numerical_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            preprocessing=self.get_data_transformer_object()

            target_column_name="math score"
            numerical_columns=["writing score","reading score"]
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]


            input_features_train_arr=preprocessing.fit_transform(input_feature_train_df)

            input_features_test_arr=preprocessing.transform(input_feature_test_df)


            train_arr=np.c_[input_features_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_features_test_arr,np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing
            )

            logging.info("data transformation done")
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            ) 
        except Exception as e:
            raise CustomException(e,sys)