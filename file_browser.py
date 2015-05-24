import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *
main=None
abc=QApplication(sys.argv)
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
		#self.installEventFilter(self)
		

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
		
		main.clear(main.layout)
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
		#renameAction.triggered.connect(download)
		self.menu.addAction(Download)
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
            
    def update(self,folderpagelist,address):
    	self.centralWidget=QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout=QGridLayout()
        self.container=QWidget()
        self.scroll=QScrollArea()
        self.layout=QGridLayout()
    	
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
            	  
        	self.h=QVBoxLayout()
        	txtlabel=QLabel()
        	txtlabel.setText(icon.name)
        	self.h.addWidget(txtlabel)
       
        	self.layout.addItem(self.h,*position2)
        		

        	self.layout.addWidget(icon,*position)
        
        self.container.setLayout(self.layout)
        
        self.scroll.setWidget(self.container)
        self.mainLayout.addWidget(self.scroll)
        self.centralWidget.setLayout(self.mainLayout)    
        self.centralWidget.setMinimumSize(600,600)
        
        

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

w=page("/Home/")
#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'
folderpagelist={}
folderpagelist.update({"/Home/":w})

makebrowser("/home/dir/Pictures/final1.png",folderpagelist,w)
makebrowser("/home/dir/DC/final.png",folderpagelist,w)
makebrowser("/home/dir/DC/final.png",folderpagelist,w)
makebrowser("/home/dir/machaya/final2.png",folderpagelist,w)
makebrowser("/home/dir/DC++/final3.png",folderpagelist,w)
makebrowser("/home/dir/DC++/yisfskl.png",folderpagelist,w)

main=Main(folderpagelist,"/Home/")
main.update(folderpagelist,"/Home/")
main.show()
sys.exit(abc.exec_())
'''
for x,y in folderpagelist.items():
	print "yo"
	print x	
'''
#w.resize(500,500)
#w.setWindowTitle("Hello World")

#w.show()
