#! python3
# crawler_keyaki.py - 欅メンバーのプロフィールをHPから取得し、JSONに記述する
import urllib.request
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# CromeドライバーにHPを読み込ませる
driver = webdriver.Chrome()
driver.get("http://www.keyakizaka46.com/s/k46o/search/artist?ima=0000")


# メンバープロフィール取得
with urllib.request.urlopen('http://www.keyakizaka46.com/s/k46o/search/artist?ima=0000') as response:
   html = response.read()
soup = BeautifulSoup(html, "html.parser")

# メンバー情報
dict = {}

members= soup.select('li[data-member]')

for i in range(0,len(members)):
    if(i < 10):
        i = str(str(0) + str(i))
    try:
        li = driver.find_element_by_xpath("//*[@data-member='{}']".format(i))
        li.click()

        # 画像
        img = driver.find_element_by_xpath("//div[@class='box-profile']/div/img").get_attribute("src")
        # 名前
        name = driver.find_element_by_css_selector('.name').text
        # ふりがな
        hurigana = driver.find_element_by_css_selector('.furigana').text
        # メンバー情報
        boxinfo = driver.find_elements_by_xpath("//div[@class='box-info']/dl/dt")
        # 生年月日
        birth = boxinfo[0].text
        # 星座
        constellation = boxinfo[1].text
        # 身長
        length = boxinfo[2].text
        # 出身地
        location = boxinfo[3].text
        # 血液型
        blood_type = boxinfo[4].text

        #TODO:メンバー情報を取得してjsonファイルに落とす

        dict["id" + str(i)] \
        = {
                "画像": img,
                "名前": name,
                "ふりがな": hurigana,
                "生年月日": birth,
                "星座": constellation,
                "身長": length,
                "出身地": location,
                "血液型": blood_type
            }

        print(dict)
        # メンバー一覧に戻る
        driver.back()

    except Exception as e:
        print(e)
f = open("keyaki.json", "w")
json.dump(dict, f, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))

print("Dump DONE")
print("Success")
