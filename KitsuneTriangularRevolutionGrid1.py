"""Makes a TRIANGULAR grid of revolution from any grid. Needs angular size as input 'b'. Needs a Profile Curve to manipulate the radius. The thickness of the grid will be perpendicular to the axis.
    Inputs:
        C: Grid to transform
        pC: Profile Curve (have to be a planar curve on the 'xy' plane, the axis is the axis 'y')
        r: The radius of the vault
        l: The length of the vault
        n: Angle of the apex of the initial isosceles triangle
        b: 3rd angular size (Beta)
        T: Vault Type (0 = cylinrical, 1 = prism)
        S: Grid Settings
    Output:
        C: The Curves of the Vault"""

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
            "Kitsune Triangular Revolution Grid 1", "Kitsune TriRevGrd 1", """Makes a TRIANGULAR grid of revolution from any grid. Needs angular size as input 'b'. Needs a Profile Curve to manipulate the radius. The thickness of the grid will be perpendicular to the axis.""", "Extra", "Kitsune")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("eeba1d75-4731-4465-9140-f5e9a4b8812a")
    
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
        self.SetUpParam(p, "pC", "pC", "Profile Curve (have to be a planar curve on the 'xy' plane, the axis is the axis 'y')")
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
        self.SetUpParam(p, "C", "C", "The Curves of the Vault")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMcSURBVEhLrdXpi5ZlFMDhKfoitGC2Z6VkUUp7RJlZ2r6ardqi7WVUtmqWRQvtexkRgkUFFqRhmKDQByEsiCL6EkF/jL/r5Z0PgyM11YGL0Wee517OOfc9IxOIPXJIpmb/7Jn/LS7N0tyUK3Nd7soJ+c/xcH7Mfbk2Z+b63Jpvcm7+dTySn7M+q/Nhnsvr+TTv5s9ckgnHQ/klnwz//UyezYo8HxM9li/zUzz/R7F31sT2F+WOGPiqrMyFeSJ3R01eigX8mjeyX3YbfmnF62Jly/JRroicv5fDo+D3RwrfzwvxnlS+k70ybryaDbH1J3NqPs7F8eHtWRLpmZsP4nfX5LVYkEkezS5hmxsjv1YoNVZ47/CnQV+OFv0qJjDonfG7y+Pde7IjYwp/UL6OFSmWLSPH+v2GGODqSJezgBodFzVSk1cijW/lu+ybQSzMm3k7cm2bc2InLw6f3RbFvTFPxU6cESueFbuzU+nx0y4d0EFY5dbYrgOlFg9G3/vAIHZmh6fkgSyI59JqcoszyUXRbd/HIgbhwWfR62ujyIrpQHlpcRwqKTKhDvPN+ZEeizGwFKmHnW2KOg5Cd/weD10HCm6bVnpLpNCKj8xlkX81Gb0yno6JZUAttuS3ODuDOCt/5fPYxeacndNzToQbdGb2yZS4TTWHbjo4Fub70VT+kBMzCC+YUaG12s05IA6TDjoqBlBg75rcGZmW5bHSyZFKu/gif2RSBuGuVyyHyiDufAPNi0H8HZBn3XJspE+BvaNNdZx3joh0atHtGRNOquKohytYTg+Lrjk+0uGaMDn+bbIzYqLHI11qsiruqDHhuH8bXXN0tN706Hk7kU8f+iOjyBdEmpwT72kC/3eCt8VOxsSMSJMa6AQFtnJ/YBRVGkwkDQ6gbjowJjwpFmD36uaytKtdwspccs7A/Fi9zpFvk+mo2cNnx0Q6Rk+8FWtb3xtnt2GV+t9g7n4DK7C0SZHVOid2IP86yDtSayLf/21oUe3pdNqNdJ2X04a0qZ9W6jR7x7NDM6FwG0qFTjKBQZzgk2MnukY3OXzjxMjITr7dnknJNxwAAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, C, pC, r, l, n, b, T, S):
        
        
        
        grid = C
        profCrv = rs.coercecurve (pC)
        
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
        
        def MakeCylindricalCoordinates (treeIn, treeOut):
            # U1, U2, U3 meghatarozasa
            
            MaxCoord = GridCornerBig (treeIn)
            x_max = MaxCoord.X
            y_max = MaxCoord.Y
            z_max = MaxCoord.Z
            
            if profCrv != None:
                profPointTree = datatree [sys.Object] ()
                profPointList = []
                
                Crv = rs.coercecurve (profCrv)
                start = rs.CurveStartPoint (Crv)
                end = rs.CurveEndPoint (Crv)
                print start.Y
                print end.Y
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
                        point = rh.Geometry.Curve.PointAtNormalizedLength(profCrv, Yarany)
                        point = rs.coerce3dpoint (point)
                        
                        pointX = point.X
                        
                        profPointTree.Add (point, treePath)
                        profPointList.append (point)
                
                profMax = GridCornerBig (profPointTree)
                profMin = GridCornerSmall (profPointTree)
                
                
            
            
            for i in range(treeIn.BranchCount):
                treeBranch = treeIn.Branch(i)
                treePath = treeIn.Path(i)
                profBranch = profPointTree.Branch(i)
                
                for j in range(treeBranch.Count):
                    elem = treeBranch[j]
                    profPoint = profBranch [j]
                    x = elem.X
                    y = elem.Y
                    z = elem.Z
                    
                    b = beta / x_max
                    c = length / y_max
                    
                    #y = y_max - y
                    # a logikus vetites miatt
                    
                    U2 = x * b
                    U3 = y * c
                    deltaZ = z_max
                    
                    
                    if deltaZ != 0:
                        deltaV = thick
                        v = ( 1 - (z / deltaZ)) * deltaV
                    else:
                        v = 0
                    
                    if profCrv != None:
                        Pmax = profMax.X
                        Pmin = profMin.X
                        pMax = math.fabs (Pmax)
                        pMin = math.fabs (Pmin)
                        if pMin > pMax:
                            MAX = pMin
                            v = -v
                        else :
                            MAX = pMax
                        r = profPoint.X * rad / MAX
                    else:
                        r = rad
                    
                    U1 = r-v
                    
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
            #CYLINDRICAL
            
            # U1, U2, U3 meghatarozasa
            CylPoints = datatree[rh.Geometry.Point3d]()
            MakeCylindricalCoordinates (KlinPoints, CylPoints)
            
            # uj x,y,z meghatarozasa
            ModiPoints = datatree[rh.Geometry.Point3d]()
            CreateVault (CylPoints, ModiPoints)
        
        else:
            #PRISM
            
            # perem U1, U2, U3 meghataarozasa
            MPoints = datatree[rh.Geometry.Point3d]()
            MRatio = datatree[sys.Object]()
            CupolaCollar (KlinPoints, MPoints, MRatio)
            
            CylMPoints = datatree[rh.Geometry.Point3d]()
            MakeCylindricalCoordinates (MPoints, CylMPoints)
            
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
        return "Kitsune Triangular Revolution Grid 1"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("e168f589-5ea0-4369-bfee-8cb11a5e0059")