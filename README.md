
```diff
+ Latest release GMXvg v0.3
+ with Ubuntu and windows executable to download and run in the directory containing XVG files.
```
> Get [GMXvg v0.3 here](https://github.com/TheBiomics/GMXvg/releases/tag/v0.3).

# GMXvg: Utility to Convert/Plot GROMACS XVG files

Commandline based GROMACS XVG File plotting utility.
* Discovers all the XVG files in the current or subdirectories and converts them in specified file formats (default JPG). 
* Logs the summary of plots in a file to quickly access the plot values along with their standard deviation values.

## Supported Platforms

The utility was developed and tested for following OS. However, we expect it to work on all windows and linux environment.

* Windows 11
* Ubuntu 20 LTS


## Command Structure

* `--<key>=<value>`: Double dash separated by equal sign
* `-<key> <val1> <val2> <val3>` Single dash (single dash is not recommended) and multiple values

## Supported overriding variables

  * `path_base`: Base path if running from different directory
  * `csv_filename`: File name for CSV output else default will be used
  * `csv_filepath`: Path where CSV output file will be stored
  * `path_move`: Path where generated images will be moved (will be deleted from the dir where XVG are stored)
  * `path_copy`: Path where generated images will be copied (source graphics will be there)
  * `pattern_xvg`: Pattern to specify XVG images for conversion e.g., *--new.xvg, old-*-temp-300.xvg
  * `merge_patterns`: Pattern to select XVGs to group their output e.g., Protein-*-RMSD.xvg
  * `export_ext`: Type of outputs, e.g., JPEG, PNG, JPG, PDF (Anything supported by Matplotlib)
  * `dpi`: Resolution of the output, e.g., 72 for quick visualisation and 600 for many publications
  * `flag_plot_mean`: yes|no; Use yes to enable plotting average line
  * `flag_plot_std`: yes|no; Use yes to enable plotting standard deviation lines
  * `flag_export_csv`: yes|no; If results should be exported in the form of CSV (includes directory name, file name, average of lines plotted and their standard deviation)
  * `flag_export_plot`: yes|no; To specify if graphics should be exported or not

## Fastest Execution (Download and go solution!)

* Download [GMXvg executable file (Windows 10/11)](https://github.com/TheBiomics/GMXvg/releases/download/v0.3/gmxvg-win-v0.3.exe) (_or check [latest or compatible release](https://github.com/TheBiomics/GMXvg/releases) for improved features_) and copy/paste the executable file in the directory where XVG is contained or the directory having subdirectories with XVG extension files. It will discover xvg extension files and process them automatically.
* After execution all xvgs will be converted to jpg. For example, "rmsd-protein.xvg" will be converted to "rmsd-protein.dpi300.jpeg". 
* After execution a CSV file containing mean and standard deviation of of the plotted lines in each xvg. For example, for gyration plot "gyration.xvg", the CSV file will hold information about `dir`: where xvg was stored, `file`: name of the xvg file which was converted to jpg,`plot`: label of the plotted line, and `mean` and `std` columns. 
* Example result output

![image](https://user-images.githubusercontent.com/87003331/168798303-330a9d46-2fed-4a53-b05f-35307b3a939f.png)
  
* To obtain customised out or results see commandline operations.

## Example Commands

The utility finds *.xvg files in a directory or sub-directory. It need not to specify a file. This utility is made for bulk conversion of XVG files and extract the results in a separate directory.
### Simple (using executable file)
This will discover XVG files and plot XVG in JPEG Format
* `gmxvg`
* `gmxvg -b <path-to-dir-containing-xvg-files>`

### Generate multiple qualitie(s) of graphics
* `gmxvg --dpi 96 300 600 --path_copy <path-to-aggregate-results-outside>`

### Export in multiple format(s)
* `gmxvg --export_ext JPEG pdf`

### Customised
* `gmxvg --dpi 96 -merge_patterns RMSD-of-Ligand.xvg RMSD-of-Protein-C-Alpha.xvg Gyration-of-Protein.xvg NPT-Temperature.xvg Inter-Ligand-Protein-H-Bonds.xvg --replacements "Receptor1--Lig2":p53-miR5 "Recptor2--Lig3":p53-miR3 --path_move <path-to-output-dir>/graphs`

## Development

* To make any changes, fork this repository
* To contribute, create a pull request after you fork or comment

## Future Improvements

* GUI
* Edit invidiual graphs through GUI

## Other things
* We recommend you going through the code to access the precision and quality of the generated results before you use.
* The code is free to be used by students, scholars, and professors.
