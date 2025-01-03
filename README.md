# HCACE

This is the implementation of Hardware-assisted Cross-domain Access Control Encryption (HCACE) in the Python language.

## Dependencies:

* [Python v.3.10.12](https://www.python.org/downloads/release/python-31012/): This is the basic Python running environment.

* [Charm-Crypto v.0.50](https://github.com/JHUISI/charm): This is a framework for rapidly prototyping advanced cryptosystems based on the Python language.

* [Occlum v.0.30.0](https://github.com/occlum/occlum): This is a memory-safe, multi-process library OS (LibOS) for [Intel SGX](https://github.com/intel/linux-sgx), thus we can run the Python code with Intel SGX without modification.

## Code Structure

The structure of the HCACE is as follows:

* ./build_blocks: This includes some building blocks for implementing HCACE.

* HCACE.py: This is the main code for the HCACE scheme.

* testHCACE.py: This gives a Python code to run "HCACE.py" under a simple example. In our experimental evaluation, we run the sender sanitizer and receiver sanitizer of HCACE with Intel SGX, and run the other algorithms normally. 

  * Run in normal world: Run the algorithms except the sender sanitizer and receiver sanitizer of HCACE by the following command:

    ```
    # cd into ./HCACE before
    python testHCACE.py
    ```

  * Run with Intel SGX: You can refer to the details of how to run the sender sanitizer and receiver sanitizer of HCACE with Intel SGX [below](#run-with-intel-sgx).

* ./occlum-HCACE: This code is to run the sender sanitizer and receiver sanitizer of HCACE with Intel SGX.

## Run with Intel SGX

1. Follow the instructions of 01.Install Intel SGX and 02.Install Occlum in [guide](./guide.pdf) to install SGX SDK and Occlum.

2. Before you run Python code in Occlum, you may need to install conda or miniconda (Refer to the 03.1 install minaconda with the following script in [guide](./guide.pdf)). Also we give out an example and you can follow the instruction of 03.Run Python in Occlum in [guide](./guide.pdf) to run this example (the code is under the folder ./occlum-HCACE/np).

3. Change directory to ./occlum-HCACE

   ```
   cd occlum-HCACE
   ```

4. Run the script init.sh

   ```
   ./init.sh
   ```

5. Run the script build.sh

   ```
   ./build.sh
   ```

6. Run the script run.sh

   ```
   ./run.sh
   ```

