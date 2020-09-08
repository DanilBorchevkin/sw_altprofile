# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:55:17 2019
@author: Danil Borchevkin
"""

import xarray as xr
import glob
import os

def process_file(filepath, latitude, longitude, var_name):

    data = []

    current_index = 0

    ds = xr.open_dataset(filepath)

    lat_idx = 0
    long_idx = 0
    lat_found = False
    long_found = False
    # Find latiude inside NetCDF
    for idx, coord in enumerate(ds.coords['latitude'].data):
        if coord == latitude:
            lat_idx = idx
            lat_found = True
            break
    if (lat_found == False):
        print("No latitude found in file")
        return data

    for idx, coord in enumerate(ds.coords['longitude'].data):
        if coord == longitude:
            long_idx = idx
            long_found = True
            break
    if (long_found == False):
        print("No longitude found in file")
        return data
    
    for time in ds.coords['time'].data:
        data.append([
                ds.coords['latitude'].data[lat_idx],
                ds.coords['longitude'].data[long_idx], 
                time])
        for level in ds.coords['level'].data:
            dsloc = ds.sel(latitude=ds.coords['latitude'].data[lat_idx], 
                            longitude=ds.coords['longitude'].data[long_idx], 
                            level=level, 
                            time=time)
            data[current_index].append(dsloc.data_vars[var_name].data.item())

        current_index += 1

    return data

def save_to_ascii_file(data_list, out_filepath, header=[]):
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def main():
    print("Script is started")

    # Change params here
    var_name = 'w'
    latitude = 69.0
    longitude = 0.0

    files = glob.glob("./input/*.*")    

    for filepath in files:
        print("Process >> " + filepath)

        try:
            data_to_save = process_file(filepath, latitude, longitude, var_name)
            out_filepath = "./output/" + os.path.basename(filepath) + ".dat"
            
            if (len(data_to_save) > 0):
                save_to_ascii_file(data_to_save, out_filepath)
                print("Saved to >> " + out_filepath)
            else:
                print("No data for saving. Ignoring")
            
        except:
            print("Cannot process >> ", filepath)
            
        finally:
            print()

    print("Script is finished")

if __name__ == "__main__":
    main()