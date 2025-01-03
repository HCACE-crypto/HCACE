# HCACE
This is the implementation of HCACE and We use Python to implement this scheme.

## Dependencies:
* [Charm-Crypto](https://github.com/JHUISI/charm): This is a framework for rapidly prototyping advanced cryptosystems based on the Python language.

* [Occlum](https://github.com/occlum/occlum): This is is a memory-safe, multi-process library OS (LibOS) for [Intel SGX](https://github.com/intel/linux-sgx), thus we can run the python code in SGX with no modification.

We tested in Ubuntu 22.04 in the following environment:
* Python 3.10.12

* Charm-Crypto 0.50

* Occlum 0.30.0

## Scheme
The structure of the HCACE is as follows:
* ./build_blocks: Building blocks for implementing HCACE.

* HCACE.py: Python code for the HCACE scheme.

* testHCACE.py: Python code to run "HCACE.py" under a simple example. 
    * Run in SGX: In our paper, we need to run the sender sanitization and receiver sanitization of HCACE in TEE. To simplify the experiment, we just run the whole HCACE scheme in TEE (SGX is actually used) and record the time spent on sender sanitization and receiver sanitization. You can see how to run the code in SGX in [Run in SGX](#run-in-sgx).

    * Run in normal world: For the same reason, in the experiment we record the running time of all algorithms except sender sanitization and receiver sanitization when we run this code in normal world.

* ./ooclum-HACE: The code to run HCACE in SGX.

## Run in SGX
The following are the steps to run HCACE in SGX (note that your machine need to support Intel SGX):
1. Follow the instructions of 01.Install Intel SGX and 02.Install Occlum in [guide](./guide.pdf) to install SGX and Occlum.

2. Before you can run Python in Occlum, you also need to install a conda or miniconda(Refer to the 03.1 install minaconda with the following script in [guide](./guide.pdf)). Also we give out an example np and you can follow the instruction of 03.Run Python in Occlum in [guide](./guide.pdf) to run this example (the code is under the folder ./occlum-HCACE/np).

3. cd into ./occlum-HCACE
    ```
    cd occlum-HCACE
    ```
4. run the script init.sh
    ```
    ./init.sh
    ```
5. run the script build.sh
    ```
    ./build.sh
    ```
6. run the script run.sh and you can run the HCACE in SGX
    ```
    ./run.sh
    ```


