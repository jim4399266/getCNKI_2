代理\redis64-3.0.501
先运行.\redis-server.exe

代理\proxy_pool-master\cli
# 首先启动调度程序
python proxyPool.py schedule

# 然后启动webApi服务
python proxyPool.py webserver