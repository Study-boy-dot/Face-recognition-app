# Backend Code

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
```
chmod +x run.sh # Ensure run.sh have priviledge to execute
# build image and push to SWR
./run.sh <image-name> [-v <version>] [-s] # Linux command if using windows build and push manually
```
**Modify Environment variables**  
Lookup to `.env.template` edit your `.env` file

**Manual**
```
docker build -t <image_name>:<version>
docker push <image_name>:<version>
```
