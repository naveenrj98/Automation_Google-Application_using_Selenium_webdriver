import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import threading
from selenium.webdriver.common.action_chains import ActionChains
from tkinter.filedialog import askopenfilename
import copy

HEADING = ("Calibri", 24)
LINES = ("Calibri", 12)
task = {}
entries = []  # this has all the entries

CREATE_FOLDER = 'Create New Folder'
UPLOAD_FILE = 'Upload New File'
GOOGLE_FORM = 'Google Form Function'
DOWNLOAD_FILE = 'download file'
LOGIN = 'login'
UPLOAD_FOLDER = 'upload folder'
LOGIN_CREDENTIALS_FILE = 'login_credentials.pickle'
TASKS_FILE = 'tasks.pickle'
GMAIL_SEND_MAIL = 'gmail send mail'


class Task:
    def __init__(self, title, disc, function):
        self.title = title
        self.disc = disc
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
            self.driver = webdriver.Chrome("G:\\PROJECTS BMSCE\\NRJ&NRV\\chromedriver")
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
            # needs to have a field called folderName
            self.createFolderFunction(job.newFolder)
        elif job.function == GOOGLE_FORM:
            self.googleFormFunction()
        elif job.function == UPLOAD_FILE:
            self.uploadFileFunction()
        elif job.function == UPLOAD_FOLDER:
            self.uploadFileFunction()
        elif job.function == GMAIL_SEND_MAIL:
            self.gmailSendMailFunction(self.app.userEnt.get(), self.app.passEnt.get(), job.to_addresses, job.subject,
                                       job.body, job.attachment)

    def gmailSendMailFunction(self, *args):
        print(args)
        print('please')



















    def loginFunction(self):
        driver = self.driver
        driver.get("https://drive.google.com/drive/my-drive")
        # First step google login
        # finding login element's id
        element = driver.find_element_by_id("identifierId")
        element.clear()
        element.send_keys(self.app.userEnt.get())
        # finding next element's id
        button_element = driver.find_element_by_id("identifierNext")
        button_element.click()

        time.sleep(3)

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
        # search = driver.find_element_by_xpath("//*[@class='lb-k-Kk g-Gh']/parent::*")
        # search.find_element_by_xpath('./*').clear()
        # search.find_element_by_xpath('./*').send_keys(folderName)
        search = driver.find_element_by_xpath("//*[@class='lb-k-Kk g-Gh']")
        search.clear()
        search.send_keys(folderName)
        driver.find_element_by_xpath("//*[text()='Create']").click()

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

        form_title.clear()

        form_title.send_keys("Contact Information")

        # form_title.send_keys(Keys.ENTER)

        form_description = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[2]/div[2]/div[2]/content/div/div[1]/div[2]/textarea')
        time.sleep(1)

        form_description.clear()

        form_description.send_keys("Details of Students")

        # first_question_select=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')

        time.sleep(5)

        # first_question_select.click()

        # first_question=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[2]')
        # first_question=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div[4]')
        # time.sleep(3)
        # actions.reset_actions()
        # first_question.click()
        # time.sleep(2)

        # upbtf=driver.find_element_by_xpath("//*[contains(text(), '" + "Short answer" + "')]")
        # upbtf.click()
        # first_question.send_keys(Keys.ENTER)


        # add_question=driver.find_element_by_css_selector('.quantumWizButtonPapericonbuttonEl.quantumWizButtonPapericonbuttonLight.freebirdFormeditorViewFatMenuItem.isUndragged')

        add = driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[1]/div/div/div[1]/div')
        time.sleep(5)
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
        r1 = driver.find_element_by_xpath('//*[@id="c4"]')
        time.sleep(1)
        r1.click()
        new_ele2 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(3)
        new_ele2.send_keys('Semester :')
        r2 = driver.find_element_by_xpath('//*[@id="c10"]')
        time.sleep(1)
        r2.click()
        time.sleep(1)

        f1 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[3]/div[1]/div/content/div/div/div[1]/input')
        time.sleep(2)
        f1.clear()

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

        time.sleep(1)
        new_ele3 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[3]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(3)
        new_ele3.send_keys('Email Address ')
        r3 = driver.find_element_by_xpath('//*[@id="c17"]')
        time.sleep(1)
        r3.click()
        new_ele4 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[4]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(3)
        new_ele4.send_keys('Phone Number')
        r4 = driver.find_element_by_xpath('//*[@id="c25"]')
        time.sleep(1)
        r4.click()
        new_ele5 = driver.find_element_by_xpath(
            '//*[@id="SchemaEditor"]/div/div[2]/div/div/div[3]/div[5]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/content/div/div/div[1]/div[2]/textarea')
        time.sleep(5)
        new_ele5.clear()
        new_ele5.send_keys('Branch ')
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

        # time.sleep(2)

        # actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    def add_task(self, task):
        print(task)
        print(dir(task))
        self.jobQueue.append(task)
        self.lock.release()


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # tk.Tk.iconbitmap(self,default="Drive.ico")
        tk.Tk.wm_title(self, "Automated Google Applications")
        self.geometry("550x400")
        self.r = 1
        self.i = 0
        self.var = dict()  # this far each of the text boxes
        self.target_robots = dict()  # this is a list of text entries corresponding to the correct task
        username = ""
        password = ""
        self.widgets()
        self.load_username_and_password()
        self.load_tasks()
        self.robots = {}  # this will contain a list of all the robots this is controlling
        # self.jobQueue = []
        # self.jobQueue.append({'type': LOGIN})
        # self.jobQueue.append({'type': CREATE_FOLDER, 'folderName': 'my_new_folder_from_gui'})

    def widgets(self):
        notebook = ttk.Notebook(self, height=500)
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
        notebook.add(Start, text='Start')
        notebook.add(Gmail, text='Gmail')
        notebook.grid(row=0, column=0, sticky="NSEW")

        label = tk.Label(Intro, text="Introduction", font=HEADING)
        label.grid(row=0, column=3, columnspan=3, sticky="NSEW")

        label2 = tk.Label(Intro,
                          text="\n\nThis project is used to automate the functionalities of Google Drive. "
                          , font=LINES).grid(row=2, column=3, columnspan=3, sticky="E")

        label3 = tk.Label(Intro,
                          text="The project should be able to "
                          , font=LINES).grid(row=3, column=3, columnspan=3, sticky="W")

        label4 = tk.Label(Intro,
                          text="- Upload a spefic file to the Drive"
                          , font=LINES).grid(row=4, column=3, columnspan=3, sticky="W")

        label5 = tk.Label(Intro,
                          text="- Download a file"
                          , font=LINES).grid(row=5, column=3, columnspan=3, sticky="W")

        label6 = tk.Label(Intro,
                          text="- Create a  new folder\n\n\n\n"
                          , font=LINES).grid(row=6, column=3, columnspan=3, sticky="W")

        label7 = tk.Label(User, text="  Automated Google Applications\n", font=HEADING)
        label7.grid(row=0, column=0, columnspan=3)

        Userlabel = tk.Label(User, text="Username :", font=LINES)
        Userlabel.grid(row=2, column=1)
        self.userEnt = tk.Entry(User)
        self.userEnt.grid(row=2, column=2, sticky="W")

        Passlabel = tk.Label(User, text="Password :", font=LINES)
        Passlabel.grid(row=3, column=1)
        self.passEnt = tk.Entry(User)
        self.passEnt.grid(row=3, column=2, sticky="W")
        self.passEnt['show'] = '*'

        tk.Label(User, text="").grid(row=4)
        button1 = ttk.Button(User, text="Save",
                             command=self.check_username_and_password
                             )
        button1.grid(row=5, column=2, columnspan=3, sticky="SW")

        label8 = tk.Label(Tasks, text="\tCreate Task\n", font=HEADING)
        label8.grid(row=0, column=0, columnspan=3, sticky="E")

        Tlabel = tk.Label(Tasks, text="Title :", font=LINES)
        Tlabel.grid(row=2, column=1, sticky="E")
        self.TEntry = tk.Entry(Tasks, width=33)
        self.TEntry.grid(row=2, column=2, columnspan=2, sticky="W")

        Dlabel = tk.Label(Tasks, text="Discription :", font=LINES)
        Dlabel.grid(row=3, column=1, sticky="E")
        self.DText = tk.Text(Tasks, width=25, height=3)
        self.DText.grid(row=3, column=2, columnspan=2, rowspan=3, sticky="W")

        Flabel = tk.Label(Tasks, text="Function :", font=LINES)
        Flabel.grid(row=7, column=1, sticky="E")
        self.function = tk.StringVar()
        Popup = tk.OptionMenu(Tasks, self.function, CREATE_FOLDER
                              , UPLOAD_FILE, DOWNLOAD_FILE, GOOGLE_FORM, UPLOAD_FOLDER, command=self.type)
        Popup.grid(row=7, column=2, sticky="E")

        label9 = tk.Label(Start, text="\tStart Process\n", font=HEADING)
        label9.grid(row=0, column=0, columnspan=3, sticky="E")

        button2 = ttk.Button(self.Start, text="Start", command=self.startClicked)
        button2.grid(row=50, column=3, sticky="SW")
        button3 = ttk.Button(self.Start, text="Remove", command=self.removeClick)
        button3.grid(row=50, column=0, sticky="SW")

        # gmail part
        self.gmail_function = tk.StringVar()
        gmail_drop_down = tk.OptionMenu(Gmail, self.gmail_function, "Send Mails", 'Read Mails')
        gmail_drop_down.grid(row=0, column=0)
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

        tk.Button(Gmail, text='SEND!', command=self.gmail_send).grid(row=80, column=1)
        tk.Button(Gmail, text='Explore', command=self.startFileExplorer).grid(row=70, column=3)

    def startFileExplorer(self):
        fname = askopenfilename()
        self.gmail_attachment.delete(0.0, tk.END)
        self.gmail_attachment.insert(0.0, fname)

    def gmail_send(self):
        self.gmail_robot = Robot(self)
        self.gmail_robot.lock.acquire()
        task = Task('this is gmail task', 'disc', GMAIL_SEND_MAIL)
        task.to_addresses = self.gmail_to.get(0.0, tk.END)
        task.subject = self.gmail_subject.get(0.0, tk.END)
        task.body = self.gmail_body.get(0.0, tk.END)
        task.attachment = self.gmail_attachment.get(0.0, tk.END)
        self.gmail_robot.add_task(task)
        self.gmail_robot.start()

    def type(self, *args):
        if self.function.get() == CREATE_FOLDER:
            Newlabel = tk.Label(self.Tasks, text="Folder Name :", font=LINES)
            Newlabel.grid(row=8, column=1, sticky="E")
            self.NEntry = tk.Entry(self.Tasks, width=33)
            self.NEntry.grid(row=8, column=2, columnspan=2, sticky="W")
        elif self.function.get() == UPLOAD_FILE:
            Uplabel = tk.Label(self.Tasks, text="Select File :", font=LINES)
            Uplabel.grid(row=8, column=1, sticky="E")
            self.UpEntry = tk.Entry(self.Tasks, width=33)
            self.UpEntry.grid(row=8, column=2, columnspan=2, sticky="W")
        elif self.function.get() == DOWNLOAD_FILE:
            Downlabel = tk.Label(self.Tasks, text="Enter Name :", font=LINES)
            Downlabel.grid(row=8, column=1, sticky="E")
            self.DownEntry = tk.Entry(self.Tasks, width=33)
            self.DownEntry.grid(row=8, column=2, columnspan=2, sticky="W")

        tk.Label(self.Tasks, text="\n").grid(row=9)
        button2 = ttk.Button(self.Tasks, text="Save",
                             command=self.MakeTask)
        button2.grid(row=10, column=3, columnspan=3, sticky="SW")

    def MakeTask(self, *args):
        if not self.TEntry.get() or not self.DText.get("1.0", "end"):
            tk.Label(self.Tasks, text="Please Enter all the fields", foreground="red"
                     ).grid(row=9, column=2, columnspan=3, sticky="SW")
        else:
            task = Task(self.TEntry.get(), self.DText.get("1.0", "end"), self.function.get())
            # task['title'] = self.TEntry.get()
            # task['disc'] = self.DText.get("1.0", "end")
            # task['func'] = self.function.get()
            if self.function.get() == CREATE_FOLDER:
                task.newFolder = self.NEntry.get()
                self.NEntry.delete(0, 'end')
            elif self.function.get() == UPLOAD_FOLDER:
                task.uploadDir = self.UpEntry.get()
                self.UpEntry.delete(0, 'end')
            elif self.function.get() == DOWNLOAD_FILE:
                task.downloadName = self.DownEntry.get()
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
            titLabel.grid(row=self.r, column=1, rowspan=2, sticky="S")
            discLabel = tk.Label(self.Start, text=task.disc, wraplength=100, font=LINES)
            discLabel.grid(row=self.r, column=2, rowspan=2, sticky="SW")
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
            alert = tk.Label(self.User, text="Please Enter both Username and Password", foreground="red")
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
        # self.robots.update({"robo1": Robot(self)})
        # self.robots['robo1'].lock.acquire()
        # self.robots['robo1'].start()
        # self.robots.update({"robo2": Robot(self)})
        # self.robots['robo2'].lock.acquire()
        # self.robots['robo2'].start()
        # time.sleep(10)
        # self.robots['robo1'].addTask({'type': LOGIN})
        i = 0
        while i < len(entries):
            if self.var[i].get():
                robot_names = self.target_robots[i].get().split(',')
                for robot_name in robot_names:
                    if robot_name in self.robots.keys():
                        # self.robots[robot_name].add_task(Task('temp', 'desc', LOGIN))
                        self.robots[robot_name].add_task(copy.copy(entries[i]))
                    else:
                        self.robots.update({robot_name: Robot(self)})
                        self.robots[robot_name].lock.acquire()
                        self.robots[robot_name].start()  # self.robot.startSequence()
                        self.robots[robot_name].add_task(copy.copy(entries[i]))
            i += 1

    def removeClick(self):
        i = 0
        while i < len(entries):
            if self.var[i].get():
                # robot_names = self.target_robots[i].get().split(',')
                # for robot_name in robot_names:
                #     if robot_name in self.robots.keys():
                #         # self.robots[robot_name].add_task(Task('temp', 'desc', LOGIN))
                #         self.robots[robot_name].add_task(copy.copy(entries[i]))
                #     else:
                #         self.robots.update({robot_name: Robot(self)})
                #         self.robots[robot_name].lock.acquire()
                #         self.robots[robot_name].start()  # self.robot.startSequence()
                #         self.robots[robot_name].add_task(copy.copy(entries[i]))
                del entries[i]
            i += 1
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

        label9 = tk.Label(Start, text="\tStart Process\n", font=HEADING)
        label9.grid(row=0, column=0, columnspan=3, sticky="E")

        button2 = ttk.Button(self.Start, text="Start", command=self.startClicked)
        button2.grid(row=50, column=3, sticky="SW")
        button3 = ttk.Button(self.Start, text="Remove", command=self.removeClick)
        button3.grid(row=50, column=0, sticky="SW")
        self.load_tasks()


if __name__ == "__main__":
    app = SampleApp()
    robo = Robot(app)
    app.mainloop()
