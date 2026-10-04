from .__metadata__ import __version__, __description__, __build__, __name__
from .GMXvg import GMXvg
from UtilityLib import CMDLib, OS, EntityPath

_cli_settings = {
    "path_base"        : (['-b'], None, OS.getcwd(), 'Provide base directory to run the process.', {}),
    "patterns_xvg"     : (['-p'], "*", ["*.xvg"], 'File patterns to match XVG files.', {}),
    "path_input_dirs"  : (['-i'], "*", None, 'Input directories containing XVG files.', {}),
    "export_ext"       : (['-e'], "*", ["jpg"], 'Export file extensions for plots.', {}),
    "export_dpi"       : (['-d'], "*", ["300"], 'DPI settings for exported plots.', {}),
    "flag_plot_mean"   : (['-m'], None, "Y", 'Flag to plot mean line (Y/N).', {}),
    "flag_plot_std"    : (['-s'], None, None, 'Flag to plot standard deviation lines (Y/N).', {}),
    "flag_export_csv"  : (['-c'], None, "Y", 'Flag to export results as CSV (Y/N).', {}),
    "flag_export_plot" : (['-f'], None, "Y", 'Flag to export plots (Y/N).', {}),
    "flag_cleanup"     : (['-x'], None, None, 'Flag to cleanup generated files (Y/N).', {}),
    "csv_filename"     : (['-o'], "*", "XVG-Plot-Values.csv", 'Output CSV filename for results.', {}),
  }

def xvgplot_cli():
  global _cli_settings
  _args = CMDLib.get_registered_args(_cli_settings, version=f"{__name__}-{__version__}")
  # Validate DPI upfront - fail fast if invalid
  _dpi_vals = _args.get('export_dpi', ['300'])
  if not isinstance(_dpi_vals, list):
    _dpi_vals = [_dpi_vals]
  _dpi_range = (72, 2400)
  _valid = [str(_d) for _d in _dpi_vals if str(_d).isdigit() and _dpi_range[0] <= int(_d) <= _dpi_range[1]]
  if _dpi_vals and not _valid:
    import sys
    sys.stderr.write(f"Error: No valid DPI values in {_dpi_vals}. Accepted range: {_dpi_range[0]}..{_dpi_range[1]}\n")
    sys.exit(1)
  _m = GMXvg(**_args)
  _m.plot()

def xvgplot_cli_test():
  # Setup test example
  global _cli_settings

  # Setup destination for test examples
  _test_destination = EntityPath('~/Desktop/GMXvg-Example-XVGs').resolved()
  if _test_destination.exists():
    _test_destination.delete(is_protected=False)  # force delete
  # Don't call validate() here - it creates the directory

  # Check for examples in the repo's docs directory (works in dev and pip install . from source)
  _package_dir = EntityPath(__file__).parent()
  _repo_root = _package_dir.parent()
  _test_examples = _repo_root / 'docs/example-xvgs'

  # Check if examples exist, otherwise download from GitHub
  if _test_examples.exists():
    print(f"Using examples from: {_test_examples.full_path}")
    _test_examples.copy(_test_destination)
  else:
    print(f"Examples not found. Downloading from GitHub...")
    _m_temp = GMXvg()

    # GitHub raw content URLs for example files
    _base_url = "https://raw.githubusercontent.com/TheBiomics/GMXvg/development/docs/example-xvgs"
    _example_files = [
      "gyrate_mdsim.xvg",
      "hbond_mdsim.xvg",
      "lig-hbond_mdsim.xvg",
      "lig-rmsd_mdsim.xvg",
      "rmsd_mdsim.xvg",
      "rmsf_mdsim.xvg",
      "pre-md/NPT-Temperature.xvg",
      "pre-md/NVT-Energy.xvg",
      "pre-md/Potential-Energy.xvg",
      "sasa/sas_mdsim.xvg",
      "sasa/sas_resarea_mdsim.xvg",
      "sasa/volume/sas_volume_mdsim.xvg",
    ]

  _args = CMDLib.get_registered_args(_cli_settings, version=f"{__name__}-{__version__}")
  _args['path_base'] = _test_destination.full_path

  _module = GMXvg(**_args)
  for _file_uid in _example_files:
    # Don't download if file already exists
    _dest = _test_destination / _file_uid
    if _dest.exists():
      continue
    _url = f"{_base_url}/{_file_uid}"
    _dest.parent().validate()
    _module.get_file(_url, _dest.full_path)
  _module.plot()
