import tkinter
import tkinter.messagebox
import tkinter.font

import shapely.geometry.polygon
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
from queue import PriorityQueue
import pdb


def motion(event):
    x, y = event.x, event.y
    print(x, y)


class Graph:

    def __init__(self, vertices):
        self.N = vertices
        self.graph = []
        for i in range(self.N):
            self.graph.append([])

    def addEdge(self, u, v, w):
        self.graph[u].append([v, w])
        self.graph[v].append([u, w])

    def printGraph(self):
        f = open("graph.txt", "w")
        for i in range(self.N):
            f.writelines(str(i) + "\n")
            for edge in self.graph[i]:
                f.writelines(str(edge) + "\n")
        f.close()

    def Dijkstra(self, start, end):
        dist = [1e9] * self.N
        Trace = [-1] * self.N
        dist[start] = 0
        Trace[start] = start
        pq = PriorityQueue()
        pq.put([0, start])
        while not pq.empty():
            [d, u] = pq.get()
            if dist[u] < -d:
                continue
            for edge in self.graph[u]:
                [v, w] = edge
                if dist[v] > dist[u] + w:
                    Trace[v] = u
                    dist[v] = dist[u] + w
                    pq.put([-dist[v], v])
        E = end
        path = [end]
        while end != Trace[end]:
            end = Trace[end]
            path.append(end)
        path.reverse()
        return [dist[E], path]


class GUI:

    def __init__(self):
        # Khai bao bien
        myFont = 12
        self.current_input = []
        self.current_output = []
        self.current_input_coordinate = []
        self.current_output_coordinate = []
        self.Input_Line_List = []
        self.Input_Line_Data = []
        self.Output_Line_List = []
        self.Output_Line_Data = []
        self.Direct = []
        self.Shortest_Path = []
        self.appear = False
        self.Find_Appear = False
        # Khai bao UI
        self.main_window = tkinter.Tk()
        self.top_frame = tkinter.Frame(self.main_window)
        self.mid_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)

        self.Map = tkinter.Button(self.top_frame, text="Map 1", command=self.Map_1, padx=40, pady=10, font=myFont)
        self.Map2 = tkinter.Button(self.top_frame, text="Map 2", command=self.Map_2, padx=40, pady=10, font=myFont)
        self.Find = tkinter.Button(self.top_frame, text="Find", command=self.Find_Func, padx=40, pady=10,
                                   font=myFont)
        self.Visible = tkinter.Button(self.top_frame, text="Visible", command=self.Visible_Func, padx=40, pady=10,
                                      font=myFont)
        self.value = tkinter.StringVar()
        self.ResultDes = tkinter.Label(self.bottom_frame, text="Shortest Path: ", font=myFont)
        self.Result = tkinter.Label(self.bottom_frame, textvariable=self.value, font=myFont)
        self.canvas = tkinter.Canvas(self.mid_frame, width=1096, height=588, bg="black")
        self.Map.pack(side="left")
        self.Map2.pack(side="left")
        self.Find.pack(side="left")
        self.Visible.pack(side="left")
        self.Find.pack(side="left")
        self.canvas.pack()
        self.ResultDes.pack(side="left")
        self.Result.pack(side="left")
        # self.main_window.bind('<Motion>', motion)
        self.main_window.bind('<Button-1>', self.pressed1)
        self.main_window.bind('<Button-3>', self.pressed3)

        # Khai bao bien Map
        self.shape = []
        self.Line_List = []
        self.p = []
        self.polygon = Polygon([])
        self.polygon_data = []
        self.N = 0
        self.G = Graph(0)
        self.Line_Data = []
        # Frame Pack
        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()


        tkinter.mainloop()

    def Map_1(self):
        self.Clear()
        with open("map1.txt") as file:
            shape_list = str(file.readline()).split()
            for string in shape_list:
                self.shape.append(int(string))
        self.create_map()

    def Map_2(self):
        self.Clear()
        with open("map2.txt") as file:
            shape_list = str(file.readline()).split()
            for string in shape_list:
                self.shape.append(int(string))
        self.create_map()

    def create_map(self):
        for i in range(0, len(self.shape) // 2):
            self.p.append([self.shape[i * 2], self.shape[i * 2 + 1]])
        self.polygon_data = self.canvas.create_polygon(self.shape, fill="red")
        self.polygon = Polygon(self.p)
        for i in range(1, len(self.p)):
            for j in range(i+1):
                if not LineString([self.p[i], self.p[j]]).crosses(self.polygon):
                    midpoint = Point((self.p[i][0] + self.p[j][0]) / 2, (self.p[i][1] + self.p[j][1]) / 2)
                    if self.polygon.contains(midpoint):
                        self.Line_List.append([j, i])
        for i in range(len(self.p) - 1):
            self.Line_List.append([i, i + 1])
        self.N = len(self.p)
        self.G = Graph(self.N + 2)
        for line in self.Line_List:
            self.G.addEdge(line[0], line[1], ((self.p[line[0]][0] - self.p[line[1]][0]) ** 2 + (self.p[line[0]][1] - self.p[line[1]][1]) ** 2) ** (1 / 2))

    def Find_Func(self):
        if not self.shape:
            tkinter.messagebox.showinfo('Response', "Please choose a map!")
            return
        if not self.current_input or not self.current_output:
            tkinter.messagebox.showinfo('Response', "Please type in two valid points!")
            return
        self.Find_Appear = not self.Find_Appear
        self.find_shortest(self.N, self.N + 1)

    def Visible_Func(self):
        self.appear = not self.appear
        if self.appear:
            for line in self.Line_List:
                self.Line_Data.append(self.canvas.create_line(self.p[line[0]], self.p[line[1]], fill="white"))
            for line in self.Input_Line_List:
                self.Input_Line_Data.append(
                    self.canvas.create_line(self.current_input_coordinate, self.p[line], fill="white"))
            for line in self.Output_Line_List:
                self.Output_Line_Data.append(
                    self.canvas.create_line(self.current_output_coordinate, self.p[line], fill="white"))
            if self.current_input and self.current_output and not LineString(
                    [self.current_input_coordinate, self.current_output_coordinate]).crosses(self.polygon):
                self.Direct_Connect()
        else:
            for line in self.Line_Data:
                self.canvas.delete(line)
            for line in self.Input_Line_Data:
                self.canvas.delete(line)
            for line in self.Output_Line_Data:
                self.canvas.delete(line)
            if self.current_input and self.current_output and not LineString(
                    [self.current_input_coordinate, self.current_output_coordinate]).crosses(self.polygon):
                self.Direct_Connect()
            self.Line_Data.clear()
            self.Input_Line_Data.clear()
            self.Output_Line_Data.clear()

    def connect(self, lists, data, idx):
        data.clear()
        lists.clear()
        if idx == self.N:
            point = self.current_input_coordinate
        else:
            point = self.current_output_coordinate
        for i in range(len(self.p)):
            path = LineString([self.p[i], point])
            if not path.crosses(self.polygon):
                lists.append(i)
                self.G.addEdge(idx, i, ((point[0] - self.p[i][0]) ** 2 + (point[1] - self.p[i][1]) ** 2) ** (1 / 2))
                if self.appear:
                    data.append(self.canvas.create_line(self.p[i][0], self.p[i][1], point[0], point[1], fill="white"))

    def Direct_Connect(self):
        for line in self.Direct:
            self.canvas.delete(line)
        self.Direct.clear()
        if self.current_input and self.current_output:
            path = LineString([self.current_input_coordinate, self.current_output_coordinate])
            if not path.crosses(self.polygon) and self.appear:
                self.Direct.append(
                    self.canvas.create_line(self.current_input_coordinate[0], self.current_input_coordinate[1],
                                            self.current_output_coordinate[0],
                                            self.current_output_coordinate[1],
                                            fill="white"))

    def pressed1(self, event):
        point = Point(event.x, event.y)
        if self.polygon.contains(point) and str(event.widget) == ".!frame2.!canvas":
            if self.current_input:
                for line in self.Input_Line_Data:
                    self.canvas.delete(line)
                self.canvas.delete(self.current_input)
                for edge in self.G.graph[self.N]:
                    [v, w] = edge
                    self.G.graph[v].remove([self.N, w])
                self.G.graph[self.N].clear()
            self.start = [event.x, event.y]
            self.current_input = self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5,
                                                         fill="blue")
            self.current_input_coordinate = [event.x, event.y]
            self.connect(self.Input_Line_List, self.Input_Line_Data, self.N)
            self.find_shortest(self.N, self.N+1)

    def pressed3(self, event):
        point = Point(event.x, event.y)
        if self.polygon.contains(point) and str(event.widget) == ".!frame2.!canvas":
            if self.current_output:
                for line in self.Output_Line_Data:
                    self.canvas.delete(line)
                self.canvas.delete(self.current_output)
                for edge in self.G.graph[self.N + 1]:
                    [v, w] = edge
                    self.G.graph[v].remove([self.N + 1, w])
                self.G.graph[self.N+1].clear()
            self.start = [event.x, event.y]
            self.current_output = self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5,
                                                          fill="yellow")
            self.current_output_coordinate = [event.x, event.y]
            self.connect(self.Output_Line_List, self.Output_Line_Data, self.N + 1)
            self.find_shortest(self.N, self.N + 1)

    def find_shortest(self, start, end):
        if not self.current_input or not self.current_output:
            return

        for line in self.Shortest_Path:
            self.canvas.delete(line)
        self.Shortest_Path.clear()

        if not LineString([self.current_input_coordinate, self.current_output_coordinate]).crosses(self.polygon):
            [res, path] = [((self.current_input_coordinate[0] - self.current_output_coordinate[0]) ** 2 +
                    (self.current_input_coordinate[1] - self.current_output_coordinate[1]) ** 2) ** (1/2),
                    [self.N, self.N+1]]
        else:
            [res, path] = self.G.Dijkstra(start, end)
        self.value.set(str(res) + " pixels")
        if self.Find_Appear:
            for i in range(len(path) - 1):
                if i == 0 and i + 1 == len(path) - 1:
                    self.Shortest_Path.append(
                        self.canvas.create_line(self.current_input_coordinate, self.current_output_coordinate, fill="green", width=5))
                elif i == 0:
                    self.Shortest_Path.append(
                        self.canvas.create_line(self.current_input_coordinate, self.p[path[i + 1]], fill="green", width=5))
                elif i == len(path) - 2:
                    self.Shortest_Path.append(
                        self.canvas.create_line(self.p[path[i]], self.current_output_coordinate, fill="green", width=5))
                else:
                    self.Shortest_Path.append(
                        self.canvas.create_line(self.p[path[i]], self.p[path[i + 1]], fill="green", width=5))

    def Clear(self):
        self.shape.clear()
        self.Line_List.clear()
        self.polygon = Polygon(self.shape)
        self.canvas.delete(self.polygon_data)
        self.p.clear()
        self.N = 0
        self.G = Graph(0)
        for line in self.Line_Data:
            self.canvas.delete(line)
        for line in self.Direct:
            self.canvas.delete(line)
        self.Direct.clear()
        for line in self.Shortest_Path:
            self.canvas.delete(line)
        self.canvas.delete(self.current_input)
        self.canvas.delete(self.current_output)
        for line in self.Input_Line_Data:
            self.canvas.delete(line)
        for line in self.Output_Line_Data:
            self.canvas.delete(line)

        self.Input_Line_Data.clear()
        self.Output_Line_Data.clear()
        self.Input_Line_List.clear()
        self.Output_Line_List.clear()
        self.Shortest_Path.clear()
        self.appear = False
        self.Find_Appear = False


my_gui = GUI()
