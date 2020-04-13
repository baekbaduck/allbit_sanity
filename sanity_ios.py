import unittest
import os
from appium import webdriver
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import time

from kucoin.client import Client

api_key = '5da8173338300c5593ce60cb'
api_secret = '1656f653-6d7e-483f-8360-4e9df8d43d2d'
api_passphrase = 'qwerasdf1234!'

client = Client(api_key, api_secret, api_passphrase)
depth = client.get_order_book('ETH-BTC')


driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723/wd/hub',
    desired_capabilities={
        "platformName": "iOS",
        "platformVersion": "13.1.3",
        "deviceName": "<디바이스 이름>>",
        "app": "/Users/xxx/xxx_internal.ipa",
        "automationName": "XCUITest",
        "bundleId": "com.ozys.xxx.internal",
        "udid": "<udid 기입>",
        "noReset": "true",
        "appActivity": "com.xxx.SplashActivity",
        "newCommandTimeout": 7200,
        "xcodeOrgId": "<애플 개발자 코드 입력>",
        "xcodeSigningId": "iPhone Developer"
    })
# 첫 스플래쉬
driver.implicitly_wait(5)
driver.find_element_by_accessibility_id("btn_dismiss_dialog").click()

# 아무키나 눌러주세요.
def wait():
    m.getch()

# 로그인
def Login(usedId, userPw):
    try:
        driver.find_element_by_accessibility_id("계정").click()
        # driver.find_element_by_xpath("//XCUIElementTypeButton[@name=\"계정\"]")
        driver.find_element_by_accessibility_id("btn_login").click()
        id_input = driver.find_element_by_xpath("//XCUIElementTypeTextField")
        id_input.send_keys(usedId)
        pw_input = driver.find_element_by_xpath("//XCUIElementTypeSecureTextField")
        pw_input.send_keys(userPw)
        driver.find_element_by_accessibility_id("로그인").click()

    except Exception as e:
        print("로그인 선택이 불가합니다. 이미 로그인 되어 있는지 확인해주세요.")

    input("캡차가 통과되었으면 ENTER를 눌러주세요.")
    driver.find_element_by_accessibility_id("거래소").click()

# 지갑 선택
def WalletSelect():
    driver.find_element_by_accessibility_id("계정").click()
    driver.find_element_by_xpath("//XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]").click()

    print('1. 첫번째 지갑')
    print('2. 두번째 지갑')
    numberwallet = input('선택하세요 : ')
    try:
        if numberwallet == "1":
            wallet_1 = driver.find_element_by_xpath("(//XCUIElementTypeButton[@name=\"ic wallet checkbox\"])[1]")
            wallet_1.click()
        elif numberwallet == "2":
            wallet_2 = driver.find_element_by_xpath("(//XCUIElementTypeButton[@name=\"ic wallet checkbox\"])[2]")
            wallet_2.click()

        # 다른 월렛 선택시 딜레이 필요
        time.sleep(2)

        # xpath 설정이 불가하여 TouchAction으로 직접 선택
        TouchAction(driver).tap(x=295, y=45).perform()
        TouchAction(driver).tap(x=350, y=45).perform()

        time.sleep(2)
        # driver.back()
        driver.find_element_by_accessibility_id("거래소").click()

    except Exception as e:
        print(e)

# 매수하기
def BTC_ETH_BUY():
    try:
        driver.find_element_by_accessibility_id("거래소").click()
        BTC_ETH = driver.find_element_by_xpath(
            "//XCUIElementTypeApplication[@name=\'올비트\']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]")
        BTC_ETH.click()
        driver.find_element_by_accessibility_id("25%").click()

        # 여기서부터 이어서 작성필요 10.16(수)
        read_price = driver.find_element_by_accessibility_id("textfield_trading_price")

        price_half = depth.get('asks')[0][0].replace("'", "")
        # 현재가의 절반가로 구매
        set_price_half = float(price_half) / 2
        set_price_half = round(set_price_half, 8)
        set_price_half = str(set_price_half)

        read_price.click()
        for x in range(10):
            read_price.send_keys(Keys.DELETE)
        driver.implicitly_wait(3)

        input_price = driver.find_element_by_accessibility_id("textfield_trading_price")
        input_price.clear()
        input_price.send_keys(set_price_half)

        driver.find_element_by_xpath('//XCUIElementTypeWindow[1]').click()

        driver.find_element_by_accessibility_id("매수하기").click()
        second_pwd("001234")

        driver.implicitly_wait(5)
        driver.find_element_by_accessibility_id("button_finish_auth").click()
        driver.find_element_by_accessibility_id("거래소").click()
    except Exception as e:
        print(e)
        print("생체인증이 설정되어 있을 시 직접 인증하셔야 합니다.")

def BTC_ETH_CANCEL():
    try:
        driver.find_element_by_accessibility_id("자산관리").click()

        driver.find_element_by_accessibility_id("management_orderlist_dropdown_parent").click()
        driver.find_element_by_xpath("//XCUIElementTypeOther[@name=\'management_orderlist_dropdown\']/XCUIElementTypeOther[2]/XCUIElementTypeTable/XCUIElementTypeCell[2]").click()
        driver.find_element_by_xpath("(//XCUIElementTypeButton[@name=\"button_cancel_order\"])[1]").click()
        second_pwd("001234")
        time.sleep(2)

        driver.find_element_by_accessibility_id("button_finish_auth").click()
        driver.find_element_by_accessibility_id("거래소").click()
    except Exception as e:
        print(e)
        print("취소할 주문이 없거나 동작 중 오류가 발생하였습니다.")

def ETH_BTC_SELL():
    try:
        driver.find_element_by_accessibility_id("거래소").click()
        driver.find_element_by_accessibility_id("ETH").click()
        ETH_BTC = driver.find_element_by_xpath(
            "//XCUIElementTypeApplication[@name=\’올비트\’]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]")
        ETH_BTC.click()

        driver.find_element_by_accessibility_id("매도").click()
        driver.find_element_by_id("com.xxx.internal.debug:id/amount_radio_25p").click()

        read_price = driver.find_element_by_accessibility_id("textfield_trading_price")
        price_2x = read_price.text
        # 현재가의 2배가로 구매
        set_price_2x = float(price_2x) * 2
        set_price_2x = round(set_price_2x, 8)
        set_price_2x = str(set_price_2x)

        read_price.click()
        driver.implicitly_wait(3)
        input_price = driver.find_element_by_accessibility_id("textfield_trading_price")
        input_price.clear()
        input_price.send_keys(set_price_2x)

        #driver.back()
        driver.find_element_by_xpath('//XCUIElementTypeWindow[1]').click()
        second_pwd("001234")

        driver.implicitly_wait(5)
        driver.find_element_by_accessibility_id("button_finish_auth").click()
        #driver.back()
        driver.find_element_by_accessibility_id("거래소").click()

    except Exception as e:
        print(e)
        print("동작 중 오류가 발생하였습니다.")

def ETH_BTC_CANCEL():
    try:
        driver.find_element_by_accessibility_id("자산관리").click()
        driver.find_element_by_accessibility_id("management_orderlist_dropdown_parent").click()
        driver.find_element_by_xpath("//XCUIElementTypeOther[@name=\'management_orderlist_dropdown\']/XCUIElementTypeOther[2]/XCUIElementTypeTable/XCUIElementTypeCell[3]").click()
        driver.find_element_by_xpath("(//XCUIElementTypeButton[@name=\"button_cancel_order\"])[1]").click()
        second_pwd("001234")
        time.sleep(2)

        driver.find_element_by_id("com.xxx.internal.debug:id/btn_ok").click()
        driver.find_element_by_accessibility_id("거래소").click()
    except Exception as e:
        print(e)

def second_pwd(walletPw):
    try:
        driver.find_element_by_accessibility_id("textfield_auth_second_password").send_keys(walletPw)

        #현재 앱에서는 hide_keyboard 동작 불가
        #driver.hide_keyboard()
        #TouchAction을 활용하여 키보드를 내림
        TouchAction(driver).tap(x=150, y=75).perform()

        driver.find_element_by_accessibility_id("button_auth_next").click()
        driver.find_element_by_xpath("//XCUIElementTypeButton[@name=\"취소\"]").click()
    except Exception as e:
        print(e)
        print("동작중 오류가 발생하였습니다.")

def exchange_search(token):
    try:
        driver.find_element_by_accessibility_id("거래소").click()
        driver.find_element_by_id("com.xxx.internal.debug:id/search_button").click()
        driver.find_element_by_id("com.xxx.internal.debug:id/search_src_text").send_keys(token)
        driver.find_element_by_xpath(
            "//android.widget.LinearLayout[1]/android.widget.FrameLayout/android.view.ViewGroup").click()
        driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="위로 이동"]')
        x = 0
        for x in range(5):
            driver.back()
        driver.find_element_by_accessibility_id("거래소").click()
    except Exception as e:
        print(e)
        print("동작중 오류가 발생하였습니다.")

Login("<로그인 아이디>", "<암호>")

number = ""
while number != "8":
    print('확인할 케이스를 선택하세요')
    print()
    print('1. 로그인')
    print('2. 지갑선택')
    print('3. 거래소 코인 검색')
    print('4. 매수하기')
    print('5. 매수 취소하기')
    print('6. 매도하기')
    print('7. 매도 취소하기')
    print('8. 끝내기')
    number = input('선택하세요 : ')

    if number == "1":
        Login("<로그인 아이디>", "<암호>")
    elif number == "2":
        WalletSelect()
    elif number == "3":
        # exchange_search("trx")
        print('아이폰은 거래소 내 검색을 제공하지 않습니다.')
    elif number == "4":
        BTC_ETH_BUY()
    elif number == "5":
        BTC_ETH_CANCEL()
    elif number == "6":
        ETH_BTC_SELL()
    elif number == "7":
        ETH_BTC_CANCEL()
    if number == "8":
        driver.quit()
        sys.exit(1)
        break
