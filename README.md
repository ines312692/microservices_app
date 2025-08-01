# Microservices

## Project Structure

```
microservices_app/
│
├── README.md
├── docker-compose.yml
├── helm/
│   ├── gateway/
│   ├── users/
│   ├── orders/
│   └── microservices-app/
├── Jenkins/
│   ├── build/
│   ├── deploy/
│   └── jenkins-master/
├── k8s/
│   ├── namespace.yaml
│   └── networkpolicy.yaml
├── gateway/
│   ├── Dockerfile
│   ├── main.py
│   ├── auth.py
│   ├── conf.py
│   ├── core.py
│   ├── exceptions.py
│   ├── network.py
│   ├── post_processing.py
│   ├── requirements.txt
│   └── datastructures/
├── orders/
│   ├── Dockerfile
│   ├── main.py
│   ├── init_db.py
│   ├── models.py
│   └── requirements.txt
└── users/
    ├── Dockerfile
    ├── main.py
    ├── auth.py
    ├── datastructures.py
    ├── requirements.txt
    ├── fake/
    └── tests/
```

