
import pandas as pd
import numpy as np
import threading
import copy

import general as GENFUNC
import constants as CONST



class DataProcessor():
    def __init__(self, inputs, data_lock, info_lock) -> None:
        self.inputs = inputs
        self.data_lock = data_lock # mutex for accessing the data directory

        self.info_lock = info_lock # lock for controlling its running information
        self.shut_down = False
        return
    
    def dataThread(self):

        while True:
            self.info_lock.acquire()
            if self.shut_down:
                self.info_lock.release()
                break
            self.info_lock.release()
            
            self.inputs.lock.acquire()
            areas = copy.copy(self.inputs.areas)
            self.inputs.lock.release()

            for area in areas:
                file_name = CONST.DATA_DIRECTORY + GENFUNC.location_convert(area) + ".csv"

                df = pd.read_csv(file_name)

                result_df = self.getHousesBelowAverage(df)



        return
    

    def startThread(self):
        data_thread = threading.Thread(target=self.dataThread, args=[])
        data_thread.start()

        return data_thread
    

    def getHousesBelowAverage(self, df):
        dataframe = df
        # clean up and standardize units
        dataframe = self.acreToSqft(dataframe)
        # dataframe = dataframe.dropna()

        # create the two value needed to be compared to, if livingArea is not available, use NaN
        dataframe["livinglotratio"] = np.where(dataframe["livingArea"] > 0, dataframe["livingArea"] / dataframe["lotAreaValue"], np.nan)
        dataframe["unitprice"] = np.where(dataframe["livingArea"] > 0, dataframe["price"] / dataframe["livingArea"], np.nan)

        average_llr = dataframe.loc[:, 'livinglotratio'].mean()
        average_unit_price = dataframe.loc[:, 'unitprice'].mean()

        df_below_r = self.belowAverageRatio(dataframe, average_llr)
        df_below_up = self.belowAverageUnitPrice(dataframe, average_unit_price)

        dataframe = pd.concat([df_below_r, df_below_up]).drop_duplicates()

        return dataframe


    def acreToSqft(self, df):
        df.loc[df["lotAreaUnit"] == "acres", "lotAreaValue"] = df["lotAreaValue"] * CONST.SQFT_IN_ACRE
        df.loc[df["lotAreaUnit"] == "acres", "lotAreaUnit"] = "sqft"
        return df
    
    def belowAverageRatio(self, df, average_ratio):
        result = df[df["livinglotratio"] <= average_ratio]
        return result

    def belowAverageUnitPrice(self, df, average_unit_price):
        result = df[df["unitprice"] <= average_unit_price]
        return result

    

