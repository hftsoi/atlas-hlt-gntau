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
