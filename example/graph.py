from itertools import islice
import os


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
                m.seek(0, os.SEEK_SET)  #将文件指针置为开始位置
    common_nodes = in_source & in_match
    unsoure_nodes = in_match - in_source
    print(len(in_source - common_nodes)) 
    print(len(unsoure_nodes))

    __log('Ltest.txt', "in_source:\n"+str(in_source)+"\n")
    __log('Ltest.txt', "in_match:\n"+str(in_match)+"\n")
    __log('Ltest.txt', "common_nodes:\n"+str(common_nodes)+"\n")
    __log('Ltest.txt', "common_edges:\n"+str(common_edges)+"\n")
    __log('Ltest.txt', "match_edges:\n"+str(match_edges)+"\n")
def __get_graph(path, category):
    nodes = set()
    edges = list()
    with open(path) as f:
        for line in f:
            splits = line.split()
            if len(splits) == 2:
                nodes.add(splits[0])
                nodes.add(splits[1])
                edges.append({"source":splits[0], "target":splits[1]})
    dict_nodes = []
    lable = 0
    if category == "GraphB":
        lable = 1
    for node in nodes:
        '''
        {
            "name": "AnalyserNode",
            "value": 1,
            "category": 4
        },

        '''
        dict_nodes.append({"name":category, "value":node, "category":lable})
    return (list(dict_nodes), edges)

def __get_sim(match):
    edges = []
    with open(match) as f:
        for line in f:
            splits = line.split()
            if len(splits) == 2:
                edges.append({"source":splits[0], "target":splits[1]})
    return edges
def gen_json(fileA, fileB, match):
    # a_node = set()
    # b_node = set()
    # a_edges = list()
    # b_edges = list()
    # matched_edges = list()


    nodes = []
    edges = []
    ga = __get_graph(fileA, "GraphA")
    gb = __get_graph(fileA, "GraphB")
    em = __get_sim(match)
    nodes = ga[0] + gb[0]
    edges = ga[1] + gb[1] + em
    my_json =  {
    "type": "force",
    "categories": [
        {
            "name": "GraphA",
            "keyword": {},
            "base": "GraphA"
        },
        {
            "name": "GraphB",
            "keyword": {},
            "base": "GraphB"
        },
        {
            "name": "GraphA & GraphB",
            "keyword": {},
            "base": "GraphB"
        }
    ],
    "nodes": nodes,
    "links": edges
    }
    return my_json



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
    print(gen_json("./data/graphA.txt", "./data/graphB.txt", "./data/match.txt"))
    pass