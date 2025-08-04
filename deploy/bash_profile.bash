# if [ -f $HOME/.bashrc ]; then source $HOME/.bashrc; fi;

# git config --global pull.rebase true

# git config --global user.email firstlast@.com
# git config --global user.name 'First Last'
# git config --global --get user.email
# git config --global --get user.name

export LANG='C.UTF-8'
PS1='$\[\033]0;$TITLEPREFIX:$PWD\007\]\n\[\033[32m\]\u@\h \[\033[35m\]$MSYSTEM \[\033[33m\]\w\[\033[36m\]`__git_ps1`\[\033[0m\]\n$'
PS1='\D{%H:%M:%S} \u@\h:\W\$ '
PS1='\[\e[35;1m\]\D{%H:%M:%S}\[\e[0m\] \[\e[32;1m\]\u\[\e[0m\]@\[\e[34;1m\]\h\[\e[0m\]:\[\e[33;1m\]\W\[\e[0m\] \[\e[31;1m\]\$\[\e[0m\] '

alias gl="git log --graph --abbrev-commit --date=relative --pretty=format:'%C(bold red)%h%Creset - %s %C(bold green)(%cr)%Creset %C(bold blue)<\"%an\", %ae>%Creset%C(bold magenta)%d%Creset'"
