import re
from InputDataGraph import InputDataGraph
from Dag import DAG

def LearnProgram( vertices, inOutExs ):
    """
    Learns an expression that conforms to a set of m examples.
    Inputs: Input Rows and In-Out Examples.
    Outputs: Top ranked expression.
    """
    IDG = InputDataGraph("")
    G = IDG.GenInpDataGraph(vertices) # It's supposed to make the IDG given the input rows. How?
    dag = GenerateDag( inOutExs[0], G )
    m = len(inOutExs)
    for i in range(1,m):
        tempD = GenerateDag( inOutExs[i], G )
        dag = IntersectDags(dag, tempD)
    return TopRankExpr(dag)

def IntersectDags(dag1, dag2):
    """
    
    """
    intersected = DAG("")
    intersected.nodes = list(set(dag1.nodes).intersection(set(dag2.nodes)))

    for edge, labels1 in dag1.edges.items():
        if edge in dag2.edges:
            commonLabels = [
                label for label in labels1 if label in dag2.edges[edge]
            ]
            if commonLabels:
                intersected.edges[edge] = commonLabels
    return intersected

def TopRankExpr(dag):
    """
    
    """
    scores = {}
    print("DAG Edges:", dag.edges)
    for edge, transformations in dag.edges.items():
        for transformation in transformations:
            score = len(transformation["constant"])
            scores[transformation] = scores.get(transformation, 0) + score
    
    return max(scores, key=scores.get)

def GenerateRegex(transformation):
    return re.escape(transformation["constant"])

def GenSubStrExpr(inStr, leftIdx, rightIdx, graph):
    """
    Generates a set of substring expressions.
    Inputs: Input string (inStr), left index of the substring (leftIdx), 
            right index of the substring (rightIdx), InputDataGraph (graph).
    Outputs: substring (SubStr).
    """
    print(f"InStr={inStr}")
    id = hash(inStr) # Arbitrary unique ID for a given substring
    vLeft = {}
    vRight = {}
    for v in range(0, len(G.vertices) + 1):
        if (id, l) in I(v): V_l = union(V_l, {v})
        if (id, r) in I(v): V_r = union(V_r, {v})
    pLeft = vLeft.union(ConstantPos(l)) # TODO: We still need to figure out ConstantPos()
    pRight = vRight.union(ConstantPos(r)) # TODO: We still need to figure out ConstantPos()
    return SubStr(s, pLeft, pRight)

"""def GenerateDag( vertices, outStr, graph ):
    \"""
    Inputs: Takes in input row {v_1, ..., v_k}, an output string o_s, and an IDG G.
    Output: a DAG that represents all string expressions in the language L_s that can transform
        the input strings to the output string.
    \"""
    \"""
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
    """

def GenerateDag( inputGraph, outStr):
    dag = DAG(outStr)

    for start in range(len(outStr)):
        for end in range(start + 1, len(outStr) + 1):
            subStr = outStr[start:end]

            subStrExprs = GenSubStrExpr(inputGraph, start, end, subStr)

            for expr in subStrExprs:
                dag.addEdge(start, end, expr)
    
    return dag

def Synthesize( ins, outs ):
    """
    Inputs: Arrays of input and output strings.
    Output: The best regex, if any are possible.
    """
    graphs = [InputDataGraph(inStr) for inStr in ins]
    dags = [
        generateDag(graph, outStr)
        for graph, outStr in zip(graphs, outs)
    ]

if __name__ == "__main__":
    inputs = [
        "Call me at 913-213-3825.",
        "You can reach me at (923) 328-3253",
        "My number is +1-390-623-6345, send me a text at anytime!"
        ]
    outputs = [
        "913-213-3825",
        "(923) 328-3253",
        "+1-390-623-6345"
        ]
    synthesizedRegex = LearnProgram(inputs, outputs)
    print(f"Synthesized Regex: {synthesizedRegex}")

    # TODO: Once bestProg is a thing, use it on a new input without giving it an output to check.
    #freshInput = "Contact me at (555) 123-4567."
    #matches = re.findall(synthesizedRegex, freshInput)
    #print(f"Extracted Output: {matches}")
    