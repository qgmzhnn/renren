import pickle
import hashlib

class UrlManager(object):
    def __init__(self):
        self.new_urls=self.load_progress('new_urls.txt')#未爬的
        self.old_urls = self.load_progress('old_urls.txt')#已爬的
    def has_new_url(self):
        return self.new_url_size()!=0

    def get_new_url(self):
        new_url=self.new_urls.pop()#pop用于删除列表中的一个元素，并且返回该元素的值
        m=hashlib.md5()
        m.update(new_url.encode('utf-8'))
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url
    '''将未爬的url添加到集合中'''
    def add_new_url(self,url):
        if url is None:
            return
        m=hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5=m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:#判断未爬取并且还未添加
            try:
                self.new_urls.add(url)
                # print(self.new_urls)
            except Exception as e:
                print(e)

    def add_new_urls(self,urls):
        '''urls为url集合'''
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self) :
        return len(self.new_urls)
    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self,path,data):
        with open(path,'wb') as f:
            '''以字节对象形式返回封装的对象，不需要写入文件中'''
            pickle.dump(data,f)
            # f.close()
    def load_progress(self,path):
        print('[+] 从文件加载进度: %s'%path)
        try:
            with open(path,'rb') as f:
                '''从字节对象中读取被封装的对象，并返回'''
                tmp=pickle.load(f)
                return tmp
        except EOFError:
                print('[!] 文件为空')
        return set()