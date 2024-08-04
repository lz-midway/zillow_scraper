
import pandas as pd
import numpy as np
import threading
import copy
import time

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
        process_data = True

        slept_cycle = 0

        while True:
            self.info_lock.acquire()
            if self.shut_down:
                self.info_lock.release()
                break
            self.info_lock.release()
            
            self.inputs.lock.acquire()
            areas = copy.copy(self.inputs.areas)
            to_change = copy.copy(self.inputs.to_change)
            self.inputs.lock.release()

            if to_change and process_data: # if there is update and need to process new scraped data
                print("processor updating")
                result_dfs = []

                # iterate through each area
                for area in areas:
                    file_name = CONST.DATA_DIRECTORY + GENFUNC.location_convert(area) + ".csv"

                    df = pd.read_csv(file_name)

                    result_df = self.getHousesBelowAverage(df)
                    # sort by unitprice, then livinglotratio, then get head amount
                    result_df = result_df.sort_values(by=['unitprice','livinglotratio']).head(CONST.HEAD)

                    result_dfs.append(result_df)

                self.writeFilteredData(result_dfs, CONST.DATA_DIRECTORY + CONST.READIED_DATA)

                self.inputs.lock.acquire()
                self.inputs.to_change = False
                self.inputs.to_send_email = True
                self.inputs.lock.release()

                process_data = False
                slept_cycle = 0

            else: # sleep when there is nothing to do
                print("processor sleeping")
                time.sleep(CONST.SLEEP_CYCLE_TIME)
                slept_cycle += 1

                if slept_cycle > CONST.DATAPROCESS_SLEEP_CYCLE:
                    process_data = True


        return
    

    # Task functions are not to be used at the sametime with the threads
    def dataTask(self):
        # for running regular timed tasks using a scheduler
        
        self.inputs.lock.acquire()
        areas = copy.copy(self.inputs.areas)
        to_change = copy.copy(self.inputs.to_change)
        input_changed = copy.copy(self.inputs.input_changed)
        self.inputs.lock.release()

        if to_change and not input_changed: # if there is update and need to process new scraped data, and input configuration is not changed
            print("processor updating")
            result_dfs = []

            # iterate through each area
            for area in areas:
                file_name = CONST.DATA_DIRECTORY + GENFUNC.location_convert(area) + ".csv"

                df = pd.read_csv(file_name, dtype=CONST.column_dtype)

                result_df = self.getHousesBelowAverage(df)
                # sort by unitprice, then livinglotratio, then get head amount
                result_df = result_df.sort_values(by=['unitprice','livinglotratio']).head(CONST.HEAD)

                result_dfs.append(result_df)

            self.writeFilteredData(result_dfs, CONST.DATA_DIRECTORY + CONST.READIED_DATA)

            self.inputs.lock.acquire()
            self.inputs.to_change = False
            self.inputs.to_send_email = True
            self.inputs.lock.release()

        else:
            # sleep
            print("nothing to do, processor sleeping")

        return
            
    

    def startThread(self):
        data_thread = threading.Thread(target=self.dataThread, args=[])
        data_thread.start()

        return data_thread
    

    def writeFilteredData(self, result_dfs, file_name):
        self.data_lock.acquire()
        with open(file_name, "w") as file:
            for df in result_dfs:
                file.write(df.to_string())
                file.write("\n\n")
        self.data_lock.release()
        return
    

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

    

