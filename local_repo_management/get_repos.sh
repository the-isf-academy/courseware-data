#!/bin/bash
FRONT_URL="https://github.com/the-isf-academy/"
LAB_PREFIX="$2"
BACK_URL=".git"
grep . $1 | while read LINE ; do 
    #Strip new line from LINE
    #echo "$FRONT_URL$LAB_PREFIX-${LINE//[$'\t\r\n ']}$BACK_URL"
    git clone "$FRONT_URL$LAB_PREFIX-${LINE//[$'\t\r\n ']}$BACK_URL"
done
