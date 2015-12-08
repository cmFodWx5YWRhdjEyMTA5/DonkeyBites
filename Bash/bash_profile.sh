# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

export PATH

# User specific aliases and functions

alias ll='ls -lahG'
alias dss = 'du -skh * | sort -nr'
alias dssg = 'du -skh * | sort -nr | grep G'

export PS1="\[\033]0;$MSYSTEM:${PWD//[^[:ascii:]]/?}\007\]\n\[\033[32m\]\u@\h \[\033[33m\]\w$(__git_ps33)\[\033[0m\]\n$ "
source /etc/bash_completion.d/git

export http_proxy=http://proxy:8080
export https_proxy=http://proxy:8080
export ftp_proxy=$http_proxy
export JAVA_HOME=/usr/java/jdk1.7.0_65
export M2_HOME=/opt/apache-maven-3.0.5
export M2=$M2_HOME/bin
export PATH=$JAVA_HOME/bin:$M2:$PATH


alias ll='ls -lahG'
__git_ps33 () 
{ 
 local b="$(git symbolic-ref HEAD 2>/dev/null)";
    if [ -n "$b" ]; then
        printf " (%s)" "${b##refs/heads/}";
    else
        printf "";
    fi
}

