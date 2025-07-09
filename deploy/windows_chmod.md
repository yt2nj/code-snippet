# Windows `icacls` for `chmod` Users

On Linux and macOS, file permissions are managed with the `chmod` command. The equivalent on Windows is `icacls`, a powerful command-line tool for displaying and modifying Access Control Lists (ACLs).

This guide maps common `chmod` numeric modes to their `icacls` counterparts for easy reference.

## Permission Mapping: `chmod` vs. `icacls`

The following table shows how to replicate common `chmod` permissions using `icacls` in PowerShell.

| `chmod` Mode | Description                                         | `icacls` (Windows PowerShell) Command                                           |
| :----------- | :-------------------------------------------------- | :------------------------------------------------------------------------------ |
| `600`        | **User only**: Read.                                | `icacls "file" /inheritance:r /grant:r "$($env:USERNAME):R"`                    |
| `644`        | **User**: Read/Write. **Everyone**: Read.           | `icacls "file" /inheritance:r /grant "$($env:USERNAME):RW" /grant "Everyone:R"` |
| `700`        | **User only**: Full Control (Read/Write/Execute).   | `icacls "file" /inheritance:r /grant "$($env:USERNAME):F"`                      |
| `755`        | **User**: Full Control. **Everyone**: Read/Execute. | `icacls "file" /inheritance:r /grant "$($env:USERNAME):F" /grant "Everyone:RX"` |
| `777`        | **Everyone**: Full Control. (**Warning**: Insecure) | `icacls "file" /inheritance:r /grant "Everyone:F"`                              |

**Key `icacls` Parameters:**

*   `/inheritance:r`: **Removes** all inherited ACLs. Crucial for a clean permission slate.
*   `/grant <User>:<Perms>`: **Grants** permissions.
    *   `<User>` can be a username like `$env:USERNAME`, or a group like `Everyone`, `Authenticated Users`, or `SYSTEM`.
    *   `<Perms>` are permission codes:
        *   `F`: Full control
        *   `RW`: Read & Write
        *   `RX`: Read & Execute
        *   `R`: Read-only

## Examples

### Example 1: Secure a Private Key (`chmod 600`)

To protect a sensitive file like an SSH private key (`id_rsa`), you must ensure only your user account can read it.

```powershell
# Remove inheritance and grant current user Read-only access
icacls "D:\path\to\id_rsa" /inheritance:r /grant:r "$($env:USERNAME):R"
```

To verify the permissions, run `icacls "D:\path\to\id_rsa"`. The output should list only your user account with `(R)` permissions.

### Example 2: Set Executable Script Permissions (`chmod 755`)

To allow everyone to run a script while only you can modify it:

```powershell
# Grant yourself Full Control and Everyone else Read & Execute
icacls "C:\scripts\my_script.ps1" /inheritance:r /grant "$($env:USERNAME):F" /grant "Everyone:RX"
```

This ensures the script is secure and usable by others on the system.
