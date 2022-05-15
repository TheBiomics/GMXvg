import pandas as PD
import os as OS
import re as REGEX
from Helper import Helper
import matplotlib.pyplot as PLOT

class GMXVGHelper(Helper):
  name = "GMX XVG Helper"
  version = "0.3"
  release_date = "May 15th, 2022"

  def __init__(self, *args, **kwargs):
    super(GMXVGHelper, self).__init__(**kwargs)
    self.__update_attr(**kwargs)

  def __set_defaults(self):
    if getattr(self, "csv_filepath") is None and len(getattr(self, "csv_filename", "")) > 4:
      self.csv_filepath = f"{self.path_base}{OS.sep}{self.csv_filename}"

  def __update_attr(self, *args, **kwargs):
    if not hasattr(self, "__defaults"): self.__defaults =  {
        "replacements_gmx": {
          'Hydrogen bonds': None,
          'Rg': None,
          '(nm)': None,
          'RMSD (nm)': None,
        },
        "replacements": None,
        "csv_filename": "XVG-Plot-Values.csv",
        "csv_filepath": None,
        "path_base": OS.getcwd(),
        "path_move": None,
        "path_copy": None,
        "pattern_xvg": "*.xvg",
        "merge_patterns": [],
        "export_ext": ["jpg"],
        "dpi": 300,
        "flag_plot_mean": "yes",
        "flag_plot_std": "no",
        "flag_export_csv": "no",
        "flag_export_plot": "y",
        "group_part": -2,
        "output_files": []
      }

    # Set all defaults
    [setattr(self, _k, self.__defaults[_k]) for _k in self.__defaults.keys() if not hasattr(self, _k)]
    self.__defaults = dict() # Unset defaults to prevent running for second time
    [setattr(self, _k, kwargs[_k]) for _k in kwargs.keys()]

    self.__set_defaults()

  def __plot_xvgs(self, *args, **kwargs):
    _xvgs = args[0] if len(args) > 0 else kwargs.get("xvg_paths")
    _result_dict = []
    for _xvg in _xvgs:
      _result = self.__plot_xvg(_xvg, **kwargs)
      _file_name = self.filename(_xvg)
      _dir_name = _xvg.split(self.path_base)[-1]
      _dir_name = _dir_name.replace(self.filename(_xvg, with_ext=True), "")
      _dir_name = _dir_name.strip("/")
      for _col in _result.columns[1:].tolist():
        _result_dict.append({
            "dir": _dir_name,
            "file": _file_name,
            "plot": _col,
            "mean": _result[_col].mean(),
            "std": _result[_col].std(),
        })
    if getattr(self, "flag_export_csv", False):
      _results = PD.DataFrame(_result_dict)
      self.log_info(f"Writing results to {self.csv_filepath}.")
      _results.to_csv(self.csv_filepath, index=False)
    else:
      self.log_info("Not writing the results.", type="warn")

  def __find_xvgs(self, *args, **kwargs):
    _xvgs = []
    if hasattr(self, "pattern_dir"):
      self.pattern_dir = [self.pattern_dir] if isinstance(self.pattern_dir, str) else self.pattern_dir
      _directories = []
      for _dp in self.pattern_dir:
        _d = self.search_dirs(self.path_base, _dp)
        _directories.extend(_d)
      for _dir in _directories:
        for _px in self.pattern_xvg:
          _x = self.search_files(_dir, _px)
          _xvgs.extend(_x)
    else:
      _xvgs = self.get_file_types(self.path_base, (".xvg"))

    return _xvgs

  def __rearrange_files(self):
    _bool_copy = getattr(self, "path_copy") and len(self.path_copy) > 2
    _bool_move = getattr(self, "path_move") and len(self.path_move) > 2
    for _file in self.output_files:
      _rel_path = _file.split(self.path_base)[-1]
      _rel_path = _rel_path.strip("/")
      self.copy(_file, f"{self.path_copy}/{_rel_path}") if _bool_copy else None
      self.move(_file, f"{self.path_move}/{_rel_path}") if _bool_move else None

  @staticmethod
  def process_text(_str):
      _str = _str.strip()
      _str = REGEX.sub(r'\s{2,}', " ", _str)
      _str = _str.replace(r"\s", "").replace(r"\N", "")
      return _str

  @staticmethod
  def process_attrib(_line):
      _line = _line.strip("@").strip()
      _matches = REGEX.findall('(.*)"([^"]*)"', _line)
      _attribs = {}
      if _line.startswith("legend"):
          _ls = _line.split(" ", 1)
          _attribs["plot_display_setting"] = GMXVGHelper.process_text(_ls[-1])
      elif len(_matches) > 0:
        for _v in _matches:
          _attribs[GMXVGHelper.process_text(_v[0])] = GMXVGHelper.process_text(_v[-1])
      elif len(_line.split(" ", 1)) == 2:
          _ls = _line.split(" ", 1)
          _attribs[GMXVGHelper.process_text(_ls[0])] = GMXVGHelper.process_text(_ls[-1])
      return _attribs

  def __parse_xvg_table_attributes(self, _xvg_path):
    _xvg_content = self.read_text(_xvg_path)

    _data_rows = []
    _attributes = {}
    for _line in _xvg_content:
        _line = _line.strip("\n").strip()
        if _line.startswith("#"):
            continue # As it is a comment
        elif _line.startswith("@"):
            _attr = self.process_attrib(_line)
            if len(_attr.keys()) > 0 and isinstance(_attr, dict):
                _attributes.update(_attr)
        else:
            _data_rows.append(_line.split())
    _df = PD.DataFrame(_data_rows)
    _df = _df.apply(PD.to_numeric)

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

  # Parse XVG File and Plot Graph
  def __plot_xvg(self, *args, **kwargs):
    _xvg = args[0] if len(args) > 0 else kwargs.get("xvg_path")
    self.log_info(f"Plotting {_xvg}.")

    _df, _attributes = self.__parse_xvg_table_attributes(_xvg)

    self.export_ext = [self.export_ext] if isinstance(self.export_ext, (str)) else self.export_ext

    _xaxis_label = _attributes.get('xaxis label')
    _yaxis_label = _attributes.get('yaxis label')

    _exp = getattr(self, "flag_export_plot", "yes")

    if _exp.lower().startswith("y"):
      _plot_title = REGEX.sub(r'[\s-]{2,}', " ", self.filename(_xvg))
      if _attributes.get("subtitle"):
          _subtitle = _attributes.get("subtitle")
          _plot_title = f"{_plot_title}\n{_subtitle}"

      _plot = _df.set_index(_df.columns[0]).plot(title=_plot_title, linewidth=1)

      for _pl in _plot.get_lines():
          _pl_ydata = _pl.get_ydata()
          _pl_ydata_mean = _pl_ydata.mean()

          if self.flag_plot_mean.lower().startswith("y"):
            _plot.axhline(y=_pl_ydata_mean, color=_pl.get_color(), linestyle="--", linewidth=1)

          if self.flag_plot_std.lower().startswith("y"):
            _pl_ydata_std = _pl_ydata.std()
            _pl_ydata_upper = _pl_ydata_mean + _pl_ydata_std
            _pl_ydata_lower = _pl_ydata_mean - _pl_ydata_std
            _plot.axhline(y=_pl_ydata_upper, color=_pl.get_color(), linestyle="--", linewidth=0.5)
            _plot.axhline(y=_pl_ydata_lower, color=_pl.get_color(), linestyle="--", linewidth=0.5)

      _legend = _plot.legend(fontsize=8)
      _plot.set_xlabel(_xaxis_label)
      _plot.set_ylabel(_yaxis_label)

      for _ext in self.export_ext:
        _dpi = [self.dpi] if isinstance(self.dpi, (str, int)) else self.dpi
        for _d in _dpi:
          _out_file = self.change_ext(_xvg, f"{_d}dpi.{_ext}")
          self.output_files.append(_out_file)
          _figure = _plot.get_figure()
          _figure.savefig(_out_file, dpi=int(_d), bbox_inches='tight')
      _figure.clear()
      PLOT.close(_figure)

    return _df

  def __merge_xvgs(self, *args, **kwargs):
    self.__update_attr(**kwargs)
    self.merge_patterns = [self.merge_patterns] if isinstance(self.merge_patterns, str) else self.merge_patterns
    _replacements = {}
    _replacements.update(self.replacements_gmx)

    for _r in self.replacements:
      _k_v = REGEX.split('[:=]', _r)
      if len(_k_v) > 1:
        _k = _k_v[0]
        _v = _k_v[-1]
        _replacements[_k.strip()] = _v.strip()

    if isinstance(self.path_base, (str)):
      for _mp in self.merge_patterns:
        _xvgs = self.get_file_types(self.path_base, _mp)
        self.log_info(f"Merging {len(_xvgs)} xvg(s) for {_mp} pattern.")
        _merged_df = None
        _plot_name = self.filename(_mp.replace("*", ""))
        _y_label = None
        for _xvg in _xvgs:
          _df, _attr = self.__parse_xvg_table_attributes(_xvg)

          _complex_name = self.get_parts(_xvg, self.group_part) #

          _xvg_str_rep = _replacements.copy()

          for _k, _v in _xvg_str_rep.items():
            _complex_name = _complex_name.replace(_k, _v) if _v is not None else _complex_name

          _required_cols = _df.columns[:2] # Only first two columns would be plotted
          _df_min = _df[_required_cols].copy()

          _xvg_str_rep.update({_df_min.columns[1]: _complex_name})
          _xvg_str_rep = {_rc: _complex_name for _rc in _xvg_str_rep.keys()}

          _y_label = _df_min.columns[1] if _y_label is None else _y_label

          _df_min = _df_min.rename(columns=_xvg_str_rep) #

          if _merged_df is None:
            _merged_df = _df_min
          else:
            _merged_df[_complex_name] = _df_min[_complex_name]

        _plot = _merged_df.set_index(_required_cols[0]).plot(title=_plot_name, lw=1)
        _legend = _plot.legend(fontsize=6)
        _plot.set_ylabel(_y_label)
        for _pl in _plot.get_lines():
          _pl_ydata = _pl.get_ydata()
          _pl_ydata_mean = _pl_ydata.mean()

          if self.flag_plot_mean.lower().startswith("y"):
            _plot.axhline(y=_pl_ydata_mean, color=_pl.get_color(), linestyle="--", linewidth=1)

          if self.flag_plot_std.lower().startswith("y"):
            _pl_ydata_std = _pl_ydata.std()
            _pl_ydata_upper = _pl_ydata_mean + _pl_ydata_std
            _pl_ydata_lower = _pl_ydata_mean - _pl_ydata_std
            _plot.axhline(y=_pl_ydata_upper, color=_pl.get_color(), linestyle="--", linewidth=0.5)
            _plot.axhline(y=_pl_ydata_lower, color=_pl.get_color(), linestyle="--", linewidth=0.5)

        _dpi = [self.dpi] if isinstance(self.dpi, (str, int)) else self.dpi

        for _d in _dpi:
          _out_file = f"{self.path_base}/Combined-{_plot_name}.{_d}.jpg"
          print(_out_file)
          self.output_files.append(_out_file)
          _figure = _plot.get_figure()
          _figure.savefig(_out_file, dpi=int(_d), bbox_inches='tight')

        _figure.clear()
        PLOT.close(_figure)
    else:
      self.log_error("Error with working dir.")

  def export_xvg(self, *args, **kwargs):
    self.__update_attr(**kwargs)
    self.pattern_xvg = [self.pattern_xvg] if isinstance(self.pattern_xvg, str) else self.pattern_xvg

    if isinstance(self.path_base, (str)):
        self.__plot_xvgs(self.__find_xvgs())
        self.__rearrange_files()
        self.__merge_xvgs() if len(self.merge_patterns) > 0 else ""
    else:
      self.log_error("Error with working dir.")
