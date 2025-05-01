import pytest
from techies.utils import topology_sort_partial, is_topology_ordered

def test_topology_sort_basic():
    """Test basic functionality with a simple directed acyclic graph."""
    vertices = ["A", "B", "C", "D", "E"]
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
    
    # Starting from A should include all vertices
    result = topology_sort_partial(vertices, edges, "A")
    assert len(result) == 5
    assert result[0] == "A"
    assert result[-1] == "E"
    # Check relative ordering
    assert result.index("B") < result.index("D")
    assert result.index("C") < result.index("D")
    assert result.index("D") < result.index("E")
    
    # Starting from B should include B, D, E
    result = topology_sort_partial(vertices, edges, "B")
    assert set(result) == {"B", "D", "E"}
    assert result[0] == "B"
    assert result[-1] == "E"
    assert result.index("B") < result.index("D") < result.index("E")
    
    # Starting from E should include only E
    result = topology_sort_partial(vertices, edges, "E")
    assert result == ["E"]

def test_topology_sort_single_node():
    """Test with a graph containing a single node."""
    vertices = ["A"]
    edges = []
    
    result = topology_sort_partial(vertices, edges, "A")
    assert result == ["A"]

def test_topology_sort_disconnected():
    """Test with a disconnected graph."""
    vertices = ["A", "B", "C", "D", "E"]
    edges = [("A", "B"), ("C", "D"), ("D", "E")]
    
    # Starting from A should include only A and B
    result = topology_sort_partial(vertices, edges, "A")
    assert set(result) == {"A", "B"}
    assert result[0] == "A"
    assert result[1] == "B"
    
    # Starting from C should include C, D, E
    result = topology_sort_partial(vertices, edges, "C")
    assert set(result) == {"C", "D", "E"}
    assert result.index("C") < result.index("D") < result.index("E")

def test_topology_sort_nonexistent_start():
    """Test error when start node doesn't exist."""
    vertices = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C")]
    
    with pytest.raises(ValueError) as excinfo:
        topology_sort_partial(vertices, edges, "X")
    assert "not found in graph" in str(excinfo.value)

def test_topology_sort_cycle():
    """Test error when a cycle is detected."""
    vertices = ["A", "B", "C", "D"]
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "B")]  # Cycle: B -> C -> D -> B
    
    with pytest.raises(ValueError) as excinfo:
        topology_sort_partial(vertices, edges, "A")
    assert "Cycle detected" in str(excinfo.value)
    
    # Test with self-loop
    vertices = ["A", "B"]
    edges = [("A", "B"), ("B", "B")]  # Self-loop on B
    
    with pytest.raises(ValueError) as excinfo:
        topology_sort_partial(vertices, edges, "A")
    assert "Cycle detected" in str(excinfo.value)

def test_topology_sort_complex():
    """Test with a more complex graph structure."""
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
    edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), 
        ("C", "F"), ("D", "G"), ("E", "G"), ("F", "H")
    ]
    
    result = topology_sort_partial(vertices, edges, "A")
    assert len(result) == 8
    assert result[0] == "A"
    
    # Verify partial ordering constraints
    assert result.index("A") < result.index("B")
    assert result.index("A") < result.index("C")
    assert result.index("B") < result.index("D")
    assert result.index("B") < result.index("E")
    assert result.index("C") < result.index("F")
    assert result.index("D") < result.index("G")
    assert result.index("E") < result.index("G")
    assert result.index("F") < result.index("H")

def test_is_topology_ordered_valid():
    """Test is_topology_ordered with valid topological orderings."""
    # Simple linear case
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    array = ["A", "B", "C", "D"]
    assert is_topology_ordered(edges, array) is True
    
    # Branching case
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    array = ["A", "B", "C", "D"]
    assert is_topology_ordered(edges, array) is True
    
    # Different valid ordering for the same graph
    array = ["A", "C", "B", "D"]
    assert is_topology_ordered(edges, array) is True
    
    # Disconnected graph
    edges = [("A", "B"), ("C", "D")]
    array = ["C", "D", "A", "B"]
    assert is_topology_ordered(edges, array) is True

def test_is_topology_ordered_invalid():
    """Test is_topology_ordered with invalid topological orderings."""
    # Simple violation
    edges = [("A", "B"), ("B", "C")]
    array = ["A", "C", "B"]  # B should come before C
    assert is_topology_ordered(edges, array) is False
    
    # Multiple violations
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    array = ["D", "C", "B", "A"]  # Completely reversed
    assert is_topology_ordered(edges, array) is False

def test_is_topology_ordered_edge_cases():
    """Test is_topology_ordered with edge cases."""
    # Empty array
    edges = [("A", "B")]
    array = []
    assert is_topology_ordered(edges, array) is True
    
    # Empty edges
    edges = []
    array = ["A", "B", "C"]
    assert is_topology_ordered(edges, array) is True
    
    # Subset of vertices
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    array = ["A", "B"]  # Only includes a subset of vertices
    assert is_topology_ordered(edges, array) is True
    
    # Extra vertices in array
    edges = [("A", "B")]
    array = ["X", "A", "B", "Y"]  # Contains vertices not in the edges
    assert is_topology_ordered(edges, array) is True 