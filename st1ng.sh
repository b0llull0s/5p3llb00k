#!/bin/bash
# St1ng - By b0llull0s
echo "      .. ..',..''''','',,,,,,,,,,',,,,'.,,',,,,,,;,,,,,,,,,,,,'.',,'.  ..."
echo "       .   ..'...'.,'''''',,;;;,,,,;,,''.',';,,,;;;;;,,,,,,'......,'.    .."
echo "            .'..'..'',,;,;;;;;;;,;;;,,.';;;',;;;;:;;;;;;;,,...''';,.   ."
echo "             .....'''''''''''''''''''..''''.'''''''''''''''''.....'."
echo "            .,;;:;;::::;,,,'''.'',;;::;;;;::::;,,'',;;;;:::::;;;;;'.    ...."
echo "           .',,,''',,,,','.. .......',''',,,''''.....''',,,,,'',,,'.    ...."
echo "           ....''.....            . .',,','..... .   ........'',,,''.     ."
echo "            ... .                   ..';;;.....                .'''.."
echo "            .                         .........                    ."
echo "         .'.                          ..'......                    ..."
echo "         ',.           ...     ..    .;,,,'.'..              ..     ''"
echo "         .'            ...         .'','''.','.                     ..."
echo "        .',.    ........'.  .    .,;,. ..  .:;,'.       ....        .,'"
echo "        ..''.   ...'.......... ..','.       .''''.   .........      ...."
echo "       .....,,.....'......'....,,,;.         .''',,............    .',.."
echo "      .';,. ..''''''..',;,;,,.'',,'          .......''','........''''..'"
echo "   ....,,''..   ......',''..   .'.             ..........''...'.......''."
echo "   ...',;,,...      ..,,;;'.. .;.              .....,,,'.'.. ......';;;:,...."
echo "       .....          ....,,....                .'.','''..      ...''''.. .."
echo "        ...   . ..       .,,..''                .'.,;,'..    ...  ...,."
echo "               ............;,.,,.       ..      ''',,....  ...'.....'.."
echo "                    .........'''.      .'.     ..''.... ........   .."
echo "                     ...''.';:;;;;'...;:;,'....;':;,','  .;,..                  .."
# Display function
usage() {
    echo "Usage: $0 -u URL -d IP_ADDRESS -p PORT -f FILE_NAME [-c] [-w]"
    echo "  -u URL          : URL to download the file from"
    echo "  -d IP_ADDRESS   : IP address to send the file to"
    echo "  -p PORT         : Port number to send the file to"
    echo "  -f FILE_NAME    : Name of the file to save and send"
    echo "  -c              : Use curl to download the file (default is wget)"
    exit 1
}

# Variables
use_curl=false
use_wget=false

# Arguments
while getopts "u:d:p:f:cw" opt; do
    case ${opt} in
        u ) url=$OPTARG ;;
        d ) ip_address=$OPTARG ;;
        p ) port=$OPTARG ;;
        f ) file_name=$OPTARG ;;
        c ) use_curl=true ;;
        w ) use_wget=true ;;
        * ) usage ;;
    esac
done

# Validate arguments
if [ -z "$url" ] || [ -z "$ip_address" ] || [ -z "$port" ] || [ -z "$file_name" ]; then
    usage
fi

if [ "$use_curl" = false ] && [ "$use_wget" = false ]; then
    use_wget=true
fi

# Download loop
if [ "$use_curl" = true ]; then
    echo "Downloading file using curl..."
    curl -o "$file_name" "$url"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download file using curl."
        exit 1
    fi
elif [ "$use_wget" = true ]; then
    echo "Downloading file using wget..."
    wget -O "$file_name" "$url"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download file using wget."
        exit 1
    fi
fi

# Ncat loop
echo "Sending file using ncat..."
ncat --send-only "$ip_address" "$port" < "$file_name"
if [ $? -ne 0 ]; then
    echo "Error: Failed to send file using ncat."
    exit 1
fi

echo "File sent successfully."
