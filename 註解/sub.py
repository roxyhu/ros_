#!/usr/bin/env python

# Libraries
import rospy
import time
from std_msgs.msg import Int16
import RPi.GPIO as GPIO
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

# 初始化
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

#設定四顆馬達分別名為myMotor1,2,3,4
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
myMotor3 = mh.getMotor(3)
myMotor4 = mh.getMotor(4)
#################################################
	
class listener(object):
	
	def __init__(self):  
		#對應至launch
		rospy.init_node('UltraSonic_Listener_Node', anonymous = False) 		
		#初始化名為UltraSonic_Listener_Node的節點，anonymous引數在為True的時候會在原本節點名字的後面加一串隨機數，來保證可以同時開啟多個同樣的節點，如果為false的話就只能開一個
		rospy.Subscriber('UltraSonic_Talker_First', Int16, self.callback1)	#訂閱launch檔中名為UltraSonic_Talker_First的節點 資料型別：INT16 放入定義名為callback1功能
		rospy.Subscriber('UltraSonic_Talker_Second', Int16, self.callback2)	#訂閱launch檔中名為UltraSonic_Talker_Second的節點 資料型別：INT16 放入定義名為callback2功能
		rospy.Subscriber('UltraSonic_Talker_Third', Int16, self.callback3)	#訂閱launch檔中名為UltraSonic_Talker_Third的節點 資料型別：INT16 放入定義名為callback3功能
		self.distance1= 0						#初始化變數 distance1 = 0
		self.distance2= 0						#初始化變數 distance2 = 0 
		self.distance3= 0						#初始化變數 distance3 = 0 
		print 'Subscriber Created'				#印出'Subscriber Created'
	
	#*車體前方超音波* 
	def callback1(self, data):					#第一顆超音波感測器副程式名為"callback1" 
		self.distance1 = data.data				#讀取第一顆超音波的data數值放入名為"distance1"變數中
		rospy.loginfo("distance1")				#印出文字"distance1"
		rospy.loginfo(self.distance1)			#印出distance1中的數值(第一顆超音波讀取到的數值)

	#*車體右側前方超音波*
	def callback2(self, data):					#第二顆超音波感測器副程式名為"callback2" 
		self.distance2 = data.data				#讀取第二顆超音波的data數值放入名為"distance2"變數中
		rospy.loginfo("distance2")				#印出文字"distance2"
		rospy.loginfo(self.distance2)			#印出distance2中的數值(第二顆超音波讀取到的數值)

	#*車體右側中間超音波*
	def callback3(self, data):					#第三顆超音波感測器副程式名為"callback3" 
		self.distance3 = data.data				#讀取第三顆超音波的data數值放入名為"distance3"變數中
		rospy.loginfo("distance3")				#印出文字"distance3"
		rospy.loginfo(self.distance3)			#印出distance3中的數值(第三顆超音波讀取到的數值)
		self.action()							#執行action()副程式
	
	#*判斷車子姿態副程式*
	def action(self):							#action()副程式
		if self.distance1 >= 10 and self.distance2 >= 8 and self.distance3 >= 8:
			#當車頭與前方牆面距離大於等於10公分 且 車頭右側與右側牆面距離大於等於8公分 且 車子右側中間位置與右側牆面距離大於等於8公分 時，執行下面動作
			turnright()							#右轉
			print("1")							#印出狀態"1"
		elif self.distance1 >= 10 and self.distance1 < 50 and  self.distance2 >= 8 and self.distance3 < 8:
			#當車頭與前方牆面距離介於10至49公分 且 車頭右側與右側牆面距離大於等於8公分 且 車子右側中間位置與右側牆面距離小於8公分 時，執行下面動作
			turnright()							#右轉
			print("2")							#印出狀態"2"
		elif self.distance1 >= 10 and self.distance2 < 8 and self.distance3 < 8:
			#當車頭與前方牆面距離大於等於10公分 且 車頭右側與右側牆面距離小於8公分 且 車子右側中間位置與右側牆面距離小於8公分 時，執行下面動作
			turnleft()							#左轉
			print("3")							#印出狀態"3"
		elif self.distance1 >= 10 and self.distance2 < 8 and self.distance3 >= 8:
			#當車頭與前方牆面距離大於等於10公分 且 車頭右側與右側牆面距離小於8公分 且 車子右側中間位置與右側牆面距離大於等於8公分 時，執行下面動作
			turnleft()							#左轉
			print("4")							#印出狀態"4"
		elif self.distance1 >= 50 and self.distance2 >= 8 and self.distance3 < 8:
			#當車頭與前方牆面距離大於等於50公分 且 車頭右側與右側牆面距離大於等於8公分 且 車子右側中間位置與右側牆面距離小於8公分 時，執行下面動作
			forward()							#直走
			print("4.5")						#印出狀態"4.5"
		elif self.distance1 < 10 and self.distance2 >= 8 and self.distance3 < 8:
			#當車頭與前方牆面距離小於10公分 且 車頭右側與右側牆面距離大於等於8公分 且 車子右側中間位置與右側牆面距離小於8公分 時，執行下面動作
			turnleft()							#左轉
			print("5")							#印出狀態"5"
		elif self.distance1 < 10 and self.distance2 < 8 and self.distance3 >= 8:
			#當車頭與前方牆面距離小於10公分 且 車頭右側與右側牆面距離小於8公分 且 車子右側中間位置與右側牆面距離大於等於8公分 時，執行下面動作
			turnleft()							#左轉
			print("6")							#印出狀態"6"
		elif self.distance1 < 10 and self.distance2 >= 8 and self.distance3 >= 8:
			#當車頭與前方牆面距離小於10公分 且 車頭右側與右側牆面距離大於等於8公分 且 車子右側中間位置與右側牆面距離大於等於8公分 時，執行下面動作
			backward()							#倒退
			time.sleep(0.3)						#0.3秒
			turnleft()							#左轉
			time.sleep(1.8)						#1.8秒
			forward()							#直走
			time.sleep(0.1)						#0.1秒
			print("7")							#印出狀態"7"
		elif self.distance1 < 10 and self.distance2 < 8 and self.distance3 < 8:
			#當車頭與前方牆面距離小於10公分 且 車頭右側與右側牆面距離小於8公分 且 車子右側中間位置與右側牆面距離小於8公分 時，執行下面動作
			backward()							#倒退
			time.sleep(0.3)						#0.3秒
			turnleft()							#左轉
			time.sleep(1.8)						#1.8秒
			forward()							#前進
			time.sleep(0.1)						#0.1秒
			print("8")							#印出狀態"8"
	
		else:									#否則：上述都未成立
			print("000000")						#印出狀態"000000"

#*左轉副程式*
def turnleft():
	myMotor1.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor2.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor3.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor4.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor1.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor2.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor3.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor4.setSpeed(70)						#馬達轉速設定PWM:70

#*右轉副程式*
def turnright():
	myMotor1.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor2.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor3.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor4.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor1.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor2.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor3.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor4.setSpeed(0)						#馬達轉速設定PWM:0

#*直走副程式*
def forward():
	myMotor1.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor2.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor3.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor4.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor1.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor2.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor3.setSpeed(70)						#馬達轉速設定PWM:70
	myMotor4.setSpeed(70)						#馬達轉速設定PWM:70

#*停車副程式*
def stop():
	myMotor1.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor2.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor3.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor4.run(Raspi_MotorHAT.FORWARD);		#馬達正轉
	myMotor1.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor2.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor3.setSpeed(0)						#馬達轉速設定PWM:0
	myMotor4.setSpeed(0)						#馬達轉速設定PWM:0

#*倒退副程式*
def backward():	
	myMotor1.run(Raspi_MotorHAT.BACKWARD);		#馬達反轉
	myMotor2.run(Raspi_MotorHAT.BACKWARD);		#馬達反轉
	myMotor3.run(Raspi_MotorHAT.BACKWARD);		#馬達反轉
	myMotor4.run(Raspi_MotorHAT.BACKWARD);		#馬達反轉
	myMotor1.setSpeed(75)						#馬達轉速設定PWM:75
	myMotor2.setSpeed(75)						#馬達轉速設定PWM:75
	myMotor3.setSpeed(75)						#馬達轉速設定PWM:75
	myMotor4.setSpeed(75)						#馬達轉速設定PWM:75

if __name__ == '__main__':
	try:
		print 'Initialing'						#印出"Initialing"				
		start = listener()						#執行listener()
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass
