from itertools import islice
import os
from collections import Counter

def getGraph(path):
    with open(path) as f:
        graph = {"nodes":[], "edges":[]}
        splits = []
        priSplits = []  #去除重复节点

        # index = 20    #test
        for _ in islice(f, 1, None):   #跳过第一行
            splits = _.split()
            
            # ####test
            # index -= 1
            # if index >= 0:
            #     print(splits,priSplits)

            # ####end test
            if len(splits) == 2:
                if not splits[0] in priSplits:
                    graph["nodes"].append(dict({"data":{"id":splits[0]}}))
                if not splits[1] in priSplits:
                    graph["nodes"].append(dict({"data":{"id":splits[1]}}))

                graph["edges"].append(dict({"data":{"source":splits[0], "target": splits[1]}}))
            else:
                priSplits = []

            ########

            priSplits = splits
            splits = []

    return graph
def __getGraph(path):
    edges = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            splits = line.split()
            if len(splits) == 2:
                edges.append([splits[0], splits[1]])

    return edges

def __get_nodes_edges(edge_list, owners, count_dict):
    edges = []
    nodes = set()
    for s, t in edge_list:
        nodes.add(s)
        nodes.add(t)
        edges.append({"data":{"source":owners+str(s), "target": owners+str(t), "type":owners}})
    # print(len(nodes))
    nodes = list(nodes)
    # print(len(nodes))
    nodes.sort()
    # print(len(nodes))
    json_nodes = []
    for node in nodes:
        mdgree = count_dict.get(str(node))
        if not mdgree:
            mdgree = 0
        json_nodes.append({"data":{"id":owners+str(node),"type": str(owners), "mdgree": int(mdgree)}})
    return (json_nodes, edges)
def __get_matched_edges(edge_list):
    edges = []
    e_a = []
    e_b = []
    #应该在这里优化一下  循环的同时进行计数
    for s, t in edge_list:
        e_a.append(str(s))
        e_b.append(str(t))
        edges.append({"data":{"source":"ga"+str(s), "target": "gb"+str(t), "type": "matched"}})
    count_a = Counter(e_a)
    count_b = Counter(e_b)
    return (edges, count_a, count_b)
def getFullGraph(ga, gb=None, match=None):
    path_a = r"C:\Users\Shawn\Desktop\flask-graph-matching-viz\example\upload\graphA.txt"
    path_b = r"C:\Users\Shawn\Desktop\flask-graph-matching-viz\example\upload\graphB.txt"
    path_m = r"C:\Users\Shawn\Desktop\flask-graph-matching-viz\example\upload\match.txt"
    #先从匹配边中把匹配节点的度计算出来
    gm = __getGraph(path_m)
    ga = __getGraph(path_a)
    gb = __getGraph(path_b)
 
    nodes = set()
    edges = []
    res_m, count_a, count_b = __get_matched_edges(__getGraph(path_m))
    res_a = __get_nodes_edges(__getGraph(path_a), "ga", count_a)
    res_b = __get_nodes_edges(__getGraph(path_a), "gb", count_b)
    
    result = dict()
    result["nodes"] = res_a[0] + res_b[0]
    result["edges"] = res_a[1] + res_b[1] + res_m

    # print(result)
    return result
    # print(ga)
    # print(gb)
    # print(gm)
def getNodePairs(mpath, graph):

    with open(mpath) as m:

        for mline in m:
            splits = mline.split()
            for node in graph['nodes']:
                if (node['data']['id'] == splits[1] or node['data']['id'] == splits[0]) and node['data'].get('type') == None:
                    node['data']['type'] = "matched"
            graph["edges"].append(dict({"data":{"source":splits[0], "target": splits[1], "type":"matched"}}))
    return graph


def test(source, match):
    common_nodes = set()
    in_source = set()
    in_match = set()
    common_edges = set()
    match_edges = set()
    with open(source) as s:
        with open(match) as m:
            for s_line in s:
                pair = s_line.split()
                # print(pair, end="sline\n")
                      
                if(len(pair)) == 2:
                    in_source.add(pair[0])
                    in_source.add(pair[1])
                for m_line in m:
                    mpair = m_line.split()

                    # print(mpair, end="mline\n")

                    if(len(mpair) == 2):
                        in_match.add(mpair[0])
                        in_match.add(mpair[1])
                    # print(mpair, pair)
                    if pair == mpair:
                        common_edges.add(tuple(pair))
                        break
                    else:
                        match_edges.add(tuple(mpair))
                m.seek(0, os.SEEK_SET)  #这个坑太大了， 将文件指针置为开始位置
    common_nodes = in_source & in_match
    unsoure_nodes = in_match - in_source
    print(len(in_source - common_nodes)) 
    print(len(unsoure_nodes))

    __log('Ltest.txt', "in_source:\n"+str(in_source)+"\n")
    __log('Ltest.txt', "in_match:\n"+str(in_match)+"\n")
    __log('Ltest.txt', "common_nodes:\n"+str(common_nodes)+"\n")
    __log('Ltest.txt', "common_edges:\n"+str(common_edges)+"\n")
    __log('Ltest.txt', "match_edges:\n"+str(match_edges)+"\n")


def __log(doc, content):
    with open(doc, 'a') as f:
        f.write(content)
        


if __name__ == '__main__':
    # print(getGraph('./sample.txt'))
    # res = getNodePairs( './data/match.txt',getGraph('./data/graphA.txt'))
    # res = getGraph('./data/graphA.txt')
    # s = str(res)
    # with open('test.txt', "w") as f:
    #     f.write(s)
    # print(s[:100])

    # test("./data/graphA.txt", "./data/match.txt")
    # test("./data/myA.txt", "./data/mymatch.txt")
    getFullGraph("")
    pass