"""Makes a TRIANGULAR grid of revolution from any grid. Needs angular size as input 'b'. Needs a Profile Curve to manipulate the radius. The thickness of the grid will be perpendicular to the tangent of the Profile Curve.
    Inputs:
        C: Grid to transform
        pC: Profile curve (have to be a planar curve on the 'xy' plane, the axis is the axis 'y')
        r: The radius of the vault
        l: The length of the vault
        n: Angle of the apex of the initial isosceles triangle
        b: 3rd angular size (Beta)
        T: Vault Type (0 = cylinrical, 1 = prism)
        S: Grid Settings
    Output:
        C: The Curves of the Dome
        D: Curveture vectors of the Profile Curve"""

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System as sys
import Rhino as rh
import rhinoscriptsyntax as rs
import Grasshopper.Kernel.Data.GH_Path as ghpath
import Grasshopper.DataTree as datatree
import math

__author__ = "Reka Sarkozi"
__version__ = "2018.06.22"

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Kitsune Triangular Revolution Grid 2", "Kitsune TriRevGrd 2", """Makes a TRIANGULAR grid of revolution from any grid. Needs angular size as input 'b'. Needs a Profile Curve to manipulate the radius. The thickness of the grid will be perpendicular to the tangent of the Profile Curve.""", "Extra", "Kitsune")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("6505ec5c-62ef-44c2-9404-514ca647133b")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "C", "C", "Grid to transform")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "pC", "pC", "Profile curve (have to be a planar curve on the 'xy' plane, the axis is the axis 'y')")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "r", "r", "The radius of the vault")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "l", "l", "The length of the vault")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "n", "n", "Angle of the apex of the initial isosceles triangle")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "b", "b", "3rd angular size (Beta)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "T", "T", "Vault Type (0 = cylinrical, 1 = prism)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "S", "S", "Grid Settings")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "C", "C", "The Curves of the Dome")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "D", "D", "Curveture vectors of the Profile Curve")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        p7 = self.marshal.GetInput(DA, 7)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMdSURBVEhLzdXXa1RREIDxtSPWxN5bYuxir9g1lmCJXRF7x4oFa2LB3kHsHXsX7Aii6IsK6oOCIj6I4n+h33c9Ky6uRvLkwA83yd5zZubMPcb+hyiIFhiNxZiAGRiPziiMfEc/HMM7PMBMnMBR7MIzXIW/L4R/jiY4hDeYjA1YhjaYgoUYHv7dhq24CyvKM3rAzO7hAtbCRQfDTffCFrn4aizCYdzCI8zBHyMFJ3EJOXiCt3Cz0ziAG7BFtu4hXuMp3PAgrqMekoYH6UJHsBFmb+mfYFW5cBOTMONvmAur2IPjcON5SBr78QIrYasmYSjc0Gru4zms4ituYhDGoDkcgLO4hgJIiLJ4id0wA7O136Ng9o9h1p9xBq9gG3vD30/FKaxC0jb5xfcw6/PwwCx/CczM7O/AanbCCbPiDjiHzdiEy7CFVpYQZm17/JIjOQ1Oz3b4sGfzEZZvArZqH2znQDiqmZgPq7W6hNiCD5iNWYEV+LAvXEmMhAfaCg0xAB3hcNiaBdgBz8gkvAWiKAIP5zbWwy+moinqhM91f/lcHW5QAi1hv13Mt9tzuwJbWRlR1MQXLA2fnedOcLbN0uyHoBmMnuiGUnAIrLQ9vKscFtt2Eb0QxTBYgRn7oGPnF13ch9vBzf2914Fv63K0xViMg3dRFmyfVTkUP89hTeCrXwnOdP2gKww3cQHDRLw6jAZwkjKQDs/Mv3mmnkcU0+H168XWF2mBD9aAi7iAl6B9bRx+9hz8W7yFFWB7fDk9Rz9H4eXlePlF++7Ielt6DdtnWxXvf3c0+vExWtQp8pAdZROaCBMwaUc9Cvvqi9EHludDteFE2Ro39U3tAjf3YRdbAau2Gs/FZDxs17GKeBujsCT/UBUelA/5s2H2VmSFvhM+7P9kDoTnURRubqIVYTIjkPC/XXE4fi7krFtRFViuh+1klId997PD4Jl4RmZdDG6cDc+xNH4Lb8DWMMt1cBHvKG9Ww4ydFL/XH7VgYrbQkTVrn88znGkX8iycc/vsg/bfn83c98Iq3dyEfNPzHfa4HKyoWvi3DGzLXyIW+w41c6SGJWsobwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, C, pC, r, l, n, b, T, S):
        
        
        
        grid = C
        if pC != None:
            profileCrv = rs.coercecurve (pC)
        
        rad = r
        if rad == None:
            rad = 10
        
        angle = n
        if angle == None:
            angle = 60
        
        length = l
        if length == None:
            length = 10
        
        beta = b
        if beta == None:
            beta = 90
        
        type = T
        if type == None:
            type = 0
        
        set = S
        
        # default values of Dome Settings
        
        thick = 0                   # thickness of the dome
        gap = 0                     # gap angle (lambda)
        CurveOrLine = 0             # division of the lines //line:0, curve:1
        origo = rs.AddPoint (0,0,0) # origo of the sturcture
        axis = 2                    # axis of the structure // x:0, y:1, z:2
        
        # overwrite Dome Settings from input
        
        if set.DataCount != 0:
            thick = set.Branch(0)[0]
            if thick == None:
                thick = 0
            
            gap = set.Branch(1)[0]
            if gap == None:
                gap = 0
            
            CurveOrLine = set.Branch(2)[0]
            if CurveOrLine == None:
                CurveOrLine = 0
            
            origo = set.Branch(3)[0]
            origo = rs.coerce3dpoint (origo)
            if origo == None:
                origo = rs.AddPoint (0,0,0)
                origo = rs.coerce3dpoint (origo)
            
            axis = set.Branch(4)[0]
            if axis == None:
                axis = 2
        
        gridNum = 0
        for i in range (grid.BranchCount):
            gridBranch = grid.Branch (i)
            gridNum = gridNum + len (gridBranch)
        
        print "a racs " + str (gridNum) + "elembol all"
        print "a sugar: " + str (rad)
        print "a hossz: " + str (length)
        print "a beta szog: " + str (beta)
        
        if type == 0:
            racstip = "CYLINDRICAL"
        elif type == 1:
            racstip = "PRISM"
        else:
            racstip = "nem ismert"
        
        print "a keszulo racs " + racstip + " tipusu"
        
        print "a racs vastagsaga: " + str (thick)
        print "a lyuk szoge: " + str (gap)
        
        if CurveOrLine == 0:
            IsItLine = "EGYENESEK"
        elif CurveOrLine == 1:
            IsItLine = "IVESEK"
        else:
            IsItLine = "nem ismertek"
        
        print "a keszulo racs rudai " + IsItLine
        print "a keszulo racs origoja: " + str (origo)
        
        if axis == 0:
            AxisTyp = "az X tengely"
        elif axis == 1:
            AxisTyp = "az Y tengely"
        elif axis == 2:
            AxisTyp = "a Z tengely"
        else:
            AxisTyp = "nem ismert"
        print "a keszulo racs tengelye " + AxisTyp
        
        
        def TreeToList (treeIn):
            listOut = []
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    listOut.append (elem)
            return listOut
        
        def GridType ():
            # check curve/line division
            
            if CurveOrLine == 0:
                div = 1
                #Grid of lines!
            else:
                div = 10
                #Grid of curves!
            return div
        
        def GridCornerSmall (treeIn):
            
            listIn = TreeToList (treeIn)
            
            cor_x = []
            cor_y = []
            cor_z = []
            
            for i in listIn:
                cX = i.X
                cY = i.Y
                cZ = i.Z
                cor_x.append (cX)
                cor_y.append (cY)
                cor_z.append (cZ)
            
            cor_x.sort ()
            cor_y.sort ()
            cor_z.sort ()
            
            corx_min = (cor_x [0])
            cory_min = (cor_y [0])
            corz_min = (cor_z [0])
            
            cor_x.reverse ()
            cor_y.reverse ()
            cor_z.reverse ()
            
            corx_max = (cor_x [0])
            cory_max = (cor_y [0])
            corz_max = (cor_z [0])
            
            SmallCorner = rs.AddPoint (corx_min, cory_min, corz_min)
            SmallCorner = rs.coerce3dpoint (SmallCorner)
            BigCorner = rs.AddPoint (corx_max, cory_max, corz_max)
            BigCorner = rs.coerce3dpoint (BigCorner)
            
            return (SmallCorner)
        
        def GridCornerBig (treeIn):
            
            listIn = TreeToList (treeIn)
            
            cor_x = []
            cor_y = []
            cor_z = []
            
            for i in listIn:
                cX = i.X
                cY = i.Y
                cZ = i.Z
                cor_x.append (cX)
                cor_y.append (cY)
                cor_z.append (cZ)
            
            cor_x.sort ()
            cor_y.sort ()
            cor_z.sort ()
            
            corx_min = (cor_x [0])
            cory_min = (cor_y [0])
            corz_min = (cor_z [0])
            
            cor_x.reverse ()
            cor_y.reverse ()
            cor_z.reverse ()
            
            corx_max = (cor_x [0])
            cory_max = (cor_y [0])
            corz_max = (cor_z [0])
            
            SmallCorner = rs.AddPoint (corx_min, cory_min, corz_min)
            SmallCorner = rs.coerce3dpoint (SmallCorner)
            BigCorner = rs.AddPoint (corx_max, cory_max, corz_max)
            BigCorner = rs.coerce3dpoint (BigCorner)
            
            return (BigCorner)
        
        def DivideCurves (curves, NumberOfPoints, treeOut):
            # gorbe felosztasa, pontok listaba es faba rendezese
            
            
            pathNum=0
            
            for i in range (curves.BranchCount):
                treeBranch = curves.Branch (i)
                treePath = curves.Path (i)
                
                for j in range (len (treeBranch)):
                    PointsPerCurve= rs.DivideCurve (treeBranch [j], NumberOfPoints, True, True)
                    NumOfPtCrv = len (PointsPerCurve)
                    path = ghpath (treePath.AppendElement (j))
                    loopNum = 0
                    
                    while (loopNum < NumOfPtCrv):
                        treeOut.Add(PointsPerCurve[loopNum], path)
                        loopNum = loopNum+1
        
        def MoveGridToOrigo (treeIn, treeOut):
            
            RacsOrigo = GridCornerSmall (treeIn)
            RacsOrigo = rs.coerce3dpoint (RacsOrigo)
            
            ORIGO = rs.AddPoint (0,0,0)
            ORIGO = rs.coerce3dpoint (ORIGO)
            
            # A kiindulasi racs eltolasa
            
            Eltolas = ORIGO - RacsOrigo
            Eltolas = rs.coerce3dpoint (Eltolas)
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    point = treeBranch[j] + Eltolas
                    point = rs.coerce3dpoint (point)
                    treeOut.Add (point, treePath)
        
        def CupolaCollar (treeIn, profilePointsIn, profileVectorsIn, treeOut, ratioOut, profilePointsOut, profileVectorsOut):
            
            Pmax = GridCornerBig (treeIn)
            Xmax = Pmax.X
            Ymax = Pmax.Y
            Zmax = Pmax.Z
            
            Pmin = GridCornerSmall (treeIn)
            Xmin = Pmin.X
            Ymin = Pmin.Y
            Zmin = Pmin.Z
            
            print profilePointsIn
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                profPointsBranch = profilePointsIn.Branch(i)
                profVectorsBranch = profileVectorsIn.Branch(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch [j]
                    profPoint = profPointsBranch [j]
                    profVector = profVectorsBranch [j]
                    
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    Xr = x/Xmax
                    Yr = y/Ymax
                    
                    if Zmax == 0:
                        Zr = 0
                    else:
                        Zr = z/Zmax
                    
                    P1 = rs.AddPoint (Xmin, y, z)
                    P1 = rs.coerce3dpoint (P1)
                    P2 = rs.AddPoint (Xmax, y, z)
                    P2 = rs.coerce3dpoint (P2)
                    path = ghpath (treePath.AppendElement (j))
                    
                    treeOut.Add (P1, path)
                    treeOut.Add (P2, path)
                    ratioOut.Add (Xr, path)
                    profilePointsOut.Add (profPoint, path)
                    profilePointsOut.Add (profPoint, path)
                    profileVectorsOut.Add (profVector, path)
                    profileVectorsOut.Add (profVector, path)
        
        def CreateModPoints (treeIn, ratioIn, treeOut):
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                ratioBranch = ratioIn.Branch(i)
                treePath = treeIn.Path(i)
                
                P1 = treeBranch[0]
                P2 = treeBranch[1]
                ratio = ratioBranch[0]
                
                line = rs.AddLine (P1, P2)
                line = rs.coercecurve (line)
                
                point = rh.Geometry.Curve.PointAtNormalizedLength(line, ratio)
                
                path = ghpath (treePath.CullElement())
                
                treeOut.Add (point, path)
        
        def ProfileCurveThings (treeIn, profCrv, profPointTreeOut, vectorTreeOut, vectorLineTree, tOut):
            
            MaxCoord = GridCornerBig (treeIn)
            x_max = MaxCoord.X
            y_max = MaxCoord.Y
            z_max = MaxCoord.Z
            
            profPointList = []
            profVecDirection = []
            vectorList = []
            curvatureTree = datatree [sys.Object] ()
            directionTree = datatree [sys.Object] ()
            
            
            Crv = rs.coercecurve (profCrv)
            start = rs.CurveStartPoint (Crv)
            end = rs.CurveEndPoint (Crv)
            
            if start.Y > end.Y :
                Crv = rh.Geometry.Curve.Reverse (Crv)
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    
                    elem = treeBranch[j]
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    Yarany = y / y_max
                    crvPoint = rh.Geometry.Curve.PointAtNormalizedLength(profCrv, Yarany)
                    crvPoint = rs.coerce3dpoint (crvPoint)
                    
                    
                    t = rs.CurveClosestPoint (profCrv, crvPoint)
                    
                    curvature = rs.CurveCurvature(profCrv, t)[4]
                    tangent = rs.CurveCurvature(profCrv, t)[1]
                    angle1 = rs.VectorAngle ([0,1,0], curvature)
                    angle2 = rs.VectorAngle ([0,1,0], tangent)
                    
                    curvatureRot = curvature
                    curvatureRot = rs.coerce3dpoint (curvatureRot)
                    
                    rs.RotateObject (curvatureRot, [0,0,0], 90, [0,0,1])
                    curvatureRot = rs.coerce3dvector (curvatureRot)
                    
                    angle = rs.VectorAngle (curvatureRot, tangent)
                    curvature = rs.coerce3dpoint(curvature)
                    
                    
                    if 179.99 < angle <180.01:
                        angleDirect = 0
                    else:
                        angleDirect = 1
                    
                    profPointList.append (crvPoint)
                    profVecDirection.append (angleDirect)
                    vectorList.append (curvature)
                    
                    curvatureTree.Add (curvature, treePath)
                    profPointTreeOut.Add (crvPoint, treePath)
                    directionTree.Add (angleDirect, treePath)
                    tOut.Add (Yarany, treePath)
            
            profPoint_x_List = []
            for i in range (profPointList.Count):
                profPoint = profPointList [i]
                profPoint_x = profPoint.X
                profPoint_x_List.append (profPoint_x)
            
            a = 0
            for i in range (profPoint_x_List.Count):
                x = profPoint_x_List [i]
                Xabs = math.fabs (x)
                if Xabs > a:
                    b = i
                    a = Xabs
                    c = x
                
            directByMax = profVecDirection [b]
            
            vectorByMax = vectorList [b]
            pointByMax = profPointList [b]
            stableByMax = pointByMax
            pointX = math.fabs (stableByMax.X)
            moveByMax = pointByMax
            unitVecByMax = rs.VectorUnitize (vectorByMax)
            rs.MoveObject (moveByMax, 5* unitVecByMax)
            moveX = math.fabs (moveByMax.X)
            
            
            if moveX > pointX:
                mirror = 1
            else:
                mirror = 0
            
            
            for i in range(curvatureTree.BranchCount):
                treeBranch = curvatureTree.Branch(i)
                treePath = curvatureTree.Path(i)
                pointBranch = profPointTreeOut.Branch(i)
                directionBranch = directionTree.Branch(i)
                
                for j in range(treeBranch.Count):
                    curvature = treeBranch [j]
                    crvPoint = pointBranch [j]
                    direction = directionBranch [j]
                    
                    curvature = rs.coerce3dpoint(curvature)
                    
                    if mirror == 0:
                        if direction != directByMax:
                            rs.RotateObject (curvature, [0,0,0], 180, [0,0,1])
                    
                    if mirror == 1:
                        if direction == directByMax:
                            rs.RotateObject (curvature, [0,0,0], 180, [0,0,1])
                    
                    
                    curvature = rs.coerce3dvector(curvature)
                    unitCrvVec = rs.VectorUnitize (curvature)
                    
                    
                    if c < 0:
                        unitCrvVec2 = - unitCrvVec
                    else:
                        unitCrvVec2 = unitCrvVec
                    
                    unitCrvVec = rs.coerce3dvector (unitCrvVec)
                    unitCrvVec2 = rs.coerce3dvector (unitCrvVec2)
                    
                    moveCrvPoint = crvPoint + (unitCrvVec*5)
                    
                    moveCrvPoint = rs.coerce3dpoint (moveCrvPoint)
                    vectorLine = rs.AddLine (crvPoint, moveCrvPoint)
                    vectorTreeOut.Add (unitCrvVec2, treePath)
                    vectorLineTree.Add (vectorLine, treePath)
        
        def MakeCylindricalCoordinates (treeIn, profPointTreeIn, treeOut, thicknessOut, angleOut):
            # U1, U2, U3 meghatarozasa
            
            profMax = GridCornerBig (profPointTreeIn)
            profMin = GridCornerSmall (profPointTreeIn)
            
            MaxCoord = GridCornerBig (treeIn)
            x_max = MaxCoord.X
            y_max = MaxCoord.Y
            z_max = MaxCoord.Z
            
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                profBranch = profPointTreeIn.Branch(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    profPoint = profBranch [j]
                    
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    b = beta / x_max
                    
                    
                    #y = y_max - y
                    # a logikus vetites miatt
                    
                    U2 = x * b
                    
                    
                    PmaxY = profMax.Y
                    PminY = profMin.Y
                    delta = PmaxY - PminY
                    U3 = (profPoint.Y - PminY) * length / delta
                    
                    
                    deltaZ = z_max
                    
                    
                    if deltaZ != 0:
                        deltaV = thick
                        v = ( 1 - (z / deltaZ)) * deltaV
                        
                        
                    else:
                        v = 0
                    
                    
                    PmaxX = profMax.X
                    PminX = profMin.X
                    
                    pMax = math.fabs (PmaxX)
                    pMin = math.fabs (PminX)
                    
                    if pMin > pMax:
                        MAX = pMin
                        v = -v
                    else :
                        MAX = pMax
                    r = profPoint.X * rad / MAX
                    
                    U1 = r
                    
                    EllPoint = rs.AddPoint (U1,U2,U3)
                    EllPoint = rs.coerce3dpoint (EllPoint)
                    treeOut.Add (EllPoint, treePath)
                    thicknessOut.Add (v, treePath)
                    angleOut.Add (U2, treePath)
        
        def MoveWithVector (treeIn, profPointTreeIn, vectorTreeIn, thicknessIn, angleIn, treeOut):
            
            profMax = GridCornerBig (profPointTreeIn)
            profMin = GridCornerSmall (profPointTreeIn)
            
            max =  GridCornerBig (treeIn)
            
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                profBranch = profPointTreeIn.Branch(i)
                vectorBranch = vectorTreeIn.Branch(i)
                thicknessBranch = thicknessIn.Branch(i)
                angleBranch = angleIn.Branch(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    profPoint = profBranch [j]
                    vector = vectorBranch [j]
                    v = thicknessBranch [j]
                    angle = angleBranch [j]
                    
                    
                    if type != 0:
                        elemLapos = rs.AddPoint (elem.X,elem.Y,0)
                        elemLapos = rs.coerce3dvector (elemLapos)
                        
                        #angle = rs.VectorAngle ([1,0,0], elemLapos)
                        betaRad = math.radians (beta)
                        
                        gammaRad = math.radians (angle)
                        
                        if gammaRad > betaRad/2:
                            gammaRad = gammaRad - betaRad/2
                        else:
                            gammaRad = betaRad/2 - gammaRad
                        
                        v = (math.cos (betaRad/2)) / (math.cos (gammaRad)) *v
                    
                    vec = rs.coerce3dpoint (vector)
                    rotVecX = vec.X
                    rotVecZ = vec.Y
                    rotVecY = vec.Z
                    rotVec = rs.AddPoint (rotVecX, rotVecY, rotVecZ)
                    rotVec = rs.coerce3dpoint (rotVec)
                    ORIGO = rs.AddPoint (0,0,0)
                    ORIGO = rs.coerce3dpoint (ORIGO)
                    VECTOR = rs.RotateObject(rotVec, ORIGO, angle, [0,0,1])
                    
                    vector = rs.coerce3dvector (VECTOR)
                    vector = vector * v
                    
                    elem = rs.coerce3dpoint (elem)
                    
                    MovePoint = rs.MoveObject (elem, vector)
                    MovePoint = rs.coerce3dpoint (MovePoint)
                    
                    treeOut.Add (elem, treePath)
        
        def CreateVault (treeIn, treeOut):
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    
                    U1 = elem.X
                    U2 = elem.Y
                    U2rad = math.radians (U2)
                    U3 = elem.Z
                    
                    x = U1 * math.cos (U2rad)
                    y = U1 * math.sin (U2rad)
                    z = U3
                    
                    NewPoint = rs.AddPoint (x,y,z)
                    NewPoint = rs.coerce3dpoint (NewPoint)
                    
                    treeOut.Add (NewPoint, treePath)
        
        def DomeAxisOrigo (treeIn, treeOut, axisIn, origoIn):
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    if axisIn == 0:
                        x2 = z
                        y2 = x
                        z2 = y
                        
                    elif axisIn == 1:
                        x2 = y
                        y2 = z
                        z2 = x
                        
                    else:
                        x2 = x
                        y2 = y
                        z2 = z
                        
                    origoIn = rs.coerce3dpoint (origoIn)
                    Ox = origoIn.X
                    Oy = origoIn.Y
                    Oz = origoIn.Z
                    
                    x3 = x2 + Ox
                    y3 = y2 + Oy
                    z3 = z2 + Oz
                    
                    ujelem = rs.CreatePoint (x3, y3, z3)
                    treeOut.Add (ujelem, treePath)
        
        def CreateDomeGrid (treeIn, treeOut):
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                path = ghpath (treePath.CullElement())
                if treeBranch[0] != treeBranch[1]:
                    
                    curves = rs.AddCurve (treeBranch)
                    curves = rs.coercecurve (curves)
                    
                    treeOut.Add (curves, path)
        
        def CarthesianToKlinogonial (treeIn, treeOut):
            
            Pmax = GridCornerBig (treeIn)
            Xmax = Pmax.X
            Ymax = Pmax.Y
            Zmax = Pmax.Z
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    
                    szog = math.radians ((180-angle)/2)
                    
                    v1 = x - (y / math.tan(szog))
                    
                    #v1 aranyositasa
                    v1max = Xmax - 2 * (y / math.tan(szog))
                    
                    # kerekites !!!!!!!!
                    if -0.000000001 < v1max < 0.000000001:
                        v1r = Xmax / 2
                    else:
                        v1r = v1 / v1max * Xmax
                    
                    v2 = y / math.sin(szog)
                    
                    ujelem = rs.AddPoint (v1r, v2, z)
                    ujelem = rs.coerce3dpoint (ujelem)
                    
                    treeOut.Add (ujelem, treePath)
        
        
        # osztaspontok szama egyenes/gorbe tipus alapjan
        NumPerCrv = GridType()
        
        # gorbe felosztasa
        Points = datatree[rh.Geometry.Point3d]()
        DivideCurves (grid, NumPerCrv, Points)
        
        # halo mozgatasa az origoba
        MovedPoints = datatree[rh.Geometry.Point3d]()
        MoveGridToOrigo (Points, MovedPoints)
        
        # profilgorbe alkalmazasa
        ProfCrvPoints = datatree[rh.Geometry.Point3d]()
        ProfCrvVectors = datatree [rh.Geometry.Vector3d]()
        VecLine = datatree[sys.Object]()
        tOut = datatree[sys.Object]()
        ProfileCurveThings (MovedPoints, profileCrv, ProfCrvPoints, ProfCrvVectors, VecLine, tOut)
        
        # atalakitas klinogonalis koordinatakka
        KlinPoints = datatree[rh.Geometry.Point3d]()
        CarthesianToKlinogonial (MovedPoints, KlinPoints)
        
        if type == 0:
            #CYLINDRICAL
            
            # U1, U2, U3 meghatarozasa
            CylPoints = datatree[rh.Geometry.Point3d]()
            Thickness = datatree[sys.Object]()
            Angle =  datatree[sys.Object]()
            MakeCylindricalCoordinates (KlinPoints, ProfCrvPoints, CylPoints, Thickness, Angle)
            
            # uj x,y,z meghatarozasa
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateVault (CylPoints, ModiPoints)
            
            #vastagsag
            ModiMovePoints = datatree[rh.Geometry.Point3d]()
            MoveWithVector (ModiPoints, ProfCrvPoints, ProfCrvVectors, Thickness, Angle, ModiMovePoints)
        
        else:
            #PRISM
            
            # perem U1, U2, U3 meghatarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            ProfCrvPoints2 = datatree[rh.Geometry.Point3d]()
            ProfCrvVectors2 = datatree [rh.Geometry.Vector3d]()
            CupolaCollar (KlinPoints, ProfCrvPoints, ProfCrvVectors, MPoints, MRatio, ProfCrvPoints2, ProfCrvVectors2)
            
            # U1, U2, U3 meghatarozasa
            CylPoints = datatree[rh.Geometry.Point3d]()
            Thickness = datatree[sys.Object]()
            Angle =  datatree[sys.Object]()
            MakeCylindricalCoordinates (MPoints, ProfCrvPoints2, CylPoints, Thickness, Angle)
            
            # perem uj x,y,z meghatarozasa
            NewMPoints = datatree[rh.Geometry.Point3d]()
            CreateVault (CylPoints, NewMPoints)
            
            #vastagsag
            MovePoints = datatree[rh.Geometry.Point3d]()
            MoveWithVector (NewMPoints, ProfCrvPoints2, ProfCrvVectors2, Thickness, Angle, MovePoints)
            
            # pontok berakasa a perem koze
            ModiMovePoints = datatree[rh.Geometry.Point3d]()
            CreateModPoints (MovePoints, MRatio, ModiMovePoints)
        
        
        # axis, origo modositasa
        FinalPoints = datatree[rh.Geometry.Point3d]()
        DomeAxisOrigo (ModiMovePoints, FinalPoints, axis, origo)
        
        # pontok osszekotese
        CylCurves = datatree[rh.Geometry.Curve]()
        CreateDomeGrid (FinalPoints, CylCurves)
        
        
        C = CylCurves
        D = VecLine
        
        
        
        
        
        # return outputs if you have them; here I try it for you:
        return (C,D)
    

import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Kitsune Triangular Revolution Grid 2"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("075cd7fc-533b-494e-bdc2-8ee9ba83ae54")