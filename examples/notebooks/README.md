### Notebook Environment Setup 

To run on a the notebook examples , follow these steps to quickly set up and deploy the Data Prep Kit in your virtual Python environment.

```bash
conda create -n data-prep-kit -y python=3.11
conda activate data-prep-kit
python --version
```
If you are using a linux system and a transform that 
use `fasttext` (currently only `lang_id`), 
install gcc using the below commands:

```bash
conda install gcc_linux-64
conda install gxx_linux-64
```

Next, install the data prep toolkit library. This library installs both the python and ray versions of the transforms. For better management of dependencies, it is recommended to install the same tagged version of both the library and the transform. 

```bash
pip3 install  'data-prep-toolkit[ray]==0.2.3.dev0'
pip3 install  'data-prep-toolkit-transforms[ray]==0.2.3.dev1'
pip3 install jupyterlab   ipykernel  ipywidgets

## install custom kernel
python -m ipykernel install --user --name=data-prep-kit --display-name "dataprepkit"
```

Test, your installation. If you are able to import these data-prep-kit libraries successfully in python, your installation has succeeded. 

```bash
## start python interpreter
$   python
````

# import DPK libraries
```python
>>> from data_processing_ray.runtime.ray import RayTransformLauncher
>>> from data_processing.runtime.pure_python import PythonTransformLaunche
```

### Run your first transform locally

Let's try the same simple transform to extract content from PDF files on a local machine. 

**Local Notebook versions**

To run the notebooks, launch jupyter from the same virtual environment 
you created using the command below. 

`jupyter lab`

After opening the jupyter a notebook  (explore the sub-directories), 
change the kernel to `dataprepkit`, so all libraries will be properly loaded.

### Run your first data prep pipeline

Now that you have run a single transform, the next step is to explore how to put these transforms 
together to run a data prep pipeline for an end to end use case like fine-tuning a model or building 
a RAG application. 
This [notebook](fine%20tuning/code/sample-notebook.ipynb) gives an example of 
how to build an end to end data prep pipeline for fine-tuning for code LLMs. Similarly, this 
[notebook](fine%20tuning/language/demo_with_launcher.ipynb) is a fine-tuning 
example of an end-to-end sample data pipeline designed for processing language datasets. 
You can also explore how to build a RAG pipeline [here](examples/notebooks/rag).