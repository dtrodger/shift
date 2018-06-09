# Ponos Microservice Specification

### GET [ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift](ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift)

Headers
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Authorization - Welcome2018!

Return
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;200 - all Shift resources
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4** - Client error with helpful message
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;500 - Server error

Behavior
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Queries Mongo running as docker container on EC2 for all Shift documents. Serializes returned documents through marshmallow schema. Returns JSON API formatted resource objects.

### GET [ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift/1](ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift/<shift_id>)

Headers
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Authorization - Welcome2018!

Return
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;200 - Shift resource with resource shift_id = url <shift_id>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4** - Client error with helpful message
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;500 - Server error
Behavior
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Queries Mongo running as docker container on EC2 for Shift document matching url <shift_id>. Serializes returned document through marshmallow schemas. Returns JSON API formatted resource object.


### POST [ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift](ec2-34-230-18-142.compute-1.amazonaws.com/ponos/shift)

Headers
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Content-Type - application/vnd.api+json
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Accept - application/vnd.api+json
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Authorization - Welcome2018!

Body
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;post_shift.json provided with specification

Returns
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;200 - Success message
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4** - Client error with helpful message
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;500 - Server error

Behavior
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Validates request payload format against marshmallow json api schema. Stores request payload in Redis running as docker container on EC2. Publishes to SNS topic with Redis record key and meta data about how to process job. SQS queue subscribed to SNS topic adds job to queue. Worker daemon running on EC2 pulls jobs from the queue and uses Redis record key and job meta data to add the POST’d payload to Mongo running as docker container on EC2.