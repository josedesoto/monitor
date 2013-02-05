#! /bin/bash
#
# collectd - start and stop the statistics collection daemon

### BEGIN INIT INFO
# Provides:          collectd
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Should-Start:      $network $named $syslog $time
# Should-Stop:       $network $named $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start the statistics collection daemon
### END INIT INFO

set -e



DESC="statistics collection and monitoring daemon"
NAME=collectd
DAEMON=/opt/collectd/sbin/collectd

#We are using dmon, so we type pid file for dmon
PIDFILE=/opt/collectd/var/run/collectdmon.pid

CONFIGFILE=/opt/collectd/etc/collectd.conf
COLLECTDMON_DAEMON=/opt/collectd/sbin/collectdmon

MAXWAIT=30

case "$1" in
start)

    if test ! -e "$CONFIGFILE"; then
        # we get here during restart
        echo -n " - no configuration ($CONFIGFILE) found."
        return 0
    fi

    if ! $DAEMON -t -C "$CONFIGFILE"; then
        if test -n "$1"; then
            echo "$1" >&2
        fi
        exit 1
    fi

    start-stop-daemon --start --quiet --oknodo --exec $COLLECTDMON_DAEMON -- -c "$DAEMON"



;;
stop) 
    PID=$( cat "$PIDFILE" 2> /dev/null ) || true

    start-stop-daemon --stop --quiet --oknodo --pidfile "$PIDFILE"

    sleep 1
    if test -n "$PID" && kill -0 $PID 2> /dev/null; then
        i=0
        while kill -0 $PID 2> /dev/null; do
            i=$(( $i + 2 ))
            echo -n " ."

            if test $i -gt $MAXWAIT; then
                echo "$still_running_warning" >&2
                return 1
            fi

            sleep 2
        done
        return 0
    fi

;;
restart)
	echo "Not yet developed"



;;
status)
    PID=$( cat "$PIDFILE" 2> /dev/null ) || true

    if test -n "$PID" && kill -0 $PID 2> /dev/null; then
        echo "collectd ($PID) is running."
        exit 0
    else
        PID=$( pidof collectd ) || true

        if test -n "$PID"; then
            echo "collectd ($PID) is running."
            exit 0
        else
            echo "collectd is stopped."
        fi
    fi
    exit 1
;;

*)
    echo "usage: $0 (start|stop|restart|status)"

esac
