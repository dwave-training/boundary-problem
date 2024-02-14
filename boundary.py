# Copyright 2024 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel, Binary

from helpers import build_graph, draw_solution, draw_boundary

# TODO:  Add code here to define your Binary Quadratic Model (BQM)
def build_bqm(G):
    """Returns a BinaryQuadraticModel.

    Args:
        G(NetworkX graph): weighted graph of image
    """

    bqm = BinaryQuadraticModel('BINARY')

    # Initialize variables
    x = {(i,j): Binary((i,j)) for (i,j) in G.nodes}

    # Add BQM construction here
    for (a,b) in G.edges:

        # TODO: Objective terms for every edge
        

        # TODO: Objective terms if the endpoints are the same color
        

    # print(bqm)
    
    return bqm

# TODO:  Choose QPU parameters in the following function
def run_on_qpu(bqm, sampler):
    """Runs the BQM on the sampler provided.

    Args:
        bqm(BinaryQuadraticModel): a representation of a BQM
        sampler(dimod.Sampler): a sampler that uses the QPU
    """

    chainstrength = 1 # update
    numruns = 1 # update

    sample_set = sampler.sample(bqm, chain_strength=chainstrength, num_reads=numruns, label='Training - Boundary Problem')

    return sample_set

## ------- Main program -------
if __name__ == "__main__":

    ## ------- Set up our image grid -------
    img = [[0,0,0],[1,0,1],[1,1,1]]

    ## ------- Build the graph -------
    G = build_graph(img)

    ## ------- Set up our QUBO dictionary -------

    bqm = build_bqm(G)

    ## ------- Run our QUBO on the QPU -------

    sampler = EmbeddingComposite(DWaveSampler())

    sample_set = run_on_qpu(bqm, sampler)
    sample = sample_set.first.sample

    draw_solution(sample, G)

    draw_boundary(sample, G, img)
