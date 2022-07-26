#!/bin/bash

BIN_DIR="../bin"

acl_file="filter-fase1"
acl_tmp="filter-sist"
acl_final="filter-fase2"
alias_file="aliases-fase1"
alias_tmp="aliases-sist"
alias_final="aliases-fase2"

# Converts ACLs from CSV to pfSense XML
$BIN_DIR/csv2pfsense $acl_tmp.csv | grep -v filter\> > $acl_tmp.xml

# Find the last line of rules in original file
marker='/rule'
marker_line=$(echo $(grep -n $marker $acl_file.xml | tail -1) | cut -d: -f1 -)
echo $marker_line

# Insert the new rules into position
sed -e "${marker_line}r $acl_tmp.xml" $acl_file.xml > $acl_final.xml

# Converts a list of CSV aliases to pfSense XML
$BIN_DIR/gen-pfsense-aliases.py $alias_tmp.csv | grep -v aliases\> > $alias_tmp.xml

# Find the last line of aliases in original file
marker='/aliases'
marker_line=$(expr $(echo $(grep -n $marker $alias_file.xml | tail -1) | cut -d: -f1 -) - 1)
echo $marker_line

# Insert the new aliases into position
sed -e "${marker_line}r $alias_tmp.xml" $alias_file.xml > $alias_final.xml

/bin/rm -f $acl_tmp.xml $alias_tmp.xml
#
# End of makexml.sh
#
