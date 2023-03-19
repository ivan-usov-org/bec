Start docker containers for MongoDB, SciBec API server, and Redis
==================================================================

.. NOTE::
    - **This step requires sudo privileges or docker running with elevated permissions.**
    - The minimum docker version is 18.09.
    - As SciBec tries to establish a connection to MongoDB and Redis, make sure that they are running before you start SciBec.

Linux:
------

Run MongoDB on docker:

.. code-block:: bash

    sudo docker run -p 27017:27017 --name mongo-bec -d mongo

Run redis on docker: 

.. code-block:: bash

    sudo docker run --network=host --name redis-bec -d redis
 
Run SciBec on docker (clone code, build, and run SciBec API server):

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/bec.git
    cd bec/scibec
    sudo docker build -t scibec -f ./Dockerfile .
    sudo docker run --network=host --name scibec -d scibec


Now you could open a browser and check out `<http://localhost:3030>`_ page.



macOS:
-------
.. warning::
    **MacOS does not support network=host**. Instead you have to expose all ports explicitly. This also leads to a significant increase in latency for redis.


Run MongoDB on docker:

.. code-block:: bash

    sudo docker run -p 27017:27017 --name mongo-bec -d mongo

Run redis on docker: 

.. code-block:: bash

    sudo docker run -p 6379:6379 --name redis-bec -d redis
 
Run SciBec on docker (clone code, build, and run SciBec API server):

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/bec.git
    cd bec/scibec
    sudo docker build -t scibec -f ./Dockerfile .
    sudo docker run -p 3030:3030 --name scibec -d scibec


Now you could open a browser and check out `<http://localhost:3030>`_ page.



Inspect services
-----------------

To check the running docker containers:

.. code-block:: bash

    sudo docker ps
  
To connect to a running docker container:

.. code-block:: bash

    sudo docker exec -it <container-name> /bin/bash


MongoDB
--------
Inspect MongoDB 

If the MongoDB instance is running on docker, first connect to the container using

.. code-block:: bash

    sudo docker exec -it <container-name> /bin/bash

Running `mongo` (mongoDB version < 6) or `mongosh` (mongoDB version >= 6) will connect you to the mongo shell. Once connected, the database can be selected with `use scibec` . 
You can now run queries on e.g. devices using `db.Device.find()`.
To delete everything, use `db.Device.drop()`

If you want to reset the entire database, you will have to delete the data stored in Beamline, Session and Device.