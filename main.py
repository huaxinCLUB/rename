from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader

from PySide2.QtGui import QIcon
import os




class Rename:

	def __init__(self):
		# 从文件中加载UI定义

		# 从 UI 定义中动态 创建一个相应的窗口对象
		# 注意：里面的控件对象也成为窗口对象的属性了
		# 比如 self.ui.button , self.ui.textEdit
		self.ui = QUiLoader().load('UI/main.ui')
		self.ui.setWindowIcon(QIcon("images/logo.png"))

		#增加浏览按钮的槽
		self.ui.browse.clicked.connect(self.browse_files)

		#加载按钮的槽
		self.ui.load.clicked.connect(self.loading)
		
		#预览按钮的槽
		self.ui.preview.clicked.connect(self.handlePreview)
		#确认按钮的槽
		self.ui.confirm.clicked.connect(self.handleConfirm)
	
		


	#浏览按钮的槽函数
	def browse_files(self):
		filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
		self.ui.file_path.setText(filePath)
		#将音频文件名放到files列表里
		files = os.listdir(filePath)
		#print(files)
		#sorted(files,key= rule)
		files.sort()
		#print(files)
		#设置表格列数（根据文件个数）
		self.ui.tableWidget.setRowCount(len(files))
		#将文件名填入表格第一列
		row = 0
		for i in files:
			self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(i))
			row += 1
		
		#设置表格宽度自动缩放
		self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)





	#加载码号槽函数
	def loading(self):
		#获取文本框内用户输入的码号，
		text = self.ui.codes.toPlainText()
		#将获取到的text多行字符串，按行放入列表codes里
		codes = text.splitlines()
		#判断用户是否输入空行
		if "" in codes:
			QMessageBox.critical(self.ui,'错误','请不要输入空行！')
		#将码号写入表格第二列	
		row = 0
		for code in codes:
			self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(code))
			row += 1

	#预览槽函数
	def handlePreview(self):
		#获取前两列的值，并拼接成新文件名
		for i in range(self.ui.tableWidget.rowCount()):
			newName = self.ui.tableWidget.item(i,0).text()[:-4] + "=" + self.ui.tableWidget.item(i,1).text() + ".mp3"
			self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(newName))

		


	def handleConfirm(self):
		for i in range(self.ui.tableWidget.rowCount()):
			file_path = self.ui.file_path.text()
			oldName = self.ui.tableWidget.item(i,0).text()
			newName = self.ui.tableWidget.item(i,2).text()
			try:
				os.rename(os.path.join(file_path,oldName),os.path.join(file_path,newName))

			except FileNotFoundError  as e:
				QMessageBox.critical(self.ui,'错误','未发现音频文件，请重启软件后重试')

		QMessageBox.information(self.ui,'重命名成功','请到音频文件夹下查看')


app = QApplication([])
rename = Rename()
rename.ui.show()
app.exec_()