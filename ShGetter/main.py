from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import subprocess
import sys
import os
import re
from collections import namedtuple


sh_url = 'https://www.soundhouse.co.jp/search/index/?search_all='


def get_product_sh(query: str) -> namedtuple:
    with webdriver.Chrome() as driver:
        driver.get(sh_url + query)
        driver.find_element_by_xpath('//*[@id="globalContents"]/div/ul[1]/li[1]/div[1]/a').click()

        driver.implicitly_wait(20)

        img_url = driver.find_element_by_id('target').get_attribute('src')

        product_url = driver.current_url

        afi_url = f'http://h.accesstrade.net/sp/cc?rk=01001xqc00itei&url={product_url}" rel="nofollow" target="_blank"'

        sh = namedtuple('sh', ('img_urls', 'product_url'))
        sh.img_urls = [img_url]
        sh.product_url = afi_url
        return sh
        # driver.get(access_trade_url)

        # user_in = driver.find_element_by_xpath('//*[@id="login_p"]/form/label[1]/input')
        # passwd_in = driver.find_element_by_xpath('//*[@id="login_p"]/form/label[2]/input')
        # user_in.send_keys(user_id)
        # passwd_in.send_keys(password)
        # submit = driver.find_element_by_xpath('//*[@id="login_p"]/form/input')
        # submit.click()

        # driver.get(sh_program_url)

        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "bannerTypeId")))

        # select_item = Select(driver.find_element_by_xpath('//*[@id="bannerTypeId"]'))
        # select_item.select_by_index(2)
        # driver.find_element_by_xpath('//*[@id="search_btn"]').click()
        # driver.find_element_by_xpath('//*[@id="goodsDetailURL"]').send_keys(item_url)
        # driver.find_element_by_xpath('//*[@id="goodsImageURL"]').send_keys(item_img)
        # driver.find_element_by_xpath('//*[@id="create_link_btn"]').click()

        # code = driver.find_element_by_xpath('//*[@id="result_box"]/div[2]/section[2]/div[1]/textarea').text

        # url = re.findall(r'"([^"]*)"', code)

        # code_enclosed = '<div class="soundhouse">' + code + \
        #                 '<div class="btn-wrap"><a href="' + url[0] + '" target="_blank">' + \
        #                 'Soundhouseで詳細を見る</a></div></div>'

        # script_location = os.path.realpath(
        #         os.path.join(os.getcwd(), os.path.dirname(__file__)))

        # with open(os.path.join(script_location, 'urls.txt'), 'a', encoding='utf-8') as writer:
        #         writer.write('\n' + query + ':\n' + code_enclosed + '\n')

        # コメントを外すとクリップボードにテキストをコピーします
        # process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        # process.communicate(enclosed_html.encode('utf-8'))

        # コメントを外すと終了時に音が鳴ります(Mac限定)
        # os.system('afplay /System/Library/Sounds/Glass.aiff')
        

if __name__ == "__main__":
    get_product_sh(sys.argv[1])