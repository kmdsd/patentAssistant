import requests
import re
import os

# 定数定義
keyword_st = '発明を実施するための形態'
keyword_ed = '符号の説明'

# APIが社内(IIS)の場合
proxies = {
    "http": None,
    "https": None,
}

def pickup_text(base_text):
    
    global keyword_st
    global keyword_ed

    # 文中の記号を置換する
    base_text = base_text.replace('<SUP>','^')
    base_text = base_text.replace('</SUP>','')
    base_text = base_text.replace('<SUB>','_')
    base_text = base_text.replace('</SUB>','')
    
    # HTMLタグで分割
    work_text = re.split('<[A-Z]{2,}>|</[A-Z]{2,}>',base_text)
    main_text = [s for s in work_text if '書類名' in s]
    
    # 文章の修正
    main_text_work = re.sub('【[０-９]{4}】','', main_text[0])
    main_text_work_1 = re.sub('　|\r\n', '', main_text_work)
    main_text_list = re.split('【|】', main_text_work_1)
    
    method_idx_st = main_text_list.index(keyword_st)
    method_idx_ed = main_text_list.index(keyword_ed)
    
    return '.'.join(main_text_list[method_idx_st+1:method_idx_ed])

def get_patent_info(patent_no):
    url = f'https://patsrv66.konicaminolta.org/kouho/{patent_no}/{patent_no}.htm'
    res = requests.get(url, proxies=proxies)
    return res

def main(patent_no):
    
    responce = get_patent_info(patent_no)
    
    if responce.status_code == 200:
        responce.encoding = 'shift_jis'
        target_txt = responce.text
        result_txt = pickup_text(target_txt)
        print(len(result_txt))
        if os.path.isdir('temp') == False:
            os.mkdir('temp')
        path = f'./temp/{patent_no}.txt'
        with open(path, mode='w') as f:
            f.write(result_txt[:29000])
    else:
        print('    公報情報なし')

## 実行
if __name__ == "__main__":
    
    patent_no = 'B54400JP01'   
    result = main(patent_no)
    
    print(result)
    
    path = f'./{patent_no}.txt'
    with open(path, mode='w') as f:
        f.write(result)




