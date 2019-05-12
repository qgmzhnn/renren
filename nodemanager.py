import random,time
from multiprocessing.managers import BaseManager
from urlmanager import UrlManager
import csv

class NodeManager(object):
    def start_Manager(self,url_q,result_q,page_q,data_q):
        #将创建的队列注册在网络上，利用register方法，callable参数关联了
        #Queue对象，将Queue对象在网络中暴露
        self.url_q=url_q
        self.result_q=result_q
        self.page_1=page_q
        self.data_q=data_q
        BaseManager.register('get_task_queue',callable=lambda :url_q)
        BaseManager.register('get_result_queue',callable=lambda :result_q)
        BaseManager.register('get_page_queue', callable=lambda : page_q)
        BaseManager.register('get_data_queue', callable=lambda : data_q)
        #绑定端口8001，设置验证口令“yuan”，这个相当于对象的初始化
        manager=BaseManager(address=('',8001),authkey='yuan'.encode('utf-8'))
        return manager
    def get_url_q(self):
        return self.url_q

    def get_result_q(self) :
        return self.result_q

    def url_manager_proc(self, url_q, conn_q, root_url) :
        url_manager = UrlManager()
        # url_manager.add_new_url(root_url)
        while True :
            while (url_manager.has_new_url()) :

                # 从URL管理器获取新的url
                new_url = url_manager.get_new_url()
                print(new_url)
                # 将新的URL发给工作节点
                url_q.put(new_url)
                print( 'old_url=', url_manager.old_url_size())

                # 加一个判断条件，当爬去2000个链接后就关闭,并保存进度
                if (url_manager.old_url_size() > 2000) :
                    # 通知爬行节点工作结束
                    url_q.put('end')
                    print( '控制节点发起结束通知!')

                    # 关闭管理节点，同时存储set状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
            # 将从result_solve_proc获取到的urls添加到URL管理器之间
            try :
                if not conn_q.empty() :
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException as e :
                time.sleep(0.1)  # 延时休息
    def result_solve_proc(self,result_q,conn_q,store_q,data_q):
        while True:
            try:
                if not result_q.empty():
                    urls=result_q.get()
                    conn_q.put(urls)  # url为set类型
                    if urls=='end':
                        print('结果分析进程接收通知然后结束')
                        store_q.put('end')
                        return
                    data = data_q.get()
                    store_q.put(data)#解析出来的数据为dict类型
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(e)
                time.sleep(0.1)

    def store_proc(self, store_q) :
        with open('人人车.csv','w',newline='')as f:
            csv_writer=csv.writer(f,dialect='excel')
            csv_writer.writerow(["车名", "价格", "分期", "服务费", "行驶里程", "上牌时间", "车牌所在地", "外迁", "变速箱", "过户记录"])
            while True :
                if not store_q.empty():
                    data = store_q.get()
                    if data == 'end' :
                        print( '存储进程接受通知然后结束!')
                        f.close()
                        return
                    if data is not  None:
                        f.write(data)
                else :
                    time.sleep(0.1)


