from EventFilter.DTTFRawToDigi.dttfunpacker_cfi import *

dttfunpacker.DTTF_FED_Source = 'rawDataCollector'  ## MWGR Feb12 

dtunpacker = cms.EDProducer("DTUnpackingModule",
                            dataType = cms.string('DDU'),
                            ##inputLabel = cms.InputTag('source'), ## needed for new versions, at least >356  
                            inputLabel = cms.InputTag('rawDataCollector'), ## MWGR Feb12
                            ###useStandardFEDid = cms.untracked.bool(True),
                            useStandardFEDid = cms.bool(True),
                            ###fedbyType = cms.untracked.bool(True),
                            ###fedbyType = cms.bool(False), ## tracked for new versions, at least >356, and also false ???? 
                            fedbyType = cms.bool(True),
                            dqmOnly = cms.bool(False),   ## needed for new versions, at least >356  
                            readOutParameters = cms.PSet(debug = cms.untracked.bool(False),
                                                       rosParameters = cms.PSet(writeSC = cms.untracked.bool(True),
                                                                                readingDDU = cms.untracked.bool(True),
                                                                                performDataIntegrityMonitor = cms.untracked.bool(True),
                                                                                readDDUIDfromDDU = cms.untracked.bool(True),
                                                                                debug = cms.untracked.bool(False),
                                                                                localDAQ = cms.untracked.bool(False)
                                                                                ),
                                                       localDAQ = cms.untracked.bool(False),
                                                       performDataIntegrityMonitor = cms.untracked.bool(True)
                                                       )
                            )


###from Configuration.StandardSequences.Geometry_cff import *  ##  Deprecated in new versions > 53X
from Configuration.Geometry.GeometryIdeal_cff import *
from RecoLocalMuon.Configuration.RecoLocalMuonCosmics_cff import *
dt1DRecHits.dtDigiLabel = 'dtunpacker'


from RecoTracker.Configuration.RecoTracker_cff import *  ## Needed at least in  710pre8 to avoid an error in RecoMuonCosmics file (GroupedCkfTrajectoryBuilder)
from RecoMuon.Configuration.RecoMuonCosmics_cff import *
from RecoVertex.BeamSpotProducer.BeamSpot_cff import *
from TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagator_cfi import *

##cosmicMuonsBarrelOnly.TrajectoryBuilderParameters.EnableRPCMeasurement = False
## cosmicMuonsBarrelOnly doesn't exist on 44X, the only barrel used is 1leg
CosmicMuonSeed.EnableCSCMeasurement = False
cosmicMuons.TrajectoryBuilderParameters.EnableCSCMeasurement = False
cosmicMuons.TrajectoryBuilderParameters.EnableRPCMeasurement = False

from CondCore.DBCommon.CondDBSetup_cfi import *

##from Configuration.StandardSequences.FrontierConditions_GlobalTag_cff import * # DB v1
from Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff import *  #DB v2, at least since GR_E_V42

##GlobalTag.globaltag = 'GR_R_311_V1::All'  ## For online
##GlobalTag.globaltag = 'GR_E_V33A::All'  ## For Express 53X>=538HI 
##GlobalTag.globaltag = 'GR_E_V47::All' ## For Express >=741
GlobalTag.globaltag = 'GR_E_V47' ## With DB V2






unpackers  = cms.Sequence(dtunpacker + dttfunpacker)
reco       = cms.Sequence(dt1DRecHits * dt2DSegments * dt4DSegments)
###globalreco = cms.Sequence(CosmicMuonSeedBarrelOnly * offlineBeamSpot * cosmicMuonsBarrelOnly)
globalreco = cms.Sequence(CosmicMuonSeed*offlineBeamSpot*cosmicMuons)


#######################################################################################
# DT DPG DQM modules follow

from UserCode.DTDPGAnalysis.DTOfflineAnalyzer_cfi import *
DTOfflineAnalyzer.SALabel='cosmicMuons'
from UserCode.DTDPGAnalysis.STAOfflineAnalyzer_cfi import *
STAOfflineAnalyzer.SALabel='cosmicMuons'
from UserCode.DTDPGAnalysis.DTEffOfflineAnalyzer_cfi import *

from DQMServices.Components.MEtoEDMConverter_cfi import *
from DQMServices.Core.DQM_cfg import *

from DQM.DTMonitorModule.dtDataIntegrityTask_cfi import *
DTDataIntegrityTask.dtDDULabel = 'dtunpacker'   ## Needed from, at least, 710  
DTDataIntegrityTask.dtROS25Label = 'dtunpacker' ## Needed from, at least, 710  

from DQM.DTMonitorModule.dtDigiTask_cfi import *
dtDigiMonitor.readDB = True
dtDigiMonitor.doNoiseOccupancies = True
dtDigiMonitor.doInTimeOccupancies = True

from DQM.DTMonitorModule.dtTriggerTask_cfi import *
dtTriggerMonitor.process_dcc = True
dtTriggerMonitor.dcc_label   = 'dttfunpacker'
dtTriggerMonitor.process_seg = True

from DQM.DTMonitorModule.dtEfficiencyTask_cfi import *
from DQM.DTMonitorModule.dtChamberEfficiencyTask_cfi import *
from DQM.DTMonitorModule.dtResolutionTask_cfi import *

from DQM.DTMonitorModule.dtSegmentTask_cfi import *
dtSegmentAnalysisMonitor.detailedAnalysis = True

dummyProducer = cms.EDProducer("ThingWithMergeProducer")

from DQM.L1TMonitor.L1TGMT_cfi import *

###sources = cms.Sequence( dummyProducer + dtDigiMonitor + dtTriggerMonitor + dtEfficiencyMonitor + dtChamberEfficiencyMonitor + dtSegmentAnalysisMonitor + dtResolutionAnalysisMonitor)
## From, at least, 710 DTDataIntegrityTask MUST be included also in the sources if not the folders 00-DataIntegrity and FEDIntegrity are missing
sources = cms.Sequence( dummyProducer + DTDataIntegrityTask + dtDigiMonitor + dtTriggerMonitor + dtEfficiencyMonitor + dtChamberEfficiencyMonitor + dtSegmentAnalysisMonitor + dtResolutionAnalysisMonitor + l1tGmt)


analysis = cms.Sequence(DTOfflineAnalyzer + DTEffOfflineAnalyzer + STAOfflineAnalyzer)

