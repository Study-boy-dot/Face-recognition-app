#!/bin/bash
# Name: run.sh
# Purpose:  build and push docker image to SWR
# AUTHOR: Study-boy-dot
# -----------------------------------------------------------------------------

# Function to display usage information
usage() {
	echo "Usage: $0 -n <image_name> [-v <version>] [-s] [-f]"
	exit 1
}

# Initialize variables
version_specified=""
show_version_only=false
force_flag=false

# Parse the options
while getopts v:sn:f flag
do
	case "${flag}" in
		v ) version_specified=${OPTARG};;
		s ) show_version_only=true;;
		n ) name=${OPTARG};;
        f ) force_flag=true;;
		\?) usage;;
	esac
done

# Check if the correct number of arguments is provided
# if [ $# -lt 1 ]; then
#     usage
# fi

if [ -z "$name" ]; then
	name="backend"
	echo "INFO: Set image name as default: backend"
fi

# Define the version file
version_file="${name}_version.txt"
push_status_file="${name}_push_status.txt"

# Initialize version
version="1.0"

# Show the current version and exit if -s option is provided
if [ "$show_version_only" = true ]; then
    current_version="$(cat $version_file)"
    echo "INFO [$0]: Current version of ${name}: v${current_version}"
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

# Initialize image name
build_image="swr.ap-southeast-3.myhuaweicloud.com/model-deploy/${name}"
push_image=""

skip_flag=false
# Check if push previously failed and the image exists locally
if [ -f "$push_status_file" ] && [ "$(cat $push_status_file)" = "failed" ]; then
    # Check existing of image
    if [ -n "$version_specified" ]; then
        docker image inspect "$build_image:v${version}" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            if [ "$force_flag" = false ]; then
                echo "INFO [$0]: Previous push failed. Skipping build and retrying push for ${build_image}:v${version}."
                skip_flag=true
            else
                echo "INFO [$0]: Force flag is set, rebuilding the image."
                docker build -t "$build_image:v${version}" .
                echo "INFO [$0]: Successfully build ${build_image}:v${version}"
            fi
            push_image="${build_image}:v${version}"
            echo ${push_image}
        fi
    else
        docker image inspect "$build_image:v${current_version}" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            if [ "$force_flag" = false ]; then
                echo "INFO [$0]: Previous push failed. Skipping build and retrying push for ${build_image}:v${current_version}."
                skip_flag=true
                push_image="${build_image}:v${current_version}"
            else
                echo "INFO [$0]: Force flag is set, rebuilding the image."
                docker build -t "$build_image:v${version}" .
                echo "INFO [$0]: Successfully build ${build_image}:v${version}"
                push_image="${build_image}:v${version}"
            fi
        fi
    fi
else
    echo "INFO [$0]: Building image ${build_image}:v${version}."
    docker build -t "$build_image:v${version}" .
    echo "INFO [$0]: Successfully build ${build_image}:v${version}"
    push_image="${build_image}:v${version}"
fi

# Check if the build was successful
if [ $? -eq 0 ]; then
    # Update version file after a successful build
    if [ "$skip_flag" = false ]; then
        echo "$version" > "$version_file"
        echo "INFO [$0]: Update ${version_file} file."
    fi
    # Push the Docker image to the repository
    docker push ${push_image}

    if [ $? -eq 0 ]; then
        echo "INFO [$0]: Successfully built and pushed ${push_image}"
        echo "success" > "$push_status_file"
    else
        echo "ERROR [$0]: Docker push failed. Version remains v$(cat ${version_file})."
        echo "INFO [$0]: Run again $0 will ONLY push the existed latest image."
        echo "INFO [$0]: If you want to rebuld a new version run $0 -n ${name} -f"
        echo "failed" > "$push_status_file"
    fi
else
    if [ -f "${version_file}" ]; then
        version=$current_version
    fi
    # Revert version file to the previous version if the build fails
    echo "$version" > "$version_file"
    echo "ERROR [$0]: Docker build failed. Version remains v$(cat ${version_file})."
fi
