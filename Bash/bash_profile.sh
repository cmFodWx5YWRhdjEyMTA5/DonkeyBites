# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

export PATH



# .bashrc

# User specific aliases and functions

alias ll='ls -lahG'

export PS1='\[\e[1;31m\][\u@\h \W]\$\[\e[0m\] '
export http_proxy=http://proxy:8080
export https_proxy=http://proxy:8080
export https_proxy=$http_proxy
export ftp_proxy=$http_proxy
export JAVA_HOME=/usr/java/jdk1.7.0_65
export M2_HOME=/opt/apache-maven-3.0.5
export M2=$M2_HOME/bin
export PATH=$JAVA_HOME/bin:$M2:$PATH
export DISPLAY=:11.0

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi