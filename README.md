## Usage
Build and run docker image 

```bash
docker build -t kmscrypt . --no-cache
docker run -e KMS_ID=123-456-789 -e AWS_REGION=ap-southeast-2 -e AWS_PROFILE=test -v$HOME/.aws:/root/.aws:ro -p 9000:8080 kmscrypt
```

GET request
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"value": "test123"}'
```
