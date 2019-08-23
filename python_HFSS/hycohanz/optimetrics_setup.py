# -*- coding: utf-8 -*-
"""
Functions in this module correspond more or less to the functions described
in the HFSS Scripting Guide, Section "Analysis Setup Module Script Commands"

At last count there were 2 functions implemented out of 20.
"""
from __future__ import division, print_function, unicode_literals, absolute_import

from hycohanz.design import get_module


def insert_optimetrics_setup(oDesign,
                             Name,
                             Sweepname,
                             variable,
                             startvalue,
                             stopvalue,
                             count=None,
                             stepsize=None,
                             SaveFields=False,
                             OffsetF1=False,
                             ):
    if (count is None) == (stepsize is None):
        raise ValueError("Exactly one of 'points' and 'delta' must be specified")

    oOptimetricsSetup=get_module(oDesign, "Optimetrics")

    if stepsize is not None:
        SweepData="LIN "+str(startvalue)+"mm "+str(stopvalue)+"mm "+str(stepsize) + "mm"
    else:
        SweepData = "LINC " + str(startvalue) + "mm " + str(stopvalue) + "mm " + str(count)
    oOptimetricsSetup.InsertSetup("OptiParametric",
                                  ["NAME:"+Name,
                                   "IsEnabled:=", True,
                                   "SaveFields:=", SaveFields,
                                   ["NAME:StartingPoint"],
                                   "Sim. Setups:=",
                                   [Sweepname],
                                   [
                                       "NAME:Sweeps",
                                        ["NAME:SweepDefinition",
                                         "Variable:=",variable,
                                         "Data:=", SweepData,
                                         "OffsetF1:=",OffsetF1,
                                         "Synchronize:=",0
                                         ]
                                   ],
                                   ["NAME:Sweep Operations"],
                                   ["NAME:Goals"]
                                   ])
    return Name
def param_setup(oDesign,name):
    oOptimetricsSetup = get_module(oDesign, "Optimetrics")
    oOptimetricsSetup.SolveSetup(name)

def insert_optioptimization_setup(oDesign,
                                  name,
                                  goals,
                                  startvalue,stopvalue,
                                  value,
                                  variable,
                                  minvalue,maxvalue,
                                  minstep,maxstep,
                                  SaveFields=False,
                                  ):
    oOptimetricsSetup = get_module(oDesign, "Optimetrics")
    DiscreteValues = ""
    for i in range(startvalue,stopvalue+1):
        DiscreteValues = DiscreteValues + str(i) + "GHz" + ','
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers",
                    "LocalVariables"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:"+variable,
                        [
                            "NAME:Optimization",
                            "Included:="	, True
                        ]
                    ]
                ]
            ]
        ])
    oOptimetricsSetup.InsertSetup("OptiOptimization",
                                  ["NAME:"+name,
                                   "IsEnabled:=",True,
                                   [
                                       "NAME:ProdOptiSetupDataV2",
                                       "Savefields:=",SaveFields,
                                       "CopyMesh:=",False,
                                       "SolveWithCopiedMeshOnly:=", True
                                   ],
                                   [
                                       "NAME:StartingPoint"
                                   ],
                                   "Optimizer:=","Quasi Newton",
                                   [
                                       "NAME:AnalysisStopOptions",
                                       "StopForNumIteration:=", True,
                                       "StopForElapsTime:=", False,
                                       "StopForSlowImprovement:=", False,
                                       "StopForGrdTolerance:=", False,
                                       "MaxNumIteration:=", 1000,
                                       "MaxSolTimeInSec:=", 3600,
                                       "RelGradientTolerance:=", 0,
                                       "MinNumIteration:=", 10
                                   ],
                                   "CostFuncNormType:=", "L2",
                                   "PriorPSetup:="	, "",
                                   "PreSolvePSetup:="	, True,
                                   [
                                       "NAME:Variables",
                                       variable+":=",
                                       ["i:=", True,
                                        "Min:=", minvalue,
                                        "Max:=", maxvalue,
                                        "MinStep:=", minstep,
                                        "MaxStep:=", maxstep]
                                   ],
                                   [
                                       "NAME:LCS"
                                   ],
                                   [
                                       "NAME:Goals",
                                       [
                                           "NAME:Goal",
                                           "ReportType:="	, "Modal Solution Data",
                                           "Solution:="		, "Setup1 : Sweep1",
                                           [
                                               "NAME:SimValueContext",
                                               "Domain:="		, "Sweep"
                                           ],
                                           "Calculation:="		, goals,
                                           "Name:="		, goals,
                                           [
                                               "NAME:Ranges",
                                               "Range:="		, ["Var:=", "Freq",
                                                                   "Type:="	, "rd",
                                                                   "Start:=", str(startvalue)+"GHz",
                                                                   "Stop:="	, str(stopvalue)+"GHz",
                                                                   "DiscreteValues:=", DiscreteValues
                                                                   ]
                                           ],
                                           "Condition:=", "==",
                                           [
                                               "NAME:GoalValue",
                                               "GoalValueType:=", "Independent",
                                               "Format:=", "Real/Imag",
                                               "bG:=", ["v:=", "[2.813;]"]
                                           ],
                                           "Weight:=", "[1;]"
                                       ]
                                   ],
                                   "Acceptable_Cost:=", 0,
                                   "Noise:="	, 0.0001,
                                   "UpdateDesign:="	, False,
                                   "UpdateIteration:="	, 5,
                                   "KeepReportAxis:="	, True,
                                   "UpdateDesignWhenDone:=", True
                                   ])
    return name
