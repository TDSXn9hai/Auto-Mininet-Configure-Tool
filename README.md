（更新：支持的连接数量已经提高到65535条，但是并未经过完全测试，可能出现BUG。255条以内的连接应该不会出现问题）
使用时直接运行MininetGen_New文件即可。
这是一个自动配置Mininet虚拟网络拓扑的程序。您需要在data.csv中输入您网络拓扑中的每一条连接。
data.csv是一个示例文件，您可以直接使用这个网络拓扑，或者修改data.csv中的内容自定义拓扑结构。
data.csv文件中要求主机的名字为hx（如h1, h2, h3等），路由器的名字为rx（如r1, r2, r3等），且序号应该是连续的。
读取文件后，您可以选择是否要查看网络拓扑图。您也可以保存这个图。
本程序将每一条连接两端的设备划入同一个子网。
==================================================================
(Update: Linklist has been extended to 65535, but not well tested. Bugs may be exist. No more than 255 links seems to be safer.)
Run MininetGen_New.py file and you can get your topo. 
It is a programme to configure a topo run by Mininet automatically. You are expected to claim all the links in your topo. 
data.csv is an example. You can use it directly, or you may edit the file by yourself. 
Hosts in data.csv are expected to be like hx (eg: h1, h2, h3, etc), and names of routers should be like rx (eg: r1, r2, r3, etc). 
After reading a csv file, you can decide whether to check the graph or not. You can also save the graph. 
Both side of a link will be divided into the same subnet. 
