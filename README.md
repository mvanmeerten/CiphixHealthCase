# CiphixHealth Case
NER of unstructured medical text using [AWS comprehend medical](https://aws.amazon.com/comprehend/medical/)

# Installation (Python 3.7)
This section describes how to run the demo. First, clone the repository and install the requirements (in a virtual environment).
```bash
$ git clone https://github.com/mvanmeerten/CiphixHealthCase.git
$ cd CiphixHealthCase/PredictAPI; pip install -r requirements.txt
```

To use AWS comprehend medical, follow steps 1 and 2 in the [getting started section](https://docs.aws.amazon.com/comprehend/latest/dg/getting-started.html) of AWS Comprehend Medical. Here you will create an AWS account and install and configure the AWS CLI.

# Running the demo
The demo can be run by executing the following command from within the PredictAPI folder
```bash
$ python app.py
```
Navigate to http://127.0.0.1:5000/ and upload the test medical document, which be found [here](https://github.com/mvanmeerten/CiphixHealthCase/blob/master/PredictAPI/documents/MedDocTest.pdf)

![alt text](https://puu.sh/GicTt/2b9cc5fba4.png)

# Dataset
https://www.nature.com/articles/sdata201635
