import os
import pprint
import pygame
import time
import math 

from pymycobot.mypalletizer import MyPalletizer
r0 = 0.0
r1 = 0.0
r2 = 0.0
r3 = 0.0

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        
        self.mc = None
        self.mc  = MyPalletizer("/dev/ttyAMA0" , 1000000)
        self.r0 = 0.0
        self.r1 = 0.0
        self.r2 = 0.0
        self.r3 = 0.0
        self.g_pos=0
        self.mc.send_radians([0, 0, 0 , 0] , 80)
        self.mc.set_gripper_value(self.g_pos, 70)
    
    def send_rd(self):
    	self.mc.send_radians([ self.r0 , self.r1, self.r2 , self.r3] , 70)
    	time.sleep(0.005)
    	
    def control_gripper(self):
        self.mc.set_gripper_value(self.g_pos, 100)
        time.sleep(0.005)
    
    def restriction_check(self):
        l0=0.13
        l1=0.13
        x0=l0*math.sin(self.r1)
        y0=l0*math.cos(self.r1)
        x1=x0+l1*math.cos(self.r1+self.r2)
        y1=y0-l1*math.sin(self.r2+self.r1)
        if y1>0.023 and y1<0.13:
            valid=True
        else:
            valid=False
        #print("COORDINATES",[x1,y1],"ANGLES",[self.r1,self.r2])
        return valid

    def robot(self):
        step_gripper=3
        max_step=0.3
        max_ang_0=2.5
        min_ang_0=-2.5
        max_ang_1=1.2
        min_ang_1=0
        max_ang_2=0.85
        min_ang_2=-0.85
        max_ang_3=2.5
        min_ang_3=-2.5
        r1_past=self.r1
        r2_past=self.r2
        if 0 in self.axis_data:
            #self.g_pos=255
            #print("HOLA",self.axis_data[0])
            step=self.axis_data[0]
            if step > max_step:
                step=max_step
            elif step<-max_step:
                step=-max_step
            self.r0 = self.r0-(0.05*step)
            if self.r0>max_ang_0:
                self.r0=max_ang_0
            elif self.r0<min_ang_0:
                self.r0=min_ang_0
        if 1 in self.axis_data:
            #self.g_pos=0
            #print("HOLA",self.axis_data[0])
            step=self.axis_data[1]
            if step > max_step:
                step=max_step
            elif step<-max_step:
                step=-max_step
            self.r1 = self.r1+(0.05*step)
            if self.r1>max_ang_1:
                self.r1=max_ang_1
            elif self.r1<min_ang_1:
                self.r1=min_ang_1
        if 4 in self.axis_data:
            #print("HOLA",self.axis_data[0])
            step=self.axis_data[4]
            if step > max_step:
                step=max_step
            elif step<-max_step:
                step=-max_step
            self.r2 = self.r2+(0.05*step)
            if self.r2>max_ang_2:
                self.r2=max_ang_2
            elif self.r2<min_ang_2:
                self.r2=min_ang_2
        if 3 in self.axis_data:
            #print("HOLA",self.axis_data[0])
            step=self.axis_data[3]
            if step > max_step:
                step=max_step
            elif step<-max_step:
                step=-max_step
            self.r3 = self.r3-(0.05*step)
            if self.r3>max_ang_3:
                self.r3=max_ang_3
            elif self.r3<min_ang_3:
                self.r3=min_ang_3
        if self.button_data[0]:
            self.g_pos=self.g_pos+step_gripper
            if self.g_pos>110:
                self.g_pos=110
            self.control_gripper()

        if self.button_data[1]:
            self.g_pos=self.g_pos-step_gripper
            if self.g_pos<0:
                self.g_pos=0
            self.control_gripper()
            
        #self.mc.send_angles([0,0,0,0],80)
        valid=self.restriction_check()
        if valid==False:
            self.r1=r1_past
            self.r2=r2_past
        self.send_rd()
        #self.control_gripper()
        #print("Angles",[self.r0,self.r1,self.r2,self.r3])
        #print("GRIPPER",self.g_pos)
        #print("X",self.button_data[0])
        #print("STATE",self.mc.is_gripper_moving())
    
    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            self.robot()
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                #self.r0 = self.r0-(0.1*self.axis_data[0])
                #self.send_rd()
                
                
                
                # In the current setup, I have the state simply printing out to the screen.
                
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    #main_loop=True
    #while main_loop==True:
    #    print("MAIN")
    #    ps4.robot()
    #ps4.robot()
    
