#!/bin/bash


red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
cian='\033[0;36m'
white='\e[0m'


archives_dir="archives"
datasets_dir="datasets"

regex="(.*).zip"

function extract () 
{
  if [ -f $1 ] ; then
      case $1 in
          *.tar.bz2)   tar xvjf $1    ;;
          *.tar.gz)    tar xvzf $1    ;;
          *.bz2)       bunzip2 $1     ;;
          *.rar)       rar x $1       ;;
          *.gz)        gunzip $1      ;;
          *.tar)       tar xvf $1     ;;
          *.tbz2)      tar xvjf $1    ;;
          *.tgz)       tar xvzf $1    ;;
          *.zip)       unzip $1       ;;
          *.Z)         uncompress $1  ;;
          *.7z)        7z x $1        ;;
          *)           echo "don't know '$1'..." ;;
      esac
  else
      echo "'$1' is not a valid file!"
  fi
}

for arch_name in $(ls "$archives_dir")
do
	echo -n "unzip $arch_name . . . "
	if [[ $arch_name =~ $regex ]]; then
		dir_to_extract="$datasets_dir/${BASH_REMATCH[1]}"
		if [[ -d $dir_to_extract ]];  then
			echo -e "${yellow}$Directory exists${white}: $dir_to_extract"
		else
			unzip "$archives_dir/$arch_name" -d "$datasets_dir" >/dev/null
			echo -e "${green}OK${white}"
		fi
	fi


done