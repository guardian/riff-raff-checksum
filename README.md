## Riff-Raff Checksum Calculator

This project is designed to assist teams with the migration from TeamCity to
GitHub Actions for CI. It takes an input of a Riff-Raff project name, and two
build numbers, and then tells you whether or not the two builds are identical.
This is so teams can verify the integrity and completeness of their builds
during migration.


You should not use this action after migration is complete, as it will fail if
the builds are not identical (ie if the code has changed).

### Running locally

You can run this script with riff-raff read-only credentials by:
- grabbing the credentials from Janus, setting the correct profile
- installing the dependencies with `pip install -r requirements.txt`
- running `python3 compare.py <stack>::<app> <build1> <build2>`.

### Running as an Action

Prerequisites: This action requires the use of the `aws-actions/configure-aws-credentials`
action, using `GU_RIFF_RAFF_CHECKSUM_ROLE_ARN`.

When running in CI, the first build number is the most recent build TeamCity
performed on the main branch. The second build number is the build number of
the current CI run. This action should run as part of the CI action, **after**
actions-riff-raff has completed.