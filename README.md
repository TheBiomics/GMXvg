
```diff
> Get older binaries for Ubuntu and Windows here -> [GMXvg v0.3](https://github.com/TheBiomics/GMXvg/releases/tag/v0.3) .
```

# GMXvg: Utility to Convert/Plot GROMACS XVG files (#xmgrace)

* Commandline based GROMACS XVG File plotting utility.
* Discovers all the XVG files in the current or subdirectories and converts them in specified file formats (default JPG).
* Logs the summary of plots in a file (CSV file) to quickly access the plot values along with their standard deviation values.
* This tool may be an alternative to `xmgrace`.

## Quick Demo on Youtube

[Watch Demo](https://www.youtube.com/watch?v=99Eeqjp_0kI)

[![Watch Demo](https://img.youtube.com/vi/99Eeqjp_0kI/0.jpg)](https://www.youtube.com/watch?v=99Eeqjp_0kI)


## Easy to install and use

Install using pypi or other directly from source using python's pip module:

* Install using: `pip install gmxvg`
* Check Version: `gmxvg --version`
* Usage:
  - Switch to the directory where XVG files are located `cd <xvg-file-directory`
  - Run `xvg`
  - See further instructions to modify title, legends, or other outputs

## Supported Platforms

The utility was developed and tested for Ubuntu and Windows. However, we expect it to work on all windows, linux, and iOS environments.

## Command Structure

* `gmxvg --<key>=<value>`: Double dash separated by equal sign
* `gmxvg -<key> <val1> <val2> <val3>` Single dash (single dash is not recommended) and multiple values

## Overriding default variables
Use `gmxvg -h` to see all options.

  * `path_base`: Base path if running from different directory
  * `csv_filename`: File name for CSV output else default will be used
  * `csv_filepath`: Path where CSV output file will be stored
  * `path_move`: Path where generated images will be moved (images will be deleted from the dir where XVG are stored)
  * `path_copy`: Path where generated images will be copied (source graphics will NOT be deleted)
  * `pattern_xvg`: Pattern to specify XVG images for conversion e.g., *--new.xvg, *-RMSD*.xvg (Helpful when you want to convert some selected files)
  * `merge_patterns`: Pattern to select XVGs to group their output e.g., Protein-*-RMSD.xvg (This will merge file names matching the pattern into single graph for comparative visualisation)
  * `export_ext`: Type of outputs, e.g., JPEG, PNG, JPG, PDF (Any output format supported by Matplotlib)
  * `dpi`: Resolution of the output, e.g., 72 for quick visualisation and 600 for standard publications
  * `flag_plot_mean`: yes|no; Use yes to enable plotting average value line
  * `flag_plot_std`: yes|no; Use yes to enable plotting standard deviation line
  * `flag_export_csv`: yes|no; If results should be exported in a CSV file (includes directory name, file name, average of lines plotted and their standard deviation)
  * `flag_export_plot`: yes|no; To specify if graphics should be exported or not (in case only values are needed)

## Exe Files (download and go solution!)

* **Download [GMXvg executable file (Windows 10/11)](https://github.com/TheBiomics/GMXvg/releases/download/v0.3/gmxvg-win-v0.3.exe) (_or check [latest or compatible executable](https://github.com/TheBiomics/GMXvg/releases) for improved features_) and copy/paste the exe file in the directory where XVG is contained. It will discover all xvg extension files in current or child folders and process them automatically.**
* After execution all xvgs will be converted to jpg. For example, "rmsd-protein.xvg" will be converted to "rmsd-protein.dpi300.jpeg".
* After execution a CSV file containing mean and standard deviation of of the plotted lines in each xvg. For example, for gyration plot "gyration.xvg", the CSV file will show following columns
  - `dir`: where xvg was stored
  - `file`: name of the processed xvg file
  - `plot`: label of the plotted line
  - `mean`: Mean of the plotted line
  - `std`: Standard deviation for the plotted line
* Example result output

![image](https://user-images.githubusercontent.com/87003331/168798303-330a9d46-2fed-4a53-b05f-35307b3a939f.png)

## Example Commands (using source code or executable file)

The utility finds *.xvg files in a directory or sub-directory. It need not to specify a file. This utility is made for bulk conversion of XVG files and extract the results in a separate directory.

### Simple (directly opening gxmvg executable file)
This will discover XVG files in the subdirectory where `gmxvg` executable is present and plot XVG in JPEG Format
* `gmxvg`

### Custom options using commandline
* `gmxvg -b <path-to-dir-containing-xvg-files>`

### Generate multiple qualities of graphics
* `gmxvg --dpi 96 300 600 --path_copy <path-to-aggregate-results-outside>`

### Export in multiple format(s)
* `gmxvg --export_ext JPEG pdf`

### Other customisations and advance functions

* To **merge multiple xvg files** having ending (e.g., /complex1/lig.xvg, /complex2/lig.xvg, /complex3/lig.xvg) passed to `-merge_patterns RMSD.xvg` so that it will combine all to plot one file. `--uid_part -1` parameter can be useful to define the Legend of the merged graphs.

```gmxvg --dpi 96 -merge_patterns RMSD-of-Ligand.xvg RMSD-of-Protein-C-Alpha.xvg Gyration-of-Protein.xvg NPT-Temperature.xvg Inter-Ligand-Protein-H-Bonds.xvg --replacements "Receptor1--Lig2":p53-miR5 "Recptor2--Lig3":p53-miR3 --path_move <path-to-output-dir>/graphs```

* Example to merge Protein-RMSD.xvg and Ligand-RMSD.xvg files in the same directory.
```gmxvg -merge_patterns RMSD.xvg -uid_part -1```

* Use `-replacements` options to replace any text in the plot will change the labels and legends of the plot

## Development

* To make any changes, fork this repository
* To contribute, create a pull request after you fork or comment

## Future Plans

* GUI or web interface through local server for [interactive visualisation](https://www.chartjs.org/docs/latest/samples/animations/progressive-line.html)
* Edit labels or text for invidiual graphs through GUI
* Small executable size
* Fast Executable
* Webserver to convert and combine graphs

## Accessory Details
* We recommend you going through the code to access the precision and quality of the generated results before you use.
* The code is free to be used by students, scholars, and professors.
* If you want to cite our work cite the publicly hosted version using [DOI:10.5281/zenodo.6563931](https://dx.doi.org/10.5281/zenodo.6563931).

## Troubleshooting installation

* Use `pip cache purge` in case of installation issue
