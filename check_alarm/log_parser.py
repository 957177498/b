#! /usr/bin/python
# encoding:utf-8

import re
import paramiko
import tools
from datetime import datetime, timedelta
import check_mysql
import MySQLdb


log1="""/usr/sbin/mysqld, Version: 5.6.27-0ubuntu0.14.04.1 ((Ubuntu)). started with:
Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
Time                 Id Command    Argument
# Time: 160218 18:00:39
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 61154
# Query_time: 11.293570  Lock_time: 0.861997 Rows_sent: 0  Rows_examined: 0
use dtops_test;
SET timestamp=1455789639;
SELECT `ecs_hourinstancemonitordata`.`id`, `ecs_hourinstancemonitordata`.`InstanceId`, `ecs_hourinstancemonitordata`.`CPU`, `ecs_hourinstancemonitordata`.`IntranetRX`, `ecs_hourin
stancemonitordata`.`IntranetTX`, `ecs_hourinstancemonitordata`.`IntranetBandwidth`, `ecs_hourinstancemonitordata`.`InternetRX`, `ecs_hourinstancemonitordata`.`InternetTX`, `ecs_ho
urinstancemonitordata`.`InternetBandwidth`, `ecs_hourinstancemonitordata`.`IOPSRead`, `ecs_hourinstancemonitordata`.`IOPSWrite`, `ecs_hourinstancemonitordata`.`BPSRead`, `ecs_hour
instancemonitordata`.`BPSWrite`, `ecs_hourinstancemonitordata`.`TimeStamp` FROM `ecs_hourinstancemonitordata` WHERE (`ecs_hourinstancemonitordata`.`InstanceId` = 1 AND `ecs_hourin
stancemonitordata`.`TimeStamp` >= '2016-02-17 10:00:27.793648' AND `ecs_hourinstancemonitordata`.`TimeStamp` < '2016-02-18 10:00:27.793648');
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 61157
# Query_time: 11.325522  Lock_time: 0.894025 Rows_sent: 2  Rows_examined: 2
use dtops_perf;
SET timestamp=1455789639;
SELECT `dbops_host_list`.`host_id`, `dbops_host_list`.`tenant_id`, `dbops_host_list`.`host_name`, `dbops_host_list`.`ip`, `dbops_host_list`.`idc`, `dbops_host_list`.`os_type`, `db
ops_host_list`.`load1`, `dbops_host_list`.`up_days`, `dbops_host_list`.`gmt_modified` FROM `dbops_host_list` WHERE `dbops_host_list`.`user_id` = 6;
# Time: 160218 18:30:25
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 62376
# Query_time: 15.920030  Lock_time: 3.956444 Rows_sent: 341  Rows_examined: 341
SET timestamp=1455791425;
/*vcopts=sampleexplain*/ SHOW /*!50003 GLOBAL*/ STATUS;
# Time: 160218 18:30:29
# User@Host: monitor[monitor] @  [120.55.81.111]  Id: 62246
# Query_time: 19.583696  Lock_time: 3.956475 Rows_sent: 341  Rows_examined: 341
SET timestamp=1455791429;
/*vcopts=sampleexplain*/ SHOW /*!50003 GLOBAL*/ STATUS;
# Time: 160218 18:30:34
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 62232
# Query_time: 24.647439  Lock_time: 7.410976 Rows_sent: 13  Rows_examined: 13
SET timestamp=1455791434;
/*vcopts=sampleexplain*/ SELECT ID, USER, HOST, DB, COMMAND, TIME, STATE, INFO FROM information_schema.processlist;
# Time: 2016-08-29T10:01:29.610606Z
# User@Host: monitor[monitor] @ localhost [127.0.0.1]  Id:  3795
# Query_time: 0.086522  Lock_time: 0.000118 Rows_sent: 1  Rows_examined: 706
SET timestamp=1472464889;
show global status where variable_name in (
            'uptime',
            'x'
        );
"""


log2 = """
# Time: 2016-09-10T08:31:56.192844Z
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 10856
# Schema:   Last_errno: 0  Killed: 0
# Query_time: 1.001602  Lock_time: 0.000000  Rows_sent: 1  Rows_examined: 0  Rows_affected: 0
# Bytes_sent: 63
SET timestamp=1473496316;
select sleep(1);
# Time: 2016-09-10T08:31:58.609792Z
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 10856
# Schema:   Last_errno: 0  Killed: 0
# Query_time: 1.000284  Lock_time: 0.000000  Rows_sent: 1  Rows_examined: 0  Rows_affected: 0
# Bytes_sent: 63
SET timestamp=1473496318;
select sleep(1);
# Time: 2016-09-10T08:32:15.651339Z
# User@Host: root[root] @ localhost [127.0.0.1]  Id: 10856
# Schema:   Last_errno: 0  Killed: 0
# Query_time: 14.095501  Lock_time: 0.000000  Rows_sent: 1  Rows_examined: 0  Rows_affected: 0
# Bytes_sent: 65
SET timestamp=1473496335;


# Time: 160910 16:12:34
# User@Host: dtlog[dtlog] @  [120.55.81.111]  Id: 1778143
# Query_time: 0.077018  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0
SET timestamp=1473495154;
commit;
# Time: 160910 16:15:36
# User@Host: dtlog[dtlog] @  [120.55.81.111]  Id: 1779343
# Query_time: 0.083835  Lock_time: 0.000117 Rows_sent: 0  Rows_examined: 0
SET timestamp=1473495336;
insert into dtops_slow_log (query_times,return_row_counts,user_id,check_time,tenant_id,start_time,parse_row_counts,instance_name,db_name,sql_text,lock_times,host_address) values('24.647439','13',1,'2016-09-10 08:15:36.259234',1,'2016-02-18 10:30:09.352561','13','test','dtops_perf','/*vcopts=sampleexplain*/ SELECT ID, USER, HOST, DB, COMMAND, TIME, STATE, INFO FROM information_schema.processlist;
# Time: 2016-08-29T10:01:29.610606Z','7.410976','root[root] @ localhost [127.0.0.1]');

# Time: 2016-09-10T08:07:09.307948Z
# User@Host: root[root] @ localhost []  Id: 84798
# Query_time: 1.000277  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1473494829;
select sleep(1);
# Time: 2016-09-10T08:07:11.240015Z
# User@Host: root[root] @ localhost []  Id: 84798
# Query_time: 1.000256  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1473494831;
select sleep(1);


# Time: 2016-09-10T08:07:12.986405Z
# User@Host: root[root] @ localhost []  Id: 84798
# Query_time: 1.000265  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1473494832;
select sleep(1);
# Time: 2016-09-10T08:07:16.846098Z
# User@Host: root[root] @ localhost []  Id: 84798
# Query_time: 1.000249  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1473494836;
select sleep(1);
# Time: 2016-09-10T08:08:40.323492Z
# User@Host: root[root] @ localhost []  Id: 84808
# Query_time: 1.000276  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1473494920;
select sleep(1);

/usr/sbin/mysqld, Version: 5.5.46-MariaDB-log (openSUSE package). started with:
Tcp port: 3306  Unix socket: /var/run/mysql/mysql.sock
Time                 Id Command    Argument
# Time: 160910 16:28:32
# User@Host: root[root] @ localhost []
# Thread_id: 108673  Schema:   QC_hit: No
# Query_time: 1.000178  Lock_time: 0.000000  Rows_sent: 1  Rows_examined: 0
SET timestamp=1473496112;
select sleep(1);

# Time: 180530 16:53:23
# User@Host: x_user_new[x_new] @  [10.1.3.4]  Id: 1368082
# Schema: x_user  Last_errno: 0  Killed: 0
# Query_time: 2.766787  Lock_time: 0.000133  Rows_sent: 0  Rows_examined: 471266  Rows_affected: 0
# Bytes_sent: 2208
SET timestamp=1527670403;
SELECT id,
        FROM tab
        where 1=1
        ORDER BY gmt_modify DESC;
"""

log3 = """
Sat May 05 18:24:42 2018
MRP0: Background Media Recovery cancelled with status 16037
Errors in file /u01/app/oracle/diag/rdbms/orcl_adg/orcl/trace/orcl_mrp0_45273.trc:
ORA-16037: user requested cancel of managed recovery operation
Managed Standby Recovery not using Real Time Apply
Recovery interrupted!
Recovered data files to a consistent state at change 35898735
MRP0: Background Media Recovery process shutdown (orcl)
Managed Standby Recovery Canceled (orcl)
Completed: alter database recover managed standby database cancel
alter database commit to switchover to primary with session shutdown
ALTER DATABASE SWITCHOVER TO PRIMARY (orcl)
Maximum wait for role transition is 15 minutes.
Database not available for switchover
  End-Of-REDO archived log file has not been recovered
  Archived log files detected beyond End-Of-REDO
  Incomplete recovery SCN:0:35898735 archive SCN:0:35889506
Database not available for switchover
  End-Of-REDO archived log file has not been recovered
  Archived log files detected beyond End-Of-REDO
  Incomplete recovery SCN:0:35898735 archive SCN:0:35889506
Switchover: Media recovery required - standby not in limbo
ORA-16139 signalled during: alter database commit to switchover to primary with session shutdown...
alter database open
ORA-1531 signalled during: alter database open...
Sat May 05 18:25:22 2018
Primary database is in MAXIMUM PERFORMANCE mode
RFS[8]: Assigned to RFS process 50756
RFS[8]: Selected log 5 for thread 1 sequence 1906 dbid 1485808053 branch 960908345
Sat May 05 18:25:22 2018
RFS[9]: Assigned to RFS process 50758
RFS[9]: Selected log 4 for thread 1 sequence 1905 dbid 1485808053 branch 960908345
Sat May 05 18:25:23 2018
Archived Log entry 1063 added for thread 1 sequence 1905 ID 0x5a9831f8 dest 1
"""

TZ_ADJUST = timedelta(hours=8)

def slowlog_test_stream(log):
    log_lines = log.splitlines()
    for line in log_lines:
        if line != '':
            yield (line, 0)

    yield ('', 0)

def save_data(host,port,tags,slow_log_file,SQL_META):
    if SQL_META:
        start_time = SQL_META['start_time']
        host_client = SQL_META['host']
        db_name = ''
        if 'db_name' in SQL_META:
            db_name = SQL_META['db_name']
        sql_text = SQL_META['sql_text']
        query_time = float(SQL_META['query_time'])
        lock_time = float(SQL_META['lock_time'])
        rows_examined = int(SQL_META['rows_examined'])
        rows_sent = int(SQL_META['rows_sent'])
        thread_id = SQL_META['thread_id']

        if not sql_text.startswith('commit'):
            sql = "insert into mysql_slowquery(host,port,tags,slow_log_file,start_time,client_host,db_name,sql_text,query_time,lock_time," \
                  "rows_examined,rows_sent,thread_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            values = (
                host, port, tags, slow_log_file, start_time, host_client, db_name, sql_text, query_time, lock_time,
                rows_examined,
                rows_sent, thread_id)

            tools.mysql_exec(sql, values)


SQL_META_MAP = {}

def parse_slow_logs(log_stream,tags,host,port,slow_log_file):
    ## User@Host: root[root] @ localhost [127.0.0.1]  Id: 626474
    # Query_time: 0.230439  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0
    #use dtops_test;

    SQL_META = {}

    reg_ts = re.compile('^SET timestamp=\d+;$')


    reg_time = re.compile('^# Time: ((\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.*?$)|((\d\d\d\d\d\d (?:\d| )\d:\d\d:\d\d)$))')
    # reg_host = re.compile('^# User@Host: (.+) @ (.*) \[(.*)\](?:  Id: (\d+))?$')
    reg_host = re.compile('^# User@Host:\s+(.*\])(?:\s+Id:\s+(\d+))?$')
    reg_querytime = re.compile('^# Query_time:\s+(\d+\.\d+)\s+Lock_time:\s+(\d+\.\d+)\s+Rows_sent:\s+(\d+)\s+Rows_examined:\s+(\d+)')
    reg_db = re.compile('^use ([^;]*);$')
    reg_schema = re.compile('^# Schema: (\w+)')
    reg_ignore = re.compile('^# Bytes_sent:')


    #state 0: before match
    #state 1: get time
    #state 2: get host
    #state 3: get query time
    #state 4: match sql
    sql_lines = []
    state = 0
    for log_l, f_pos in log_stream:
        if state == 0:
            m = reg_time.match(log_l)
            if m:
                state = 1
                query_start_time = m.groups()[0]
                SQL_META['start_time'] = query_start_time
        elif state == 1:
            m = reg_host.match(log_l)
            if m:
                state = 2
                host, thread_id = m.groups()
                SQL_META['host'] = host
                SQL_META['thread_id'] = thread_id
        elif state == 2:
            m = reg_schema.match(log_l)
            if m:
                SQL_META['db_name'] = m.groups()[0]

            m = reg_querytime.match(log_l)
            if m:
                state = 3
                query_time, lock_time, rows_sent, rows_examined = m.groups()
                SQL_META['query_time'] = query_time
                SQL_META['lock_time'] = lock_time
                SQL_META['rows_sent'] = rows_sent
                SQL_META['rows_examined'] = rows_examined
        elif state == 3:
            m = reg_time.match(log_l)
            if m:
                query_start_time = m.groups()[0]
                state = 1
                if len(sql_lines) > 0:
                    sql_text = "".join(sql_lines).strip()
                    SQL_META['sql_text'] = sql_text
                    save_data(host,port,tags,slow_log_file,SQL_META)

                sql_lines = []
                SQL_META['start_time'] = query_start_time
            elif log_l == '':
                sql_text = "".join(sql_lines).strip()
                SQL_META['sql_text'] = sql_text
                save_data(host, port, tags, slow_log_file, SQL_META)

            else:
                # same query time
                m = reg_host.match(log_l)
                if m:
                    state = 2
                    host, thread_id = m.groups()

                    sql_text = "".join(sql_lines)
                    SQL_META['sql_text'] = sql_text.strip()
                    save_data(host,port,tags,slow_log_file,SQL_META)

                    SQL_META['host'] = host
                    SQL_META['thread_id'] = thread_id
                    sql_lines = []
                else:
                    # /usr/sbin/mysqld, Version: 5.6.27-0ubuntu0.14.04.1 ((Ubuntu)). started with:
                    # Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
                    # Time                 Id Command    Argument


                    if reg_ts.match(log_l) or log_l == '':
                        continue
                    else:
                        m = reg_db.match(log_l)
                        if m:
                            SQL_META['db_name'] = m.groups()[0]
                        else:
                            m = reg_ignore.match(log_l)
                            if m:
                                continue
                            sql_lines.append(log_l)

        #end of file
        if log_l == '':
            return f_pos


def test_slow_log():
    parse_slow_logs(slowlog_test_stream(), 'test')



def get_log_level_oracle(log_content):
    if 'ORA-' in log_content or 'Error' in log_content:
        return "error"
    elif 'Starting ORACLE instance' in log_content:
        return 'startup'
    elif 'Shutting down instance' in log_content:
        return 'shutdown'
    else:
        return "info"

def oracle_alert_stream(log):
    log_lines = log.splitlines()
    for line in log_lines:
        if log_lines != '':
            yield (line, 0)

    yield ('', 0)

OracleKeyWordList=['ORA-','Starting ORACLE instance','Shutting down instance']

def save_oracle_alert_log(tags,host,log_meta):
    for key in OracleKeyWordList:
        if log_meta:
            save = False
            if key in log_meta['log_content']:
                save = True
            if save:
                if log_meta.has_key('log_time'):
                    log_time = log_meta['log_time']
                else:
                    log_time = ''
                sql = "insert into alert_log(tags,host,server_type,log_time,log_level,log_content) values(%s,%s,%s,%s,%s,%s)"
                values = (tags, host, 'Oracle',log_time, log_meta['log_level'], log_meta['log_content'])
                tools.mysql_exec(sql, values)
                log_meta = []


def parse_oracle_alert_logs(tags,host,log_stream,version):
    """Wed Mar 02 14:00:30 2016"""
    # datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')
    log_buffer = []

    log_meta = {}

    for log_line, log_pos in log_stream:
        try:
            log_line_strip = log_line.strip()
            if version == '12c':
                log_time = datetime.strptime(log_line_strip, '%Y-%m-%dT%H:%M:%S.%f+08:00')
            else:
                log_time = datetime.strptime(log_line_strip, '%a %b %d %H:%M:%S %Y')

            match_time = True

        except ValueError:
            match_time = False

        if match_time:
            if len(log_buffer) > 0:
                log_content = "\r\n".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_oracle(log_content)
                save_oracle_alert_log(tags,host,log_meta)
                log_buffer = []


            log_meta['log_time'] = str(log_time)
        else:
            if log_line != '':
                log_buffer.append(log_line)

        if len(log_buffer) > 100:
            log_content = "\r\n".join(log_buffer).strip()
            log_meta['log_content'] = log_content
            log_meta['log_level'] = get_log_level_oracle(log_content)
            save_oracle_alert_log(tags, host, log_meta)
            log_buffer = []

    if len(log_buffer) > 0:
        log_content = "\r\n".join(log_buffer).strip()
        log_meta['log_content'] = log_content
        log_meta['log_level'] = get_log_level_oracle(log_content)
        save_oracle_alert_log(tags, host, log_meta)

    return log_pos


def mysql_slow_query(tags,host,port,user,password,slow_log_file):
    # 建立ssh连接
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, 22, user, password)
    #获取慢查询日志文件
    command = 'cat %s' % slow_log_file
    std_in, std_out, std_err = ssh_client.exec_command(command)
    fd = std_out
    log = fd.read()
    # 日志解析
    parse_slow_logs(slowlog_test_stream(log), tags,host,port,slow_log_file)


MysqlKeyWordList=['ERROR','Warning']

def mysql_errorlog_stream(log):
    log_lines = log.splitlines()
    for line in log_lines:
        if log_lines != '':
            yield (line, 0)

    yield ('', 0)

def get_log_level_mysql(log_content):
    if "[ERROR]" in log_content:
        return "error"
    elif "[Warning]" in log_content:
        return "warn"
    else:
        return "info"


def save_mysql_alert_log(tags,host,log_meta):
    for key in MysqlKeyWordList:
        if log_meta:
            save = False
            if key in log_meta['log_content']:
                save = True
            if save:
                if log_meta.has_key('log_time'):
                    log_time = log_meta['log_time']
                else:
                    log_time = ''
                sql = "insert into alert_log(tags,host,server_type,log_time,log_level,log_content) values(%s,%s,%s,%s,%s,%s)"
                values = (tags, host,'MySQL',log_time, log_meta['log_level'], log_meta['log_content'])
                tools.mysql_exec(sql, values)
                log_meta = []


def parse_mysql_alert_logs(tags,host,log_stream):

    log_meta = {}

    reg_date = re.compile('(\d{6} \d{2}:\d{2}:\d{2})|(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')

    log_buffer = []

    for log_line, log_pos in log_stream:
        if log_line == '\n' or log_line == '':
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_mysql(log_content)
                save_mysql_alert_log(tags,host,log_meta)
                log_buffer = []
            continue

        m = reg_date.match(log_line)
        if m:
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_mysql(log_content)
                save_mysql_alert_log(tags,host,log_meta)
                log_buffer = []

            log_t1, log_t2,log_t3 = m.groups()
            if log_t2 is not None:
                log_time = datetime.strptime(log_t2, '%Y-%m-%d %H:%M:%S')
            elif log_t3 is not None:
                log_time = datetime.strptime(log_t3, '%Y-%m-%dT%H:%M:%S')
            else:
                log_time = datetime.strptime(log_t1, '%y%m%d %H:%M:%S')

            log_meta['log_time'] = str(log_time - TZ_ADJUST)
            log_meta['log_content'] = log_line.strip()
            log_meta['log_level'] = get_log_level_mysql(log_line)
            save_mysql_alert_log(tags, host, log_meta)
            continue

        log_buffer.append(log_line)
        if len(log_buffer) > 100:
            log_content = "".join(log_buffer).strip()
            log_meta['log_content'] = log_content
            log_meta['log_level'] = get_log_level_mysql(log_content)
            save_mysql_alert_log(tags, host, log_meta)
            log_buffer = []

    if len(log_buffer) > 0:
        log_content = "".join(log_buffer).strip()
        log_meta['log_content'] = log_content
        log_meta['log_level'] = get_log_level_mysql(log_content)
        save_mysql_alert_log(tags, host, log_meta)
        log_buffer = []

    return log_pos


def get_oracle_alert(conn,tags,host,user,password,ssh_port,version):
    # 取后台日志路径
    cur = conn.cursor()
    diag_trace_sql = "select value from v$diag_info where name = 'Diag Trace'"
    cur.execute(diag_trace_sql)
    diag_trace = cur.fetchall()
    diag_trace_dir = diag_trace[0][0]
    # 建立ssh连接，抓取后台日志
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, ssh_port, user, password)
    command = 'tail -300 %s/alert_*.log' %diag_trace_dir
    std_in, std_out, std_err = ssh_client.exec_command(command)
    fd = std_out
    log = fd.read()
    # 清空原日志数据
    sql = "delete from alert_log where tags='%s'  and server_type='Oracle' " %tags
    tools.mysql_exec(sql,'')
    parse_oracle_alert_logs(tags,host,oracle_alert_stream(log),version)

def get_mysql_alert(conn,tags,host,user,password):
    # 取后台日志路径
    alert_log = check_mysql.get_mysql_para(conn,'log_error')
    # 建立ssh连接，抓取后台日志
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, 22, user, password)
    command = 'tail -300 %s' %alert_log
    std_in, std_out, std_err = ssh_client.exec_command(command)
    fd = std_out
    log = fd.read()
    # 清空原日志数据
    sql = "delete from alert_log where tags='%s' and server_type='MySQL' " %tags
    tools.mysql_exec(sql,'')
    parse_mysql_alert_logs(tags,host,oracle_alert_stream(log))


if __name__ == '__main__':

    tags = 'mysql'
    host = '192.168.48.50'
    port = 3306
    user = 'mysql'
    password = 'mysqld'
    conn = MySQLdb.connect(host=host, user='root', passwd='mysqld', port=int(port), connect_timeout=5, charset='utf8')
    # 清空原日志数据
    sql = "delete from alert_log where tags='%s' " % tags
    tools.mysql_exec(sql, '')
    get_mysql_alert(conn,tags,host,user,password)





