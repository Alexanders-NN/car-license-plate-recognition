#!/bin/bash


red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
cian='\033[0;36m'
white='\e[0m'

arch_name=$1

[[ "$arch_name" = "" ]] && arch_name=datasets.zip

unzip "$arch_name" 


