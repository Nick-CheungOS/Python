from DrissionPage import ChromiumPage
import datetime
import csv
from time import sleep

# 创建页面对象
page = ChromiumPage()

work_name = ['python', 'java', 'web', '测试', '运维' ]  # 创建需要被爬取数据的岗位名称(修改查询名称需要修改的值)

# 设置记录岗位数量的变量(修改查询名称需要修改的值)
first = 0
second = 0
third = 0
fourth = 0
fifth = 0

# 创建CSV文件记录爬取数据
with open(f'广州_Boss_{datetime.date.today()}.csv', 'w', encoding='utf-8', newline='') as filename:
    csv_dictwriter = csv.DictWriter(filename, fieldnames=[
        '岗位名称',
        '公司名称',
        '薪资',
        '福利待遇',
    ])
    csv_dictwriter.writeheader()
    for name in work_name:  # 按顺序遍历,开始逐个爬取work_name的相关数据
        for i in range(1, 11):  # boss平台最多显示10页内容
            print(f'----------------------------正在爬取{name}的第{i}页数据---------------------------------------')

            # 访问网页
            page.get(
                f'https://www.zhipin.com/web/geek/job?query={name}&city=101280100&experience=102&degree=203&page={i}')
            sleep(2.8)  # 等待数据加载
            # 如果页面出现弹窗将自动关闭
            wrap = page('.boss-login-dialog', timeout=2)
            if wrap:
                wrap.ele('.boss-login-close').click()
            else:
                pass

            # 如果超出了该岗位的检索数量就自动爬取下一个岗位
            if page.s_ele('t:div').ele('.job-empty-box'):  # 用于判断检索是否超出
                print("此页码已无内容,该岗位名称已爬取完毕")
                break
            else:
                pass

            # 通过路径获取目标元素
            links = page.ele('.job-list-box')
            for mov in page.eles('.job-card-wrapper'):
                # 获取需要的信息
                jos_name = mov('.job-name').text
                company_name = mov('.company-name').text
                salary = mov('.salary').text
                benefits = mov('.info-desc').text
                dict = {
                    '岗位名称': jos_name,
                    '公司名称': company_name,
                    '薪资': salary,
                    '福利待遇': benefits
                }
                csv_dictwriter.writerow(dict)
                print(dict)

                # 给记录岗位数量的变量作赋值(修改查询名称需要修改的值)
                if name == 'python':
                    first += 1
                elif name == 'java':
                    second += 1
                elif name == 'web':
                    third += 1
                elif name == '测试':
                    fourth += 1
                else:
                    fifth += 1

filename.close()

# 数据可视化制作
import pyecharts.options as opts
from pyecharts.charts import Pie

x_data = ['python', 'java', 'web', '测试', '运维' ]  # (修改查询名称需要修改的值)
y_data = [first , second, third, fourth, fifth ]  # (修改查询名称需要修改的值)
data_pair = [list(z) for z in zip(x_data, y_data)]
data_pair.sort(key=lambda x: x[1])

(
    Pie(init_opts=opts.InitOpts(bg_color="#2c343c"))
    .add(
        series_name="Boss直聘",
        data_pair=data_pair,
        rosetype="radius",
        radius="55%",
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Boss直聘平台互联网相关岗位面向应届生在招岗位状况",
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
    )
    .render("customized_pie.html")
)
