#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// For Python GUI scripts, use "start /b pythonw.exe script.py".

const char * prefix = "git log -n 8 --graph --abbrev-commit --date=relative "
                      "--pretty=format:\"%C(bold red)%h%Creset - %s %C(bold green)(%cr)%Creset %C(bold blue)<\"%an\", %ae>%Creset%C(bold magenta)%d%Creset\" ";

int main(int argc, char * argv[])
{

    size_t total_length = strlen(prefix) + 1;

    for (int i = 1; i < argc; i++) {
        total_length += strlen(argv[i]) + 1;
    }

    char * command = (char * ) malloc(total_length * sizeof(char));

    if (command == NULL) {
        perror("Memory allocation failed");
        return EXIT_FAILURE;
    }

    strcpy(command, prefix);

    size_t current_index = strlen(prefix);

    for (int i = 1; i < argc; i++) {

        strcpy(command + current_index, argv[i]);
        current_index += strlen(argv[i]);

        command[current_index] = (i < (argc - 1)) ? ' ' : '\0';
        current_index++;

    }

    int status = system(command);

    free(command);

    return status;
}
