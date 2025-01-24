## &#x2757; Execution on laptops with Apple Silicon (CPU)
Starting with certain models introduced in late 2020, Apple began the transition from Intel processors to Apple silicon in Mac computers.
These CPUs have ARM architecture and are incompatible with Intel processors. 

### Transforms
Developing transforms for either the [python or Ray runtimes](../data-processing-lib/doc/transform-runtimes.md), without KubeFlow pipelines (KFP), should have no issues on Apple silicon Macs,
or other platforms for that matter.
Therefore, to the extent the supported versions of python are used, transforms can be developed that will run on Apple silicon Macs. 
### Virtualization Considerations

Desktops such as [Docker Desktop](https://www.docker.com/products/docker-desktop/),
[Podman desktop](https://podman-desktop.io/) and [Rancher desktop](https://docs.rancherdesktop.io/) use different virtualization and emulation techniques,
([qemu](https://www.qemu.org/), [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization))
to allow the execution of containers based on images compiled for Intel silicon. However, emulation significantly
impacts performance, and there are additional restrictions, such as Virtual Machine RAM size.

On the other hand, executing a Kind Kubernetes cluster with KubeFlow pipelines (KFP) and local data storage (Minio)
requires a significant amount of memory. For this initial Data Prep Kit release, we do not recommend local (Kind)
execution on Mac computers with Apple silicon. Instead, we suggest using a real Kubernetes cluster or a Linux virtual
machine with an Intel CPU.

### Memory Considerations

To verify that running transforms through KFP does not leak memory and also get an idea on the required Podman VM memory size configuration, a few tests were devised and run, as summarized below:

#### Memory and Endurance Considerations

A test was devised with a set of 1483 files on a Mac with 32GB memory and 4CPU cores. Traceback library was used to check for memory leak. 
10 iterations were run and the memory usage was observed, which peaked around 4 GB. There were no obvious signs of a memory leak. 

Another set of tests was done with the 1483 files on a podman VM with different memory configurations. The results are shown below.
It seems that it needed around 4GB of available memory to run successfully for all 1483 files.

|CPU Cores                       | Total Memory       | Memory Used by Ray             | Transform             | Files Processed Successfully             |
|------------------------------  |-------------------|------------------|--------------------|------------------------|
|4             |8GB |4.2GB|                  NOOP  |1483      |
|4             |6GB |3GB|                NOOP    |910 |
|4             |4GB |2GB|  NOOP                  |504  | 



> **Note**: the *current* release does not support building cross-platform images, therefore, please do not build images 
on the Apple silicon. 
