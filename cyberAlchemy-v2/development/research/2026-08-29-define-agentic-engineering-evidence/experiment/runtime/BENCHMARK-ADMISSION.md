# Public Software-Agent Benchmark Admission

Status: `planned-after-L3`

This is the L3.5 step. It begins only after one repository-local L3 synthetic
task block validates. It does not select or execute a public benchmark task by
itself.

## Purpose

Public coding benchmarks can test whether Define's experiment mechanics travel
beyond this repository. They also create contamination, licensing, dependency,
and hidden-truth risks. Admission makes those risks explicit before selection.

## Candidate Record

Each candidate must record:

- benchmark name, version, task ID, and source URL;
- repository and exact base commit;
- issue-text digest and permitted local copy;
- hidden patch and hidden-test handling;
- allowed and forbidden paths;
- offline runtime identity and test command;
- license and redistribution limits;
- estimated time and resource budget;
- contamination risk and reason;
- low- or high-ambiguity classification.

## Admission Rule

A candidate is eligible only when it runs offline, needs no credentials or
external service, has bounded writes, keeps the reference patch and hidden
tests absent from agent views, and can use the same source/runtime across all
four conditions.

L3.5 produces a current research inventory and recommends one low-ambiguity and
one high-ambiguity task. The experiment owner selects explicitly. After
selection, each task must independently pass L2 isolation and L3 packet
compilation before any native agent session is considered.

Benchmark scores are supporting comparison evidence. They do not by themselves
prove that Define improves product outcomes, and public-task memorization
remains a named confounder.
