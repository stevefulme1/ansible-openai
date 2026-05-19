# Changelog

## [2.1.2] - 2026-05-18

## [2.2.0] - 2026-05-19

### Added
- Added 41 _info modules for comprehensive query coverage
- Total module count: 143

### Security
- Add `secret: true` to inventory plugin api_key option

## [2.0.0] - 2026-05-17

## [2.2.0] - 2026-05-19

### Added
- Added 41 _info modules for comprehensive query coverage
- Total module count: 143

### Added
- Pagination support (limit/offset) for all _info modules
- 3 operational roles for OpenAI API management
- Usage, rate_limit, and audit_log info modules
- Comprehensive README with module index, EDA, and examples
- Comprehensive unit and integration test suites
- Pre-commit and linting configuration (ruff, ansible-lint)

### Fixed
- Missing offset param added to DOCUMENTATION and limit defaults fixed
- Boilerplate, namespace, meta, lint config added
- Role README files added for Galaxy compliance
- doc-default-does-not-match-spec and no-log-needed sanity issues resolved
- CI failures resolved across Python 3.11-3.13

### Changed
- Auto-formatted all modules with ruff
- Excluded roles from ansible-lint syntax-check

## [1.0.0] - 2026-05-15

## [2.2.0] - 2026-05-19

### Added
- Added 41 _info modules for comprehensive query coverage
- Total module count: 143

### Added
- 103 modules covering full OpenAI platform API (models, fine-tuning, assistants, moderation, governance, MCP)
- CRUD + info module for every resource type
- EDA source plugins for event-driven automation
- Unit tests and CI pipeline
