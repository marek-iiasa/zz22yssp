Data provided by Julian as individual countries.xlsx renamed to: countries.xlsx

The new china.{numbers, xlsx} spread=sheets (for mac-numbers and ms-excel, respectively)
are composed of selected columns of countries.xlsx, namely: A, EL, EM, EN, EO, EP
(EL to EO: normalized value between [0,1], EP: demand in MW unit.).

Original note on the content of XLSX:
Columns of the XLS (from Zixuan) corresponding to the data used for exploring
time-slices:
A  - time-stamp (in one column), e.g., 1.01.2015  0:00:00
EL - solar
EM - wind
EN - demand
EO - hydro

Warning: countries.xlsx was removed from an old commit because it hung the
push (the file is 70MB). Therefore this file is now in .gitignore. It looks
like the file is included in the cloned repo (on GitHub). It might cause
problems with pulling the repo.
;