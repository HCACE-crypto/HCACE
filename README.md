# HCACE
This is the implementation of HCACE and We use Python to implement this scheme.

## Dependencies:
* [Charm-Crypto](https://github.com/JHUISI/charm): this is a framework for rapidly prototyping advanced cryptosystems based on the Python language.

We tested in the following environment:
* Python 3.10.12
* Charm-Crypto 0.50

## Scheme
The structure of the HCACE is as follows:
* /build_blocks: Building blocks for implementing HACE. It mainly includes the implementation of an AKPABE (Anonymous Key-Policy ABE) scheme and a [CDABACE](https://github.com/CDABACE/CDABACE) scheme, etc.
* HCACE.py: Python code for the HCACE scheme.
* testHCACE.py: Python code to run "HCACE.py" under a simple example.
* /ooclum-HACE: This directory shows how to run the HCACE sheme in the SGX. Please see the README in this directory to know more.

