#ifndef ntupler_constructor_H
#define ntupler_constructor_H

#include <iostream>
#include <string>
#include <TH1F.h>
#include <TTree.h>
#include <vector>

#include <AnaAlgorithm/AnaAlgorithm.h>
#include <xAODEventInfo/EventInfo.h>
#include <xAODTau/TauJetContainer.h>
class constructor : public EL::AnaAlgorithm
{
   public:
      constructor (const std::string& name, ISvcLocator* pSvcLocator);
      ~constructor () override;

      virtual StatusCode initialize () override;
      virtual StatusCode execute () override;
      virtual StatusCode finalize () override;

   public:
      using vfloat = std::vector<float>;
      using vuint8 = std::vector<uint8_t>;

      // Variables in the output tree
      unsigned long long m_mcEventNumber; //!
      int m_mcChannelNumber; //!
      float m_mcEventWeight; //!
      int m_nTracks; //!
      int m_nTracksIsolation; //!
      int m_nTracksFailTrackFilter; //!
      float m_pt; //!
      float m_eta; //!
      float m_phi; //!
      float m_ptJetSeed; //!
      float m_etaJetSeed; //!
      float m_phiJetSeed; //!

      // RNN Score
      float m_RNNJetScore;
      float m_GNTauScore;
      float m_GNTauScoreSigTrans;
      float m_RNNJetScoreSigTrans;
      float m_Offline_RNNJetScoreSigTrans;
      float m_Offline_RNNJetScore;

      // Truth variables
      unsigned long m_truthProng; //!
      double m_truthEtaVis; //!
      double m_truthPtVis; //!
      char m_IsTruthMatched; //!
      unsigned long m_truthDecayMode; //!
      float m_truthRdecay; //!
      // float m_truthRprod; //!
      //unsigned int m_truthParticleType; //!
      //unsigned int m_truthParticleOrigin; //!
      char m_IsHadronicTau; //!
      //int m_truthOriginPdgId; //!
  
      // Variables for regular ID
      double m_mu; //!
      int m_nVtxPU; //!
      float m_centFrac; //!
      float m_isolFrac; //!
      float m_EMPOverTrkSysP; //!
      float m_innerTrkAvgDist; //!
      float m_ptRatioEflowApprox; //!
      float m_dRmax; //!
      float m_trFlightPathSig; //!
      float m_mEflowApprox; //!
      float m_SumPtTrkFrac; //!
      float m_absipSigLeadTrk; //!
      float m_massTrkSys; //!
      float m_etOverPtLeadTrk; //!
      float m_ptDetectorAxis; //!
      float m_ptFinalCalib; //!
      int m_truthJetPdgId; //!

      // Track variables
      vfloat m_trk_pt; //!
      vfloat m_trk_eta; //!
      vfloat m_trk_phi; //!
      vfloat m_trk_dEta; //!
      vfloat m_trk_dPhi; //!
      vfloat m_trk_z0sinthetaTJVA; //!
      vfloat m_trk_z0sinthetaSigTJVA; //!
      vfloat m_trk_d0TJVA; //!
      vfloat m_trk_d0SigTJVA; //!
      vfloat m_trk_chargedScoreRNN; //!
      vfloat m_trk_isolationScoreRNN; //!
      vfloat m_trk_conversionScoreRNN; //!
      vfloat m_trk_fakeScoreRNN; //!
      vuint8 m_trk_nInnermostPixelHits; //!
      vuint8 m_trk_expectInnermostPixelLayerHit; //!
      vuint8 m_trk_nIBLHitsAndExp; //!
      vuint8 m_trk_nPixelHits; //!
      vuint8 m_trk_nPixelHitsPlusDeadSensors; //!
      vuint8 m_trk_nSCTHits; //!
      vuint8 m_trk_nSCTHitsPlusDeadSensors; //!
      vuint8 m_trk_isLoose; //!
      vuint8 m_trk_passVertexCut; //!

      // Cluster variables
      vfloat m_cls_e; //!
      vfloat m_cls_et; //!
      vfloat m_cls_eta; //!
      vfloat m_cls_phi; //!
      vfloat m_cls_dEta; //!
      vfloat m_cls_dPhi; //!
      vfloat m_cls_SECOND_R; //!
      vfloat m_cls_CENTER_LAMBDA; //!
      vfloat m_cls_SECOND_LAMBDA; //!
      vfloat m_cls_CENTER_MAG; //!
      vfloat m_cls_FIRST_ENG_DENS; //!
      vfloat m_cls_EM_PROBABILITY; //!

   private:
      const xAOD::EventInfo *m_eventInfo = nullptr;
      const xAOD::TauJetContainer *m_taus = nullptr;

   protected:
      // For the output tree
      bool m_deco_truth;
      bool m_deco_rnnscore;
};

#endif
