# phd_kgs

PhD Course submission. Ran and tested on Ubuntu 22, Python 3.10

## RESULTS

The serialized results we've computed are located in the output folder. One for each alignment model.

1. baseline_align.ttl
2. owl2vec_aling.ttl

## Prerequisites

Available command-line arguments are in `src/utils/utils.py`, or `python3 main.py -h`

0. Clone this repository with `--recursive` flag; e.g. `git clone <REPO_LINK> --recursive`, this will pull the `Owl2Vec` submodule that is used for the embedding-based alignment algorithm.
1. Python 3.10, install requirements.txt
2. Execute `./get_res.sh` to fetch input data, this requires wget. Otherwise download the `confOf.owl` and `ekaw.owl` files and place them into `./res/` folder. Custom paths can be specified
3. Additionally you can download the Word2Vec model from [here](https://tinyurl.com/word2vec-model); make sure to update your

## Baseline algorithm

Baseline algorithm is based on string similarity and uses `isub` library for performing the computation. The algorithm is implemented in `src/baseline.py` file.

1. Run it with `python3 main.py -a baseline -o output/baseline_algn.ttl`
2. Output will be saved in the `output/` folder

## Embedding-based algorithm

Based on the `Owl2Vec` library, the algorithm is implemented in `src/owl_vec_alignment.py` file. Ensure to have the Word2Vec model downloaded and placed in the `./res/` folder and specify the path in the `./res/default_kg1.cfg` and `./res/default_kg1.cfg` files under `pre_train_model` variable.

1. Run it with `python3 main.py -a owl2vec -o output/owl2vec_algn.ttl`
2. Output will be saved in the `output/` folder
