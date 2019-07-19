"""Gives additional setting options for the Kitsune Dome, Vault and Polar Grid tools.
    Inputs:
        t: Thickness of the grid
        g: The gap angle in the center of the Dome or Polar Grid (no effect on Vaults)
        l: Are the final rods lines or curves? 0 = line, 1 = curve
        O: Origo of the Dome
        a: Axis of the Dome. 0 = x, 1 = y, 2 = z
    Output:
        S: Dome Settings. You can connect to the Settings input of the Kitsune Dome, Vault and Polar Grid tools. """

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System as sys
import Rhino as rh
import rhinoscriptsyntax as rs
import Grasshopper.Kernel.Data.GH_Path as ghpath
import Grasshopper.DataTree as datatree
import math

__author__ = "Reka Sarkozi"
__version__ = "2018.07.26"

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Kitsune Grid Settings", "GridSettings", """Gives additional setting options for the Kitsune Dome, Vault and Polar Grid tools.""", "Extra", "Kitsune")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("4d4c7a7f-a41b-4c76-b8d4-7446a81d7e9d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "t", "t", "Thickness of the grid")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "g", "g", "The gap angle in the center of the Dome or Polar Grid (no effect on Vaults)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "l", "l", "Are the final rods lines or curves? 0 = line, 1 = curve")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "O", "O", "Origo of the Dome")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "a", "a", "Axis of the Dome. 0 = x, 1 = y, 2 = z")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "S", "S", "Dome Settings. You can connect to the Settings input of the Kitsune Dome, Vault and Polar Grid tools. ")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAEASURBVEhL7dHNSwJRFMbhocwsN4KEiGW060MRXQiiQq4URJDKSFuUC8WVoH2YBG2CVqGrQPpr+73jjMlsIgRX94WHOwxz7z3njGViYrK+HKKLS/j0YilRZw3Bjz2k9OI/+UYZB9hADjcI4wsNjPEGHX6GY9yjBqWCO5wijmssCqniE9qQxgzq6BEDJNBGHVlnfYL2ab3FECW84AHauw87W9jFBO+YIg9VoAvUyRWKSELddRBwnp+h4mIYQWPt4RV2LqCD+oigCW04gSrWxxqJvtHFGajaIM5xhBY+oA4KUMfu+OxsOqsb78/+KxqXKtaIFe95K2cH2/NHExOT31jWD848Ho72MceJAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, t, g, l, O, a):
        
        
        settings = datatree[sys.Object]()
        path0 = ghpath (0)
        settings.Add (t, path0)
        
        path1 = ghpath (1)
        settings.Add (g, path1)
        
        path2 = ghpath (2)
        settings.Add (l, path2)
        
        path3 = ghpath (3)
        settings.Add (O, path3)
        
        path4 = ghpath (4)
        settings.Add (a, path4)
        
        S = settings
        
        # return outputs if you have them; here I try it for you:
        return S


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Kitsune Grid Settings"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("62492522-06d4-4e46-bba8-f2699e422ebd")