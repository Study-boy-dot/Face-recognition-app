# Backend Code

# Environment
|Packages    |Versioin    |
|------------|------------|
|Python      |3.10.12     |
|Docker      |27.2.0      |

# Create Workload
![Screenshot from 2024-09-10 15-14-37](https://github.com/user-attachments/assets/369af1e9-50e7-4d53-a584-a8e363f3240e)
**Configuration**  
Cores can set to 1, Memory set to 2048mib  
Edit environment variables
![image](https://github.com/user-attachments/assets/39766198-e918-43b8-9679-52f56c95c760)
**Add Share storage for node has multiple pods**  
![image](https://github.com/user-attachments/assets/2eed19aa-f5b7-46b3-a827-0270bd78a266)

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
