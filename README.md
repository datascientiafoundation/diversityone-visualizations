# _DiversityOne_: a multi-purpose cross-country dataset about students’ everyday life


Matteo Busso, Andrea Bontempelli, Leonardo Javier Malcotti, Lakmal Meegahapola, Peter Kun, Shyam Diwakar, Chaitanya Nutakki, Marcelo Dario Rodas Britez, Hao Xu, Donglei Song, Salvador Ruiz Correa, Andrea-Rebeca Mendoza-Lara, George Gaskell, Sally Stares, Miriam Bidoglia, Amarsanaa Ganbold, Altangerel Chagnaa, Luca Cernuzzi, Alethia Hume, Ronald Chenu-Abente, Roy Alia Asiku, Ivan Kayongo, Daniel Gatica-Perez, Amalia de Götzen, Ivano Bison, and Fausto Giunchiglia. 2025. _DiversityOne: A Multi-Country Smartphone Sensor Dataset for Everyday Life Behavior Modeling._ Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 9, 1, Article 1 (March 2025)

[![](https://img.shields.io/badge/DOI-10.1145%2F3712289-blue)](https://doi.org/10.1145/3712289)

Useful links

- [data catalog](https://datascientiafoundation.github.io/LivePeople/)
- [dataset description](https://datascientia.eu/projects/diversityone/)

The code in this repository reproduces the visualizations on sensors and time diaries data of the paper.

## Requirements

- Python > 3.11

## Install

Clone the repository

```bash
git clone git@github.com:datascientiafoundation/diversityone-visualizations.git diversityone
cd diversityone
```

Create a new environment

```bash
python3 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

## Usage

Ensure that you have placed the dataset files in the `data` folder (the dataset can be requested on [Datascientia platform](https://ds.datascientia.eu/marketplace/welcome)). The script generate the plot with [seaborn](https://seaborn.pydata.org/).

```bash
python sensors.py
python timediaries.py
```

## Repository structure

```bash
.
├── data                // datasets
├── figures             // output of the scripts
├── config.py           // configure colors and university names
├── README.md           
├── requirements.txt    
├── sensors.py          // generate plots of sensors data
├── timediaries.py      // generate plots of time diaries
└── utils.py            
```
