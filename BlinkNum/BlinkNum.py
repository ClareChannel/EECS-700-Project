"""
This file is my (ongoing) attempt at translating the pseudocode from the 
original BlinkFill paper to working Python code.

For now, expect it to have many, many syntax errors as I translate things.
"""

# Algorithm for constructing the input graph for a set of n input rows each consisting of k columns/strings.
#def GenInpDataGraph( { (v_1^1, ..., v_k^1) , ... , (v_1^n, ..., v_k^n) } )
def GenInpDataGraph(columns):
    """
    The key idea of the algorithm is to first construct a graph for each 
    spreadsheet column, and then return the union of these graphs as the 
    resulting graph for the spreadsheet data.

    Input: Set of all input rows (n), each for k columns/strings.
    Output: Post-union graph.
    """
    G = {} # collection of generated graphs for each column
    k = len(columns[0])
    #for i = 1 to k:
    for i in range(0, k):
        #G_i = GenGraphColumn({v_i^1, ..., v_i^n}) # GenGraphColumn(sets[i])
        G = G.union(GenGraphColumn(columns[i]))
    #return union_(1 <= i <= k) G_i
    return G

#def GenGraphColumn( {(s_1, ..., s_n)} ): # input is strings for each row?
def GenGraphColumn(input: set):
    """
    Input: Set of strings for each row.
    Output: InputDataGraph
    """
    #G := GenGraphStr(s_1)
    G = GenerateInputGraph(input[0])
    #for i = 2 to n:
    n = len(input)
    for i in range(1, n):
        #G := Intersect(G, GenGraphStr(s_i)) # GenGraphStr(s_i) seems to be GenerateInputGraph(s)
        G = G.intersection(input[i])
    return G

# Algorithm for constructing the input graph for an input string s.
def GenerateInputGraph(s): # s = input string
    """
    
    """
    # V is the set of nodes; v_# are nodes.
    # E is the set of edges corresponding to a set of ordered node pairs,
    # I : V -> {(id, idx)_i}_i is a labeling function that labels each node with
    #   a set of string id and index pair (id, idx),
    # L : E -> {(r,k)_i}_i maps each edge to a list of token matches.
    V = {}, E = {}, I = {}, L = {}
    id = string2Id[s] # This function isn't in the paper. We could make something up.
    #foreach i in range(0, len(s) + 3):
    for i in range(0, len(s) + 3):
        #V = union(V, v_i) # unions with a node that doesn't exist yet...?
        V = V.union(V[i])
        I[i] = { (id, i) } # Could just be something that adds a label to a given node, or is a whole different set. Idk.
    #L((v_0, v_1) = { (^,1) } # First and second vertices
    L.add( { V[0], V[1], {'^','1'} } )
    #L((v_(len(s)+1), v_(len(s)+2) = {($,1)} # Second to last and last vertices
    #L.add = { V[len(s)+1], V[len(s)+2], {'$','1'} } # moved to the end of the function
    #foreach i in range(1, len(s) + 1):
    for i in range(1, len(s) + 1):
        #foreach j in range(i+1, len(s) + 2):
        for j in range(i+1, len(s) + 2):
            leftIdx = i, rightIdx = j-1
            #E = union(E, (v_i, v_j)
            E = E.union(V[i], V[j])
            #c_s = s[leftIdx..rightIdx]
            constantString = s[leftIdx:rightIdx]
            L((v_i,v_j)) = {(c_s, GetMId(c_s,s,i))} # GetMId apparently uses has lookup. There's not etach more information than that.
            #foreach r in T and Match(r, c_s):
            for r in T and Match(r, c_s):
                L((v_i, v_j)) = union(L((v_i, v_j)),(r,GetMId(r,s,i)))
    L.add = { V[len(s)+1], V[len(s)+2], {'$','1'} }
    return (V,E,I,L)

# Learns an expression that conforms to a set of m examples
#def LearnProgram( { (v_1^1, ..., v_k^1), ..., (v_1^n, ..., v_k^n) }, {((v_1^1, ..., v_k^1), o_s^1), ..., ((v_1^m, ..., v_k^m),o_s^m) } ):
def LearnProgram( vertices, setOfOs ):
    """
    
    """
    #G := GenInpDataGraph( { (v_1^1,...,v_k^1), ..., (v_1^n,...,v_k^n) } )
    G = GenInpDataGraph(vertices[0])
    #Dag d := GenerateDag( (v_1^1,...,v_k^1 s), o_s^1, G)
    d = GenerateDag( setOfOs[0], G )
    #for i = 2 to m:
    m = len(setOfOs)
    for i in range(1,m):
        #Dag d' := GenerateDag( (v_1^i, ..., v_k^i s), o_s^i, G)
        tempD = GenerateDag( setOfOs[i], G )
        #d := Intersect(d, d')
        d = d.Intersection(tempD)
    return TopRankExpr(d)

# Algorithm for generating a set of substring expressions given an input string 
# s, the left and right indices l and r of the substring, and the InputDataGraph G.
def GenSubStrExpr(s, l, r, G):
    """
    
    """
    id = string2Id[s]
    #V_l = nullSet, V_r = nullSet
    vLeft = {}, vRight = {}
    #foreach v in V(G):
    for v in range(0, len(G.vertices) + 1):
        if (id, l) in I(v): V_l = union(V_l, {v})
        if (id, r) in I(v): V_r = union(V_r, {v})
    #p_l = union(V_l, ConstantPos(l))
    pLeft = vLeft.union(ConstantPos(l))
    #p_r = union(V_r, ConstantPos(r))
    pRight = vRight.union(ConstantPos(r))
    #return SubStr(s, p_l, p_r)
    return SubStr(s, pLeft, pRight)

#def GenerateDag( {v_1, ..., v_k}, o_s, G ):
def GenerateDag( vertices, outStr, graph ):
    """
    Inputs: Takes in input row {v_1, ..., v_k}, an output string o_s, and an IDG G.
    Output: a DAG that represents all string expressions in the language L_s that can transform
        the input strings to the output string.
    """
    # First creates len(o_s) number of nodes with labels eta = {0,...,len(o_s)}
    # Sets the start node eta^s to be the node with label 0, and final node eta^f
    #   with label len(o_s).
    # Iterates over all substrings o_s[i..j] of the output string, and adds an
    #   edge (i,j) between the nodes with labels i and j.
    # For each edge (i,j), the algorithm learns the function W that maps the
    #   edge to a constant string expression ConstantStr(o_s[i..j]) and a set 
    #   of substring expressions obtained by calling GenSubStrExpr(v_k,l,r,G) 
    #   (for each (k,l,r) such that v_k[l..(r-1)] = o_s[i..j]).

# Algorithm for assigning scores to the nodes of an InputDataGraph G.    
def RankInpGNodes(G):
    """
    
    """
    # phi_eta (v_1, v_2) := sum_(id in I(v_1)) abs(v_2[id] - v_1[id])
    # phi_eta is the "node distance function"
    #foreach v in V(G):
    for v in G.vertices:
        #v.out := 0, v.in := 0, v.score := 0
        v.out = 0, v.inp = 0, v.score = 0
    #foreach v in V(G) in topological order:
    for v in G.vertices: # may have to "order" these first?
        #foreach (v,v_i) in E(G):
        for edge in G.edges:
            #v.out := Max(v.out, v_i.out + phi_eta (v, v_i) )
            v.out = max(v.out, )
    #foreach v in V(G) in reverse topological order:
    for v in G.vertices: # in "reverse topological order"?
        #foreach (v_i, v) in E(G):
        for v_i, v in G.edges:
            #v.in := Max(v.in, v_i.in + phi_eta (v_i, v) )
            v.inp = max(v.inp, v_i.inp ) # still needs the + phi_eta (v_i, v)
    #foreach v in V(G):
    for v in G.vertices:
        #v.score := v.in + v.out
        v.score = v.inp + v.out
    #return v with the highest v score
    maxScoreVert = G.vertices[0]
    for v in G.vertices:
        if v.score > maxScoreVert.score:
            maxScoreVert = v
    return maxScoreVert

# Node Distance Function. Equivalent to the φ_η (phi_eta) function from the paper.
def NodeDistance(vertex1, vertex2, I):
    """
    Python translation of the following pseudocode:
    phi_eta (v_1, v_2) := sum_(id in I(v_1)) abs(v_2[id] - v_1[id])

    Inputs: Two vertices (vertex1, vertex2) and 
            an InputDataGraph's set of vertex labels (I).
    Outputs: The sum of the equation.
    """
    ret = 0
    for id in I[vertex1]:
        ret += abs(vertex2.id - vertex1.id)
    return ret

# It's possible that Python's intersect function takes care of this well enough, 
# but if we have intersection errors, then this should be filled out and used instead.
def Intersect(G_1, G_2):
    """
    Inputs: Two IDGs G_1 = (V_1, E_1, I_1, L_1) and G_2 = (V_2, E_2, I_2, L_2)
    Outputs: New IDG G = (V, E, I, L)
    """
    V = {} # V = {(v_i, v_j) such that v_i in V_1, v_j in V_2}
    E = {} # E = {((v_i, v_j), (v_k, v_l)) such that (v_i, v_k) in E_1, (v_j, v_l) in E_2 }
    I = {} # I = ((v_i, v_j)) = union(I_1(v_i), I_2(v_j)), for all v_i in V_1, v_j in V_2
    L = {} # L = (((v_i, v_j), (v_k, v_l))) = { (r,k)|(r,k) is in L_1((v_i,v_k)) and (r,k) is in L_2((v_j, v_l))} for all E_1, (v_j, v_i) is in E_2
    return (V,E,I,L)