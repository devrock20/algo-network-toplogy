from __future__ import division
import numpy as np 
import random
import queue
import math
import json
from string import Template
import  os


class Graph():
    def __init__(self,root_dir,grp_file):
        self.nodes = []
        self.edges = []
        relative_path = os.path.join(root_dir,grp_file)
        with open(relative_path) as file:
            for s in file.readlines():
                if ')' in s and 'edge' not in s:
                    self.nodes.append(int(s.split(')')[0]))
                elif 'edge' not in s and '*' not in s:
                    self.edges.append((s.split('\n')[0]))
                else:
                    pass
        self.no_nodes = len(self.nodes)
        self.no_edges = len(self.edges)
        self.adjancey_matrix = np.zeros((self.no_nodes+1,self.no_nodes+1))
        self.populate_matrix()
        
    def populate_matrix(self):
        for edge in self.edges:
            i = int(edge.split('-')[0])
            j = int(edge.split('-')[1])
            self.adjancey_matrix[i][j] = random.randint(1,10)
        #print(self.adjancey_matrix)
        
    def compute_node_deg(self):
        node_dict = {}
        node_sum =  0
        if self.no_nodes == 0:
            return None,None
        for i in range(self.no_nodes+1):
            node_deg = 0
            for j in range(self.no_nodes+1):
                if self.adjancey_matrix[i][j] > 0:
                    node_deg += 1
            node_dict[i]  = node_deg
            node_sum  +=  node_deg
        avg_nodes = node_sum/self.no_nodes
        return node_dict,avg_nodes
        

    def compute_strength_distibution(self):
        strength_dict = {}
        strength_sum =  0
        for i in range(self.no_nodes+1):
            strength = 0
            for j in range(self.no_nodes+1):
                strength += self.adjancey_matrix[i][j]
            strength_dict[i]  = strength
            strength_sum += strength
        avg_strength = strength_sum/self.no_nodes
        return strength_dict,avg_strength

    def compute_avg_weight(self):
        total_weight = 0
        for i in range(self.no_nodes+1):
            for j in range(self.no_nodes+1):
                total_weight += self.adjancey_matrix[i][j]
        node_weight = 0
        for i  in range(self.no_nodes+1):
            for j in range(self.no_nodes+1):
                node_weight += self.adjancey_matrix[i][j]
        avg_weight = node_weight/self.no_edges
        return avg_weight
        

    def compute_distance_between_nodes(self,beg_node):
        unvistied  = queue.Queue()
        unvistied.put(beg_node)
        vistied = []
        each_node_arr = np.full(self.no_nodes+1,np.inf)
        each_node_arr[beg_node] = 0
        while len(vistied) != len(self.nodes):
            node = unvistied.get()
            neighbhors = []
            for j in range(self.no_nodes+1):
                if self.adjancey_matrix[node][j]  > 0:
                    neighbhors.append(j)
            for each in neighbhors:
                dist = each_node_arr[node]  + self.adjancey_matrix[node][each]
                if dist  < each_node_arr[each]:
                    each_node_arr[each] = dist
            vistied.append(node)
            next_node = self.find_min(each_node_arr,vistied)
            unvistied.put(next_node)
        each_node_arr  = np.where(each_node_arr==np.inf,0,each_node_arr)
        return each_node_arr
            

    def find_min(self,array,vistied_nodes):
        array_dict = {}
        for value in np.unique(array):
            array_dict[value]  = np.where(array==value)[0].tolist()
        sorted_array = np.sort(np.delete(array,vistied_nodes))
        min_index =   sorted_array.min()
        for item in array_dict[min_index]:
            if item not in vistied_nodes:
                next_node = item
        return next_node

    def charestric_path_length(self):
        try:
            sum_of_distnaces = 0
            for i in self.nodes:
                sum_of_distnaces  += np.sum(self.compute_distance_between_nodes(i))
            char_path_length = sum_of_distnaces/(self.no_nodes * (self.no_nodes-1))
            return char_path_length
        except Exception as e:
            print("Skipping this metric")


    def clustering_coeffiecnt(self,node_dgerees):
        try:
            cc = 0
            for node,node_deg in node_dgerees.items():
                if node == 0:
                    continue
                k  = node_deg
                neighbors_edges  = 0
                neighbhors = []
                for j in range(self.no_nodes+1):
                    if self.adjancey_matrix[node][j]  > 0:
                        neighbhors.append(j)
                for q in range(len(neighbhors)):
                    for p in range(len(neighbhors)):
                        if self.adjancey_matrix[neighbhors[q]][neighbhors[p]] > 0:
                            neighbors_edges  += 1
                    p = 0
                if neighbors_edges == 0:
                    cc += 0
                else:
                    cc += (2 * neighbors_edges)/(k * (k-1))
            cc_n = cc/self.no_nodes
            return cc_n
        except Exception as e:
            print("Skiping this metric")
            return 0

    def closness_centrality(self):
        closse_ness  = []
        for i in self.nodes:
            closeness = (self.no_nodes -1 )/np.sum(self.compute_distance_between_nodes(i))
            closse_ness.append(closeness)
        return closse_ness

    

    def write_characteristics(self,charc_dict,template_file,graph_name):
        charc_dict['graph_name'] = graph_name
        with  open(template_file,'r') as f:
            t= Template(json.dumps(json.load(f)))
            data = t.safe_substitute(charc_dict)
        return data
        


        
        
            


    
if __name__ == "__main__":
    g = Graph(root_dir= "Data/Bacillus_subtilis_168", grp_file=  "(deoxy)ribose_phosphate_degradation.grp")
