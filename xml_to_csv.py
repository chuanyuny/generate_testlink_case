# -*-coding:utf-8 -*-

import xml.dom.minidom
import csv
import html
import re

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

if __name__ == "__main__":
    dom = xml.dom.minidom.parse('test.xml')
    root = dom.documentElement
    testcase = root.getElementsByTagName("testcase")
    print("测试用例总数为 %d 条"%len(testcase))
    for each in testcase:
        li=[]
        path_li=get_case_path_list(li,each)
        str1=each.getAttribute("name")
        str2="none" if not ObjectExist(each.getElementsByTagName("preconditions")[0]) else each.getElementsByTagName("preconditions")[0].firstChild.data.replace("<p>", "").replace("</p>","").replace("\n", "")
        path_li.append(html.unescape(str1).split("ycy"))
        path_li.append(html.unescape(str2).split("ycy"))
        print(path_li)
        write_to_csv("aa.csv",path_li)

        step = each.getElementsByTagName("step")
        for item in step:
            li2=[]
            number = "default_number" if not ObjectExist(item.getElementsByTagName("step_number")[0]) else item.getElementsByTagName("step_number")[0].firstChild.data
            steps = "default_steps" if not ObjectExist(item.getElementsByTagName("actions")[0]) else item.getElementsByTagName("actions")[0].firstChild.data.replace("<p>", "").replace("</p>","").replace("\n", "")
            expect_result = "default_expect_result" if not ObjectExist(item.getElementsByTagName("expectedresults")[0]) else item.getElementsByTagName("expectedresults")[0].firstChild.data.replace("<p>","").replace("</p>", "").replace("\n", "")
            dr = re.compile(r'<[^>]+>', re.S)
            steps = dr.sub('', html.unescape(steps))
            expect_result = dr.sub('', html.unescape(expect_result))
            li2.append(number)
            li2.append(steps)
            li2.append(expect_result)
            print(li2)
            write_to_csv2("aa.csv", li2)









