
from random import randrange
from tkinter import *
from Ship import *

import _thread

class Application(Frame):
    width = 800
    height = 400
    bg = "white"
    indent = 2
    gauge = 32
    offset_y = 40
    offset_x_user = 30
    offset_x_comp = 430
    fleet_comp = []
    fleet_user = []

    def createCanvas(self):
        self.canv = Canvas(self)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()
        self.canv.bind("<Button-1>",self.userPlay)
        self.canv.bind("<X>",self.new_game)

    def new_game(self):
        self.canv.delete('all')
        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "my_"+str(i)+"_"+str(j))

        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "nmy_"+str(i)+"_"+str(j),fill="gray")

        #генерация кораблей противника
        _thread.start_new_thread(self.createShips,("nmy",))
        #self.createShips("nmy")
        #генерация своих кораблей
        self.createShips("my")

    def createShips(self, prefix):
        count_ships = 0
        while count_ships < 10:
            fleet_array = []
            count_ships = 0
            fleet_ships = []
            for length in reversed(range(1,5)):
                for i in range(5-length):
                    tries = 0
                    while 1:
                        tries += 1
                        if tries >= 50:
                            break
                        #Пока рандомное расположение
                        ship_point = prefix+"_"+str(randrange(10))+"_"+str(randrange(10))
                        orientation = randrange(2)
                        new_ship = Ship(length,orientation,ship_point)
                        if new_ship.ship_correct == 1 and len(list(set(fleet_array) & set(new_ship.around_map+new_ship.coord_map))) == 0:
                            fleet_array += new_ship.around_map + new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        if prefix == "nmy":
            self.fleet_comp = fleet_ships
        else:
            self.fleet_user = fleet_ships
            self.paintShips(fleet_ships)

    def paintShips(self,fleet_ships):
        for obj in fleet_ships:
            for point in obj.coord_map:
                self.canv.itemconfig(point,fill="gray")

    def paintCross(self,xn,yn,tag):
        xk = xn + self.gauge
        yk = yn + self.gauge
        self.canv.itemconfig(tag,fill="white")
        self.canv.create_line(xn+2,yn+2,xk-2,yk-2,width="3")
        self.canv.create_line(xk-2,yn+2,xn+2,yk-2,width="3")

    def paintMiss(self,point):
        new_str = int(point.split("_")[1])
        new_stlb = int(point.split("_")[2])
        if point.split("_")[0] == "nmy":
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_comp
        else:
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_user
        yn = new_str*self.gauge + (new_str+1)*self.indent + self.offset_y
        self.canv.itemconfig(point,fill="white")
        self.canv.create_oval(xn+13,yn+13,xn+17,yn+17,fill="gray")

    #метод проверки финиша
    def GO(self,type):
        status = 0
        if type == "user":
            for ship in self.fleet_comp:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status 
    #метод для игры пользователя
    def userPlay(self,e):
        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if e.x >= xn and e.x <= xk and e.y >= yn and e.y <= yk:
                    #проверить попали ли мы в корабль
                    hit_status = 0
                    for obj in self.fleet_comp:
                        if "nmy_"+str(i)+"_"+str(j) in obj.coord_map:
                            hit_status = 1
                            self.paintCross(xn,yn,"nmy_"+str(i)+"_"+str(j))
                            if obj.shoot("nmy_"+str(i)+"_"+str(j)) == 2:
                                obj.death = 1
                                for point in obj.around_map:
                                    self.paintMiss(point)
                            break

                    if hit_status == 0:
                        self.paintMiss("nmy_"+str(i)+"_"+str(j))
                        #передать управление компьютеру
                        #if self.GO("user") < 10:
                            #Здесь должна быть нейронка
                       # else:
                          #  showinfo("Seabattle", "You aren't idiot!")
                    break

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createCanvas()
        self.new_game()


root = Tk()
root.title = "Seabattle"
root.geometry("800x500+100+100")
app = Application(master=root)
app.mainloop()