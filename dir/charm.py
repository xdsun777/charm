from selenium import webdriver
from selenium.webdriver.common.by import By
import time,re,sys


#关于引入驱动有两种方式，一是给驱动添加环境变量，二是直接引入驱动位置，我使用的是第一种方式
def login():
    start = webdriver.Chrome()
    start.get('https://passport2.chaoxing.com/login?fid=&newversion=true&refer=http://i.chaoxing.com')
    start.implicitly_wait(2)
    phone = input("请输入手机号：")
    start.find_element(By.ID, 'phone').send_keys(phone)
    paw = input("请输入密码：")
    
    start.find_element(By.ID, "pwd").send_keys(paw)
    time.sleep(2)
    start.find_element(By.ID, "loginBtn").click()
    time.sleep(2)
    return start



def curricula_variable(start):
    time.sleep(2)
    start.switch_to.frame("frame_content")
    course = input("请输入课程：")
    try:
        start.find_element(By.LINK_TEXT, course).click()
    except:
        print("请输入正确的课程名")
        print("请保证输入的课程名与页面显示的课程名一致")
        print("若有疑问请加Q：2113733946")
        sys.exit(0)
    win_List = start.window_handles
    for i in win_List:
        start.switch_to.window(i)
        if start.title == "学习进度页面":
            return start



def detection_1(start):
    list_em = len(start.find_elements(By.CSS_SELECTOR, "em.orange"))
    single_em = start.find_element(By.CSS_SELECTOR, "em.orange")
    single_em_text = single_em.find_element(By.XPATH, "../following-sibling::span").text
    single_em.find_element(By.XPATH, "../following-sibling::span").click()
    li = []
    li.append(list_em)
    li.append(single_em_text)
    return li



def detection_finish(start):
    start.switch_to.frame("iframe")
    time.sleep(2)
    try:
        start.find_element(By.CSS_SELECTOR,'div.ans-attach-ct.ans-job-finished')
        print("页面已完成完成")
        return True
    except:
        print("页面未完成")
        return False


def detection_video(start):
    time.sleep(2)
    try:
        start.switch_to.frame(start.find_element(By.TAG_NAME, "iframe"))
        start.find_element(By.TAG_NAME,"video")
        print("视频存在")
        return True
    except:
        print("视频不存在\n")
        return False


def search_video(start):
    start.switch_to.default_content()
    time.sleep(2)
    try:
        dct = start.find_elements(By.CSS_SELECTOR, "/html/body/div[3]/div/div[2]/div[1]/span[1]")  # 查找《视频》并点击
        for i in range(len(dct)):
            if dct[i].get_attribute("title")=="视频":
                return True
    except:
        return False



def play_video(start):
    time.sleep(2)
    start.find_element(By.CSS_SELECTOR, "button.vjs-big-play-button").click()#点击视频
    time.sleep(2)



def num_dispose(num):
    try:
        num.strip()
        taw = re.split(":", num)
        minute =  taw[0].strip()
        second = taw[1].strip()
        minute = int(minute)*60
        second = int(second)
        return minute+second
    except:
        print("无法获取视频时间，将设置视频播放15分钟")
        return 900



def video_time(start):
    print("获取已播放时间中。。。")
    min_time = start.find_element(By.CSS_SELECTOR, "span.vjs-current-time-display").text
    time.sleep(1)
    get_min_time = num_dispose(min_time)
    print("视频已播放：" + str(get_min_time) + "s")
    print("获取视频总时长中。。。")
    max_time = start.find_element(By.CSS_SELECTOR, "span.vjs-duration-display").text
    time.sleep(1)
    get_max_time = num_dispose(max_time)
    print("视频总时长："+str(get_max_time)+"s")
    surplus_time = get_max_time - get_min_time
    print("视频剩余时长："+str(surplus_time)+"\n")
    return surplus_time



def do_exercise(start,max_time):
    start_time = time.time()
    while  True:
       try:
            nodes = start.find_elements(By.NAME,"ans-videoquiz-opt")
            for node in nodes:
                val = node.get_attribute("value")
                if val == "true":
                    time.sleep(1)
                    node.click()
            try:
                start.find_element(By.ID,"ext-gen1044").click()
            except:
                start.find_element(By.ID,"ext-gen1043").click()
       except:
           time.sleep(2)
       end_time = time.time() - start_time
       
       if end_time>max_time:
            print(end_time,max_time)
            time.sleep(3)
            break


def click_next_page(start):
    start.switch_to.default_content()
    try:
        taw = start.find_element(By.CSS_SELECTOR, "div.orientationright")
        js = "window.scrollTo(0, document.body.scrollHeight)"
        driver.execute_script(js, taw)
        start.find_element(By.CSS_SELECTOR, "div#right2.orientationright").click()  # 定位《下一页》并点击
    except:
        try:
            start.find_element(By.CSS_SELECTOR, "div#right1.orientationright").click()
        except:
            start.find_element(By.CSS_SELECTOR, "div.orientationright").click()
            try:
                start.find_element(By.CSS_SELECTOR, "div#right3.orientationright").click()
            except:
                start.find_element(By.CSS_SELECTOR, "div.orientationright").click()


driver = login()
curricula_variable(driver)
object_list = detection_1(driver)
object_0 = object_list[0]-1
object_1 = object_list[1]
print("未学习课程数："+str(object_0)+str(1))
print("准备播放："+object_1)
for i in range(object_0):
    det_finish = detection_finish(driver)
    det_video = detection_video(driver)
    if (det_finish==False) and (det_video==True):
        play_video(driver)
        get_video_time = video_time(driver)
        do_exercise(driver, get_video_time)
        click_next_page(driver)
    else:
        if search_video(driver) == True:
            det_finish1 = detection_finish(driver)
            if det_finish1 == False:
                driver.switch_to('//*[@id="video_html5_api"]')
                play_video(driver)
                get_video_time = video_time(driver)
                do_exercise(driver,get_video_time)
                click_next_page(driver)
            else:
                click_next_page(driver)
        else:
            click_next_page(driver)
