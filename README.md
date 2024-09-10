![image](https://github.com/user-attachments/assets/acd7bab4-0d5b-42fc-b8fa-a38446cf2a5f)# Face-recognition-app

Using Huawei cloud resources to create an inference model for face recognition

## Example
![image](https://github.com/user-attachments/assets/b58142cb-266a-4916-babd-4f8713f4ae26)

## Environment
|Environment|Version|Function|
|-----------|----------|----------|
|Architecture |x86_64   |                   |
|Ubuntu       |22.04    |                   |
|python       |3.10.12  |                   |
|Docker       |27.2.0   |Deploy image       |
|Kubectl      |4.5.7    |For K8s debugging  |

## Resources
- VPC
- ELB
- CCE
- NAT
- Redis
- RDS
- Function Graph
- OBS
- EIP x 3
- SWR

## Resources Explanation
Focus on some complicated service only. Others just follow documentation to create.

**CCE**: Using for deploying application
1. Choose any type (I choose CCE Turbo Cluster)
2. Create nodepool (I choose spec: c7n.4xlarge.2 | 16 vCPUs | 32 GiB)
3. Create deployment & service in backend_code/README.md

   
**NAT**: Bind with CCE's node subnet, provide node with capability to connect public internet for downloading document
1. Create NAT
2. Buy EIP
3. Create SNAT rule and bind with EIP bought just now

   
**SWR**: SWR is a service to upload CCE needed image
1. Copy login cmd from SWR

## Workflow
1. Create Resources
2. Clone this repository
3. Update environment variables
4. Modify push docker image dest
```
# Build the Docker image
image="swr.ap-southeast-3.myhuaweicloud.com/model-deploy/${name}"
docker build -t ${image}:v${version} .
```
5. run script inside `backend_code` directory and `frontend_code` directory
```
./run.sh <image-name> [-v <version>] [-s]
```
6. Create workload in CCE (choose correct image and update environment variable)
![image](https://github.com/user-attachments/assets/eb4a110a-0c00-4006-af55-aa11940a4e28)
![image](https://github.com/user-attachments/assets/f79edc20-183f-4fde-ac44-c5beb6039fb5)


## Future work
1. Generate terraform script for one-step create resources
2. Generate yaml script for one-step deploy CCE
