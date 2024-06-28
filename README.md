（更新1：允许在命令行传入输入的csv文件参数，您可以自定义输入的文件名称。此外，您可以不输入任何文件参数，程序将引导您创建一个默认的网络拓扑，您只需要输入路由器的数量）
（更新1备注：默认的拓扑是一个路由器之间全联通的网络拓扑，同时每个路由器与一台主机相连）
（更新：支持的连接数量已经提高到65535条，但是并未经过完全测试，可能出现BUG。255条以内的连接应该不会出现问题）
使用时运行python MininetGen_New.py example.csv指令。其中example.csv可缺省，此时程序将引导您创建一个默认的网络拓扑。
这是一个自动配置Mininet虚拟网络拓扑的程序。您需要在data.csv中输入您网络拓扑中的每一条连接。
data.csv是一个示例文件，您可以直接使用这个网络拓扑，或者修改data.csv中的内容自定义拓扑结构。
data.csv文件中要求主机的名字为hx（如h1, h2, h3等），路由器的名字为rx（如r1, r2, r3等），且序号应该是连续的。
读取文件后，您可以选择是否要查看网络拓扑图。您也可以保存这个图。
本程序将每一条连接两端的设备划入同一个子网。
-------------------------------------------------------------------
(Update1: Custom input file is supported. You can choose which file to be input. In addition, if you input no file, programme will guide you to create a default topo. You are only expected to input how many routers do you need.)
(Note1: A default topo is one that all routers are connected, with one host connected to each routers.)
(Update: Linklist has been extended to 65535, but not well tested. Bugs may be exist. No more than 255 links seems to be safer.)
Run with code 'python MininetGen_New.py example.csv'. You can leave out 'example.csv', in that case, porgramme will guide you to create a default topo. 
It is a programme to configure a topo run by Mininet automatically. You are expected to claim all the links in your topo. 
data.csv is an example. You can use it directly, or you may edit the file by yourself. 
Hosts in data.csv are expected to be like hx (eg: h1, h2, h3, etc), and names of routers should be like rx (eg: r1, r2, r3, etc). 
After reading a csv file, you can decide whether to check the graph or not. You can also save the graph. 
Both side of a link will be divided into the same subnet. 
