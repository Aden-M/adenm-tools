__version__ = "1.0"
"""
Script for generating vector field plots. 

Expected inputs are two CSVs of gridded data of the same size.
One should contain all of the vector x components.
Onc should contain all of the vector y components.
This was modified by Aden Mann for fair use educational purposeses.
Send copyright complaints if any to adenmann@tamu.edu 
"""

from math import exp, log
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

print("Program modified by Aden Mann.")
print("Warning!")
print("The plots outputted by this program are flipped in the x step direction compared to run magnet scan!")
print("The top left datapoint is set to 0 as it does not load properly, if this concerns you, edit the code.")
print("This tool does not include provisioning for axis titles or title changes, edit the code to change this.")
print()
def load_grid_data():
    """Loads in the data from user inputs.
    Returns x_data and y_data.
    """
    
    print("* Specify the CSVs containing your vector component data *")
    # X values
    while True:
        resp = input("Data for VS y: ")
        try:
            x_data = np.genfromtxt(resp, delimiter=",")
            x_data[0,0] = 0
        except Exception as err:
            print("Unable to load data:", err)
        else:
            break
    # Y values
    while True:
        resp = input("Data for VS x: ")
        try:
            y_data = np.genfromtxt(resp, delimiter=",")
            y_data[0,0] = 0
        except Exception as err:
            print("Unable to load data:", err)
        else:
            break
    # Check that data sets are the same
    if np.shape(x_data) != np.shape(y_data):
        print("X-data and Y-data are not the same shape and size")
        exit()
    return x_data, y_data


def scale_data(x_data, y_data, factor=1000):
    """
    Applies a log scale to the x and y data.
    The factor determines the spread of the final scaled magnitudes.
    Returns the scaled data and calculated magnitudes.
    """
    # Calculate magnitudes
    magnitudes = np.sqrt(x_data ** 2 + y_data ** 2)
    # Linearly map magnitudes
    # factor = exp(factor)
    largest = np.max(magnitudes)
    smallest = np.min(magnitudes)
    linear_map = (magnitudes - smallest) * ((factor - 1) / (largest - smallest)) + 1
    # Logarithmically scale magnitudes
    scaled_magnitudes = np.log(linear_map)
    scale_factor = np.divide(
        scaled_magnitudes,
        magnitudes,
        out=np.zeros_like(magnitudes),
        where=magnitudes != 0,
    )
    # Apply the scaling to the x and y components
    scaled_x = scale_factor * x_data
    scaled_y = scale_factor * y_data
    # Return
    return scaled_x, scaled_y, magnitudes


def plot_data(x_data, y_data, magnitudes, log=False):
    """
    Generates a quiver plot of the supplied data.
    No return.
    """
    dpimod = int(input("Input DPI (Output Resolution per inch) (200-800 recommended): "))
    print('Resolution is not applied to images in an IDE, only in the output file!')
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
    fig.savefig(filename, dpi=dpimod)
    # Cleanup
    plt.clf()
    plt.close()


if __name__ == "__main__":
    x_data, y_data = load_grid_data()
    while True:
        response = input("Apply log scale to data? (y/n): ").rstrip()
        if response.lower() == "y":
            scaled_x, scaled_y, magnitudes = scale_data(x_data, y_data)
            plot_data(scaled_x, scaled_y, magnitudes, log=True)
            break
        elif response.lower() == "n":
            magnitudes = np.sqrt(x_data ** 2 + y_data ** 2)
            plot_data(x_data, y_data, magnitudes)
            break
        else:
            print("Enter 'y' or 'n'")
