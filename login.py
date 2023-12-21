import streamlit as st
import pymysql
import LinkApi
import datetime

#以下密钥信息从控制台获取
api_key ="Link_JKarAw3EXbwVg2hX0AAfwuu1Xu8CsHbpDhizzQIHdk"
Link_url = "https://api.link-ai.chat/v1/chat/completions"
st.set_page_config(page_title="AD家园AI小助手", layout="centered", page_icon="🔥",initial_sidebar_state="auto",menu_items=None)

text =[]
def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
    
@st.cache_resource
def init_connection():
    host = "localhost"
    database = "python"
    user = "root"
    password = "bxcvbuynt1!!"
    return pymysql.connect(host=host, database=database, user=user, password=password)

con = init_connection()
#con = pymysql.connect(host="localhost", user="root", password="bxcvbuynt1!!", database="python", charset="utf8")
c = con.cursor()

# 密码长度判断
def pw_len(passwd):
    """
    :param passwd:
    :return:  是否合法， 计分
    """
    passwd_len = len(passwd)
    if passwd_len > 8:
        return 1
    else:
        return 0


# 判断密码复杂度
# flake
# 函数命名、变量命名。英文。风格。
def pw_fzd(passwd1):
    passwd_len = len(passwd1)
    fh = 0
    letters = 0
    sz = 0
    for i in passwd1:
        i_ascii = ord(i)
        if 33 <= i_ascii <= 47 or 58 <= i_ascii <= 64 or 91 <= i_ascii <= 96 or 123 <= i_ascii <= 126:
            fh = 1
        elif 65 <= i_ascii <= 90 or 97 <= i_ascii <= 122:
            letters = 1
        elif 48 <= i_ascii <= 57:
            sz = 1
    if fh == 1 & letters == 1 & sz == 1:
        return 1
    else:
        return 0


# 判断密码是否有超过三位的重复
# abcdefabc
def pwd_cfd(passwd1):
    passwd_len = len(passwd1)
    for i in range(passwd_len - 4):
        # 当前字符+3
        str_1 = passwd1[i:i + 3]
        str_2 = passwd1[i + 3:]
        if str_1 in str_2:
            return 0
    return 1


def compare(passwd1, passwd2):
    if passwd1 == passwd2:
        return 1
    else:
        return 0


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username VARCHAR(20) PRIMARY KEY NOT NULL , password VARCHAR(20))')

def create_user_daytimes_table():
    c.execute('CREATE TABLE IF NOT EXISTS userdaytimestable(userdate VARCHAR(20) PRIMARY KEY NOT NULL ,times INT)')


def add_userdata(username, password):
    today=datetime.datetime.now().strftime('%Y-%m-%d')
    usertoday=username+'_'+today
    if c.execute('SELECT username FROM userstable WHERE username = %s',(username)):
        st.warning("用户名已存在，请更换一个新的用户名。")
    else:
        c.execute('INSERT INTO userstable(username,password) VALUES(%s,%s)',(username,password))
        c.execute('INSERT INTO userdaytimestable(userdate,times) VALUES(%s,%s)',(usertoday,0))
        #c.execute('insert into userdaytimestable(userdate,times) select %s,%s from userdaytimestable where not exists (select userdate from userdaytimestable where userdate=%s',(usertoday,0,usertoday)
        con.commit()
        st.success("恭喜，您已成功注册。")
        st.info("请在左侧选择登录选项进行登录。")

def add_usertimesdata(username):
    today=datetime.datetime.now().strftime('%Y-%m-%d')
    usertoday=username+'_'+today
    if not c.execute('SELECT times FROM userdaytimestable WHERE userdate = %s' ,(usertoday)):
        c.execute('INSERT INTO userdaytimestable(userdate,times) VALUES(%s,%s)',(usertoday,0))
        #c.execute('insert into userdaytimestable(userdate,times) select (%s,%s) from userdaytimestable where not exists (select userdate from userdaytimestable where userdate=%s',(usertoday,0,usertoday)
    c.execute('SELECT times FROM userdaytimestable WHERE userdate = %s' ,(usertoday))
    date_times=c.fetchall()[0][0]
    con.commit()
    if date_times==0:
        st.info("第1次会话")
        c.execute('UPDATE  userdaytimestable SET times=%s ',(1))
        #c.execute('insert into userdaytimestable(userdate,times) select (%s,%s) from userdaytimestable where not exists (select userdate from userdaytimestable where userdate=%s',(usertoday,1,usertoday)
        con.commit()
        return True
    else:
        #times=c.execute('SELECT times FROM userdaytimestable WHERE userdate = %s' ,(usertoday))
        if date_times<=10:
            date_times+=1
            info="第"+str(date_times)+"次会话"
            st.info(info)
            c.execute('UPDATE  userdaytimestable SET times=%s WHERE userdate = %s',(date_times,usertoday))
            con.commit()
            return True
        else:
            st.info("今日已经超过免费次数，请明日再来")
            return False

def login_user(username,password):
    if c.execute('SELECT *  FROM userstable WHERE username = %s',(username)):
        c.execute('SELECT * FROM userstable WHERE username = %s AND password = %s' ,(username,password))
        data=c.fetchall()
        return data
    else:
        st.warning("用户名不存在，请先选择注册按钮完成注册。")

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():
    menu = ["首页","登录","注册", "注销"]

    if 'count' not in st.session_state:
        st.session_state.count = 0

    choice = st.sidebar.selectbox("选项",menu)
    st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,)

    if choice =="首页":
        #st.title("说明")
        st.caption ("本网站是兜兜有糖编写的针对特应性皮炎(AD)的AI问答机器人，参考了多篇特皮文献资料，可以专业的回答绝大部分病友的问题！")
        st.caption ("由于资源有限，每人每天只有:red[10]次免费问答机会，请大家珍惜！:sunglasses:")
        st.latex(r'''a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
            \sum_{k=0}^{n-1} ar^k =
            a \left(\frac{1-r^{n}}{1-r}\right)
        ''')
        st.subheader ("首次登录需要注册账号，点击左侧注册按钮注册！",divider='rainbow')
        #st.divider()
        #st.subheader ("有其他问题或者想加病友群交流的可以加管理员咨询！")
        col1, col2 = st.columns(2)
        with col1:
            st.image("pic/QR_code.jpg",caption='有其他问题或者想加病友群交流的可以加管理员咨询！')
        with col2:
            st.image("pic/money_code.jpg",caption='觉得做的还行的可以请兜兜喝杯咖啡！')
        
    elif choice =="登录":
        st.sidebar.subheader("登录区域")
        username = st.sidebar.text_input("用户名")
        password = st.sidebar.text_input("密码",type = "password")
        if st.sidebar.checkbox("开始登录"):
            logged_user = login_user(username,password)
            if logged_user:
                st.session_state.count += 1
                if st.session_state.count >= 1:
                    #st.balloons()
                    if "chat_history" not in st.session_state:
                        st.session_state["chat_history"] = []
                    st.sidebar.success("您已登录成功，您的用户名是 {}".format(username))
                    st.success("欢迎与AD家园AI小助手进行交流,咨询结果不能作为治疗依据,详情请咨询专业医生！")
                    user_input = st.chat_input("请输入你想咨询的问题！")
                    with st.container():
                        if user_input is not None:
                            if add_usertimesdata(username):
                                progress_bar = st.empty()
                                with st.spinner("内容已提交，AI小助手正在作答中！"):
                                    question = checklen(getText("user", user_input))
                                    LinkApi.answer = ""
                                    LinkApi.main(user_input)
                                    feedback = getText("assistant", LinkApi.answer)[1]["content"]
                                    if feedback:
                                        progress_bar.progress(100)
                                        st.session_state['chat_history'].append((user_input, feedback))
                                        for i in range(len(st.session_state["chat_history"])):
                                            user_info = st.chat_message("user")
                                            user_content = st.session_state["chat_history"][i][0]
                                            user_info.write(user_content)
                                            assistant_info = st.chat_message("assistant")
                                            assistant_content = st.session_state["chat_history"][i][1]
                                            assistant_info.write(assistant_content)
                                
                                        with st.sidebar:
                                            if st.sidebar.button("清除对话历史"):
                                                st.session_state["chat_history"] = []
                                    else:
                                        st.info("对不起，我回答不了这个问题，请你更换一个问题，谢谢！")
                                
            else:               
                st.sidebar.warning("用户名或者密码不正确，请检查后重试。")   

    elif choice =="注册":
        st.subheader("密码检查:")
        new_user = st.sidebar.text_input("用户名")
        passwd1 = st.sidebar.text_input("密码",type = "password")
        passwd2 = st.sidebar.text_input("确认密码",type = "password")
        com = compare(passwd1, passwd2)
        if com == 0:
            st.warning("两次密码不一致 ")
            st.warning(f"注册失败密码安全等级为0分")
        else:
            # 判断密码长度
            cd = pw_len(passwd1)
            if cd == 0:
                st.warning("密码小于8位 ")
            # 判断密码复杂度
            fzd = pw_fzd(passwd1)
            if fzd == 0:
                st.warning("密码复杂度不够 ")
            # 判断密码重复度
            cfd = pwd_cfd(passwd1)
            if cfd == 0:
                st.warning("密码有超过三位的重复 ")
            # 密码等级
            pw_g = cd + fzd + cfd + 2
            if (pw_g == 5):
                st.warning(f"密码安全等级为{pw_g}可以注册")
                if st.sidebar.button("注册"):
                    create_usertable()
                    create_user_daytimes_table()
                    add_userdata(new_user,passwd1)
            else:
                st.warning(f"密码安全等级为{pw_g}")




    elif choice =="注销":
        st.session_state.count = 0
        if st.session_state.count == 0:
            st.info("您已成功注销，如果需要，请选择左侧的登录按钮继续登录。")



if __name__=="__main__":
    main()
