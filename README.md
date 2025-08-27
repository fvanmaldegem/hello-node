# hello-node
A simple Hello Node application

## Environment variables
Flask specific environment variables:
- `FLASK_RUN_HOST`: The IP address to bind to
- `FLASK_RUN_PORT`
- `FLASK_DEBUG`

More info here: https://flask.palletsprojects.com/en/stable/quickstart/

Application specific environment variables:
- `HOSTNAME`: The specific hostname to report. If omitted, it will be read from `/etc/hostname`
- `DENYLIST`: a comma seperated list of IPv4/6 addresses that need to be denied.

## Examples
Run image directly
```bash
docker run -e "FLASK_RUN_HOST=::" -e "DENYLIST=192.168.0.1" --name hello-node --detach --rm -p 8080:8080 -v /etc/hostname:/etc/hostname fvanmaldegem/hello-node:latest
```

Run with `docker compose`
```yaml
# docker-compose.yaml
services:
  app:
    image: fvanmaldegem/hello-node:latest
    ports:
      - '8080:8080'
    volumes:
      - type: bind
        source: /etc/hostname
        target: /etc/hostname
        read_only: true
    environment:
      - FLASK_RUN_HOST=::
      - DENYLIST=192.168.0.1
```
```bash
docker compose up -d
```

Run with Kubernetes
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-node-deployment
  labels:
    app: hello-node-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-node
  template:
    metadata:
      labels:
        app: hello-node
    spec:
      containers:
      - name: hello-node
        image: fvanmaldegem/hello-node:latest
        ports:
        - containerPort: 8080
        env:
        - name: FLASK_RUN_HOST
          value: "::"
        - name: HOSTNAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: DENYLIST
          value: "192.168.0.1"
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-node-service
spec:
  type: LoadBalancer
  selector:
    app: hello-node
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```
```bash
kubectl apply -f deployment.yaml -f service.yaml
```