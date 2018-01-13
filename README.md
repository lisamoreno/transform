# transform

Transforms a CSV dataset by applying operations listed in a JSON-based data transformation specification
and returns them in a new file, `transformed_data.csv`.

## Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Arguments](#arguments)
- [Available Operations](available-operations)
- [Transformation Specification](#transformation-specification)
- [Dataset File](#dataset-file)
- [Testing](#testing)

## Installation

- Clone this repo:
  - `git clone https://github.com/lisamoreno/transform.git`
- Install dependencies:
  - `pip install --user -r requirements.txt`

## Usage

`./transform --transformspec /path/to/transform-spec.json --dataset /path/to/dataset.csv`

### Arguments

Two arguments are required:
1. `--transformspec` takes a full path to your [JSON-based data transformation spec](#transformation-specification)
2. `--dataset` takes a full path to your [dataset file](#dataset-file).

## Available Operations

The following operations have been implemented and can be specified in your [transformation specification](#transformation-specification).

- `slugify`, operates on strings: Removes all punctuation, converts all whitespace into hyphens, and lowercases all letters
- `f-to-c`, operates on floats or integers: Returns the temperature converted to Celsius, rounded to 1 decimal place.
- `hst-to-unix`, operates on date and time strings: Assumes the source date and times are in Hawaii Standard Time (UTC-10). Converts into the UTC time zone and into a UNIX timestamp format. If this operation is included, one column must include a date as `MM/DD/YY` and another column must include the time as `HH:MM:SS`. A new column for the timestamp will be added.

## Transformation Specification

- The spec must be valid JSON in the following format:
```javascript
{
	"spec_version": 1.0,
	"transforms": [
		{
			"operation": "OPERATION", # Include a [valid operation](#available-operations)
			"column": "COLUMN_NAME" # The `operation` specified will be applied to all values in `column`
		},
		{ ... },
		{ ... }
	]
}

```
- **Note:** If an `operation` is specified more than once for the same column, the latest one will be applied.

## Dataset File

- This script was made specifically to work with [solar radiation measures from the Sun](https://docs.google.com/spreadsheets/d/1M_G3N_RhYwWJT4Dxpm160X7-BO39JETXTJ5aRlP8YkI/edit#gid=605241074), as captured by NASA from various locations around the Earth.
- It can be used with other datasets.

## Testing
