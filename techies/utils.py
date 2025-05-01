from typing import List, Tuple, Dict, Set

def topology_sort_partial(vertices: List[str], edges: List[Tuple[str, str]], start: str):
    """
    Perform a partial topological sort of the graph starting from the specified vertex.
    
    Args:
        vertices: List of vertex names
        edges: List of (from, to) edges
        start: Starting vertex for the partial sort
        
    Returns:
        List of topologically sorted vertices reachable from start
        
    Raises:
        ValueError: If start vertex is not in the graph or if a cycle is detected
    """
    # Check if start vertex exists
    if start not in vertices:
        raise ValueError(f"Start vertex '{start}' not found in graph")
    
    # Build adjacency list
    graph: Dict[str, List[str]] = {v: [] for v in vertices}
    for from_v, to_v in edges:
        if from_v in graph:
            graph[from_v].append(to_v)
    
    result = []  # Sorted result
    visited: Set[str] = set()  # Vertices that have been fully processed
    temp_visited: Set[str] = set()  # Vertices being processed in current DFS
    
    def dfs(vertex: str):
        """
        Depth-first search with cycle detection.
        """
        if vertex in temp_visited:
            # We've found a cycle
            cycle_path = " -> ".join(list(temp_visited) + [vertex])
            raise ValueError(f"Cycle detected in graph: {cycle_path}")
        
        if vertex in visited:
            return
        
        temp_visited.add(vertex)
        
        # Visit all neighbors
        for neighbor in graph.get(vertex, []):
            dfs(neighbor)
        
        # Mark as fully visited and add to result
        temp_visited.remove(vertex)
        visited.add(vertex)
        result.append(vertex)
    
    # Start DFS from the start vertex
    dfs(start)
    
    # Reverse to get topological order
    return result[::-1]

def is_topology_ordered(edges: List[Tuple[str, str]], array: List[str]) -> bool:
    """
    Check if the given array respects the topological ordering defined by the edges.
    
    Args:
        edges: List of (from, to) edges representing dependencies
        array: List of vertex names to check for topological ordering
        
    Returns:
        bool: True if the array is topologically ordered according to the edges, False otherwise
    """
    # Create a mapping from vertex name to its position in the array
    if not array:
        return True
        
    position = {vertex: index for index, vertex in enumerate(array)}
    
    # Check if every edge (from, to) has from before to in the array
    for from_v, to_v in edges:
        # Skip edges with vertices not in the array
        if from_v not in position or to_v not in position:
            continue
            
        # Check if from_v comes before to_v in the array
        if position[from_v] >= position[to_v]:
            return False
            
    return True 