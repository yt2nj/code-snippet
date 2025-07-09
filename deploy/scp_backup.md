# How to Create a Secure, SFTP-Only User on Linux

This guide details how to create a restricted user account on a Linux server that can only be used for file transfers via SFTP with SSH key authentication. This is ideal for secure, automated backups or for allowing a third party to upload files to a specific directory without granting them shell access.

The process is divided into two parts: generating keys on your **client machine** and configuring the user on the **server**.

---

## Part 1: On Your Client Machine - Generate SSH Keys

Before configuring the server, you need an SSH key pair on your local (client) machine. The public key will be used to grant access, while the private key will be used to authenticate.

### 1. Generate a New SSH Key Pair

If you don't already have an SSH key, generate a new one. Open a terminal on your **local machine** and run:

```bash
# -t specifies the type of key to create (ed25519 is modern and secure)
# -f specifies the filename for the key
ssh-keygen -t ed25519 -f ~/.ssh/backup_user_key
```

When prompted, you can optionally enter a passphrase to encrypt your private key. This adds an extra layer of security.

This command creates two files:
- `~/.ssh/backup_user_key`: Your **private key**. Keep this file secret and secure!
- `~/.ssh/backup_user_key.pub`: Your **public key**, which you can safely share.

### 2. Secure Your Private Key

Your SSH client will reject a private key that has permissions that are too open. To secure it, run:

```bash
chmod 600 ~/.ssh/backup_user_key
chmod 644 ~/.ssh/backup_user_key.pub
```

### 3. Copy Your Public Key

You will need the content of the public key to authorize it on the server. Display it in your terminal and copy it to your clipboard.

```bash
cat ~/.ssh/backup_user_key.pub
```

---

## Part 2: On Your Server - Configure the Backup User

Now, connect to your server and perform the following steps.

### 1. Create a Backup User

First, create a new user. The `--disabled-password` flag ensures this user cannot log in with a password.

```bash
sudo adduser --disabled-password backup_user
```

### 2. Create and Secure the `.ssh` Directory

Create the `.ssh` directory in the new user's home and set the correct ownership and permissions.

```bash
sudo mkdir -p /home/backup_user/.ssh
sudo chmod 700 /home/backup_user/.ssh
sudo chown backup_user:backup_user /home/backup_user/.ssh
```

### 3. Add the Client's Public Key

Create the `authorized_keys` file and paste the public key you copied from your client machine into it.

```bash
sudo vi /home/backup_user/.ssh/authorized_keys
# Paste the public key (from `backup_user_key.pub`), then save and exit.
```

### 4. Set Permissions for `authorized_keys`

Ensure the `authorized_keys` file has the correct permissions and ownership:

```bash
sudo chmod 600 /home/backup_user/.ssh/authorized_keys
sudo chown backup_user:backup_user /home/backup_user/.ssh/authorized_keys
```

### 5. Create a Directory for File Transfers

This is the directory where the `backup_user` will be able to read and write files.

```bash
sudo mkdir -p /home/backup_user/uploads
sudo chown backup_user:backup_user /home/backup_user/uploads
sudo chmod 777 /home/backup_user/uploads
```
> `777` allows the owner/group/others to read/write/execute, 7 = 4 + 2 + 1 = read + write + execute (rwx).

> A user can visit `/a/b/c/file` if and only if it can visit all its ancestors `/`, `/a/`, `/a/b/`, `/a/b/c/`. You may also need `sudo chmod o+x /home/backup_user`. For a directory, the execution permission means the ability to enter and traverse the directory, which does not mean the ability t read the contents of the files in the directory.

### 6. Restrict the User to SFTP-Only Access

Edit the SSH daemon configuration file (`/etc/ssh/sshd_config`) to limit what this user can do.

```bash
sudo vi /etc/ssh/sshd_config
```

Add the following block at the **end of the file**:

```ini
Match User backup_user
    # Force the user to only use the SFTP protocol and set their landing directory.
    ForceCommand internal-sftp -d /uploads
    
    # Disable port forwarding, TTY allocation, and X11 forwarding.
    AllowTCPForwarding no
    PermitTTY no
    X11Forwarding no
    
    # Enforce public key authentication for this user.
    PasswordAuthentication no
    PubkeyAuthentication yes
```

> `ForceCommand` does not create a `chroot` jail. However, `ChrootDirectory` must be **owned by root** (`root:root`) and **not writable by group/others** (`chmod 755`).

### 7. Reload SSH Service

Apply the changes by reloading the SSH daemon.

```bash
sudo systemctl reload sshd
```

---

## Part 3: Verification

### 1. Check Server Permissions

The permissions for the `backup_user`'s home and `.ssh` directories should look like this. Note that **only the public key** is present in `authorized_keys`; the private key is not on the server.

```bash
# ls -ld /home/backup_user /home/backup_user/.ssh /home/backup_user/uploads
drwxr-xr-x 4 backup_user backup_user 4096 Dec  3 10:00 /home/backup_user
drwx------ 2 backup_user backup_user 4096 Dec  3 10:05 /home/backup_user/.ssh
drwxr-xr-x 2 backup_user backup_user 4096 Dec  3 10:10 /home/backup_user/uploads

# ls -l /home/backup_user/.ssh
total 4
-rw------- 1 backup_user backup_user 402 Dec  3 10:05 authorized_keys
```

### 2. Test the SFTP Connection

From your **client machine**, try to connect to the server using the `backup_user` and your private key. You should be logged in directly to the `/uploads` directory and be unable to execute any shell commands.

```bash
# Replace server_ip with your server's IP address
sftp -i ~/.ssh/backup_user_key backup_user@server_ip
```

If successful, you will see an SFTP prompt: `sftp>`. You can now use commands like `put`, `get`, and `ls`.

---

**Do not copy `id_rsa` for security! If you insist doing that, you should know that `id_rsa` ends with a newline.**


