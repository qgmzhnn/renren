from nodemanager import NodeManager

from multiprocessing import Process,Queue
if __name__ == '__main__':
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    page_q=Queue()
    data_q = Queue()
    for i in range(1,10):
        page_q.put(i)
    # 创建分布式管理器
    node = NodeManager()
    manager = node.start_Manager(url_q, result_q,page_q,data_q)
    # 创建URL管理进程、 数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc,
                               args=(url_q, conn_q, 'https://www.renrenche.com/nc/ershouche/p1',))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,data_q))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()