from os import path
import csv
import can
from scipy.io import savemat
#constants------------------------------------------------------------------------------------
TITLE_1="Timestamp"
TITLE_2="CAN ID"
TITLE_3="Byte0"
TITLE_4="Byte1"
TITLE_5="Byte2"
TITLE_6="Byte3"
TITLE_7="Byte4"
TITLE_8="Byte5"
TITLE_9="Byte6"
TITLE_10="Byte7"

#--------------------------------User defined functions--------------------------------
# (1)---Input assert function
def inputAssert(prompt,min,max):
    userInput=input(prompt)
    while(not userInput.isnumeric() or int(userInput)<min or int(userInput)>max):
        if not userInput.isnumeric():
            print(f"{userInput} is not a valid,please try again...")
        else:
            print("Out of boundary,please try again...")
        userInput=input(prompt)
    return int(userInput)

# (2)---data directory function
def dataDirectory():
    dataPath=input("Enter data file directory, or press 'q' to quit:")
    while(not path.exists(dataPath) or (path.splitext(dataPath))[1]!='.csv'):
        if dataPath=='q':
            return 'q'
        elif not path.exists(dataPath):
            print(f"{dataPath} does not exist")
        else:
            print(f"{dataPath} is not a csv file")
        dataPath=input("Enter dataset file location, or press 'q' to quit:")
    return dataPath

def splitCSV(fileDrectory,chunk_size):
    """
    Splits a CSV file into smaller chunks of specified size.
    
    Parameters:
        fileDrectory (str): Path to the input CSV file.
        chunk_size (int): Number of rows per chunk.
        
    Returns:
        list: List of paths to the split files.
    """
    split_files = []
    with open(fileDrectory, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        chunk = []
        for i, row in enumerate(reader):
            chunk.append(row)
            if (i + 1) % chunk_size == 0:
                split_file_path = f"{fileDrectory}_part_{len(split_files) + 1}.csv"
                with open(split_file_path, "w", newline='') as split_file:
                    writer = csv.writer(split_file)
                    writer.writerow(header)  # Write the header to each split file
                    writer.writerows(chunk)
                split_files.append(split_file_path)
                chunk = []  # Reset the chunk for the next batch
        if chunk:  # Write any remaining rows
            split_file_path = f"{fileDrectory}_part_{len(split_files) + 1}.csv"
            with open(split_file_path, "w", newline='') as split_file:
                writer = csv.writer(split_file)
                writer.writerow(header)  # Write the header to each split file
                writer.writerows(chunk)
            split_files.append(split_file_path)
    return split_files

def dataExtract(fileDrectory):
    """
    Extracts data from a CSV file and returns a list of dictionaries.
    
    Parameters:
        fileDrectory (str): Path to the input CSV file.
    """
    with open(fileDrectory, "r") as file:
        reader = csv.reader(file)
        chunk = []
        for row in enumerate(reader):
            chunk.append([row[1][0],row[1][2],row[1][6],row[1][7],row[1][8],row[1][9],row[1][10],row[1][11],row[1][12],row[1][13]])
        split_file_path = f"{fileDrectory}__processed.csv"
        with open(split_file_path, "w", newline='') as split_file:
            writer = csv.writer(split_file)
            writer.writerows(chunk)
        file.close()
    print("Data extraction completed.")

def messageStatistics(fileDrectory):
    idList=[]
    fileHandle = open(fileDrectory, "r")
    for row in fileHandle.readlines()[1:]:
        itemList=row.split(",")
        idList.append(itemList[1])
    unique_ids = set(idList)
    for can_id in unique_ids:
        print(f"{can_id}: {idList.count(can_id)}")
    fileHandle.close()

def messagePrint(fileDrectory):
    can_id=input("please input a CAN ID:")
    fileHandle = open(fileDrectory, "r")
    for row in fileHandle.readlines()[1:]:
        itemList=row.split(",")
        if can_id in itemList[1]:
            print(row)
    fileHandle.close()

def messagePrintAll(fileDrectory):
    can_id=input("please input a CAN ID:")
    with open(fileDrectory, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if can_id== row[1]:
                print(row)
    file.close()
""""
def blf2mat():
    directory=input("please input the blf file directory:")
    blf_data = []
    with can.BLFReader(directory) as log:
        for msg in log:
            blf_data.append({
                'timestamp': msg.timestamp,
                'arbitration_id': msg.arbitration_id,
                'data': list(msg.data)
            })
    # Convert to .mat
    savemat("processed.mat", {'blf_data': blf_data})
""""
#--------------------------------------main flow----------------------------------------------
#file directory input
filePath=dataDirectory()

while(not filePath=='q'):
    #splitCSV(filePath,200000)
    #messagePrintAll(filePath)
    messageStatistics(filePath)
    #messagePrint(filePath)
    
    filePath=dataDirectory()

