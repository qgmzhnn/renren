import  requests
from lxml import etree
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

}
class HtmlDownloader(object):
    def download(self,page):
        if page is None:
            return None
        r=requests.get(url='https://www.renrenche.com/nc/ershouche/p{}/'.format(page),headers=headers)
        text = r.text
        tree = etree.HTML(text)
        list = tree.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        urls=set()
        for car in list :
            car_url = 'https://www.renrenche.com' + car.xpath('a')[0].attrib['href']
            urls.add(car_url)
        return urls