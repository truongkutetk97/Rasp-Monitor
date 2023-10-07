CPU_USAGE="$(uname -a | awk '{print $1, $2, $3, $13}' | tr ' ' '_') $(date "+%Y-%m-%d %H:%M:%S") CPU: $(top -b -n 1 | awk '/Cpu\(s\)/ {print 100 - $8"%"}') Temp:$(vcgencmd measure_temp | awk -F"=" '{print $2}') Up: $(uptime | awk '{print $3}' | sed 's/,//g')"

echo $CPU_NAME $CPU_USAGE $CPU_TEMP $CPU_UP
