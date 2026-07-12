# Test Files for SubVoid+

This directory contains specialized test files designed to validate the filtering and block-level parsing logic of the <a href="https://codeberg.org/pwshAgyjkcrg761/SubVoid-plus" target="_blank">SubVoid+</a> script.

## Purpose
These files are intended for development and verification use only. They contain dummy subtitle entries embedded with common advertisement URLs, recruitment phrases, and cryptographic spam patterns. Use them to verify that the script correctly:
*   Identifies and purges entire **SRT** blocks when a trigger is detected.
*   Surgically cleans **ASS/SSA** dialogue payloads without corrupting formatting tags.
*   Correctly handles custom user Find/Replace strings.

## License
The contents of the `test files` directory in this repository are licensed under the <a href="LICENSE" target="_blank">Creative Commons Attribution 4.0 International License</a>.

## How to use
1. Copy the `test files` directory to a safe testing location.
2. Launch <a href="https://codeberg.org/pwshAgyjkcrg761/SubVoid-plus" target="_blank">SubVoid+</a> and select this directory.
3. Enable the automated filters in `Tools > Filters`.
4. Run the process and review the output in the generated `_updated-SubVoid+` folder to ensure the triggers were successfully neutralized.

*Note: These files do not contain actual media content or legitimate subtitle dialogue; they are structured purely to trigger script logic.*