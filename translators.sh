#!/usr/bin/env bash

echo "Files: po/*" >  translators.txt
echo "Copyright:"  >> translators.txt
grep Last-Translator po/*.po | cut -d':' -f3 | sort -u | grep -v Unknown | grep -v "FULL NAME" | cut -d'\' -f1 >> translators.txt
