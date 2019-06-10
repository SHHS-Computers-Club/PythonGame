from tkinter import *
from random import randint
from datetime import datetime

class Game:
    def __init__(self, master):
        root.title('Game')
        root.resizable(width=False, height=False)
        frame = Frame(master=root)
        frame.pack_propagate(0)
        frame.grid()
        self.grid = [[],[],[],[],[],[],[],[],[],[]]
        self.bgrid = [[],[],[],[],[],[],[],[],[],[]]
        self.reveal_grid = [[],[],[],[],[],[],[],[],[],[]]
        self.reveal_grid2 = [[],[],[],[],[],[],[],[],[],[]]
        self.worker_grid = [[],[],[],[],[],[],[],[],[],[]]
        self.gold = 0
        self.pop = 1
        self.place_pop = 0
        self.food = 0
        self.food_list = [[],[],[]]
        self.wood = 0
        self.iron = 0
        self.placing = False
        self.removing = False
        self.startxy = [1,1]
        self.turn = 1
        self.a_reset = True
        self.show_conv = False
                
        for row in self.grid:
            for i in range(10):
                rs = randint(1,3)
                if rs == 1:
                    rs = 'xFood'
                    qt = randint(1,4)
                    if qt == 4:
                        qt = randint(2,3)
                elif rs == 2:
                    rs = 'xWood'
                    qt = randint(1,3)
                else:
                    rs = 'xIron'
                    qt = randint(1,2)
                
                row.append(str(qt)+rs)
        
        self.turn_lbl = Label(frame,text='Turn: '+str(self.turn))
        self.turn_lbl.grid(row=1,column=1)
        self.gold_lbl = Label(frame,text='Gold: '+str(self.gold)+' (0)')
        self.gold_lbl.grid(row=1,column=2,columnspan=2,sticky='W')
        self.gold_c = 0
        self.pop_lbl = Label(frame,text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
        self.pop_lbl.grid(row=1,column=3,columnspan=2)
        self.food_lbl = Label(frame,text='Food: '+str(self.food)+' ('+str(sum(self.food_list[-1]))+')')
        self.food_lbl.grid(row=1,column=5,columnspan=2)
        self.wood_lbl = Label(frame,text='Wood: '+str(self.wood)+' (0)')
        self.wood_lbl.grid(row=1,column=7,columnspan=2)
        self.wood_c = 0
        self.iron_lbl = Label(frame,text='Iron: '+str(self.iron)+' (0)')
        self.iron_lbl.grid(row=1,column=9,columnspan=2)
        self.iron_c = 0
        self.load_lbl = Label(frame,text='',fg='red')

        self.it = 1
        for row in range(10):
            self.ct = 1
            for col in range(10):
                if self.is_touching([[1,1]],[self.it-1,self.ct-1]):
                    self.bgrid[row].append(Button(frame, text=self.grid[row][col], width=6, height=3))
                    self.reveal_grid[row].append(True)
                    self.reveal_grid2[row].append(True)
                else:
                    self.bgrid[row].append(Button(frame, text='',width=6, height=3))
                    self.reveal_grid[row].append(False)
                    self.reveal_grid2[row].append(False)
                self.worker_grid[row].append(False)
                self.bgrid[row][col].grid(row=self.it+1,column=self.ct,sticky='NSEW')
                self.bgrid[row][col].bind("<Button-1>",self.get_rsc)
                self.ct += 1
            self.it += 1
        self.placer_btn = Button(frame, text='Place worker', width=14, height=3,command=self.place)
        self.placer_btn.grid(column=1,row=12,columnspan=2)
        self.remove_btn = Button(frame, text='Remove worker', width=14, height=3,command=self.remove)
        self.remove_btn.grid(column=3,row=12,columnspan=2)
        self.end_btn = Button(frame, text='End Turn', width=14, height=3, command=self.end)
        self.end_btn.grid(column=5,row=12,columnspan=2)
        self.save_btn = Button(frame, text='Save', width=14, height=3, command=self.save)
        self.save_btn.grid(row=12, column=7, columnspan=2)
        self.load_btn = Button(frame, text='Load', width=14, height=3, command=self.load)
        self.load_btn.grid(row=12, column=9, columnspan=2)
        self.bgcolor = self.end_btn.cget('background')

        self.blank_lbl = StringVar(frame)
        self.blank_lbl.set("")
        self.trade_lbl = StringVar(frame)
        self.trade_lbl.set("Trade Resource")
        self.trade_rsc = OptionMenu(frame, self.trade_lbl, "Trade: Food","Trade: Wood","Trade: Iron","Trade: Gold")
        self.trade_rsc.grid(row=2,column=11,columnspan=2,sticky='NEW')
        self.trade_qty_lbl = Label(frame,text='Qty:')
        self.trade_qty_lbl.grid(row=2,column=11,sticky='WS')
        self.trade_qty = Entry(frame, width=5)
        self.trade_qty.grid(row=2,column=11, sticky='S')
        self.receive_lbl = StringVar(frame)
        self.receive_lbl.set("Receive Resource")
        self.receive_rsc = OptionMenu(frame, self.receive_lbl, "Receive: Food","Receive: Wood","Receive: Iron","Receive: Gold")
        self.receive_rsc.grid(row=3,column=11,columnspan=2,sticky='NEW')
        self.receive_qty_lbl = Label(frame,text='Min:')
        self.receive_qty_lbl.grid(row=3,column=11,sticky='WS')
        self.receive_qty = Entry(frame, width=5)
        self.receive_qty.grid(row=3,column=11, sticky='S')
        self.trade_reset = Button(frame,text='Auto-Reset: ON', width=12, command=self.autoreset)
        self.trade_reset.grid(row=4,column=11,sticky='NWS')
        self.t_set = Button(frame,text='Reset', width=6, command=self.tradereset)
        self.t_set.grid(row=4,column=12, sticky='NS')
        self.show_calc = Button(frame,text='Show conversion rates', command=self.showcalc)
        self.show_calc.grid(row=5,column=11,columnspan=2,sticky='NEW')
        self.refresh_calc = Button(frame,text='Refresh',command=self.refreshcalc)
        self.conv_to_food_lbl = Button(frame,text='',command=lambda:self.autoreceive('food'))
        self.conv_to_wood_lbl = Button(frame,text='',command=lambda:self.autoreceive('wood'))
        self.conv_to_iron_lbl = Button(frame,text='',command=lambda:self.autoreceive('iron'))
        self.conv_to_gold_lbl = Button(frame,text='',command=lambda:self.autoreceive('gold'))
        self.conv_error_lbl = Label(frame,text='')

    def save(self):
        self.savescreen = Tk()
        self.savescreen.title('Save')
        name_lbl = Label(self.savescreen,text='File name:',width=10)
        name_lbl.grid(row=1,column=1)
        ctime = str(datetime.now())
        for i in range(len(ctime)):
            if ctime[i] == '.':
                ctime = ctime[:i]
                break
            if ctime[i] == ' ':
                ctime = ctime[:i]+'~'+ctime[i+1:]
            elif ctime[i] == ':':
                ctime = ctime[:i]+'-'+ctime[i+1:]
        self.name_enter = Entry(self.savescreen,width=20)
        self.name_enter.grid(row=1,column=2)
        self.name_enter.insert(0,ctime)
        save_cancel = Button(self.savescreen,text='Cancel',command=lambda:self.scrdestroy(self.savescreen))
        save_cancel.grid(row=2,column=1,sticky='NEWS')
        save_ok = Button(self.savescreen,text='Save',command=self.confsave)
        save_ok.grid(row=2,column=2,sticky='NEWS')

    def load(self):
        self.loadscreen = Tk()
        self.loadscreen.title('Load')
        name_lbl = Label(self.loadscreen,text='File name:',width=10)
        name_lbl.grid(row=1,column=1)
        self.name_enter = Entry(self.loadscreen,width=20)
        self.name_enter.grid(row=1,column=2)
        load_cancel = Button(self.loadscreen,text='Cancel',command=lambda:self.scrdestroy(self.loadscreen))
        load_cancel.grid(row=2,column=1,sticky='SEWN')
        load_ok = Button(self.loadscreen,text='Load',command=self.confload)
        load_ok.grid(row=2,column=2,sticky='SEWN')
        
    def confsave(self):
        bad_char = False
        for i in self.name_enter.get():
            for m in '.<>:"/\\|?*':
                if i == m:
                    bad_char = True
        try:
            f = open(self.name_enter.get()+'.py')
            filetext = f.read()
            f.close()
            f = True
        except:
            f = False
        if f and self.name_enter.get().lower() != 'game.py':
            self.confirm = Tk()
            self.confirm.title('')
            confirm_txt = Label(self.confirm,text='A file with this name already exists.\nAre you sure you want to overwrite it?')
            confirm_txt.grid(row=1,column=1,columnspan=2,rowspan=2)
            confirm_ccl = Button(self.confirm,text='No',command=lambda:self.scrdestroy(self.confirm))
            confirm_ccl.grid(row=3,column=1,sticky='NEWS')
            confirm_yes = Button(self.confirm,text='Yes',command=self.realsave)
            confirm_yes.grid(row=3,column=2,sticky='NEWS')
        elif self.name_enter.get().lower() == 'game.py' or bad_char:
            self.invalidfile()
        else:
            self.realsave()

    def confload(self):
        try:
            load = __import__(self.name_enter.get())
            for row in range(10):
                for col in range(10):
                    self.grid[row][col] = load.grid[row][col]
                    self.worker_grid[row][col] = load.worker_grid[row][col]
                    self.reveal_grid[row][col] = load.reveal_grid[row][col]
                    self.reveal_grid2[row][col] = load.reveal_grid2[row][col]
            self.pop = int(load.pop)
            self.place_pop = int(load.place_pop)
            self.gold = int(load.gold)
            self.gold_c = int(load.gold_c)
            self.food = int(load.food)
            for m in range(len(load.food_list)):
                for n in range(len(load.food_list[m])):
                    self.food_list[m][n] = load.food_list[m][n]
            self.wood = int(load.wood)
            self.wood_c = int(load.wood_c)
            self.iron = int(load.iron)
            self.iron_c = int(load.iron_c)
            self.turn = int(load.turn)
            if load.a_reset:
                self.a_reset = True
            else:
                self.a_reset = False
            if load.show_conv:
                self.show_conv = True
            else:
                self.show_conv = False
            self.trade_lbl.set(load.trade_lbl)
            self.trade_qty.delete(0,'end')
            self.trade_qty.insert(0,load.trade_qty)
            self.receive_lbl.set(load.receive_lbl)
            self.receive_qty.delete(0,'end')
            self.receive_qty.insert(0,load.receive_qty)
            self.placing = False
            self.removing = False
            if self.a_reset:
                self.trade_lbl.set("Trade Resource")
                self.receive_lbl.set("Receive Resource")
                self.trade_qty.delete(0,'end')
                self.receive_qty.delete(0,'end')

            self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
            self.gold_lbl.configure(text='Gold: '+str(self.gold)+' ('+str(self.gold-self.gold_c)+')')
            self.food_lbl.configure(text='Food: '+str(self.food)+' ('+str(sum(self.food_list[-1]))+')')
            self.wood_lbl.configure(text='Wood: '+str(self.wood)+' ('+str(self.wood-self.wood_c)+')')
            self.iron_lbl.configure(text='Iron: '+str(self.iron)+' ('+str(self.iron-self.iron_c)+')')
            self.turn_lbl.configure(text='Turn: '+str(self.turn))
            
            for row in range(10):
                for col in range(10):
                    if load.reveal_grid[row][col]:
                        self.bgrid[row][col].configure(text=self.grid[row][col])
                    else:
                        self.bgrid[row][col].configure(text='')
                    if load.worker_grid[row][col]:
                        self.bgrid[row][col].configure(bg='lightgray')
                    else:
                        self.bgrid[row][col].configure(bg=self.bgcolor)
        except:
            self.invalidfile()
        self.load_lbl.configure(text='Loaded File!')
        self.load_lbl.grid(row=1,column=11,columnspan=2)
            
    def scrdestroy(self,screen):
        try:
            screen.destroy()
            screen = False
        except:
            pass
        
    def invalidfile(self):
        self.confirm = Tk()
        self.confirm.title('')
        L_margin = Label(self.confirm,text='', width=2)
        L_margin.grid(row=1,column=1)
        R_margin = Label(self.confirm,text='',width=2)
        R_margin.grid(row=1,column=3)
        error_txt = Label(self.confirm,text='Invalid file name!')
        error_txt.grid(row=1,column=2)
        ok_btn = Button(self.confirm,text='OK',command=lambda:self.scrdestroy(self.confirm))
        ok_btn.grid(row=2,column=2,sticky='NEWS')
        
    def realsave(self):
        file = open(self.name_enter.get()+'.py','w')
        file.write('grid = '+str(self.grid)+'\n')
        file.write('worker_grid = '+str(self.worker_grid)+'\n')
        file.write('reveal_grid = '+str(self.reveal_grid)+'\n')
        file.write('reveal_grid2 = '+str(self.reveal_grid2)+'\n')
        file.write('pop = '+str(self.pop)+'\n')
        file.write('place_pop = '+str(self.place_pop)+'\n')
        file.write('gold = '+str(self.gold)+'\n')
        file.write('gold_c = '+str(self.gold_c)+'\n')
        file.write('food = '+str(self.food)+'\n')
        file.write('food_list = '+str(self.food_list)+'\n')
        file.write('wood = '+str(self.wood)+'\n')
        file.write('wood_c = '+str(self.wood_c)+'\n')
        file.write('iron = '+str(self.iron)+'\n')
        file.write('iron_c = '+str(self.iron_c)+'\n')
        file.write('turn = '+str(self.turn)+'\n')
        file.write('a_reset = '+str(self.a_reset)+'\n')
        file.write('show_conv = '+str(self.show_conv)+'\n')
        file.write("trade_lbl = \""+self.trade_lbl.get()+"\"\n")
        if self.trade_qty.get() == '':
            trade_qty = ''
        else:
            trade_qty = self.trade_qty.get()
        file.write("trade_qty = \""+trade_qty+"\"\n")
        file.write("receive_lbl = \""+self.receive_lbl.get()+"\"\n")
        if self.receive_qty.get() == '':
            receive_qty = ''
        else:
            receive_qty = self.receive_qty.get()
        file.write("receive_qty = \""+receive_qty+"\"\n")
        file.close()
        self.scrdestroy(self.savescreen)
        self.scrdestroy(self.confirm)
        self.confirm = Tk()
        self.confirm.title('')
        error_txt = Label(self.confirm,text='Saved!',width=6)
        error_txt.grid(row=1,column=1,padx=35)
        ok_btn = Button(self.confirm,text='OK',command=lambda:self.scrdestroy(self.confirm))
        ok_btn.grid(row=2,column=1,sticky='NEWS',padx=35)

    def autoreset(self):
        if self.a_reset:
            self.a_reset = False
            self.trade_reset.configure(text='Auto-Reset: OFF')
        else:
            self.a_reset = True
            self.trade_reset.configure(text='Auto-Reset: ON')

    def tradereset(self):
        self.trade_lbl.set("Trade Resource")
        self.receive_lbl.set("Receive Resource")
        self.trade_qty.delete(0,'end')
        self.receive_qty.delete(0,'end')

    def showcalc(self):
        if self.show_conv:
            self.show_conv = False
            self.show_calc.configure(text='Show conversion rates')
            self.conv_to_food_lbl.grid_forget()
            self.conv_to_wood_lbl.grid_forget()
            self.conv_to_iron_lbl.grid_forget()
            self.conv_to_gold_lbl.grid_forget()
            self.conv_error_lbl.grid_forget()
            self.refresh_calc.grid_forget()
        else:
            self.show_conv = True
            self.show_calc.configure(text='Hide conversion rates')
            self.refresh_calc.grid(row=5,column=11,columnspan=2,sticky='SEW')
            self.refreshcalc()

    def refreshcalc(self):
        trading = str(self.trade_lbl.get())[7:]
        if trading == 'esource':
            show = False
        t_qty = self.trade_qty.get()
        try:
            t_qty = int(t_qty)
            show = True
        except:
            show = False
            self.conv_to_food_lbl.grid_forget()
            self.conv_to_wood_lbl.grid_forget()
            self.conv_to_iron_lbl.grid_forget()
            self.conv_to_gold_lbl.grid_forget()
            self.conv_error_lbl.grid_forget()
            if t_qty == '' or trading == 'esource':
                self.conv_error_lbl.configure(text='Nothing to trade!')
            else:
                self.conv_error_lbl.configure(text='Could not read qty.')
            self.conv_error_lbl.grid(row=6,column=11,columnspan=2,sticky='NEWS')
        if show:
            self.conv_error_lbl.grid_forget()
            if trading == 'Food':
                self.r_rsc = [int(0.9*t_qty*0.9),int(0.9*t_qty*1.1),int(0.45*t_qty*0.9),int(0.45*t_qty*1.1),int(0.18*t_qty*0.9),int(0.18*t_qty*1.1),int(0.009*t_qty*0.9),int(0.009*t_qty*1.1)]
            elif trading == 'Wood':
                self.r_rsc = [int(1.8*t_qty*0.9),int(1.8*t_qty*1.1),int(0.9*t_qty*0.9),int(0.9*t_qty*1.1),int(0.36*t_qty*0.9),int(0.36*t_qty*1.1),int(0.018*t_qty*0.9),int(0.018*t_qty*1.1)]
            elif trading == 'Iron':
                self.r_rsc = [int(4.5*t_qty*0.9),int(4.5*t_qty*1.1),int(2.25*t_qty*0.9),int(2.25*t_qty*1.1),int(0.9*t_qty*0.9),int(0.9*t_qty*1.1),int(0.045*t_qty*0.9),int(0.045*t_qty*1.1)]
            else:
                self.r_rsc = [int(90*t_qty*0.9),int(90*t_qty*1.1),int(45*t_qty*0.9),int(45*t_qty*1.1),int(18*t_qty*0.9),int(18*t_qty*1.1),int(0.9*t_qty*0.9),int(0.9*t_qty*1.1)]
            for neg in range(len(self.r_rsc)):
                if self.r_rsc[neg] < 0:
                    self.r_rsc[neg] = 0
            self.conv_to_food_lbl.configure(text='Food: '+str(self.r_rsc[0])+' - '+str(self.r_rsc[1]))
            self.conv_to_food_lbl.grid(row=6,column=11, columnspan=2, sticky='NEW')
            self.conv_to_wood_lbl.configure(text='Wood: '+str(self.r_rsc[2])+' - '+str(self.r_rsc[3]))
            self.conv_to_wood_lbl.grid(row=6,column=11, columnspan=2, sticky='SEW')
            self.conv_to_iron_lbl.configure(text='Iron: '+str(self.r_rsc[4])+' - '+str(self.r_rsc[5]))
            self.conv_to_iron_lbl.grid(row=7, column=11, columnspan=2, sticky='NEW')
            self.conv_to_gold_lbl.configure(text='Gold: '+str(self.r_rsc[6])+' - '+str(self.r_rsc[7]))
            self.conv_to_gold_lbl.grid(row=7, column=11, columnspan=2, sticky='SEW')
                
    def autoreceive(self,rsc):
        if rsc == 'food':
            self.receive_qty.delete(0,'end')
            self.receive_qty.insert(0,self.r_rsc[0])
            self.receive_lbl.set('Receive: Food')
        elif rsc == 'wood':
            self.receive_qty.delete(0,'end')
            self.receive_qty.insert(0,self.r_rsc[2])
            self.receive_lbl.set('Receive: Wood')
        elif rsc == 'iron':
            self.receive_qty.delete(0,'end')
            self.receive_qty.insert(0,self.r_rsc[4])
            self.receive_lbl.set('Receive: Iron')
        else:
            self.receive_qty.delete(0,'end')
            self.receive_qty.insert(0,self.r_rsc[6])
            self.receive_lbl.set('Receive: Gold')
        
    def remove_workers(self):
        for i in range(2):
            for row in range(10):
                for col in range(10):
                    if self.worker_grid[row][col] and self.place_pop > self.pop:
                        if str(self.grid[row][col])[2] != 'F' or i == 1:
                            self.worker_grid[row][col] = False
                            self.bgrid[row][col].configure(background=self.bgcolor)
                            self.place_pop -= 1
        
    def is_touching(self,points,test_coord): #points should be a list
        return_tf = False
        for pt in points:
            if abs(test_coord[0]-pt[0]) < 2 and abs(test_coord[1]-pt[1]) < 2:
                return_tf = True
        return return_tf

    def get_rsc(self,event):
        row,col = str(event.widget)[-2],str(event.widget)[-1]
        if col == 'n':
            col = 1
        if row == 'n' or row == 'o':
            row = 0
        if row != 'n' and col == '0':
            row = int(row)-1
        row = int(row)
        col = (int(col)+9) % 10
        if self.reveal_grid[row][col]:
            if self.placing and not self.worker_grid[row][col]:
                self.worker_grid[row][col] = True
                self.place_pop += 1
                self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
                event.widget.configure(background='lightgray')
                if self.place_pop == self.pop:
                    self.placing = False
            elif self.removing and self.worker_grid[row][col]:
                self.worker_grid[row][col] = False
                self.place_pop -= 1
                self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
                event.widget.configure(background=self.bgcolor)
                if self.place_pop == 0:
                    self.removing = False
    def trade(self):
        trading = self.trade_lbl.get()
        if trading != 'Trade Resource':
            trading = trading[7:]
        t_qty = self.trade_qty.get()
        try:
            t_qty = int(t_qty)
        except:
            t_qty = 0
        receiving = self.receive_lbl.get()
        if receiving != 'Receive Resource':
            receiving = receiving[9:]
        r_qty = self.receive_qty.get()
        try:
            r_qty = int(r_qty)
        except:
            r_qty = 0
        if r_qty > 0 and t_qty > 0:
            
            ### KEY ###
            ## Food = 1 Unit
            ## Wood = 2 Units
            ## Iron = 5 Units
            ## Gold = 100 Units
            ## "TAX" = -10% on conversion
            ### KEY ###
            
            if trading == 'Food':
                rsc_qty = self.food
                if receiving == 'Food':
                    multiplier = 0.9
                elif receiving == 'Wood':
                    multiplier = 0.45
                elif receiving == 'Iron':
                    multiplier = 0.18
                else:
                    multiplier = 0.009
            elif trading == 'Wood':
                rsc_qty = self.wood
                if receiving == 'Food':
                    multiplier = 1.8
                elif receiving == 'Wood':
                    multiplier = 0.9
                elif receiving == 'Iron':
                    multiplier = 0.36
                else:
                    multiplier = 0.018
            elif trading == 'Iron':
                rsc_qty = self.iron
                if receiving == 'Food':
                    multiplier = 4.5
                elif receiving == 'Wood':
                    multiplier = 2.25
                elif receiving == 'Iron':
                    multiplier = 0.9
                else:
                    multiplier = 0.045
            else:
                rsc_qty = self.gold
                if receiving == 'Food':
                    multiplier = 90
                elif receiving == 'Wood':
                    multiplier = 45
                elif receiving == 'Iron':
                    multiplier = 18
                else:
                    multiplier = 0.9
            true_qty = randint((int(multiplier*t_qty*0.9)),(int(multiplier*t_qty*1.1)))
        else:
            true_qty = 0
            rsc_qty = 0
        if true_qty >= r_qty:
            r_qty = true_qty
        else:
            r_qty = 0
        if r_qty != 0:
            if trading == 'Food' and t_qty <= self.food:
                self.food = self.food - t_qty
                for i in range(len(self.food_list)):
                    if t_qty <= self.food_list[i]:
                        self.food_list[i].append(0-t_qty)
                    else:
                        t_qty = t_qty - sum(self.food_list[i])
                        self.food_list[i] = [0]
            elif trading == 'Wood' and t_qty <= self.wood:
                self.wood = self.wood - t_qty
            elif trading == 'Iron' and t_qty <= self.iron:
                self.iron = self.iron - t_qty
            elif t_qty <= self.gold:
                self.gold = self.gold - t_qty
        if t_qty <= rsc_qty:
            if receiving == 'Food':
                self.food_list[-1].append(r_qty)
            elif receiving == 'Wood':
                self.wood = self.wood + r_qty
            elif receiving == 'Iron':
                self.iron = self.iron + r_qty
            else:
                self.gold = self.gold + r_qty

    def end(self):
        self.wood_c = int(self.wood)
        self.iron_c = int(self.iron)
        self.gold_c = int(self.gold)
        self.food_list.append([])
        del self.food_list[0]
        self.collect_rsc()
        self.trade() #intentionally before food consumption
        self.refreshcalc()
        if self.turn > 5:
            death = float(0.01*randint(65,90))
            if randint(1,1000) == 1:
                death = float(0.09)
            self.pop = int(self.pop * death)
        if self.food < self.pop:
            self.pop = self.food
            self.food = 0
            for i in range(len(self.food_list)):
                self.food_list[i] = [0]
        else:
            consumption = self.pop
            for i in range(len(self.food_list)):
                sum_ = sum(self.food_list[i])
                if consumption >= sum_:
                    consumption = consumption - sum_
                    self.food_list[i] = [0]
                else:
                    self.food_list[i] = [sum_ - consumption]
                    consumption = 0
            
                
            #self.food = self.food - self.pop
        
        if self.place_pop > self.pop:
            self.remove_workers()

        self.game = True
        if self.pop == 0 and self.turn > 1:
            root.destroy()
            gover = Label(text='Game Over!',width=20,height=3)
            gover.grid(row=1,column=1)
            self.game = False

        self.pop = self.pop + int(self.food/5)
        
        if self.game:
            self.placing = False
            self.removing = False
            if self.a_reset:
                self.trade_lbl.set("Trade Resource")
                self.receive_lbl.set("Receive Resource")
                self.trade_qty.delete(0,'end')
                self.receive_qty.delete(0,'end')
            self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
            self.gold_lbl.configure(text='Gold: '+str(self.gold)+' ('+str(self.gold-self.gold_c)+')')
            self.food_lbl.configure(text='Food: '+str(self.food)+' ('+str(sum(self.food_list[-1]))+')')
            self.wood_lbl.configure(text='Wood: '+str(self.wood)+' ('+str(self.wood-self.wood_c)+')')
            self.iron_lbl.configure(text='Iron: '+str(self.iron)+' ('+str(self.iron-self.iron_c)+')')
            self.turn += 1
            self.turn_lbl.configure(text='Turn: '+str(self.turn))
            for row in range(10):
                for col in range(10):
                    if not self.reveal_grid[row][col]:
                        for row_ in range(-1,2):
                            for col_ in range(-1,2):
                                if -1 < row+row_ and row+row_ < 10 and -1 < col+col_ and col+col_ < 10:
                                    if self.worker_grid[row+row_][col+col_]:
                                        if randint(1,2) == 1:
                                            self.reveal_grid2[row][col] = True
            
            for row in range(10):
                for col in range(10):
                    if self.reveal_grid2[row][col]:
                        self.reveal_grid[row][col] = True
                        self.bgrid[row][col].configure(text=self.grid[row][col])
            
    def collect_rsc(self):
        for row in range(10):
            for col in range(10):
                if self.worker_grid[row][col]:
                    rsc_amt = int(str(self.grid[row][col])[0])
                    if str(self.grid[row][col])[2] == 'F':
                        self.food_list[-1].append(rsc_amt)
                        self.food_halflist = self.food_list[:]
                        for i in range(len(self.food_halflist)):
                            self.food_halflist[i] = sum(self.food_halflist[i])
                        self.food = sum(self.food_halflist)
                    elif str(self.grid[row][col])[2] == 'W':
                        self.wood = self.wood + rsc_amt
                    else:
                        self.iron = self.iron + rsc_amt
                    
    def place(self):
        if self.place_pop < self.pop:
            if self.placing:
                self.placing = False
            else:
                self.placing = True
            if self.removing:
                self.removing = False

    def remove(self):
        if self.removing:
            self.removing = False
        else:
            self.removing = True
        if self.placing:
            self.placing = False
root = Tk()
game = Game(root)
root.mainloop()
