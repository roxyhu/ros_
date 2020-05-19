#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Libraries
import rospy
from std_msgs.msg import Int16
import time, atexit, os
import RPi.GPIO as GPIO

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#######################
def kill():
	os.system("kill -KILL " + str(os.getpid()))

#重置超音波接收
def resetUltraSoinc(echo_pin):
	resetPin = echo_pin

	GPIO.setup(resetPin, GPIO.OUT)
	time.sleep(0.00001)

	GPIO.output(resetPin, GPIO.LOW)
	time.sleep(0.00001)

	GPIO.setup(resetPin, GPIO.IN)
	time.sleep(0.00001)

	rospy.loginfo("***** Reset! *****")
	pass


def talker():
	#對應到launch
	rospy.init_node('UltraSonic_Talker_Node', anonymous = False)
	#初始化名為UltraSonic_Talker_Node的節點，anonymous引數在為True的時候會在原本節點名字的後面加一串隨機數，來保證可以同時開啟多個同樣的節點，如果為false的話就只能開一個
	rospy.on_shutdown(kill)
	rate = rospy.Rate(10)
	
	myTopic = rospy.get_param("~my_topic")			#去抓取launch檔中參數名為my_topic的值放入myTopic中
	trigger_pin = rospy.get_param("~GPIO_TRIGGER")	#去抓取launch檔中參數名為GPIO_TRIGGER的值放入trigger_pin中
	echo_pin = rospy.get_param("~GPIO_ECHO")		#去抓取launch檔中參數名為GPIO_ECHO的值放入echo_pin中
    
	#GPIO初始化
	GPIO.setup(trigger_pin, GPIO.OUT)
	GPIO.setup(echo_pin, GPIO.IN)

	#pub = rospy.Publisher('UltraSonic_Talker', Int16, queue_size = 1, tcp_nodelay = True)
	pub = rospy.Publisher(myTopic, Int16, queue_size = 10, tcp_nodelay = True)
	print 'Publisher Created'

	#超音波距離計算
	while not rospy.is_shutdown():
		isReseted = False
        # set Trigger to LOW
		GPIO.output(trigger_pin, GPIO.LOW)
		time.sleep(0.000005)

        # set Trigger after 5us to HIGH
		GPIO.output(trigger_pin, GPIO.HIGH)
        # set Trigger after 10us to LOW

		time.sleep(0.00001)
		GPIO.output(trigger_pin, GPIO.LOW)

		StartTime = time.time()
		StopTime = time.time()

        # save time of StartTime
		while (GPIO.input(echo_pin) == 0):
			StartTime = time.time()
			if (StartTime - StopTime > 0.5):
				resetUltraSoinc(echo_pin)
				isReseted = True
				break

			if (isReseted == True):
				continue

        # save time of StopTime
		while (GPIO.input(echo_pin) == 1):
			StopTime = time.time()
			if (StopTime - StartTime > 0.5):
				resetUltraSoinc(echo_pin)
				isReseted = True
				break

			if (isReseted == True):
				continue

		TimeElapsed = StopTime - StartTime
		distance = (TimeElapsed * 34300) / 2
		pub_str = "%s Distance is :%s" % (rospy.get_caller_id(), distance)
		#rospy.loginfo(pub_str)
		pub.publish(distance)

		rate.sleep()

if __name__ == '__main__':
	try:
		print 'Initialing'
		talker()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
