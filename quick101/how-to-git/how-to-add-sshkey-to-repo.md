# Steps tp  **generate an SSH keypair** (private + public)

# 1) Create a new keypair

**macOS / Linux / WSL**

```bash
# recommended:
ssh-keygen -t ed25519 -C "you@example.com" -f ~/.ssh/id_ed25519

# if you need RSA (legacy servers):
ssh-keygen -t rsa -b 4096 -C "you@example.com" -f ~/.ssh/id_rsa
```

You’ll be asked for a passphrase (strongly recommended). The `-f` sets the filename; omit it to accept the default.

**Windows (PowerShell)**

```powershell
ssh-keygen -t ed25519 -C "you@example.com" -f $env:USERPROFILE\.ssh\id_ed25519
# or RSA:
ssh-keygen -t rsa -b 4096 -C "you@example.com" -f $env:USERPROFILE\.ssh\id_rsa
```

# 2) Where the files are saved

Default locations:

* Private key: `~/.ssh/id_ed25519`  (DON'T share this)
* Public key:  `~/.ssh/id_ed25519.pub` (this is what you give to servers/GitHub)

# 3) View / copy the public key (safe to share)

**macOS**

```bash
cat ~/.ssh/id_ed25519.pub        # show it
pbcopy < ~/.ssh/id_ed25519.pub  # copy to clipboard
```

**Linux**

```bash
cat ~/.ssh/id_ed25519.pub
# copy to clipboard (depends on distro)
# e.g. with xclip:
xclip -selection clipboard < ~/.ssh/id_ed25519.pub
# or with wl-copy on Wayland:
wl-copy < ~/.ssh/id_ed25519.pub
```

**Windows PowerShell**

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | clip
```

# 4) If you only have the private key and need the public

```bash
ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub
```

This reads the private key and writes the corresponding public key.

# 5) Add key to ssh-agent (so you don’t type passphrase every time)

**macOS / Linux**

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**Windows PowerShell**

```powershell
# Start the agent (if needed)
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

# 6) Permissions (important!)

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

Wrong permissions may make SSH refuse the key.

# 7) Test the key (example: GitHub)

* Add the contents of `id_ed25519.pub` to GitHub/GitLab/your server’s “authorized keys”.
* Test:

```bash
ssh -T git@github.com
# or to test a server:
ssh user@server.example.com
```

# 8) Helpful quick commands

* List keys loaded in agent: `ssh-add -l`
* Show fingerprint of public key: `ssh-keygen -lf ~/.ssh/id_ed25519.pub`
* Generate with a custom name: `-f ~/.ssh/my_special_key`

# 9) Security reminders

* **Never** share your private key (`id_ed25519`). Treat it like a password.
* Use a passphrase on private keys.
* Keep backups in an encrypted location.
* Revoke/replace keys if a machine is lost/compromised.
