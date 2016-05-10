#!/usr/bin/sh
mkdir title
mkdir content
./crawlTitle.py
./crawlContent.py
cat content/* > Corpus
rm -rf content/*
echo "Corpus has been download successfully!"
echo "Now run NGram.py to get N-word frequency."