# BARCS
_**Ballistic Asynchronous Reversible Computing with Superconductors**_ project.
The BARCS repository contains the RevComp team's`barc`tool for BARCS functional element enumeration and classification.

## Background

Since late 2016, a research effort has been pursued at Sandia National Laboratories to develop and explore a novel _asynchronous_ model of ballistic reversible computing (ARC or ABRC); this research has been described in a number of papers and talks, some of which are listed below. We have mainly been exploring possible implementations of ABRC in superconducting circuits; this sub-effort is called **B**allistic **A**synchronous **R**eversible **C**omputing with **S**uperconductors (BARCS).

## Description

This repository contains the source code for (and results from) a Python program called`barc`whose purpose is to enumerate and categorize the possible BARCS functional elements having two internal states and up to three I/O ports. It takes a few hours to run.  Complete output from the program is in the file [`results/RESULTS.txt`](results/RESULTS.txt) and the results are summarized in [`results/SUMMARY.txt`](results/SUMMARY.txt). Results are discussed in reference [4] below.

## References

1. Michael Frank, (2017). "Asynchronous Ballistic Reversible Computing" 2017 IEEE International Conference on Rebooting Computing, ICRC 2017 – Proceedings. [doi:10.1109/ICRC.2017.8123659](https://doi.org/10.1109/ICRC.2017.8123659).
2. Michael Frank, Rupert Lewis, Nancy Missert, Matthaeus Wolak, Michael Henry, (2019). "Asynchronous Ballistic Reversible Fluxon Logic" _IEEE Transactions on Applied Superconductivity_. [doi:10.1109/tasc.2019.2904962](https://doi.org/10.1109/tasc.2019.2904962).
3. Michael Frank, Rupert Lewis, Nancy Missert, M. Henry, Matthaeus Wolak, Erik Debenedictis, (2019). "Semi-Automated Design of Functional Elements for a New Approach to Digital Superconducting Electronics: Methodology and Preliminary Results" ISEC 2019 – International Superconductive Electronics Conference. [doi:10.1109/ISEC46533.2019.8990900](https://doi.org/10.1109/ISEC46533.2019.8990900).
4. M. P. Frank and R. M. Lewis, "Ballistic Asynchronous Reversible Computing in Superconducting Circuits," 2022 IEEE International Conference on Rebooting Computing (ICRC), San Francisco, CA, USA, 2022, pp. 30-35. [doi:10.1109/ICRC57508.2022.00018](https://doi.org/10.1109/ICRC57508.2022.00018).
