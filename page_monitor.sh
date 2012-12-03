#!/bin/bash

# somehing quick and dirty
# usage: page_monitor.sh http://www.example.com/page/to/watch text-to-grep myself@example.com

while true; do
  if [[ -f /tmp/new_page.html ]]; then
    mv /tmp/new_page.html /tmp/old_page.html
  fi
  clear
  date
  curl -s -S $1 |egrep -i $2 |tee /tmp/new_page.html
  diff /tmp/new_page.html /tmp/old_page.html > /dev/null
  if [[ $? -ne 0 ]]; then
    printf "From: automated <kkaji@Splinter.local>\nTo: %s\n\nPage changed: %s\n" $3 $1 |/usr/sbin/sendmail -F "automated" -f "kkaji@Splinter.local" $3

    # exit 1

    # while true; do afplay alarm_gen.mp3; sleep 1; done;    
  fi

  sleep 60
done
