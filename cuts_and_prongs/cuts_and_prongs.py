import pandas as pd
import numpy as np
import h5py
import os, glob
import tqdm
import argparse
import os

def get_parser():
    """
    Argument parser for Preprocessing script.

    Returns
    -------
    args: parse_args
    """
    parser = argparse.ArgumentParser(description="Converting command line options.")

    parser.add_argument(
        "-p",
        "--nProngs",
        type=str,
        choices=['0', '1', '3', 'm'],
        required=True,
        help="Number of prongs for the dataset [0, 1, 3, m]",
    )

    parser.add_argument(
        "-s",
        "--Sample",
        type=str,
        choices=['Signal', 'Background', 'All'],
        required=True,
        default='All',
        help="Type of sample to be processed [Signal, Background, All]",
    )
    return parser.parse_args()



def GetBatchesPerFile(filename: str, batch_size = 500000):
    """
    Split the file into batches to avoid that the loaded data is too large.

    Parameters
    ----------
    filename : str
        name of file to be split in batches

    Returns
    -------
    str
        filename
    list
        tuples of start and end index of batch

    """
    with h5py.File(filename, "r") as data_set:
        # get total number of jets in file
        total_n_jets = len(data_set["jets"])
        # first tuple is given by (0, batch_size)
        start_batch = 0
        end_batch = batch_size
        indices_batches = [(start_batch, end_batch)]
        # get remaining tuples of indices defining the batches
        while end_batch <= total_n_jets:
            start_batch += batch_size
            end_batch = start_batch + batch_size
            indices_batches.append((start_batch, end_batch))
    return (filename, indices_batches)

def building_new(var, label, first_array):
    new_array = np.zeros(
        first_array.shape, 
        dtype=(first_array.dtype.descr + [(label, '<f4')]))
    existing_keys = list(first_array.dtype.fields.keys())
    new_array[existing_keys] = first_array[existing_keys]
    new_array[label] = var
    return new_array

def jets_generator(files_in_batches: list, tracks_name = 'tracks', cells_name = 'cells'):
    """
    Helper function to extract jet and track information from a h5 ntuple.

    Parameters
    ----------
    files_in_batches : list
    tuples of filename and tuple of start and end index of batch

    Yields
    -------
    numpy.ndarray
    jets
    numpy.ndarray
    tracks
    numpy.ndarray
    cells
    """
    for filename, batches in files_in_batches:
        with h5py.File(filename, "r") as data_set:
            for batch in batches:
                jets = data_set["jets"][batch[0] : batch[1]]
                tracks = data_set[tracks_name][batch[0] : batch[1]]
                cells = data_set[cells_name][batch[0] : batch[1]]
                yield (jets, tracks, cells)


def split_dataset(input_files, output_file,prongs=0 ,tracks_name='tracks', cells_name = 'cells', n_jets_to_get = 50000, n_jets_per_file=int(1e6),sample='Signal'):
    create_file = True
    jets_curr_file = 0
    _output_file = output_file
    displayed_writing_output = True
    files_in_batches = map(GetBatchesPerFile, input_files)
    pbar = tqdm.tqdm(total=n_jets_to_get)
    output_file = f'{_output_file[:-3]}_{n_jets_to_get // n_jets_per_file}.h5'
    print(f'Writing out {sample} jets with {prongs} prong(s).')
    for jets, tracks, cells in jets_generator(files_in_batches):
        if len(jets) == 0:
            continue
        jets = building_new(np.where((jets['TauJets.IsHadronicTau'] == 1), 5, 0), 'HadronConeExclTruthLabelID', jets)
        # jets = building_new(tracks['tauPt'][:, 0], 'pt', jets)
        # jets = building_new(np.abs(jets['TauJets.eta'][:]), 'absEta', jets)
        # jets = building_new(np.arange(curr_jets, jets.shape[0]), 'eventNumber', jets)
        jets_in_this_file = jets.size
        mainmask = np.ones(len(jets), dtype=bool)
        if sample == 'Signal':
            # Includes both hadronic and Leponic taus (Not used for Tau ID trainings)
            # mainmask = (jets['TauJets.truthOriginPdgId'] == 15) | (jets['TauJets.truthOriginPdgId'] == -15) 
            mainmask = jets['TauJets.IsHadronicTau'] == 1 
        elif sample == 'Background':
            # Doesnt include both hadronic and "Leponic taus" in background (Not used for Tau ID trainings)
            # mainmask = (jets['TauJets.truthJetPdgId'] != 15) & (jets['TauJets.truthJetPdgId'] != -15) 
            mainmask = jets['TauJets.IsHadronicTau'] == 0

        if prongs == '0':
            mask1 = jets['TauJets.pt'] > 20000
            mask2 = jets['TauJets.pt'] < 600000
            mask3 = abs(jets['TauJets.eta']) < 2.5
            mask4 = jets['TauJets.nTracks'] == 0

            mask = mask1 & mask2 & mask3 & mask4 & mainmask
                       
        elif prongs == '1':
            mask1 = jets['TauJets.pt'] > 20000
            mask2 = jets['TauJets.pt'] < 600000
            mask3 = abs(jets['TauJets.eta']) < 2.5
            mask4 = jets['TauJets.nTracks'] == 1
            mask5 = ((jets['TauJets.IsTruthMatched'] == 1) & (abs(jets['TauJets.truthEtaVis']) < 2.5)) | (jets['TauJets.IsHadronicTau'] != 1)
            mask6 = ((jets['TauJets.truthProng'] == 1) | (jets['TauJets.truthProng'] == 3)) | (jets['TauJets.IsHadronicTau'] != 1)

            mask = mask1 & mask2 & mask3 & mask4 & mask5 & mask6 & mainmask
        
        elif prongs == 'm':
            mask1 = jets['TauJets.pt'] > 20000
            mask2 = jets['TauJets.pt'] < 600000
            mask3 = abs(jets['TauJets.eta']) < 2.5
            mask4 = (jets['TauJets.nTracks'] == 2) | (jets['TauJets.nTracks'] == 3)
            mask5 = ((jets['TauJets.IsTruthMatched'] == 1) & (abs(jets['TauJets.truthEtaVis']) < 2.5)) | (jets['TauJets.IsHadronicTau'] != 1)
            mask6 = ((jets['TauJets.truthProng'] == 1) | (jets['TauJets.truthProng'] == 3)) | (jets['TauJets.IsHadronicTau'] != 1)

            mask = mask1 & mask2 & mask3 & mask4 & mask5 & mask6 & mainmask

        jets = jets[mask]
        tracks = tracks[mask]
        cells = cells[mask]
        
        pbar.update(jets_in_this_file)
        n_jets_to_get -= jets.size
        if jets_curr_file >= n_jets_per_file:
             create_file = True
             jets_curr_file = 0
             output_file = f'{_output_file[:-3]}_{n_jets_to_get // n_jets_per_file}.h5'
        else:
             jets_curr_file += jets.size
        if create_file:
            pbar.write("Creating output file: " + output_file)
            create_file = False  # pylint: disable=W0201:
            # write to file by creating dataset
            with h5py.File(output_file, "w") as out_file:
                out_file.create_dataset(
                    "jets",
                    data=jets,
                    compression="gzip",
                    chunks=True,
                    maxshape=(None,),
                )
                out_file.create_dataset(
                    tracks_name,
                    data=tracks,
                    compression="gzip",
                    chunks=True,
                    maxshape=(None, tracks.shape[1]),
                )
                out_file.create_dataset(
                    cells_name,
                    data=cells,
                    compression="gzip",
                    chunks=True,
                    maxshape=(None, cells.shape[1]),
                )
        else:
            # appending to existing dataset
            if displayed_writing_output:
                pbar.write("Writing to output file: " + output_file)
            with h5py.File(output_file, "a") as out_file:
                out_file["jets"].resize(
                    (out_file["jets"].shape[0] + jets.shape[0]),
                    axis=0,
                )
                out_file["jets"][-jets.shape[0] :] = jets
                out_file[tracks_name].resize(
                    (
                        out_file[tracks_name].shape[0]
                        + tracks.shape[0]
                    ),
                    axis=0,
                )
                out_file[tracks_name][
                    -tracks.shape[0] :
                ] = tracks
                out_file[cells_name].resize(
                    (
                        out_file[cells_name].shape[0]
                        + cells.shape[0]
                    ),
                    axis=0,
                )
                out_file[cells_name][
                    -cells.shape[0] :
                ] = cells
            displayed_writing_output = False
        if n_jets_to_get <= 0:
            break
    pbar.close()
    


gammatautau_dataset = ['/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/Gtautau.h5']
dijet_dataset = [
                 '/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/JZ1.h5',
                 '/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/JZ2.h5',
                 '/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/JZ3.h5',
                 '/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/JZ4.h5',
]
ttbar_dataset = ['/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/ttbar.h5']
Ztautau_PyPh_dataset = ['/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/Ztautau_PyPh.h5']
Ztautau_Sherpa_dataset = ['/Users/hofungtsoi/Desktop/gntau-train/H5/raw/mc23c/Ztautau_sherpa.h5']

datasets = {
    'gammatautau' : gammatautau_dataset,
    'dijet' : dijet_dataset,
     'ttbar' : ttbar_dataset,
     'Ztautau_PyPh' : Ztautau_PyPh_dataset,
     'Ztautau_Sherpa' : Ztautau_Sherpa_dataset
}

args = get_parser()
prongs = args.nProngs
sample = args.Sample
outpath = {
           'gammatautau':f'/Users/hofungtsoi/Desktop/gntau-train/H5/selection/mc23c/{prongs}p/{sample}/gammatautau/',
           'dijet':f'/Users/hofungtsoi/Desktop/gntau-train/H5/selection/mc23c/{prongs}p/{sample}/dijet/',
            'ttbar':f'/Users/hofungtsoi/Desktop/gntau-train/H5/selection/mc23c/{prongs}p/{sample}/ttbar/',
            'Ztautau_PyPh':f'/Users/hofungtsoi/Desktop/gntau-train/H5/selection/mc23c/{prongs}p/{sample}/Ztautau_PyPh/',
            'Ztautau_Sherpa':f'/Users/hofungtsoi/Desktop/gntau-train/H5/selection/mc23c/{prongs}p/{sample}/Ztautau_Sherpa/'
            }

# Create output directories if they don't exist
for path in outpath.values():
    os.makedirs(path, exist_ok=True)

for samp, samp_files in datasets.items():
    for i, samp_file in enumerate(samp_files):

        # get total number of jets in file
        with h5py.File(samp_file, "r") as data_set:
            total_n_jets = len(data_set["jets"])
        print(f'DATASET: {samp_file} with {total_n_jets} jets')
        split_dataset([samp_file], 
            f'{outpath[samp]}{samp}_samp{i}.h5',
            prongs=prongs,
            n_jets_to_get=total_n_jets, 
            n_jets_per_file=total_n_jets,
            sample=sample)
