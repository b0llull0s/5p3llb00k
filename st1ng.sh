#!/bin/bash
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
# St1ng - By b0llull0s

# Display Function
usage() {
    echo "Usage: $0 -u URL -d IP_ADDRESS -p PORT -f FILE_NAME [-c] [-w] [-l]"
    echo "  -u URL          : URL to download the file from"
    echo "  -d IP_ADDRESS   : IP address to send the file to (ignored in listening mode)"
    echo "  -p PORT         : Port number to send or listen on"
    echo "  -f FILE_NAME    : Name of the file to save and send"
    echo "  -c              : Use curl to download the file (default is wget)"
    echo "  -w              : Use wget to download the file (default if neither -c nor -w is specified)"
    echo "  -l              : Listen for inbound connections instead of sending outbound"
    exit 1
}

# Variables
use_curl=false
use_wget=false
listen_mode=false

# Aguments
while getopts "u:d:p:f:cwl" opt; do
    case ${opt} in
        u ) url=$OPTARG ;;
        d ) ip_address=$OPTARG ;;
        p ) port=$OPTARG ;;
        f ) file_name=$OPTARG ;;
        c ) use_curl=true ;;
        w ) use_wget=true ;;
        l ) listen_mode=true ;;
        * ) usage ;;
    esac
done

# Validation
if [ -z "$url" ] || [ -z "$port" ] || [ -z "$file_name" ]; then
    usage
fi

if [ "$use_curl" = false ] && [ "$use_wget" = false ]; then
    use_wget=true
fi

# Downloading loop
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
if [ "$listen_mode" = true ]; then
    echo "Listening for inbound connections using ncat..."
    sudo ncat -l -p "$port" --send-only < "$file_name"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to listen for inbound connections using ncat."
        exit 1
    fi
else
    if [ -z "$ip_address" ]; then
        usage
    fi
    echo "Sending file using ncat..."
    ncat --send-only "$ip_address" "$port" < "$file_name"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to send file using ncat."
        exit 1
    fi
fi

echo "Operation completed successfully."
