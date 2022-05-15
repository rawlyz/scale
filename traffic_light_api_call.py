### Traffic Light Annotation API Call ###
# Rawlison Zhang
# 15 May 2022

## Purpose:
# Label images of traffic lights using Scale's Image Annotation annotation API endpoint

## Prerequistes:
# install with pip: $ pip install scaleapi --upgrade --quiet
# -or-
# install with conda: $ conda install -c conda-forge scaleapi

import scaleapi
from scaleapi.tasks import TaskType
from scaleapi.exceptions import ScaleException
import json

## 0. Settings
api_key = '' # input API key here
proj_name = 'traffic_lights'
batch_name = 'traffic_lights_batch_1'
callback_url = 'rawlison@scaleapi.com'
instruction_link = '<iframe src="https://docs.google.com/document/d/e/2PACX-1vR1SSLKmTo5rVKFevAFcSMBWtnQpmt6Mjs1wSuVJ1KNfuoTL3jG309rueLNj_PcgRjKxkFsHdwfNEuS/pub?embedded=true"></iframe>'
client = scaleapi.ScaleClient(api_key)
scaleapi._version_ # check version is >= 2.5.0


## 1. Create a project
# url = 'https://api.scale.ai/v1/projects'
project = client.create_project(
    project_name = proj_name,
    task_type = TaskType.ImageAnnotation,
    params = {'instruction': instruction_link}
)
print(project.name)


## 2. Create Batch
# url = 'https://api.scale.ai/v1/batches'
batch = client.create_batch(
    project = proj_name,
    callback = callback_url,
    batch_name = batch_name
)


## 3. Add tasks to the batch
# url = 'https://api.scale.com/v1/task/imageannotation'
attachments = [
    'https://i.imgur.com/iDZcXfS.png',
    'https://cdn.vox-cdn.com/thumbor/Q7_74k0zUmVCID7lnfaxKMuSaVU=/0x0:4000x2667/1200x800/filters:focal(1680x1014:2320x1654)/cdn.vox-cdn.com/uploads/chorus_image/image/65027193/shutterstock_788608396.0.jpg',
    'https://a.cdn-hotels.com/gdcs/production152/d996/c45c6d23-25e3-46c9-9ffe-7ca8c4840e54.jpg?impolicy=fcrop&w=800&h=533&q=medium'
]

labels = [
    'Single Light', 
    'Double Light', 
    'Pedestrian Light', 
    'Bike Light',
    'Other'
]

for image in attachments:
    payload = {
        'batch' : batch_name,
        'callback_url' : callback_url,
        'attachment_type' : 'image',
        'attachment' : image,
        'geometries': { # allow to draw boxes
            'box': {
                'objects_to_annotate' : labels,
                'min_height': 10,
                'min_width': 10,
                'can_rotate': True
            },
        },
        'with_labels': True,
        'annotation_attributes': {
            'Light 1' : { # annotate color of single and double lights
                'type' : 'category',
                'description' : 'What color is the light?',
                'choices' : [
                    'Green',
                    'Yellow',
                    'Red'
                ],
                'conditions' : {
                    'label_condition' : {
                        'label' : [
                            labels[0],
                            labels[1]
                        ]
                    }
                },
                'allow_multiple': False
            },
            'Arrow 1' : { # annotate direction of single and double lights 
                'type' : 'category',
                'description' : 'What direction is the light indicating?',
                'choices' : [
                    'Up',
                    'Left',
                    'Right',
                    'Left U-Turn',
                    'Right U-Turn'
                ],
                'conditions' : {
                    'label_condition' : {
                        'label' : [
                            labels[0],
                            labels[1]
                        ]
                    }
                },
                'allow_multiple': False
            },
            'Light 2' : { # annotate the color of the second light for double lights
                'type' : 'category',
                'description' : 'What color is the light?',
                'choices' : [
                    'Green',
                    'Yellow',
                    'Red'
                ],
                'conditions' : {
                    'label_condition' : {
                        'label' : labels[1]
                    }
                },
                'allow_multiple': False
            },
            'Arrow 2' : { # annotate the direction of the second light for double lights
                'type' : 'category',
                'description' : 'What direction is the light indicating?',
                'choices' : [
                    'Up',
                    'Left',
                    'Right',
                    'Left U-Turn',
                    'Right U-Turn'
                ],
                'conditions' : {
                    'label_condition' : {
                        'label' : labels[1]
                    }
                },
                'allow_multiple': False
            }
        }
    }

    try:
        task = client.create_task(TaskType.ImageAnnotation, **payload)
        print(json.dumps(task.as_dict(), indent=2))
    except ScaleException as err:
        print(err.code)
        print(err.message)