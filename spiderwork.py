from  multiprocessing.managers import BaseManager
from download import HtmlDownloader
from Parser import HtmlParser
class SpiderWork(object):
    def __init__(self):
        #初始化分布式进程工作节点的连接工程
        #实现第一步，使用BaseManager注册用于获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        BaseManager.register('get_page_queue')
        BaseManager.register('get_data_queue')
        sever_addr='127.0.0.1'

        print('Connect to sever %s...'%sever_addr)
        self.m=BaseManager(address=(sever_addr,8001),authkey='yuan'.encode('utf-8'))
        self.m.connect()
        self.task=self.m.get_task_queue()
        self.result=self.m.get_result_queue()
        self.page=self.m.get_page_queue()
        self.data=self.m.get_data_queue()
        self.downloader=HtmlDownloader()
        self.parser = HtmlParser()
        print('*--------------------------------------------*')
        print('初始化完成')
        print('*--------------------------------------------*')
    def crawl(self):
        a=1
        # exit()
        while True:
            try:
                if not self.page.empty() :
                    page = self.page.get()
                    urls = self.downloader.download(page)
                    # print(len(urls))
                    self.result.put(urls)
                if  not self.task.empty():
                    url=self.task.get()
                    if url=='end':
                        print('控制节点通知爬虫节点停止工作')
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫节点正在解析第%s条'%a)
                    a=a+1
                    data = self.parser.parser(url)
                    self.data.put(data)
            except EOFError:
                print('连接工作节点失败')
                return
            except Exception as e:
                print(e)
                print('Crawl fail')
if __name__ == '__main__':
    spider=SpiderWork()
    spider.crawl()


