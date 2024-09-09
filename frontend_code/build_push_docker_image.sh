#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 <image-name> [-v <version>] [-s]"
    exit 1
}

# Initialize variables
version_specified=""
show_version_only=0

# Parse the options
while getopts ":v:s" opt; do
    case ${opt} in
        v )
            version_specified=$OPTARG
            ;;
        s )
            show_version_only=1
            ;;
        \? )
            usage
            ;;
    esac
done
shift $((OPTIND -1))

# Check if the correct number of arguments is provided
if [ $# -lt 1 ]; then
    usage
fi

# Assign the input argument to the variable 'name'
name=$1

# Define the version file
version_file="${name}_version.txt"

# Check if the version file exists, if not, create it with version 1
if [ ! -f "$version_file" ]; then
    echo "1" > "$version_file"
fi

# Show the current version and exit if -s option is provided
if [ $show_version_only -eq 1 ]; then
    current_version="$(cat $version_file)"
    echo "Current version of ${name}: v${current_version}"
    exit 0
fi

# Determine the version to use
if [ -n "$version_specified" ]; then
    version="$version_specified"
else
    # Read the current version from the version file
    version="$(cat $version_file)"
    # Increment the version if not specified by the user
    version=$((version + 1))
fi

# Build the Docker image
image="swr.ap-southeast-3.myhuaweicloud.com/model-deploy/${name}"
docker build -t ${image}:v${version} .

# Check if the build was successful
if [ $? -eq 0 ]; then
    # Push the Docker image to the repository
    docker push ${image}:v${version}
    if [ $? -eq 0 ]; then
        # Save the new version to the version file if not manually specified
        if [ -z "$version_specified" ]; then
            echo "$version" > "$version_file"
        fi
        echo "Successfully built and pushed ${image}:v${version}"
    else
        echo "Docker push failed. Version remains v${version}."
    fi
else
    echo "Docker build failed. Version remains v${version}."
fi
