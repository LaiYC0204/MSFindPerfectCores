from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import json
import os

import MSFindPerfectCoresUI

"""
connect某物件做某動作連接到某function，function可以疊加
disconnect將某物件做某動作所有連接的function刪除
"""


class Main(QtWidgets.QMainWindow, MSFindPerfectCoresUI.Ui_MSFindPerfectCores):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 設定變數
        self.data = self.read_job_data()
        self.selectPerfectCores = [False] * 15
        # 技能按鈕
        self.button_skill_list = [
            self.buttonSkill_1, self.buttonSkill_2, self.buttonSkill_3,
            self.buttonSkill_4, self.buttonSkill_5, self.buttonSkill_6,
            self.buttonSkill_7, self.buttonSkill_8, self.buttonSkill_9,
            self.buttonSkill_10, self.buttonSkill_11, self.buttonSkill_12,
            self.buttonSkill_13, self.buttonSkill_14, self.buttonSkill_15
        ]

        # 初始化下拉式選單
        self.update_job_name()
        self.update_skill_image()

        # 當職業下拉列表變化時，更新職業名稱下拉列表
        self.jobGroup.currentIndexChanged.connect(self.update_job_name)
        self.job.currentIndexChanged.connect(self.update_job_name)
        # 當職業名稱下拉列表變化時，更新技能按鈕圖示
        self.jobName.currentIndexChanged.connect(self.update_skill_image)
        # 載入、儲存使用者資料
        self.buttonLoad.clicked.connect(self.update_select_perfect_cores)
        self.buttonSave.clicked.connect(self.set_select_perfect_cores)

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

    #選擇不同職業名稱，更新技能列表
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

            # 檢查圖片是否存在
            if os.path.exists(skill_path):
                icon = QIcon(skill_path)  # 如果存在，使用該圖片
                button.setIcon(icon)
                button.setIconSize(icon.actualSize(icon.availableSizes()[0])) # 設置圖標尺寸
            else:
                button.setIcon(QIcon()) # 否則使用空圖標

    def update_select_perfect_cores(self):
        for i, button in enumerate(self.button_skill_list):
            button.setChecked(self.selectPerfectCores[i])

    def set_select_perfect_cores(self):
        for i, button in enumerate(self.button_skill_list):
            self.selectPerfectCores[i] = button.isChecked()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())