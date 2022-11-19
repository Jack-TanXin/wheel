from tkinter import *
from tkinter import messagebox

from pydocx import PyDocX

from pdf2docx import Converter
from win32com import client
import tkinter.font as tkFont


# python 实现 pdf 转 word
def pdf_docx(file_path):

    if "pdf" in file_path:
        text.insert("1.0", "请删去文件拓展名pdf!!!\n")

    text.insert("1.0", "开始读取文件\n")
    pdf_file = file_path + ".pdf"
    docx_file = file_path + ".docx"
    text.insert("2.0", "开始转换文件\n")
    # convert pdf to docx
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()
    text.insert("3.0", "转换完成\n")


# python 实现 word 转html
def docx2html(path):

    if "docx" in path:
        text.insert("1.0", "请删去文件拓展名docx!!!\n")

    text.insert("1.0", "开始读取文件\n")
    html = PyDocX.to_html(path + ".docx")
    text.insert("2.0", "开始转换文件\n")
    f = open(path + ".html", 'w', encoding="utf-8")
    f.write(html)
    f.close()
    text.insert("3.0", "转换完成\n")


# python 实现 word 转pdf
def docx2pdf(fn):

    if "pdf" in fn:
        text.insert("1.0", "请删去文件拓展名docx!!!\n")

    text.insert("1.0", "开始读取文件\n")
    word = client.Dispatch("Word.Application")  # 打开word应用程序
    # for file in files:
    doc = word.Documents.Open(fn + ".docx")  # 打开word文件
    text.insert("2.0", "开始转换文件\n")
    doc.SaveAs("{}.pdf".format(fn), 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf
    doc.Close()  # 关闭原来word文件
    word.Quit()
    text.insert("3.0", "转换完成\n")


# 删除函数
def text_delete():
    text.delete('1.0', 'end')


def one():
    path = enter.get()
    pdf_docx(path)


def two():
    path = enter.get()
    docx2html(path)


def three():
    path = enter.get()
    docx2pdf(path)

def mx1():
    messagebox.showinfo('关于产品',
                        "由于一次偶然的机会幸运地在本科期间接触到了科研工作，当前需要阅读大量外文文献，然而想要找到免费、方便的翻译软件谈何容易，因此本人制作了这款产品。\n"
                        "我们从各大检索网站下载的pdf文献，首先经过本产品转换为word，这里的转换效果不会完美，因为word和pdf终究是不一样的，\n"
                        "然后将word转换为html，成功以后，通过谷歌浏览器自带的翻译引擎即可完美的解决翻译问题，作者亲测有效。\n"
                        "\n"
                        "\n"
                        "详细的使用说明与案例示范请参考猩猩的CSDN博客：\n"
                        "https://blog.csdn.net/weixin_59740529/article/details/127618667")


def mx2():
    messagebox.showinfo('使用方法',
                        "将需要转换的文件放在指定文件中，最好在D盘的无其他文件的文件夹\n"
                        "\n"
                        "并在输入框中输入其路径(不含文件自身的拓展名)，转换后的文件会在同一个文件夹下出现\n"
                        "\n"
                        "以我放在D盘Tan_pro文件夹下的  文件转换器.pdf  为例:\n"
                        "\n"
                        "将其转换为.docx的word：在输入框输入：D:\\Tan_Pro\\文件转换器 即可\n"
                        "\n"
                        "千万不要文件拓展名！！！")



def mx3():
    messagebox.showinfo('联系方式',
                        "如果您在使用的时候发现了无法解决的问题，欢迎联系：\n"
                        "1792733991@qq.com\n"
                        "\n"
                        "如果您不是长辈，请不要直接加QQ，作者不喜欢，您发邮件作者一定会及时收到回复的！")


def mx4():
    messagebox.showinfo('值得注意',
                        "几点使用经验(奇怪，明明这就是我开发的)分享给大家：\n"
                        "1、文件路径千万不要含拓展名！！！\n"
                        "2、如果你输入的文件位置没有问题，在你按下按钮时按钮应该会变灰至少一秒\n"
                        "3、文件路径千万不要含拓展名！！！\n"
                        "4、pdf转word是比较耗时的，而且我测试发现产品会无响应，请耐心等待，不要真的以为产品卡死了\n"
                        "5、文件路径千万不要含拓展名！！！\n"
                        "6、路径中的一条”\“最好改为两条”\“，因为本产品是用python写的\n"
                        "7、文件路径千万不要含拓展名！！！\n"
                        "8、如果您按下按钮后终端仅显示 “开始读取数据” ，且半分钟都没出现 “开始转换数据”"
                        "请立刻检查您的路径是否符合要求，如果符合，麻烦您在D盘再新建一个文件夹并修改输入框的路径重新尝试，这种失败主要会出现在 word -> pdf")


# 定义一个gui界面
window = Tk()
window.title("猩猩的文件转换器")
window.geometry("560x450+50+50")


f1 = tkFont.Font(family='microsoft yahei', size=25, weight='bold')
Label(text="使用方法见菜单栏“使用方法”", font=f1).place(x=50, y=200)



# 按钮
btn1 = Button(window, text="pdf -> word", width=14, height=2, command=one)
btn1.pack()
btn1.place(x=50, y=120)

btn2 = Button(window, text="word -> html", width=14, height=2, command=two)
btn2.pack()
btn2.place(x=230, y=120)

btn3 = Button(window, text="word -> pdf", width=14, height=2, command=three)
btn3.pack()
btn3.place(x=410, y=120)

btn4 = Button(window, text="清空终端", width=8, height=1, command=text_delete)
btn4.pack()
btn4.place(x=50, y=330)


Label(text="请在此文本框输入路径").place(x=160, y=60)
enter = Entry(window)
enter.place(x=300, y=60)


# 文字框
text = Text(window, width=40, height=12)
text.pack(side="bottom", fill=Y)


menubar = Menu(window)
# 定义一个竖条
filemenu = Menu(menubar, tearoff=0)
# 在顶部再添加两个菜单项
Menu(menubar, tearoff=0)
menubar.add_cascade(label='关于产品', command=mx1)
menubar.add_cascade(label='使用方法', command=mx2)
menubar.add_cascade(label='值得注意', command=mx4)
menubar.add_cascade(label='联系作者', command=mx3)

# 将菜单配置给窗口
window.config(menu=menubar)

window.mainloop()

