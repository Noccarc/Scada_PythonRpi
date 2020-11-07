try:
    import os
    import sys
    import datetime
    import time
    import boto3
    import threading
    import serial
    import pymysql
    import RPi.GPIO as GPIO 
    from time import sleep    
    from datetime import date
    from xbee import ZigBee
    import numpy as np
    import urllib
    import binascii
    
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))

payload=0
sub=0   
pre_comp_cyle_var=0    #o
update_var=0        #m
row_cycle_var=0     #c
row_cycle_var1=0    #e
t=0
count=0  
count1=0
flag_count=0
p='"'
q='%'
bat="*"
r="#"
gpln="@"

flag=1
global x1,row
x1=datetime.datetime.now()
x1=x1.strftime("%Y-%m-%d")


ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0)
xbee=ZigBee(ser)
#dest_addr_long_1=['0x00','0x13','0xA2','0X00','0x41','0x04','0x35','0xC0']
#dest_addr_long_1= bytearray( int(x,16) for  x in dest_addr_long_1)

class MyDb(object):
    def __init__(self):
            self.conn=pymysql.connect(
                host='192.168.1.151',
                port=3306,
                user='pi',
                password='admin',
                db='nocca'
                )
            
            self.cursor=self.conn.cursor()
    def db_insert_table(self,Robot_No, Date, Table_Clean, Water_Saved, Operational_Hour, Auto_mode, Theft_mode, Manual_mode):
            query= """ INSERT INTO Robot_data (Robot_No, Date, Table_Clean, Water_Saved, Operational_Hour, Auto_mode, Theft_mode, Manual_mode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            data=(Robot_No, Date, Table_Clean, Water_Saved, Operational_Hour, Auto_mode, Theft_mode, Manual_mode)
            self.cursor.execute(query,data)
            self.conn.commit()   
    def update_data(self,Robot_No,Table_Clean, Water_Saved, Operational_Hour):
        query="""UPDATE Robot_data SET Table_Clean=%s,Water_Saved=%s, Operational_Hour=%s WHERE Robot_No=%s"""
        data=(Table_Clean, Water_Saved, Operational_Hour,Robot_No)
        self.cursor.execute(query,data)
        self.conn.commit()
        print("updated succusses fully")
    def update_auto_mode(self,Robot_No,Auto_mode):
        query="""UPDATE Robot_data SET Auto_mode=%s WHERE Robot_No=%s"""
        data=(Auto_mode,Robot_No)
        self.cursor.execute(query,data)
        self.conn.commit()
        #print("updated succusses fully")
    def update_theft_mode(self,Robot_No,Theft_mode):
        query="""UPDATE Robot_data SET Theft_mode=%s WHERE Robot_No=%s"""
        data=(Theft_mode,Robot_No)
        self.cursor.execute(query,data)
        self.conn.commit()
        #print("updated succusses fully")
    def update_manual_mode(self,Robot_No,Manual_mode):
        query="""UPDATE Robot_data SET Manual_mode=%s WHERE Robot_No=%s"""
        data=(Manual_mode,Robot_No)
        self.cursor.execute(query,data)
        self.conn.commit()
        #print("updated succusses fully") 
        
    def get(self):
        
        query="""SELECT * from Robot_data """
        #data=(Robot_No,Date)
        self.cursor.execute(query)
        global rows
        rows=self.cursor.fetchall()               
        #Robot_theft=row[6]
        #Robot_dir=row[7]
        #self.controll(Robot_id,Robot_Status)
        return rows

    def get_1(self):
       rows1=self.get()
       for i in rows1:
           Id=i[0]
           St=i[4]
           thef=i[5]
           man=i[6]
           Xbee_add=i[7]
           dest_addr_long_1=binascii.unhexlify(Xbee_add)
           
           #print(i[0],St[4])
          #print(self.onoff(2))
           if St!=3 or 4:
               #print(Id,St)
               if  St==1:
                   print(dest_addr_long_1)
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id)+":"+str(1)))
                   print("Robot_No is on =",Id)
                   self.update_auto_mode(Id,St+2)
               elif St==2:
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id) +":"+str(2)))
                   print("Robot_NO off=",Id)
                   self.update_auto_mode(Id,St+2)
           if thef!=5 or 6:
               #print(Id,St)
               if  thef==3:
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id)+":"+str(5)))
                   print("Robot_No is locked =",Id)
                   self.update_theft_mode(Id,thef+2)
               elif thef==4:
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id) +":"+str(6)))
                   print("Robot_NO is unlocked=",Id)
                   self.update_theft_mode(Id,thef+2)
           if man!=9 or 10:
               #print(Id,St)
               if  man==7:
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id)+":"+str(7)))
                   print("Robot_No running in left =",Id)
                   self.update_manual_mode(Id,man+2)
               elif man==8:
                   xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data=str(str(Id) +":"+str(8)))
                   print("Robot_NO in right=",Id)
                   self.update_manual_mode(Id,man+2)
                
            
            
        
    
    def xb_data_1(self,xbee_data):
            global q,bat,x1,count,flag_count
            
            xbee_data=xbee_data
            print(xbee_data)
            l=len(xbee_data)   # length of data
            if l<7:
                status=xbee_data.split(":")
                self.update_auto_mode(status[0],status[1])
                
            if l>8 and l<20:
                global row_cycle_var,pre_comp_cyle_var,row_cycle_var1,update_var,robot_no,cycle_data,batt_data
                flag_count=0
                row_cycle_var_1=row_cycle_var
                pre_comp_cyle_var_1=pre_comp_cyle_var
                row_cycle_var1_1=row_cycle_var1
                update_var_1=update_var
                
        
                #Db_d_cln_1=self.get(1,'2019-12-14')
  
                #print("Data base Cleancycle=",Db_d_cln_1[2])
                #stored_cln_value=Db_d_cln_1[2]
                robot_no,cycle_data,batt_data=self.xbee_data_split(xbee_data)
                
                robot_no=int(robot_no)
                cycle_data=int(cycle_data)
                batt_data=int(batt_data)
                oprh=count*18
                print(robot_no,cycle_data,batt_data,oprh)
                #print("cycle_clean-1=",cycle_data)
                #area_clean,pre_comp_cyle_var_1,row_cycle_var_1=self.calculate_cycle(cycle_data,stored_cln_value,row_cycle_var_1,row_cycle_var1_1,update_var_1,pre_comp_cyle_var_1)
                ## publishing the data to aws##############
                #print("area clean1=",area_clean)
                
                self.update_data(robot_no,cycle_data,batt_data,oprh)

                #if pre_comp_cyle_var_1<row_cycle_var_1:   
                   #pre_comp_cyle_var_1=row_cycle_var_1
                
                
    def calculate_cycle(self,cycle_data,stored_cln_value,row_cycle_var_1,row_cycle_var1_1,update_var_1,pre_comp_cyle_var_1):   
            row_cycle_var_1=row_cycle_var_1
            pre_comp_cyle_var_1=pre_comp_cyle_var_1
            update_var_1=update_var_1       
            row_cycle_var1_1=row_cycle_var1_1  
            #global area_clean
            stored_cln_value=stored_cln_value
            
            
            row_cycle_var_1=cycle_data    
            row_cycle_var1_1=cycle_data
            if  row_cycle_var_1==1 or pre_comp_cyle_var_1>(row_cycle_var_1+update_var_1): 
               update_var_1=0     
            row_cycle_var_1=update_var_1+row_cycle_var_1

            if pre_comp_cyle_var_1>row_cycle_var_1:   
               update_var_1=pre_comp_cyle_var_1      
               row_cycle_var_1=update_var_1+row_cycle_var_1
              
            if pre_comp_cyle_var_1==0 and stored_cln_value>row_cycle_var1_1: 
               update_var_1=stored_cln_value+1-row_cycle_var1_1
               row_cycle_var_1=update_var_1+row_cycle_var1_1

            area_clean=row_cycle_var_1   # this value can change plant to plan
            area_clean=round(area_clean,2)   # made decimal to 2 point
            print("calculate function areaclean=",area_clean)
            return area_clean,pre_comp_cyle_var_1,row_cycle_var_1
        
    
        

    def xbee_data_split(self,xbee_data):
            xb_data=xbee_data.split(':')
            robot_no=int(xb_data[0][xb_data[0].find(r)+len(r):xb_data[0].rfind(r)])
            cycle_data=int(xb_data[1][xb_data[1].find(q)+len(q):xb_data[1].rfind(q)])
            batt_data=xb_data[2][xb_data[2].find(bat)+len(bat):xb_data[2].rfind(bat)]
            
            return robot_no,cycle_data,batt_data

     

while True:
    global obj
    obj=MyDb()
    #bj.get()
    obj.get_1()
   # xbee.tx(dest_addr_long=dest_addr_long_1,frame_id='\x00',data='123:124')
    #time.sleep(1)
    def print_data(data):
            global count
            
            global xbee_data
            xb_addr =data['source_addr_long']
            xbee_data=data['rf_data']   #xbee data are comming here from robots
            xbee_data=xbee_data.decode()
            obj.xb_data_1(xbee_data)
            count=count+1
            #print(xbee_data)
            
               
    xbee=ZigBee(ser,callback=print_data) 
    xbee.halt()
