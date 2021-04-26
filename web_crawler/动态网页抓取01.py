import requests
def get_book_info(page_num):
    url = 'https://www.epubit.com/pubcloud/content/front/portal/getUbookList'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Origin-Domain': 'www.epubit.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    params = (
        ('page', '1'),
        ('row', '20'),
        ('', ''),
        ('startPrice', ''),
        ('endPrice', ''),
        ('tagId', ''),
    )
    response = requests.get(url = url, headers=headers, params=params).json()
    return response
def extract_data(json):
    books_list = json['data']['records']
    for i in books_list:
        print(f"书名：{i['name']},价格：{i['price']}")

def get_data():
    for num in range(1,20):
        json_data = get_book_info(num)
        extract_data(json_data)

if __name__ =='__main__':
    get_data()