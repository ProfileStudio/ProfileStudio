# Tasks

## 1. Fixtures

- [ ] 1.1 Record anonymized REST and GraphQL responses for two sample profiles (small and large)
- [ ] 1.2 Add a fixture loader that replaces `rest`, `graphql` and `commit_count` in tests

## 2. Tests

- [ ] 2.1 Snapshot tests: one profile per theme, light and dark CSS present, stable output
- [ ] 2.2 Layout checks: text width estimates stay inside each card for long names and labels
- [ ] 2.3 Config tests: invalid `profile.json` values exit with a clear message

## 3. CI

- [ ] 3.1 Workflow running the suite on Python 3.9 and the latest Python on pull requests
- [ ] 3.2 Document how to run and update snapshots in CONTRIBUTING notes
