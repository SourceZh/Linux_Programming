#!/usr/bin/sh
if [[ $# < 1 ]]; then
	echo "Usage - $0 dir";
	echo "        Where dir is a directory";
	exit 1;
fi
if [[ -d $1 ]]; then
	# list all include hidden files
	# list all files in the directory
	lsF=`ls -aF $1`;
	# number of directory
	dirnum=$(echo "$lsF"|grep -c /$);
	# except . and .. directory
	let dirnum=$dirnum-2;
	echo "Directories num: $dirnum";
	# number of exec files
	execnum=$(echo "$lsF"|grep -c \*$);
	echo "Exec file num: $execnum";
	# number of no extension files
	noextnum=$(echo "$lsF"|grep -v /$|grep -vc [.]);
	echo "No extension file num: $noextnum";
	# lsFX=`ls -aFX $1`;
	# extfile=$(echo "$lsFX"|grep -v /$|grep [.]|sed 's/[\*\@>\|]$//g');
	# use awk to replace
	# use -X to sort by extension
	lslX=`ls -alX $1`;
	extfile=$(echo "$lslX"|grep -v "^[d|t]"|awk '{print $9}'|grep [.]);
	extension="";
	num=0;
	for file in $extfile; do
		fileext=${file##*.};
		if [[ $extension != $fileext ]]; then
			if [[ $num != 0 ]]; then
				echo ".$extension extension file num: $num";
			fi
			extension=$fileext;
			num=1;
		else
			let num=$num+1;
		fi
	done
	if [[ $num != 0 ]]; then
		echo ".$extension extension file num: $num";
	fi
else
	echo "Usage - $0 dir";
	echo "        Where dir is a directory";
	exit 1;	
fi