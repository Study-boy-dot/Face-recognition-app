# Frontend Code
Provide UI for user to upload image for inference.

# Environment
|Packages    |Versioin    |
|------------|------------|
|Python      |3.10.12     |
|Docker      |27.2.0      |

# Run script
**Login SWR**
```
# Copy your own from SWR
docker login -u ap-southeast-3 ...... swr.ap-southeast-3.myhuaweicloud.com
```
Modify `run.sh` to your SWR endpoint before execute it. `line 63`  
For huawei cloud service refer: [Huawei cloud endpoint](https://console-intl.huaweicloud.com/apiexplorer/#/endpoint)
```
# Build the Docker image
image="swr.ap-southeast-3.myhuaweicloud.com/model-deploy/${name}"
docker build -t ${image}:v${version} .
```
**Modify Environment variables**  
Moidfy BACKEND_SERVICE_NAME and BACKEND_SERVICE_PORT
```
location /predict {
        proxy_pass http://${BACKEND_SERVICE_NAME}:${BACKEND_SERVICE_PORT}/predict;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```
**Execute**  
```
chmod +x run.sh # Ensure run.sh have priviledge to execute
# build image and push to SWR
./run.sh <image-name> [-v <version>] [-s] # Linux command if using windows build and push manually
```

**Manual**
```
docker build -t <image_name>:<version>
docker push <image_name>:<version>
```
