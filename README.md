# pre-commit-sops

Pre-commit hook to ensure that secret files are encrypted with SOPS.

## Repository

https://github.com/DrizzleAI/pre-commit-sops

## Author

Aymen Segni, Drizzle:AI Team  
contact@drizzle.systems

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:  
- repo: https://github.com/DrizzleAI/pre-commit-sops
  rev: v1.2
  hooks:
  - id: sops-encryption
    # Define the file patterns to check with the hook
    files: .*drizzle-ai.yaml*  # Example: change it to fit your file pattern to ensure sops encryption
    pattern: secret # Optional, pattern in the checked file to include in the test
```

You can customize the `files:` pattern to match the files you want checked for SOPS encryption.

## Usage

This hook will check that files matching your pattern are encrypted with SOPS before allowing commits. If a file is not properly encrypted, the commit will be blocked.

## Installation

You can checke manually if your selected file(s) are encrypted by running the following commands:

1. Install the pre-commit
```bash
pre-commit install
```

2. Run the pre-commit check
Execute this command to run pre-commit on all files in the repository (not only changed files):

```bash
pre-commit run -a 
```

3. Example of teh output:

```bash
[INFO] Initializing environment for https://github.com/DrizzleAI/pre-commit-sops.
[INFO] Installing environment for https://github.com/DrizzleAI/pre-commit-sops.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
Ensure secrets are encrypted with sops...................................Failed
- hook id: sops-encryption
- exit code: 1

drizzle-ai.yaml: sops metadata key not found in file, is not properly encrypted
```


## License

Apache 2.0
