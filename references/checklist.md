# Review Checklist

Quick reference for the four review categories.

## Correctness
- [ ] Does the logic match the stated intent?
- [ ] Are loop bounds and indices correct?
- [ ] Are edge cases (empty, null, zero, large) handled?
- [ ] Are error paths handled, not just the happy path?

## Security
- [ ] No user input flows into SQL/OS/shell commands unescaped
- [ ] No hardcoded secrets, tokens, or keys
- [ ] No unsafe deserialization (pickle, yaml.load, eval)
- [ ] Paths are validated before file access

## Performance
- [ ] No unnecessary work inside loops
- [ ] No accidental N+1 queries or repeated I/O
- [ ] Collections chosen appropriately (list vs set vs dict)

## Style & Clarity
- [ ] Names describe intent
- [ ] No dead or commented-out code
- [ ] Functions are small and single-purpose
- [ ] Complex logic is explained with a comment
