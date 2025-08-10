#include "ntupler/constructor.h"


// constructor
constructor::constructor (const std::string& name,
                      ISvcLocator *pSvcLocator)
   : EL::AnaAlgorithm (name, pSvcLocator)
{
   declareProperty( "decoTruth", m_deco_truth = false,
                    "Add truth info to output tree" );
   declareProperty( "decoRnnScore", m_deco_rnnscore = false,
                    "Add rnn scores to output tree" );
}

StatusCode constructor::initialize()
{
   ANA_CHECK( book( TTree("tautree", "Tree full of taus") ) );
   TTree* tautree = tree("tautree");

   tautree->Branch("TauJets.mcEventNumber", &m_mcEventNumber);
   tautree->Branch("TauJets.mcChannelNumber", &m_mcChannelNumber);
   tautree->Branch("TauJets.mcEventWeight", &m_mcEventWeight);
   tautree->Branch("TauJets.nTracks", &m_nTracks);
   tautree->Branch("TauJets.nTracksIsolation", &m_nTracksIsolation);
   tautree->Branch("TauJets.pt", &m_pt);
   tautree->Branch("TauJets.eta", &m_eta);
   tautree->Branch("TauJets.phi", &m_phi);
   tautree->Branch("TauJets.ptJetSeed", &m_ptJetSeed);
   tautree->Branch("TauJets.etaJetSeed", &m_etaJetSeed);
   tautree->Branch("TauJets.phiJetSeed", &m_phiJetSeed);

   // RNNJetScore
   if (m_deco_rnnscore) {
       //tautree->Branch("TauJets.RNNJetScore_experimental", &m_RNNJetScore_experimental);
       tautree->Branch("TauJets.RNNJetScore", &m_RNNJetScore);
       tautree->Branch("TauJets.GNTauScore", &m_GNTauScore);
       tautree->Branch("TauJets.GNTauScoreSigTrans", &m_GNTauScore);
       tautree->Branch("TauJets.RNNJetScoreSigTrans", &m_RNNJetScoreSigTrans);
       tautree->Branch("TauJets.Offline_RNNJetScore", &m_Offline_RNNJetScore);
       tautree->Branch("TauJets.Offline_RNNJetScoreSigTrans", &m_Offline_RNNJetScoreSigTrans);
   }

   // Truth variables
   if (m_deco_truth) {
       tautree->Branch("TauJets.truthProng", &m_truthProng,
                      "TauJets.truthProng/l");
       tautree->Branch("TauJets.truthEtaVis", &m_truthEtaVis);
       tautree->Branch("TauJets.truthPtVis", &m_truthPtVis);
       tautree->Branch("TauJets.IsTruthMatched", &m_IsTruthMatched);
       tautree->Branch("TauJets.truthDecayMode", &m_truthDecayMode,
                      "TauJets.truthProng/l");
       tautree->Branch("TauJets.truthRdecay", &m_truthRdecay);
      //  tautree->Branch("TauJets.truthRprod", &m_truthRprod);
      // tautree->Branch("TauJets.truthOriginPdgId", &m_truthOriginPdgId);
       tautree->Branch("TauJets.IsHadronicTau", &m_IsHadronicTau);
//       tautree->Branch("TauJets.truthParticleOrigin", &m_truthParticleOrigin);
      // tautree->Branch("TauJets.truthParticleType", &m_truthParticleType);
   }

   // Variables for regular ID
   tautree->Branch("TauJets.mu", &m_mu);
   tautree->Branch("TauJets.nVtxPU", &m_nVtxPU);
   tautree->Branch("TauJets.centFrac", &m_centFrac);
   tautree->Branch("TauJets.isolFrac", &m_isolFrac);
   tautree->Branch("TauJets.EMPOverTrkSysP", &m_EMPOverTrkSysP);
   tautree->Branch("TauJets.innerTrkAvgDist", &m_innerTrkAvgDist);
   tautree->Branch("TauJets.ptRatioEflowApprox", &m_ptRatioEflowApprox);
   tautree->Branch("TauJets.dRmax", &m_dRmax);
   tautree->Branch("TauJets.trFlightPathSig", &m_trFlightPathSig);
   tautree->Branch("TauJets.mEflowApprox", &m_mEflowApprox);
   tautree->Branch("TauJets.SumPtTrkFrac", &m_SumPtTrkFrac);
   tautree->Branch("TauJets.absipSigLeadTrk", &m_absipSigLeadTrk);
   tautree->Branch("TauJets.massTrkSys", &m_massTrkSys);
   tautree->Branch("TauJets.etOverPtLeadTrk", &m_etOverPtLeadTrk);
   tautree->Branch("TauJets.ptDetectorAxis", &m_ptDetectorAxis);
   tautree->Branch("TauJets.ptFinalCalib", &m_ptFinalCalib);

   // Track variables
   tautree->Branch("TauTracks.pt", &m_trk_pt);
   tautree->Branch("TauTracks.eta", &m_trk_eta);
   tautree->Branch("TauTracks.phi", &m_trk_phi);
   tautree->Branch("TauTracks.dEta", &m_trk_dEta);
   tautree->Branch("TauTracks.dPhi", &m_trk_dPhi);
   tautree->Branch("TauTracks.z0sinthetaTJVA", &m_trk_z0sinthetaTJVA);
   tautree->Branch("TauTracks.z0sinthetaSigTJVA", &m_trk_z0sinthetaSigTJVA);
   tautree->Branch("TauTracks.d0TJVA", &m_trk_d0TJVA);
   tautree->Branch("TauTracks.d0SigTJVA", &m_trk_d0SigTJVA);
   tautree->Branch("TauTracks.nInnermostPixelHits", &m_trk_nInnermostPixelHits);
   tautree->Branch("TauTracks.expectInnermostPixelLayerHit", &m_trk_expectInnermostPixelLayerHit);
   tautree->Branch("TauTracks.nIBLHitsAndExp", &m_trk_nIBLHitsAndExp);
   tautree->Branch("TauTracks.nPixelHits", &m_trk_nPixelHits);
   tautree->Branch("TauTracks.nPixelHitsPlusDeadSensors", &m_trk_nPixelHitsPlusDeadSensors);
   tautree->Branch("TauTracks.nSCTHits", &m_trk_nSCTHits);
   tautree->Branch("TauTracks.nSCTHitsPlusDeadSensors", &m_trk_nSCTHitsPlusDeadSensors);
   tautree->Branch("TauTracks.chargedScoreRNN", &m_trk_chargedScoreRNN);
   tautree->Branch("TauTracks.isolationScoreRNN", &m_trk_isolationScoreRNN);
   tautree->Branch("TauTracks.conversionScoreRNN", &m_trk_conversionScoreRNN);
   tautree->Branch("TauTracks.fakeScoreRNN", &m_trk_fakeScoreRNN);

   // Cluster variables
   tautree->Branch("TauClusters.e", &m_cls_e);
   tautree->Branch("TauClusters.et", &m_cls_et);
   tautree->Branch("TauClusters.eta", &m_cls_eta);
   tautree->Branch("TauClusters.phi", &m_cls_phi);
   tautree->Branch("TauClusters.dEta", &m_cls_dEta);
   tautree->Branch("TauClusters.dPhi", &m_cls_dPhi);
   tautree->Branch("TauClusters.SECOND_R", &m_cls_SECOND_R);
   tautree->Branch("TauClusters.CENTER_LAMBDA", &m_cls_CENTER_LAMBDA);
   tautree->Branch("TauClusters.SECOND_LAMBDA", &m_cls_SECOND_LAMBDA);
   tautree->Branch("TauClusters.CENTER_MAG", &m_cls_CENTER_MAG);
   tautree->Branch("TauClusters.FIRST_ENG_DENS", &m_cls_FIRST_ENG_DENS);
   tautree->Branch("TauClusters.EM_PROBABILITY", &m_cls_EM_PROBABILITY);

   return StatusCode::SUCCESS;
}

StatusCode constructor::execute()
{
   // general event info
   ANA_CHECK( evtStore()->retrieve(m_eventInfo, "EventInfo") );

   m_mcEventNumber = m_eventInfo->mcEventNumber();
   m_mcChannelNumber = m_eventInfo->mcChannelNumber();
   m_mcEventWeight = m_eventInfo->mcEventWeight();

   // retrieve taus
   ANA_CHECK( evtStore()->retrieve(m_taus, "TrigTauJets") );
   for (auto tau : *m_taus) {
      m_nTracks = tau->auxdata<int>("nTracks");
      m_nTracksIsolation = tau->auxdata<int>("nTracksIsolation");
      m_pt = tau->pt();
      m_eta = tau->eta();
      m_phi = tau->phi();
      m_ptJetSeed = tau->auxdata<float>("trk_ptJetSeed");
      m_etaJetSeed = tau->auxdata<float>("trk_etaJetSeed");
      m_phiJetSeed = tau->auxdata<float>("trk_phiJetSeed");

      if (m_deco_rnnscore) {
         m_RNNJetScore = tau->auxdata<float>("RNNJetScore");
         m_GNTauScore = tau->auxdata<float>("GNTauScore");
         m_GNTauScore = tau->auxdata<float>("GNTauScoreSigTrans");
         m_RNNJetScoreSigTrans = tau->auxdata<float>("RNNJetScoreSigTrans");
         m_Offline_RNNJetScore = tau->auxdata<float>("Offline_RNNJetScore");
         m_Offline_RNNJetScoreSigTrans = tau->auxdata<float>("Offline_RNNJetScoreSigTrans");
      }

      // Truth variables
      if (m_deco_truth) {
         // m_truthJetPdgId = tau->auxdata<int>("truthOriginPdgId");
         m_truthProng = tau->auxdata<unsigned long>("truthProng");
         m_truthEtaVis = tau->auxdata<double>("truthEtaVisDressed");
         m_truthPtVis = tau->auxdata<double>("truthPtVisDressed");
         m_IsTruthMatched = tau->auxdata<char>("IsTruthMatched");
         m_truthDecayMode = tau->auxdata<unsigned long>("truthDecayMode");
         m_truthRdecay = tau->auxdata<float>("truthRdecay");
         // m_truthRprod = tau->auxdata<float>("truthRprod");
         m_IsHadronicTau = tau->auxdata<char>("IsHadronicTau");
 //        m_truthParticleOrigin = tau->auxdata<unsigned int>("truthParticleOrigin");
        // m_truthParticleType = tau->auxdata<unsigned int>("truthParticleType");
         //m_truthOriginPdgId = tau->auxdata<int>("truthOriginPdgId");
      }

      // Variables for regular ID
      m_mu = tau->auxdata<float>("mu");
      m_nVtxPU = tau->auxdata<int>("nVtxPU");
      m_centFrac = tau->auxdata<float>("centFrac");
      m_isolFrac = tau->auxdata<float>("isolFrac");
      m_EMPOverTrkSysP = tau->auxdata<float>("EMPOverTrkSysP");
      m_innerTrkAvgDist = tau->auxdata<float>("innerTrkAvgDist");
      m_ptRatioEflowApprox = tau->auxdata<float>("ptRatioEflowApprox");
      m_dRmax = tau->auxdata<float>("dRmax");
      m_trFlightPathSig = tau->auxdata<float>("trFlightPathSig");
      m_mEflowApprox = tau->auxdata<float>("mEflowApprox");
      m_SumPtTrkFrac = tau->auxdata<float>("SumPtTrkFrac");
      m_absipSigLeadTrk = m_nTracks > 0 ? TMath::Abs( ( tau->auxdata<vfloat>("trk_d0SigTJVA") ).at(0) ) : -1.;
      m_massTrkSys = tau->auxdata<float>("massTrkSys");
      m_etOverPtLeadTrk = tau->auxdata<float>("etOverPtLeadTrk");
      m_ptDetectorAxis = tau->auxdata<float>("ptDetectorAxis");
      m_ptFinalCalib = tau->auxdata<float>("ptFinalCalib");

      // Track variables
      m_trk_pt = tau->auxdata<vfloat>("trk_pt");
      m_trk_eta = tau->auxdata<vfloat>("trk_eta");
      m_trk_phi = tau->auxdata<vfloat>("trk_phi");
      m_trk_dEta = tau->auxdata<vfloat>("trk_dEta");
      m_trk_dPhi = tau->auxdata<vfloat>("trk_dPhi");
      m_trk_z0sinthetaTJVA = tau->auxdata<vfloat>("trk_z0sinthetaTJVA");
      m_trk_z0sinthetaSigTJVA = tau->auxdata<vfloat>("trk_z0sinthetaSigTJVA");
      m_trk_d0TJVA = tau->auxdata<vfloat>("trk_d0TJVA");
      m_trk_d0SigTJVA = tau->auxdata<vfloat>("trk_d0SigTJVA");
      m_trk_nInnermostPixelHits = tau->auxdata<vuint8>("trk_nInnermostPixelHits");
      m_trk_expectInnermostPixelLayerHit = tau->auxdata<vuint8>("trk_expectInnermostPixelLayerHit");
      m_trk_nIBLHitsAndExp = tau->auxdata<vuint8>("trk_nIBLHitsAndExp");
      m_trk_nPixelHits = tau->auxdata<vuint8>("trk_nPixelHits");
      m_trk_nPixelHitsPlusDeadSensors = tau->auxdata<vuint8>("trk_nPixelHitsPlusDeadSensors");
      m_trk_nSCTHits = tau->auxdata<vuint8>("trk_nSCTHits");
      m_trk_nSCTHitsPlusDeadSensors = tau->auxdata<vuint8>("trk_nSCTHitsPlusDeadSensors");
      m_trk_chargedScoreRNN = tau->auxdata<vfloat>("trk_chargedScoreRNN");
      m_trk_isolationScoreRNN = tau->auxdata<vfloat>("trk_isolationScoreRNN");
      m_trk_conversionScoreRNN = tau->auxdata<vfloat>("trk_conversionScoreRNN");
      m_trk_fakeScoreRNN = tau->auxdata<vfloat>("trk_fakeScoreRNN");

      // Cluster variables
      m_cls_e = tau->auxdata<vfloat>("cls_e");
      m_cls_et = tau->auxdata<vfloat>("cls_et");
      m_cls_eta = tau->auxdata<vfloat>("cls_eta");
      m_cls_phi = tau->auxdata<vfloat>("cls_phi");
      m_cls_dEta = tau->auxdata<vfloat>("cls_dEta");
      m_cls_dPhi = tau->auxdata<vfloat>("cls_dPhi");
      m_cls_SECOND_R = tau->auxdata<vfloat>("cls_SECOND_R");
      m_cls_CENTER_LAMBDA = tau->auxdata<vfloat>("cls_CENTER_LAMBDA");
      m_cls_SECOND_LAMBDA = tau->auxdata<vfloat>("cls_SECOND_LAMBDA");
      m_cls_CENTER_MAG = tau->auxdata<vfloat>("cls_CENTER_MAG");
      m_cls_FIRST_ENG_DENS = tau->auxdata<vfloat>("cls_FIRST_ENG_DENS");
      m_cls_EM_PROBABILITY = tau->auxdata<vfloat>("cls_EM_PROBABILITY");

      tree("tautree")->Fill();
   }


   return StatusCode::SUCCESS;
}

StatusCode constructor::finalize()
{
   return StatusCode::SUCCESS;
}

constructor::~constructor(){
}

