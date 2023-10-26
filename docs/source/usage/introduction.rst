#############
Introduction
#############

BEC is a **B**\ eamline **E**\ xperiment **C**\ ontrol system that relies on multiple small services for orchestrating and steering the experiment at large research facilities. The usage of small services allows for a more modular system and facilitates the long-term maintainability. 

The system is designed to be deployed at large research facilities where the interoperability with other systems is a key requirement, see 

.. image:: ../assets/BEC_context_user_centric.png


BEC is an event-driven system with Redis as the central component for message passing. 
Multiple users can be connected to the system at the same time while the scan server uses a queue to schedule the requests received from users or other services such as feedback loops from automatic data-processing pipelines. 

.. image:: ../assets/bec_architecture.png