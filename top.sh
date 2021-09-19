#!/bin/bash
top -b -n1 > top0.txt &
top -u jvb  -b -n1 > top1.txt &
top -u jicofo -b -n1 > top2.txt &
top -u messagebu -b -n1 > top3.txt &
top -u prosody -b -n1 > top4.txt

