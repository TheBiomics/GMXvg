import os as OS
import argparse as ARGUMENT
import re as REGEX
import pandas as PD
from UtilityLib import UtilityManager
import matplotlib.pyplot as PLOT
import shutil as SHUtil

class GMXvg(UtilityManager):
  __package__ = "GMXvg"
  __version__ = "0.4"
  __subversion__ = "20230830"
  __author__ = "Vishal Kumar Sahu"

  def __init__(self, *args, **kwargs):
    super(GMXvg, self).__init__(**kwargs)
    _use_tex = True if SHUtil.which('latex') else False
    PLOT.rcParams.update({
      "text.usetex": _use_tex,
      "font.family": "sans-serif",
    })
    self.__update_attr(**kwargs)

  def __set_defaults(self):
    self.csv_filepath = f"{self.path_base}{OS.sep}{self.csv_filename}"

  def __update_attr(self, *args, **kwargs):
    if not hasattr(self, "__defaults"): self.__defaults =  {
        "replacements_gmx": {
          'Hydrogen bonds': None,
          'Rg': None,
          '(nm)': None,
          'RMSD (nm)': None,
          ".xvg": "",
          "Plot": ""
        },
        "replacements": {},
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
        "uid_part": -2,
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
            "min": _result[_col].min(),
            "q_10": _result[_col].quantile(0.1),
            "q_50": _result[_col].quantile(0.5),
            "q_90": _result[_col].quantile(0.9),
            "max": _result[_col].max(),
        })
    if getattr(self, "flag_export_csv", False) and len(_result_dict) > 0:
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
    self.output_files.append(self.csv_filepath)
    for _file in self.output_files:
      _rel_path = _file.split(self.path_base)[-1]
      _rel_path = _rel_path.strip("/")

      self.copy(_file, f"{self.path_copy}/{_rel_path}") if _bool_copy and self.check_path(_file) else None
      self.move(_file, f"{self.path_move}/{_rel_path}") if _bool_move and self.check_path(_file) else None

  @staticmethod
  def process_text(_str):
      _str = _str.strip()
      _str = r'{}'.format(_str)
      _str = REGEX.sub(r'\s{2,}', " ", _str)
      _str = REGEX.sub(r'[\s-]{1,}', " ", _str)
      _str = _str.replace("_", "-")
      _str = REGEX.sub(r'\\S(\w+)\\N', "$^\\1$", _str)
      _str = REGEX.sub(r'\\s(\w)\\N', "$_\\1$", _str)
      return _str

  @staticmethod
  def process_attrib(_line):
      _line = _line.strip("@").strip()
      _matches = REGEX.findall('(.*)"([^"]*)"', _line)
      _attribs = {}
      if _line.startswith("legend"):
          _ls = _line.split(" ", 1)
          _attribs["plot_display_setting"] = GMXvg.process_text(_ls[-1])
      elif len(_matches) > 0:
        for _v in _matches:
          _attribs[GMXvg.process_text(_v[0])] = GMXvg.process_text(_v[-1])
      elif len(_line.split(" ", 1)) == 2:
          _ls = _line.split(" ", 1)
          _attribs[GMXvg.process_text(_ls[0])] = GMXvg.process_text(_ls[-1])
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
      _plot_title = self.process_text(self.filename(_xvg))

      if _attributes.get("subtitle"):
          _subtitle = self.process_text(_attributes.get("subtitle"))
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
          _complex_name = self.get_parts(_xvg, self.uid_part) #

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


        if isinstance(_merged_df, PD.DataFrame):
          _plot = _merged_df.set_index(_required_cols[0]).plot(title=_plot_name, lw=1)
          _legend = _plot.legend(fontsize=6)
          _plot.set_ylabel(self.process_text(_y_label))
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
            self.output_files.append(_out_file)
            _figure = _plot.get_figure()
            _figure.savefig(_out_file, dpi=int(_d), bbox_inches='tight')

          _figure.clear()
          PLOT.close(_figure)
          PLOT.cla()
        else:
          self.log_error("Some error occurred.")
    else:
      self.log_error("Error with working dir.")

  def export_xvg(self, *args, **kwargs):
    self.__update_attr(**kwargs)
    self.pattern_xvg = [self.pattern_xvg] if isinstance(self.pattern_xvg, str) else self.pattern_xvg

    if isinstance(self.path_base, (str)):
      self.__merge_xvgs() if len(self.merge_patterns) > 0 else ""
      self.__plot_xvgs(self.__find_xvgs())
      self.__rearrange_files()
    else:
      self.log_error("Error with working dir.")

def xvgplot():
  print(f"{GMXvg.__package__} v{GMXvg.__version__} (Build-{GMXvg.__subversion__})")
  print("=" * 80)
  print(f"Other available options are:")
  print(f"csv_filename, csv_filepath, path_base, path_move, path_copy, pattern_xvg, merge_patterns,")
  print(f"export_ext, dpi, flag_plot_mean, flag_plot_std, flag_export_csv, flag_export_plot, output_files")
  print("=" * 80)
  _plotter = GMXvg()
  _parser = ARGUMENT.ArgumentParser(prog=GMXvg.name)

  _parser.add_argument('-b', '--path_base', nargs = None, default = OS.getcwd(), help = 'Provide base directory. Default: %(default)s.')
  _parser.add_argument('-e', '--export_ext', nargs = "*", default = ["jpg"], help = 'Output formats. Default: %(default)s.')
  _parser.add_argument('-d', '--dpi', nargs = "*", default = [300], help = 'Output quality. Default: %(default)s.')

  _reg_args, _unreg_args = _parser.parse_known_args()
  _reg_args = vars(_reg_args)
  _reg_args = {_k: _reg_args[_k] for _k in _reg_args.keys() if _reg_args[_k] is not None}

  _params = _plotter.unregistered_arg_parser(_unreg_args)
  _params.update(_reg_args)
  _plotter.export_xvg(**_params)
