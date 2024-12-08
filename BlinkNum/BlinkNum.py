from InputDataGraph import InputDataGraph

def LearnProgram( vertices, setOfOs ):
    """
    Learns an expression that conforms to a set of m examples.
    Inputs: Vertices and Examples.
    Outputs: Top ranked expression.
    """
    G = GenInpDataGraph(vertices[0])
    d = GenerateDag( setOfOs[0], G )
    m = len(setOfOs)
    for i in range(1,m):
        tempD = GenerateDag( setOfOs[i], G )
        d = d.Intersect(tempD)
    return TopRankExpr(d)

def GenSubStrExpr(inStr, leftIdx, rightIdx, graph):
    """
    Generates a set of substring expressions.
    Inputs: Input string (inStr), left index of the substring (leftIdx), 
            right index of the substring (rightIdx), InputDataGraph (graph).
    Outputs: substring (SubStr).
    """
    id = string2Id[s]
    vLeft = {}
    vRight = {}
    for v in range(0, len(G.vertices) + 1):
        if (id, l) in I(v): V_l = union(V_l, {v})
        if (id, r) in I(v): V_r = union(V_r, {v})
    pLeft = vLeft.union(ConstantPos(l))
    pRight = vRight.union(ConstantPos(r))
    return SubStr(s, pLeft, pRight)

def GenerateDag( vertices, outStr, graph ):
    """
    Inputs: Takes in input row {v_1, ..., v_k}, an output string o_s, and an IDG G.
    Output: a DAG that represents all string expressions in the language L_s that can transform
        the input strings to the output string.
    """
    # TODO: Finish this.
    # First creates len(o_s) number of nodes with labels eta = {0,...,len(o_s)}
    # Sets the start node eta^s to be the node with label 0, and final node eta^f
    #   with label len(o_s).
    # Iterates over all substrings o_s[i..j] of the output string, and adds an
    #   edge (i,j) between the nodes with labels i and j.
    # For each edge (i,j), the algorithm learns the function W that maps the
    #   edge to a constant string expression ConstantStr(o_s[i..j]) and a set 
    #   of substring expressions obtained by calling GenSubStrExpr(v_k,l,r,G) 
    #   (for each (k,l,r) such that v_k[l..(r-1)] = o_s[i..j]).

if __name__ == "__main__":
    # TODO: Put everything together.
    pass