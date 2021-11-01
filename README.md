# NTU-SCSE21-0117
Nanyang Technological University (NTU) Final Year Project (FYP) 2021

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

external libraries required can be found in requirements.txt
* python
* sqlite3

## Installation

If CSV files are not downloaded from the repository
* download [Azure Trace for Packing 2020](https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md) and place it into the working folder
* run savefile.py

<!-- USAGE EXAMPLES -->
## Usage

```usage
   run.py [VM entry.CSV] [VM Type List.CSV] [Algorithm]
   
   example: python run.py "csv/vm entry list(100).csv" "vm type list.csv" "bestfit"
```



### Algorithms
* firstfit
* nextfit
* bestfit
* worstfit


