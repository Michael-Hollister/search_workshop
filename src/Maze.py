import random as braisedRNJesus


class Maze:
    __width = None
    __height = None
    __walls = []
    __cells = []
    __wallsLowered = 0

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        wallOrder = []
        for i in range(width * height * 2):
            self.__walls.append(False)
            wallOrder.append(i)
            if (i < width * height):
                self.__cells.append(-1)

        temp = 0
        # generate the order in which the walls will be checked
        for i in range(width * height - 1, 1, -1):
            j = braisedRNJesus.randint(0, i)
            temp = wallOrder[j]
            wallOrder[j] = wallOrder[i]
            wallOrder[i] = temp

        # width*height cells, 2 walls per cell, on the bottom and right
        # wall id'd in ascending order from left to right, wall 1 is the first
        # vertical wall, wall width*1 is the first horizontal wall

        for wall in wallOrder:
            if ((self.__vertical(wall))
                    and ((wall + 1) % self.__width !=
                         0)):  # second false when cell is rightmost
                adj = self.__vWallAdjCells(wall)
                cellL = self.__coordToCell(adj[0])
                cellR = self.__coordToCell(adj[1])
                self.__walls[wall] = self.__mergeD(cellL, cellR)  # will
            elif (not self.__vertical(wall)
                  and ((wall // self.__width) // 2 != (self.__height - 1)
                       )):  # second is false when wall is bottom most
                adj = self.__hWallAdjCells(wall)
                cellU = self.__coordToCell(adj[0])
                cellD = self.__coordToCell(adj[1])
                self.__walls[wall] = self.__mergeD(cellU, cellD)

    # // - floor division
    # returns true if wall is vertical, false if horizontal
    def __vertical(self, wallNum):
        return (wallNum // self.__width) % 2 == 0

    # vert wall -> adj cells
    # left cell x = wallNum - left cell y * 2 * width
    # left cell y = wallNum // (2*width)
    # right cell x = left cell
    def __vWallAdjCells(self, wallNum):
        y = wallNum // (2 * self.__width)
        leftX = wallNum - y * 2 * self.__width
        rightX = leftX + 1
        return [(leftX, y), (rightX, y)]

    # horiz wall -> adj cells
    # col = wallNum % 4
    # up y = (wallNum // 4 // 2)
    # down y = up y + 1
    def __hWallAdjCells(self, wallNum):
        x = wallNum % self.__width
        topY = (wallNum // self.__width) // 2
        botY = topY + 1
        return [(x, topY), (x, botY)]

    def __coordToCell(self, coords):
        return coords[1] * self.__width + coords[0]

    # cell wall up = (y-1)*2*width + x + width (y!=0)
    def __UpPassage(self, coords):
        return self.__walls((coords[1] - 1) * 2 * self.__width + coords[0] +
                            self.__width) and (coords[1] != 0)

    # cell wall down = cell wall up + 2 * width (y != height-1)
    def __DownPassage(self, coords):
        return self.__walls((coords[1]) * 2 * self.__width + coords[0] +
                            self.__width) and (coords[1] != self.__height - 1)

    # cell wall left = cell wall up + width - 1 (x != 0)
    def __LeftPassage(self, coords):
        return self.__walls(coords[1] * 2 * self.__width + coords[0] - 1) and (
            coords[0] != 0)

    # cell wall right = cell wall left + 1    (x !- width-1)
    def __RightPassage(self, coords):
        return self.__walls(coords[1] * 2 * self.__width + coords[0]) and (
            coords[0] != self.__width - 1)

    def __mergeD(self, cell1, cell2):
        # returns true if they merged
        retVal = True
        tracer = cell1
        mod = []
        while (self.__cells[tracer] != -1):
            mod.append(tracer)
            tracer = self.__cells[tracer]
        root1 = tracer
        tracer = cell2
        while (self.__cells[tracer] != -1):
            mod.append(tracer)
            tracer = self.__cells[tracer]
        root2 = tracer
        if (root1 == root2):
            retVal = False

        else:
            self.__cells[root2] = root1
        for c in mod:
            self.__cells[c] = root1

        if (retVal):
            self.__wallsLowered += 1
        return retVal

    def getSuccessorFunc(self):
        def successors(coords):
            s = []
            if (self.__UpPassage(coords)):
                s.append((coords[0], coords[1] - 1))
            if (self.__DownPassage(coords)):
                s.append((coords[0], coords[1] + 1))
            if (self.__LeftPassage(coords)):
                s.append((coords[0] - 1, coords[1]))
            if (self.__RightPassage(coords)):
                s.append((coords[0] + 1, coords[1]))
            return s

        return successors

    def getTerminalFunc(self):
        def terminalTest(coords):
            return (coords[0] == self.__width - 1) and (
                coords[1] == self.__height - 1)

        return terminalTest

    def print(self, path=set()):
        wall_str = "[]"
        space_str = "  "
        path_str = "::"
        for i in range(self.__height * (self.__width - 1)):
            if ((i // self.__width) % 2 == 0):
                coords = (i // self.__width, i % self.__height)
                if coords in path:
                    print(path_str, end="")
                else:
                    print(
                        space_str, end=""
                    )  # print space for a cell - can't be a wall here
            if (self.__walls[i]):
                print(space_str, end="")  # print space for a lack of wall here
            else:
                print(wall_str, end="")  # print x for wall here
            if ((i // self.__width) % 2 == 1):
                print(wall_str, end="")  # print x - grid vertex wall
            if ((i + 1) % self.__width == 0):
                coords = (i // self.__width, i % self.__height)
                if coords in path:
                    print(path_str, end="")
                else:
                    print("")
        for i in range(self.__width * 2):
            print(wall_str, end="")
        print()

    def altPrint(self):
        for i in range(self.__height * self.__width):
            c = "x"
            if (self.__walls[i]):
                c = "0"
            print(c, end="")
            if ((i + 1) % self.__width == 0):
                print("")

    def binPrint(self):
        for i in range(self.__height * self.__width):
            if (self.__walls[i]):
                print("1", end="")
            else:
                print("0", end="")
            if ((i + 1) % self.__width == 0):
                print("")

    def __find(self, cell):
        if (self.__cells[cell] == -1):
            return cell
        else:
            return self.__find(self.__cells[cell])

    def allUnioned(self):
        c = self.__find(0)
        for i in range(len(self.__cells)):
            if (c != self.__find(i)):
                return False
        return True


if __name__ == '__main__':
    m = Maze(30, 30)
    path = set()
    path.add((0, 0))
    m.print(path=path)