# Author: Andrew Kim
# Version: 1.0.0 19 June 2023
# CSV writing handler

import csv

class Writer:
    FILEPATH = "./data/data.csv"

    # truncates file for new session
    @staticmethod
    def truncate():
        file = open(Writer.FILEPATH, 'w')
        file.truncate()
        file.close()


    # appends data of new reading
    @staticmethod
    def append_reading(new_reading):
        contents = [str(reading) for reading in new_reading]
        with open(Writer.FILEPATH, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(contents)