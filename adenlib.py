# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 19:37:50 2024

@author: Aden Mann
@copyright©: Aden Mann, AMSolutions ©
"""

## Dependencies:
from matplotlib import pyplot as plt
import numpy as np
import scipy as scp
from math import sqrt
import json
import copy

class adentools():
            
    def csv_reader(filename): # Operates through a CSV with given filename.
        ''' - Reads through a csv and returns a list of the lines of the csv.
            - This function will not work where there are proximal doubleline 
              indicators.'''
        file = open(filename, 'r')  
        raw_data = file.read()
        list_data = raw_data.split('\n')
        return list_data
    
    def csv_writer(filename, string):
        ''' - Writes list of list to csv'''
        with open('filename', 'w') as file:
            file.write(string)
    
    def empty_remover(data):  # Removes empty indexes from inputted list.
        ''' - Removes empty indices from inputted list and returns pruned list.'''
        for i in range(len(data)):
            if ',,' in data[i]:
                data[i] = 'empty'
            elif data[i] == ['']:
                data[i] = 'empty'
        while 'empty' in data:
            data.remove('empty')
        return data
    
    def data_splitter(data):
        ''' - splits comma string by comma/''s and outputs a list'''
        for i in range(len(data)):
            data[i] = data[i].split(',')
        return data
    
    def graphscatter(x,y,title='no title', xlabel='no x-label', ylabel='no y-label'
                     ,color='green'):
        ''' - This function graphs a scatterplot with inputted x and y lists 
            - Title Color, and Axes Labels can be inputted.'''
        fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
        ax.scatter(x, y, color=color, label='Data Points')
        
        # Adding labels and title with larger font sizes for readability
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, fontsize=14)

        # Customize tick labels for better readability
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Add grid for readability and style improvements
        ax.grid(True)

        # Display the legend
        ax.legend(fontsize=12)

        # Show the plot on screen
        plt.show()
    
    def rolling_avg(data):
        ''' - This function creates a rolling average which is the average of all 
              of the points which lead up to the current value of interation'''
        rolling_output = []
        for i in range(len(data)):
            i += 1
            sub_avg = sum(data[0:i])/len(data[0:i])
            rolling_output.append(sub_avg)
        return rolling_output
    
    def rolling_stdev(data,uncertainties):
        ''' - This function creates a rolling standard deviation based on the rolling averages 
              of the points which lead up to the current value of iteration.'''
        ''' This function is deprecated.'''
        rolling_avg_output= []
        rolling_stdev_output = []
        rolling_stder_output= []
        for i in range(len(data)):
            if i<30:
                #print('aden',i)
                i+=1
                uncpsu = uncertainties[0]
                uncdaq = uncertainties[1]
                uncsys = np.sqrt(uncpsu**2+uncdaq**2)
                #print(uncsys)
                rolling_stder = np.sqrt(i)/i*(uncsys)
                rolling_stder_output.append(rolling_stder)
                #print(rolling_stder)
            else:
                i+=1
                sub_data = data[29:i]
                sub_avg = np.mean(sub_data)
                rolling_avg_output.append(sub_avg)
                rolling_stdev = np.std(sub_data, ddof=1)
                rolling_stdev_output.append(rolling_stdev)  
                rolling_stder = rolling_stdev / sqrt(len(rolling_stdev_output))  # Forumla for stderr
                rolling_stder_output.append(rolling_stder)
                static_stder = np.std(data, ddof=1)/sqrt(len(data))
        return [rolling_avg_output, rolling_stdev_output, rolling_stder_output,static_stder]
            
    def filename_tool(filenames,string):
        '''Finds filenames in an inputted list of filenames which include an
           inputted string and outputs their index.'''
        in_indices = []  # My string in the filename
        notin_indices = []  # My string not in the filename
        for i in range(len(filenames)):
            if string in filenames[i]:
                in_indices.append(i)
            else:
                notin_indices.append(i)
        return notin_indices, in_indices
    
    def samplemaker(data):
        ''' - Creates a "sample" datapoint for every index in an inputted list.'''
        samples = []
        for i in range(len(data)):
            sample = i+1
            samples.append(sample)
        return samples
    
    
    def lpam(mylist,index,datatype='Float',type_='Column'):  # Pulls items at set index from a list and appends to a new list.
        ''' Pulls objects from sublist at index i in a list of lists,
            this function operates through an entire list.'''
        
        newlist = []
        mylist = copy.copy(mylist)
        
        ## Column (Default)
        if type_ == 'Column':
                for i in range(len(mylist)):
                    if datatype=='Float':
                        try:
                            newlist.append(float(mylist[i][index]))
                        except:
                            pass
                    elif datatype=='String':
                        newlist.append(str(mylist[i][index]))
        
        ## Row (Optional)
        elif type_ == 'Row':
            for i in range(len(mylist[index])):
                if datatype=='Float':
                    try:
                        newlist.append(float(mylist[index][i]))
                    except:
                        pass
                elif datatype=='String':
                    newlist.append(str(mylist[index[i]]))
        return newlist## Files to index and important values:
    
    def finite_differences(numerators,denominators):
        ''' Computes the finite differences for an inputted list of numerators
            and an inputted list of denominators, returns a single list.'''
        output = []
        if numerators == denominators:
            print("Error: Dataset length not equal.")
        else:
            for i in range(len(numerators)-1):
                numerator         = numerators[i+1]-numerators[i]
                denominator       = denominators[i+1]-denominators[i]
                finite_difference = numerator / denominator
                output.append(finite_difference)
        return output
                
class vectortools():
    def vector_magnitude(vector):
        '''Computes the magnitude of an inputted vector in list form
           e.g. <x,y> or <x,y,z>'''
        if len(vector) == 2:
            magnitude = sqrt(vector[0]**2,vector[1]**2)
        elif len(vector) == 3:
            magnitude = sqrt(vector[0]**2,vector[1]**2,vector[2]**2)
        return magnitude
    def mass_magnitude(list1):
        ''' Computes the magnitude of a list of list component vectors'''
        magnitudes = []
        if len(list1) == 2:
            for i in range(len(list1[0])):
                magnitude = sqrt(list1[0][i]**2 + list1[1][i]**2)
                magnitudes.append(magnitude)
        elif len(list1) == 3:
            for i in range(len(list1[0])):
                magnitude = sqrt(list1[0][i]**2 + list1[1][i]**2 + list1[2][i]**2)
                magnitudes.append(magnitude)
        return magnitudes
            
                
            
    def vector_plot(x_data, y_data, magnitudes, log=False):
        """
        Generates a quiver plot of the supplied data.
        No return.
        Copyright Texas A&M University
        """
        # Plot setup
        plt.ion()
        fig, ax = plt.subplots()
        # Generate vector plot
        pivot = "mid"
        title = "Vector Field"
        if log:
            title += " (lengths log scaled)"
        q = ax.quiver(x_data, y_data, magnitudes, pivot=pivot)
        # ax.set_xlabel("CNC Y-axis (steps)")
        # ax.set_ylabel("CNC X-axis (steps)")
        ax.set_title(title)
        # Add colorbar
        cbar = plt.colorbar(q)
        cbar.set_label("Vector magnitude", rotation=90)
        # Display plot
        plt.pause(0.1)
        plt.draw()
        # Save image
        filename = input("Enter a filename to save the plot: ")
        filename += "_vector_plot.png"
        print("Saving plot to {}".format(filename))
        fig.savefig(filename)
        # Cleanup
        plt.clf()
        plt.close()

from pathlib import Path
import os

class input_tools():
    def check_for_directory(folder):
        '''check program's directory for some file of interest.'''
        program_directory = Path.cwd()
        content = os.listdir(program_directory)
        while True:
            if folder in content:
                base_message = "{:<20} was detected in this program's directory."
                #print(f"/{sub_folder}/ was detected in /{primary_folder}/ in this program's directory")
                print(base_message.format(f"/{folder}/"))
                break
            elif folder not in content:
                print(f'/{folder}/ is not detected?')
                cancel = input('Stop Program (Y/N)?: ')
                if cancel == 'Y':
                    break
                else:
                    pass
            
    def check_for_subdirectory(primary_folder, sub_folder):
        ''' check a known subdirectory from the viewpoint of the program for 
            some file of interest. '''
        program_directory = Path.cwd()
        pfolder_path = program_directory / primary_folder
        
        # Does the primary folder exist?
        if not pfolder_path.exists() or not pfolder_path.is_dir():
            print(f"/{primary_folder}/ does not exist.")
            while True:
                if pfolder_path.exists():
                    print(f'/{primary_folder}/ detected.')
                    break
                else:
                    print(f'/{primary_folder}/ is not detected.')
                    cancel = input('Stop Program (Y/N)?: ')
                    if cancel == 'Y':
                        break
                    else:
                        pass
        sfolder_path = pfolder_path / sub_folder
        if not sfolder_path.exists() or not sfolder_path.is_dir():
            print(f"Folder /{sub_folder}/ does not exist.")
            while True:
                if sfolder_path.exists():
                    print(f'/{sub_folder}/ detected in {primary_folder}.')
                    break
                else:
                    print(f'{sub_folder} is not detected in {primary_folder}.')
                    cancel = input('Stop Program (Y/N)?: ')
                    if cancel == 'Y':
                        break
                    else:
                        pass
        else:
            base_message = "{:<11} was detected in {:<9} in this program's directory."
            #print(f"/{sub_folder}/ was detected in /{primary_folder}/ in this program's directory")
            print(base_message.format(f"/{sub_folder}/", f"/{primary_folder}/"))
        return sfolder_path
    
    def check_for_subdirectory_custompath(pfolder_path,primary_folder,sub_folder):
        '''Check a known subdirectory with known path that is somewhere in the 
           viewpoint of the program for some folder of interest.'''
        sfolder_path = pfolder_path / sub_folder
        # Does the primary folder exist?
        if not pfolder_path.exists() or not pfolder_path.is_dir():
            print(f"/{primary_folder}/ does not exist.")
            while True:
                if pfolder_path.exists():
                    print(f'/{primary_folder}/ detected.')
                    break               
                else:
                    print(f'/{primary_folder}/ is not detected.')
                    cancel = input('Stop Program (Y/N)?: ')
                    if cancel == 'Y':
                        break
                    else:
                        pass
        sfolder_path = pfolder_path / sub_folder
        if not sfolder_path.exists() or not sfolder_path.is_dir():
            print(f"Folder /{sub_folder}/ does not exist.")
            while True:
                if sfolder_path.exists():
                    print(f'/{sub_folder}/ detected in {primary_folder}.')
                    break
                else:
                    print(f'{sub_folder} is not detected in {primary_folder}.')
                    cancel = input('Stop Program (Y/N)?: ')
                    if cancel == 'Y':
                        break
                    else:
                        pass
        else:
            base_message = "{:<11} was detected in {:<9} in {:<9} this program's directory."
            #print(f"/{sub_folder}/ was detected in /{primary_folder}/ in this program's directory")
            print(base_message.format(f"/{sub_folder}/", f"/{primary_folder}/",f"/{pfolder_path.parent.name}/"))
        return sfolder_path
    
    def check_for_files_custompath(pfolder_path,primary_folder,sub_folder):
        '''Check a known subdirectory with known path that is somewhere in the 
           viewpoint of the program for some folder of interest.'''
        sfolder_path = pfolder_path / sub_folder
        # Does the primary folder exist?
        base_message = "{:<30} was detected in {:<9} in {:<9} this program's directory."
        #print(f"/{sub_folder}/ was detected in /{primary_folder}/ in this program's directory")
        print(base_message.format(f"/{sub_folder}/", f"/{primary_folder}/",f"/{pfolder_path.parent.name}/"))
        return sfolder_path
    
    #def peek_in_subdirectory_custompath
    #def listfilesfrompath(path):
    
   # def 
        
        
#class spt_tools():
#    def readfromjson(filename):
#        data = json.load(filename)
#        return data
        
   
        
        
## Deprecated:
def listpullandmake(mylist,index,datatype='Float'):  # Pulls items at set index from a list and appends to a new list.
    ''' Pulls objects from sublist at index i in a list of lists,
        this function operates through an entire list.'''
    newlist = []
    mylist = copy.copy(mylist)
    for i in range(len(mylist)):
        if datatype=='Float':
            newlist.append(float(mylist[i][index]))
        elif datatype=='String':
            newlist.append(str(mylist[i][index]))
    return newlist## Files to index and important values:
   