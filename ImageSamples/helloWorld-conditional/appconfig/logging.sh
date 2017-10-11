#!/bin/env bash
################################################################################
# Copyright (c) 2015, BlueData Software, Inc.                                  #
#                                                                              #
# Logging facilities for a catalog configuration bundle                        #
################################################################################

set -o pipefail
[[ -z ${LOG_FILE_PATH} ]] && export LOG_FILE_PATH="/var/log/bluedata/configpackage-$(date +%Y%m%d%H%M%S).log"

# Some global logging functions
log() {
    echo "$@" | tee -a ${LOG_FILE_PATH}
}

log_file() {
    echo "$@" 2>&1 &>>$LOG_FILE_PATH
}

log_exec_no_exit() {
    [ "$VERBOSE" == 'true' ] && log "EXECUTING: $@"
    eval "$@" 2>&1 | tee -a $LOG_FILE_PATH
}

# To run the command as root
log_sudo_exec_no_exit() {
    [ "$VERBOSE" == 'true' ] && log "EXECUTING: $@ as sudo"
    eval "sudo -nE -- /bin/bash -c \"$@\"" 2>&1 | tee -a $LOG_FILE_PATH
}

# To run a command as a different user
log_su_exec_no_exit() {
    User=$1
    shift
    Command=$@
    [ "$VERBOSE" == 'true' ] && log "EXECUTING: $Command"
    eval 'sudo -nE su - -m $User -c "$Command"' 2>&1 | tee -a $LOG_FILE_PATH
}


# To run a command with the current user in a different group
log_sg_exec_no_exit() {
    Group=$1
    shift
    Command=$@
    [ "$VERBOSE" == 'true' ] && log "EXECUTING: $Command"
    eval 'getent group $Group | grep -qw $USER && sg $Group -c "$Command"' 2>&1 | tee -a $LOG_FILE_PATH
}

# Writes the messages to both STDOUT and the log file.
log_exec() {
    log_exec_no_exit $@
    if [ $? -ne 0 ]; then
        log "Failed to exec: $@"
        exit 120
    fi
}

log_sudo_exec() {
    log_sudo_exec_no_exit $@
    if [ $? -ne 0 ]; then
        log "Failed to exec: $@"
        exit 120
    fi
}

log_su_exec() {
    User=$1
    shift
    Command=$@
    log_su_exec_no_exit $User $Command
    if [ $? -ne 0 ]; then
        log "Failed to exec: $@"
        exit 120
    fi
}

log_sg_exec() {
    Group=$1
    shift
    Command=$@
    log_sg_exec_no_exit $Group $Command
    if [ $? -ne 0 ]; then
        log "Failed to exec: $@"
        exit 120
    fi
}

log_exec_no_error() {
    log_exec_no_exit $@ || true
}

log_sudo_exec_no_error() {
    log_sudo_exec_no_exit $@ || true
}

log_sg_exec_no_error() {
    Group=$1
    shift
    Command=$@
    log_sg_exec_no_exit $Group $Command || true
}

log_su_exec_no_error() {
    User=$1
    shift
    Command=$@
    log_su_exec_no_exit $User $Command || true
}

# Log are only written to the file without echoing to the console.
log_file_exec() {
    log_exec_no_exit "$@" > /dev/null
}

log_sudo_file_exec() {
    log_sudo_exec "$@" > /dev/null
}

log_sudo_file_exec_no_error() {
    log_sudo_exec_no_exit "$@" > /dev/null
}

log_su_file_exec() {
    User=$1
    shift
    Command=$@
    log_su_exec_no_exit $User $Command > /dev/null
}

log_nonewline() {
    echo -n "$@" | tee -a ${LOG_FILE_PATH}
}

log_verbose() {
   [ "$VERBOSE" == "true" ] && log "$@" || true
}

log_verbose_nonewline() {
    [ "$VERSION" == 'false' ] && return

    echo -n "$@" | tee -a ${LOG_FILE_PATH}
}

log_error() {
    log "ERROR: $@"
}

log_warn() {
    log "WARNING: $@"
}

NOT_IMPLEMENTED() {
    log "NOT_IMPLEMENTED: $@"
}
