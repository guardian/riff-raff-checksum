## Riff-Raff Checksum Calculator

This project is designed to assist teams with the migration from TeamCity to
GitHub Actions for CI. It takes an input of a Riff-Raff project name, and two
build numbers, and then tells you whether or not the two builds are identical.
This is so teams can verify the integrity and completeness of their builds
during migration.

When running in CI, the first build number is the most recent build TeamCity
performed on the main branch. The second build number is the build number of
the current CI run. This action should run as part of the CI action, **after**
actions-riff-raff has completed.

You should not use this action after migration is complete, as it will fail if
the builds are not identical (ie if the code has changed).