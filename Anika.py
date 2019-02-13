import time
import copy
import pickle
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

HEADING = ("Berlin Sans FB", 20)
LINES = ("Century Schoolbook", 12)
task = {}
entries = []  # this has all the entries

LOGIN = 'Login'
CREATE_FOLDER = 'Create New Folder'
UPLOAD_FILE = 'File Upload'
UPLOAD_FOLDER = 'Folder Upload'
GOOGLE_FORM = 'Google Form'
SEARCH_FILE='Search for a File'
GMAIL_SEND_MAIL = 'Send a Mail'
GMAIL_READ_MAIL = 'Read a Mail'
LOGIN_CREDENTIALS_FILE = 'login_credentials.pickle'
TASKS_FILE = 'tasks.pickle'

class Task:
    def __init__(self, title, desc, function):
        self.title = title
        self.desc = desc
        self.function = function

class Robot(threading.Thread):

    def __init__(self, a):
        super(Robot, self).__init__()
        self.app = a  # app is the reference to Sample App
        self.driver = None  # this will hold the reference to the driver
        # app.robots.update() = self  # todo important
        self.actions = None
        self.jobQueue = []
        self.lock = threading.Lock()
        self.logged_in_to_drive = False

    def run(self):
        super(Robot, self).run()
        self.startSequence()

    def startSequence(self):
        if self.driver == None:
            self.driver = webdriver.Chrome("C:\\Users\\jyothiramesh\\Desktop\\samrt\\project\\chromedriver.exe")
            self.actions = ActionChains(self.driver)
        while True:
            self.actions.reset_actions()
            if len(self.jobQueue) > 0:
                job = self.jobQueue[0]
                del self.jobQueue[0]
                self.execute(job)
            else:
                try:
                    self.lock.acquire()
                except:
                    pass

    def execute(self, job):
        driver = self.driver
        if job.function == LOGIN:
            self.loginFunction()
        elif job.function == CREATE_FOLDER:
            self.createFolderFunction(job.newFolder)
        elif job.function == UPLOAD_FILE:
            self.uploadFileFunction(job.uploadDir)
        elif job.function == UPLOAD_FOLDER:
            self.uploadFolderFunction(job.newFol)
        elif job.function == GOOGLE_FORM:
            self.googleFormFunction()
        elif job.function == SEARCH_FILE:
            self.searchFileFunction(job.fileName)
        elif job.function == GMAIL_SEND_MAIL:
            self.gmailSendMailFunction(self.app.userEnt.get(), self.app.passEnt.get(), job.to_addresses, job.subject,job.body, job.attachment)
        elif job.function == GMAIL_READ_MAIL:
            self.gmailReadMailFunction()

    def loginFunction(self):
        driver = self.driver
        driver.get('https://www.google.com/intl/en/drive/')
        time.sleep(3)
        a = driver.find_elements_by_xpath("//*[contains(text(), '" + "Go to Google Drive" + "')]")
        try:
            a[1].click()
        except:
            print("II")
        # First step google login
        # finding login element's id
        element = driver.find_element_by_id("identifierId")
        element.clear()
        element.send_keys(self.app.userEnt.get())

        # finding next element's id
        button_element = driver.find_element_by_id("identifierNext")
        button_element.click()
        time.sleep(2)

        # finding password element's xpath
        password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password.clear()
        password.send_keys(self.app.passEnt.get())

        # finding next button's id
        button_element1 = driver.find_element_by_id("passwordNext")
        button_element1.click()
        time.sleep(5)
        self.logged_in_to_drive = True

    def createFolderFunction(self, folderName):
        driver = self.driver
        if not self.logged_in_to_drive:
            self.loginFunction()
        newbt = driver.find_element_by_xpath(
            '//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/button[1]/div[2]')
        time.sleep(2)
        actions = self.actions
        actions.reset_actions()
        actions.click(newbt).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        search = driver.find_element_by_xpath("//*[@class='lb-k-Kk g-Gh']")
        search.clear()

        search.send_keys(folderName)
        driver.find_element_by_xpath("//*[text()='Create']").click()
        time.sleep(2)

    def uploadFileFunction(self, fileName):
        driver = self.driver
        actions = self.actions
        if not self.logged_in_to_drive:
            self.loginFunction()
        newbt = driver.find_element_by_xpath(
            '//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/button[1]/div[2]')
        time.sleep(2)
        actions.reset_actions()
        #newbt.send_keys(Keys.ENTER)
        time.sleep(3)
        actions.click(newbt).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        FileUp = driver.find_element_by_xpath("//input[@type='file']")
        FileUp.send_keys(fileName)
        time.sleep(2)

    def uploadFolderFunction(self, folderName):
        driver = self.driver
        actions = self.actions
        if not self.logged_in_to_drive:
            self.loginFunction()
        newbt = driver.find_element_by_xpath(
            '//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/button[1]/div[2]')
        time.sleep(2)
        actions.reset_actions()
        actions.click(newbt).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        time.sleep(2)
        filepath = driver.find_element_by_xpath("//input[@type='file']")
        #fn1 = '"' + str("\\\\" + folderName.split("/")) + '"'
        #print("Folder" + fn1)
        filepath.send_keys(folderName)
        time.sleep(2)

    def googleFormFunction(self):
        driver = self.driver
        actions = self.actions
        if not self.logged_in_to_drive:
            self.loginFunction()

        new_button = driver.find_element_by_xpath(
            '//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/button[1]')

        new_button.click()

        for i in range(0, 7):
            new_button.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)

        new_button.send_keys(Keys.ARROW_RIGHT)
        new_button.send_keys(Keys.ARROW_RIGHT)
        new_button.send_keys(Keys.ENTER)

        time.sleep(2)

        a = driver.window_handles[1]

        driver.switch_to_window(str(a))

        time.sleep(8)

        form_title = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[2]/div[2]/div[1]/content/div/div[1]/div[2]/textarea')

        form_title.send_keys(Keys.CONTROL + "a")
        form_title.send_keys(Keys.DELETE)
        form_title.send_keys("Goldman Sachs Internship Application")

        # form_title.send_keys(Keys.ENTER)

        form_description = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[2]/div[2]/div[2]/content/div/div[1]/div[2]/textarea')
        time.sleep(1)

        form_description.clear()

        form_description.send_keys("2020 graduating candidates from the courses: CSE/ECE/EEE/ISE")
        time.sleep(5)

        add = driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[1]/div/div/div[1]/div')
        time.sleep(2)
        add.click()
        time.sleep(2)
        add.click()
        time.sleep(2)
        add.click()
        time.sleep(2)
        add.click()
        time.sleep(5)

        new_ele = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(3)
        new_ele.send_keys('Name :')

        new_ele2 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(3)
        new_ele2.send_keys('Semester :')
        time.sleep(1)

        f1 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[3]/div[1]/div/content/div/div/div[1]/input')
        time.sleep(2)
        f1.send_keys(Keys.CONTROL + "a")
        f1.send_keys(Keys.DELETE)
        f1.send_keys('1st')
        f2 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/div[2]/input')
        time.sleep(2)
        f2.clear()
        f2.send_keys('3rd')
        f3 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/div[2]/input')
        time.sleep(2)
        f3.clear()
        f3.send_keys('5th')
        f4 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/div[2]/input')
        time.sleep(2)
        f4.clear()
        f4.send_keys('7th')
        time.sleep(2)

        new_ele3 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[3]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(2)
        new_ele3.send_keys('Email Address ')
        new_ele4 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[4]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(2)

        new_ele4.send_keys('Phone Number')
        new_ele5 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[5]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(1)
        new_ele5.clear()
        new_ele5.send_keys('Grade ')
        r5 = driver.find_element_by_xpath('//*[@id="i2"]')
        time.sleep(1)
        r5.click()
        time.sleep(1)

        new_ref = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[5]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]')
        actions.reset_actions()
        actions.move_to_element(new_ref)
        time.sleep(2)
        actions.click()
        time.sleep(1)

        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(1)
        actions.send_keys(Keys.ENTER).perform()

    def searchFileFunction(self, fileName):
        driver = self.driver
        actions = self.actions
        if not self.logged_in_to_drive:
            self.loginFunction()

        search = driver.find_elements_by_xpath("//*[@type='text']")
        search[1].send_keys(fileName)
        search[1].send_keys(Keys.RETURN)
        time.sleep(3)

    def gmailSendMailFunction(self, *args):
        driver = self.driver
        actions = self.actions
        GMAIL_USER = args[0]
        GMAIL_PASSWORD = args[1]
        TO = args[2]
        SUBJECT = args[3]
        MESSAGE = args[4]
        ATTACH = args[5]
        #print("Attach"+ATTACH)

        # Navigate to Gmail
        is_logged_in = False
        google_login = "https://gmail.com"

        try:
            driver.get(google_login)
            time.sleep(5)

            # get userName input id
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, 'identifierId')))

            # write user name
            element.clear()
            element.send_keys(GMAIL_USER)

            # finding next element's id
            button_element = driver.find_element_by_id("identifierNext")
            button_element.click()

            time.sleep(1)

            # finding password element's xpath
            wait1 = WebDriverWait(driver, 10)
            password = wait1.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))

            # write password
            password.clear()
            password.send_keys(GMAIL_PASSWORD)

            # finding next button's id
            time.sleep(1)
            button_element1 = driver.find_element_by_id("passwordNext")
            button_element1.click()

            time.sleep(4)

        except Exception as ex:
            print(str(ex))
            is_logged_in = False
        # Verify login
        assert "Gmail" in driver.title

        # clicking on compose in gmail
        time.sleep(4)
        a = driver.find_element_by_class_name("aic").click();
        time.sleep(4)

        # find "to" elements Xpath
        p = driver.find_element_by_name("to")
        p.send_keys(TO)

        # find "subject" elements xpath
        time.sleep(4)
        sub = driver.find_element_by_name("subjectbox")
        sub.send_keys(SUBJECT)
        #time.sleep(4)

        # find Body xpath
        content = driver.find_element_by_xpath("//*[@class='Am Al editable LW-avf']")
        content.send_keys(MESSAGE)
        time.sleep(4)

        # find send button xpath
        fbt = driver.find_element_by_xpath("//*[@class='wG J-Z-I']")
        fbt.click()
        time.sleep(4)

        # find attach button xpath
        driver.find_element_by_xpath("//input[@type='file']").send_keys(ATTACH)
        #fiup.send_keys(ATTACH)

        time.sleep(4)
        #actions.reset_actions()
        actions.click(content).send_keys(Keys.CONTROL, Keys.ENTER).perform()

    def gmailReadMailFunction(self):

        driver = self.driver
        actions = self.actions
        # Navigate to Gmail
        is_logged_in = False
        google_login = 'https://gmail.com'

        try:
            driver.get(google_login)
            time.sleep(5)

            # get userName input id
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, 'identifierId')))

            # write user name
            element.clear()
            element.send_keys(self.app.userEnt.get())

            # finding next element's id
            button_element = driver.find_element_by_id("identifierNext")
            button_element.click()

            time.sleep(1)

            # finding password element's xpath
            wait1 = WebDriverWait(driver, 10)
            password = wait1.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))

            # write password
            password.clear()
            password.send_keys(self.app.passEnt.get())

            # finding next button's id
            time.sleep(1)
            button_element1 = driver.find_element_by_id("passwordNext")
            button_element1.click()

            time.sleep(4)

        except Exception as ex:
            print(str(ex))
            is_logged_in = False
        # Verify login
        assert "Gmail" in driver.title

        # reading of the mail
        tbody = driver.find_element_by_xpath('//*[@class="F cf zt"]/tbody')
        for row in tbody.find_elements_by_xpath(".//tr"):
            from1 = row.find_elements_by_xpath(".//*[@class='yW']")
            subj = row.find_elements_by_xpath(".//*[@class='y6']")
            print(from1[0].text)
            print(subj[0].text)

    def add_task(self, task):
        print(task)
        print(dir(task))
        self.jobQueue.append(task)
        self.lock.release()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap(self,default="Drive.ico")
        #tk.Tk.wm_title(self, "Automating Google Applications")
        self.geometry("600x450")
        username = ""
        password = ""
        self.r = 3
        self.i = 0
        self.var = {}  # this for each of the text boxes
        self.target_robots = {}  # this is a list of text entries corresponding to the correct task
        self.robots = {}   # this will contain a list of all the robots this is controlling
        self.widgets()
        self.load_username_and_password()
        self.load_tasks()


    def widgets(self):
        notebook = ttk.Notebook(self, height=450, width=600)
        self.notebook = notebook
        Intro = ttk.Frame(notebook)
        User = ttk.Frame(notebook)
        Tasks = ttk.Frame(notebook)
        Start = ttk.Frame(notebook)
        Gmail = ttk.Frame(notebook)

        self.User = User  # I did this just so that the check function can create Label
        self.Tasks = Tasks
        self.Start = Start
        self.Gmail = Gmail

        notebook.add(Intro, text='Introduction')
        notebook.add(User, text='User')
        notebook.add(Tasks, text='Tasks')
        notebook.add(Gmail, text='Gmail')
        notebook.add(Start, text='Start')
        notebook.grid(row=0, column=0, sticky="NSEW")

        label = tk.Label(Intro, text="Introduction", font=HEADING)
        label.grid(row=0, column=3, columnspan=3, sticky="NSEW")

        label2 = tk.Label(Intro,
                          text="\n\tThis project is designed to automate the functionalities of various \nGoogle Applications "
                          , font=LINES).grid(row=2, column=3, columnspan=3, sticky="E")

        label3 = tk.Label(Intro,
                          text="\n   The application is able to "
                          , font=LINES).grid(row=3, column=3, columnspan=3, sticky="W")

        label4 = tk.Label(Intro,
                          text="\n\t- Create a  new folder"
                          , font=LINES).grid(row=4, column=3, columnspan=3, sticky="W")

        label5 = tk.Label(Intro,
                          text="\n\t- Upload a spefic file/folder to the Drive"
                          , font=LINES).grid(row=5, column=3, columnspan=3, sticky="W")

        label6 = tk.Label(Intro,
                          text="\n\t- Search for a particular file\n"
                          , font=LINES).grid(row=6, column=3, columnspan=3, sticky="W")

        label61 = tk.Label(Intro,
                           text="\t- Sending or Reading Mails\n\n\n\n"
                           , font=LINES).grid(row=7, column=3, columnspan=3, sticky="W")



        it creates a list of tasks that have to be done. Later the user can approve all the tasks in the list, and the application will do all the tasks automatically.

        tk.Label(User, text="").grid(row=0)
        label7 = tk.Label(User, text=" \t Automating Google Applications\n", font=HEADING)
        label7.grid(row=1, column=1, columnspan=3)

        tk.Label(User, text="").grid(row=2, column=1)
        tk.Label(User, text="").grid(row=3)
        Userlabel = tk.Label(User, text="User Name :", font=LINES)
        Userlabel.grid(row=4, column=1)
        self.userEnt = tk.Entry(User, width=30)
        self.userEnt.grid(row=4, column=2, columnspan=2, sticky="W")

        tk.Label(User, text="").grid(row=5)

        Passlabel = tk.Label(User, text="Password :", font=LINES)
        Passlabel.grid(row=6, column=1)
        self.passEnt = tk.Entry(User, width=30)
        self.passEnt.grid(row=6, column=2, sticky="W")
        self.passEnt['show'] = '*'

        tk.Label(User, text="").grid(row=7)
        tk.Label(User, text="").grid(row=8)

        button1 = ttk.Button(User, text="Save",
                             command=self.check_username_and_password
                             )
        button1.grid(row=9, column=3, sticky="W")

        tk.Label(Tasks, text="").grid(row=0)
        label8 = tk.Label(Tasks, text="\tCreate a Task\n", font=HEADING)
        label8.grid(row=1, column=0, columnspan=3, sticky="E")

        Tlabel = tk.Label(Tasks, text="Title :", font=LINES)
        Tlabel.grid(row=2, column=1, sticky="E")
        self.TEntry = tk.Entry(Tasks, width=33)
        self.TEntry.grid(row=2, column=2, columnspan=2, sticky="W")
        tk.Label(Tasks, text="").grid(row=3)
        Dlabel = tk.Label(Tasks, text="Description :", font=LINES)
        Dlabel.grid(row=4, column=1, sticky="E")
        self.DText = tk.Text(Tasks, width=25, height=3)
        self.DText.grid(row=4, column=2, columnspan=2, rowspan=3, sticky="W")
        tk.Label(Tasks, text="").grid(row=5)
        tk.Label(Tasks, text="").grid(row=6)
        Flabel = tk.Label(Tasks, text="Function :", font=LINES)
        Flabel.grid(row=7, column=1, sticky="E")
        self.function = tk.StringVar()
        Popup = tk.OptionMenu(Tasks, self.function, CREATE_FOLDER
                              , UPLOAD_FILE, UPLOAD_FOLDER, GOOGLE_FORM, SEARCH_FILE, command=self.type)
        Popup.grid(row=7, column=2, sticky="E")
        tk.Label(Tasks, text="").grid(row=8)

        label9 = tk.Label(Start, text="\t Start a Process\n", font=HEADING)
        label9.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        label9 = tk.Label(Start, text="Task\n", font=LINES)
        label9.grid(row=2, column=1, sticky="W")
        label9 = tk.Label(Start, text="Description\n", font=LINES)
        label9.grid(row=2, column=2,sticky="W")

        button2 = ttk.Button(self.Start, text="Start", command=self.startClicked)
        button2.grid(row=50, column=3, sticky="SW")
        button3 = ttk.Button(self.Start, text="Remove", command=self.removeClick)
        button3.grid(row=50, column=1, sticky="SW")

        # gmail part
        self.gmail_function = tk.StringVar()
        gmail_drop_down = tk.OptionMenu(Gmail, self.gmail_function, "Send Mails", 'Read Mails')
        gmail_drop_down.grid(row=0, column=55)
        tk.Label(Gmail, text="\t\t").grid(row=5)

       # self.arr = tk.PhotoImage(file=r'C:\\Users\\Neha\\Desktop\\arr.png')
        #self.small_aks = self.arr.subsample(27, 27)
       # gmail_drop_down.config(image=self.small_aks, compound=tk.LEFT)
        # arrow = tk.PhotoImage("C:\\Users\\Neha\\Desktop\\darr.gif")
        # gmail_drop_down.configure(compound='right', image=arrow, width=35, height=20) #indicatoron=0

        tk.Label(Gmail, text="To:").grid(row=10, column=0)
        tk.Label(Gmail, text=" ").grid(row=20, column=0)
        tk.Label(Gmail, text="Subject:").grid(row=30, column=0)
        tk.Label(Gmail, text=" ").grid(row=40, column=0)
        tk.Label(Gmail, text="Body:").grid(row=50, column=0)
        tk.Label(Gmail, text=" ").grid(row=60, column=0)
        tk.Label(Gmail, text="Attachment:").grid(row=70, column=0)

        self.gmail_to = tk.Text(Gmail, width=40, height=1)
        self.gmail_to.grid(row=10, column=1)
        self.gmail_subject = tk.Text(Gmail, width=40, height=1)
        self.gmail_subject.grid(row=30, column=1)
        self.gmail_body = tk.Text(Gmail, width=40, height=10)
        self.gmail_body.grid(row=50, column=1)
        self.gmail_attachment = tk.Text(Gmail, width=40, height=1)
        self.gmail_attachment.grid(row=70, column=1)

        tk.Label(Gmail, text="").grid(row=75)
        tk.Button(Gmail, text='SEND!', command=self.gmail_send).grid(row=80, column=1)
        tk.Button(Gmail, text='Explore', command=self.startFileExplorer).grid(row=70, column=45, sticky="E")

    def startFileExplorer(self):
        fname = askopenfilename()
        #ffname =str("//".join(fname.split("/")))
        #print("File Name :" + ffname, end=" ")
        self.gmail_attachment.delete(0.0, tk.END)
        self.gmail_attachment.insert(0.0, fname)

    def startFileDialog(self):
        fname = askopenfilename()
       # fname = askopenfilename()
        #ffname = '"' + str("//".join(fname.split("/"))) + '"'
        print(fname)
        self.UpEntry.delete(0, tk.END)
        self.UpEntry.insert(0, fname)

    def startFoldDialog(self):
        fname = askdirectory()
        #ffname = '"' + str("//".join(fname.split("/"))) + '"'
        self.UpEnt.delete(0, tk.END)
        self.UpEnt.insert(0, fname)

    def gmail_send(self):
        self.gmail_robot = Robot(self)
        self.gmail_robot.lock.acquire()
        task = Task('Sending a Mail', 'desc', GMAIL_SEND_MAIL)
        task.to_addresses = self.gmail_to.get(0.0, tk.END)
        task.subject = self.gmail_subject.get(0.0, tk.END)
        task.body = self.gmail_body.get(0.0, tk.END)
        task.attachment = self.gmail_attachment.get("1.0",'end-1c')
        #print("task attach" + task.attachment)
        self.gmail_robot.add_task(task)
        self.gmail_robot.start()

    def type(self, *args):
        if self.function.get() == CREATE_FOLDER:
            Newlabel = tk.Label(self.Tasks, text="Folder Name :", font=LINES)
            Newlabel.grid(row=9, column=1, sticky="E")
            self.NEntry = tk.Entry(self.Tasks, width=40)
            self.NEntry.grid(row=9, column=2, columnspan=2, sticky="W")
        elif self.function.get() == UPLOAD_FILE:
            Uplabel = tk.Label(self.Tasks, text="Select File :", font=LINES)
            Uplabel.grid(row=9, column=1, sticky="W")
            self.UpEntry = tk.Entry(self.Tasks, width=40)
            self.UpEntry.grid(row=9, column=2, columnspan=2, sticky="W")
            tk.Button(self.Tasks, text='Explore', command=self.startFileDialog).grid(row=9, column=3, sticky="E")

        elif self.function.get() == SEARCH_FILE:
            Downlabel = tk.Label(self.Tasks, text="Enter Name :", font=LINES)
            Downlabel.grid(row=9, column=1, sticky="W")
            self.DownEntry = tk.Entry(self.Tasks, width=40)
            self.DownEntry.grid(row=9, column=2, columnspan=2, sticky="W")
        elif self.function.get() == UPLOAD_FOLDER:
            Upla = tk.Label(self.Tasks, text="Select Folder :", font=LINES)
            Upla.grid(row=9, column=1, sticky="W")
            self.UpEnt = tk.Entry(self.Tasks, width=40)
            self.UpEnt.grid(row=9, column=2, columnspan=2, sticky="W")
            tk.Button(self.Tasks, text='Explore', command=self.startFoldDialog).grid(row=9, column=3, sticky="E")
        if self.function.get() == GOOGLE_FORM:
            Newlabel = tk.Label(self.Tasks, text="", font=LINES)
            Newlabel.grid(row=9, column=1, sticky="W")

        tk.Label(self.Tasks, text="\n").grid(row=10)
        button2 = ttk.Button(self.Tasks, text="Add Task",
                             command=self.MakeTask)
        button2.grid(row=11, column=3, columnspan=3, sticky="SW")

    def MakeTask(self, *args):
        if not self.TEntry.get() or not self.DText.get("1.0", "end"):
            tk.Label(self.Tasks, text=" *** Please Enter all the fields", foreground="red"
                     ).grid(row=9, column=2, columnspan=3, sticky="SW")
        else:
            task = Task(self.TEntry.get(), self.DText.get("1.0", "end"), self.function.get())
            if self.function.get() == CREATE_FOLDER:
                task.newFolder = self.NEntry.get()
                self.NEntry.delete(0, 'end')
            elif self.function.get() == UPLOAD_FILE:
                task.uploadDir = self.UpEntry.get()
                self.UpEntry.delete(0, 'end')

            elif self.function.get() == UPLOAD_FOLDER:
                task.newFol = self.UpEnt.get()
                self.UpEnt.delete(0, 'end')
            elif self.function.get() == SEARCH_FILE:
                task.fileName = self.DownEntry.get()
                self.DownEntry.delete(0, 'end')
            entries.append(task)
            self.TEntry.delete(0, 'end')
            self.DText.delete(0.0, 'end')

            self.var[self.i] = tk.BooleanVar()
            chk = tk.Checkbutton(self.Start, variable=self.var[self.i])
            chk.grid(row=self.r, column=0, rowspan=2, sticky="W")
            self.target_robots[self.i] = tk.Entry(self.Start)
            self.target_robots[self.i].grid(row=self.r, column=3, rowspan=2)
            titLabel = tk.Label(self.Start, text=task.title, wraplength=100, font=LINES)
            titLabel.grid(row=self.r, column=1, rowspan=2, sticky="N")
            discLabel = tk.Label(self.Start, text=task.desc, wraplength=100, font=LINES)
            discLabel.grid(row=self.r, column=2, rowspan=2, sticky="NW")
            self.r = self.r + 2
            self.i = self.i + 1

            # serialize and write to file
            with open(TASKS_FILE, 'wb') as f:
                try:
                    pickle.dump(entries, f)
                except Exception as e:
                    print(e)

    def make_task_from_params(self, task):
        entries.append(task)

        self.var[self.i] = tk.BooleanVar()
        chk = tk.Checkbutton(self.Start, variable=self.var[self.i])
        self.target_robots[self.i] = tk.Entry(self.Start)
        self.target_robots[self.i].grid(row=self.r, column=3, rowspan=2)
        chk.grid(row=self.r, column=0, rowspan=2, sticky="W")
        titLabel = tk.Label(self.Start, text=task.title, wraplength=100, font=LINES)
        titLabel.grid(row=self.r, column=1, rowspan=2, sticky="S")
        discLabel = tk.Label(self.Start, text=task.disc, wraplength=100, font=LINES)
        discLabel.grid(row=self.r, column=2, rowspan=2, sticky="SW")
        self.r = self.r + 2
        self.i = self.i + 1

    def load_tasks(self):
        try:
            with open(TASKS_FILE, 'rb') as f:
                all_tasks = pickle.load(f)
                for task in all_tasks:
                    self.make_task_from_params(task)
        except:
            pass

    def check_username_and_password(self):
        if not self.userEnt.get() or not self.passEnt.get():
            alert = tk.Label(self.User, text="*** Please Enter both Username and Password", foreground="red")
            alert.grid(row=1, column=2, sticky="W")
        else:
            username = self.userEnt.get()  # Username
            password = self.passEnt.get()  # Password
            # save the password to a serialized file file
            pickle.dump({"username": username, "password": password}, open(LOGIN_CREDENTIALS_FILE, 'wb'))

    def load_username_and_password(self):
        try:
            with open(LOGIN_CREDENTIALS_FILE, 'rb') as f:
                cred = pickle.load(f)
                self.userEnt.delete(0, tk.END)
                self.userEnt.insert(0, cred['username'])
                self.passEnt.delete(0, tk.END)
                self.passEnt.insert(0, cred['password'])
        except:
            pass

    def startClicked(self):
        k = 0
        while k < len(entries):
            if (self.var[k].get()):
                robot_names = self.target_robots[k].get().split(',')
                for robot_name in robot_names:
                    if robot_name in self.robots.keys():
                        # self.robots[robot_name].add_task(Task('temp', 'desc', LOGIN))
                        self.robots[robot_name].add_task(copy.copy(entries[k]))
                    else:
                        self.robots.update({robot_name: Robot(self)})
                        self.robots[robot_name].lock.acquire()
                        self.robots[robot_name].start()  # self.robot.startSequence()
                        self.robots[robot_name].add_task(copy.copy(entries[k]))
            k += 1

    def removeClick(self):
        n = 0
        while n < len(entries):
            if (self.var[n].get()):
                del entries[n]
            n += 1
        with open(TASKS_FILE, 'wb') as f:
            try:
                pickle.dump(entries, f)
            except Exception as e:
                print(e)
        self.Start.destroy()
        entries.clear()
        notebook = self.notebook
        Start = ttk.Frame(notebook)
        self.Start = Start
        notebook.add(Start, text='Start')

        label9 = tk.Label(Start, text="\t Start a Process\n", font=HEADING)
        label9.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        label9 = tk.Label(Start, text="Task\n", font=LINES)
        label9.grid(row=2, column=1, sticky="W")
        label9 = tk.Label(Start, text="Description\n", font=LINES)
        label9.grid(row=2, column=2, sticky="W")

        button2 = ttk.Button(self.Start, text="Start", command=self.startClicked)
        button2.grid(row=50, column=3, sticky="SW")
        button3 = ttk.Button(self.Start, text="Remove", command=self.removeClick)
        button3.grid(row=50, column=1, sticky="SW")
        self.load_tasks()

if __name__ == "__main__":
    app = SampleApp()
    robo = Robot(app)
    app.mainloop()