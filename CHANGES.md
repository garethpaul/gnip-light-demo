# Changes

## 2026-06-08

- Added `make check` for static legacy GNIP demo verification.
- Replaced dynamic `exec` link parsing with `ast.literal_eval`.
- Switched editable git dependencies from `git://` to HTTPS transport.
- Fixed `Timeframe.days` after inverted date fallback and covered it with a unit test.
- Documented required GNIP credential environment variables and ignored local exports.
