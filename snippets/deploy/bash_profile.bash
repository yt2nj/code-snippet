# if [ -f $HOME/.bashrc ]; then source $HOME/.bashrc; fi;

# git config --global pull.rebase true

export LANG='C.UTF-8'
PS1='\[\e[35;1m\]\D{%H:%M:%S}\[\e[0m\] \[\e[32;1m\]\u\[\e[0m\]@\[\e[34;1m\]\h\[\e[0m\]:\[\e[33;1m\]\W\[\e[0m\] \[\e[31;1m\]\$\[\e[0m\] '

alias gl="git log --graph --abbrev-commit --date=relative --pretty=format:'%C(bold red)%h%Creset - %s %C(bold green)(%cr)%Creset %C(bold blue)<\"%an\", %ae>%Creset%C(bold magenta)%d%Creset'"
