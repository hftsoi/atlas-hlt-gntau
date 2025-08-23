# atlas-hlt-gntau

<details>
  <summary>THOR (AOD->MxAOD)</summary>
    
  THOR framework to extract tau jet info, source repo at https://gitlab.cern.ch/atlas-perf-tau/THOR
  ```
  mkdir THOR
  cd THOR
  git clone https://gitlab.cern.ch/atlas-perf-tau/THOR.git
  cd THOR
  source setup.sh
  sh THOR/prod/localTestStreamTrigGNN.sh
  ```
  adapt using scripts in THOR folder here
  - no tau perf chains in current phase2 samples -> use idperf for all
  - input files mc23c/pu140/pu200
  - modify stream dependent cut for phase2 samples: tau jet abs(eta) < 2.5 -> 4.0 (auto for Upgrade stream but we are doing TrigGNN stream)
</details>

<details>
  <summary>ntupler (MxAOD->ntuple)</summary>
    
  ntupler framework to produce ntuple from MxAOD using event loop, source repo at https://gitlab.cern.ch/soerdek/ntupler
  ```
  mkdir ntupler
  cd ntupler
  git clone https://gitlab.cern.ch/soerdek/ntupler.git
  cd ntupler
  source setup.sh
  plant.py -m [path to MxAOD] -i [path to sample] -s [path to output] --truth --rnnscore
  ```
  adapt using scripts in ntupler folder here
  - comment out irrelevant/unavailable variables in `constructor.cxx` and `constructor.h`, such as `m_truthParticleOrigin`
  - output ntuple in `output_path/data-ANALYSIS/`
</details>

<details>
  <summary>ntup_to_h5</summary>
    
  convert ntuple to h5 file, source repo at https://gitlab.cern.ch/asudhaka/online-tau-id
  ```
  python ntup_to_h5.py --config ntup_to_h5_config.yaml
  ```
  adapt using scripts in ntup_to_h5 folder here
  - comment out irrelevant/unavailable variables and change paths in `ntup_to_h5_config.yaml`
  - note the invalid cells/tracks are padded with np.nan according to the last variable in the corresponding list (to avoid padding the valid ones as well). e.g. `TauTracks.fakeScoreRNN` and etc. should be commented out since these are all nan
</details>

<details>
  <summary>truth labeling and splits</summary>
  
  apply selection cuts, split into signal tau jets and background jets with different prongness, source repo at https://gitlab.cern.ch/asudhaka/online-tau-id
  ```
  python cuts_and_prongs.py -p [0,1,m] -s ['Signal','Background']
  ```
  adapt using scripts in cuts_and_prongs folder here
  - selection and input/output paths in `cuts_and_prongs.py`
</details>

<details>
  <summary>umami preprocessing</summary>
  
  resample jets so the kinematic distributions like pt and eta match between signal and bkg (remove bias from input jet pt and eta), then split into train/val/test, source repo at https://umami-hep.github.io/umami-preprocessing/run/
  ```
  # pip install umami-preprocessing
  preprocess --config config.yaml --split all
  ```
  adapt using scripts in umami folder here
  - input jet variables in `tau-variables_1p.yaml` etc.
  - resampling and split configs in `config_1p.yaml` etc.
    - use modulo to do first splitting under `global_cuts`
    - set final # of jets per set per sig/bkg after resampling under `components`
    - define binning and method for resampling under `resampling`
    - set # of jets to do resampling under `global`
</details>

<details>
  <summary>salt training</summary>
  
  define salt model and train, source repo at https://ftag-salt.docs.cern.ch/
  ```
  # pip install salt-ml
  salt fit --config GN2_like_models/config_GN2Tau_1p.yaml --force --data.num_workers=0
  salt test --config mc23c/1p/GNTau_SC4_HP0_20250816-T120141/config.yaml
  ```
  adapt using scripts in salt folder here
  - define model and training config in `config_GN2Tau_1p.yaml` etc.
  - create Comet account for logging and monitoring, put the account api key into the yaml file
</details>
