import os 
print(os.getcwd())
from src.exception import CustomException
from src.logger import logging 
import os 
import sys
import pandas as pd 

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformationConfig, DataTransformation
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','data.csv')



class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        self.ingestion_config=data_ingestion_config
    
    def initiate_data_ingestion(self):
        logging.info("entered data ingestion component")

        try:
            df=pd.read_csv('C:\\Users\\shawn\\OneDrive\\Desktop\\Krish Naik MLOPS\\e2e3\\notebook\\data\\StudentsPerformance.csv')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")

            train_set,test_set=train_test_split(df,test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)


            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                                        )

        except Exception as e:
            raise CustomException(e,sys)



if __name__=="__main__":
    data_ingestion_config=DataIngestionConfig()
    data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
    train_data,test_data=data_ingestion.initiate_data_ingestion()

    data_transformation_config=DataTransformationConfig()
    data_transformation=DataTransformation(data_transformation_config=data_transformation_config)
    train_arr,test_arr,preprocessor_path=data_transformation.initiate_data_transformation(train_data,test_data) 

    model_trainer_config=ModelTrainerConfig()
    model_trainer=ModelTrainer(model_trainer_config=model_trainer_config)
    model_trainer.initiate_model_trainer(train_arr,test_arr,preprocessor_path)


    
    


   