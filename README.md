# Vehicle JSON parser

A Python script to extract and transform specific attributes from electric vehicle datasets, with automatic unit conversion and attribute renaming.

## Overview

This script processes JSON datasets containing electric vehicle specifications and extracts a subset of relevant attributes. It automatically converts energy consumption from kWh/100 miles to kWh/100 km and renames attributes for better clarity.

## Data Source

The script is designed to work with electric vehicle data from:
- **Source**: https://public.opendatasoft.com/explore/dataset/all-vehicles-model/information/?flg=fr-fr&sort=modifiedon&refine.fueltype=Electricity
- **Format**: JSON array of vehicle objects
- **Content**: EPA vehicle certification data with technical specifications

## Features

- Extracts 13 specific attributes from vehicle data
- Converts energy consumption from Imperial (kWh/100 miles) to Metric (kWh/100 km)
- Renames attributes for improved clarity
- Handles missing values gracefully
- Provides data preview and file size statistics
- Interactive command-line interface

## Extracted Attributes

| Original Attribute | Output Attribute | Description |
|-------------------|------------------|-------------|
| `make` | `make` | Vehicle manufacturer |
| `model` | `model` | Complete model name |
| `basemodel` | `basemodel` | Base model name |
| `year` | `year` | Model year |
| `combe` | `cons_kwh_per_100km` | Energy consumption (converted to kWh/100km) |
| `range` | `range` | Vehicle range in miles |
| `charge240` | `time_charge240` | Standard 240V charge time (hours) |
| `charge240b` | `time_charge240b` | Fast 240V charge time (hours) |
| `c240dscr` | `c240dscr` | Standard charger description |
| `c240bdscr` | `c240bdscr` | Fast charger description |
| `tcharger` | `tcharger` | Turbo charger info |
| `scharger` | `scharger` | Super charger info |
| `modifiedon` | `modifiedon` | Last modification date |

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Usage

1. **Prepare your data file**:
    - Download the dataset from the source URL above
    - Save it as `vehicles_data_original.json` or use a custom filename

2. **Run the script**:
   ```bash
   python extract_vehicle_data.py
   ```

3. **Follow the prompts**:
    - Enter input filename (default: `vehicles_data_original.json`)
    - Enter output filename (default: `vehicles_data_extracted.json`)
    - Choose whether to preview the results

## Example Output

```json
[
  {
    "make": "Tesla",
    "model": "Model S AWD - P100D",
    "basemodel": "Model S",
    "year": "2017",
    "cons_kwh_per_100km": 21.75,
    "range": 315,
    "time_charge240": 12,
    "time_charge240b": 4.75,
    "c240dscr": "standard charger",
    "c240bdscr": "80 amp dual charger",
    "tcharger": null,
    "scharger": null,
    "modifiedon": "2022-02-02"
  }
]
```

## Unit Conversion

The script automatically converts energy consumption using the formula:
```
kWh/100km = kWh/100miles × (100 ÷ 160.9344)
```

Where 160.9344 km = 100 miles (1 mile = 1.609344 km)

## Error Handling

- Invalid JSON files are detected and reported
- Missing attributes are set to `null` in the output
- Conversion errors result in `null` values
- File I/O errors are caught and displayed

## License

This script is provided as-is for data processing purposes. Please respect the terms of use of the original data source.