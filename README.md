# 4-Party Asynchronous Communication with Perfect Secrecy

This is a Multi-party one-time pad protocol for asynchronous broadcast, using a split-half d-gap design.

## Requirements
- Python 3.10+

No external dependencies. Standard library only.

## Quick Demo for Running the Protocol

```bash
python protocol.py
```

## Running the Testing program

```bash
python testing.py
```

With custom parameters you can choose:
```bash
python testing.py -n 2000 -d 20 -e 200 --seed 188
```

Options:
- -n : Pad sequence length (default: 1000)
- -d : Gap size (default: 10)
- -e , --executions : Number of protocol runs per scenario (default: 100)
- --seed : Random seed (default: 42)

Scenarios:
- **S.1**: 1 random party sends
- **S.2**: 2 random parties send
- **S.4**: All 4 parties send

Each protocol run until at least one party cannot send. Output includes average wasted pads, max and min wasted pads etc.
