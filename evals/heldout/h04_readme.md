## Getting Started

Welcome to **lintwise**, a blazing-fast, lightweight, and highly configurable linter for YAML files! Whether you're managing Kubernetes manifests or CI pipelines, lintwise empowers you to catch errors before they reach production.

### Installation

lintwise requires Python 3.10 or later. Install it with pip:

```bash
pip install lintwise
```

### Usage

Simply point lintwise at a file or directory:

```bash
lintwise check ./config
```

By default, lintwise checks indentation, duplicate keys, and trailing whitespace. You can customize the rules by creating a `.lintwise.toml` file in your project root. It's important to note that lintwise exits with code 1 if any errors are found, making it seamless to integrate into your CI workflow.
