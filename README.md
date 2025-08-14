# atlas-hlt-gntau

## THOR (AOD->MxAOD)
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

## ntupler (MxAOD->ntuple)
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

## ntup_to_h5
convert ntuple to h5 file, source repo at https://gitlab.cern.ch/asudhaka/online-tau-id
```
python ntup_to_h5.py --config ntup_to_h5_config.yaml
```
adapt using scripts in ntup_to_h5 folder here
- comment out irrelevant/unavailable variables and change paths in `ntup_to_h5_config.yaml`
- note the invalid cells/tracks are padded with np.nan according to the last variable in the corresponding list (to avoid padding the valid ones as well). e.g. `TauTracks.fakeScoreRNN` and etc. should be commented out since these are all nan

## truth labeling and splits, source repo at https://gitlab.cern.ch/asudhaka/online-tau-id
apply selection cuts, split into signal tau jets and background jets with different prongness
```
python cuts_and_prongs.py -p [0,1,m] -s ['Signal','Background']
```
adapt using scripts in cuts_and_prongs folder here
- selection and input/output paths in `cuts_and_prongs.py`
