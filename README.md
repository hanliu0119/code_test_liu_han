# Kognic Coding Assignment

This coding assignment is designed to mimic some of the coding tasks that you might encounter while working together with Kognic. In order to complete this assignment you need to be proficient in Python, know how python packages are generated and be familiar with basic REST APIs. You are free to use any libraries you want.

> Hint: The `pydantic` library can be very powerful when dealing with json structures

## Assignment - Annotation Format Conversion Service

### Background
Annotations are produced during the process of labeling data. An annotation is a text file (usually json) that describes the content of the data. If you for instance were to produce a bounding-box annotation for an image containing a vehicle, the resulting annotation in the *kognic_format* could look something like this:
```
{
    "objects": [
        {
            "type": "vehicle",
            "id": "d9c42ffd-ed63-4f6a-8ac7-227de8a9945f"
            "position": {
                "x_min": 50,
                "x_max": 150,
                "y_min": 50,
                "y_max": 150
            }
        }
    ]
}
```

, where the `id` field is an identifier of the vehicle object, and `x_min`, `x_max`, `y_min`, `y_max` defines the boundaries of the box in pixel coordinates.

![2022-03-09-07-27-07-27-52](https://user-images.githubusercontent.com/65158011/157385146-1a6f6c3e-8c44-446b-8ad8-58384c692192.png)

> Hint: This is not how the bounding box coordinates are defined in the openlabel format


### Assignment
One challenge when dealing with annotations is that there many different formats available. Due to this there is a need for being able to convert to and from different formats, all while making sure that the contents of the annotations are not altered.

For this assignment you are tasked with creating a REST API that performs conversion of annotations from a simplified version of the *Kognic* format to a simplified version of the *OpenLABEL* format. In order to implement this you have two files available, `kognic_format.json` containing the annotation in the Kognic format, as well as `open_label_format.json` containing the same annotation but in OpenLABEL format. These files both describe an annotation consisting of 3 different classes - `Vehicle`, `Animal` and `LicensePlate`.

In the annotation files there are 3 instances of the `Vehicle` class, 1 instance of the `Animal` class and 1 instance of the `LicensePlate` class present, but the API should be able convert annotations containing any number instances of these 3 different classes.

The API should be able to receive a GET http-request containing a json on the kognic json format and respond with the OpenLABEL converted annotation.

In order to make communication with the API easier you are also expected to provide a python client in the form of a pip-installable python package. You are free to design the client as you wish as long as it can after installation be used in a way similar to this example:

```python
from annotation_converter import convert
import json

path_to_kognic_annotation = 'kognic_format.json'
with open(path_to_kognic_annotation, 'r') as content:
    kognic_annotation = json.load(content)

open_label_annotation = convert(kognic_annotation)
```
### Regarding ASAM OpenLabel
Included is a HTML file with documentation regarding the ASAM OpenLabel format. The document includes the full specification of the format, but for this code test you will only need a small part of it

> Hint: 7.10.1. Bounding boxes


### How to deliver the assignment
The finished assignment should be pushed to this github repository on a branch named `code_test_<yourname>`. In addition to all the neccessary code it should contain a README that describes:
1. How to start the REST API locally
2. How to install and use your python-library
