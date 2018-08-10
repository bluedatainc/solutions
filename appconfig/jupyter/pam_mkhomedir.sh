#!/usr/bin/env bash
if [ -f /usr/sbin/mkhomedir_helper ]; then
  /usr/sbin/mkhomedir_helper $PAM_USER 0077
else
  if [ -f /sbin/mkhomedir_helper ]; then
    /sbin/mkhomedir_helper $PAM_USER 0077
  fi
fi
exit 0
