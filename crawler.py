import os
import time
import sys
import re
import sqlite3

from win_unc import (DiskDrive, UncDirectory,
                     UncDirectoryConnection, UncDirectoryMount)
from win_unc.errors import ShellCommandError
from win_unc.errors import NoDrivesAvailableError


def main():
    while 1:

        # conn = sqlite3.connect("lan.db")
        # curr = conn.cursor()
        # curr.execute("DELETE FROM lan_crawler_table ")
        # conn.commit()
        smb_connection_check()

        print 'program start after specific time'

        time.sleep(30)

        conn = sqlite3.connect("lan.db")
        curr = conn.cursor()
        curr.execute("DELETE FROM lan_crawler_table ")
        conn.commit()

def smb_connection_check():
    print 'main'
    # Connect a shared directory without authorization.
    for i in range(179, 181):

        unc = UncDirectory(r'\\192.168.77.%d\share' % i)
        path = unc.get_path()
        print path
        conn = UncDirectoryConnection(unc, persistent=True)
        status1 = conn.get_connection_status()
        print 'before connection', status1
        try:
            conn.connect()
        except ShellCommandError:
            print 'shellcommand error'
        except:
            print 'unknown error'

        if conn.is_connected() == True:
            status2 = conn.get_connection_status()
            print 'ip 192.168.77.%d' % i, 'is connected '
            print 'after conncetion', status2
            print 'Connected?', conn.is_connected()
            # calling mount function
            mount(path)
            print 'after excuting mount function'
            conn.disconnect()
            print 'after disconnection'
            print '----------------'
        else:
            print '192.168.0.%d' % (i), 'is not connected'
            print '-----------------'


def mount(path):
    print 'in mount function'
    # Setup a connection handler:
    conn = UncDirectoryMount(UncDirectory(path), DiskDrive('P:'))
    # conn = UncDirectoryMount(path, DiskDrive('Z:'))
    print 'before mounting'
    try:
        conn.mount()
    except NoDrivesAvailableError:
        print 'no drive availavle to mount'
    except:
        print 'there is problem in mountig'

    print 'Drive connected:?', conn.is_mounted()
    print "Mounted at:", conn.disk_drive
    # calling metadata_fetch function()
    metadata(path)
    try:
        conn.unmount()
    except:
        print 'there is some problem in unmounting'
        # assert (not conn.is_mounted())


def metadata(path):
    print 'in metadata fuction'
    for root, dirs, files in os.walk(path):
        print "current location", root
        print "folder inside current location(", root, "):", dirs
        print "files inside current locatiion(", root, "):", files

        # file variabel contain name of the file
        for file in files:
            print 'file Name:',file
            # print re.findall(r'.[\w]+', file)
            # print 'absolute path', os.path.abspath(file)

            # fp variable give full path
            fp = os.path.join(root, file)
            print 'file full path:', fp

            # chexk file or not
            print 'file?',os.path.isfile(fp)

            # file_size variable give file size
            file_size = os.path.getsize(fp)
            print 'file_size:',file_size

            # file_created_time give file created time
            var1 = os.path.getctime(fp)
            file_created_time = time.ctime(var1)
            print 'file created time:',file_created_time

            # file_extension variable give extension of that file
            filename, file_extension = os.path.splitext(file)
            print 'extension of these file:',file_extension

            # calling lan_database
            lan_database(file, fp, file_extension, file_size, file_created_time)
            print 'retuned from database function'


def lan_database(file, fp, file_extension, file_size, file_created_time):
    print 'in database function'
    conn = sqlite3.connect("lan.db")
    curr = conn.cursor()

    # curr.execute("DROP TABLE IF EXISTS lan_crawler_table")

    curr.execute("CREATE TABLE IF NOT EXISTS lan_crawler_table( \
                      Id INTEGER PRIMARY KEY NOT NULL ,\
                      Name TEXT NOT NULL , \
                      Path TEXT NOT NULL , \
                      Extension TEXT(10) NOT NULL, \
                      Size INTEGER NOT NULL , \
                      Date NUMERIC NOT NULL );")

    print 'database successfully created'
    curr.execute("INSERT INTO lan_crawler_table (Name, Path, Extension, Size, Date) \
                        VALUES (?,?,?,?,?)", [file, fp, file_extension, file_size, file_created_time]);
    conn.commit()
    print 'insertion completed'
    #
    #
    # row_count = curr.execute("SELECT COUNT(*) FROM lan_crawler_table").fetchone()[0]
    #
    # # Number_of_rows = curr.execute("SELECT count(*) FROM lan_crawler_table")
    # # row_count = len(Number_of_rows.fetchall())
    # print 'checking no of rows'
    # print 'row_count',row_count
    #
    # if row_count == 0:
    #     curr.execute("INSERT INTO lan_crawler_table (Name, Path, Extension, Size, Date) \
    #                          VALUES (?,?,?,?,?)", [file, fp, file_extension, file_size, file_created_time]);
    #     conn.commit()
    #     print 'insertion completed'
    #
    # else :
    #     ret = curr.execute("SELECT count(*) FROM lan_crawler_table WHERE Name = 'file' AND Path = 'fp' \
    #                  AND Extension = 'file_extension' AND Size = 'file_size' AND Date = 'file_created_time'")
    #     conn.commit()
    #     dup_count = len(ret.fetchall())
    #     print "duplicate count",dup_count
    #
    #     if ret == 0:
    #         curr.execute("INSERT INTO lan_crawler_table (Name, Path, Extension, Size, Date) \
    #                       VALUES (?,?,?,?,?)", [file, fp, file_extension, file_size, file_created_time]);
    #         conn.commit()
    #         print "insert metadata due to duplication is not present"
    #     else:
    #         curr.execute("DELETE FROM lan_crawler_table WHERE Name = 'file' AND Path = 'fp' \
    #                  AND Extension = 'file_extension' AND Size = 'file_size' AND Date = 'file_created_time'")
    #         conn.commit()
    #         print "deleting metadata due to duplication"

    curr.execute("SELECT Id, Name, Path, Extension, Size, Date  FROM lan_crawler_table");

    for row in curr:
        print row
    conn.commit()
    conn.close()
    print 'last statement'

# time.sleep(600)

if __name__ == '__main__':
    main()
