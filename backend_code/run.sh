#!/bin/bash
# Name: run.sh
# Purpose:  build and push docker image to SWR
# AUTHOR: Study-boy-dot
# -----------------------------------------------------------------------------

# Function to display usage information
usage() {
	echo "Usage: $0 -n <image_name> [-v <version>] [-s]"
	exit 1
}

# Initialize variables
version_specified=""
show_version_only=false

# Parse the options
while getopts v:sn: flag
do
	case "${flag}" in
		v ) version_specified=${OPTARG};;
		s ) show_version_only=true;;
		n ) name=${OPTARG};;
		\?) usage;;
	esac
done

# Check if the correct number of arguments is provided
# if [ $# -lt 1 ]; then
#     usage
# fi

if [ -z "$name" ]; then
	name="backend"
	echo "INFO: Set image name as default: frontend"
fi

# Define the version file
version_file="${name}_version.txt"

# Initialize version
version="1.0"

# Show the current version and exit if -s option is provided
if [ "$show_version_only" = true ]; then
    current_version="$(cat $version_file)"
    echo "Current version of ${name}: v${current_version}"
    exit 0
fi

# Check the version file exist
if [ -f "${version_file}" ]; then
    # Read the current version
    current_version="$(cat ${version_file})"
    # Get the digit before dot
    major_version=${current_version%%.*}
    # Update latest build version
    version="$(( ${major_version} + 1)).0"
fi

# Determine the version to use
if [ -n "$version_specified" ]; then
    version="$version_specified"
fi

# Build the Docker image
image="swr.ap-southeast-3.myhuaweicloud.com/model-deploy/${name}"
docker build -t ${image}:v${version} .

# Check if the build was successful
if [ $? -eq 0 ]; then
    # Update version file
    echo "$version" > "$version_file"
    # Push the Docker image to the repository
    docker push ${image}:v${version}
    if [ $? -eq 0 ]; then
        echo "Successfully built and pushed ${image}:v${version}"
    else
        echo "Docker push failed. Version remains v$(cat ${version_file})."
    fi
else
    if [ -f "${version_file}" ]; then
        version=$current_version
    fi
    # Update version file
    echo "$version" > "$version_file"
    echo "Docker build failed. Version remains v$(cat ${version_file})."
fi
