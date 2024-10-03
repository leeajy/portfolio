# polygonio-stock-pipeline

This project contains an event-based pipeline for fetching data from polygon.io APIs. Each task in the pipeline is defined via a lambda function, which can be invoked by an event (ex. EventBridge) or through an orchestrator (ex. Step Functions). 

Most of the data transformations are done via pandas on python. 

## folder contents

lambda-functions: contains all the lambda functions that make up the pipeline.  
lambda-layers: contains the python packages that are used by the lambda functions.  
notebooks: contains a notebook that has an example on how the ingested data could be used.  
step-functions: contains a step function json that shows how lambda functions can be orchestrated.  
terraform: contains terraform which transforms all infrastructure to code.

