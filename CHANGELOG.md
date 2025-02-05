# Changelog

## [1.1.0] - 2024-01-20

### Added
- Comprehensive genomic file parsing system
- Support for multiple file formats:
  * BAM (Binary Alignment Map)
  * CRAM (Compressed Reference-oriented Alignment Map)
  * SFF (Standard Flowgram Format)
  * CSFASTA (Color Space FASTA)
- Quality metrics analysis with:
  * Coverage depth calculation
  * GC content analysis
  * Read length statistics
  * Phred score analysis
- File format registry for extensible parser support
- Caching system for improved performance
- Full test coverage for all parsers and handlers

### Changed
- Improved error handling in file parsers
- Enhanced documentation with usage examples
- Standardized parser interfaces
- Unified quality filtering system

### Fixed
- CRAM parser reference genome handling
- Quality metrics calculation for empty files
- File caching mechanism reliability
- Parser validation edge cases

### Documentation
- Added comprehensive module documentation
- Created technical documentation for parsers
- Added user guide with examples
- Updated inline documentation

### Dependencies
- pysam>=0.21.0
- numpy>=1.26.0
- biopython>=1.81

### Development
- Added comprehensive test suite
- Improved code coverage to 83%
- Added type hints throughout the codebase 