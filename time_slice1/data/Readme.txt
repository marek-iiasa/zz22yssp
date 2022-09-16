Data provided by Zixuan as individual countries.xlsx renamed to: countries.xlsx

The new china.{numbers, xlsx} spread=sheets (for mac-numbers and ms-excel, respectively)
are composed of selected columns of countries.xlsx, namely: A, EL, EM, EN, EO, EP
(the content of EP needs to be clarified).

Original note on the content of XLSX:
Columns of the XLS (from Zixuan) corresponding to the data used for exploring
time-slices:
A  - time-stamp (in one column), e.g., 1.01.2015  0:00:00
EL - solar
EM - wind
EN - hydro
EO - demand

However, the py-code implies other sequence of hydro and demand, see e.g.,
lines 56-57 of zzx01.py:
    hydro = dt[:, 4 + 5 * value[region]]
    demand = dt[:, 3 + 5 * value[region]]
I guess rather the code than the above description is correct. Please explore
and comment.

Warning: countries.xlsx was removed from an old commit because it hanged the
push (the file is 70MB). Therefore this file is now in .gitignore. It looks
like the file is included in the cloned repo (on github). It might cause
problems with pulling the repo.
