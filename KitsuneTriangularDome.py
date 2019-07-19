"""Makes a Kitsune Dome from any TRIANGULAR grid. Needs angular size as input 'a' and 'b'.
    Inputs:
        C: Triangular Grid to transform (It has to be an isosceles triangle - or a part of it -, the symmetry axis has to be parallel with the axis 'y'.)
        r: The radius of the dome
        h: The height of the dome
        n: Angle of the apex of the initial isosceles triangle
        a: 2nd angular size (Alpha)
        b: 3rd angular size (Beta)
        T: Dome Type (0 = ellipsoidal, 1 = cupola, 2 = cone, 3 = pyramid)
        S: Grid Settings
    Output:
        C: The Curves of the Dome"""

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
            "Kitsune Tringular Dome", "Kitsune TriDome", """Makes a Kitsune Dome from any TRIANGULAR grid. Needs angular size as input 'a' and 'b'.""", "Extra", "Kitsune")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("ec73742d-c1b2-43c5-9530-a20e09e3b1e7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "C", "C", "Triangular Grid to transform (It has to be an isosceles triangle - or a part of it -, the symmetry axis has to be parallel with the axis 'y'.)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "r", "r", "The radius of the dome")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "h", "h", "The height of the dome")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "n", "n", "Angle of the apex of the initial isosceles triangle")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "a", "a", "2nd angular size (Alpha)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "b", "b", "3rd angular size (Beta)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "T", "T", "Dome Type (0 = ellipsoidal, 1 = cupola, 2 = cone, 3 = pyramid)")
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
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMTSURBVEhLzdTXz1RVFIbxQSxgpQkWlCJIU0ABsdLECkjQKBCwQRQ0ColETTSCsd2AwRivTLhS/0+f3zDnSwAF4pUreTLnzNnl3e9aa4/+DzE/nonP49v4Pk7FB7E7ZsR/itvi4zgfv8Yv8XrsidPxWZyLP+No3BLXHWvibFjoi3g7nogXwqJvxrPxaLwS++NMLItrxtb4K3bER7Ez9k6eH5o8s+yp+CYOT3g/LsTG+NeggBVfBysOxsL4Kg7F6lgVm2Np2OjJ+DG2hdP8EIvjirgpHPPDYIOJoJzHT8drcSB+ipNxT1iUpUviy/ANN8Ql8U5I2KbYFS/G4/F8UPRgmMQm3q8NY1jJVlay6kT8HApiKlQM/0x4N+4PyiRSqJA5QbGyNX5WiAVBhPFO+erkmW1TleXov4cEShLfPfP14cm7/xeFMPG+uD1YQ62xN4YTKWFJXx/jOB4ayfEomxcrY3ZYbEXIjQQrBO9OyirjjWEZAXODmD/i0xhNi9/iWNjx5uA5dYNivxI5JI6F20NVsWt63Bt3xJYghACiR3eH9n/AS/FSPHLxcbwQj03m/8wYbHHKO8Ni8uI7sQpE0u+K72I8WAUNg5QhFaqGBewQkuz4y4NiwigWxuhyvWGe8ibgSIwTaAMVRBErBnWuCJXhdAQ8F5LLc2Lkg31+JdWmvhGt0zXdeMIn4VgUebep0LEWgiS+F/pAjlSNvBEj/MeuobqUrqIZVwqlBroeJM2zCTbiv6DUAoLX8qTSbCj5xru6VZAG1QsuwXFsCH67bzwbxCrBU/5LuJO4UixKhHdWsmjYQKO5o1Skzh6HxDmyiaqG15rPIiYPVWUxiRxOxQ7Bc/YNNj0WrncnnAqL+yBR7HASVaOjlZ7vJr8Rkg4drBec8uXQdEQ4gTmXhDZfFzahmCXKUXKV4a2h/CTPQq6QfUG1sCER7GW3PvjHoFyCJF8e+C/ZmoyVfNftNrCId89+CTGX2KuGiY7+VphoYepNtBmFEuqZED0kh0PJXncoWYs4lbtHwi2k06lWKRI8XN2XxWj0N8aqXLK+LiATAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, C, r, h, n, a, b, T, S):
        
        
        
        grid = C
        rad = r
        if rad == None:
            rad = 10
        
        height = h
        if height == None:
            height = 10
        
        angle = n
        if angle == None:
            angle = 60
        
        alpha = a
        if alpha == None:
            alpha = 90
        
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
        print "a magassag: " + str (height)
        print "az alpha szog: " + str (alpha)
        print "a beta szog: " + str (beta)
        
        if type == 0:
            racstip = "ELLIPSOIDAL"
        elif type == 1:
            racstip = "CUPOLA"
        elif type == 2:
            racstip = "CONE"
        elif type == 3:
            racstip = "PYRAMID"
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
        
        def ConeCollar (treeIn, treeOut, ratioOut):
            
            Pmax = GridCornerBig (treeIn)
            Xmax = Pmax.X
            Ymax = Pmax.Y
            Zmax = Pmax.Z
            
            Pmin = GridCornerSmall (treeIn)
            Xmin = Pmin.X
            Ymin = Pmin.Y
            Zmin = Pmin.Z
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    Xr = x/Xmax
                    Yr = y/Ymax
                    
                    if Zmax == 0:
                        Zr = 0
                    else:
                        Zr = z/Zmax
                    
                    P1 = rs.AddPoint (x, Ymin, z)
                    P1 = rs.coerce3dpoint (P1)
                    P2 = rs.AddPoint (x, Ymax, z)
                    P2 = rs.coerce3dpoint (P2)
                    path = ghpath (treePath.AppendElement (j))
                    
                    treeOut.Add (P1, path)
                    treeOut.Add (P2, path)
                    ratioOut.Add (Yr, path)
        
        def CupolaCollar (treeIn, treeOut, ratioOut):
            
            Pmax = GridCornerBig (treeIn)
            Xmax = Pmax.X
            Ymax = Pmax.Y
            Zmax = Pmax.Z
            
            Pmin = GridCornerSmall (treeIn)
            Xmin = Pmin.X
            Ymin = Pmin.Y
            Zmin = Pmin.Z
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    
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
        
        def PyramidCollar (treeIn, treeOut, ratioOut):
            
            Pmax = GridCornerBig (treeIn)
            Xmax = Pmax.X
            Ymax = Pmax.Y
            Zmax = Pmax.Z
            
            Pmin = GridCornerSmall (treeIn)
            Xmin = Pmin.X
            Ymin = Pmin.Y
            Zmin = Pmin.Z
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    Xr = x/Xmax
                    Yr = y/Ymax
                    if Zmax == 0:
                        Zr = 0
                    else:
                        Zr = z/Zmax
                    
                    P1 = rs.AddPoint (Xmin, Ymin, z)
                    P1 = rs.coerce3dpoint (P1)
                    P2 = rs.AddPoint (Xmin, Ymax, z)
                    P2 = rs.coerce3dpoint (P2)
                    P3 = rs.AddPoint (Xmax, Ymin, z)
                    P3 = rs.coerce3dpoint (P3)
                    P4 = rs.AddPoint (Xmax, Ymax, z)
                    P4 = rs.coerce3dpoint (P4)
                    path = ghpath (treePath.AppendElement (j))
                    
                    treeOut.Add (P1, path)
                    treeOut.Add (P2, path)
                    treeOut.Add (P3, path)
                    treeOut.Add (P4, path)
                    ratioOut.Add (Xr, path)
                    ratioOut.Add (Yr, path)
        
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
        
        def CreatePyramidPoints (treeIn, ratioIn, treeOut):
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                ratioBranch = ratioIn.Branch(i)
                treePath = treeIn.Path(i)
                
                P1 = treeBranch[0]
                P2 = treeBranch[1]
                P3 = treeBranch[2]
                P4 = treeBranch[3]
                ratioX = ratioBranch[0]
                ratioY = ratioBranch[1]
                
                line1 = rs.AddLine (P1, P2)
                line1 = rs.coercecurve (line1)
                
                pointXmin = rh.Geometry.Curve.PointAtNormalizedLength(line1, ratioY)
                
                line2 = rs.AddLine (P3, P4)
                line2 = rs.coercecurve (line2)
                
                pointXmax = rh.Geometry.Curve.PointAtNormalizedLength(line2, ratioY)
                
                line3 = rs.AddLine (pointXmin, pointXmax)
                line3 = rs.coercecurve (line3)
                
                point = rh.Geometry.Curve.PointAtNormalizedLength(line3, ratioX)
                
                path = ghpath (treePath.CullElement())
                
                treeOut.Add (point, path)
        
        def MakeEllipsoidalCoordinates (treeIn, treeOut):
            # U1, U2, U3 meghatarozasa
            
            MaxCoord = GridCornerBig (treeIn)
            x_max = MaxCoord.X
            y_max = MaxCoord.Y
            z_max = MaxCoord.Z
            
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    a = alpha / x_max
                    b = beta / y_max
                    
                    y = y_max - y
                    # a logikus vetites miatt
                    
                    U2 = x * a
                    U3 = y * b + gap
                    
                    deltaZ = z_max
                    
                    if deltaZ != 0:
                        deltaV = thick
                        v = ( 1 - (z / deltaZ)) * deltaV
                    else:
                        v = 0
                    
                    
                    U2rad = math.radians (U2)
                    U3rad = math.radians (U3)
                    
                    a = math.sin (U3rad) * math.sin (U3rad)
                    b = (rad-v) * (rad-v)
                    c = math.cos (U3rad) * math.cos (U3rad)
                    d = (height-v) * (height-v)
                    
                    U1 = math.sqrt (1/(a/b+c/d))
                    
                    EllPoint = rs.AddPoint (U1,U2,U3)
                    EllPoint = rs.coerce3dpoint (EllPoint)
                    treeOut.Add (EllPoint, treePath)
        
        def CreateDome (treeIn, treeOut):
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    U1 = elem.X
                    U2 = elem.Y
                    U2rad = math.radians (U2)
                    U3 = elem.Z
                    U3rad = math.radians (U3)
                    
                    x = U1 * math.cos (U2rad) * math.sin (U3rad)
                    y = U1 * math.sin (U2rad) * math.sin (U3rad)
                    z = U1 * math.cos (U3rad)
                    
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
        
        # atalakitas klinogonalis koordinatakka
        KlinPoints = datatree[rh.Geometry.Point3d]()
        CarthesianToKlinogonial (MovedPoints, KlinPoints)
        
        if type == 0:
            #ELLIPSOIDAL
            
            # U1, U2, U3 meghatarozasa
            EllPoints = datatree[rh.Geometry.Point3d]()
            MakeEllipsoidalCoordinates (KlinPoints, EllPoints)
            
            # uj x,y,z meghatarozasa
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateDome (EllPoints, ModiPoints)
        
        elif type == 1:
            #CUPOLA
            
            # perem U1, U2, U3 meghataarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            CupolaCollar (KlinPoints, MPoints, MRatio)
            
            EllMPoints = datatree[rh.Geometry.Point3d]()
            MakeEllipsoidalCoordinates (MPoints, EllMPoints)
            
            # perem uj x,y,z meghatarozasa
            NewMPoints = datatree[rh.Geometry.Point3d]()
            CreateDome (EllMPoints, NewMPoints)
            
            # pontok berakasa a perem koze
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateModPoints (NewMPoints, MRatio, ModiPoints)
            
        elif type == 2:
            #CONE
            
            # perem U1, U2, U3 meghataarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            ConeCollar (KlinPoints, MPoints, MRatio)
            
            EllMPoints = datatree[rh.Geometry.Point3d]()
            MakeEllipsoidalCoordinates (MPoints, EllMPoints)
            
            # perem uj x,y,z meghatarozasa
            NewMPoints = datatree[rh.Geometry.Point3d]()
            CreateDome (EllMPoints, NewMPoints)
            
            # pontok berakasa a perem koze
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateModPoints (NewMPoints, MRatio, ModiPoints)
            
        else:
            #PYRAMID
            
            # perem U1, U2, U3 meghataarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            PyramidCollar (KlinPoints, MPoints, MRatio)
            
            EllMPoints = datatree[rh.Geometry.Point3d]()
            MakeEllipsoidalCoordinates (MPoints, EllMPoints)
            
            # perem uj x,y,z meghatarozasa
            NewMPoints = datatree[rh.Geometry.Point3d]()
            CreateDome (EllMPoints, NewMPoints)
            
            # pontok berakasa a perem koze
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreatePyramidPoints (NewMPoints, MRatio, ModiPoints)
        
        
        # axis, origo modositasa
        FinalPoints = datatree[rh.Geometry.Point3d]()
        DomeAxisOrigo (ModiPoints, FinalPoints, axis, origo)
        
        # pontok osszekotese
        EllCurves = datatree[rh.Geometry.Curve]()
        CreateDomeGrid (FinalPoints, EllCurves)
        
        
        C = EllCurves
        
        
        
        
        
        # return outputs if you have them; here I try it for you:
        return (C)
    

import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Kitsune Tringular Dome"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("673a4df8-7217-4698-b43d-f4efd20d3cd5")