# Diversity 1: a multi-purpose cross-country dataset about students’ everyday life

Source code of the visualization in the paper.

```bash
source venv/bin/activate
jupyter
```

To download the data from Streambase

```bash
rsync -rv  --include='Synchronic-Interactions/*' \
            --include='*/' \
            --exclude='*'  \
            streambase3:/datascientia_repository/CREP/Collection/2020.09.28-2021.08.15_Diversity1/v3/Location/ data/
```