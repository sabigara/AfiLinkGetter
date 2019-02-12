
import amazon.api
import os
import subprocess
from PIL import Image, ImageTk
import PIL
import requests
from io import BytesIO
import tkinter as tk
from tkinter import *
import sys
from collections import namedtuple
from PyInquirer import prompt
from ShGetter.main import get_product_sh


access_key_id = os.environ['AWS_ACCESS_KEY_ID']
secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
associate_tag = os.environ['ASSOCIATE_TAG']
region = os.environ['AWS_REGION']

amazon = amazon.api.AmazonAPI(access_key_id, secret_access_key, associate_tag, Region=region)

image_list = []
image_index = 0

root = Tk() 
root.geometry("600x600")

panel = tk.Label(root)

def main(keywords: str, get_am=True, get_sh=True) -> int:
    setup_tkinter()

    img_urls: [str] = []
    am: namedtuple = None
    sh: namedtuple = None
    if get_am:
        am: namedtuple = get_product_am(keywords)
        img_urls += am.img_urls
    if get_sh:
        sh: namedtuple = get_product_sh(keywords)
        img_urls += sh.img_urls

    img_url = prompt_choose_img(img_urls)

    short_code = create_shortcode(am=am, sh=sh, img_url=img_url)

    output(short_code)
    make_sound()    
    
    return 0

def get_product_am(keywords: str) -> namedtuple:
    products = search_product_am(keywords)
    product = prompt_choose_product_am(products)

    afi_url = product.detail_page_url

    am = namedtuple('am', ('product_url', 'img_urls'))
    am.product_url = afi_url
    am.img_urls = [image.LargeImage.URL.text for image in product.images]
    return am

def search_product_am(keywords: str) -> amazon.api.AmazonSearch:
    for i in range(4):
        try:
            product = amazon.search(Keywords=keywords, SearchIndex='All')
            break
        except Exception as e:
            print(type(e), e.args, e)
            sys.exit('商品データ取得に失敗しました・・・_(._.)_')
    
    return product


def prompt_choose_product_am(products: amazon.api.AmazonSearch) -> amazon.api.AmazonProduct:
    product_list = [product for product in list(enumerate(products))]
    product_name_list = [f'{product[0]} {product[1].title}\n \
                        {product[1].detail_page_url.replace("&tag=sabigara-22", "")}\n' \
                        for product in product_list]
    question = [
        {
            'type': 'list',
            'name': 'products',
            'message': 'What do you want to do?',
            'choices': product_name_list
        }
    ]
    answer = prompt(question)
    index = int(answer['products'][0:1])
    return product_list[index][1]

def prompt_choose_img(img_urls: [str]) -> str:

    index = 0
    for image_url in img_urls:
        res = requests.get(image_url)
        img = PIL.Image.open(BytesIO(res.content))

        img_tk = ImageTk.PhotoImage(img)

        image_list.append(img_tk)

        index += 1

    update_img()
    root.mainloop()

    return img_urls[image_index]

def create_shortcode(img_url: str, am: namedtuple, sh: namedtuple) -> str:
    am_product_url = ''
    sh_product_url = ''
    if am:
        am_product_url = am.product_url
    if sh:
        sh_product_url = sh.product_url

    return f'[afi amurl="{am_product_url}" shurl="{sh_product_url}" img_url="{img_url}"]'

def output(short_code: str) -> None:
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(short_code.encode('utf-8'))

    print(short_code)

def make_sound() -> None:
    os.system('afplay /System/Library/Sounds/Glass.aiff')

def setup_tkinter():
    root.bind('<Left>', show_prev)
    root.bind('<Right>', show_next)

    panel.pack(side="bottom", fill="both", expand="yes")
    panel.bind("<Button-1>", on_click)
    
def on_click(event):
    root.quit()

def show_prev(event):
    global image_index

    if not image_index <= 0:
        image_index -= 1

        update_img()


def show_next(event):
    global image_index

    if not image_index >= (len(image_list) - 1):
        image_index += 1

        update_img()


def update_img():
    panel.configure(image=image_list[image_index])
    panel.image = image_list[image_index]


if __name__ == '__main__':
    keywords = ''    
    if len(sys.argv) > 2:
        keywords = sys.argv[2]
        if sys.argv[1] == 'a':
            main(keywords, True, False)
        elif sys.argv[1] == 's':
            main(keywords, False, True)
    elif len(sys.argv) == 2:
        keywords = sys.argv[1]
        main(keywords)
    else:
        sys.exit('Arguments error')

