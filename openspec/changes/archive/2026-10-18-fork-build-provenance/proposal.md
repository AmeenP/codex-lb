# Identify the fork build (P05)

## Why
Operators need to distinguish the installed fork from the upstream package and identify its patch stack.

## What Changes
Use the ameen.2 version suffix in Python package metadata, runtime version headers, and frontend build metadata. Record deployment validation and patch provenance.

## Impact
Version identification only. No routing or migration behavior changes.
