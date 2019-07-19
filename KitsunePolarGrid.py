"""Makes a Kitsune Polar Grid from any grid. Needs angular size as input 'b'.
    Inputs:
        C: Grid to transform
        r: The radius of the vault
        b: 3rd angular size (Beta)
        T: Polar Grid Type (0 = polar, 1 = polygon)
        S: Grid Settings
    Output:
        C: The Curves of the Polar Grid"""

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
            "Kitsune Polar Grid", "Kitsune PolarGrd", """Makes a Kitsune Polar Grid from any grid. Needs angular size as input 'b'.""", "Extra", "Kitsune")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("76344a13-a409-4873-874a-7fd7344667eb")
    
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
        self.SetUpParam(p, "r", "r", "The radius of the vault")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "b", "b", "3rd angular size (Beta)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "T", "T", "Polar Grid Type (0 = polar, 1 = polygon)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "S", "S", "Grid Settings")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "C", "C", "The Curves of the Polar Grid")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAALmSURBVEhLpdYJTxRBEMXxAeN9K+KN94EiXngLXggemGiMJn7/L8L7dbo2JrAJGzr5Z4eZ7qpXr2pnGSZY+8LBcCgcDnvCrteRMBeehI/hWb/+2q/vhUtB4onW3rAYXoelIOin8DAshG/93tOwEeyTaEeL6jvhflgLggiqgkedz0GyV+F7uBkedI6GsWsmvA9Xw5Ug+Jcg4ZtAqSCqYQ+rVHgjqPhHIGB/2LLYcjksh/VA1flAOaUCvw0CSPY4sIoQdrFK0mvB2S3rVLjQUb4DgvhbIApfhOdBwA9BUnvsVcXFQKSqPButM+FdcNPUsIoy9ghYPRDM36q0XyL9IML+l0HfJNfDA6EtmR32YLV/ssJkUMOileCwRBLrlZ7oD+vYanQJJFjMs2GYCsqi2gNBHbK5/Kf4Z/jTP38HDaZYP+w/HkzQuSB4VdXG8nqQRINud3h6K/Cd8n9BQGW79zewqWxzbbqgOqh6mA0scYPaUuzTYTj8q98zDCyRkP+CE1gDwgEVnA6msJXGq5PhRP9UKrtMDgvYpTfm3MSwybVnNVFEua4ecKYlcME3wfVhPjjI/5qqSiKQxtYrREXuO8de1bDIWdesbt86/pv9mgxfmGNByaZDLxyAgL7h9rnPQj2SwBkW1pePlW2KNM0hJbFLVZrsoNfG3cACFRFiv+eS85pSqo02e9xTFWfaciG7SnwaO55TIqFmUkgE1dR5HUisar8P9Vo3EJrM8jamlh8PSjVXDyivqeA1GySnXAKBjSxhKpLYD5Ek4hiA+m6MlnHlveDKFNABnntVCMx3I8keyVhjH2uc9cPjuUls/v+/poNp8dAm6gTlrVKVTbWkqKoo9d6RhG2+iFzY9pUtiUZqEHu8DjRecIGoklw/VMAqDZWQkKpOH8cuU6V0DRNUMAqruRKCWmPrPkthGIjb0RKUDRTpj0QarhoJVKhaz+xVjf88JlqqMaYaqNnlM9Wq1DN/j/mvYhg2AaPbTh+wEYlTAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, C, r, b, T, S):
        
        
        
        grid = C
        
        rad = r
        if rad == None:
            rad = 10
        
        
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
        print "a beta szog: " + str (beta)
        
        if type == 0:
            racstip = "POLAR"
        elif type == 1:
            racstip = "POLYGON"
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
        
        def MakePolarCoordinates (treeIn, treeOut):
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
                    
                    b = beta / x_max
                    c = rad / y_max
                    
                    y = y_max - y
                    # a logikus vetites miatt
                    
                    U2 = x * b
                    deltaZ = z_max
                    
                    if deltaZ != 0:
                        deltaV = thick
                        v = ( 1 - (z / deltaZ)) * deltaV
                        U3 = thick-v
                    else:
                        v = 0
                        U3 = v
                    
                    
                    U1 = y * c + gap
                    
                    EllPoint = rs.AddPoint (U1,U2,U3)
                    EllPoint = rs.coerce3dpoint (EllPoint)
                    treeOut.Add (EllPoint, treePath)
        
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
        
        
        # osztaspontok szama egyenes/gorbe tipus alapjan
        NumPerCrv = GridType()
        
        # gorbe felosztasa
        Points = datatree[rh.Geometry.Point3d]()
        DivideCurves (grid, NumPerCrv, Points)
        
        # halo mozgatasa az origoba
        MovedPoints = datatree[rh.Geometry.Point3d]()
        MoveGridToOrigo (Points, MovedPoints)
        
        if type == 0:
            #POLAR
            
            # U1, U2, U3 meghatarozasa
            CylPoints = datatree[rh.Geometry.Point3d]()
            MakePolarCoordinates (MovedPoints, CylPoints)
            
            # uj x,y,z meghatarozasa
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateVault (CylPoints, ModiPoints)        
        
        else:
            #POLYGON
            
            # perem U1, U2, U3 meghataarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            CupolaCollar (MovedPoints, MPoints, MRatio)
            
            CylMPoints = datatree[rh.Geometry.Point3d]()
            MakePolarCoordinates (MPoints, CylMPoints)
            
            # perem uj x,y,z meghatarozasa
            NewMPoints = datatree[rh.Geometry.Point3d]()
            CreateVault (CylMPoints, NewMPoints)
            
            # pontok berakasa a perem koze
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateModPoints (NewMPoints, MRatio, ModiPoints)
        
        
        # axis, origo modositasa
        FinalPoints = datatree[rh.Geometry.Point3d]()
        DomeAxisOrigo (ModiPoints, FinalPoints, axis, origo)
        
        # pontok osszekotese
        CylCurves = datatree[rh.Geometry.Curve]()
        CreateDomeGrid (FinalPoints, CylCurves)
        
        
        C = CylCurves
        
        
        
        
        
        # return outputs if you have them; here I try it for you:
        return (C)
    

import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Kitsune Polar Grid"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("76e10b3c-903c-45dc-9075-4014ce59821c")