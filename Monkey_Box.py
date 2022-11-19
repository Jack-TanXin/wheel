# coding:utf-8

from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from scipy.stats import kstest, levene, ttest_ind, ttest_rel, mannwhitneyu, wilcoxon


"""测试缺失值"""
def first_a(path):

    """
    :param path: 数据集路径
    :return: 返回缺失值测试结果，并在终端显示
    """

    dataset = pd.read_excel(path)
    result = dataset.isnull().sum()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    text.insert("1.0", result)


def a1():
    path = one.get()
    first_a(path)


"""缺失值处理"""
def second_a(path, name=None, method="均值", num=0):

    """
    :param path: 数据集所在路径
    :param name: 待处理缺失值的列的名称——默认无
    :param method: 处理方式——”均值“（默认）、”中位数“、”众数“、”剔除“、"指定数"
    :param num: 选择方法为 “指定数” 时填补的数值
    :return: 将处理后的数据写入csv文件存放在D盘根目录，名为new_data.csv，并在终端汇报
    """

    dataset = pd.read_excel(path)
    if method == "均值":
        dataset[name].fillna(dataset[name].mean(), inplace=True)
        dataset.to_csv("D:\\new_data.csv")
        text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")
    elif method == "中位数":
        dataset[name].fillna(dataset[name].median(), inplace=True)
        dataset.to_csv("D:\\new_data.csv")
        text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")
    elif method == "指定数":
        dataset[name].fillna(num, inplace=True)
        dataset.to_csv(num)
        text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")
    elif method == "众数":
        dataset[name].fillna(dataset[name].mode()[0], inplace=True)
        dataset.to_csv("D:\\new_data.csv")
        text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")
    elif method == "剔除":
        dataset = dataset.dropna()
        dataset.to_csv("D:\\new_data.csv")
        text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")


def a2():
    path = one.get()
    if two.get() != "":
        name = two.get()
    else:
        name = 0
    if three.get() == "":
        method = "均值"
    else:
        method = three.get()
    if four.get() == "":
        num = 0
    else:
        num = float(four.get())
    second_a(path, name, method, num)


"""数据的特征缩放"""
def third_a(path, method="0-1"):

    """
    :param path: 数据集所在路径
    :param method: 特征缩放的方法：0-1（默认）或 “标准化”
    :return: 将处理后的数据写入csv文件存放在D盘根目录，名为new_data.csv，并在终端汇报
    """

    dataset = np.array(pd.read_excel(path))
    m, n = dataset.shape
    new = np.ones(shape=(m, n))

    if method == "标准化":
        for i in range(0, n):
            mean_num = np.mean(dataset[:, i])
            std_num = np.var(dataset[:, i])
            new[:, i] = (dataset[:, i] - mean_num) / std_num

    if method == "0-1":
        for i in range(0, n):
            new[:, i] = (dataset[:, i] - np.mean(dataset[:, i])) / (np.max(dataset[:, i] - np.min(dataset[:, i])))

    new = pd.DataFrame(new)
    new.to_csv("D:\\new_data.csv")
    text.insert("1.0", "已将处理好的数据存入csv文件放在D盘目录中\n")


def a3():
    path = one.get()
    if two.get() == "":
        method = "0-1"
    else:
        method = two.get()
    third_a(path, method)


"""特征选择"""
def fourth_a(path, method="方差选择法", max_num=None, x=None, y=None):
    dataset = pd.read_excel(path)
    m, n = dataset.shape
    a = np.ones(shape=(1, n))
    b = np.ones(shape=(1, n))

    if method == "方差选择法":
        dataset = np.array(dataset)
        for i in range(0, n):
            a[i] = np.var(dataset[:, i])
            if a[i] < max_num:
                b[i] = 0
        text.insert("1.0", b)

    if method == "互信息":
        X = dataset[x]
        Y = dataset[y]
        # 使用字典统计每一个x元素出现的次数
        d_x = dict()  # x的字典
        for x in X:
            if x in d_x:
                d_x[x] += 1
            else:
                d_x[x] = 1
        # 计算每个元素出现的概率
        p_x = dict()
        for x in d_x.keys():
            p_x[x] = d_x[x] / X.size
        # 使用字典统计每一个y元素出现的次数
        d_y = dict()  # y的字典
        for y in Y:
            if y in d_y:
                d_y[y] += 1
            else:
                d_y[y] = 1
        # 计算每个元素出现的概率
        p_y = dict()
        for y in d_y.keys():
            p_y[y] = d_y[y] / Y.size
        # 使用字典统计每一个(x,y)元素出现的次数
        d_xy = dict()  # x的字典
        for i in range(X.size):
            if (X[i], Y[i]) in d_xy:
                d_xy[X[i], Y[i]] += 1
            else:
                d_xy[X[i], Y[i]] = 1
        # 计算每个元素出现的概率
        p_xy = dict()
        for xy in d_xy.keys():
            p_xy[xy] = d_xy[xy] / X.size
        # 初始化互信息值为0
        mi = 0
        for xy in p_xy.keys():
            mi += p_xy[xy] * np.log(p_xy[xy] / (p_x[xy[0]] * p_y[xy[1]]))
        text.insert("1.0", "二者互信息为%.5f" % mi)


def a4():
    path = one.get()
    if two.get() == "":
        method = "数值"
    else:
        method = two.get()
    if three.get() == "":
        max_num = 10086
    else:
        max_num = float(three.get())

    if four.get() == "":
        x = 10086
    else:
        x = four.get()
    if five.get() == "":
        y = 10086
    else:
        y = five.get()
    fourth_a(path, method, max_num, x, y)


# 单变量分析
def first_b(path, x, method, m=10, n=10):
    dataset = pd.read_excel(path)
    plt.figure(figsize=(m, n))
    sns.set(style="white", color_codes=True)
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams['font.size'] = 12  # 字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    if method == "数值":
        plt.subplot(1, 2, 1)
        sns.histplot(dataset[x], kde=False)
        plt.subplot(1, 2, 2)
        plt.boxplot(dataset[x])
        plt.title(x)

    if method == "分类":
        plt.figure(figsize=(10, 10))
        sns.countplot(x=x, palette='Set2', data=dataset)
        plt.title(x)

    text.insert("1.0", "绘图成功，请在D盘根目录下查看")
    plt.savefig("D:\\绘图结果.jpg")


def a5():
    path = five.get()
    x = six.get()
    method = seven.get()
    if nine.get() == "":
        m = 10
    else:
        m = int(nine.get())
    if ten.get() == "":
        n = 10
    else:
        n = int(ten.get())
    first_b(path, x, method, m, n)


# 多变量分析
def second_b(path, x, y, method, m=10, n=10):
    dataset = pd.read_excel(path)
    plt.figure(figsize=(m, n))
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams['font.size'] = 12  # 字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    if method == "分类-分类标签1":
        sns.set(style="white", color_codes=True)
        sns.countplot(x=y, hue=x, palette='Set2', data=dataset)

    if method == "分类-分类标签2":
        xx = pd.crosstab(dataset[x], dataset[y])
        xx.div(xx.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)

    if method == "数值-分类标签1":
        dataset.groupby(y)[x].mean().plot.bar()

    if method == "数值-分类标签2":
        dataset.groupby(y)[x].median().plot.bar()

    text.insert("1.0", "绘图成功，请在D盘根目录下查看")
    plt.savefig("D:\\绘图结果.jpg")


def a6():
    path = five.get()
    x = six.get()
    y = seven.get()
    method = eight.get()
    if nine.get() == "":
        m = 10
    else:
        m = int(nine.get())
    if ten.get() == "":
        n = 10
    else:
        n = int(ten.get())
    second_b(path, x, y, method, m, n)


# 相关性分析
def third_b(path, method, m=10, n=10, png=None):
    dataset = pd.read_excel(path)
    corrs = dataset.corr(method)
    text.insert("1.0", corrs)

    if png is not None:
        plt.figure(figsize=(m, n))
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams['font.size'] = 12  # 字体大小
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

        sns.heatmap(corrs, annot=True, square="equal", cmap="OrRd")
        text.insert("1.0", "绘图成功，请在D盘根目录下查看")
        plt.savefig("D:\\绘图结果.jpg")


def a7():
    path = five.get()
    method = six.get()
    if nine.get() == "":
        m = 10
    else:
        m = int(nine.get())
    if ten.get() == "":
        n = 10
    else:
        n = int(ten.get())
    if seven.get() != "":
        png = seven.get()
    third_b(path, method, m, n, png)


# 散点图
def fourth_b(path, m=10, n=10):
    dataset = pd.read_excel(path)
    plt.figure(figsize=(m, n))
    scatter_matrix(dataset, diagonal="kde", marker='o', c="red")
    text.insert("1.0", "绘图成功，请在D盘根目录下查看")
    plt.savefig("D:\\绘图结果.jpg")


def a8():
    path = five.get()
    if nine.get() == "":
        m = 10
    else:
        m = int(nine.get())
    if ten.get() == "":
        n = 10
    else:
        n = int(ten.get())
    fourth_b(path, m, n)


# 正态性检验
def first_c(path, x, y=None):
    dataset = pd.read_excel(path)
    if y is None:
        a, b = kstest(dataset[x], 'norm')
    else:
        a, b = kstest(dataset[x] - dataset[y], 'norm')
    text.insert("1.0", "正态性检验的结果为p_value=%.8f\n" % b)
    if b < 0.05:
        text.insert("3.0", "给定数据未通过正态性检验，不能进行后续的t检验\n")
        text.insert("5.0", "请使用对应非参数检验来进行显著性分析\n")
    else:
        text.insert("3.0", "恭喜！给定数据未通过正态性检验\n")



def a9():
    path = eleven.get()
    x = twelve.get()
    if thirteen.get() == "":
        first_c(path, x)
    else:
        y = thirteen.get()
        first_c(path, x, y)


# 方差齐性检验
def second_c(path, x, y):
    dataset = pd.read_excel(path)
    text.insert("1.0", "请在两组数据均通过正态性检验的情况下进行方差齐性检验，否则做了也白做\n")
    e, f = levene(dataset[x], dataset[y])
    if f > 0.05:
        text.insert("3.0", "方差齐性检验通过，可以进行独立样本t检验\n")
    else:
        text.insert("3.0", "方差齐性检验未通过，拒绝原假设，将使用独立样本t检验中针对无方差齐性的方法\n")


def a10():
    path = eleven.get()
    x = twelve.get()
    y = thirteen.get()
    second_c(path, x, y)


# 独立样本t检验
def third_c(path, x, y, method=1):
    text.insert("1.0", "请在两组数据均通过正态性检验的情况下进行独立样本t检验，否则做了也白做\n")
    text.insert("3.0", "若未通过方差齐性检验，请在第四个输入框输入0\n")
    dataset = pd.read_excel(path)
    if method == 1:
        s, p = ttest_ind(dataset[x], dataset[y])
    else:
        s, p = ttest_ind(dataset[x], dataset[y], equal_var=False)

    text.insert("7.0", "独立样本t检验所得p_value为%0.5f\n" % p)
    if p < 0.05:
        text.insert("16.0", "拒绝原假设，两组数据具有显著性\n")
    else:
        text.insert("16.0", "不具有显著性\n")


def a11():
    path = eleven.get()
    x = twelve.get()
    y = thirteen.get()
    if fourteen.get() == "":
        method = 1
    else:
        method = fourteen.get()
    third_c(path, x, y, method)


# 配对样本t检验
def fourth_c(path, x, y):
    text.insert("1.0", "请在两组数据均通过正态性检验的情况下进行配对样本样本t检验，否则做了也白做\n")
    dataset = pd.read_excel(path)
    s, p = ttest_rel(dataset[x], dataset[y])
    text.insert("7.0", "配对样本t检验所得p_value为%0.5f\n" % p)
    if p < 0.05:
        text.insert("8.0", "配对样本Wilcoxon检验通过，两组数据具有显著差异\n")
    else:
        text.insert("8.0", "配对样本Wilcoxon检验未通过，拒绝原假设，数据与所给检验值不具有显著差异\n")


def a12():
    path = eleven.get()
    x = twelve.get()
    y = thirteen.get()
    fourth_c(path, x, y)


# 独立样本非参数检验
def fifth_c(path, x, y):
    dataset = pd.read_excel(path)
    s, p = mannwhitneyu(dataset[x], dataset[y])
    text.insert("7.0", "Mann-Whitney检验所得p_value为%0.5f\n" % p)
    if p < 0.05:
        text.insert("16.0", "拒绝原假设，两组数据具有显著性\n")
    else:
        text.insert("16.0", "不具有显著性\n")


def a13():
    path = eleven.get()
    x = twelve.get()
    y = thirteen.get()
    fifth_c(path, x, y)


# 配对样本非参数检验
def sixth_c(path, x, y):
    dataset = pd.read_excel(path)
    s, p = wilcoxon(dataset[x], dataset[y])
    text.insert("4.0", "配对样本Wilcoxon检验所得p_value为%0.5f\n" % p)
    if p < 0.05:
        text.insert("5.0", "配对样本Wilcoxon检验通过，两组数据具有显著差异\n")
    else:
        text.insert("5.0", "配对样本Wilcoxon检验未通过，拒绝原假设，数据与所给检验值不具有显著差异\n")


def a14():
    path = eleven.get()
    x = twelve.get()
    y = thirteen.get()
    sixth_c(path, x, y)


# 描述性统计分析
def seventh(path):
    dataset = pd.read_excel(path)
    x = dataset.describe()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    text.insert("1.0", x)


def a15():
    path = five.get()
    seventh(path)


# 删除函数
def text_delete():
    text.delete('1.0', 'end')


# ---------------------------------------------
#
# ---------------------------------------------
#
# ---------------------------------------------
#
# ---------------------------------------------

def create1():

    top1 = Toplevel()
    top1.geometry("600x450+700+50")
    top1.title('数据预处理')

    settings_1(top1)


# “数据预处理”界面的标签、输入框以及按钮
def settings_1(top):
    global one
    global two
    global three
    global four
    global five

    f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')
    Label(top, text="数据预处理工具箱", font=f1).place(x=160, y=20)

    Label(top, text="请输入数据集所在的路径~").place(x=50, y=100)
    one = Entry(top)
    one.place(x=50, y=120)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=160)
    two = Entry(top)
    two.place(x=50, y=180)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=220)
    three = Entry(top)
    three.place(x=50, y=240)

    Label(top, text="请输入数据集所在的路径~").place(x=50, y=280)
    four = Entry(top)
    four.place(x=50, y=300)

    Label(top, text="请输入数据集所在的路径~").place(x=50, y=340)
    five = Entry(top)
    five.place(x=50, y=360)

    btn11 = Button(top, bg="red", text="测试缺失值", width=14, height=2, command=a1)
    btn11.place(x=300, y=100)

    btn12 = Button(top, bg="red", text="缺失值处理", width=14, height=2, command=a2)
    btn12.place(x=420, y=100)

    btn13 = Button(top, bg="red", text="特征缩放", width=14, height=2, command=a3)
    btn13.place(x=300, y=210)

    btn13 = Button(top, bg="red", text="特征选择", width=14, height=2, command=a4)
    btn13.place(x=420, y=210)


# 选择“变量分析”时的弹窗界面设置
def create2():
    top2 = Toplevel()
    top2.geometry("600x480+700+50")
    top2.title('变量分析')

    settings_2(top2)


# “变量分析”界面的标签、输入框以及按钮
def settings_2(top):
    global five
    global six
    global seven
    global eight
    global nine
    global ten

    f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')
    Label(top, text="变量分析工具箱", font=f1).place(x=160, y=20)

    Label(top, text="请输入数据集所在的路径~").place(x=50, y=100)
    five = Entry(top)
    five.place(x=50, y=120)
    Label(top, text="请按照文档输入规定参数~").place(x=50, y=160)
    six = Entry(top)
    six.place(x=50, y=180)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=220)
    seven = Entry(top)
    seven.place(x=50, y=240)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=280)
    eight = Entry(top)
    eight.place(x=50, y=300)

    Label(top, text="请输入图片的长~").place(x=50, y=340)
    nine = Entry(top)
    nine.place(x=50, y=360)

    Label(top, text="请输入图片的宽~").place(x=50, y=400)
    ten = Entry(top)
    ten.place(x=50, y=420)

    btn11 = Button(top, bg="red", text="单变量分析", width=14, height=2, command=a5)
    btn11.place(x=300, y=100)

    btn12 = Button(top, bg="red", text="多变量分析", width=14, height=2, command=a6)
    btn12.place(x=420, y=100)

    btn13 = Button(top, bg="red", text="相关性分析", width=14, height=2, command=a7)
    btn13.place(x=300, y=200)

    btn13 = Button(top, bg="red", text="散点图", width=14, height=2, command=a8)
    btn13.place(x=420, y=200)

    btn14 = Button(top, bg="red", text="描述性统计分析", width=14, height=2, command=a15)
    btn14.place(x=300, y=300)


# 选择“显著性分析”时的弹窗界面设置
def create3():
    top3 = Toplevel()
    top3.geometry("650x400+700+50")
    top3.title('显著性检验')

    settings_3(top3)


# “显著性分析”界面的标签、输入框以及按钮
def settings_3(top):

    global eleven
    global twelve
    global thirteen
    global fourteen

    f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')
    Label(top, text="显著性检验工具箱", font=f1).place(x=160, y=20)

    Label(top, text="请输入数据集所在的路径~").place(x=50, y=100)
    eleven = Entry(top)
    eleven.place(x=50, y=120)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=160)
    twelve = Entry(top)
    twelve.place(x=50, y=180)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=220)
    thirteen = Entry(top)
    thirteen.place(x=50, y=240)

    Label(top, text="请按照文档输入规定参数~").place(x=50, y=280)
    fourteen = Entry(top)
    fourteen.place(x=50, y=300)


    btn15 = Button(top, bg="yellow", text="正态性检验", width=14, height=1, command=a9)
    btn15.place(x=250, y=117)

    btn16 = Button(top, bg="yellow", text="方差齐性检验", width=14, height=1, command=a10)
    btn16.place(x=250, y=200)

    btn17 = Button(top, bg="red", text="独立样本t检验", width=14, height=2, command=a11)
    btn17.place(x=400, y=100)

    btn18 = Button(top, bg="red", text="配对样本t检验", width=14, height=2, command=a12)
    btn18.place(x=400, y=200)

    btn19 = Button(top, bg="red", text="Mann-Whitney检验", width=16, height=2, command=a13)
    btn19.place(x=520, y=100)

    btn20 = Button(top, bg="red", text="配对样本Wilcoxon检验", width=16, height=2, command=a14)
    btn20.place(x=520, y=200)


# 快速上手通道
def create4():
    top4 = Toplevel()
    top4.geometry("1200x700+150+50")
    top4.title('Monkey Box快速上手指南')

    settings_4(top4)


# 快速上手通道界面的标签、输入框以及按钮
def settings_4(top):
    # 设置字体和大小
    f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')
    f2 = tkFont.Font(family='microsoft yahei', size=15, weight='bold')
    # 标题
    Label(top, text="Monkey Box贴心指南~", font=f1).place(x=380, y=5)
    Label(top, text="鼠标放在各文本框内滚动可以往下看哟~").place(x=600, y=50)
    # 第一部分
    Label(top, text="第一部分：请你清楚你需要做什么", font=f2).place(x=10, y=150)
    # 第二部分
    Label(top, text="第二部分：(第一次)使用需要注意什么", font=f2).place(x=430, y=150)
    # 第三部分
    Label(top, text="第三部分：每个工具箱功能的简述", font=f2).place(x=850, y=150)

    # 第一部分文字框
    text1 = Text(top, width=48, height=30)
    text1.place(x=10, y=250)
    text1.insert("1.0", "亲爱的使用者：\n你好。相信你可以看出我已经很有礼貌了，之所以这么有礼貌完全是因为产品做的太垃圾了，希望您轻点喷\n"
                        "好了，正式进入主题：\n"
                        "首先你现在拿着这个数据集，我猜测你需要解决这样几个问题：\n"
                        "\n"
                        "1、你的数据总不可能是完美的吧，总会有一些小可爱不认真填，漏选漏填吧；你的问卷设计或实验指标设置是可能存在问题的，也许经过实验你会发现——这问题或指标设置得根本没有作用呀！！！\n"
                        "这个时候，请你打开数据处理工具箱(我这话术跟传销的也什么区别呜呜呜~)\n"
                        "\n"
                        "2、你肯定是需要对数据进行初步分析的吧，不是得出你结论的那种，而是为了了解你数据的情况。你可能需要对每个变量做一次单变量分析，以了解它们的分布情况——不管是数值特征还是分类特征，我都在工具箱准备好了，直接供你使用；还有多变量分析（用于探究变量间的关系）、相关性分析（这个闭着眼睛都知道什么意思吧）、散点图（勇于探究两变量分布关系）、描述性统计分析（直接输出均值、中位数、等重要指标）\n"
                        "这个时候，请你打开变量分析工具箱\n"
                        "\n"
                        "3、你的实验设计肯定有前后测吧，啥？没有？我不听，就有！你首先需要对对照组和实验组前测进行独立样本检验来确定两个组的初态是可视为无差别的，然后你需要通过配对样本检验来确定前后测是有区别的或者对照组、实验组后测是有区别的。值得注意的是参数检验和非参数检验区别很大，参数检验要求更高，在参数检验用不了的情况下才会使用非参数检验\n"
                        "这个时候，请你打开显著性分析工具箱\n")

    # 第二部分文字框
    text2 = Text(top, width=48, height=30)
    text2.place(x=430, y=250)
    text2.insert("1.0", "亲爱的使用者：\n你好。相信你可以看出我已经很有礼貌了，之所以这么有礼貌完全是因为产品做的太垃圾了，希望您轻点喷\n"
                        "好了，正式进入主题\n"
                        "当你刚拿到实验数据时，首先你要确定你的数据处理、分析需求，然后打开”Monkey Box快速上手指南“（奇怪，你不是已经打开了吗）——这样你可以知道本工具箱是否可以帮助到你，如果不能，请你果断卸载不要浪费时间，本工具箱高度封装（人话：不像别的软件你可以想干嘛就干嘛），或者你可以联系1792733991@qq.com，本人可以帮你分析（只要你好意思哈哈哈哈~）\n"
                        "\n"
                        "好了不开玩笑了，如果你确定本工具箱能帮到你，请你接着往下看。当你无法明确自己需要使用什么功能时，请你先看右边的第三个框，它会告诉你每个功能是用来干嘛的、需要注意什么\n"
                        "当你明确自己需要使用什么功能时，你有两种选择：\n"
                        "1、打开工具箱主页CSDN链接，上面有一套完整的算法原理和使用说明，适合想了解算法的童鞋\n"
                        "2、如果你对算法根本不感兴趣，马上就要交论文了！！！请你初步查看菜单栏里对应功能的帮助文档，上面已经写明了你要如何实现功能——只是你可能会因为不知道原理而用错算法\n"
                        "\n"
                        "还有另一个点，就是当你出错了得不到结果怎么办？？？\n"
                        "\n"
                        "这个时候你要做的第一件事是怒骂作者，如果不是他水平不够你怎么会得不到结果？？？然后运行不出结果两个情况：\n"
                        "1、你自己没有按照作者的意思输入规定参数。如果这样的话你一方面可以仔细阅读帮助文档和CSDN博客，另一方面可以去查看菜单中的常见错误，它可能会给你答案\n"
                        "2、可能……运行不出结果的原因是这本来就是个bug，这个时候建议你一边辱骂作者（不要拖家带口），一边联系作者的邮箱\n"
                        "1792733991@qq.com\n"
                        "不要直接加QQ，作者不喜欢，你联系邮箱我微信会立刻收到，我会及时回复，同时如果你跟作者关系好你可以顺带着让本人直接帮你分析数据，如果不认识也没关系，你可以适当贿赂，比如一瓶营养快线\n"
                        "\n"
                        "因为本产品还在测试，所以就没有建群，建群以后会方便很多，我设计这个产品的原因也是为了方便大家，欢迎大家为本产品做出贡献，剔除bug，作者不甚感激\n")

    # 第三部分文字框
    text3 = Text(top, width=48, height=30)
    text3.place(x=850, y=250)
    text3.insert("1.0", "亲爱的使用者：\n你好。相信你可以看出我已经很有礼貌了，之所以这么有礼貌完全是因为产品做的太垃圾了，希望您轻点喷\n"
                        "好了，正式进入主题\n"
                        "等等，别急，我补充一下：下面我可能会使用特征、变量、指标等名词，其实是一码事哈，机器学习里一般都叫特征\n"
                        "写完上面两个部分我真的要累趴了，但这个部分应该是最难写的，我尽力用最通俗易懂的语言描述各个功能的作用，我们就按照说明文档的顺序来吧：\n"
                        "\n"
                        "1、测试缺失值：简单来讲你的数据可能会有一些缺失值吧，在机器学习领域会说你的数据很”脏“，意思就是别特么直接用，给它处理一下，不然直接带入模型训练模型的精度会很差，这个功能只需要你把数据集的路径给出了，工具箱会自动读取并测试其中有没有缺失值，将结果反映到终端里\n"
                        "\n"
                        "2、缺失值处理：这个就更好理解了，你现在知道数据里有缺失值了，那不能让它放在那里好看呀。实现这个功能需要数据路径、含有缺失值的那一列的列名以及处理缺失值的方法，你可以用这一列的均值、中位数（一般针对数值特征）、众数（一般针对分类特征）来填补缺失值，也可以直接删除这个数据集中含有缺失值的行（这你得考虑清楚你的数据集够不够大以及缺失值多不多，别到时候给你数据集删完了），如果你用后者处理那就不需要对应列名了，工具箱会非常残忍地把所有含缺失值的行删掉\n"
                        "\n"
                        "3、特征缩放：这个你需要知道量纲的概念，我打个简单的比方吧。你要做一个调查搜集班上学生身高和体重做一个综合的评价，结果身高全都是不到2的小数，体重全都是几百，那你这个分析就很不好做。特征缩放的目的就是让你的数据全缩放到一个很小的区间、量纲相同而数据原有的特性其实没有改变，0-1和标准化是两种缩放的方式这里就不细说了，实际实验数据里如果没有负数的话我觉得二者没什么区别\n"
                        "\n"
                        "4、特征选择：这个部分我准备了两个方法供选择，方差选择法和互信息。两种方式最终目的就是找到占着茅坑不拉屎的变量，前者针对数值型特征（你这样想：如果一组变量方差为0，那就相当于是全都相同，你觉得有意义吗），后者针对分类型特征（互信息是衡量特征相关性的，越大相关性越强，而我们是希望变量之间相互独立，这种强的留一个就足够了）\n"
                        "\n"
                        "5、单变量分析：这个主要是针对数值特征和分类特征作探究分布的数据可视化，前者用的是直方图+箱线图，后者用的是条形统计图，绘图结果存放在D盘，这个没什么好讲的\n"
                        "\n"
                        "6、多变量分析：严格来讲应该叫双变量分析，其实和单变量分析都是机器学习中EDA的常见手段，说到底就是为了了解数据，我觉得至少这两个功能的作用真的是只可意会不可言传，详见我的CSDN博客吧，我只能说你做了机器学习才能领会到其对机器学习关键步骤——特征工程的重要作用\n"
                        "\n"
                        "7、相关性分析：这个我真的懒得说了，这个都不懂就好好学学语文吧"
                        "\n"
                        "8、散点图：这个散点图不是只出现两个变量间的，我直接调用pandas的函数做了一个超大的散点图，散点图的作用主要也是探究变量直接的线性性的，具有线性的变量最好还是不要\n"
                        "\n"
                        "9、描述性统计分析：这个只需要你给出数据集的路径，就会在终端把数据集的每个变量（数值特征）的平均值、中位数等好多东西都告诉你，很好用哒~\n"
                        "\n"
                        "10、剩下的就是显著性分析部分了，我放在一起说：首先想做显著性分析得有一定的数据量（>20），然后两组数据毫无关系就独立样本检验，前后测或者对照关系就用配对样本检验，两种检验我都给出了参数检验（t检验）和非参数检验，参数检验对数据集要求很高，要求两组数据分别（独立）或其差（配对）必须通过正态性检验，如果使用独立样本检验，是否通过方差齐性检验也同样关键，具体参考帮助文档；如果使用配对样本那就不管方差齐性\n"
                        "\n"
                        "介绍结束，累死我了，有什么问题发我邮箱：\n1792733991@qq.com\n"
                        "在下不甚感激！！！")


# 常见错误汇总
def create5():
    top = Toplevel()
    top.geometry("1200x700+150+50")
    top.title('懒得更了，直接发布，大家听天由命把~')


# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------

def mx1():
    messagebox.showinfo('关于',
                        '关于这个超级简陋的工具箱，我是很看不起的——看不起自己的技术只能造出这么简陋的程序\n'
                        '然而虽然它很丑陋，功能也不多，我本人并不认为它是个废物——我更认为它是很多人在实验时做数据分析的利器。\n'
                        '虽然我有在认真地完成这个项目，但我平时也很忙，而且还要考研，所以这个产品难免会有bug\n'
                        '如果使用者发现了bug，欢迎联系1792733991@qq.com\n'
                        '在下不甚感激')


def mx2():
    messagebox.showinfo('测试缺失值简要使用说明，详细介绍请参考CSDN博客',
                        '用法如下:\n'
                        '请在第一个输入框输入：数据文件路径\n'
                        '结果将在终端显示，告诉您您的数据各个特征的缺失值数量\n')


def mx3():
    messagebox.showinfo('缺失值处理简要使用说明，详细介绍请参考CSDN博客',
                        '用法如下:\n'
                        '请在第一个输入框输入：数据文件路径\n'
                        '请在第二个输入框输入：特征的名称\n'
                        '请在第三个输入框输入：均值、中位数、指定数、众数或剔除\n'
                        '请在第四个输入框输入：第三个输入框选择指定数时的指定数，若无可忽略\n'
                        '结果将写入表格放在您D盘的根目录中，名为new.csv\n')


def mx4():
    messagebox.showinfo('特征缩放简要使用说明，详细介绍请参考CSDN博客',
                        '用法如下:\n'
                        '请在第一个输入框输入：数据文件路径\n'
                        '请在第二个输入框输入：0-1或标准化\n'
                        '结果将写入表格放在您D盘的根目录中，名为new.csv\n'
                        '温馨提示：您在进行特征缩放前请保证数据没有变量含有字符串\n')


def mx5():
    messagebox.showinfo('特征选择简要使用说明，详细介绍请参考CSDN博客',
                        '用法如下:\n'
                        '请在第一个输入框输入：数据文件路径\n'
                        '请在第二个输入框输入：方差选择法或互信息\n'
                        '如果选择方差选择法，请在第三个输入框输入方差阈值\n'
                        '如果选择互信息，请在第四、五个输入框输入两个变量名称\n'
                        '结果将在终端显示\n')


def mx6():
    messagebox.showinfo('单变量分析简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：要被分析的单变量特征的名称\n"
                        "请在第三个输入框输入：数值或分类\n"
                        "请在第五、六个输入框分别输入：图片的长和宽\n"
                        "最终绘图结果讲写在D盘根目录，文件名称为绘图结果.jpg\n")


def mx7():
    messagebox.showinfo('多变量分析简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：要被分析的第一个特征的名称\n"
                        "请在第三个输入框输入：要被分析的第二个特征的名称(目前这个只能是分类特征)\n"
                        "请在第四个输入框输入：“分类-分类1”、“分类-分类2”、“数值-分类1”或“数值-分类2”\n"
                        "请在第五、六个输入框分别输入：图片的长和宽\n"
                        "最终绘图结果讲写在D盘根目录，文件名称为绘图结果.jpg\n")


def mx8():
    messagebox.showinfo('相关性分析简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：pearson或spearman\n"
                        "若您需要相关系数热力图，请在第三个输入框扣1\n"
                        "请在第五、六个输入框分别输入：图片的长和宽\n"
                        "最终绘图结果讲写在D盘根目录，文件名称为绘图结果.jpg\n")


def mx9():
    messagebox.showinfo('散点图简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第五、六个输入框分别输入：图片的长和宽\n"
                        "最终绘图结果讲写在D盘根目录，文件名称为绘图结果.jpg\n")


def mx10():
    messagebox.showinfo('描述性统计分析简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "结果将在终端显示\n")


def mx11():
    messagebox.showinfo('独立样本t检验简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：第一个特征名称\n"
                        "请在第三个输入框输入：第二个特征名称\n"
                        "如果未通过方差齐性检验，请在第四个输入框扣0\n"
                        "结果将在终端显示\n"
                        "温馨提示：请在两组数据均通过正态性检验后进行独立样本t检验\n"
                        "否则请移步：Mann-Whitney检验")


def mx12():
    messagebox.showinfo('配对样本t检验简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：第一个特征名称\n"
                        "请在第三个输入框输入：第二个特征名称\n"
                        "结果将在终端显示\n"
                        "温馨提示：请在两组数据均通过正态性检验后进行配对样本t检验\n"
                        "否则请移步：配对样本Wilcoxon检验")


def mx13():
    messagebox.showinfo('Mann-Whitney检验简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：第一个特征名称\n"
                        "请在第三个输入框输入：第二个特征名称\n"
                        "结果将在终端显示\n")


def mx14():
    messagebox.showinfo('配对样本Wilcoxon检验简要使用说明，详细介绍请参考CSDN博客',
                        "用法如下:\n"
                        "请在第一个输入框输入：数据文件路径\n"
                        "请在第二个输入框输入：第一个特征名称\n"
                        "请在第三个输入框输入：第二个特征名称\n"
                        "结果将在终端显示\n")


def mx15():
    messagebox.showinfo('敬请期待',
                        "1、数学实验工具箱：求极限、积分、逆矩阵、行列式等\n"
                        "2、多属性评价工具箱：层次分析法、熵权法、数据包络法、模糊综合评价法\n"
                        "3、机器学习工具箱：支持向量机、随机森林、K-means聚类\n")
# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------

# 菜单
def menu():
    # 在窗口上创建一个菜单栏（最上方的菜单栏横条）
    menubar = Menu(window)
    # 定义一个竖条
    filemenu = Menu(menubar, tearoff=0)
    # 在顶部再添加两个菜单项
    Menu(menubar, tearoff=0)
    menubar.add_cascade(label='关于产品（测试版）', command=mx1)
    # 在菜单单元中添加一个菜单项File
    menubar.add_cascade(label='帮助文档', menu=filemenu)
    menubar.add_cascade(label='常见使用错误汇总', command=create5)
    menubar.add_cascade(label='敬请期待', command=mx15)
    # 添加一条分割线
    filemenu.add_separator()

    submenu2 = Menu(filemenu)  # 和上面定义菜单一样，不过此处是在File上创建一个空的菜单
    submenu2.add_command(label="测试缺失值", command=mx2)
    submenu2.add_command(label="缺失值处理", command=mx3)
    submenu2.add_command(label="特征缩放", command=mx4)
    submenu2.add_command(label="特征选择", command=mx5)
    # 添加一个展开下拉菜单，并把上面的子菜单嵌入给它
    filemenu.add_cascade(label='数据处理', menu=submenu2, underline=0)

    # 和上面定义菜单一样，不过此处是在File上创建一个空的菜单
    submenu3 = Menu(filemenu)
    submenu3.add_command(label="单变量分布分析", command=mx6)  # 给submenu添加功能选项
    submenu3.add_command(label="多变量分析", command=mx7)
    submenu3.add_command(label="相关性分析", command=mx8)
    submenu3.add_command(label="散点图", command=mx9)
    submenu3.add_command(label="描述性统计分析", command=mx10)
    # 添加一个展开下拉菜单，并把上面的子菜单嵌入给它
    filemenu.add_cascade(label='变量分析', menu=submenu3, underline=0)

    # 定义一个子菜单条
    submenu1 = Menu(filemenu)  # 和上面定义菜单一样，不过此处是在File上创建一个空的菜单
    submenu1.add_command(label="独立样本t检验", command=mx11)
    submenu1.add_command(label="配对样本t检验", command=mx12)
    submenu1.add_command(label="Mann-Whitney检验", command=mx13)
    submenu1.add_command(label="配对样本Wilcoxon检验", command=mx14)
    # 添加一个展开下拉菜单，并把上面的子菜单嵌入给它
    filemenu.add_cascade(label='显著性检验', menu=submenu1, underline=0)

    # 将菜单配置给窗口
    window.config(menu=menubar)


# 总界面部件
def tool():
    btn1 = Button(window, text="数据处理工具箱", width=14, height=2, command=create1)
    btn1.pack()
    btn1.place(x=450, y=130)

    btn2 = Button(window, text="变量分析工具箱", width=14, height=2, command=create2)
    btn2.pack()
    btn2.place(x=450, y=190)

    btn3 = Button(window, text="显著性检验工具箱", width=14, height=2, command=create3)
    btn3.pack()
    btn3.place(x=450, y=250)

    btn4 = Button(window, text="Monkey Box快速上手指南", bg="green", width=25, height=1, command=create4)
    btn4.pack()
    btn4.place(x=90, y=360)

    btn5 = Button(window, text="重启终端", bg="green", width=25, height=1, command=text_delete)
    btn5.pack()
    btn5.place(x=315, y=360)

    f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')

    Label(text="Monkey Box", font=f1).place(x=200, y=50)
    Label(text="欢迎您使用Monkey Box，请选择自己需要的功能~").place(x=20, y=130)
    Label(text="请优先查看本软件的快速上手通道，非常简单保证您一分钟上手~").place(x=20, y=160)
    Label(text="如果遇到什么问题不能解决那大概率遇到bug了~").place(x=20, y=190)
    Label(text="欢迎联系:1792733991@qq.com~").place(x=20, y=220)
    Label(text="本产品已在Github开源，CSDN博客配有使用说明~").place(x=20, y=250)
    Label(text="Github:").place(x=20, y=280)
    Label(text="CSDN:").place(x=20, y=310)
    Label(text="Monkey Terminal", font=f1).place(x=160, y=420)

# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------
#
# ------------------------------------------------------


window = Tk()
window.title("Monkey Box--测试版")
window.geometry("600x800+50+50")

# 文字框
text = Text(window, width=70, height=25)
text.pack(side="bottom", fill=Y)

tool()
menu()
window.mainloop()
