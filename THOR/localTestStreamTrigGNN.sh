#!/bin/bash

DATATYPE="JET"

# Local
#EVTFLAG="-n 1000"
#INDIR="/eos/atlas/atlascerngroupdisk/perf-tau/TestxAODs/MC23/trig"
#thor THOR/share/StreamTrigGNN/Main.py ${EVTFLAG} -i ${INDIR} --trigger --triggerName HLT_tau20_perf_tracktwoMVA_L1eTAU12 --inputtrigtauscontainername HLT_TrigTauRecMerged_MVA --datatype ${DATATYPE}

# # Grid
VERSION="mc23c"
INPUTFILES="input_files.txt"
thor THOR/share/StreamTrigGNN/Main.py -r grid -g ${INPUTFILES} --trigger --triggerName HLT_tau20_idperf_tracktwoMVA_L1eTAU12 --inputtrigtauscontainername HLT_TrigTauRecMerged_MVA --gridstreamname TauID --gridrunversion ${VERSION} --datatype ${DATATYPE} --nFilesPerJob 20 

