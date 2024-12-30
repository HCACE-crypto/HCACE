# occlum-HCACE
In our paper, we need to run the sender sanitization and receiver sanitization of HCACE in TEE. To simplify the experiment, we just run the whole HCACE scheme in TEE (SGX is actually used) and record the time spent on sender sanitization and receiver sanitization.

The following are the steps to run HCACE in sgx:
1. Follow the instructions of 01.Install Intel SGX and 02.Install Occlum in [guide](./guide.pdf) to install sgx and occlum.
2. Before you can run Python in Occlum, you also need to install a conda or miniconda(Refer to the 03.1 install minaconda with the following script in [guide](./guide.pdf)). Also we give out an example np and you can follow the instruction of 03.Run Python in Occlum in [guide](./guide.pdf) to run this example(the code is in folder /np).
3. run the script init.sh
    ```
    ./init.sh
    ```
4. run the script build.sh
    ```
    ./build.sh
    ```
5. run the script run.sh
    ```
    ./run.sh
    ```
6. Then you can run the HCACE in occlum