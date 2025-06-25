# DocuRAG Deployment Guide

## Overview

This guide covers deploying DocuRAG in various environments, from local development to production Kubernetes clusters. The system is designed to be containerized and scalable.

## Prerequisites

### System Requirements
- **CPU**: 2+ cores recommended
- **Memory**: 4GB+ RAM (8GB+ for production)
- **Storage**: 10GB+ for documents and indices
- **Network**: Internet access for OpenAI API

### Software Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.20+ (for production)
- Git

### API Keys
- OpenAI API key with sufficient credits
- Optional: Monitoring service keys

## Local Development

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd DocuRAG

# Set environment variables
export OPENAI_API_KEY="your-api-key"
export VECTOR_STORE="faiss"

# Create data directory and add PDFs
mkdir -p data
# Copy your PDF files to ./data/

# Build and run with Docker Compose
docker-compose up --build
```

### Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run ingestion
python src/ingest/build_index.py --pdf_dir ./data --out ./index

# Start API server
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Deployment

### Environment Configuration
Create a `.env` file:
```env
OPENAI_API_KEY=your-api-key-here
VECTOR_STORE=faiss
INDEX_PATH=./index
CUDA_VERSION=
```

### Single Container Deployment
```bash
# Build inference image
docker build -f docker/Dockerfile.inference -t docurag-api .

# Run container
docker run -d \
  --name docurag-api \
  -p 8000:8000 \
  -v $(pwd)/index:/app/index \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e VECTOR_STORE=faiss \
  docurag-api
```

### Multi-Container with Docker Compose
```bash
# Run ingestion and API
docker-compose up -d

# Check logs
docker-compose logs -f

# Scale API instances
docker-compose up -d --scale inference=3
```

### GPU Support
```bash
# Build with CUDA support
docker build -f docker/Dockerfile.inference \
  --build-arg CUDA_VERSION=11.8 \
  -t docurag-api-gpu .

# Run with GPU
docker run --gpus all \
  -p 8000:8000 \
  -v $(pwd)/index:/app/index \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  docurag-api-gpu
```

## Production Deployment

### Docker Swarm
```yaml
# docker-stack.yml
version: '3.8'

services:
  docurag-api:
    image: docurag-api:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
      - VECTOR_STORE=faiss
    volumes:
      - docurag_index:/app/index
    secrets:
      - openai_api_key
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure

secrets:
  openai_api_key:
    external: true

volumes:
  docurag_index:
    driver: local
```

Deploy:
```bash
# Create secret
echo "your-api-key" | docker secret create openai_api_key -

# Deploy stack
docker stack deploy -c docker-stack.yml docurag
```

### Kubernetes Deployment

#### Namespace and ConfigMap
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: docurag

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: docurag-config
  namespace: docurag
data:
  VECTOR_STORE: "faiss"
  INDEX_PATH: "/app/index"
```

#### Secret
```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: docurag-secrets
  namespace: docurag
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-api-key>
```

#### Persistent Volume
```yaml
# k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: docurag-index-pvc
  namespace: docurag
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: nfs-client
```

#### Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docurag-api
  namespace: docurag
spec:
  replicas: 3
  selector:
    matchLabels:
      app: docurag-api
  template:
    metadata:
      labels:
        app: docurag-api
    spec:
      containers:
      - name: docurag-api
        image: docurag-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: docurag-secrets
              key: OPENAI_API_KEY
        envFrom:
        - configMapRef:
            name: docurag-config
        volumeMounts:
        - name: index-volume
          mountPath: /app/index
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: index-volume
        persistentVolumeClaim:
          claimName: docurag-index-pvc
```

#### Service and Ingress
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: docurag-api-service
  namespace: docurag
spec:
  selector:
    app: docurag-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: docurag-api-ingress
  namespace: docurag
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: docurag.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: docurag-api-service
            port:
              number: 80
```

#### Ingestion CronJob
```yaml
# k8s/cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: docurag-ingestion
  namespace: docurag
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: docurag-ingest
            image: docurag-ingest:latest
            env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: docurag-secrets
                  key: OPENAI_API_KEY
            volumeMounts:
            - name: data-volume
              mountPath: /app/data
            - name: index-volume
              mountPath: /app/index
            command:
            - python
            - src/ingest/build_index.py
            - --pdf_dir
            - ./data
            - --out
            - ./index
            - --store
            - faiss
          volumes:
          - name: data-volume
            persistentVolumeClaim:
              claimName: docurag-data-pvc
          - name: index-volume
            persistentVolumeClaim:
              claimName: docurag-index-pvc
          restartPolicy: OnFailure
```

Deploy to Kubernetes:
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n docurag
kubectl get services -n docurag
kubectl get ingress -n docurag
```

## Helm Chart (Stretch Goal)

### Chart Structure
```
deploy/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── pvc.yaml
│   └── cronjob.yaml
└── charts/
```

### Installation
```bash
# Install with Helm
helm install docurag ./deploy/helm-chart \
  --set secrets.openaiApiKey="your-api-key" \
  --set ingress.host="docurag.example.com"

# Upgrade
helm upgrade docurag ./deploy/helm-chart

# Uninstall
helm uninstall docurag
```

## Load Balancing

### Nginx Configuration
```nginx
upstream docurag_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name docurag.example.com;

    location / {
        proxy_pass http://docurag_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For streaming endpoints
        proxy_buffering off;
        proxy_cache off;
    }
}
```

### HAProxy Configuration
```
global
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend docurag_frontend
    bind *:80
    default_backend docurag_backend

backend docurag_backend
    balance roundrobin
    option httpchk GET /healthz
    server api1 127.0.0.1:8000 check
    server api2 127.0.0.1:8001 check
    server api3 127.0.0.1:8002 check
```

## Monitoring and Logging

### Health Checks
```bash
# Basic health check
curl http://localhost:8000/healthz

# Detailed monitoring
curl -s http://localhost:8000/healthz | jq .
```

### Prometheus Metrics (Future Enhancement)
```yaml
# Add to deployment
- name: ENABLE_METRICS
  value: "true"
- name: METRICS_PORT
  value: "9090"
```

### Centralized Logging
```yaml
# Fluentd sidecar for log collection
- name: fluentd
  image: fluent/fluentd:v1.14
  volumeMounts:
  - name: log-volume
    mountPath: /var/log
```

## Security Considerations

### API Security
1. **API Keys**: Use Kubernetes secrets or external secret management
2. **Network Policies**: Restrict pod-to-pod communication
3. **TLS**: Enable HTTPS with proper certificates
4. **Rate Limiting**: Implement request rate limiting

### Container Security
1. **Non-root user**: Run containers as non-root
2. **Read-only filesystem**: Mount root filesystem as read-only
3. **Security contexts**: Apply appropriate security contexts
4. **Image scanning**: Scan images for vulnerabilities

### Data Security
1. **Encryption at rest**: Encrypt persistent volumes
2. **Encryption in transit**: Use TLS for all communications
3. **Access controls**: Implement RBAC for Kubernetes
4. **Audit logging**: Enable audit logs for compliance

## Backup and Recovery

### Index Backup
```bash
# Backup vector index
kubectl exec -n docurag deployment/docurag-api -- \
  tar czf /tmp/index-backup.tar.gz /app/index

# Copy backup
kubectl cp docurag/pod-name:/tmp/index-backup.tar.gz ./index-backup.tar.gz
```

### Automated Backups
```yaml
# Backup CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: docurag-backup
spec:
  schedule: "0 1 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: alpine:latest
            command:
            - sh
            - -c
            - |
              tar czf /backup/index-$(date +%Y%m%d).tar.gz /app/index
              find /backup -name "index-*.tar.gz" -mtime +7 -delete
            volumeMounts:
            - name: index-volume
              mountPath: /app/index
            - name: backup-volume
              mountPath: /backup
```

## Troubleshooting

### Common Issues

**Pod not starting**
```bash
kubectl describe pod -n docurag <pod-name>
kubectl logs -n docurag <pod-name>
```

**API not responding**
```bash
kubectl port-forward -n docurag deployment/docurag-api 8000:8000
curl http://localhost:8000/healthz
```

**Index not loading**
```bash
kubectl exec -n docurag deployment/docurag-api -- ls -la /app/index
```

### Performance Tuning

**Memory optimization**
```yaml
resources:
  requests:
    memory: "2Gi"
  limits:
    memory: "4Gi"
```

**CPU optimization**
```yaml
resources:
  requests:
    cpu: "500m"
  limits:
    cpu: "2000m"
```

**Horizontal Pod Autoscaler**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: docurag-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: docurag-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```