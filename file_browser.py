import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *
import pickle
main=None
abc=QApplication(sys.argv)
#stray list is to ensure that workfile.pkl is present to load.
stray_list={'address':None}

#saved list is where all cut-paste data will remain persistent.
try:
	saved_list=pickle.load(open('workfile.pkl','rb'))
except:
	pickle.dump(stray_list,open('workfile.pkl','wb'))
	saved_list=pickle.load(open('workfile.pkl','rb'))	
class clipboard:
	string=''
#This code is to get any new icons or directories created in cloud storage.
def process_list():
	for a,b in folderpagelist.items():
		for c in b.iconlist:
			if b.windowtitle+c.name not in saved_list.keys():
				saved_list.update({b.windowtitle+c.name:None})
				pickle.dump(saved_list,open('workfile.pkl','wb'))
#This function is to change the folderpagelist according to data saved 
#in saved_list.	
def process_folderpagelist():
	for a,b in saved_list.items():
		if b!=None:
			i=a.rfind("/")
			srcname=a[i+1:]
			srcdirname=a[:i+1]
			j=b.rfind("/")
			dstdirname=b[:j+1]			
			for k in folderpagelist[srcdirname].iconlist:
				if k.name==srcname:
					folderpagelist[dstdirname].iconlist.append(k)
					folderpagelist[srcdirname].iconlist.remove(k)
	
def yo(folderpagelist,address):
	main.clear(main.mainLayout)
	#main.mainLayout.removeWidget(main.backbutton)
	#main.mainLayout.removeWidget(main.scroll)
	main.update(folderpagelist,address)
	main.show()	
class page(QWidget):
	def __init__(self,add):
		super(page,self).__init__()
		self.windowtitle=add
		self.setWindowTitle(add)
		self.resize(500,500)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		self.iconlist=[]
		
	def paste(self):
		i=clipboard.string.rfind('/')
		name=(clipboard.string)[i+1:]
		rname=(clipboard.string)[:i+1]
		tmpicon=fileicon(self,name)
		self.iconlist.append(tmpicon)
		#yo to update the screen after pasting
		yo(folderpagelist,self.windowtitle)
		#dest=destination where file has to be pasted.
		dest=self.windowtitle+name
		#code to update saved list after pasting.
		saved_list[clipboard.string]=dest
		pickle.dump(saved_list,open('workfile.pkl','wb'))
		#code to remove icon from source
		for a in folderpagelist[rname].iconlist:
			if a.name==name:
				folderpagelist[rname].iconlist.remove(a)
				break

w=page("/Home/")

class icon(QLabel):
	def __init__(self,page,name,imgadd):#decide whether you want to have a variable or just a common address
		super(icon,self).__init__(page)#each icon is associated with a page
		self.icon2=QIcon()
		self.pic=QPixmap(imgadd)#to incude a pic pixmap
		self.icon2.addPixmap(self.pic,QIcon.Normal,QIcon.On)
		self.setPixmap(self.icon2.pixmap(128,QIcon.Normal,QIcon.On))#pix map has been assighned its image
		self.foldername=QLabel(page)#label for the name of folder
		self.address=QString(name)#just for the sake of naming
		self.foldername.setText(name)#
		self.name=name
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)#move text to appropriate height
		self.mousePressEvent = self.gotclickedevent
		self.foldername.mousePressEvent=self.gotclickedevent
		self.mouseDoubleClickEvent = self.gotclickedevent
		self.foldername.mouseDoubleClickEvent=self.gotclickedevent
		self.pageadd=page.windowtitle
		self.page=page
		#self.installEventFilter(self)
		self.h=QVBoxLayout()
		
		
		self.txtlabel=QLabel()
		self.txtlabel.setToolTip(name)

		#txtlabel.setFixedSize(130,10)
		#txtlabel.setStyleSheet("QWidget {background-color:blue}")
		if len(name)>15:
			name=name[:11]+"..."
		self.txtlabel.setText(name)
		self.txtlabel.setFixedSize(130,20)
		self.txtlabel.setAlignment(Qt.AlignCenter)
 		self.setAlignment(Qt.AlignCenter)
		
		'''
	def hiddenname():
		i=15
		label=QVBoxLayout()
		label2=QLabel()
		while ((len(self.name)-15-i)>0):
			tmp=self.name[i:i+14]
			
			label2.setText(tmp)
			label.addWidget(label2)
			i=i+15
		label2.setText(self.name[i:])
		label.addWidget(label2)
		return label
		'''
	# This function simply gives clipboard the source address.	
	def cut(self):
		src=self.page.windowtitle+self.name
		
		clipboard.string=src.strip()

		
		


		#self.connect(self.foldername, SIGNAL('clicked()'), self.gotclicked)
	def move(self,x,y):#overwriting the existing function
		super(icon,self).move(x,y)
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)

	def gotclickedevent(self,event):
		#self.emit(QtCore.SIGNAL('clicked()'))
		if event.type()==QEvent.MouseButtonPress:
			if event.button()==Qt.LeftButton:
				self.leftclickevent()
				print("just got left clicked")
				#callfunction for left click on folder
				#since left click function has nothing special work to do even  if it is called with double click it won't matter
				#STILL FIND A METHOD TO MAKE CLICK AND DOUBLECLICK ACTIONS SEPARATE
			elif event.button()==Qt.RightButton:
				print("just got right clicked")
				self.rightclickevent()
				#call function for right click on folder
		elif event.type()==QEvent.MouseButtonDblClick:
			self.doubleclickevent()
			print("just got double clicked")
	

	def leftclickevent(self):
		pass

	def rightclickevent(self):
		pass			
	def doubleclickevent(self):
		'''
		main.clear(main.layout)
		main.update(folderpagelist,self.pageadd+self.name+"/")
		
		main.show()	
		'''

	def show(self):
		super(foldericon,self).show()
		self.foldername.show()	

		
class foldericon(icon):
	def __init__(self,page,name):
		super(foldericon,self).__init__(page,name,'folder.png')
	def gotclickedevent(self,event):
		super(foldericon,self).gotclickedevent(event)
	def doubleclickevent(self):
		
		main.clear(main.mainLayout)
		#main.mainLayout.removeWidget(main.backbutton)
		#main.mainLayout.removeWidget(main.scroll)
		main.update(folderpagelist,self.pageadd+self.name+"/")
		

		main.show()	
	#define leftclickevent,rightclickevent,doubleclickevent

class fileicon(icon):
	def __init__(self,page,name):
		super(fileicon,self).__init__(page,name,'file.png')	
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		renameAction = QAction('Exit',self)
		Download = QAction('Download',self)
		Cut = QAction('Cut',self)
		#renameAction.triggered.connect(download)
		Cut.triggered.connect(self.cut)
		self.menu.addAction(Download)
		self.menu.addAction(Cut)
		self.menu.popup(QCursor.pos())

	#define leftclickevent,rightclickevent,doubleclickevent
def makebrowser(address,folderpagelist,currpage):
	num=address.count('/')
	if num==1:#its a file
		for i in currpage.iconlist:
			if i.name==address[1:]:
				return


		tempfileicon=fileicon(currpage,address[1:])#change here
		currpage.iconlist.append(tempfileicon)		
		return
	else:#its a folder
		add=address.strip()
		i=(add[1:]).find('/')
		name=add[1:i+1]
		print(name)
		remainingadd=add[i+1:]
		print(remainingadd)
		newpagename=currpage.windowtitle + name+'/'
		if newpagename not in folderpagelist.keys():
			temppage=page(newpagename)
			folderpagelist.update({newpagename:temppage})
			tempfoldicon=foldericon(currpage,name) #change here
			currpage.iconlist.append(tempfoldicon)
		makebrowser(remainingadd,folderpagelist,folderpagelist[newpagename])	
			
class Main(QMainWindow):
	

	def __init__(self,folderpagelist,address,parent = None):
			super(Main, self).__init__(parent)
			self.centralWidget=QWidget()
			self.setCentralWidget(self.centralWidget)

			self.mainLayout=QGridLayout()
			self.container=QWidget()
			self.scroll=QScrollArea()
			self.layout=QGridLayout()
			self.backicon=QIcon()
			a=QSize(90,90)
			self.backicon.addFile('back.png',a,QIcon.Normal,QIcon.On)
	def update(self,folderpagelist,address):
		tmplist={}
		for a,b in folderpagelist.items():
			tmplist.update({a:b})
		self.pageadd=address
		self.layout=QGridLayout()
		self.container=QWidget()
		self.scroll=QScrollArea()
		self.layout=QGridLayout()
		self.backbutton=QPushButton(self.backicon,"Back",self.centralWidget)
		self.backbutton.setFixedSize(60,24)
		self.backbutton.clicked.connect(self.lp)
		###
		folderpagelist[address].setLayout(self.layout)
		self.ad=address
		k=0
		j=0
		i=0
		self.positions=[]
		self.positions2=[]   
		while(i<len(folderpagelist[address].iconlist)):
			j=0
			while(j<4 and i<len(folderpagelist[address].iconlist )):
					
				self.positions=self.positions+[(k,j)]
				self.positions2=self.positions2+[(k+1,j)]
				j=j+1
				i=i+1
			k=k+1
			
			#pos1=QMouseEvent.pos()
			#m=QMouseEvent()
			
		for position,icon,position2 in zip(self.positions,folderpagelist[address].iconlist,self.positions2):
				
			'''
			h=QVBoxLayout()
			label=Newlabel()
			txtlabel=QLabel()
			txtlabel.setText("Documents")
			h.addWidget(txtlabel)
			label.position=position
			label.setPixmap(icon.pixmap(size,QIcon.Normal,state))
			QtCore.QObject.connect(label, QtCore.SIGNAL('clicked()'), label.lp)
			w.addWidget(label,*position)
			h.addStretch(1)
			w.addItem(h,*position)
			'''
			overall=QVBoxLayout()
			icon.h.addWidget(icon.txtlabel)	  
			overall.addWidget(icon)
			overall.addWidget(icon.txtlabel)

			#txtlabel.move(0,100)
			#self.h.addStretch(2)
	   
			#self.layout.addItem(self.h,*position2)

			#self.layout.addWidget(txtlabel)
			#icon.setFixedSize(130,20)	

			self.layout.addItem(overall,*position)

			
			
		self.container.setLayout(self.layout)
		
		self.scroll.setWidget(self.container)
		self.mainLayout.addWidget(self.backbutton)
		self.mainLayout.addWidget(self.scroll)
		self.centralWidget.setLayout(self.mainLayout)	
		#self.centralWidget.setMaximumSize(600,600)
		
	def lp(self):
		
		i=self.ad[:-1].rfind("/")
		yo(folderpagelist,self.ad[:i+1])
		#main.clear(main.layout)
		#main.update(folderpagelist,self.ad[:i+1])
		#main.show()
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		#renameAction = QAction('Exit',self)
		#Download = QAction('Download',self)
		paste = QAction('Paste',self)
		#renameAction.triggered.connect(download)
		paste.triggered.connect(folderpagelist[self.pageadd].paste)
		#self.menu.addAction(Download)
		self.menu.addAction(paste)
		self.menu.popup(QCursor.pos())
	def mousePressEvent(self,event):

		if event.type()==QEvent.MouseButtonPress:
			if event.button()==Qt.RightButton:
				self.contextMenuEvent

	def clear(self,layout):
		'''
		for i in reversed(range(self.layout.count())):
			self.layout.itemAt(i).widget().setParent(None)
		'''

		for i in reversed(range(layout.count())):
			item = layout.itemAt(i)

			if isinstance(item, QWidgetItem):

				item.widget().close()
			# or
			# item.widget().setParent(None)
			elif isinstance(item, QSpacerItem):
				pass
			# no need to do extra stuff
			else:

				self.clear(item.layout())

		# remove the item from layout
			layout.removeItem(item)		   
  
#class fileicon()


#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'
folderpagelist={}
folderpagelist.update({"/Home/":w})

makebrowser("/home/dir/Pictures/final1.png",folderpagelist,w)
makebrowser("/home/dir/DC/final.png",folderpagelist,w)
makebrowser("/home/dir/DC/final.png",folderpagelist,w)
makebrowser("/home/dir/machaya/final2.png",folderpagelist,w)
makebrowser("/home/dir/DC++dsafsdaasdfsagfdgdgsd/final3.png",folderpagelist,w)
makebrowser("/home/dir/DC++/yisfskl.png",folderpagelist,w)
makebrowser("/home/dir/DC2++/yisfskl.png",folderpagelist,w)
makebrowser("/home/dir/DC3++/yisfskl.png",folderpagelist,w)
makebrowser("/home/dir/yisfskl.png",folderpagelist,w)
process_list()
process_folderpagelist()

main=Main(folderpagelist,"/Home/")
main.update(folderpagelist,"/Home/")
main.show()
process_folderpagelist()
sys.exit(abc.exec_())
'''
for x,y in folderpagelist.items():
	print "yo"
	print x	
'''

#w.resize(500,500)
#w.setWindowTitle("Hello World")

#w.show()
