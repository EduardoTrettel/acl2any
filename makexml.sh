#!/bin/bash

BIN_DIR="../bin"

acl_file="ACLs-rtr-corpnet-SUM-Fase1"
acl_tmp=$acl_file"-tmp"
acl_final=$acl_file"-final"
alias_file="aliases-rtr-corpnet-final"
sep_file="sep-wan-corpnet"
basic_set="basic-rtr-corpnet.xml"
marker='<wan></wan>'

# Converts ACLs from CSV to pfSense XML
$BIN_DIR/csv2pfsense $acl_file.csv > $acl_file.xml

# Merges created XML with previous basic set of rules imported from router 
$BIN_DIR/merge-xml.sh $acl_file.xml $basic_set > $acl_tmp.xml

# Creates a list of nice separators
$BIN_DIR/gen-separator.py $sep_file.csv > $sep_file.xml

# Find the start line of separators in original file
marker_line=$(echo $(grep -n $marker $acl_tmp.xml) | cut -d: -f1 -)

# Replace them with generated separators
sed -e "${marker_line}r $sep_file.xml" $acl_tmp.xml | grep -v $marker > $acl_final.xml

# echo $marker_line
#/bin/rm -f $acl_file.xml

# Converts a list of CSV aliases to pfSense XML
$BIN_DIR/gen-pfsense-aliases.py $alias_file.csv > $alias_file.xml

#
# End of makexml.sh
#