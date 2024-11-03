# Lab 2

## Usage

To run the laboratory:
- create a virtual environment with `python -m venv <ENV NAME>`
- activate the environment (on linux and mac os use the command `source <ENV NAME>/bin/activate`)
- open the notebook `tsp.ipynb` and run all the cells

## Results

All the results proposed are obtained using the `italy.csv` data

| Algorithm | Steps | Initial Solution | Cost | Calls to fitness |
| :-: | :-: | :-: | :-: | :-:  |
| H.C. + Scramble mut | 100_000 | greedy | 4431 | 100_000 |
| H.C. + Scramble mut | 100_000 | sequential | 6990 | 100_000 |
| H.C. + Inverse mut | 100_000 | greedy | 4431 | 100_000 |
| H.C. + Inverse mut | 100_000 | sequential | 7083 | 100_000 |
| H.C. + S.A. + Scramble mut | 100_000 | greedy | 4431 | 100_000 |
| H.C. + S.A. + Scramble mut | 100_000 | sequential | 7979 | 100_000 |

| Algorithm | Generations | Initial Solution | Cost | Calls to fitness | Parent sel. | Population | Offsprings |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| EA Stady State | 100_000 | sequential | 5149 | 2_000_030 | uniform | 30 | 20 |
| EA Stady State | 100_000 | greedy | 4431 | 2_000_030 | uniform | 30 | 20 |