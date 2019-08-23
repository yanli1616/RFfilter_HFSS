# -*- coding: utf-8 -*-
"""
Functions in this module correspond more or less to the functions described 
in the HFSS Scripting Guide, Section "Analysis Setup Module Script Commands"

At last count there were 2 functions implemented out of 20.
"""
from __future__ import division, print_function, unicode_literals, absolute_import

from hycohanz.design import get_module

def increment_name(base, existing):
    if not base in existing:
        return base
    n = 1
    make_name = lambda: base + str(n)
    while make_name() in existing:
        n += 1
    return make_name()

def insert_frequency_sweep(oDesign,
                           setupname,
                           sweepname,
                           startvalue,
                           stopvalue,
                           count=None,
                           stepsize=None,
                           IsEnabled=True,
                           Type="Fast",
                           SaveFields=True,
                           ExtrapToDC=False):
    """
    Insert an HFSS frequency sweep.
    
    Warning
    -------
    The API interface for this function is very susceptible to change!  It 
    currently only works for Discrete sweeps using Linear Steps.  Contributions 
    are encouraged.
    
    Parameters
    ----------
    oAnalysisSetup : pywin32 COMObject
        The HFSS Analysis Setup Module in which to insert the sweep.
    setupname : string
        The name of the setup to add
    sweepname : string
        The desired name of the sweep
    startvalue : float
        Lowest frequency in Hz.
    stopvalue : float
        Highest frequency in Hz.
    stepsize : flot
        The frequency increment in Hz  .
    IsEnabled : bool
        Whether the sweep is enabled.
    SetupType : string
        The type of sweep setup to add.  One of "LinearStep", "LinearCount", 
        or "SinglePoints".  Currently only "LinearStep" is supported.
    Type : string
        The type of sweep to perform.  One of "Discrete", "Fast", or 
        "Interpolating".  Currently only "Discrete" is supported.
    Savefields : bool
        Whether to save the fields.
    ExtrapToDC : bool
        Whether extrapolation to DC is enabled.
        
    Returns
    -------
    None
    
    """
    if (count is None) == (stepsize is None):
        raise ValueError("Exactly one of 'points' and 'delta' must be specified")
    oAnalysisSetup = oDesign.GetModule("AnalysisSetup")
    params = [
        "NAME:" + sweepname,
        "IsEnabled:=", IsEnabled,
        "StartValue:=", str(startvalue) + "GHz",
        "StopValue:=", str(stopvalue) + "GHz",
        "Type:=", Type,
        "SaveFields:=", SaveFields,
        "ExtrapToDC:=", ExtrapToDC,
    ]
    if stepsize is not None:
        params.extend([
            "SetupType:=", "LinearStep",
            "StepSize:=", str(stepsize) + "GHz",
        ])
    else:
        params.extend([
            "SetupType:=", "LinearCount",
            "Count:=", count,
        ])
    return oAnalysisSetup.InsertFrequencySweep(setupname, params)



def insert_analysis_setup(oDesign, 
                          Frequency,
                          PortsOnly=False,
                          MaxDeltaS=0.02,
                          Name='Setup1',
                          UseMatrixConv=False,
                          MaximumPasses=15,
                          MinimumPasses=1,
                          MinimumConvergedPasses=1,
                          PercentRefinement=30,
                          IsEnabled=True,
                          BasisOrder=1,
                          UseIterativeSolver=False,
                          DoLambdaRefine=True,
                          DoMaterialLambda=True,
                          SetLambdaTarget=False,
                          Target=0.3333,
                          UseMaxTetIncrease=False,
                          PortAccuracy=2,
                          UseABCOnPort=False,
                          SetPortMinMaxTri=False,
                          EnableSolverDomains=False,
                          ThermalFeedback=False,
                          NoAdditionalRefinementOnImport=False):
    """
    Insert an HFSS analysis setup.
    """
    oAnalysisSetup = get_module(oDesign, "AnalysisSetup")
    oAnalysisSetup.InsertSetup( "HfssDriven", 
                               ["NAME:" + Name, 
                                "Frequency:=", str(Frequency) +"GHz",
                                "PortsOnly:=", PortsOnly, 
                                "MaxDeltaS:=", MaxDeltaS, 
                                "UseMatrixConv:=", UseMatrixConv, 
                                "MaximumPasses:=", MaximumPasses, 
                                "MinimumPasses:=", MinimumPasses, 
                                "MinimumConvergedPasses:=", MinimumConvergedPasses, 
                                "PercentRefinement:=", PercentRefinement, 
                                "IsEnabled:=", IsEnabled, 
                                "BasisOrder:=", BasisOrder, 
                                "UseIterativeSolver:=", UseIterativeSolver, 
                                "DoLambdaRefine:=", DoLambdaRefine, 
                                "DoMaterialLambda:=", DoMaterialLambda, 
                                "SetLambdaTarget:=", SetLambdaTarget, 
                                "Target:=", Target, 
                                "UseMaxTetIncrease:=", UseMaxTetIncrease, 
                                "PortAccuracy:=", PortAccuracy, 
                                "UseABCOnPort:=", UseABCOnPort, 
                                "SetPortMinMaxTri:=", SetPortMinMaxTri, 
                                "EnableSolverDomains:=", EnableSolverDomains, 
                                "ThermalFeedback:=", ThermalFeedback, 
                                "NoAdditionalRefinementOnImport:=", NoAdditionalRefinementOnImport])
                                
    return Name

def create_output_variable(oDesign,Name,Expression):
    oModule=oDesign.GetModule("OutputVariable")
    oModule.CreateOutputVariable(Name,
                                 Expression,
                                 "Setup1:LastAdaptive",
                                 "Modal Solution Data",
                                 ["Domain:=", "Sweep"])

def create_report(oDesign, name, expr, ReportType="Rectangular Plot"):
    oReportSetup=oDesign.GetModule("ReportSetup")
    existing = oReportSetup.GetAllReportNames()
    name = increment_name(name, existing)
    oReportSetup.CreateReport(
        name, "Modal Solution Data", ReportType,
        "Setup1:Sweep1", ["Domain:=", "Sweep"], ["Freq:=", ["All"]],
        ["X Component:=", "Freq", "Y Component:=", expr], [])