# Eric Liu

# TODO

import openpyxl
import datetime
import os

def get_path(relative_path):
    """
    Returns an absolute path from the root of the project directory based on the input relative
    path

    :param:     relative_path   The relative path to convert to an absolute path
    :return:    str             The relative path as an absolute path
    """
    # get the absolute path
    abs_path = os.path.abspath(relative_path)

    # for some reason, if the input path is a directory, then the trailing "\" is removed
    if(os.path.isdir(abs_path)):
        abs_path += "\\"

    # return the path
    return abs_path

def check_directory(path):
    """
    Check if the input path (relative or absolute) exists and is a directory. If the input path
    is relative, it is assumed to be relative to the root of the project directory. If the path
    does not exist, it is created. If the path exists as a file, an error is thrown. If the path 
    exists as a directory, nothing is done

    :param:     path    The path to check 
    """
    # convert to absolute path
    path = get_path(path)

    # check that the path exists and is not a directory
    if(os.path.exists(path) and not os.path.isdir(path)):
        # raise an error indicitating that the path exists as a file and not a directory
        raise FileExistsError("Save path \"" + path + 
            "\" exists as a file and not a directory already")
    # check that the path does not exist
    elif(not os.path.exists(path)):
        # create the directory
        os.mkdir(path)
    # check that the path exists and is a directory
    elif(os.path.exists(path) and os.path.isdir(path)):
        # do nothing
        pass

def get_workbook(tickers):
    """
    Create an xl workbook using openpyxl and create the sheets in the workbook based on the input
    tickers

    :param:     tickers     A list containing all tickers

    :return:    Workbook    A Workbook created by openpyxl containing a sheet for every stock
    """
    # create the Workbook
    wb = openpyxl.Workbook()

    # add each ticker as a sheet in the wb
    for i in range(0, len(tickers)):
        # remove whitespace, tabs, and newlines
        sheet_title = "".join(tickers[i].split())

        # add the sheet to the wb
        wb.create_sheet(sheet_title, i + 1)

    # remove the original default sheet
    wb.remove_sheet(wb.get_sheet_by_name("Sheet"))

    # return the wb
    return wb

def save(wb, save_location):
    """
    Save the input workbook at the specified location. This saves using the filename:
    "option_analysis_{today's date}.xlsx"

    :param:     wb              The workbook to save
    :param:     save_location   The location at which to save. This should be a directory, and not
                                a file
    """
    try:
        # attempt to save at the requested location
        wb.save(save_location + "option_analysis_" + str(datetime.date.today()) + ".xlsx")
    except PermissionError:
        # raise an error if the file is currently open
        raise PermissionError("File cannot be saved since it is open. Close the file and run again")
