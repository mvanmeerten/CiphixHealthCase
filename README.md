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

In the image below, the extracted entities are shown. On the left, for each detected entity, a category, type and possible attribute are displayed. On the right, the original text is displayed where the entities are highlighted.

![](https://puu.sh/GicTt/2b9cc5fba4.png)

# NER Model
This demo uses AWS Comprehend Medical. If I were to train my own model, I would use the [Clinical Bert model](https://github.com/EmilyAlsentzer/clinicalBERT) and train it on the [i2b2 dataset](https://www.i2b2.org/NLP/DataSets/Main.php). I have requested access to this dataset, but unfortunately have yet to receive it.

