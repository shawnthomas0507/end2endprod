import logging
import os 
from datetime import datetime
from exception import CustomException
import sys


LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)




LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)






"""
when i write name==main that means im saying run the code in this block
only if the file is run directly and not id its imported as a module somewhere else.
"""
