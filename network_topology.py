import numpy as np 
import random


class Graph():
    def __init__(self,grp_file):
        self.nodes = []
        self.edges = []
        with open(grp_file) as file:
            for s in file.readlines():
                if ')' in s and 'edge' not in s:
                    self.nodes.append(int(s.split(')')[0]))
                elif 'edge' not in s and '*' not in s:
                    self.edges.append((s.split('\n')[0]))
                else:
                    pass
        self.no_nodes = len(self.nodes)
        self.no_edges = len(self.edges)
        self.weight_matrix = np.zeros((self.no_nodes+1,self.no_nodes+1))
        self.adjancey_matrix = np.zeros((self.no_nodes+1,self.no_nodes+1))
        self.populate_matrix()
        self.compute_node_deg()
        self.compute_strength_distibution()
        self.compute_avg_weight()

    def populate_matrix(self):
        for edge in self.edges:
            i = int(edge.split('-')[0])
            j = int(edge.split('-')[1])
            self.adjancey_matrix[i][j] = 1
            self.weight_matrix[i][j] = random.randint(0,10)
        
    def compute_node_deg(self):
        node_dict = {}
        for i in range(self.no_nodes+1):
            node_deg = 0
            for j in range(self.no_nodes+1):
                node_deg += self.adjancey_matrix[i][j]
            node_dict["Node : {0}".format(i)]  = "Degree : {0}".format(node_deg)
        print(node_dict)

    def compute_strength_distibution(self):
        strength_dict = {}
        for i in range(self.no_nodes+1):
            strength = 0
            for j in range(self.no_nodes+1):
                strength += self.adjancey_matrix[i][j] * self.weight_matrix[i][j]
            strength_dict["Node : {0}".format(i)]  = "Strength : {0}".format(strength)
        print(strength_dict)


    def compute_avg_weight(self):
        total_weight = 0
        avg_weight =  {}
        for i in range(self.no_nodes+1):
            for j in range(self.no_nodes+1):
                total_weight += self.weight_matrix[i][j]
        for i  in range(self.no_nodes+1):
            node_weight = 0
            for j in range(self.no_nodes+1):
                node_weight += self.weight_matrix[i][j]
            avg_weight[i]=node_weight/total_weight
        print(avg_weight)
        

    def compute_dis_nodes(self):
        pass

    def compute_betweeness_centrality(self):
        pass

    def check_small_scale_property(self):
        pass

if __name__ == "__main__":
    g = Graph('Data/Bacillus_subtilis_168/-beta--D-glucuronide_degradation.grp')
