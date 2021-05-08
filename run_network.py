import os
import numpy as np 
import argparse
from network_topology import Graph
import json


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Takes .grp folder as input')
    parser.add_argument('--src',
                        help='specify the folder directory eg --src Data/Bascilius',
                        required=True)
    args = parser.parse_args()
    folder_dir = args.src
    all_charc = []
    for files in os.listdir(folder_dir):
        print("Reading Graph : {0}/{1}".format(folder_dir,files))
        g = Graph(root_dir=folder_dir,grp_file=files)
        node_degeres,avg_nodes = g.compute_node_deg()
        strength_dict,avg_strength = g.compute_strength_distibution()
        char_length = g.charestric_path_length()
        cc_coeff  = g.clustering_coeffiecnt(node_degeres)
        charc_dict = {
            "avg_nodes" : avg_nodes,
            "avg_strength" :avg_strength,
            "avg_weight" : g.compute_avg_weight(),
            "char_length" : char_length,
            "cc_coeff" : cc_coeff,
            "condition" : g.check_small_scale_property(avg_nodes,char_length,cc_coeff)
        }
        template_file = "output_template.json"
        data = g.write_characteristics(charc_dict,template_file,files)
        all_charc.append(data)
    with open("output.json",'w') as f:
        json.dump(all_charc,f,indent=2)
    
    
    

    
