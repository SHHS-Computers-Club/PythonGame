from tkinter import *
from random import randint
from datetime import datetime
from os import path
from inspect import getfile, currentframe
import sys

class Game:
    def __init__(self, master):
        root.title('Game')
        root.resizable(width=False, height=False)
        self.frame = Frame(master=root)
        self.frame.pack_propagate(0)
        self.frame.grid()
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
        self.food_slot = 3
        self.wood = 0
        self.iron = 0
        self.placing = False
        self.removing = False
        self.startxy = [1,1]
        self.turn = 1
        self.turnend = False
        self.a_reset = True
        self.show_conv = False

        for row in self.grid:
            for i in range(10):
                rs = randint(1,3)
                if rs == 1:
                    rs = 'xFood\n+0'
                    qt = randint(1,4)
                    if qt == 4:
                        qt = randint(2,3)
                elif rs == 2:
                    rs = 'xWood\n+0'
                    qt = randint(1,3)
                else:
                    rs = 'xIron\n+0'
                    qt = randint(1,2)
                
                row.append(str(qt)+rs)

        self.turn_lbl = Label(self.frame,text='Turn: '+str(self.turn))
        self.turn_lbl.grid(row=1,column=1,columnspan=2,sticky='W')
        self.gold_lbl = Label(self.frame,text='Gold: '+str(self.gold)+' (0)')
        self.gold_lbl.grid(row=1,column=4,columnspan=3,sticky='W')
        self.gold_c = 0
        self.pop_lbl = Label(self.frame,text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
        self.pop_lbl.grid(row=1,column=7,columnspan=3,sticky='W')
        self.food_lbl = Label(self.frame,text='Food: '+str(self.food)+' ('+str(sum(self.food_list[-1]))+')')
        self.food_lbl.grid(row=2,column=1,columnspan=3,sticky='W')
        self.wood_lbl = Label(self.frame,text='Wood: '+str(self.wood)+' (0)')
        self.wood_lbl.grid(row=2,column=4,columnspan=3,sticky='W')
        self.wood_c = 0
        self.iron_lbl = Label(self.frame,text='Iron: '+str(self.iron)+' (0)')
        self.iron_lbl.grid(row=2,column=7,columnspan=3,sticky='W')
        self.iron_c = 0
        self.load_lbl = Label(self.frame,text='',fg='red')

        self.it = 1
        for row in range(10):
            self.ct = 1
            for col in range(10):
                if self.is_touching([[1,1]],[self.it-1,self.ct-1]):
                    self.bgrid[row].append(Button(self.frame, text=self.grid[row][col], width=6, height=3))
                    self.reveal_grid[row].append(True)
                    self.reveal_grid2[row].append(True)
                else:
                    self.bgrid[row].append(Button(self.frame, text='',width=6, height=3))
                    self.reveal_grid[row].append(False)
                    self.reveal_grid2[row].append(False)
                self.worker_grid[row].append(False)
                self.bgrid[row][col].grid(row=self.it+2,column=self.ct,sticky='NSEW')
                self.bgrid[row][col].bind("<Button-1>",self.get_rsc)
                self.ct += 1
            self.it += 1
        self.placer_btn = Button(self.frame, text='Place building', width=14, height=3,command=self.place)
        self.placer_btn.grid(column=1,row=13,columnspan=2)
        self.remove_btn = Button(self.frame, text='Remove building', width=14, height=3,command=self.remove)
        self.remove_btn.grid(column=3,row=13,columnspan=2)
        self.end_btn = Button(self.frame, text='End Turn', width=14, height=3, command=self.end)
        self.end_btn.grid(column=5,row=13,columnspan=2)
        self.save_btn = Button(self.frame, text='Save game', width=14, height=3, command=self.save)
        self.save_btn.grid(column=7,row=13,columnspan=2)
        self.load_btn = Button(self.frame, text='Load game', width=14, height=3, command=self.load)
        self.load_btn.grid(column=9,row=13,columnspan=2)
        self.bgcolor = self.end_btn.cget('background')

        self.blank_lbl = StringVar(self.frame)
        self.blank_lbl.set("")
        self.trade_head = Label(self.frame,text='Trade',width=20)
        self.trade_head.grid(row=2,column=11,columnspan=2,sticky='NEWS')
        self.trade_lbl = StringVar(self.frame)
        self.trade_lbl.set("Trade Resource")
        self.trade_rsc = OptionMenu(self.frame, self.trade_lbl, "Trade: Food","Trade: Wood","Trade: Iron","Trade: Gold")
        self.trade_rsc.grid(row=3,column=11,columnspan=2,sticky='NEW')
        self.trade_qty_lbl = Label(self.frame,text='Qty:')
        self.trade_qty_lbl.grid(row=3,column=11,sticky='WS')
        self.trade_qty = Entry(self.frame, width=5)
        self.trade_qty.grid(row=3,column=11, sticky='S')
        self.receive_lbl = StringVar(self.frame)
        self.receive_lbl.set("Receive Resource")
        self.receive_rsc = OptionMenu(self.frame, self.receive_lbl, "Receive: Food","Receive: Wood","Receive: Iron","Receive: Gold")
        self.receive_rsc.grid(row=4,column=11,columnspan=2,sticky='NEW')
        self.receive_qty_lbl = Label(self.frame,text='Min:')
        self.receive_qty_lbl.grid(row=4,column=11,sticky='WS')
        self.receive_qty = Entry(self.frame, width=5)
        self.receive_qty.grid(row=4,column=11, sticky='S')
        self.trade_reset = Button(self.frame,text='Auto-Reset: ON', command=self.autoreset)
        self.trade_reset.grid(row=5,column=11,columnspan=2,sticky='NEW')
        self.t_set = Button(self.frame,text='Reset', command=self.tradereset)
        self.t_set.grid(row=5,column=11, columnspan=2,sticky='SEW')
        self.show_calc = Button(self.frame,text='Show conversion rates', command=self.showcalc)
        self.show_calc.grid(row=6,column=11,columnspan=2,sticky='NEW')
        self.refresh_calc = Button(self.frame,text='Refresh',command=self.refreshcalc)
        self.conv_to_food_lbl = Button(self.frame,text='',command=lambda:self.autoreceive('food'))
        self.conv_to_wood_lbl = Button(self.frame,text='',command=lambda:self.autoreceive('wood'))
        self.conv_to_iron_lbl = Button(self.frame,text='',command=lambda:self.autoreceive('iron'))
        self.conv_to_gold_lbl = Button(self.frame,text='',command=lambda:self.autoreceive('gold'))
        self.conv_error_lbl = Label(self.frame,text='')
        
        self.build_panel_head = Label(self.frame,text='Buildings',width=24)
        self.build_panel_head.grid(row=2, column=13, columnspan=2, sticky='NEWS')
        self.build_drop_lbl = StringVar(self.frame)
        self.build_drop_lbl.set('Select Building')
        self.building_drop = OptionMenu(self.frame,self.build_drop_lbl,'Granary','Sawmill','Mine')
        self.building_drop.grid(row=3,column=13,columnspan=2,sticky='NEW')
        self.build_info_button = Button(self.frame,text='Info',command=self.buildinfo)
        self.build_info_button.grid(row=3,column=13,columnspan=2,sticky='SEW')
        self.build_confirm = Button(self.frame,text='Confirm Build',command=self.confbuild)
        self.build_confirm.grid(row=4,column=13,columnspan=2,sticky='NEW')
        self.build_auto = Button(self.frame,text='Auto-Reset: ON',width=11,command=self.autobuild)
        self.build_auto.grid(row=5,column=13,columnspan=2,sticky='NEW')
        self.build_auto_reset = True
        self.build_reset = Button(self.frame,text='Reset',command=self.resetbuild)
        self.build_reset.grid(row=5,column=13,columnspan=2,sticky='SEW')
        self.building = False
        self.build_info_desc = Label(self.frame,text='')
        self.build_info_cost_c = Label(self.frame,text='Cost: ')
        self.build_info_cost_1 = Label(self.frame,text='')
        self.build_info_cost_2 = Label(self.frame,text='')
        self.build_info_cost_3 = Label(self.frame,text='')
        self.buildings = [0,0,0] #granaries, sawmills, mines count
        self.build_active = [0,0,0]
        self.build_grid = []
        for i in range(10):
            self.build_grid.append([0,0,0,0,0,0,0,0,0,0])

        ###This next section looks bulky, but "for" loops don't pass the correct argument (making all of them pass the last iteration's value), and binding is dangerous for if I want to add buttons before them
          ##I already bound the grid, which only works because those are the first buttons created; leaving these unbound allows more flexibility in readjusting position.
        self.build_list = []
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(0)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(1)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(2)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(3)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(4)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(5)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(6)))
        self.build_list.append(Button(self.frame,text='',command=lambda:self.activebuild(7)))
        self.build_all = []
        self.build_workers = []
        self.build_error = Label(self.frame,text='')
        self.blist_first = 0
            
    def save(self):
        self.savescreen = Tk()
        self.savescreen.title('Save')
        self.savescreen.resizable(width=False,height=False)
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
        self.loadscreen.resizable(width=False,height=False)

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
            f = open(path.dirname(path.abspath(getfile(currentself.frame())))+'\\'+self.name_enter.get()+'.py')

            filetext = f.read()
            f.close()
            f = True
        except:
            f = False
        if f and self.name_enter.get().lower() != 'game.py':
            self.confirm = Tk()
            self.confirm.title('')
            self.confirm.resizable(width=False,height=False)
            confirm_txt = Label(self.confirm,text='A file with this name already exists.\nAre you sure you want to overwrite it?')
            confirm_txt.grid(row=1,column=1,columnspan=2,rowspan=2)
            confirm_ccl = Button(self.confirm,text='No',command=lambda:self.scrdestroy(self.confirm))
            confirm_ccl.grid(row=3,column=1,sticky='NEWS')
            confirm_yes = Button(self.confirm,text='Yes',command=self.realconf)
            confirm_yes.grid(row=3,column=2,sticky='NEWS')
        elif self.name_enter.get().lower() == 'game.py' or bad_char:
            self.invalidfile()
        else:
            self.realsave()

    def realconf(self):
        self.scrdestroy(self.confirm)
        self.realsave()

    def confload(self):
        load = ''
        if self.name_enter.get() == 'init':
            self.frame.grid_forget()
            self.__init__(root)
            self.scrdestroy(self.loadscreen)
        else:
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
                self.food_list = []
                for m in range(len(load.food_list)):
                    self.food_list.append([])
                    for n in range(len(load.food_list[m])):
                        self.food_list[m].append(load.food_list[m][n])
                self.food_slot = int(load.food_slot)
                self.wood = int(load.wood)
                self.wood_c = int(load.wood_c)
                self.iron = int(load.iron)
                self.iron_c = int(load.iron_c)
                self.turn = int(load.turn)
                self.a_reset = not load.a_reset
                self.autoreset()
                self.show_conv = not load.show_conv
                self.show_conv = not self.show_conv
                self.trade_lbl.set(load.trade_lbl)
                self.trade_qty.delete(0,'end')
                self.trade_qty.insert(0,load.trade_qty)
                self.receive_lbl.set(load.receive_lbl)
                self.receive_qty.delete(0,'end')
                self.receive_qty.insert(0,load.receive_qty)
                self.build_all = []
                self.build_workers = []
                for i in range(len(load.build_all)):
                    self.build_all.append(load.build_all[i])
                    self.build_workers.append(load.build_workers[i])
                self.blist_first = int(load.blist_first)
                self.build_drop_lbl.set(load.build_drop_lbl)
                self.building = not load.building #intentional
                self.buildings = []
                for i in range(len(load.buildings)):
                    self.buildings.append(load.buildings[i])
                self.build_active = []
                for i in range(len(load.build_active)):
                    self.build_active.append(load.build_active[i])
                self.confbuild()
                if load.build_auto_reset:
                    self.build_auto_reset = True
                    self.build_auto.configure(text='Auto-Reset: ON')
                else:
                    self.build_auto_reset = False
                    self.build_auto.configure(text='Auto-Reset: OFF')
                self.placing = False
                self.removing = False
                
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

                for i in range(8):
                    self.build_list[i].grid_forget()
                    if i+self.blist_first <= len(self.build_all) - 1:
                        self.build_list[i].configure(text=self.build_all[i+self.blist_first])
                        if i % 2 == 0:
                            self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='NEW')
                        else:
                            self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='SEW')
                        if self.build_workers[i]:
                            self.build_list[i].configure(bg='lightgray')
                        else:
                            self.build_list[i].configure(bg=self.bgcolor)

                self.scrdestroy(self.loadscreen)
                self.load_lbl.configure(text='Loaded File!')
                self.load_lbl.grid(row=1,column=11,columnspan=2)
            except:
                self.invalidfile()
        del load
            
    def scrdestroy(self,screen):
        try:
            screen.destroy()
            screen = False
        except:
            pass
        
    def invalidfile(self):
        self.confirm = Tk()
        self.confirm.title('')
        self.confirm.resizable(width=False,height=False)
        L_margin = Label(self.confirm,text='', width=2)
        L_margin.grid(row=1,column=1)
        R_margin = Label(self.confirm,text='',width=2)
        R_margin.grid(row=1,column=3)
        error_txt = Label(self.confirm,text='Invalid file name!')
        error_txt.grid(row=1,column=2)
        ok_btn = Button(self.confirm,text='OK',command=lambda:self.scrdestroy(self.confirm))
        ok_btn.grid(row=2,column=2,sticky='NEWS')
        
    def realsave(self):
        file = open(path.dirname(path.abspath(getfile(currentframe())))+'\\'+self.name_enter.get()+'.py','w')
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
        file.write('food_slot = '+str(self.food_slot)+'\n')
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
        file.write("build_all = "+str(self.build_all)+"\n")
        file.write("build_workers = "+str(self.build_workers)+"\n")
        file.write("blist_first = "+str(self.blist_first)+"\n")
        file.write("build_drop_lbl = \""+self.build_drop_lbl.get()+"\"\n")
        file.write("building = "+str(self.building)+"\n")
        file.write("build_auto_reset = "+str(self.build_auto_reset)+"\n")
        file.write("buildings = "+str(self.buildings)+"\n")
        file.write("build_active = "+str(self.build_active)+"\n")
        file.close()
        self.scrdestroy(self.savescreen)
        self.confirm = Tk()
        self.confirm.title('')
        error_txt = Label(self.confirm,text='Saved!',width=6)
        error_txt.grid(row=1,column=1,padx=35)
        ok_btn = Button(self.confirm,text='OK',command=lambda:self.scrdestroy(self.confirm))
        ok_btn.grid(row=2,column=1,sticky='NEWS',padx=35)

    def closeall(self,screen):
        try:
            for i in screen:
                self.scrdestroy(i)
            root.destroy()
        except:
            pass
        sys.exit()
        
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

    def autobuild(self):
        if self.build_auto_reset:
            self.build_auto_reset = False
            self.build_auto.configure(text='Auto-Reset: OFF')
        else:
            self.build_auto_reset = True
            self.build_auto.configure(text='Auto-Reset: ON')

    def resetbuild(self):
        self.build_drop_lbl.set('Select Building')
        self.build_info_desc.configure(text='')
        self.build_info_cost_c.configure(text='')
        self.build_info_cost_1.configure(text='')
        self.build_info_cost_2.configure(text='')
        self.build_info_cost_3.configure(text='')
        if not self.turnend:
            self.build_error.configure(text='')
        if self.building:
            self.confbuild()

    
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
            self.refresh_calc.grid(row=6,column=11,columnspan=2,sticky='SEW')
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
                if not self.turnend:
                    self.conv_error_lbl.configure(text='Nothing to trade!')
                else:
                    self.conv_error_lbl.configure(text='')
            else:
                self.conv_error_lbl.configure(text='Could not read qty.')
            self.conv_error_lbl.grid(row=7,column=11,columnspan=2,sticky='NEWS')
        if show and not self.turnend:
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
            self.conv_to_food_lbl.grid(row=7,column=11, columnspan=2, sticky='NEW')
            self.conv_to_wood_lbl.configure(text='Wood: '+str(self.r_rsc[2])+' - '+str(self.r_rsc[3]))
            self.conv_to_wood_lbl.grid(row=7,column=11, columnspan=2, sticky='SEW')
            self.conv_to_iron_lbl.configure(text='Iron: '+str(self.r_rsc[4])+' - '+str(self.r_rsc[5]))
            self.conv_to_iron_lbl.grid(row=8, column=11, columnspan=2, sticky='NEW')
            self.conv_to_gold_lbl.configure(text='Gold: '+str(self.r_rsc[6])+' - '+str(self.r_rsc[7]))
            self.conv_to_gold_lbl.grid(row=8, column=11, columnspan=2, sticky='SEW')
                
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

    def buildinfo(self):
        building = str(self.build_drop_lbl.get())
        self.build_error.grid_forget()
        show = False
        if building == 'Granary':
            self.build_info_desc.configure(text='Allows food to be kept\nlonger.')
            self.build_info_cost_1.configure(text='Wood: '+str(300+50*self.buildings[0]))
            self.build_info_cost_2.configure(text='Iron: '+str(150+50*self.buildings[0]))
            self.build_info_cost_3.configure(text='Gold: '+str(int(50+50*self.buildings[0]*(1.04**self.turn))))
            show = True
        elif building == 'Sawmill':
            self.build_info_desc.configure(text='Allows more wood to be\ncollected on one tile.')
            self.build_info_cost_1.configure(text='Wood: '+str(100+50*self.buildings[1]))
            self.build_info_cost_2.configure(text='Iron: '+str(150+50*self.buildings[1]))
            self.build_info_cost_3.configure(text='Gold: '+str(int(50+50*self.buildings[1]*(1.04**self.turn))))
            show = True
        elif building == 'Mine':
            self.build_info_desc.configure(text='Allows more iron to be\ncollected on one tile.')
            self.build_info_cost_1.configure(text='Wood: '+str(400+50*self.buildings[2]))
            self.build_info_cost_2.configure(text='Iron: '+str(200+50*self.buildings[2]))
            self.build_info_cost_3.configure(text='Gold: '+str(int(50+50*self.buildings[2]*(1.04**self.turn))))
            show = True
        if show:
            self.build_info_desc.grid(row=6,column=13,columnspan=2)
            self.build_info_cost_c.configure(text='Cost:')
            self.build_info_cost_c.grid(row=7,column=13,sticky='NW')
            self.build_info_cost_1.grid(row=7,column=14,sticky='NW')
            self.build_info_cost_2.grid(row=7,column=13,sticky='WS')
            self.build_info_cost_3.grid(row=7,column=14,sticky='WS')

    def confbuild(self):
        if self.building:
            self.build_confirm.configure(text='Confirm Build')
            self.build_confirm.configure(bg=self.bgcolor)
            self.building = False
        else:
            self.build_confirm.configure(text='Deconfirm Build')
            self.build_confirm.configure(bg='lightgray')
            self.building = True

    def build(self):
        building = str(self.build_drop_lbl.get())
        errormsg = ''
        if building == 'Granary':
            if self.wood < 300+50*self.buildings[0]:
                errormsg = 'Not enough Wood!\n'
            if self.iron < 150+50*self.buildings[0]:
                errormsg = errormsg+'Not enough Iron!\n'
            if self.gold < int(50+50*self.buildings[0]*(1.04**self.turn)):
                errormsg = errormsg+'Not enough Gold!'
            if errormsg == '':
                self.wood = self.wood - (300+50*self.buildings[0])
                self.iron = self.iron - (150+50*self.buildings[0])
                self.gold = self.gold - int(50+50*self.buildings[0]*(1.04**self.turn))
                self.buildings[0] += 1
        elif building == 'Sawmill':
            if self.wood < 100+50*self.buildings[1]:
                errormsg = 'Not enough Wood!\n'
            if self.iron < 150+50*self.buildings[1]:
                errormsg = errormsg+'Not enough Iron!\n'
            if self.gold < int(50+50*self.buildings[1]*(1.04**self.turn)):
                errormsg = errormsg+'Not enough Gold!'
            if errormsg == '':
                self.wood = self.wood - (100+50*self.buildings[1])
                self.iron = self.iron - (150+50*self.buildings[1])
                self.gold = self.gold - int(50+50*self.buildings[1]*(1.04**self.turn))
                self.buildings[1] += 1
        elif building == 'Mine':
            if self.wood < 400+50*self.buildings[2]:
                errormsg = 'Not enough Wood!\n'
            if self.iron < 200+50*self.buildings[2]:
                errormsg = errormsg+'Not enough Iron!\n'
            if self.gold < int(50+50*self.buildings[2]*(1.04**self.turn)):
                errormsg = errormsg+'Not enough Gold!'
            if errormsg == '':
                self.wood = self.wood - (400+50*self.buildings[2])
                self.iron = self.iron - (200+50*self.buildings[2])
                self.gold = self.gold - int(50+50*self.buildings[2]*(1.04**self.turn))
                self.buildings[2] += 1
        else:
            errormsg = 'No building selected!'
            
        self.build_error.configure(text=errormsg)
        self.build_error.grid(row=6,rowspan=2,column=13,columnspan=2)
        
        if errormsg == '':
            if len(self.build_all) % 8 == 0 and len(self.build_all) != 0:
                self.build_all.insert(-1,'v')
                self.build_workers.insert(-1,False)
                self.build_all.insert(-1,'^')
                self.build_workers.insert(-1,False)
                
            self.build_all.append(building)
            self.build_workers.append(False)
            for i in range(0,8):
                if i+self.blist_first > len(self.build_all) - 1:
                    break
                self.build_list[i].configure(text=self.build_all[i+self.blist_first])
                if self.build_workers[i+self.blist_first]:
                    self.build_list[i].configure(background='lightgray')
                else:
                    self.build_list[i].configure(background=self.bgcolor)
                if i % 2 == 0:
                    self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='NEW')
                else:
                    self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='SEW')
                
    def activebuild(self,i):
        building = self.build_list[i].cget('text')
        if building == 'Granary' and self.build_workers[i+self.blist_first]:
            self.build_workers[i+self.blist_first] = False
            self.place_pop -= 5
            self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
            self.build_list[i].configure(bg=self.bgcolor)
            self.build_active[0] -= 1
            self.food_slot -= 1
        elif building == 'Granary' and self.pop - self.place_pop >= 5:
            self.build_workers[i+self.blist_first] = True
            self.place_pop += 5
            self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
            self.build_list[i].configure(bg='lightgray')
            self.build_active[0] += 1
            self.food_slot += 1
            
        if building == 'Sawmill' or building == 'Mine':
            please_place = Tk()
            please_place.title('')
            please_place.resizable(width=False,height=False)
            msg = Label(please_place,text="Please use the 'Place building' button\n to use this building!")
            msg.grid(row=1,rowspan=2,column=1,columnspan=2)
            ok_btn = Button(please_place,text='OK',width=6,command=lambda:self.scrdestroy(please_place))
            ok_btn.grid(row=3,column=1,columnspan=2)

        if building == '^':
            self.blist_first -= 8
            for i in range(8):
                self.build_list[i].grid_forget()
                if i+self.blist_first <= len(self.build_all) - 1:
                    self.build_list[i].configure(text=self.build_all[i+self.blist_first])
                    if self.build_workers[i+self.blist_first]:
                        self.build_list[i].configure(bg='lightgray')
                    else:
                        self.build_list[i].configure(bg=self.bgcolor)
                    if i % 2 == 0:
                        self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='NEW')
                    else:
                        self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='SEW')
                    
        if building == 'v':
            self.blist_first += 8
            for i in range(8):
                self.build_list[i].grid_forget()
                if i+self.blist_first <= len(self.build_all) - 1:
                    self.build_list[i].configure(text=self.build_all[i+self.blist_first])
                    if self.build_workers[i+self.blist_first]:
                        self.build_list[i].configure(bg='lightgray')
                    else:
                        self.build_list[i].configure(bg=self.bgcolor)
                    if i % 2 == 0 and self.build_all[i+self.blist_first] != 'v':
                        self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='NEW')
                    elif self.build_all[i+self.blist_first] != 'v':
                        self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='SEW')
                    elif i+self.blist_first < len(self.build_all) - 1:
                        if i % 2 == 0:
                            self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='NEW')
                        else:
                            self.build_list[i].grid(row=9+int(i/2),column=11,columnspan=2,sticky='SEW')
        
    def remove_workers(self):
        mod_remove = []
        for i in range(len(self.build_workers)):
            if self.build_workers[i] and self.build_all[i] != 'Granary' and self.place_pop > self.pop:
                self.build_workers[i] = False
                self.place_pop -= 10
                if i >= self.blist_first and i - self.blist_first < 8:
                    self.build_list[i-self.blist_first].configure(bg=self.bgcolor)
                if self.build_all[i] == 'Sawmill':
                    mod_remove.append('W')
                else:
                    mod_remove.append('I')
            elif self.place_pop <= self.pop:
                break
        for row in range(10):
            for col in range(10):
                if self.worker_grid[row][col] and self.place_pop > self.pop:
                    if str(self.grid[row][col])[2] != 'F':
                        self.worker_grid[row][col] = False
                        self.bgrid[row][col].configure(background=self.bgcolor)
                        self.place_pop -= 1
                elif self.place_pop <= self.pop:
                    break
        for i in range(len(self.build_workers)):
            if self.build_workers[i+self.blist_first] and self.place_pop > self.pop:
                self.build_workers[i+self.blist_first] = False
                self.place_pop -= 5
                self.build_list[i].configure(bg=self.bgcolor)
            elif self.place_pop <= self.pop:
                break
        for row in range(10):
            for col in range(10):
                if self.worker_grid[row][col] and self.place_pop > self.pop:
                    self.worker_grid[row][col] = False
                    self.bgrid[row][col].configure(background=self.bgcolor)
                    self.place_pop -= 1
                elif self.place_pop <= self.pop:
                    break
        for row in range(10):
            for col in range(10):
                rsc,mod = self.grid[row][col][2],int(self.grid[row][col][-1])
                for i in range(2):
                    if rsc in mod_remove and mod > 0:
                        mod -= 1
                        del mod_remove[mod_remove.index(rsc)]
                self.grid[row][col] = self.grid[row][col][:-1]+str(mod)
                if self.reveal_grid[row][col]:
                    self.bgrid[row][col].configure(text=self.grid[row][col])
                if mod_remove == []:
                    break
                    
                    
                    
        self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
        
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
        rsc = str(self.grid[row][col])[2]
        mod = int(str(self.grid[row][col])[-1])
        sta = int(str(self.grid[row][col])[0])
        print(rsc,mod,sta)
        if self.reveal_grid[row][col]:
            if self.placing:
                self.placing = False
                if mod + sta < 3 and self.place_pop <= self.pop - 10:
                    if rsc == 'W' and self.build_active[1] < self.buildings[1]:
                        self.grid[row][col] = str(self.grid[row][col])[:8]+str(mod+1)
                        event.widget.configure(text=str(self.grid[row][col]))
                        self.build_active[1] += 1
                        self.place_pop += 10
                        for i in range(len(self.build_all)):
                            if self.build_all[i] == 'Sawmill' and not self.build_workers[i]:
                                self.build_workers[i] = True
                                print(i,self.blist_first)
                                if i >= self.blist_first and i - self.blist_first < 8:
                                    print(i-self.blist_first)
                                    self.build_list[i-self.blist_first].configure(background='lightgray')
                                break
                            
                        self.placing = False
                    elif rsc == 'I' and self.build_active[2] < self.buildings[2]:
                        self.grid[row][col] = str(self.grid[row][col])[:8]+str(mod+1)
                        event.widget.configure(text=str(self.grid[row][col]))
                        self.build_active[2] += 1
                        self.place_pop += 10
                        for i in range(len(self.build_all)):
                            if sulf.build_all[i] == 'Mine' and not self.build_workers[i]:
                                self.build_workers[i] = True
                                if i >= self.blist_first and i - self.blist_first < 8:
                                    self.build_list[i-self.blist_first].configure(background='lightgray')
                                break
                        self.placing = False
                    self.pop_lbl.configure(text='Pop '+str(self.pop)+' ('+str(self.place_pop)+')')
            elif self.removing:
                self.removing = False
                if mod > 0:
                    if rsc == 'W':
                        self.grid[row][col] = str(self.grid[row][col])[:8]+str(mod-1)
                        event.widget.configure(text=str(self.grid[row][col]))
                        self.build_active[1] -= 1
                        self.place_pop -= 10
                        for i in range(len(self.build_all)):
                            if self.build_all[i] == 'Sawmill' and self.build_workers[i]:
                                self.build_workers[i] = False
                                print(i,self.blist_first)
                                if i >= self.blist_first and i - self.blist_first < 8:
                                    print(i-self.blist_first)
                                    self.build_list[i-self.blist_first].configure(background=self.bgcolor)
                                break
                    elif rsc == 'I':
                        self.grid[row][col] = str(self.grid[row][col])[:8]+str(mod-1)
                        event.widget.configure(text=str(self.grid[row][col]))
                        self.build_active[2] -= 1
                        self.place_pop -= 10
                        for i in range(len(self.build_all)):
                            if self.build_all[i] == 'Mine' and self.build_workers[i]:
                                self.build_workers[i] = False
                                print(i,self.blist_first)
                                if i >= self.blist_first and i - self.blist_first < 8:
                                    print(i-self.blist_first)
                                    self.build_list[i-self.blist_first].configure(background=self.bgcolor)
                                break
                            
            elif self.place_pop < self.pop and not self.worker_grid[row][col]:
                self.worker_grid[row][col] = True
                self.place_pop += 1
                self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
                event.widget.configure(background='lightgray')
            elif self.worker_grid[row][col]:
                self.worker_grid[row][col] = False
                self.place_pop -= 1
                self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
                event.widget.configure(background=self.bgcolor)
                
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
        if r_qty > 0 and t_qty <= rsc_qty:
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
            elif trading == 'Gold' and t_qty <= self.gold:
                self.gold = self.gold - t_qty
            if receiving == 'Food':
                self.food_list[-1].append(r_qty)
            elif receiving == 'Wood':
                self.wood = self.wood + r_qty
            elif receiving == 'Iron':
                self.iron = self.iron + r_qty
            else:
                self.gold = self.gold + r_qty
                
    def collect_rsc(self):
        for row in range(10):
            for col in range(10):
                if self.worker_grid[row][col]:
                    rsc_amt = int(str(self.grid[row][col])[0])+int(str(self.grid[row][col])[-1])
                    if str(self.grid[row][col])[2] == 'F':
                        self.food_list[-1].append(rsc_amt)
                    elif str(self.grid[row][col])[2] == 'W':
                        self.wood = self.wood + rsc_amt
                    else:
                        self.iron = self.iron + rsc_amt
                    
    def place(self):
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
            
    def end(self):
        self.wood_c = int(self.wood)
        self.iron_c = int(self.iron)
        self.gold_c = int(self.gold)
        if len(self.food_list) >= self.food_slot:
            del self.food_list[0]
        while len(self.food_list) < self.food_slot:
                self.food_list.append([])
        self.collect_rsc()
        self.trade() #intentionally before food consumption
        self.food = sum(sum(i) for i in self.food_list)
        self.turnend = True
        self.refreshcalc()
        if self.building:
            self.build()
        if self.build_auto_reset:
            self.resetbuild()
        elif self.build_info_cost_1.cget('text') != '':
            self.buildinfo()
        self.turnend = False
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
            
            self.food = self.food - self.pop
        if self.place_pop > self.pop:
            self.remove_workers()
        
        for i in range(self.food):
            if self.food >= 4+i**2:
                self.pop += 1
            
        self.game = True
        if self.pop == 0 and self.turn > 1:
            overscreen = Tk()
            overscreen.title('')
            overscreen.resizable(width=False,height=False)
            gover = Label(overscreen,text='Game Over!',width=20,height=3)
            gover.grid(row=1,column=1,columnspan=2)
            gquit = Button(overscreen,text='Quit',command=lambda:self.closeall([overscreen]))
            gquit.grid(row=2,column=1,sticky='SEWN')
            gload = Button(overscreen,text='Load',command=self.load)
            gload.grid(row=2,column=2,sticky='SEWN')
            self.game = False
        
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
    
root = Tk()
game = Game(root)
root.mainloop()
