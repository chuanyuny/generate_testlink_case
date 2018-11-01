# -*-coding:utf-8 -*-

import xml.dom.minidom
import csv
import html
import re
import pandas


def get_case_path_list(li,element):
    if element.parentNode:
        try:
            if element.parentNode.getAttribute("name") != '':
                li.insert(0,html.unescape(element.parentNode.getAttribute("name")).split("ycy"))
        except:
            pass
        finally:
            element = element.parentNode
            get_case_path_list(li,element)
    return li

def write_to_csv(path,li):
    csvfile = open(path,"a",newline="",errors="ignore")
    writer=csv.writer(csvfile)
    m=len(li)
    for i in range(m):
        writer.writerow(li[i])
    csvfile.close()

def write_to_csv2(path,li):
    csvfile = open(path,"a",newline="",errors="ignore")
    writer=csv.writer(csvfile)
    writer.writerow(li)

def ObjectExist(str1):
    # ex: str1 = each.getElementsByTagName("preconditions")[0]
    try:
        str1.firstChild.data.replace("<p>", "").replace("</p>","").replace("\n", "")
    except:
        return False
    else:
        return True

def test_type(li): #li 为嵌套的列表
    '''

    :param li:
    :return: 返回列表，
    '''
    str1 = ""
    for each in li:
        str1 = str1 + each[0] + '\n'
    return str1

if __name__ == "__main__":
    header = ["测试类型", "测试标题", "前提条件", "测试步骤", "预期结果"]
    write_to_csv2("aa.csv", header)
    dom = xml.dom.minidom.parse('test.xml')
    root = dom.documentElement
    testcase = root.getElementsByTagName("testcase")
    print("测试用例总数为 %d 条"%len(testcase))
    for each in testcase:
        li_sum=[]  # 包含测试类型，测试标题，前提条件，测试步骤，预期结果
        li=[] #仅用来存在用例路径的。
        path_li=get_case_path_list(li,each)
        str1=each.getAttribute("name")  #测试用例标题
        str2="none" if not ObjectExist(each.getElementsByTagName("preconditions")[0]) else each.getElementsByTagName("preconditions")[0].firstChild.data.replace("<p>", "").replace("</p>","").replace("\n", "")
        #str2 表示测试用例前提条件
        li_sum.append(test_type(path_li))
        li_sum.append(html.unescape(str1))
        li_sum.append(html.unescape(str2))
        # print(li_sum)
        case_step=""  #测试用例步骤
        result=""
        for i in range(len(each.getElementsByTagName("step_number"))):
            dr = re.compile(r'<[^>]+>', re.S)
            number = "default_number" if not ObjectExist(each.getElementsByTagName("step_number")[i]) else \
            each.getElementsByTagName("step_number")[i].firstChild.data
            steps = "default_steps \n" if not ObjectExist(each.getElementsByTagName("actions")[i]) else \
            each.getElementsByTagName("actions")[i].firstChild.data.replace("<p>", "").replace("</p>", "").replace("\n",
                                                                                                                   "")+'\n'
            expect_result = "default_expect_result \n" if not ObjectExist(
                each.getElementsByTagName("expectedresults")[i]) else each.getElementsByTagName("expectedresults")[
                i].firstChild.data.replace("<p>", "").replace("</p>", "").replace("\n", "")+'\n'

            steps = dr.sub('', html.unescape(steps))
            expect_result = dr.sub('', html.unescape(expect_result))
            case_step=case_step+number+steps
            result=result+expect_result

        li_sum.append(case_step)
        li_sum.append(result)
        print(li_sum)
        write_to_csv2("aa.csv",li_sum)










