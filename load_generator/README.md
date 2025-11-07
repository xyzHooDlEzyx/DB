# Load generator container

Build and run locally:

```powershell
$env:TARGET_URL="http://flask-gunicorn-balancer-1991448715.eu-north-1.elb.amazonaws.com:8000/api/accounts"
$env:BASIC_AUTH="YWRtaW46cGFzc3dvcmQ="
docker build -t load-generator .
docker run --rm -e TARGET_URL -e BASIC_AUTH load-generator
```

Update the environment variables to match the deployed API before starting the container.
