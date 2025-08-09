# encoding: utf-8
"""
TauAlgorithmsHolder.py
~~~~~~~~~~~~~~~~~~~~~~


Notes: 

* All tool holder functions should have argument format: def func(tag=None)



TODO: description to go here
"""

__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2016-02-25"
__copyright__ = "Copyright 2016 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

## modules
from THOR.CommonLoads import *

#===============================================================================
# WriteContainers 
#===============================================================================
def getTruthTausContainer(branches=None):
    """Return configured TruthTaus OutputContainer"""
    return OutputContainer(OutputName = "TruthTaus",
                           ClassType = TruthParticleContainer,
                           SlimmingExpression = branches)


def getTauJetsContainer(branches=None):
    """Return configured TauJets OutputContainer"""
    return OutputContainer(OutputName = "TauJets",
                           ClassType = TauJetContainer,
                           StoreName = "TauJets_skimmed",
                           SlimmingExpression = branches)

def getTruthDiTausContainer(branches=None):
    """Return configured DiTruthTaus OutputContainer"""
    return OutputContainer(OutputName = "DiTruthTaus",
                           ClassType = TruthParticleContainer,
                           SlimmingExpression = branches)


def getDiTauJetsContainer(branches=None):
    """Return configured DiTauJets OutputContainer"""
    return OutputContainer(OutputName = "DiTauJets",
                           ClassType = DiTauJetContainer,
                           StoreName = "DiTauJets_skimmed",
                           SlimmingExpression = branches)


def getNeutralPFOsContainer(branches=None, copied=True):
    """Return configured NeutralPFOs OutputContainer

    If Pi0InfoDecorator run with ThinNeutrals=True (as configued in 
    getPi0InfoDecorator()), the default arg copied=True should be
    used to access the thinned container, otherwise, copied=False
    should explicitly be set. 

    Note: don't rename container as it will break tau->pfo links 
    """
    if copied: cname = "TauNeutralParticleFlowObjects_skimmed"
    else:      cname = "TauNeutralParticleFlowObjects"
    return OutputContainer(OutputName = cname,
                           ClassType = PFOContainer,
                           SlimmingExpression = branches)

def getHadronicPFOsContainer(branches=None):
    """Return configured HadronicPFOs OutputContainer"""
    return OutputContainer(OutputName = "TauHadronicParticleFlowObjects",
                           ClassType = PFOContainer,
                           SlimmingExpression = branches)


def getShotPFOsContainer(branches=None):
    """Return configured ShotPFOs OutputContainer"""
    return OutputContainer(OutputName = "TauShotParticleFlowObjects",
                           ClassType = PFOContainer,
                           SlimmingExpression = branches)


def getEventInfoContainer(branches=None):
    """Return configured EventInfo OutputContainer"""
    return OutputContainer(OutputName = "EventInfo",
                           ClassType = EventInfo,
                           SlimmingExpression = branches)
 

def getEmptyTauJetsContainer():
    """Return configured TauJets OutputContainer with no content"""
    return OutputContainer(OutputName = "TauJets",
                           ClassType = TauJetContainer,
                           StoreName = "TauJets_skimmed",
                           SlimmingExpression = "nothing")
   
 
def getEmptyEventInfoContainer(branches=None):
    """Return configured EventInfo OutputContainer with no content"""
    return OutputContainer(OutputName = "EventInfo",
                           ClassType = EventInfo,
                           SlimmingExpression = "nothing")

def getTauTracksContainer(branches=None):
    """Return TauTracks Container for re-running MVA tracking"""
    return OutputContainer(OutputName = "TauTracks",
                           ClassType = TauTrackContainer,
                           StoreName = "TauTracksFix",
                           SlimmingExpression = branches)

def getTracksContainer(branches=None):
    """Return InDetTrackParticles Container"""
    return OutputContainer(OutputName = "InDetTrackParticles",
                           ClassType = TrackParticleContainer,
                           SlimmingExpression = branches)

 

#===============================================================================
# Selectors 
#===============================================================================
def getTauTruthMatchingToolAndWrapper(datatype=None,
                                      inTrigger=False,
                                      TruthJetContainerName=""):
    """Return configured BuildTruthTaus, TauTruthMatchingTool and Wrapper"""

    BuildTruthTaus = ROOT.TauAnalysisTools.BuildTruthTaus("BuildTruthTaus")
    CHECK(BuildTruthTaus.setProperty("WriteVisibleChargedFourMomentum", True))
    CHECK(BuildTruthTaus.setProperty("WriteVisibleNeutralFourMomentum", True))
    CHECK(BuildTruthTaus.setProperty("TruthElectronContainerName", ""))
    CHECK(BuildTruthTaus.setProperty("TruthMuonContainerName", ""))
    CHECK(BuildTruthTaus.setProperty("TruthJetContainerName", ""))

    TauTruthMatchingTool = ROOT.TauAnalysisTools.TauTruthMatchingTool("TauTruthMatchingTool")
    CHECK(TauTruthMatchingTool.setProperty("TruthElectronContainerName", "egammaTruthParticles"))
    CHECK(TauTruthMatchingTool.setProperty("TruthMuonContainerName",     "MuonTruthParticles"))
    # AntiKt4TruthJets may not be available in AOD
    CHECK(TauTruthMatchingTool.setProperty("TruthJetContainerName", TruthJetContainerName))

    TauTruthMatchingToolWrapper = ROOT.THOR.TauTruthMatchingToolWrapper("TauTruthMatchingToolWrapper")
    CHECK(TauTruthMatchingToolWrapper.setProperty("BuildTruthTausToolName", "BuildTruthTaus"))
    CHECK(TauTruthMatchingToolWrapper.setProperty("TauTruthMatchingToolName", "TauTruthMatchingTool"))
    CHECK(TauTruthMatchingToolWrapper.setProperty("inTrigger", inTrigger))
    # deprecated property?
    CHECK(TauTruthMatchingToolWrapper.setProperty("DecorateResonanceMass",False))
    
    if datatype == "ELE":
        CHECK(TauTruthMatchingToolWrapper.setProperty("AcceptElectrons", True))
    elif datatype == "JET":
        CHECK(TauTruthMatchingToolWrapper.setProperty("AcceptAll", True))
    elif datatype == "MUON":
        CHECK(TauTruthMatchingToolWrapper.setProperty("AcceptMuons", True))
    elif datatype == "TAU":
        CHECK(TauTruthMatchingToolWrapper.setProperty("AcceptHadronicTaus", True))
    else:
        raise ValueError(f"Unknown datatype {datatype}")

    return ConfigItems(sel_tools=[TauTruthMatchingToolWrapper], aux_tools=[BuildTruthTaus, TauTruthMatchingTool])

def getDiTauTruthMatchingToolAndWrapper(tag=None):
    """Return configured DiTauTruthMatchingTool and Wrapper"""
    DT2MT = ROOT.TauAnalysisTools.DiTauTruthMatchingTool("DiTauTruthMatchingTool")
    DT2MT.msg().setLevel( ROOT.MSG.INFO )

    DT2MTWrapper = ROOT.THOR.DiTauTruthMatchingToolWrapper("DiTauTruthMatchingToolWrapper")
    CHECK(DT2MTWrapper.setProperty("DiTauTruthMatchingToolName", "DiTauTruthMatchingTool"))

    if tag == "hadhad":
        CHECK(DT2MTWrapper.setProperty("ContainerNames", stdvector('string', ["DiTauJets"])))

    return ConfigItems(sel_tools=[DT2MTWrapper], aux_tools=[DT2MT])

def getTauSelectionToolAndWrapper(tag=None, datatype=None):
    """Return configured TauSelectionTool and Wrapper"""
    TST = ROOT.TauAnalysisTools.TauSelectionTool("TauSelectionTool")
    CHECK(TST.setProperty("ConfigPath",""))

    # Stream dependent cut configuration
    # we must improve this
    if tag and tag.startswith("StreamMain"): 
        CHECK(TST.setProperty("SelectionCuts",int(CutPt|CutAbsEta)))
        CHECK(TST.setProperty("PtMin",0.))
        vAbsEtaRegion = stdvector('float', [0, 2.5])
        CHECK(TST.setProperty("AbsEtaRegion",vAbsEtaRegion))
    elif tag and tag.startswith("StreamTrack"): 
        CHECK(TST.setProperty("SelectionCuts",int(CutPt|CutAbsEta)))
        CHECK(TST.setProperty("PtMin",0.))
        vAbsEtaRegion = stdvector('float', [0, 2.5])
        CHECK(TST.setProperty("AbsEtaRegion",vAbsEtaRegion))
    elif tag and tag.startswith("StreamUpgrade"):
        CHECK(TST.setProperty("SelectionCuts",int(CutPt|CutAbsEta)))
        CHECK(TST.setProperty("PtMin",15.))
        vAbsEtaRegion = stdvector('float', [0, 4.0])
        CHECK(TST.setProperty("AbsEtaRegion",vAbsEtaRegion))
    elif tag and tag.startswith("StreamGNN"): 
        CHECK(TST.setProperty("SelectionCuts",int(CutPt|CutAbsEta)))
        CHECK(TST.setProperty("PtMin",15.))
        vAbsEtaRegion = stdvector('float', [0, 2.5])
        CHECK(TST.setProperty("AbsEtaRegion",vAbsEtaRegion))    
    else:
        CHECK(TST.setProperty("SelectionCuts",int(CutPt|CutAbsEta)))
        CHECK(TST.setProperty("PtMin",15.))
        #vAbsEtaRegion = stdvector('float',[0,1.37,1.52,2.5]) 
        vAbsEtaRegion = stdvector('float',[0,4.0])
        CHECK(TST.setProperty("AbsEtaRegion",vAbsEtaRegion))

    # CHECK(TST.setProperty("CreateControlPlots", True))
    TST.msg().setLevel( ROOT.MSG.DEBUG )
        
    TSTWrapper = ROOT.THOR.TauSelectionToolWrapper("TauSelectionToolWrapper")
    CHECK(TSTWrapper.setProperty("TauSelectionToolName", "TauSelectionTool"))

    return ConfigItems(sel_tools=[TSTWrapper], aux_tools=[TST])


def getTauTrackSelectorTool(tag=None, datatype=None):
    """Return configured TauTrackSelectorTool"""
    return ROOT.THOR.TrackingTrackSelector("TrackingTrackSelector")


#===============================================================================
# Decorators 
#===============================================================================
def getTauInfoDecorator(tag=None, datatype=None): 
    """Return configured TauInfoDecorator

    Note: turn on all decorations here, easier to set the slimming per stream
    if particular vars not wanted
    """
    tool = ROOT.tauRecToolsDev.TauInfoDecorator("TauInfoDecorator")
    CHECK(tool.setProperty("VarsForSubstructure", True))
    CHECK(tool.setProperty("VarsForFSR", True))
    CHECK(tool.setProperty("VarsForTracking", True))
    return tool


def getCommonCalculator(tag=None, datatype=None): 
    """Return configured TauCommonCalcVars"""
    return ROOT.TauCommonCalcVars("TauCommonCalcVars")


def getPi0InfoDecorator(tag=None, datatype=None): 
    """Return configued Pi0InfoDecorator"""
    tool = ROOT.tauRecToolsDev.Pi0InfoDecorator("Pi0InfoDecorator")
    CHECK(tool.setProperty("ThinNeutrals",True))
    return tool


def getExtraTauIDVarsCalculator(tag=None, datatype=None):
    """Return configued ExtraTauIDVarsCalculator"""
    return ROOT.ExtraTauIDVarsCalculator("ExtraTauIDVarsCalculator")


def getLCTESCalibration(tag=None, datatype=None):
    """Return configured TauCalibrateLC"""
    Config = ConfigItems()
    return Config


def getTauVertexedClusterDecorator(tag=None, datatype=None, calib="LC"):
    config = ConfigItems()
    
    tool = ROOT.TauVertexedClusterDecorator("TauVertexedClusterDecorator")
    CHECK(tool.setProperty("SeedJet", calib))

    config += tool
    
    return tool


def getTauCombinedTES(tag=None, datatype=None):
    """Return configured CombinedTES calibration"""
    Config = ConfigItems()
    return Config


def getMvaTESVariableDecorator(tag=None, datatype=None): 
    """Return configued MvaTESVariableDecorator"""
    tool = ROOT.MvaTESVariableDecorator("MvaTESVariableDecorator")
    return tool


def getMvaTESEvaluator(tag=None, datatype=None):
    """Get configured MvaTESEvaluator"""
    tool = ROOT.MvaTESEvaluator( "MvaTESEvaluator" )
    
    return tool


def getTauIDVarCalculator(tag=None, datatype=None):
    """Return configured TauIDVarCalculator"""
    tool = ROOT.TauIDVarCalculator(name = "TauIDVarCalculator")
    return tool

def getTauEVetoRNNEvaluator(
        NetworkFile1P="", NetworkFile3P="",
        OutputVarname="RNNEleScore", MaxTracks=10,
        MaxClusters=6, MaxClusterDR=1.0, InputLayerScalar="scalar",
        InputLayerTracks="tracks", InputLayerClusters="clusters",
        OutputLayer="rnneveto_output", OutputNode="sig_prob"):

    tool = ROOT.TauJetRNNEvaluator("TauEleRNN")
    CHECK(tool.setProperty("NetworkFile1P", NetworkFile1P))
    CHECK(tool.setProperty("NetworkFile3P", NetworkFile3P))
    CHECK(tool.setProperty("OutputVarname", OutputVarname))
    CHECK(tool.setProperty("MaxTracks", MaxTracks))
    CHECK(tool.setProperty("MaxClusters", MaxClusters))
    CHECK(tool.setProperty("MaxClusterDR", MaxClusterDR))
    CHECK(tool.setProperty("InputLayerScalar", InputLayerScalar))
    CHECK(tool.setProperty("InputLayerTracks", InputLayerTracks))
    CHECK(tool.setProperty("InputLayerClusters", InputLayerClusters))
    CHECK(tool.setProperty("OutputLayer", OutputLayer))
    CHECK(tool.setProperty("OutputNode", OutputNode))

    return tool

def getTauJetRNNEvaluator(
        NetworkFile1P="", NetworkFile3P="",
        OutputVarname="RNNJetScore", MaxTracks=10,
        MaxClusters=6, MaxClusterDR=1.0, InputLayerScalar="scalar",
        InputLayerTracks="tracks", InputLayerClusters="clusters",
        OutputLayer="rnnid_output", OutputNode="sig_prob"):

    tool = ROOT.TauJetRNNEvaluator("TauJetRNNEvaluator")
    CHECK(tool.setProperty("NetworkFile1P", NetworkFile1P))
    CHECK(tool.setProperty("NetworkFile3P", NetworkFile3P))
    CHECK(tool.setProperty("OutputVarname", OutputVarname))
    CHECK(tool.setProperty("MaxTracks", MaxTracks))
    CHECK(tool.setProperty("MaxClusters", MaxClusters))
    CHECK(tool.setProperty("MaxClusterDR", MaxClusterDR))
    CHECK(tool.setProperty("InputLayerScalar", InputLayerScalar))
    CHECK(tool.setProperty("InputLayerTracks", InputLayerTracks))
    CHECK(tool.setProperty("InputLayerClusters", InputLayerClusters))
    CHECK(tool.setProperty("OutputLayer", OutputLayer))
    CHECK(tool.setProperty("OutputNode", OutputNode))

    return tool

def getTauGNNEvaluator(
        NetworkFileInclusive="GNTau_pruned_MC23.onnx", name="TauGNNEvaluator",
        OutputVarname="GNTauScore", OutputPTau="GNTauProbTau",OutputPJet="GNTauProbJet",
        MaxTracks=30, MaxClusters=20, MaxClusterDR=15.0, InputLayerScalar="tau_vars",
        InputLayerTracks="track_vars", InputLayerClusters="cluster_vars",
        NodeNameTau="salt_pb", NodeNameJet="salt_pu"):

    tool = ROOT.TauGNNEvaluator(name)
    CHECK(tool.setProperty("NetworkFileInclusive", NetworkFileInclusive))
    CHECK(tool.setProperty("OutputVarname", OutputVarname))
    CHECK(tool.setProperty("OutputPTau", OutputPTau))
    CHECK(tool.setProperty("OutputPJet", OutputPJet))
    CHECK(tool.setProperty("MaxTracks", MaxTracks))
    CHECK(tool.setProperty("MaxClusters", MaxClusters))
    CHECK(tool.setProperty("MaxClusterDR", MaxClusterDR))
    CHECK(tool.setProperty("InputLayerScalar", InputLayerScalar))
    CHECK(tool.setProperty("InputLayerTracks", InputLayerTracks))
    CHECK(tool.setProperty("InputLayerClusters", InputLayerClusters))
    CHECK(tool.setProperty("NodeNameTau", NodeNameTau))
    CHECK(tool.setProperty("NodeNameJet", NodeNameJet))

    return tool

def getTauWPDecoratorGNN(
        flatteningFile1Prong="GNTauNAprune_flat_model_1p.root",
        flatteningFile2Prong="GNTauNAprune_flat_model_2p.root",
        flatteningFile3Prong="GNTauNAprune_flat_model_3p.root"
        ):

    wp_names = stdvector("string", ["GNTauTHOR_VL", "GNTauTHOR_L", "GNTauTHOR_M", "GNTauTHOR_T"])
    sig_eff_1p = stdvector("float", [0.95, 0.85, 0.75, 0.60])
    sig_eff_2p = stdvector("float", [0.95, 0.75, 0.60, 0.45])
    sig_eff_3p = stdvector("float", [0.95, 0.75, 0.60, 0.45])

    tool = ROOT.TauWPDecorator("TauWPDecoratorGNN")
    #CHECK(tool.setProperty("flatteningFile0Prong", flatteningFileNProng))
    CHECK(tool.setProperty("flatteningFile1Prong", flatteningFile1Prong))
    CHECK(tool.setProperty("flatteningFile2Prong", flatteningFile2Prong))
    CHECK(tool.setProperty("flatteningFile3Prong", flatteningFile3Prong))
    CHECK(tool.setProperty("DecorWPNames", wp_names))
    CHECK(tool.setProperty("DecorWPCutEffs1P", sig_eff_1p))
    CHECK(tool.setProperty("DecorWPCutEffs2P", sig_eff_2p))
    CHECK(tool.setProperty("DecorWPCutEffs3P", sig_eff_3p))
    CHECK(tool.setProperty("ScoreName", "GNTauScore"))
    CHECK(tool.setProperty("NewScoreName", "GNTauScoreSigTrans"))
    CHECK(tool.setProperty("DefineWPs", True))

    return tool

def getTauWPDecoratorJetRNN(
        flatteningFile1Prong="tauid_rnnWP_1p_R22_v0.root",
        flatteningFile3Prong="tauid_rnnWP_3p_R22_v0.root"):

    enum_vals = stdvector("int", [ROOT.xAOD.TauJetParameters.JetRNNSigVeryLoose,
                                  ROOT.xAOD.TauJetParameters.JetRNNSigLoose,
                                  ROOT.xAOD.TauJetParameters.JetRNNSigMedium,
                                  ROOT.xAOD.TauJetParameters.JetRNNSigTight])
    sig_eff_1p = stdvector("float", [0.95, 0.85, 0.75, 0.60])
    sig_eff_3p = stdvector("float", [0.95, 0.75, 0.60, 0.45])

    tool = ROOT.TauWPDecorator("TauWPDecoratorJetRNN")
    CHECK(tool.setProperty("flatteningFile1Prong", flatteningFile1Prong))
    CHECK(tool.setProperty("flatteningFile3Prong", flatteningFile3Prong))
    CHECK(tool.setProperty("CutEnumVals", enum_vals))
    CHECK(tool.setProperty("SigEff1P", sig_eff_1p))
    CHECK(tool.setProperty("SigEff3P", sig_eff_3p))
    CHECK(tool.setProperty("ScoreName", "RNNJetScore"))
    CHECK(tool.setProperty("NewScoreName", "RNNJetScoreSigTrans"))
    CHECK(tool.setProperty("DefineWPs", True))

    return tool


def getTauWPDecoratorEVetoRNN(
        flatteningFile1Prong="rnneveto_mc16d_flat_1p_fix.root",
        flatteningFile3Prong="rnneveto_mc16d_flat_3p_fix.root"):

    enum_vals = stdvector("int", [ROOT.xAOD.TauJetParameters.EleRNNLoose,
                                  ROOT.xAOD.TauJetParameters.EleRNNMedium,
                                  ROOT.xAOD.TauJetParameters.EleRNNTight])
    sig_eff_1p = stdvector("float", [0.95, 0.90, 0.85])
    sig_eff_3p = stdvector("float", [0.98, 0.95, 0.90])

    tool = ROOT.TauWPDecorator("TauWPDecoratorEVetoRNN")
    CHECK(tool.setProperty("flatteningFile1Prong", flatteningFile1Prong))
    CHECK(tool.setProperty("flatteningFile3Prong", flatteningFile3Prong))
    CHECK(tool.setProperty("CutEnumVals", enum_vals))
    CHECK(tool.setProperty("SigEff1P", sig_eff_1p))
    CHECK(tool.setProperty("SigEff3P", sig_eff_3p))
    CHECK(tool.setProperty("ScoreName", "RNNEleScore"))
    CHECK(tool.setProperty("NewScoreName", "RNNEleScoreSigTrans"))
    CHECK(tool.setProperty("DefineWPs", True))

    return tool

def getPanTauProcessorAndSubtools(tag=None, datatype=None):
    """Return configured PanTauProcessor and sub-tools"""
    Tool_InformationStore = ROOT.PanTau.Tool_InformationStore( "PanTau_InformationStore" )
        
    Tool_InputConverter  = ROOT.PanTau.Tool_InputConverter("PanTau_InputConverter")
    CHECK(Tool_InputConverter.setProperty("Tool_InformationStoreName", "PanTau_InformationStore"))
    
    Tool_TauConstituentGetter = ROOT.PanTau.Tool_TauConstituentGetter( "PanTau_TauConstituentGetter")
    CHECK(Tool_TauConstituentGetter.setProperty("Tool_InformationStoreName", "PanTau_InformationStore"))
    CHECK(Tool_TauConstituentGetter.setProperty("Tool_InputConverterName", "PanTau_InputConverter"))
        
    # ===> Tau Constituent Selector
    Tool_TauConstituentSelector = ROOT.PanTau.Tool_TauConstituentSelector( "PanTau_TauConstituentSelector")
    CHECK(Tool_TauConstituentSelector.setProperty("Tool_InformationStoreName", "PanTau_InformationStore"))
        
    # ===> Tau Feature Extractor
    Tool_FeatureExtractor = ROOT.PanTau.Tool_FeatureExtractor(   "PanTau_FeatureExtractor")
    CHECK(Tool_FeatureExtractor.setProperty("Tool_InformationStoreName", "PanTau_InformationStore" ))

        
    Tool_DetailsArranger = ROOT.PanTau.Tool_DetailsArranger( "PanTau_DetailsArranger" )
    CHECK(Tool_DetailsArranger.setProperty("Tool_InformationStoreName", "PanTau_InformationStore" ))


    curInAlg = 'CellBased'

    print("TopOptions_NewPanTau: Adding PanTau algorithms for input alg: " + curInAlg)
        
    Tool_ModeDiscri_1p0n_vs_1p1n = ROOT.PanTau.Tool_ModeDiscriminator( "PanTau_ModeDiscri_1p0n_vs_1p1n_" + curInAlg)
    CHECK(Tool_ModeDiscri_1p0n_vs_1p1n.setProperty("calibFolder", "tauRecTools/00-02-00"))
    CHECK(Tool_ModeDiscri_1p0n_vs_1p1n.setProperty("Name_InputAlg", curInAlg))
    CHECK(Tool_ModeDiscri_1p0n_vs_1p1n.setProperty("Name_ModeCase", "1p0n_vs_1p1n"))
    CHECK(Tool_ModeDiscri_1p0n_vs_1p1n.setProperty("Tool_InformationStoreName", "PanTau_InformationStore"))

    Tool_ModeDiscri_1p1n_vs_1pXn = ROOT.PanTau.Tool_ModeDiscriminator(   "PanTau_ModeDiscri_1p1n_vs_1pXn_" + curInAlg)
    CHECK(Tool_ModeDiscri_1p1n_vs_1pXn.setProperty("calibFolder", "tauRecTools/00-02-00"))
    CHECK(Tool_ModeDiscri_1p1n_vs_1pXn.setProperty("Name_InputAlg", curInAlg))
    CHECK(Tool_ModeDiscri_1p1n_vs_1pXn.setProperty("Name_ModeCase", "1p1n_vs_1pXn"))
    CHECK(Tool_ModeDiscri_1p1n_vs_1pXn.setProperty("Tool_InformationStoreName", "PanTau_InformationStore"))

    Tool_ModeDiscri_3p0n_vs_3pXn = ROOT.PanTau.Tool_ModeDiscriminator(   "PanTau_ModeDiscri_3p0n_vs_3pXn_" + curInAlg )
    CHECK(Tool_ModeDiscri_3p0n_vs_3pXn.setProperty("calibFolder", "tauRecTools/00-02-00"))
    CHECK(Tool_ModeDiscri_3p0n_vs_3pXn.setProperty("Name_InputAlg", curInAlg))
    CHECK(Tool_ModeDiscri_3p0n_vs_3pXn.setProperty("Name_ModeCase", "3p0n_vs_3pXn"))
    CHECK(Tool_ModeDiscri_3p0n_vs_3pXn.setProperty("Tool_InformationStoreName",   "PanTau_InformationStore"))

    # ===> Tau Decay Mode Determinator for current input alg
    Name_DecayModeDeterminator = "PanTau_DecayModeDeterminator_" + curInAlg
    Tool_DecayModeDeterminator = ROOT.PanTau.Tool_DecayModeDeterminator( Name_DecayModeDeterminator )
    CHECK(Tool_DecayModeDeterminator.setProperty("Tool_InformationStoreName",  "PanTau_InformationStore"))
    CHECK(Tool_DecayModeDeterminator.setProperty("Tool_ModeDiscriminator_1p0n_vs_1p1nName", "PanTau_ModeDiscri_1p0n_vs_1p1n_" + curInAlg))
    CHECK(Tool_DecayModeDeterminator.setProperty("Tool_ModeDiscriminator_1p1n_vs_1pXnName", "PanTau_ModeDiscri_1p1n_vs_1pXn_" + curInAlg))
    CHECK(Tool_DecayModeDeterminator.setProperty("Tool_ModeDiscriminator_3p0n_vs_3pXnName", "PanTau_ModeDiscri_3p0n_vs_3pXn_" + curInAlg))

    Tool_PanTauProcessor = ROOT.PanTau.PanTauProcessor(  "PanTau_PanTauProcessor" )
    CHECK(Tool_PanTauProcessor.setProperty("Name_InputAlg", curInAlg))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_InformationStoreName",       "PanTau_InformationStore"))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_TauConstituentGetterName",   "PanTau_TauConstituentGetter"))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_TauConstituentSelectorName", "PanTau_TauConstituentSelector"))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_FeatureExtractorName",       "PanTau_FeatureExtractor"))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_DecayModeDeterminatorName",  Name_DecayModeDeterminator))
    CHECK(Tool_PanTauProcessor.setProperty("Tool_DetailsArrangerName",        "PanTau_DetailsArranger"))

    subtools = [
        Tool_InformationStore, 
        Tool_InputConverter, 
        Tool_TauConstituentGetter, 
        Tool_TauConstituentSelector, 
        Tool_FeatureExtractor, 
        Tool_DetailsArranger, 
        Tool_ModeDiscri_1p0n_vs_1p1n, 
        Tool_ModeDiscri_1p1n_vs_1pXn, 
        Tool_ModeDiscri_3p0n_vs_3pXn, 
        Tool_DecayModeDeterminator,
        ] 

    return ConfigItems(dec_tools=[Tool_PanTauProcessor], aux_tools=subtools)

def getTrackVariableCalculator(tag=None, datatype=None):
    """Return tool to calculate track variables"""
    Config = ConfigItems()

    location=""

    # Track Truth Matching
    TauTruthTrackMatchingTool = ROOT.TauAnalysisTools.TauTruthTrackMatchingTool("TauTruthTrackMatchingTool")

    # Track Variable Calculator
    TrackVariableCalculator = ROOT.tauRecToolsDev.TrackVariableCalculator("TrackVariableCalculator")
    
    Config += ConfigItems(dec_tools=[TrackVariableCalculator],aux_tools=[TauTruthTrackMatchingTool])
    
    return Config 

def getTauMVATrackingDecorators(tag=None, datatype=None):
    """Return configuration to re-run MVA Tracking"""
    Config = ConfigItems() 
    return Config 

#EOF
