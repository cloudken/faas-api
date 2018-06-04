#!/bin/bash -x

# input
if [ $# -ne 4 ]; then
    echo "usage: ./build_pkg.sh pkg_name src_path build_path build_dir"
    exit 1
fi
pkg_name=$1
src_path=$2
build_path=$3
build_dir=$4

ver=`date +%Y%m%d`

# src build
cd $src_path
mkdir -p dist
cd dist
rm -f cloudframe-*.tar.gz
cd ..
python setup.py sdist

# docker build
src_file="$src_path/dist/cloudframe-*.tar.gz"
docker_img="$pkg_name:$ver"
img_tar="$pkg_name.tar"
rm -f $img_tar
cd $build_path
cd $build_dir
rm -f cloudframe-*.tar.gz
cp $src_file .
cd ..
docker rmi $docker_img
docker build -t $docker_img $build_dir
#mkdir -p $pkg_name
#docker save $docker_img > $pkg_name/$img_tar
