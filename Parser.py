from fontTools.ttLib import TTFont
import re
import requests
from lxml import etree
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

}
class HtmlParser(object) :
    def parser(self,url) :
        self.url=url
        if  url is None :
            return
        new_data = self._get_new_data(url)
        return  new_data
    def _get_new_data(self, url) :
        '''
        抽取有效数据
        '''
        data = []

        text =self.get_text()
        tree = etree.HTML(text)
        gongli = str(tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[1]/div/p/strong/text()')[0])
        shangpai = str(tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[2]/div/p[2]/text()')[0])
        new_gongli = self.tran(gongli,text)
        new_shangpai = self.tran(shangpai,text)
        text = text.replace(gongli, new_gongli).replace(shangpai, new_shangpai)
        tree = etree.HTML(text)
        name = tree.xpath('//div[@class="container detail-breadcrumb"]/p/a[5]/text()')[0]
        price = tree.xpath('//div[@class="middle-content"]/div[1]/p/text()')[0] + '万'
        fenqi = tree.xpath('//div[@class="list payment-list"]/p[2]/text()')[0] + ' ' + \
                tree.xpath('//div[@class="list payment-list"]/p[3]/text()')[0]
        fuwu_price = str(tree.xpath('//div[@class="detail-version3-service"]/p[2]/text()')[0]).replace('\n',
                                                                            '').replace(' ',
                                                                                                                   '') + \
                     tree.xpath('//div[@class="detail-version3-service"]/p[2]/span/text()')[0]
        kilometre = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[1]/div/p[1]/strong/text()')[0]
        car_summary = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[2]/div/p[2]/text()')[0]
        licensed_city = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[3]/div/p[1]/strong/text()')[0]
        car_fluid = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[4]/div/p[1]/strong/text()')[0]
        biansu = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[5]/div/p[1]/strong/text()')[0]
        car_transfer = tree.xpath('//div[@class="row-fluid-wrapper"]/ul/li[6]/p[1]/strong/text()')[0]
        # print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(name, price, fenqi, fuwu_price, kilometre,car_summary, licensed_city, car_fluid,biansu, car_transfer))
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(name, price, fenqi, fuwu_price, kilometre,car_summary, licensed_city, car_fluid,biansu, car_transfer)
    def get_text(self):
        r=requests.get(url=self.url,headers=headers)
        return  r.text
    def tran(self,text,html):
        url = re.findall("url\('(.*?.woff)'", html)[0]
        with open('人人车01.ttf', 'wb') as f :
            f.write(requests.get(url=url).content)
        font1 = TTFont('人人车.ttf')
        obj_list1 = font1.getGlyphNames()[1 :]  # 获取所有字符的对象，去除第一个和最后一个
        uni_list1 = font1.getGlyphOrder()[1 :]
        font2 = TTFont('人人车01.ttf')
        obj_list2 = font2.getGlyphNames()[1 :]  # 获取所有字符的对象，去除第一个和最后一个
        uni_list2 = font2.getGlyphOrder()[1 :]
        dict = {'zero' : '0', 'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
                'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8', 'nine' : '9'}
        dict1 = {'zero' : '0', 'one' : '1', 'two' : '2', 'four' : '3', 'three' : '4', 'five' : '5', 'seven' : '6',
                 'nine' : '7', 'six' : '8', 'eight' : '9'}
        ''' 遍历加密的内容text,在新的ttf文件中查找每一个text的元素。如果找到，则替换'''
        for a in text :
            for uni2 in uni_list2 :
                # print(uni2)
                try :
                    id = dict[str(uni2)]  # 找到unit2未加密对应的数字
                except :
                    continue
                id_1 = font2.getGlyphID(str(uni2))  # Z找到unit2在ttf文件中的id
                obj2 = font2['glyf'][uni2]
                # str(id) != str(id_1):  # 若未加密的数字id和ttf中对应的id_1不相等，说明a加密了
                if str(id) == str(a) :
                    for uni1 in uni_list1 :

                        obj1 = font1['glyf'][uni1]
                        if obj1 == obj2 :
                            text = text.replace(a, dict1[uni1])
        return text
