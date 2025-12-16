from UtilityLib import ProjectManager, EntityPath, CMDLib, ObjDict
from .__metadata__ import __name__, __version__, __description__

class GMXvg(ProjectManager):
  name        = __name__
  description = __description__
  version     = __version__

  # Section 0: Initialization and Defaults
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.__set_defaults(**kwargs)

  def __set_defaults(self, *args, **kwargs):
    __defaults =  {
        "replacements_gmx": {
          'Hydrogen bonds': None,
          'Rg'            : None,
          '(nm)'          : None,
          'RMSD (nm)'     : None,
          ".xvg"          : "",
          "Plot"          : ""
        },
        "patterns_xvg"     : ["*.xvg"],
        "path_input_dirs" : None,
        "export_ext"      : ["jpg"],
        "export_dpi"      : ["300"],
        "flag_plot_mean"  : "Y",
        "flag_plot_std"   : "N",
        "flag_export_csv" : "N",
        "flag_export_plot": "Y",
        "flag_cleanup"    : "N",
        "csv_filename"    : "XVG-Plot-Values.csv",
      }

    __defaults.update(kwargs)

    self.preset('data,plot')

    if not hasattr(self, '_path_current'):
      self._path_current = self.path_base

    self.config.file_storage = self.config.file_storage or ObjDict()
    self.require('shutil', 'SHUtil')
    _use_tex = True if self.SHUtil.which('latex') else False
    self.PLOT.rcParams.update({
      "text.usetex": _use_tex,
      "font.family": "sans-serif",
      "font.size"  : "14",
    })
    self.require('re', 'REGEX')
    self.update_attributes(self, __defaults)

  def is_flag_y(self, flag_name):
    if hasattr(self, flag_name):
      return str(getattr(self, flag_name, '')).lower().startswith('y')
    return False

  # Section 1: Discover Files and Directories
  def _get_file_patterns(self, *args, **kwargs):
    """Makes pattern xvg as list so that multiple patterns are supported to allow selective images"""
    if isinstance(self.patterns_xvg, (str)):
      self.patterns_xvg = [self.patterns_xvg]

    return self.patterns_xvg

  def _get_input_dirs(self, *args, **kwargs):
    """Returns the input directories as a list"""
    if self.path_input_dirs is None:
      # Return all the sub directories under the current directory
      self.path_input_dirs = [_d for _d in self._path_current.walk_dirs]

    if isinstance(self.path_input_dirs, (str, EntityPath)):
      self.path_input_dirs = [self.path_input_dirs]

    return [EntityPath(_inputd).expanduser().resolve() for _inputd in self.path_input_dirs]

  @property
  def all_xvg_files(self):
    if self._all_xvg_files is None or len(self._all_xvg_files) == 0:
      self._find_xvg_files()
    return self._all_xvg_files

  def _get_file_attrib(self, file_path):
      file_path = EntityPath(file_path)
      _stats_dict = {k.replace('st_', ''): getattr(file_path.get_stats(), k) for k in dir(file_path.get_stats()) if k.startswith('st_')}
      _req_attribs = ['size', 'mtime', 'ctime', 'atime', 'mode']
      _stats_dict = {k: v for k, v in _stats_dict.items() if k in _req_attribs}
      _file_attribs = ObjDict({
        'file_hash' : file_path.hash,
        'file_path' : str(file_path),
        'file_stats': _stats_dict,
      })

      return _file_attribs

  _file_storage = ObjDict()
  def set_file_storage(self, *args, **kwargs):
    self._find_xvg_files(*args, **kwargs)
    for _xvg_file in self.all_xvg_files:
      _file_attribs                     = self._get_file_attrib(_xvg_file)
      _file_attribs['generated_graphs'] = []
      _file_attribs['result_df']        = []
      self.config.file_storage[_xvg_file.full_path] = _file_attribs

  _all_xvg_files = []
  def _find_xvg_files(self, *args, **kwargs):
    """Finds files with XVG extension"""

    for _input_dir in self._get_input_dirs(*args, **kwargs):
      if not _input_dir.exists():
        self.log_warn(f'Directory {_input_dir.name} does not exist under {_input_dir.parent()}. Skipping...')
        continue
      for _xvg_pattern in self._get_file_patterns(*args, **kwargs):
        _xvgs = list(_input_dir.search(_xvg_pattern))
        self._all_xvg_files.extend(_xvgs)

    return self._all_xvg_files

  # Part 2: Helpers methods
  def _clean_text(self, _str):
    _str = _str.strip()
    _str = r'{}'.format(_str)
    _str = self.REGEX.sub(r'\s{2,}', " ", _str)
    _str = self.REGEX.sub(r'[\s-]{1,}', " ", _str)
    _str = _str.replace("_", "-")
    _str = self.REGEX.sub(r'\\S(\w+)\\N', "$^\\1$", _str)
    _str = self.REGEX.sub(r'\\s(\w)\\N', "$_\\1$", _str)
    return _str

  def _clean_attributes(self, _line):
    _line = _line.strip("@").strip()
    _matches = self.REGEX.findall('(.*)"([^"]*)"', _line)
    _attribs = {}
    if _line.startswith("legend"):
      _ls = _line.split(" ", 1)
      _attribs["plot_display_setting"] = self._clean_text(_ls[-1])
    elif len(_matches) > 0:
      for _v in _matches:
        _attribs[self._clean_text(_v[0])] = self._clean_text(_v[-1])
    elif len(_line.split(" ", 1)) == 2:
      _ls = _line.split(" ", 1)
      _attribs[self._clean_text(_ls[0])] = self._clean_text(_ls[-1])
    return _attribs

  def _parse_xvg_table_attributes(self, _xvg_path):
    _xvg_content = self.read_text(_xvg_path)
    _data_rows  = []
    _attributes = {}
    for _line in _xvg_content:
      _line = _line.strip("\n").strip()
      if _line.startswith("#"):
        # Skip comment lines
        continue
      elif _line.startswith("@"):
        _attr = self._clean_attributes(_line)
        if len(_attr.keys()) > 0 and isinstance(_attr, dict):
          _attributes.update(_attr)
      else:
        _data_rows.append(_line.split())

    _df = self.DF(_data_rows)
    _df = _df.apply(self.PD.to_numeric)

    _xaxis_label = _attributes.get('xaxis label')
    _yaxis_label = _attributes.get('yaxis label')
    _legends = [_attributes[_k] for _k in _attributes if "legend" in _k]

    if _df.shape[1] == 2 and len(_legends) < 1:
      _legends = [_yaxis_label]

    _legends.insert(0, _attributes.get('xaxis label'))
    if len(_df.columns) == len(_legends):
      _df.columns = _legends
    else:
      self.log_info(f"Cannot change the column names in {_xvg_path}.\nCOLUMNS = {_df.columns}\nLEGENDS={_legends}", type="error")
    return (_df, _attributes)

  def _get_export_exts(self, *args, **kwargs):
    """Returns the export file extensions"""
    if not self.is_iterable(self.export_ext):
      self.export_ext = ["png", "pdf"]
    return self.unique(self.export_ext)

  _dpi_range = (72, 2400)
  def _get_export_dpi(self, *args, **kwargs):
    """Returns the export DPI settings"""
    if not self.is_iterable(self.export_dpi):
      self.export_dpi = str(self.export_dpi) if isinstance(self.export_dpi, (int, str)) else "300"
      self.export_dpi = [self.export_dpi]

    self.export_dpi = [str(_d) for _d in self.export_dpi if str(_d).isdigit() and self._dpi_range[0] <= int(_d) <= self._dpi_range[1]]
    return self.unique(self.export_dpi)

  # Section 3: Post Processing
  def _merge_xvgs(self, *args, **kwargs):
    """Merges multiple XVG files into a single DataFrame
      - Overlaying of multiple plots
      - Handling of different data lengths
      - Merging of metadata attributes
    """

  def _rearrange_files(self, *args, **kwargs):
    """Post-processes the merged XVG DataFrame
      - Moving/copying files to single directory
    """
    _bool_copy = hasattr(self, "path_copy") and len(self.path_copy) > 2
    _bool_move = hasattr(self, "path_move") and len(self.path_move) > 2

    if not any([_bool_copy, _bool_move]):
      self.log_debug('No action set to file rearrange.')
      return

    if _bool_copy or _bool_move:
      # First Copy
      # Update the configuration to have duplicated paths
      ...

    if _bool_move:
      # Then Delete the original files
      # Update the configuration
      ...

  def _cleanup_working_dir(self, *args, **kwargs):
    """Cleans up the working directory by removing temporary files
      - Deletes intermediate files
      - Zips the generated files for backup
    """

    # Cleanup the generated images generated by the GMXvg
    if self.is_flag_y("flag_cleanup"):
      for _fk, _file_info in self.config.file_storage.items():
        for _fgen in _file_info.generated_graphs:
          _file_path = EntityPath(_fgen.file_path)
          if not 'file_deleted_ts' in _fgen:
            _fgen.file_deleted_ts = []

          if _file_path.exists() and _fgen.file_hash == _file_path.hash:
            _file_path.delete(False)
            _fgen.file_deleted_ts.append(self.timestamp)

      self.update_config()

  # Section 4: Process XVG Files
  def _plot_xvg(self, *args, **kwargs):
    """Parse XVG files and plot graphs"""
    _xvg_file_path = kwargs.get("xvg_path", args[0] if len(args) > 0 else None)

    if not _xvg_file_path or not EntityPath(_xvg_file_path).exists():
      return

    _xvg_file_path = EntityPath(_xvg_file_path).expanduser().resolve()

    self.log_info(f"Plotting {_xvg_file_path}.")

    _plot_df, _attributes = self._parse_xvg_table_attributes(_xvg_file_path)

    _xaxis_label = _attributes.get('xaxis label')
    _yaxis_label = _attributes.get('yaxis label')

    if self.is_flag_y("flag_export_plot"):
      _plot_title = self._clean_text(_xvg_file_path.stem)

      if _attributes.get("subtitle"):
        _subtitle   = self._clean_text(_attributes.get("subtitle"))
        _plot_title = f"{_plot_title}\n{_subtitle}\n"

      _plot = _plot_df.set_index(_plot_df.columns[0]).plot(title=_plot_title, linewidth=1)

      for _pl in _plot.get_lines():
        _pl_ydata      = _pl.get_ydata()
        _pl_ydata_mean = _pl_ydata.mean()

        if self.is_flag_y("flag_plot_mean"):
          _plot.axhline(y=_pl_ydata_mean, color=_pl.get_color(), linestyle="--", linewidth=1)

        if self.is_flag_y("flag_plot_std"):
          _pl_ydata_std   = _pl_ydata.std()
          _pl_ydata_upper = _pl_ydata_mean + _pl_ydata_std
          _pl_ydata_lower = _pl_ydata_mean - _pl_ydata_std
          _plot.axhline(y=_pl_ydata_upper, color=_pl.get_color(), linestyle="--", linewidth=0.5)
          _plot.axhline(y=_pl_ydata_lower, color=_pl.get_color(), linestyle="--", linewidth=0.5)

      _legend = _plot.legend(fontsize=8)
      _plot.set_xlabel(_xaxis_label)
      _plot.set_ylabel(_yaxis_label)

      for _ext in self._get_export_exts():
        for _d in self._get_export_dpi():
          _out_file = _xvg_file_path.with_suffix(f".{_d}dpi.{_ext}")
          _figure = _plot.get_figure()
          _figure.savefig(_out_file, dpi=int(_d), bbox_inches='tight')
          _file_attribs = self._get_file_attrib(_out_file)
          _file_attribs['dpi'] = _d
          _file_attribs['ext'] = _ext
          self.config.file_storage[_xvg_file_path.full_path]['generated_graphs'].append(_file_attribs)
      _figure.clear()
      self.PLOT.close(_figure)

    self.config.file_storage[_xvg_file_path.full_path]['result_df'] = _plot_df

  def _process_xvgs(self, *args, **kwargs):
    """Plots XVG files from the given list"""
    self.set_file_storage(*args, **kwargs)
    _result_dict = []
    for _file_path in self.config.file_storage._keys:
      self._plot_xvg(_file_path, **kwargs)

    self.update_config()

  # Section 5: Process Results
  def _generate_results(self, *args, **kwargs):
    _result_dict = []
    for _file_data in self.config.file_storage.values():
      _result_df = _file_data.result_df.copy()
      for _col in _result_df.columns[1:].tolist():
        _fp = EntityPath(_file_data.file_path)
        _result_dict.append({
            "dir" : str(_fp.parent()),
            "file": _fp.name,
            "plot": _col,
            "mean": _result_df[_col].mean(),
            "std" : _result_df[_col].std(),
            "min" : _result_df[_col].min(),
            "q_10": _result_df[_col].quantile(0.1),
            "q_50": _result_df[_col].quantile(0.5),
            "q_90": _result_df[_col].quantile(0.9),
            "max" : _result_df[_col].max(),
        })

    if self.is_flag_y("flag_export_csv") and len(_result_dict) > 0:
      _results = self.DF(_result_dict)
      self.log_info(f"Writing results to {self.csv_filename}.")
      _results.to_csv(str(self._path_current / self.csv_filename), index=False)

    else:
      self.log_info("Not writing the results.", type="warn")

  def plot(self, *args, **kwargs):
    """CLI method to plot XVG files"""
    self._process_xvgs(*args, **kwargs)
    self._generate_results(*args, **kwargs)
    self._rearrange_files(*args, **kwargs)
    self._cleanup_working_dir(*args, **kwargs)
    self.update_config()
