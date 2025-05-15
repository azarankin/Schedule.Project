#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIDGET_PATH="$DIR/schedule_widget.py"
CONFIG_FILE="$DIR/conky.conf"
export LANG=he_IL.UTF-8
export LC_ALL=he_IL.UTF-8
sleep 10
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ config file not found: $CONFIG_FILE"
    exit 1
fi
sed -i "s|python3 .*schedule_widget\.py|python3 $WIDGET_PATH|" "$CONFIG_FILE"
pkill -x conky
sleep 1
conky -c "$DIR/conky.conf" &