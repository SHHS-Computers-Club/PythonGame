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
        self.reveal_grid = [[],[],[],[],[],[],[],[],[],[]]
        self.worker_grid = [[],[],[],[],[],[],[],[],[],[]]
        self.gold = 0
        self.pop = 1
        self.pop_lbl = ''
        self.placing = False
        self.removing = False
        self.startxy = [1,1]
        
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
        self.bgrid = []
        self.gold_lbl = Label(frame,text='Gold: '+str(self.gold))
        self.gold_lbl.grid(row=1,column=1,columnspan=3)
        self.pop_lbl = Label(frame,text='Population: '+str(self.pop))
        self.pop_lbl.grid(row=1,column=4,columnspan=3)
        print(self.gold_lbl.grid_info())
        self.it = 1
        for item in self.grid:
            self.ct = 1
            for i in item:
                if self.is_touching([[1,1]],[self.it-1,self.ct-1]):
                    self.bgrid.append(Button(frame, text=i, width=6, height=3))
                    self.reveal_grid[self.grid.index(item)].append(True)
                    self.worker_grid[self.grid.index(item)].append(False)
                else:
                    self.bgrid.append(Button(frame, text='',width=6, height=3))
                    self.reveal_grid[self.grid.index(item)].append(False)
                    self.reveal_grid[self.grid.index(item)].append(False)
                self.bgrid[len(self.bgrid)-1].grid(row=self.it+1,column=self.ct,sticky='NSEW')
                self.bgrid[len(self.bgrid)-1].bind("<Button-1>",self.get_rsc)
                self.ct += 1
            self.it += 1
        self.placer_btn = Button(frame, text='Place worker', width=14, height=3,command=self.place)
        self.placer_btn.grid(column=1,row=12,columnspan=2)
        self.remove_btn = Button(frame, text='Remove worker', width=14, height=3,command=self.remove)
        self.remove_btn.grid(column=3,row=12,columnspan=2)
        self.end_btn = Button(frame, text='End Turn', width=14, height=3, command=self.end)
        self.end_btn.grid(column=5,row=12,columnspan=2)

    def is_touching(self,points,test_coord): #points should be a list
        return_tf = False
        for pt in points:
            if abs(test_coord[0]-pt[0]) < 2 and abs(test_coord[1]-pt[1]) < 2:
                return_tf = True
        return return_tf

    def get_rsc(self,event):
        print(event.widget)
        row,col = str(event.widget)[-2],str(event.widget)[-1]
        if col == 'n':
            col = 1
        if row == 'n' or row == 'o':
            row = 0
        row = int(row)
        col = (int(col)+9) % 10
        if self.reveal_grid[row][col]:
            print(row,col)
            print(self.grid[row][col])
            if self.placing and not self.worker_grid[row][col]:
                self.worker_grid[row][col] = True
            elif self.removing and self.worker_grid[row][col]:
                self.worker_grid[row][col] = False

    def end(self):
        self.collect_rsc()
    
    def collect_rsc(self):
        pass
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
root = Tk()
game = Game(root)
root.mainloop()
