import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
import argparse
import controller2
import os, sys
import time
import random




class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("GUI Audiometer")
        main_window.config(bg="#595959")
        
        ttk.Style().configure(".", font=("Helvetica", 16), justify=tk.RIGHT)
        
        self.notebook = ttk.Notebook(self)
        
        self.principal_frame = PrincipalFrame(self.notebook)
        self.notebook.add(self.principal_frame, text="Start")
        
        self.NewFrame = NewFrame2(self.notebook)
        self.notebook.add(self.NewFrame, text="Hearing_Test")
        
        self.notebook.pack(padx=5, pady=5, side="top", fill="both", expand=True )
        self. pack(side="top", fill="both", expand=True)
        




class PrincipalFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.imageL = tk.PhotoImage(file=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "images/ear_128.png"))
        self.label_image = tk.Label(self, image=self.imageL)
        self.label_image.place(x=320, y=0)
        
        self.label_patient_data = ttk.Label(self, text="Patient Data")
        self.label_patient_data.place(x=325, y=135)
        
        text_variable_name = StringVar()
        self.label_name = ttk.Label(self, text="First and last name")
        self.label_name.place(x=20, y=180)
        self.entry_name = ttk.Entry(self, textvariable=text_variable_name, font=('Helvetica', 16))
        self.entry_name.place(x=220, y=180)
        
        text_variable_name = StringVar()
        self.label_number = ttk.Label(self, text="Id number")
        self.label_number.place(x=20, y=230)
        self.entry_number = ttk.Entry(self, textvariable=text_variable_name, font=('Helvetica', 16))
        self.entry_number.place(x=125, y=230)
        
        text_variable_name = StringVar()
        self.label_age = ttk.Label(self, text="Age")
        self.label_age.place(x=480, y=230)
        self.entry_age = ttk.Entry(self, textvariable=text_variable_name, font=('Helvetica', 16))
        self.entry_age.place(x=540, y=230)
        
        ext_variable_name = StringVar()
        self.label_address = ttk.Label(self, text="Address")
        self.label_address.place(x=20, y=280)
        self.entry_address = ttk.Entry(self, textvariable=text_variable_name, font=('Helvetica', 16))
        self.entry_address.place(x=120, y=280)
        
        self.btnExit = ttk.Button(self, text="Exit", command=root.destroy, width=4)
        self.btnExit.place(x=120, y=330)
        
        
        
        
        
        
        


class NewFrame2(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ctrl = controller2.Controller()
        self._switch = "off"
        self._current_level = 0
        self._earside = 'right' 
        self._freq = 1000   
        self._dict_right = {1000:None, 1500:None, 2000:None, 3000:None, 4000:None, 6000:None, 8000:None, 750:None, 500:None, 250:None, 125:None}
        self._dict_left = {1000:None, 1500:None, 2000:None, 3000:None, 4000:None, 6000:None, 8000:None, 750:None, 500:None, 250:None, 125:None}
        self._dict_right_thresh = {1000:None, 1500:None, 2000:None, 3000:None, 4000:None, 6000:None, 8000:None, 750:None, 500:None, 250:None, 125:None}
        self._dict_left_thresh = {1000:None, 1500:None, 2000:None, 3000:None, 4000:None, 6000:None, 8000:None, 750:None, 500:None, 250:None, 125:None}
        self._famil_left = "Not Completed"
        self._famil_right = "Not Completed"
        self._thresh_right = "Not Completed"
        self._thresh_left = "Not Completed"
        self.click = True
        self._thresh_switch = "off"
        self._current_level_list = []
        self._prev = None
        self._this = None
        self._i = 0
        self._freq_switch = "off"
        
        
        
        self.rowconfigure(0, minsize=400, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, minsize=500, weight=1)
        self.columnconfigure(1, minsize=500, weight=1)
        
        self.fr_test = tk.Frame(self)
        self.fr_test.config(bg="#595959")
        self.fr_buttons = tk.Frame(self)
        self.fr_inst = tk.Frame(self)
        self.fr_inst.config(bg="light blue")
        self.fr_11 = tk.Frame(self)
        self.fr_11.config(bg="light blue")
        
        self.fr_buttons.rowconfigure(1, minsize=25, weight=1)
        self.fr_buttons.rowconfigure(2, minsize=25, weight=1)
        self.fr_buttons.rowconfigure(3, minsize=25, weight=1)
        
        self.label_fami = tk.Label(self.fr_buttons, 
                                  text="Familiarisation",
                                  fg="black",
                                  bg="light blue",
                                  width=20,
                                  height=3)
        
        self.btn_start = tk.Button(self.fr_buttons, text="Start Familiarisation", relief=tk.RAISED, borderwidth=10)
        self.btn_minus = tk.Button(self.fr_buttons, text="Decrease db", relief=tk.RAISED, borderwidth=10)
        self.btn_plus = tk.Button(self.fr_buttons, text="Increase db", relief=tk.RAISED, borderwidth=10)
        self.btn_confirm = tk.Button(self.fr_buttons, text="Confirm", relief=tk.RAISED, borderwidth=10)
        
        self.btn_start.bind("<Button-1>", self.handle_start_familiarisation)
        self.btn_minus.bind("<Button-1>", self.handle_minus)
        self.btn_plus.bind("<Button-1>", self.handle_plus)
        self.btn_confirm.bind("<Button-1>", self.handle_confirm)
        
        self.label_fami.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.btn_start.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.btn_minus.grid(row=2, column=0, sticky="ew", padx=5)
        self.btn_plus.grid(row=2, column=2, sticky="ew", padx=5)
        self.btn_confirm.grid(row=3, column=1, sticky="new", padx=5)
        
        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.fr_test.grid(row=0, column=1, sticky="nsew")
        self.fr_inst.grid(row=1, column=0, sticky="nsew")
        self.fr_11.grid(row=1, column=1, sticky="nsew")
        
        self.fr_inst.columnconfigure(1, minsize=150, weight=1)
        text_variable_name = StringVar()
        self.label_name = tk.Label(self.fr_inst, text="Instruction")
        self.label_name.grid(row=0, column=0, pady=3, padx=3)
        self._entry_name = tk.Entry(self.fr_inst, font=('Helvetica', 8))
        self._entry_name.insert("0", "Choose any earside in famialiarisation block to start")
        self._entry_name.grid(row=0, column=1, sticky="ew")
        
        self.label_thresh = tk.Label(self.fr_test,
                                     text="Threshold Testing", 
                                     fg= "black",
                                     bg= "light blue",
                                     width= 20,
                                     height= 3)
        
        self._label_tone_info = tk.Label(self.fr_test,
                                     text="No tone played for threshold testing", 
                                     fg= "black",
                                     bg= "light blue",
                                     width= 50,
                                     height= 3)
        
        self.fr_test.rowconfigure(1, minsize=25, weight=1)
        self.fr_test.rowconfigure(2, minsize=25, weight=1)
        self.fr_test.rowconfigure(3, minsize=25, weight=1)
        self.fr_test.columnconfigure(1, minsize=150, weight=1)
        
        self.btn_start_thresh = tk.Button(self.fr_test, text= "Start Threshold Testing", relief=tk.RAISED, borderwidth=10)
        self.btn_confirm_thresh = tk.Button(self.fr_test, text="Freq_confirm", relief=tk.RAISED, borderwidth=10)
        self.btn_input_thresh_yes = tk.Button(self.fr_test, text="Yes", relief=tk.RAISED, borderwidth=10)
        self.btn_input_thresh_no = tk.Button(self.fr_test, text="No", relief=tk.RAISED, borderwidth=10)
        
        
        self.label_thresh.grid(row=0, column=1, padx=5, pady=5)
        self.btn_start_thresh.grid(row=1, column=1, padx=5, pady=5)
        self.btn_confirm_thresh.grid(row=2, column=1, padx=15)
        self.btn_input_thresh_no.place(x=120, y=350)
        self.btn_input_thresh_yes.place(x=407, y=350)
        self._label_tone_info.place(x=120, y=300)
        
        
            
        
        self.earside_left = tk.Button(self.fr_buttons, text='Left Earside', bg="light green", width=10, relief=tk.RAISED, borderwidth=2)
        self.earside_left.place(x=5, y=50)
        
        self.earside_right = tk.Button(self.fr_buttons, text='Right Earside', bg="light green", width=10, relief=tk.RAISED, borderwidth=2)
        self.earside_right.place(x=115, y=50)
        
        self.btn_1 = tk.Button(self, text='1000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_1.place(x=0, y=20)
        
        self.btn_2 = tk.Button(self, text='1500', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_2.place(x=0, y=50)
        
        self.btn_3 = tk.Button(self, text='2000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_3.place(x=0, y=80)
        
        self.btn_4 = tk.Button(self, text='3000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_4.place(x=0, y=110)
        
        self.btn_5 = tk.Button(self, text='4000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_5.place(x=0, y=140)
        
        self.btn_6 = tk.Button(self, text='6000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_6.place(x=0, y=170)
        
        self.btn_7 = tk.Button(self, text='8000', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_7.place(x=0, y=200)
        
        self.btn_8 = tk.Button(self, text='750', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_8.place(x=0, y=230)
        
        self.btn_9 = tk.Button(self, text='500', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_9.place(x=0, y=260)
        
        self.btn_10 = tk.Button(self, text='250', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_10.place(x=0, y=290)
        
        self.btn_11 = tk.Button(self, text='125', bg="pink", width=4, relief=tk.RAISED, borderwidth=2)
        self.btn_11.place(x=0, y=320)
        
        self._label_freqchosen = tk.Label(self.fr_buttons, 
                                  text="Frequency Chosen = 1000 Hz",
                                  fg="black",
                                  bg="light blue",
                                  width=28,
                                  height=3)
        self._label_freqchosen.place(x=5, y=350)
        
        
        
        self.earside_left_thresh = tk.Button(self.fr_test, text='Left Earside', bg="light green", width=10, relief=tk.RAISED, borderwidth=2)
        self.earside_left_thresh.place(x=5, y=50)
        
        self.earside_right_thresh = tk.Button(self.fr_test, text='Right Earside', bg="light green", width=10, relief=tk.RAISED, borderwidth=2)
        self.earside_right_thresh.place(x=115, y=50)
        
        
        
        
        self.btn_1.bind("<Button-1>", self.handle_btn1)
        self.btn_2.bind("<Button-1>", self.handle_btn2)
        self.btn_3.bind("<Button-1>", self.handle_btn3)
        self.btn_4.bind("<Button-1>", self.handle_btn4)
        self.btn_5.bind("<Button-1>", self.handle_btn5)
        self.btn_6.bind("<Button-1>", self.handle_btn6)
        self.btn_7.bind("<Button-1>", self.handle_btn7)
        self.btn_8.bind("<Button-1>", self.handle_btn8)
        self.btn_9.bind("<Button-1>", self.handle_btn9)
        self.btn_10.bind("<Button-1>", self.handle_btn10)
        self.btn_11.bind("<Button-1>", self.handle_btn11)
        
        self.earside_left.bind("<Button-1>", self.handle_earside_left)
        self.earside_right.bind("<Button-1>", self.handle_earside_right)
        
        self.earside_left_thresh.bind("<Button-1>", self.handle_earside_left_thresh)
        self.earside_right_thresh.bind("<Button-1>", self.handle_earside_right_thresh)
        
        self.btn_start_thresh.bind("<Button-1>", self.handle_btn_start_thresh)
        self.btn_confirm_thresh.bind("<Button-1>", self.handle_btn_confirm_thresh)
        self.btn_input_thresh_yes.bind('<Button-1>',self.handle_btn_input_thresh_yes)
        self.btn_input_thresh_no.bind('<Button-1>',self.handle_btn_input_thresh_no)
        
        
        
    def handle_start_familiarisation(self, event):
        
        
        try:
            self.familiarisation()
            
        except KeyboardInterrupt:
                    sys.exit('\nInterrupted by user')
    
                    
    
    def familiarisation(self):
        if self._switch == "off":
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Choose a clearly audible loudness with the help of increase and decrease button")
            self._switch = "on"
            self._current_level = self.ctrl.audibletone2(
                                 self._freq,
                                 self.ctrl.config.beginning_fam_level,
                                 self._earside)
        
    
    def handle_minus(self, event):
        if self._switch == "on":
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click confirm once clearly audible")
            self._current_level -= 5
            self.ctrl.audibletone3(self._freq, self._current_level, self._earside)
        
    def handle_plus(self, event):
        if self._switch == "on":
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click confirm once clearly audible")
            self._current_level += 5
            self.ctrl.audibletone3(self._freq, self._current_level, self._earside)
        
    def handle_confirm(self, event):
        if self._earside == 'right':
            if self._switch == "on":
                self.ctrl.stopaudibletone()
                self._switch = "off"
                self._dict_right[self._freq] = self._current_level
                print("The earside is")
                print(self._earside)
                print("The familiarisation values are")
                print(self._dict_right)
                self._entry_name.delete(0, tk.END)
                all_done = "Yes"
                for keys in self._dict_right:
                    if self._dict_right[keys]== None:
                        all_done = "No"
                        break
                if all_done == "No":
                    self._entry_name.insert("0", "Start familiarisation of another frequency for any earside")
                elif all_done == "Yes":
                    self._entry_name.insert("0", "Famialirisation of all the frequency for right earside has been done")
                    self._famil_right = "Completed"
                
        else:
            if self._switch == "on":
                self.ctrl.stopaudibletone()
                self._switch = "off"
                self._dict_left[self._freq] = self._current_level
                print("The earside is")
                print(self._earside)
                print("The familiarisation values are")
                print(self._dict_left)
                self._entry_name.delete(0, tk.END)
                all_done = "Yes"
                for keys in self._dict_left:
                    if self._dict_left[keys]== None:
                        all_done = "No"
                        break
                if all_done == "No":
                    self._entry_name.insert("0", "Start familiarisation of another frequency for any earside")
                elif all_done == "Yes":
                    self._entry_name.insert("0", "Famialirisation of all the frequency for left earside has been done")
                    self._famil_left = "Completed"
                    
        if self._famil_right == "Completed" and self._famil_left == "Completed":
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Famialirisation completed. Click on Start Threshold Testing")
            
            

    
    
    
        
    def handle_btn1(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 1000
            self._label_freqchosen["text"] = "Frequency Chosen = 1000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn2(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 1500
            self._label_freqchosen["text"] = "Frequency Chosen = 1500 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn3(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 2000
            self._label_freqchosen["text"] = "Frequency Chosen = 2000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn4(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 3000
            self._label_freqchosen["text"] = "Frequency Chosen = 3000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn5(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 4000
            self._label_freqchosen["text"] = "Frequency Chosen = 4000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn6(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 6000
            self._label_freqchosen["text"] = "Frequency Chosen = 6000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
    
    def handle_btn7(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 8000
            self._label_freqchosen["text"] = "Frequency Chosen = 8000 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn8(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 750
            self._label_freqchosen["text"] = "Frequency Chosen = 750 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn9(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 500
            self._label_freqchosen["text"] = "Frequency Chosen = 500 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn10(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 250
            self._label_freqchosen["text"] = "Frequency Chosen = 250 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
    def handle_btn11(self, event):
        if self._switch == "off" and self._freq_switch == "off":
            self._freq = 125
            self._label_freqchosen["text"] = "Frequency Chosen = 125 Hz"
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Click on start familiarisation/Freq_confirm to start the test at this frequency")
        
        
    def handle_earside_left(self, event):
        if self._switch == "off":
            self._earside = 'left'
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Choose any frequency to start familiarisation at that frequency")
        
    def handle_earside_right(self, event):
        if self._switch == "off":
            self._earside = 'right'
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Choose any frequency to start familiarisation at that frequency")
        
    def handle_earside_left_thresh(self, event):
        if self._freq_switch == "off":
            self._earside = 'left'
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Choose a frequency and confirm to start threshold testing on that frequency")
           
        
    def handle_earside_right_thresh(self, event):
        if self._freq_switch == "off":
            self._earside = 'right'
            self._entry_name.delete(0, tk.END)
            self._entry_name.insert("0", "Choose a frequency and confirm to start threshold testing on that frequency")
            
        
        
    def handle_btn_start_thresh(self, event):
        self._entry_name.delete(0, tk.END)
        self._entry_name.insert("0", "Select earside to start threshold testing for that earside")
        self._freq = 1000
        self._label_freqchosen["text"] = "Frequency Chosen = 1000 Hz"
        
        
        
    def handle_btn_confirm_thresh(self, event):
        if self._earside == "right":
            if self._famil_right != "Completed":
                self._entry_name.delete(0, tk.END)
                self._entry_name.insert("0", "Famialirisation not completed for right earside. Exiting threshold testing")
                return
        elif self._earside == "left":
            if self._famil_left != "Completed":
                self._entry_name.delete(0, tk.END)
                self._entry_name.insert("0", "Famialirisation not completed for left earside. Exiting threshold testing")
                return
        self._entry_name.delete(0, tk.END)
        self._entry_name.insert("0", "You cannot change selected earside and frequency till this threshold testing is completed ")
        self._freq_switch = "on"
        self._thresh_switch = "on"
        self.threshold_testing(self._freq)
        
        
        
    def threshold_testing(self, freq):
        if self._earside == "right":
            self._current_level = self._dict_right[freq]
        else:
            self._current_level = self._dict_left[freq]
            
        self._label_tone_info["text"] = str(freq) + "Hz tone will be played"
        self._current_level_list = []
        self._current_level = self._current_level - self.ctrl.config.small_level_decrement
        self.clicktone(self._freq, self._current_level, self._earside)
        
    
    
    def handle_btn_input_thresh_yes(self, event):
        if self._thresh_switch == "on":
            self._prev = self._this
            self._this = "Yes"
            if self._prev == "No" and self._this == "Yes":
                self._i = self._i+1
                self._current_level_list.append(self._current_level)
                if self._i == 5:
                    if [k for k in self._current_level_list
                        if self._current_level_list.count(k) >= 3]:
                        print ([k for k in self._current_level_list if self._current_level_list.count(k) >= 3])
                        a = [k for k in self._current_level_list if self._current_level_list.count(k) >= 3][0]
                        self._prev = None
                        self._this = None
                        self._current_level_list = []
                        self._i= 0
                        self._entry_name.delete(0, tk.END)     
                        if self._earside == "right":
                            self._dict_right_thresh[self._freq] = a
                            print("The earside is")
                            print(self._earside)
                            print("The Threshold estimation values are")
                            print(self._dict_right_thresh)
                            self._thresh_switch = "off"
                            all_done = "Yes"
                            for keys in self._dict_right_thresh:
                                if self._dict_right_thresh[keys]== None:
                                    all_done = "No"
                                    break
                            if all_done == "No":
                                self._entry_name.insert("0", "Select different frequency and confirm to start its threshold testing")
                            elif all_done == "Yes":
                                self._entry_name.insert("0", "Threshold estimation of all the frequency for right earside has been done")
                                self._thresh_right = "Completed"
                        elif self._earside == "left":
                            self._dict_left_thresh[self._freq] = a
                            print("The earside is")
                            print(self._earside)
                            print("The Threshold estimation values are")
                            print(self._dict_left_thresh)
                            self._thresh_switch = "off"
                            all_done = "Yes"
                            for keys in self._dict_left_thresh:
                                if self._dict_left_thresh[keys]== None:
                                    all_done = "No"
                                    break
                            if all_done == "No":
                                self._entry_name.insert("0", "Select different frequency and confirm to start its threshold testing")
                            elif all_done == "Yes":
                                self._entry_name.insert("0", "Threshold estimation of all the frequency for left earside has been done")
                                self._thresh_left = "Completed"
                        if self._thresh_right == "Completed" and self._thresh_left == "Completed":
                            self._entry_name.delete(0, tk.END)
                            self._entry_name.insert("0", "Threshold Testing completed. Click on Save to save results")    
                        self._label_tone_info["text"] = str(self._freq) + "Hz tone threshold estimation is completed"
                        self._freq_switch = "off"
                        return
                        
                    else:
                        self._prev = None
                        self._this = None
                        self._current_level_list = []
                        self._i= 0
                        self._current_level = self._current_level + self.ctrl.config.small_level_decrement
                        self.clicktone(self._freq, self._current_level, self._earside)
                        return
                    
            self._current_level = self._current_level - self.ctrl.config.small_level_decrement
            self.clicktone(self._freq, self._current_level, self._earside)            
                        
                            
            return
    
    def handle_btn_input_thresh_no(self, event):
        if self._thresh_switch == "on":
            self._prev = self._this
            self._this = "No"
            self._current_level = self._current_level + self.ctrl.config.small_level_decrement
            self.clicktone(self._freq, self._current_level, self._earside)
            return
    
    def clicktone(self, freq, current_level_dBHL, earside):
        if self.ctrl.dBHL2dBFS(freq, current_level_dBHL) > 0:
            raise OverflowError
        self._label_tone_info["text"] = str(self._freq) + "tone is playing"
        self.ctrl._audio.start(freq, self.ctrl.dBHL2dBFS(freq, current_level_dBHL),
                          earside)
        #print("Audio started")
        time.sleep(self.ctrl.config.tone_duration)
        self.ctrl._audio.stop()
        self._label_tone_info["text"] = "Were you able to listen the tone? Click Yes Or No"
        self._entry_name.delete(0, tk.END)
        self._entry_name.insert("0", "Click button Yes or No once.The next tone will start as soon as you give response")
        
    
    
            
    
        
        
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry("1200x480")
    ThemedStyle(root).set_theme('black')
    
    app = Application(root)
    app.mainloop()
        
        
        

