from lxml import etree
import requests
import os

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
}

def get_name(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    tree = etree.HTML(r.text)
    title = tree.xpath('// *[@id="maininfo"]/div[1]/h1/text()')[0]
    print(f'小说的名字是{title}')
    return title

def mkfolder(folder_name):
    if not os.path.exists(folder_name):
        print('文件夹不存在，先创建文件夹')
        os.makedirs(folder_name)
    # 切换到文件件中
    os.chdir(folder_name)

def get_catalogue(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    tree = etree.HTML(r.text)
    title = tree.xpath('//*[@id="chapterlist"]/li/a/text()')
    link = tree.xpath('//*[@id="chapterlist"]/li/a/@href')
    catalog = list(zip(title, link))
    print(catalog)
    return catalog

def extract_data(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    tree = etree.HTML(r.text)
    title = tree.xpath('//*[@id="mains"]/div[1]/h1/text()')[0]
    content = tree.xpath('//*[@id="book_text"]//text()')
    # 将返回的列表转化成字符串，strip()方法去除元素左右的空格或回车
    content = ('\n'.join([i.strip() for i in content]))
    # 以元组（title, content）的形式进行返回
    return title, content

# 将爬到的小说文本和标题以txt格式保存到本地
def save_to_file(title, content):
    print(title + "开始保存！")
    with open(f'{title}.txt', 'w', encoding='utf-8')as f:
        f.write(content)
    print(title + "保存成功！")

base_url = 'https://www.tsxs.org'
url = 'https://www.tsxs.org/121/121401/'
def run_spider():
    # url = input('请输入要抓取的小说地址：')
    name = get_name(url)
    mkfolder(f'./{name}')
    catalog = get_catalogue(url)
    for _, link in catalog:
        full_link = f'{base_url}{link}'
        title, content = extract_data(full_link)
        save_to_file(title, content)
    print('整部小说都下载完了！')

if __name__ == '__main__':
    run_spider()