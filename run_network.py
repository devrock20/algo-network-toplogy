import os
import numpy as np 
import argparse
from network_topology import Graph


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Takes .grp folder as input')
    parser.add_argument('--src',
                        help='specify the folder directory')
    args = parser.parse_args()
    folder_dir = args.src
    grp_files = os.listdir(folder_dir)
    for file in grp_files:
        print("Reading Graph {0}/{1}".format(folder_dir/file))
        graph = Graph(file)
    
