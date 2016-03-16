#!/usr/bin/sh
baseUrl="https://en.wikipedia.org";
enter="/wiki/Main_Page";
declare -A html;
html[$enter]=1;
count=0;

mkdir .html;
curl -s -o ".html/$count.html" "$baseUrl$enter" &
# wait html download finished
wait

handlefile=0;
while [[ $count -lt 100 ]]; do
	# search urls in html
	# only use /wiki/
	temp=`awk -F '[<>]' '{for(i=1;i<=NF;i++){if($i~/href=\"\/wiki\//){print $i}}}' ".html/$handlefile.html"`;
	# - image
	tags=$(echo "$temp"|grep ^a|grep -v \#|grep -v "class=\"image\""|grep -iv ".jpg");
	# - tags
	urls=$(echo "$tags"|awk -F \" '{for(i=1;i<=NF;i++){if($i~/\/wiki\//){print $i}}}'|sort|uniq);
	for url in $urls; do
		# I can not download /wiki/Special:Random
		if [[ $url != "/wiki/Special:Random" ]]; then
			if [[ html[$url] -ne 1 ]]; then
				html[$url]=1;
				let count=$count+1;
				# save html
				echo "start download $count : $url";
				curl -s -o ".html/$count.html" "$baseUrl$url" > ".html/$count.log" &		
			fi
			# only handle 100 htmls
			if [[ $count -ge 100 ]]; then
				break;
			fi			
		fi
	done
	# search next html
	let handlefile=$handlefile+1;
done
# wait all html download finished
wait
echo "download finish";

for i in {0..99}; do
	# get words from html
	text=$(sed "s/<[^>]*>//g" ".html/$i.html"|sed "s/\t//g"|awk '{if($0!~/\.[a-zA-Z]/){print $0}}'|sed "s/[^a-zA-Z]/ /g");
	words=$(echo "$text"|awk '{for(i=1;i<=NF;i++){print $i}}' > ".html/$i.words") &
done
# wait all .words generate
wait

cat .html/*.words|sort|uniq -c|sort -nr|head -n 1000|awk '{print NR,$2,$1}' > top1000words;
echo "the result is stored at file ./top1000words";
rm -rf .html

