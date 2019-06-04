from tkinter import *
from random import randint
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

        for row in range(10):
            for col in range(10):
                self.worker_grid[row].append(False)
                
        for row in self.grid:
            for i in range(10):
                rs,qt = randint(1,3),randint(1,3)
                if rs == 1:
                    rs = 'xFood'
                elif rs == 2:
                    rs = 'xWood'
                else:
                    rs = 'xIron'
                    qt = randint(1,2)
                
                row.append(str(qt)+rs)
        self.turn_lbl = Label(frame,text='Turn: '+str(self.turn))
        self.turn_lbl.grid(row=1,column=1)
        self.gold_lbl = Label(frame,text='Gold: '+str(self.gold))
        self.gold_lbl.grid(row=1,column=2)
        self.pop_lbl = Label(frame,text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
        self.pop_lbl.grid(row=1,column=3,columnspan=2)
        self.food_lbl = Label(frame,text='Food: '+str(self.food))
        self.food_lbl.grid(row=1,column=5,columnspan=2)
        self.wood_lbl = Label(frame,text='Wood: '+str(self.wood))
        self.wood_lbl.grid(row=1,column=7,columnspan=2)
        self.iron_lbl = Label(frame,text='Iron: '+str(self.iron))
        self.iron_lbl.grid(row=1,column=9,columnspan=2)

        self.it = 1
        for row in range(10):
            self.ct = 1
            for col in range(10):
                if self.is_touching([[1,1]],[self.it-1,self.ct-1]):
                    self.bgrid[row].append(Button(frame, text=self.grid[row][col], width=6, height=3))
                    self.reveal_grid[row].append(True)
                    self.reveal_grid2[row].append(True)
                    self.worker_grid[row].append(False)
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
        self.bgcolor = self.end_btn.cget('background')

    def remove_workers(self):
        for row in range(10):
            for col in range(10):
                if self.worker_grid[row][col]:
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
        row = int(row)
        col = (int(col)+9) % 10
        if self.reveal_grid[row][col]:
            if self.placing and not self.worker_grid[row][col]:
                self.placing = False
                self.worker_grid[row][col] = True
                self.place_pop += 1
                event.widget.configure(background='lightgray')
            elif self.removing and self.worker_grid[row][col]:
                self.removing = False
                self.worker_grid[row][col] = False
                self.place_pop -= 1
                event.widget.configure(background=self.bgcolor)

    def end(self):
        self.collect_rsc()
        if self.turn > 5:
            death = float(0.01*randint(65,90))
            self.pop = int(self.pop * death)
        if self.food < self.pop:
            self.pop = self.food
            self.food = 0
            for i in self.food_list:
                i = 0
        else:
            print(self.food_list)
            consumption = self.food - self.pop
            for i in self.food_list:
                if consumption >= i:
                    consumption = consumption - i
                    i = 0
                else:
                    i = i - consumption
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
            self.pop_lbl.configure(text='Pop: '+str(self.pop)+' ('+str(self.place_pop)+')')
            self.food_lbl.configure(text='Food: '+str(self.food))
            self.wood_lbl.configure(text='Wood: '+str(self.wood))
            self.iron_lbl.configure(text='Iron: '+str(self.iron))
            self.turn += 1
            self.turn_lbl.configure(text='Turn: '+str(self.turn))

            for row in range(10):
                for col in range(10):
                    if not self.reveal_grid[row][col]:
                        reveal = False
                        for row_ in range(-1,2):
                            for col_ in range(-1,2):
                                try:
                                    if self.worker_grid[row+row_][col+col_] and [row_,col_] != [0,0] and randint(1,2) == 1:
                                        reveal = True
                                except:
                                    pass
                                    

                        if reveal:
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
                        for i in self.food_list:
                            print(i)
                            i = sum(i)
                        if len(self.food_list) > 3:
                            del self.food_list[0]
                        food_halflist = self.food_list[:]
                        ###FIX###
##                        for i in food_halflist:
##                            i = sum(i)
##                            print(type(i))
##                        print(food_halflist)
##                        self.food = sum(food_halflist)
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
