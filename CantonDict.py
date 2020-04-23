from tkinter import *
#from icon import img
import base64
import os
import tkinter.messagebox
import sys
import urllib.request
import re
import tkinter.font as tkFont

#创建新窗口
root = Tk()
print(sys.getdefaultencoding())

class Inputbox():

    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c
        self.entry = Entry(borderwidth = 5)
        self.entry.grid(row=self.r, column=self.c, columnspan=10, sticky=N+S+E+W)

    def personalized(self, key):

        self.entry.focus()
        #self.entry.bind(r'<%>'% key, lambda x: self.getinput(self.entry.get()))
        self.entry.bind('<'+key+'>', self.get_value)
        print(locals())

    def get_value(self, value):
        # 删除之前创建的临时全局变量
        createVar = globals()
        dict_list = []
        for key in globals().keys():
            dict_list.append(key)
        for k in dict_list:
            if k[0:4] == 'show':
                print(k)
                createVar[k].destroy()


        if not len(self.entry.get())<6:
            self.refresh()
        """global loading1
        loading1 = Label(root, text='查询中...', font='微软雅黑', relief='ridge', padx=1, pady=1, borderwidth=5,
                         justify='center')
        loading1.grid(row=2, column=1, sticky=N+S+E+W, columnspan=10)"""
        self.value = self.entry.get()
        print(self.value)
        #aprint(type(self.value))

        self.encode() #调用下方的encode方法
        self.refresh()

    def refresh(self):
        self.entry.delete(0, END)

    def encode(self):
        self.code = self.value.encode('gb2312')
        #print(self.code)
        #print(str(self.code))
        #print(type(str(self.code)))
        #print(type(self.code))
        #print(str(self.code)[:-1].split('\\x'))
        list = str(self.code)[:-1].split('\\x')[1:]
        #print(list)
        global utfcode
        utfcode =''
        for i in list:
            utfcode += '%' + str(i.upper())
        #print(utfcode)
        if not utfcode:
            result = tkinter.messagebox.showerror(title='出错了!', message='请确保输入5位以内正确的汉字符号！（不含标点符号或英文字母）')
            print(result)
            return
        InternetBrowser.determine(utfcode)


class InternetBrowser():

    def determine(utfcode):

        if len(utfcode) == 6:
            pattern = re.compile(r'<span class="phonetic"><font color="#FF0000">.*?</font>', re.S)
            url = 'http://www.yueyv.com/?keyword=' + utfcode + '&submit=%B2%E9+%D4%83'
            group = 0
            InternetBrowser.gomatch(pattern, url, group)
        else:
            groups = len(utfcode) // 6
            print('grousp is ' + str(groups))
            for group in range(groups):
                utf_copy = utfcode[group*6:group*6+6]
                print('utf_copy is' + utf_copy)
                pattern = re.compile(r'<span class="phonetic"><font color="#FF0000">.*?</font>', re.S)
                url = 'http://www.yueyv.com/?keyword=' + utf_copy + '&submit=%B2%E9+%D4%83'
                InternetBrowser.gomatch(pattern, url, group)

    def gomatch(pattern, url, group):
        f = urllib.request.urlopen(url)
        content = f.read().decode('gbk')
        #print(content)
        basic_content = re.findall(pattern, content)
        print(basic_content)
        #出错提示
        if not basic_content:
            result = tkinter.messagebox.showerror(title='出错了!', message='请确保输入正确的汉字符号！（不含标点符号或英文字母）')
            print(result)
            return
        lists = []
        for i in basic_content:
            i = i[45:-7]
            print(i)
            lists.append(i)
        print(lists)
        print(len(lists))

        InternetBrowser.reflect(lists, group)


    def reflect(lists, group):
        string = ''
        for list in lists:
            string = string + list + '\n'
        print(string)

        #利用locals函数创建group+1个标签变量
        createVar = globals()
        LabelTemp = group
        createVar['show'+str(group)] = Label(root, text=string, font='Calibri')
        #loading1.grid_forget()
        createVar['show'+str(group)].grid(row=1, column=group+1, sticky=N+S+E+W)
        print(createVar)



        #print(createVar)
        #label2 = Label(root, text=string, font='Calibri')
        #label2.grid(row=1, column=1, sticky=N+S+E, padx=5, pady=5, columnspan= 3)


def main():
    #修改icon
    #root.iconbitmap('.\\Canton.ico')
    """tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap("tmp.ico")
    os.remove("tmp.ico")"""

    #设置窗口大小
    #root.geometry('360x200')

    #设置标题
    root.title('广东话音拼字典')

    #创建frame
    frame = Frame(root)
    #frame.grid()

    Grid.rowconfigure(root, 0, weight=2)
    Grid.columnconfigure(root, 0, weight=2)

    #创建标题字体统一格式
    ft_title = tkFont.Font(family='微软雅黑', size=12, weight=tkFont.BOLD)

    #创建正文字体统一格式
    ft_content = tkFont.Font(family='Times', size=8, weight=tkFont.NORMAL)


    #创建引导标签对象并添加到顶层窗口
    label1 = Label(root, text = '请输入您要查询的字或词(5字以内)', fg='red', font=ft_title, padx=1, pady=1, borderwidth = 5, justify='center')
    label1.grid(row=0, column=0, columnspan=1, sticky=N+S+E+W)
    #label1.pack(fill=X) #expand表示元素是否跟随窗口大小拓展


        #创建输入窗口并个性化互动按键/导出输入值
    input1 = Inputbox(0, 1)
    #input.grid(row=1, column=1)
    input1.personalized('Return')

    #创建一个图片管理类
    photo = PhotoImage(file='E:\PyCharm\Project\CantoneseDict\pic\image.png')
    new_photo = photo.zoom(1, 1)
    new_photo = new_photo.subsample(3,3) #缩小图片
    imgLabel = Label(root, image=new_photo, padx=0, pady=0, borderwidth = 5)
    imgLabel.grid(columnspan=1, sticky=N+S+E+W)

    #创建联系方式标签
    label2 = Label(root, text = '联系作者:\nVX:huyuepeng0328\n欢迎提出宝贵意见！', font=ft_content, padx=1, pady=1, borderwidth=5, justify='center')
    label2.grid(row=2, column=0, columnspan=1, sticky=N+S+E+W)

    #开启事件主循环
    mainloop()

if __name__ == '__main__':
    main()