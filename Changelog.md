
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2023-02-08

### Added

- Add Report to Sview.

### Update

- return more descriptive response on bad http method on API endpoint.

## [1.2.0] - 2022-09-27

### Update

- API documentation update

## [1.1.3] - 2022-07-27

### Fixed

- Fix the UI implemeting changing select to 5 minute offset for recent data. (Bug)

## [1.1.2] - 2022-05-23

# Fixed

- Handle unknown IP address (Hanging application bug)

## [1.1.1] - 2022-04-13

### Added

- Add endpoint to link from router to my device page.

## [1.1.0] - 2022-04-14

### Added

- Integrate Vizapp (Dynamic DynFW visualization)

## [1.0.0] - 2022-03-10

### Added

- feature: Add Matomo tracking code.
- README: Extend section about statistics
- statistics: Add queue priority
- cli: Add cache-period,view-timeouts,clear-timeouts
- cli: Add aggregate-period command
- cli: Add migration helper command
- Add aggregation tasks
- Add aggregation queries
- Add column "raw_count" to the schema
- SQL: Prepare for filling the gaps with zeros

## Fixed

- Increase rq job timeout
- change default period to one week (bug)
- Decrease user cache ttl for short periods
- statistics: Fix view-jobs command
- statistics: Increase resource cache TTL
- statistics: Increase Job TTL to 60 minutes
- Wait few minutes before each quarterly aggregation
- statistics: Fix refresh timeout for user resources
- statistics: Improve params handling in redis keys

## Updated

- statistics: Unify cli interface
- dev: Remove obsolete dev script
- statistics: Improve blueprint structure
- Merge statistics and api blueprints
- cli: Use aggregation in commands
- Use different tables for different periods
- SQL: Prepare scheme for aggregation
- Introduce Resource class
- Simplify job status handling by adding JobState
- Mark graph points with bucket (window) ending time
- Display data times in UTC (instead of DB timezone)
- dev: Reflect "raw_count" column in testdata

## [0.5.1] - 2021-11-16

### Added

- Add dry run for queue-queries & monitoring outputs
- cli: Add command for jobs monitoring
- Keep period when using breadcrumbs

### Changed

- Keep period for statically loaded devices
- Keep period when adding/removing device tokens

### Fixed

- Fix label for statically loaded map
- Fix multiline graphs in My devices & static load
- Fix main navigation links for views without params
- sql: Fix typo

## [0.5.0] - 2021-10-22

### Fixed

- HTML: Fix device token passing in remove call
- Fix missing limit for top passwords usernames
- Fix multiple calls for one job
- Fix SQAlchemy compatibility issue
- Fix misleading time aggregation window name

### Changed

- cli: Update queue-queries command
- Allow resource refresh before cache expiration
- rlimit: Use as a function instead of decorator
- Use precise intervals in SQL queries
- Keep period param in navigation links updated
- JS: Make password and address links period aware
- Use selected period in statically loaded links
- Replace : with ; as an separator for Redis keys
- Swap DB query with log about it
- HTML: Improve data box titles
- style: Rename query names canonically
- Rename to "Sentinel View"
- README: Replace InfluxDB by TimescaleDB
- Improve SQLAlchemy exception handling
- sql: Convert ports & passwords queries to SQL
- git/help: Move query files for a better diff
- sql: Convert incident queries from FLUX to SQL
- git/help: Merge incidents queries to single file
- Replace influx by sqalchemy

### Added

- cli: Add clear-redis command
- dev: Add timescale test data
- sql: Add timescale scheme

## [0.4.0] - 2021-10-12

### Added

- Add Influx DB
- Add statistics
- Add UI content

## [0.3.2] - 2020-10-20

### Fixed

- fixed version of SQLAlchemy
- setup: gitlab domain in URL

## [0.3.1] - 2020-20-01

### Fixed

- If condition in `_macros`

## [0.3.0] - 2020-20-01

### Added

- Greylist placeholder
- Optional target parameter for nav_link

## [0.2.0] - 2019-19-12

### Added

- Dark mode support

## [0.1.0] - 2019-25-10

### Added

 - Proof of concept
