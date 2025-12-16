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
  _m = GMXvg(**_args)
  _m.plot()

def xvgplot_cli_test():
  # Setup test example
  global _cli_settings

  # Setup destination for test examples
  _test_destination = EntityPath('~/Desktop/GMXvg-Example-XVGs').resolved()
  if _test_destination.exists():
    _test_destination.delete(False)
  _test_destination.validate()

  # Get the package directory and check for bundled examples
  _package_dir = EntityPath(__file__).parent(1)
  _test_examples = _package_dir / 'data/example-xvgs'

  # Check if examples exist in the package, otherwise download from GitHub
  if _test_examples.exists():
    print(f"Using bundled examples from: {_test_examples.full_path}")
    _test_examples.copy(_test_destination)
  else:
    print(f"Bundled examples not found. Downloading from GitHub...")
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
