# Data Movement Enactor

## Overview
The Data Movement Enactor orchestrates the data movement between the different components. It also monitors updates to
the two types of data sources: MySQL and minio. It utilizes SymmetricDS and Elasticsearch to read and log updates. Also
uses grpc to communicate with the Data Access Layer, FTP to organise a shared space for file exchange and supports
multiple sync backends, keycloak for auth to the DAL.

## Requirements
Python 3.5.2+

```
connexion == 2.2.0
python_dateutil == 2.6.0
setuptools >= 21.0.0
redis==3.3.6
elasticsearch==7.1.0
requests==2.22.0
mysqlclient==1.4.2.post1
grpc-api-client==0.1.1
grpcio==1.22.0
grpcio-tools==1.22.0
```

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

Along with the swagger server, a new thread is launched which monitors updates to the predefined datasources.

## Configuration

The template for the configuration of the DME is defined in the VDC shared config:

```
{
    "Port":"{{.dme_port}}",
    "ElasticSearchURL":"{{.elasticsearch_url}}",
    "elasticsearch_authenticate": {{.elasticsearch_authenticate}},
    "elasticsearch_user": "{{.elasticsearch_user}}",
    "elasticsearch_password": "{{.elasticsearch_password}}",
    "ftp_host": "{{.ftp_host}}",
    "ftp_user": "{{.ftp_user}}",
    "ftp_pass": "{{.ftp_pass}}",
    "db_user": "{{.symmetricds_db_user}}",
    "db_pass": "{{.symmetricds_db_pass}}",
    "db_host": "{{.symmetricds_db_host}}",
    "db_port": "{{.symmetricds_db_port}}",
    "db_name": "{{.symmetricds_db_name}}"
}
```

If these are not present, the DME reverts to sensible defaults so it can continue its execution.

Settings not fetched from the dynamic config:

```
shared_volume_system_path = 'move/'

#defines the root directory used by the sync backend to build the file structure

### Common HTTP requests config
max_retries = 3
backoff_factor = 3

#DE endpoint
de_endpoint = 'http://{}:50012'.format('localhost')

#DS4M endpoint
ds4m_endpoint = 'http://{}:30003'.format('localhost')

#How the endpoints for the Deployment engine and Decision System for movement are generated.

#Redis default settings
redis_host = 'localhost'
redis_port = 6379

#The name of the elasticsearch index to be used to log DB updates
db_update_es_index = 'dme-db-updates'

#The schema for the ES document related to DB updates
db_update_es_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
        },
    "mappings": {
        "db_update": {
            "dynamic": "strict",
            "properties": {
                "query": {
                    "type": "text"
                    },
                "target_dal": {
                    "type": "text"
                    },
                "timestamp": {
                    "type": "date"
                }
                }
            }
        }
    }
```


The Swagger definition lives here:

```
http://localhost:50055/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 50055:50055 swagger_server
```