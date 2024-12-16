import time
from typing import Any

from playwright.sync_api import sync_playwright
import pandas as pd


def run_playwright(telelist: list):
    with sync_playwright() as p:
        # * executable_path
        executable_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # ! 使用本地chrome

        browser = p.chromium.launch(
            executable_path=executable_path, headless=False)
        page = browser.new_page()
        page.goto("https://msc.yoao.com/#home/index/index", timeout=60000)

        print("请登录并操作页面到搜索位置,完成后按照屏幕提示操作\n")

        num = input("请输入一个数字:\n")
        if num != "1":
            print("输入错误，退出")
            return
        time.sleep(15)
        # <input name="mobile" placeholder="请输入" type="number" id="mobile" data-__meta="[object Object]" data-__field="[object Object]" class="ant-input" value="">

        for telenum in telelist:
            print(telenum)
            page.fill('input[name="mobile"]', telenum)
            time.sleep(2)
            page.click('button[type="submit"]')
            
            time.sleep(15)
            # <div tabindex="-1" class="ant-table-body" style="max-height: calc(-280px + 100vh); overflow-y: scroll;"><table class=""><colgroup><col style="width: 120px; min-width: 120px;"><col style="width: 100px; min-width: 100px;"><col style="width: 250px; min-width: 250px;"><col style="width: 100px; min-width: 100px;"><col style="width: 100px; min-width: 100px;"></colgroup><tbody class="ant-table-tbody"><tr class="ant-table-row ant-table-row-level-0" data-row-key="C003367239"><td class="ant-table-row-cell-break-word">6977355037</td><td class="ant-table-row-cell-break-word">周世浩</td><td class="ant-table-row-cell-break-word"><div style="display: flex;"><span><div style="display: block;"><div class="ant-row antd-pro-common-components-attribution-index-create"><div class="ant-col" style="min-width: 260px; text-align: left; position: relative; display: flex; align-items: center; border: 1px solid rgb(204, 204, 204); height: 48px; background-color: rgb(255, 255, 255); padding-left: 10px;"><i aria-label="图标: lock" class="anticon anticon-lock" style="color: rgb(24, 144, 255); font-size: 24px;"><svg viewBox="64 64 896 896" focusable="false" class="" data-icon="lock" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M832 464h-68V240c0-70.7-57.3-128-128-128H388c-70.7 0-128 57.3-128 128v224h-68c-17.7 0-32 14.3-32 32v384c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V496c0-17.7-14.3-32-32-32zM332 240c0-30.9 25.1-56 56-56h248c30.9 0 56 25.1 56 56v224H332V240zm460 600H232V536h560v304zM484 701v53c0 4.4 3.6 8 8 8h40c4.4 0 8-3.6 8-8v-53a48.01 48.01 0 1 0-56 0z"></path></svg></i><div style="border-left: 1px solid rgb(204, 204, 204); height: 100%; padding-left: 5px; margin-left: 10px; line-height: 1.5;"><p>（销售线）销售人员：张俊琴</p><p>组织机构：共创客服</p></div></div></div></div><div style="display: block;"></div></span></div></td><td class="ant-table-row-cell-break-word">实名认证客户</td><td class="ant-table-row-cell-break-word">系统思维</td></tr></tbody></table></div>
            table_body_ele = page.query_selector('div.ant-table-body')
            if table_body_ele is not None:
                print("找到table")
                print(table_body_ele.text_content())
                if table_body_ele.text_content() == "":
                    print("未找到")
                    #! 清空输入框
                    time.sleep(5)
                    page.fill('input[name="mobile"]', "")
                    
                    continue
                else:
                    print("找到")
                    print(table_body_ele.text_content())
                    #! <svg viewBox="64 64 896 896" focusable="false" class="" data-icon="lock" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M832 464h-68V240c0-70.7-57.3-128-128-128H388c-70.7 0-128 57.3-128 128v224h-68c-17.7 0-32 14.3-32 32v384c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V496c0-17.7-14.3-32-32-32zM332 240c0-30.9 25.1-56 56-56h248c30.9 0 56 25.1 56 56v224H332V240zm460 600H232V536h560v304zM484 701v53c0 4.4 3.6 8 8 8h40c4.4 0 8-3.6 8-8v-53a48.01 48.01 0 1 0-56 0z"></path></svg>
                    #todo 判断icon的属性是否是lock
                    islock = table_body_ele.find('svg[data-icon="lock"]')
                    if islock is not None:
                        print("未锁定")
                        
                        with open('result.txt', "a") as f:
                            f.write( "联系人电话:" + telenum + " " + "未锁定"+ table_body_ele.text_content() + "\n")
                    else:
                        print("锁定")
                        with open('result.txt', "a") as f:
                            f.write( "联系人电话:" + telenum + " " + "锁定"+ table_body_ele.text_content() + "\n")
                    #! 清空输入框
                    page.fill('input[name="mobile"]', "")
                    time.sleep(5)
                
            time.sleep(10)
            #! 清空输入框
            page.fill('input[name="mobile"]', "")

        time.sleep(200000000)
        browser.close()


def read_xlsx() -> list | None:
    file_path = "./utils/data.xlsx"
    try:
        data = pd.read_excel('./utils/data.xlsx')
    # ? 只要第1列
        tele = data.iloc[:, 2]
    # ? 转换为list
        telelist = tele.tolist()
        # ! 要前20个
        telelist = telelist[:5]
        #! 遍历元素 如果元素充包含1个或者多个分号,根据分号分解成两个或者多个元素
        split_data = []
        for item in telelist:
        # 判断是否包含分号
            if ';' in item:
            # 根据分号分解成多个元素
                split_data.extend(item.split(';'))
            else:
            # 如果没有分号，则原样保留
                split_data.append(item)
        print(len(split_data))
        split_data[2] = '13301561910'
        split_data[4] = '18861613634'
        return split_data
    except Exception as e:
        print(e)
        return None


def dojob():
    print("dojob")
    telephone_list = read_xlsx()
    if telephone_list is None:
        print("read_xlsx failed")
        return
    run_playwright(telephone_list)


if __name__ == "__main__":
    dojob()
    # read_xlsx()
