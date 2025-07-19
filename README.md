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
  - repo: https://github.com/DrizzleAI/pre-commit-sops
    rev: v1.1
    hooks:
      - id: sops-encryption
        # Define the file patterns to check with the hook
        files: .*secret.*  # Example: change it to fit your file pattern to ensure sops encryption
```

You can customize the `files:` pattern to match the files you want checked for SOPS encryption.

## Usage

This hook will check that files matching your pattern are encrypted with SOPS before allowing commits. If a file is not properly encrypted, the commit will be blocked.

## License

Apache 2.0
