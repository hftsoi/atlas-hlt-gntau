import argparse
import glob
import os
import yaml
import h5py
import numpy as np
import uproot
from numpy.lib.recfunctions import unstructured_to_structured
from numpy import nan
from tqdm import tqdm

def get_parser():
    """
    Argument parser for Preprocessing script.

    Returns
    -------
    args: parse_args
    """
    parser = argparse.ArgumentParser(description="Converting command line options.")

    parser.add_argument(
        "-c",
        "--config_file",
        type=str,
        required=True,
        help="Enter the name of the config file to convert the sample.",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        default=None,
        help="Enter the name of the input file or folder to overwrite the one specified in the config file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default=None,
        help="Enter the name of the output file to overwrite the one specified in the config file.",
    )

    parser.add_argument(
        "-n",
        "--njets",
        type=int,
        required=False,
        default=None,
        help="Enter the number of jets to be processed.",
    )

    return parser.parse_args()


class PrepareSamples:
    """
    This class is preparing the samples for further processing defined in the
    configuration file:
        - writes these iteratively to h5 output files
        - uses the information provided in the preprocessing config.
    """

    def __init__(self, config, args):
        """Preparation of h5 samples.

        Parameters
        ----------
        args : parse_args
            command line arguments
        config : config class
            preprocessing configuration class containing all info about preprocessing
        """
        self.config = config
        self.input = args.input
        self.output = args.output
        self.n_jets = args.njets
        self.rnd_seed = 42
        self.run_all = False
        self.__setup()

    def __setup(self):
        """Setting up preparation class

        Parameters
        ----------

        Raises
        ------
        KeyError
            if no samples defined in preprocessing config
        KeyError
            if specified sample not in preprocessing configuration
        KeyError
            if requested sample category not defined in global config
        """
        # Variables and input file check
        self.track_variables = self.config["variables"]["track_variables"]
        self.cell_variables = self.config["variables"]["cell_variables"]
        self.jet_variables = self.config["variables"]["jet_variables"]
        if self.input is not None:
            if os.path.isfile(self.input):
                self.input_files = [self.input]
            elif os.path.isdir(self.input):
                self.input_files = glob.glob(self.input + "/*.root")
            else:
                raise ValueError("--input argument is neither file nor folder!")
        else:
            self.input_files = glob.glob(self.config['input_folder'] + "/*.root")
        self.tree_name = self.config.get("tree_name", "tautree")

        # Output configs
        self.batchsize = self.config.get("batch_size", 100000)
        if self.input is not None:
            self.output_name = self.output
        else:
            self.output_name = self.config['output']['output_name']
        if self.n_jets is None:
            self.n_jets = int(float(self.config['output']['n_jets']))
        self.max_tracks = self.config['output']['max_tracks']
        self.max_cells = self.config['output']['max_cells']
        self.shuffle_array = self.config['output']['shuffle_array']
        self.samplename = self.config['input_folder'].split("/")[-1]
        if self.n_jets == -1:
            self.run_all = True

        # bookkeeping variables for running over the ntuples
        self.jets_loaded = 0
        self.create_file = True

    def get_batches_per_file(self, filename: str):
        """
        Split the file into batches to avoid that the loaded data is too large.

        Parameters
        ----------
        filename : str
            name of ROOT file to be split in batches

        Returns
        -------
        str
            filename
        list
            tuples of start and end index of batch

        """
        with uproot.open(filename) as rootfile:
            # get total number of jets in file
            total_n_jets = rootfile[self.tree_name].num_entries
            if self.n_jets > total_n_jets or self.n_jets == -1:
                self.n_jets = total_n_jets
            else:
                total_n_jets = self.n_jets
            # first tuple is given by (0, batch_size)
            start_batch = 0
            end_batch = self.batchsize
            indices_batches = [(start_batch, end_batch)]
            # get remaining tuples of indices defining the batches
            while end_batch <= total_n_jets:
                start_batch += self.batchsize
                end_batch = start_batch + self.batchsize
                indices_batches.append((start_batch, end_batch))
        return (filename, indices_batches)

    def jets_generator(self, files_in_batches: list) -> tuple:
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
        """
        def convert(el):
            return np.array(el)[0]

        for filename, batches in files_in_batches:
            with uproot.open(filename) as rootfile:
                for batch in batches:
                    # load jets in batches
                    jets = rootfile[self.tree_name].arrays(
                        self.jet_variables,
                        entry_start=batch[0],
                        entry_stop=batch[1],
                        library="np",
                    )
                    tracks = rootfile[self.tree_name].arrays(
                        self.track_variables,
                        entry_start=batch[0],
                        entry_stop=batch[1],
                        library="np",
                    )
                    cells = rootfile[self.tree_name].arrays(
                        self.cell_variables,
                        entry_start=batch[0],
                        entry_stop=batch[1],
                        library="np",
                    )

                    yield jets, tracks, cells

    def _convert_jets(self, jets):
        jet_dtypes = []
        jets_output = []
        for key in jets.keys():
            if key != "TauJets.mcEventNumber":
                jet_dtypes.append((key, "f4"))
            else:
                jet_dtypes.append((key, "int"))
            jets_output.append(np.array([arr for arr in jets[key]]))
        if self.config["output"]["include_sample_info"]:
            jet_dtypes.append(("TauJets.Sample", "int"))
            jets_output.append(np.full(len(jets[key]),self.config["sample_info"][self.samplename]))
        return unstructured_to_structured(
            np.stack(jets_output, axis=-1), dtype=np.dtype(jet_dtypes)
        )

    def _convert_constituents(self, array, max_size):
        dtypes = []
        output = []
        for key in array.keys():
            output.append(
                np.array(
                    [
                        np.pad(
                            arr[:max_size].astype(np.float32),
                            (0, max_size - len(arr[:max_size])),
                            "constant",
                            constant_values=nan,
                        )
                        if arr.size > 0 else [nan for _ in range(max_size)]
                        for arr in array[key]
                    ]
                )
            )
            dtypes.append((key, "f4"))
        output.append(np.isfinite(output[-1]) * 1)
        dtypes.append(("valid", "bool"))
        return unstructured_to_structured(
            np.stack(output, axis=-1), dtype=np.dtype(dtypes)
        )

    def run(self):
        """Run over Ntuples to extract jets, tracks and cells."""
        # get list of batches for each file
        files_in_batches = [self.get_batches_per_file(file) for file in self.input_files]
        tot = 0
        for file in self.input_files:
            with uproot.open(file) as rootfile:
                tot += rootfile[self.tree_name].num_entries

        if self.run_all:
            pbar = tqdm(total=tot)
        
        else:
            pbar = tqdm(total=self.n_jets)

        rem_jets = tot
        # loop over batches for all files and load the batches separately
        displayed_writing_output = True
        for jets, tracks, cells in self.jets_generator(files_in_batches):

            jets = self._convert_jets(jets)
            tracks = self._convert_constituents(tracks, self.max_tracks)
            cells = self._convert_constituents(cells, self.max_cells)
            pbar.update(jets.size)
            pbar.refresh()
            self.jets_loaded += jets.size
            pbar.write("{} / {} jets converted ({}%)".format(self.jets_loaded, tot, 100 * self.jets_loaded / tot))
            self.n_jets -= jets.size
            rem_jets -= jets.size
            if self.shuffle_array:
                pbar.write("Shuffling array")

                # Init a index list
                rng_index = np.arange(len(jets))

                # Shuffle the index list
                rng = np.random.default_rng(seed=self.rnd_seed)
                rng.shuffle(rng_index)

                # Shuffle jets (and tracks)
                jets = jets[rng_index]
                tracks = tracks[rng_index]
                cells = cells[rng_index]

            if self.create_file:
                self.create_file = False
                # write to file by creating dataset
                pbar.write(f"Creating output file: {self.output_name}")
                with h5py.File(self.output_name, "w") as out_file:
                    out_file.create_dataset(
                        "jets",
                        data=jets,
                        compression="gzip",
                        chunks=True,
                        maxshape=(None,),
                    )
                    out_file.create_dataset(
                        "tracks",
                        data=tracks,
                        compression="gzip",
                        chunks=True,
                        maxshape=(None, tracks.shape[1]),
                    )
                    out_file.create_dataset(
                        "cells",
                        data=cells,
                        compression="gzip",
                        chunks=True,
                        maxshape=(None, cells.shape[1]),
                    )
            else:
                # appending to existing dataset
                if displayed_writing_output:
                    pbar.write(f"Writing to output file: {self.output_name}")
                with h5py.File(self.output_name, "a") as out_file:
                    out_file["jets"].resize(
                        (out_file["jets"].shape[0] + jets.shape[0]),
                        axis=0,
                    )
                    out_file["jets"][-jets.shape[0]:] = jets
                    out_file["tracks"].resize(
                        (out_file["tracks"].shape[0] + tracks.shape[0]),
                        axis=0,
                    )
                    out_file["tracks"][-tracks.shape[0]:] = tracks
                    out_file["cells"].resize(
                        (out_file["cells"].shape[0] + cells.shape[0]),
                        axis=0,
                    )
                    out_file["cells"][-cells.shape[0]:] = cells
                displayed_writing_output = False

            if self.run_all and rem_jets < 0:
                break

            if not self.run_all and self.n_jets <= 0:
                break

        pbar.close()


if __name__ == "__main__":
    args = get_parser()

    with open(args.config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    preparation_tool = PrepareSamples(config=config, args=args)
    preparation_tool.run()
