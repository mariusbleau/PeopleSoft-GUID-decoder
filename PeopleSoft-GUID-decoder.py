# Author: Marius Bleau
# Email: Marius.Bleau@gmail.com
# Disclaimer: Just started learning Python. The code below works just fine (for my infrastructure) but does not have exception handling.
# About: this was created in order to learn some Python and because the only examples of how to do this in Java are so weird. This is much easier to read and understand.


import argparse
import zlib
import cx_Oracle


# PARSER RELATED STUFF
parser = argparse.ArgumentParser(description="Connects to PeopleSoft DB and extracts information based on GUID, see -h for more info")
inputargs = parser.add_mutually_exclusive_group() # added in order to make the options bellow mutually excusive (use only one of them at the same time)
inputargs.add_argument("-G", '--GUID', type=str, metavar="", help="accepts only one GUID as argument and extracts the request and response")
inputargs.add_argument("-F", '--FILE', type=argparse.FileType('r'), metavar="", help="name of the input file, one GUID per line")
parser.add_argument("-T", '--TIME', type=int, metavar="", help="number of minutes to search in the past, will be used only together with -U. do not use more than 10-30 minutes or you will be forced to take a coffee break")
parser.add_argument("-U", '--USER', type=str, metavar="", help="name of the user that made the request")
args = parser.parse_args()


# DECLARE STUFF FOR THE DB CONNECTION
dsn_tns = cx_Oracle.makedsn('hostname', 'port', 'SID') # replace 'hostname', 'port' and 'SID' with your own stuff
con = cx_Oracle.connect(user='user', password='securepassword', dsn=dsn_tns) # replace 'user' and 'securepassword' with your own stuff
cursor = con.cursor()


# CHECK ARGUMENT AND EXECUTE THE CORRECT STUFF
if args.GUID:
    cursor.execute("SELECT PUBDATALONG FROM psbmpr11.PSIBLOGDATA WHERE guid = '%s'" % args.GUID)
    resp = cursor.fetchall()
    print zlib.decompress(resp[0][0], 0, 1024)
    print "------------------------------"
    print zlib.decompress(resp[1][0], 0, 1024)
    print "\n"
elif args.FILE:
    for line in args.FILE:
        cursor.execute("SELECT PUBDATALONG FROM psbmpr11.PSIBLOGDATA WHERE guid = '%s'" % line.strip())
        resp = cursor.fetchall()
        print zlib.decompress(resp[0][0], 0, 1024)
        print "------------------------------"
        print zlib.decompress(resp[1][0], 0, 1024)
        print "\n"
elif args.USER and args.TIME:
    cursor.execute("select GUID from psbmpr11.PSIBLOGHDR where LASTUPDDTTM > sysdate - (%i/1440) AND Upper(PUBLISHER)=Upper('%s')" % (args.TIME, args.USER))
    get_guid = cursor.fetchall()
    for value in get_guid:
        cursor.execute("SELECT pubdatalong FROM psbmpr11.PSIBLOGDATA WHERE guid = '%s'" % value)
        resp = cursor.fetchall()
        print zlib.decompress(resp[0][0], 0, 1024)
        print "------------------------------"
        print zlib.decompress(resp[1][0], 0, 1024)
        print "\n"
