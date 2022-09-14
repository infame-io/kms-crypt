## Usage
### Unittests
Run unittests
```bash
docker build -t kmscrypt -f Dockerfile.tests . --no-cache
docker run --name kmscrypt kmscrypt 
```

### Run lambda locally
Build and run docker image 

```bash
docker build -t kmscrypt . --no-cache
docker run -e AWS_PROFILE=ss-sandbox-devops -e KMSKEYID=123-456-789 -v$HOME/.aws:/root/.aws:ro -p 9000:8080 kmscrypt
```

GET request
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"value": "test123"}'
```
