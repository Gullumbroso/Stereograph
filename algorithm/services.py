import networkx as nx
from heapq import heappush, heappop
from networkx import NetworkXError


'''
def populate_server():
    def num_of_search_to_weight(num_of_search):
        if num_of_search == "LOW":
            return 1
        elif num_of_search == "MEDIUM":
            return 1 / 5
        elif num_of_search == "HIGH":
            return 1 / 20

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./local_static/A-Star_Algorithm-e13b7033c464.json',
                                                                   scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key("13zVMccgzUZ8oIk2V4joIVC3AiT98iXmMVMqau4Yfy6o")
    sheet = wks.sheet1
    phrases = sheet.col_values(1)
    num_of_searches = sheet.col_values(2)

        re_exp = re.compile('(\w+) people are (\w+)')
    not_flag = False

    for i in range(1, sheet.row_count):
        phrase = phrases[i]
        matcher_is = re_exp.match(phrase)
        if matcher_is:
            if " not " in phrase:
                not_flag = True
                phrase = phrase.replace('not ', '')
                matcher_is = re_exp.match(phrase)
            # a is b
            p1 = matcher_is.group(1).lower()
            p2 = matcher_is.group(2).lower()
            if p1 != p2:
                node1 = Characteristic(value=p1)
                node2 = Characteristic(value=p2)
                try:
                    node1.save()
                    node2.save()
                    break
                except ValueError:
                    print("There was an error! with saveing ")
                weight = num_of_search_to_weight(num_of_searches[i])
                edge1 = Edge(source=p1, destination=p2, weight=weight, is_negative=not_flag)
                try:
                    edge1.save()
                    break
                except ValueError:
                    print("There was an error with the edge: " + edge1.source + "To" + edge1.destination)
            not_flag = False
'''


def prepare_graph(nodes, edges):
    graph = nx.DiGraph()
    nodes_values = [node['value'] for node in nodes]
    graph.add_nodes_from(nodes_values)
    for edge in edges:
        u = edge['source']     # Source
        v = edge['destination']     # Destination
        w = edge['weight']     # Weight
        graph.add_weighted_edges_from([(u, v, w)])
    return graph


def shortest_path(graph, source, target):
    try:
        length, path = nx.bidirectional_dijkstra(graph, source.lower(), target.lower())
        return length, path
    except:
        return -1, []


def astar_path(G, source, target, heuristic=None):
    """
    Return a list of nodes in a shortest path between source and target
    using the A* ("A-star") algorithm.

    There may be more than one shortest path.  This returns only one.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : node
       Ending node for path

    heuristic : function
       A function to evaluate the estimate of the distance
       from the a node to the target.  The function takes
       two nodes arguments and must return a number.


    See Also
    --------
    shortest_path(), dijkstra_path()

    """
    if G.multigraph == True:
        raise NetworkXError("astar_path() not implemented for Multi(Di)Graphs")

    if heuristic is None:
        # The default heuristic is h=0 - same as Dijkstra's algorithm
        def heuristic(u, v):
            return 0
    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    queue = [(0, source, 0, None)]
    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    while queue:
        # Pop the smallest item from queue.
        _, curnode, dist, parent = heappop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            if neighbor in explored:
                continue
            ncost = dist + w
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost < ncost, a longer path to neighbor remains
                # enqueued. Removing it would need to filter the whole
                # queue, it's better just to leave it there and ignore
                # it when we visit the node a second time.
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            heappush(queue, (ncost + h, neighbor, ncost, curnode))

    raise NetworkXError("Node %s not reachable from %s" % (source, target))