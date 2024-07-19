from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPolygonF, QPainterPath, QColor, QPen
from find import find_core_combinations
import json
import os

import MSFindPerfectCoresUI
import formPerfectCores

"""
connect某物件做某動作連接到某function，function可以疊加
disconnect將某物件做某動作所有連接的function刪除
"""

class FindPerfectCores(QtCore.QThread):
    # 當任務完成發出信號
    finished = QtCore.pyqtSignal()

    def __init__(self, cores, core_count, enumerate_mode, selected_perfect_cores):
        super().__init__()
        self.cores = cores
        self.core_count = core_count
        self.enumerate_mode = enumerate_mode
        self.selected_perfect_cores = selected_perfect_cores
        self.text = ''

    def run(self):
        perfect_core_combination = find_core_combinations(self.cores, self.core_count, self.enumerate_mode, self.selected_perfect_cores)
        if perfect_core_combination:
            for index, perfect_core in enumerate(perfect_core_combination):
                self.text += f'-----第{index + 1}組解-----\n'
                for i, core in enumerate(perfect_core):
                    self.text += f'第{i + 1}顆核心：{core}\n'
        else:
            self.text = '未找到完美核心'

        self.finished.emit()

    def get_text(self):
        return self.text

class Main(QtWidgets.QMainWindow, MSFindPerfectCoresUI.Ui_MSFindPerfectCores):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 設定對齊方法靠左
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)  

        # 設定變數
        self.data = self.read_job_data()
        self.select_perfect_cores = [False] * 15
        # 技能按鈕
        self.button_skill_list = [
            self.buttonSkill_1, self.buttonSkill_2, self.buttonSkill_3,
            self.buttonSkill_4, self.buttonSkill_5, self.buttonSkill_6,
            self.buttonSkill_7, self.buttonSkill_8, self.buttonSkill_9,
            self.buttonSkill_10, self.buttonSkill_11, self.buttonSkill_12,
            self.buttonSkill_13, self.buttonSkill_14, self.buttonSkill_15
        ]
        # 篩選技能按鈕
        self.button_select_skill_list = [
            self.buttonMainCore,
            self.buttonSecondCore,
            self.buttonThirdCore
        ]
        # 核心
        self.select_skills = [-1, -1, -1]
        # 篩選核心列表
        self.cores = []
        # 需要修改技能
        self.skill_id = -1

        # 初始化下拉式選單
        self.update_job_name()
        self.update_skill_image()

        # 當職業下拉列表變化時，更新職業名稱下拉列表
        self.jobGroup.currentIndexChanged.connect(self.update_job_name)
        self.job.currentIndexChanged.connect(self.update_job_name)
        # 當職業名稱下拉列表變化時，更新技能按鈕圖示
        self.jobName.currentIndexChanged.connect(self.update_skill_image)
        # 載入、儲存使用者資料
        self.buttonLoad.clicked.connect(self.load_user_job_file)
        self.buttonSave.clicked.connect(self.save_user_job_file)
        # 選擇核心
        self.buttonMainCore.clicked.connect(lambda: self.select_core_buttons('主要核心'))
        self.buttonSecondCore.clicked.connect(lambda: self.select_core_buttons('第二核心'))
        self.buttonThirdCore.clicked.connect(lambda: self.select_core_buttons('第三核心'))
        # 新增核心
        self.buttonAddCore.clicked.connect(self.add_core)
        # 篩選核心
        self.buttonFindPerfectCore.clicked.connect(self.find_perfect_cores)

    # 讀取職業JSON文件
    def read_job_data(self):
        with open('static/job.json', 'r', encoding='utf-8') as file:
            json_data = file.read()
        data = json.loads(json_data)
        return data
    
    # 尋找相對應的英文職業名稱
    def get_EN_job_name(self, CH_job_name):
        for item in self.data:
            if item.get('CH_job_name') == CH_job_name:
                return item.get('EN_job_name')
        return 'NO_SERCH_CH_JOB_NAME'
    
    # 當職業下拉列表變化時，更新職業名稱下拉列表
    def update_job_name(self):
        #所選下拉式選單文字
        selected_group = self.jobGroup.currentText()
        selected_job = self.job.currentText()

        # 過濾符合職業群、職業的職業名稱
        matching_groups = [job['CH_job_name'] for job in self.data if job['job_group'] == selected_group or selected_group == '全選']
        matching_jobs = [job['CH_job_name'] for job in self.data if job['job'] == selected_job or selected_job == '全選']
        matching_job_names = [job for job in matching_groups if job in matching_jobs]

        # 清空並填充職業名稱下拉列表
        self.jobName.clear()
        self.jobName.addItems(matching_job_names)

    # 選擇不同職業名稱，更新技能列表
    def update_skill_image(self):
        #所選下拉式選單文字
        selected_job_name = self.jobName.currentText()

        # 尋找相對應的英文職業名稱資料夾
        selected_EN_job_name = self.get_EN_job_name(selected_job_name)
        jobname_folder_path = "static/skill_icon/" + selected_EN_job_name

        #設定按鈕圖片
        for skill_index in range(1,16):
            skill_path = f"{jobname_folder_path}/{str(skill_index).zfill(2)}.png"
            button_name = "buttonSkill_" + str(skill_index)
            button = getattr(self, button_name) # 抓取同名稱的物件
            button.setEnabled(True)
            # 檢查圖片是否存在
            if os.path.exists(skill_path):
                icon = QIcon(skill_path)  # 如果存在，使用該圖片
                button.setIcon(icon)
                button.setIconSize(icon.actualSize(icon.availableSizes()[0])) # 設置圖標尺寸
            else:
                button.setIcon(QIcon()) # 否則使用空圖標
                button.setEnabled(False)

    # 設定完美核心按鈕的checked狀態
    def set_select_perfect_cores(self):
        for i, button in enumerate(self.button_skill_list):
            button.setChecked(self.select_perfect_cores[i])

    # 抓取完美核心按鈕的checked狀態
    def get_select_perfect_cores(self):
        for i, button in enumerate(self.button_skill_list):
            self.select_perfect_cores[i] = button.isChecked()

    # 關閉完美核心按鈕的checked
    def close_select_perfect_cores(self):
        for button in self.button_skill_list:
            button.setCheckable(False)

    # 開啟完美核心按鈕的checked
    def open_select_perfect_cores(self):
        for button in self.button_skill_list:
            button.setCheckable(True)

    # 重製選擇核心按鈕
    def reset_select_core_buttons(self):
        self.buttonMainCore.setIcon(QIcon())
        self.buttonMainCore.setText("主要")
        self.buttonSecondCore.setIcon(QIcon())
        self.buttonSecondCore.setText("第二")
        self.buttonThirdCore.setIcon(QIcon())
        self.buttonThirdCore.setText("第三")
        self.select_skills = [-1, -1, -1]

    # 設定篩選核心按鈕icon
    def set_select_core_buttons(self):
        for index in range(3):
            skill = self.select_skills[index]
            if skill != -1:
                temp_button = self.button_skill_list[skill]
                self.button_select_skill_list[index].setIcon(temp_button.icon())
                self.button_select_skill_list[index].setIconSize(temp_button.size())
                self.button_select_skill_list[index].setText("")

    # 點選篩選核心按鈕後設定完美核心group
    def select_core_buttons(self, button_text):
        self.get_select_perfect_cores()
        self.close_select_perfect_cores()
        self.selectPerfectCoresGroupBox.setTitle(f"選擇{button_text}")

        for index, button in enumerate(self.button_skill_list):
            # 斷開button之前的連接
            try:
                button.clicked.disconnect()
            except TypeError:
                pass  # 如果沒有連接就忽略這個錯誤
            
            button.clicked.connect(lambda checked, index=index, button_text=button_text: self.select_perfect_core(index, button_text))

    # 點選完美核心group設定篩選核心
    def select_perfect_core(self, perfect_core_button_ID, button_text):
        if perfect_core_button_ID in self.select_skills:
            self.labelSelectError.setText('核心不能一樣')
            return

        if button_text == '主要核心':
            self.select_skills[0] = perfect_core_button_ID
        elif button_text == '第二核心':
            self.select_skills[1] = perfect_core_button_ID
        elif button_text == '第三核心':
            self.select_skills[2] = perfect_core_button_ID

        self.set_select_core_buttons()

        for button in self.button_skill_list:
            # 斷開button之前的連接
            try:
                button.clicked.disconnect()
            except TypeError:
                pass  # 如果沒有連接就忽略這個錯誤

        self.open_select_perfect_cores()
        self.set_select_perfect_cores()
        self.selectPerfectCoresGroupBox.setTitle("完美核心")
        self.labelSelectError.setText('')

    # 新增核心到列表中
    def add_core(self):
        if -1 in self.select_skills:
            self.labelSelectError.setText('有未篩選核心')
            return
        
        if self.select_skills in self.cores:
            self.labelSelectError.setText('這顆核心重複了')
            return
        
        self.cores.append(self.select_skills)

        self.reset_select_core_buttons()
        self.set_cores_button()

    # 搜尋完美核心、顯示結果
    def find_perfect_cores(self):
        if not self.cores:
            self.labelSelectError.setText('核心列表是空的')
            return
        
        # 設 '1' 列出所有解, 設 '2' 列第一組合乎成本解
        if self.comboBoxSelectMode.currentText() == '第一組合乎成本完美核心':
            enumerate_mode = 2  
        elif self.comboBoxSelectMode.currentText() == '所有完美核心':
            enumerate_mode = 1
        selected_perfect_cores = [] # 完美核心
        cores = self.cores # 請在陣列s1中輸入您持有的核心，用來找四核六技，以','分隔
        core_count = len(cores)  # 核心總數量

        self.get_select_perfect_cores()
        for index, core in enumerate(self.select_perfect_cores):
            if core:
                selected_perfect_cores.append(index)

        if not selected_perfect_cores:
            self.labelSelectError.setText('請選擇完美核心')
            return
        
        self.buttonFindPerfectCore.setEnabled(False)
        self.buttonAddCore.setEnabled(False)
        self.labelSelectError.setText("正在尋找完美核心...")

        self.findThread = FindPerfectCores(cores, core_count, enumerate_mode, selected_perfect_cores)
        self.findThread.finished.connect(self.find_perfect_cores_finished)
        self.findThread.start()

    # 搜尋完後
    def find_perfect_cores_finished(self):
        self.labelSelectError.setText('')
        self.buttonFindPerfectCore.setEnabled(True)
        self.buttonAddCore.setEnabled(True)

        text = self.findThread.get_text()
        # 建立一副視窗顯示完美核心
        self.sub_window = QtWidgets.QWidget()
        self.ui = formPerfectCores.Ui_formPerfectCores()
        self.ui.setupUi(self.sub_window)
        self.ui.label.setText(text)
        self.sub_window.show()

    # 合成核心圖片
    def synthesis_img(self, icons):
        width = icons[0].width()
        height = icons[0].height()

        # 建立一个空的 QPixmap
        mergedPixmap = QPixmap(width, height)
        mergedPixmap.fill()

        # 使用 QPainter 合成图标
        painter = QPainter(mergedPixmap)

        # 主要技能區域
        triangle1 = QPolygonF([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(width // 2, height // 2),
            QtCore.QPoint(width, 0)
        ])

        # 第二技能區域
        triangle2 = QPolygonF([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(width // 2, height // 2),
            QtCore.QPoint(width // 2, height),
            QtCore.QPoint(0, height)
        ])

        # 第三技能區域
        triangle3 = QPolygonF([
            QtCore.QPoint(width, 0),
            QtCore.QPoint(width // 2, height // 2),
            QtCore.QPoint(width // 2, height),
            QtCore.QPoint(width, height)
        ])

        triangles = [triangle1, triangle2, triangle3]

        for index in range(0,3):
            path = QPainterPath()
            path.addPolygon(triangles[index])
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, icons[index])

        # 畫筆顏色灰色
        painter.setClipping(False)
        painter.setPen(QPen(QColor('gray'), 2))
        painter.drawLine(0, 0, width // 2, height // 2)
        painter.drawLine(width, 0, width // 2, height // 2)
        painter.drawLine(width // 2, height, width // 2, height // 2)

        # 結束畫布
        painter.end()

        return mergedPixmap
    
    # 清除核心列表所有物件
    def clear_cores_button(self):
        while self.horizontalLayout.count():
            item = self.horizontalLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    # 以cores設定所有核心button
    def set_cores_button(self):
        self.clear_cores_button()
        
        for skill_id, core in enumerate(self.cores):
            icons = []
            for index in core:
                temp_button = self.button_skill_list[index]
                icons.append(temp_button.icon().pixmap(temp_button.iconSize()))

            # 合成圖片
            icon = self.synthesis_img(icons)

            # 將資料變成button放到 擁有核心列表內
            button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button.setIcon(QIcon(icon))
            button.setFixedSize(61, 61)  # 設定按鈕大小
            button.setIconSize(button.size())
            button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # 設置固定大小
            button.clicked.connect(lambda checked, skill_id=skill_id: self.selected_cores_button(skill_id))
            self.horizontalLayout.addWidget(button)
    
    # 點選核心列表的核心       
    def selected_cores_button(self, skill_id):
        self.skill_id = skill_id
        self.select_skills = self.cores[self.skill_id]
        self.set_select_core_buttons()
        self.buttonAddCore.clicked.disconnect()
        self.buttonAddCore.clicked.connect(self.update_cores_skill)
        self.buttonAddCore.setText('修改')

    # 更新核心
    def update_cores_skill(self):
        self.cores[self.skill_id] = self.select_skills
        self.set_cores_button()
        self.reset_select_core_buttons()
        self.buttonAddCore.clicked.disconnect()
        self.buttonAddCore.clicked.connect(self.add_core)
        self.buttonAddCore.setText('新增')

    # 讀取使用者資料
    def load_user_job_file(self):
        # 打開選擇檔案的對話框
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇檔案", "", "JSON Files (*.json);;All Files (*)", options=options)

        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                json_data = file.read()
            user_data = json.loads(json_data)

            try:
                self.job.setCurrentText('全選')
                self.jobGroup.setCurrentText('全選')
                self.jobName.setCurrentText(user_data['jobName'])
                self.select_perfect_cores = user_data['select_perfect_cores']
                self.set_select_perfect_cores()
                self.cores = user_data['cores']
                self.set_cores_button()
            except:
                self.labelSelectError.setText('檔案錯誤')

    # 儲存使用者資料
    def save_user_job_file(self):
        self.get_select_perfect_cores()
        user_data = {
            'jobName':self.jobName.currentText(),
            'select_perfect_cores':self.select_perfect_cores,
            'cores':self.cores
        }
        # 設定檔案初始位置
        initialDir = os.path.dirname(os.path.abspath(__file__))
        # 預設檔案名稱
        defaultFileName = "job.json"
        # 儲存檔案的對話框
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "儲存檔案", os.path.join(initialDir, defaultFileName), "JSON Files (*.json);;All Files (*)", options=options)

        if fileName:
            if not fileName.lower().endswith('.json'):
                fileName += '.json'
            with open(fileName, 'w') as file:
                json.dump(user_data, file, indent=4)

    # 新增資料(測試用)
    def add_cores(self):
        import random
        selected_perfect_cores = [0,1,2,3,4,5,6,7,8]
        for _ in range(100):
            skills = []
            while len(skills) < 3:
                skill = random.randint(0,15)
                if skill in skills or skill not in selected_perfect_cores:
                    continue
                skills.append(skill)
            if skills in self.cores:
                continue
            self.cores.append(skills)

        self.set_cores_button()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())