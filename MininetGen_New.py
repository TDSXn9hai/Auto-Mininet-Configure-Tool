import csv
import sys
import matplotlib.pyplot as plt
import networkx as nx


# 读取csv文件
with open('data.csv', 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    nodes1 = [row['source'] for row in reader]
with open('data.csv', 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    nodes2 = [row['target'] for row in reader]
nodes1.extend(nodes2)       # 连接两个列表
raw_hosts = []
raw_routers = []
for element in nodes1:      # 检查所有涉及到的节点
    if element in raw_hosts:    # 出现不止一次，证明是路由器，而不是主机。
        raw_hosts.remove(element)
        # raw_routers.append([element, 2])     # 这时候应该是路由器出现了第二次，也就是有两个接口
        raw_routers.append(element)
    elif element not in raw_routers:
    # else:
        raw_hosts.append(element)
        # for router in raw_routers:
        #     if router[0] == element:    # 记录路由器用到的接口数量
        #         router[1] = router[1] + 1
        #         raw_hosts.remove(element)
        #         break
            # else:
                # hosts.append(element)     # 目前只出现了一次，暂时认为是主机。
# 排序主机和路由器
# print(raw_hosts)
# print(raw_routers)
hosts = []
routers = []
i = 1
for element in raw_hosts:
    # print(element.split('h')[1])
    if element.split('h')[1] == str(i):
        hosts.append(element)
    i = i + 1
i = 1
while raw_routers:
    for element in raw_routers:
        # print(element)
        # print(element[0].split('r')[1])
        if element.split('r')[1] == str(i):
            routers.append(element)
            raw_routers.remove(element)
            break
    i = i + 1
# 生成连接列表，并且为各个节点赋值ip
linklist = []
with open('data.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)    # 去除首行
    for line in reader:
        linklist.append(line)
# print(linklist)
# 是否生成无向图[y or n]
if_graph = input('Do you want to generate a graph?[y/n]')
if if_graph == 'y' or if_graph == 'Y':
    print('Graph generating.It may take a while.')
    G = nx.Graph()
    nodes2 = hosts + routers
    # 建立节点和序号的对应关系
    i = 0
    for element in nodes2:
        i = i + 1
        G.add_node(i, desc=element)
    for link in linklist:
        line = [0, 0]
        for i in range(2):
            j = 0
            for element in nodes2:   # 遍历列表
                j = j + 1
                # print(line[i])
                if link[i] == element:
                    line[i] = j
                    # print("=========Changed=========")
                    break
        G.add_edge(line[0], line[1])
    pos = nx.spring_layout(G)  # 用 FR算法排列节点
    nx.draw(G, pos, with_labels=True, alpha=0.5)
    node_labels = nx.get_node_attributes(G, 'desc')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    print("Graph Generated Successfully")
    # print(linklist)
    plt.show()
elif if_graph == 'N' or if_graph == 'n':
    print('Got it.Graph will not be generated.')
else:
    print('%s seems to be an invalid input.Graph will not be generated.' % if_graph)
    input('Press any key to continue.')
# 分配IP
ipbase = '10.%d.%d.%d'
if len(linklist) > 65535:
    print('Too much links!Expected no more than 65535!')
    sys.exit(1)
j = 0
k = 0
for i in range(len(linklist)):          # linklist格式为[name1, name2, ip1, ip2]
    if k > 255:
        k = k - 256
        j = j + 1
    linklist[i].append(ipbase % (j, k, 1))
    linklist[i].append(ipbase % (j, k, 2))
    k = k + 1
# print(linklist)
# 接下来创建主机、路由器与IP之间的映射关系
hostlist = []
raw_routers = []
for link in linklist:
    if link[0] in hosts:
        hostlist.append([link[0], link[2]])
    elif link[0] in routers:
        raw_routers.append([link[0], link[2]])
    if link[1] in hosts:
        hostlist.append([link[1], link[3]])
    elif link[1] in routers:
        raw_routers.append([link[1], link[3]])
# 整合路由器列表，使得列表的每个元素结构为[name, eth0ip, eth1ip, eth2ip ...]，且name不重复
routerlist = []
for router in routers:
    routerinfo = [router]
    for element in raw_routers:
        if element[0] == router:
            routerinfo.append(element[1])
    routerlist.append(routerinfo)
print('IP generated.')
# print(hostlist)
# print(routerlist)
# 完成了IP地址的分配，开始生成文件
topohead = '''#!/usr/bin/python

import time
import os

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\\n' )
    info( '*** Add switches\\n')

    r = {} # routers
    r_net = {} # networks (ip prefix) of each router

'''
#   输入为 路由器id，路由器名，路由器id
routercreate = '''    r[%d] = net.addHost('%s', cls=Node, ip='0.0.0.0')
    r[%d].cmd('sysctl -w net.ipv4.ip_forward=1')
'''
#   输入内容是路由器数量
routercreate2 = '''    for i in range(1, %d):
        r_net[i] = []
        r[i].cmd('sysctl -w net.ipv4.icmp_errors_use_inbound_ifaddr=1')

'''
hosthead = '''    info( '*** Add hosts\\n')
'''
#   输入内容是主机名，主机名，主机IP
hostcreate = '''    %s = net.addHost('%s', cls=Host, ip='%s/24', defaultRoute=None)
'''
linkhead = '''
    info( '*** Add links\\n')
'''
#   输入内容是连接的主机名或者是路由器接口号:(r[1])格式
linkcreate = '''    net.addLink(%s, %s)
'''
ncscreate = '''
    info( '*** Starting network\\n')
    net.build()
    info( '*** Starting controllers\\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\\n')

'''
ethiphead = '''    info( '*** Post configure switches and hosts\\n')
'''
#   输入分别为路由器序号，路由器名，接口序号，接口IP
ethipcreate = '''    r[%d].cmd('ifconfig %s-eth%d %s/24')
'''
#   输入分别是主机名，与主机相连的接口IP
defaultgwcreate = '''    %s.cmd('route add default gw %s')
'''
#   输入分别是路由器序号，接口所在的子网
rnetappend = '''    r_net[%d].append('%s0')
'''
confhead = """
    conf_template = '''
    hostname r%d_ospfd
    password 123
    enable password 123

    router ospf
        ospf router-id 1.1.1.%d
    '''

    conf_rest = '''
    debug ospf event
    log file /tmp/r%d.log
    '''

    net_template = 'network %s/24 area 0'

"""
#   输入内容是路由器个数+1
for_sentence = '''    for i in range(1, %d):
'''
quaggamodule1 = '''        r[i].cmdPrint('/usr/sbin/zebra -d -f /etc/quagga/zebra.conf -i /tmp/zebra%d.pid -z /tmp/zebra%d.sock'%(i,i))
        r[i].waitOutput()

    time.sleep(1)

'''
quaggamodule2 = '''        fp = open('/tmp/r%d.conf'%i, 'w')
        conf = conf_template%(i,i)
        for j in range(len(r_net[i])):
            conf += '\\n'
            conf += net_template%r_net[i][j]
        conf += conf_rest%i
        fp.write(conf)
        fp.close()
        r[i].cmdPrint('/usr/sbin/ospfd -d -f /tmp/r%d.conf -i /tmp/ospf%d.pid -z /tmp/zebra%d.sock'%(i, i, i))
        r[i].waitOutput()
'''
filetail = '''    time.sleep(120)
    CLI(net)
    net.stop()

    os.system("killall -9 ospfd zebra")

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
'''
print('Starting file generation.')
with open('topo.py', 'w') as pyfile:
    pyfile.write(topohead)
    i = 1
    for element in routerlist:
        pyfile.write(routercreate % (i, element[0], i))
        i = i + 1
    pyfile.write(routercreate2 % (len(routerlist)+1))
    pyfile.write(hosthead)
    for element in hostlist:
        pyfile.write(hostcreate % (element[0], element[0], element[1]))
    pyfile.write(linkhead)
    for link in linklist:
        node1 = link[0]
        node2 = link[1]
        if node1 in routers:
            node1 = 'r[' + link[0].split('r')[1] + ']'
        if node2 in routers:
            node2 = 'r[' + link[1].split('r')[1] + ']'
        pyfile.write(linkcreate % (node1, node2))
    pyfile.write(ncscreate)
    i = 1
    for element in routerlist:
        for j in range(1, len(element)):   #   element由路由器名和接口ip组成
            pyfile.write(ethipcreate % (i, element[0], j-1, element[j]))
        i = i + 1
    for link in linklist:
        if link[0] in hosts:
            pyfile.write(defaultgwcreate % (link[0], link[3]))
        elif link[1] in hosts:
            pyfile.write(defaultgwcreate % (link[1], link[2]))
    i = 1
    for element in routerlist:
        for j in range(1, len(element)):
            pyfile.write(rnetappend % (i, element[j][:-1]))   # 去掉最后一个字符即可
        i = i + 1
    pyfile.write(confhead)
    pyfile.write(for_sentence % (len(routerlist) + 1))
    pyfile.write(quaggamodule1)
    pyfile.write(for_sentence % (len(routerlist) + 1))
    pyfile.write(quaggamodule2)
    pyfile.write(filetail)
    print('File generated.')

