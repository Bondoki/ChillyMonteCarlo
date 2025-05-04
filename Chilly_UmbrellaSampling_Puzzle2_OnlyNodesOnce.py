from collections import deque, defaultdict
from itertools import permutations
import copy
import numpy as np

# Define the grid for puzzle 2
data = [
      "OY #    $ Y$Y",
      " X          Y",
      "  T # T   $O ",
      " T       T  T",
      "#Y   #  TT# #",
      "Y T $    Y ##",
      "      Y T $  ",
      "TT   Y  Y#Y T",
      " $ #    # $  ",
      "  $ # Y   T  ",
      "T    T     P#",
      "  Y $  Y T  Y"
]

# Function to create the graph based on WSAD movement with longest empty cells and periodic boundaries
def create_graph(data):
    # Create a list to hold the coordinates of empty fields and '$'
    valid_fields = []
    
    # Parse the grid and find valid fields
    # ' ': empty
    # '$': egg
    # 'P': player
    # 'O': wormhole
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == ' ' or data[r][c] == '$' or data[r][c] == 'P' or data[r][c] == 'O':
                valid_fields.append((r, c))
    
    # Create a graph as a dictionary
    graph = defaultdict(list)
    
    # Directions for WSAD movement (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (row_change, col_change)

    # Create connections based on longest WSAD movement with periodic boundaries
    for r, c in valid_fields: # Possible start positions: ' ', '$', 'P', 'O'
        for dr, dc in directions:
            # Start from the current position
            nr, nc = r, c
            traversed_nodes = []  # To collect all traversed nodes
            
            # Move in the direction until hitting a wall or non-empty cell
            while True:
                nr += dr
                nc += dc
                
                # Apply periodic boundary conditions
                nr = nr % len(data)  # Wrap around rows
                nc = nc % len(data[nr])  # Wrap around columns

                # Check if the new position is valid
                # (empty or '$', 'P', 'O') 
                if data[nr][nc] == ' ' or data[nr][nc] == '$' or data[nr][nc] == 'P':
                    traversed_nodes.append(f'({nr}, {nc})')  # Collect traversed node
                    continue  # Keep moving in this direction
                elif data[nr][nc] == 'X'  or data[nr][nc] == 'O':
                    # hit the exit 'X' or wormhole -> stops the move
                    nr += dr
                    nc += dc
                    
                    # Apply periodic boundary conditions
                    nr = nr % len(data)  # Wrap around rows
                    nc = nc % len(data[nr])  # Wrap around columns
                    traversed_nodes.append(f'({nr}, {nc})')  # Collect traversed node
                    break
                else:
                    break  # Hit a wall 'YT#' or non-empty cell
            
            
            # If we moved at least one step, connect to the last valid cell found
            # but neglecting the starting one
            # Note the periodic boundary conditions
            last_valid_cell = ((nr - dr)% len(data), (nc - dc)% len(data[nr]))
            #if (nr - dr, nc - dc) in valid_fields and (nr - dr, nc - dc) != (r, c):
            # Collect the direction information and all traversed nodes
            # Note that traversed_nodes[:-1] exclude the last node (destination)
            if last_valid_cell != (r, c):
                if (dr, dc) == (-1, 0):
                  graph[str((r, c))].append((str(last_valid_cell), 'U', traversed_nodes[:-1]))
                elif (dr, dc) == (1, 0):
                  graph[str((r, c))].append((str(last_valid_cell), 'D', traversed_nodes[:-1]))
                elif (dr, dc) == (0, -1):
                  graph[str((r, c))].append((str(last_valid_cell), 'L', traversed_nodes[:-1]))
                elif (dr, dc) == (0, 1):
                  graph[str((r, c))].append((str(last_valid_cell), 'R', traversed_nodes[:-1]))
    
    return graph

# Function to find all wormholes in the grid
def find_wormholes(data):
    wormholes = []
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 'O':
                wormholes.append(str((r, c)))
    return wormholes

# Function to find the player location in the grid
def find_player(data):
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 'P':
                return str((r, c))
    return None

# Function to find the exit in the grid
def find_exit(data):
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 'X':
                return str((r, c))
    return None

# Function to find the eggs in the grid
def find_eggs(data):
    eggs = []
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == '$':
                eggs.append(str((r, c)))
    return eggs

# Function to replace destination cells in the graph based on the provided mapping synchronously
def replace_wormhole_destinations(graph, mapping):
    # Create a new graph to hold the updated edges
    new_graph = defaultdict(list)
    
    # Iterate through each node in the original graph
    for node, edges in graph.items():
        for destination, direction, traversed_nodes in edges:
            # Check if the destination is in the mapping
            if destination in mapping:
                # Replace the destination with the mapped value
                new_destination = mapping[destination]
                new_graph[node].append((new_destination, direction, traversed_nodes))
            else:
                new_graph[node].append((destination, direction, traversed_nodes))
    
    # Replace the original graph with the new graph
    return new_graph

# Print the graph
#for node, edges in graph.items():
#    print(f"Node {node} connects to: {edges}")

# Find and print all wormholes
#wormholes = find_wormholes(data)
#print("Wormholes found at:", wormholes)

# Mapping for wormhole destinations
wormhole_mapping = {
    '(0, 0)': '(2, 11)',
    '(2, 11)': '(0, 0)'
}


# Create the graph
graph = create_graph(data)


# Replace wormhole destinations in the graph using the mapping synchronously
updated_graph = replace_wormhole_destinations(graph, wormhole_mapping)

# Print the updated graph
for node, edges in updated_graph.items():
    print(f"Node {node} connects to: {edges}")

print()
# Perform the Monte Carlo walk
start_node = find_player(data) 
end_node = find_exit(data)
print(f"Start {start_node} to exit {end_node}")

# Find the egg positions
egg_nodes = find_eggs(data)
print(f"Eggs: {egg_nodes}")

print("##############################################")
print("Brute Force Monte Carlo With Umbrella Sampling")
print("##############################################")
import random

def bias(L, L0, k):
    return 0.5 * k * (L - L0)**2

def monte_carlo_walk(graph, start_node, end_node, exact_steps, all_egg_positions):
    current_node = start_node
    #visited_edges = set()  # To keep track of visited edges
    path = [current_node]  # To store the path taken
    visited_node = set()  # To keep track of visited node
    
    all_traversed_nodes_path = [start_node]
    

    tmp_path_length = 1#len(path)+1
    
    hist = {}
    sweeps_per_check = 100000
    k = 0.005
    L0 = 33  # bias target
    
    while True:
      for sweep in range(sweeps_per_check):
        if sweep == 0:
            print(hist)
        
        # Get the possible moves from the current node
        possible_moves = graph[current_node]
        
        # Filter out moves that would revisit an edge
        #valid_moves = [move for move in possible_moves if (current_node, move[0]) not in visited_edges]
        
        # Filter out moves that would revisit an node
        valid_moves = [move for move in possible_moves if move[0] not in visited_node]
        # Decide whether to move or reverse the last move
        # Move or if no valid move, then reject every time
        if random.random() > 1.0/(len(valid_moves) + 1):
            # Randomly select a valid move
            next_node = random.choice(valid_moves)[0]
            
            # try the new path
            tmp_new_path_length = len(path)-1 
            
            deltaU = bias(tmp_new_path_length, L0, k) - bias(tmp_path_length, L0, k)
            
            if np.random.rand() < np.exp(-deltaU):
                tmp_path_length = tmp_new_path_length
            else:
                hist[tmp_path_length] = hist.get(tmp_path_length, 0) + 1
                continue

            hist[tmp_new_path_length] = hist.get(tmp_new_path_length, 0) + 1
            
            # Count how many items in all_egg_positions are in all_traversed_nodes_path
            count = sum(1 for item in all_egg_positions if item in all_traversed_nodes_path)
            
            # Mark the edge as visited
            #visited_edges.add((current_node, next_node))
            
            # Mark the node as visited
            visited_node.add(next_node)
            
            # Update the traversed nodes for the edge
            for i, (destination, direction, traversed) in enumerate(graph[current_node]):
                if destination == next_node:
                    # Add the traversed_nodes to the traversed set (implicit no double counting)
                    for item in traversed:
                        #unique_traversed_nodes.add(item)
                        all_traversed_nodes_path.append(item)
                    # Add the destination node
                    #unique_traversed_nodes.add(destination)
                    all_traversed_nodes_path.append(destination)
            
            
            
            # Move to the next node
            path.append(next_node)
            current_node = next_node
            
            
                    
            # Check for end-condition
            if current_node == end_node and (len(path)-1) >= exact_steps:
                # Check if all elements of Eggs are in All_traversed_nodes
                if all(item in all_traversed_nodes_path for item in all_egg_positions):
                  return path, all_traversed_nodes_path
        else:
            # No valid moves left, reverse the last move or if diced so
            if len(path) > 1:  # Ensure there is a previous node to go back to
                last_node = path[-2]  # Get the last node
                current_node = path[-1] 
                # Mark the edge as unvisited (reverse the last move)
                #print('visited_edges', visited_edges)
                #visited_edges.remove((last_node, current_node))
                
                # Mark the node as unvisited (reverse the last move)
                #print('visited nodes', visited_node, 'now remove', current_node)
                visited_node.remove(current_node)
                #
                # Update the traversed nodes for the edge when reversing
                for i, (destination, direction, traversed) in enumerate(graph[last_node]):
                    if destination == current_node:
                        # Remove the destination node
                        #unique_traversed_nodes.remove(destination)
                        all_traversed_nodes_path.pop()#(destination)
                        # Remove the last node from the traversed list if present
                        for item in traversed:
                            #unique_traversed_nodes.remove(item)
                            all_traversed_nodes_path.pop() #remove(item)
                        
                        
                current_node = last_node  # Move back to the last node
                path.pop()  # Remove the last node from the path
                tmp_path_length = len(path)-1
      

    return path, all_traversed_nodes_path


minimum_steps = 33  # Number of minimal steps to take
result_path, all_traversed_nodes = monte_carlo_walk(updated_graph, start_node, end_node, minimum_steps, egg_nodes)

# Print the result
print("Path taken:", result_path, " with length: ", len(result_path)-1)
print("All traversed nodes:", all_traversed_nodes, " with length: ", len(all_traversed_nodes)-1)

# Print the properties of the edges in the path
solution_string = ""
for i in range(len(result_path) - 1):
    node_from = result_path[i]
    node_to = result_path[i + 1]
    # Find the property of the edge
    edge_property = next((prop for neighbor, prop, traversed_tiles in updated_graph[node_from] if neighbor == node_to), None)
    #print(f"Edge from {node_from} to {node_to} has property: {edge_property}")
    solution_string += edge_property

print((len(result_path)-1), "steps:", solution_string)

# Puzzle 2
# 33 steps: UDUDLURLULULRDULRURLDRDULRULDLDRL # Umbrella
# 37 steps: UDDULDURLDULDULRDULRULDLRDULRULRDLDRL  # Umbrella
# 40 steps: UDUDLDURLDULDULRDULRURLUDLRDULRULRDRLDRL # Umbrella
