#!/bin/bash

echo '<filter>'

#if [ ! -z "$@" ]; then
   for f in $@
   do
       grep -v filter\> $f
       #echo "$f"
   done 
#fi

echo '</filter>'
