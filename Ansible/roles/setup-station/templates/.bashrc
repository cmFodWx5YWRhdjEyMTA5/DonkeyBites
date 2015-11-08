# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
      . /etc/bashrc
fi

if [ -f ~/.git-completion.bash ]; then
      . ~/.git-completion.bash
fi

# Use a long listing format ##
alias ll='ls -la --color=auto'

# Prompt will be changed only for interactive sessions 
if [[ $- == *i* ]]
 then
    export PS1="\[\033[38;5;6m\][\[$(tput sgr0)\]\[\033[38;5;14m\]\w\[$(tput sgr0)\]\[\033[38;5;6m\]]\[$(tput sgr0)\]\[\033[38;5;15m\] (\$(git branch 2>/dev/null | grep '^*' | colrm 1 2))\n\[$(tput sgr0)\]\[\033[38;5;11m\]\u\[$(tput sgr0)\]\[\033[38;5;15m\]@\h: \[$(tput sgr0)\]"
fi


# User specific aliases and functions

