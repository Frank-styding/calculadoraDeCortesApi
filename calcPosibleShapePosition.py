def getPointsOfShape(shapes):
    points = []
    for idx,shape in enumerate(shapes):
        for point in shape:
            if len(point) != 3:
                points.append([point[0], point[1],[idx]])
            else:
                points.append([point[0], point[1],point[2]])
    return points;

def checkPoints(points):

    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                if points[i][0] == points[j][0] and points[j][1] == points[i][1]:
                    aux = list(set(points[i][2] + points[j][2]))
                    points[i][2] = [] + aux
                    points[j][2] = [] + aux
                    

    result = [(point[0],point[1]) for point in points if len(point[2]) == 1]
    
    return result

def some(points,pointToFind):
    for point in points:
        if pointToFind[0] == point[0] and pointToFind[1] == point[1]:
            return True
    return False

def findNextPoint(points,path,direction,currentPoint):
    _points = []

    minPoint = None

    for point in points:
        if point[direction] == currentPoint[direction] and point[1 - direction] != currentPoint[1 - direction] and not some(path,point):
            if minPoint == None:
                minPoint = point
            else:
                if abs(point[1 - direction] - currentPoint[1 - direction]) < abs(minPoint[1 - direction] - currentPoint[1 - direction]):
                    minPoint = point

    return minPoint

def orderPoints(points):
    vertical = True
    path = [(0,0)]

    while len(path) <= len(points) :

        currentPoint = path[len(path) - 1]
        direction = 1 if vertical else 0
        nextPoint = findNextPoint(points,path,direction,currentPoint)

        if nextPoint != None:
            path.append(nextPoint)
        else:
            break

        vertical = not vertical
    
    

    return path

def filterNextStartPoints(points):
    _points = []
    for i in range(len(points)):
        
        a = points[i % len(points)]
        b = points[(i+1) % len(points)]

        if a[0] == b[0]:
            _points.append(a)
    
    return _points

def moveShape(shape,pos):
    result = []

    for point in shape:
            result.append((point[0] + pos[0],point[1] + pos[1]))
    
    return result

def intersectLines(a,b,c,d):

    _a = a
    _b = b
    _c = c
    _d = d

    if a[0] == b[0] and c[1] == d[1]:
        
        if a[1] > b[1]:
            _b = a
            _a = b
        
        if c[0] > d[0]:
            _c = d
            _d = c
        
        return _d[0] > _a[0] and _a[0] > _c[0] and _b[1] > _c[1] and _c[1] > _a[1]

    if c[0] == d[0] and a[1] == b[1]:
        
        if c[1] > d[1]:
            _d = c
            _c = d
        
        if a[0] > b[0]:
            _a = b
            _b = a
            
        return _b[0] > _c[0] and _c[0] > _a[0] and _d[1] > _a[1] and _a[1] > _c[1]
    
    if a[1] == b[1] and c[1] == d[1] and a[1] == c[1] : 
        
        if a[0] > b[0]:
            _b = a;
            _a = b;
        
        if c[0] > d[0]:
            _d = c;
            _c = d;
        
        return (_b[0] > _c[0] and _c[0] > _a[0]) or (_b[0] > _d[0] and _d[0] > _a[0]) or (_d[0] > _a[0] and _a[0] > _c[0]) or (_d[0] > _b[0] and _b[0] > _c[0]) or _b[0] == _d[0] or _a[0] == _c[0]
    
    return False

def intersectShapes(shapeA,shapeB):
    global intersectShapes
    intersectsCount = 0

    for i in range(len(shapeA)):
        for j in range(len(shapeB)):
            if intersectLines(shapeA[i % len(shapeA)],shapeA[(i + 1) % len(shapeA)], shapeB[j % len(shapeB)], shapeB[(j + 1) % len(shapeB)]):

                intersectsCount += 1
            if intersectsCount > 1:

                return True

    return False            

def exitsIntersect(shapes):
    for i in range(len(shapes)):
        for j in range(len(shapes)):
            if i == j: continue

            if intersectShapes(shapes[j],shapes[i]):
                return True
    return False

def isInMaxSpace(shapes,width,height):

    points = getPointsOfShape(shapes)

    return len([point for point in points if point[0] <= width and point[1] <= height]) == len(points)

def rectPath (width,height):
    return [
        (0,0),
        (width,0),
        (width,height),
        (0,height)
    ]

def rotateShape(shape):
    return [(point[1],point[0]) for point in shape ]

def calcPosibleShapePosition(shapes,width,height,idx = 0,startPoints = [(0,0)],shapesOnSpace = []):

    if len(startPoints) == 0:
        return []

    if len(shapes) == idx:
        return [shapesOnSpace]

    shape = shapes[idx]

    posibleShapesOnSpace = [ moveShape(shape,startPoint) for startPoint in startPoints ] + [ moveShape(rotateShape(shape),startPoint) for startPoint in startPoints ]
    
    

    for posibleShape in posibleShapesOnSpace:
        

        nextShapes = shapesOnSpace + [posibleShape]

        if not exitsIntersect(nextShapes) and isInMaxSpace(shapes,width,height):
            
            nextStartPoints = filterNextStartPoints(orderPoints(checkPoints(getPointsOfShape(shapes))))

            aux = calcPosibleShapePosition(shapes,width,height,idx + 1,nextStartPoints,nextShapes)

            if len(aux) > 0:
                return aux

    return []

shapes = [
  rectPath(40, 40),
  rectPath(30, 30),
  rectPath(80, 10),
  rectPath(80, 10),
  rectPath(80, 10),
  rectPath(80, 10),
  rectPath(10, 10),
  rectPath(10, 10),
  rectPath(10, 10),
  rectPath(10, 10),
  rectPath(10, 10),

]

print(calcPosibleShapePosition(shapes,300,300))

