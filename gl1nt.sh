#!/bin/bash

# Finish output messages
# Work on input user to add flexibility
# Add modes
# Add Ports loop
# Finish ffuf
# finish to add all tools
# Add Style to the outputs
# Add Banner
# Add dorkings


# Path to the tool in your system
PATH_TO_DIRSEARCH="/PATH/TO/USER"
TODAY=$(date)
echo "What a lovelly $TODAY to Hack The Planet!!"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY"
mkdir $DIRECTORY
# Nmap -
nmap_scan()
{
    nmap $DOMAIN > $DIRECTORY/nmap
    echo "Nmap logs ready --> $DIRECTORY/nmap"
}
# dirsearch - Feroxbuster
dirsearch_scan()
{
    $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
    echo "Dirsearch logs ready --> $DIRECTORY/dirsearch"
}
# Crt Scan
crt_scan()
{
    curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
    echo "Crt scan logs ready --> $DIRECTORY/crt."
}
# Feroxbuster
feroxbuster_scan()
{
    feroxbuster $DOMAIN > $DIRECTORY/feroxbuster
    echo "Feroxbuster logs ready --> $DIRECTORY/feroxbuster"
}
# ffuf - Directories Only so far
ffuf_scan()
{
    ffuf -w wordlist.txt:FUZZ -u $DOMAIN/FUZZ
    ffuf -w subdomains-top1million-5000.txt:FUZZ -u FUZZ.$DOMAIN > $DIRECTORY/ffuf_domains

}
# gobuster
# wfuzz



# Alternetives 
case $2 in
    nmap-only)
    nmap_scan
    ;;
    dirsearch-only)
    dirsearch_scan
    ;;
    crt-only)
    crt_scan
    ;;
    *)
    nmap_scan
    dirsearch_scan
    crt_scan
    ;;
esac
echo "Generating recon report from output files..."
TODAY=$(date)
echo "This scan was created on $TODAY" > $DIRECTORY/report
echo "Results for Nmap:" >> $DIRECTORY/report
grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
echo "Results for Dirsearch:" >> $DIRECTORY/report
cat $DIRECTORY/dirsearch >> $DIRECTORY/report
echo "Results for crt.sh:" >> $DIRECTORY/report
jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report