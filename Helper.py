import os as OS
from pathlib import Path as PATH
from warnings import warn as WARN
import shutil as SHUTIL

class Helper:
  def __init__(self, *args, **kwargs):
    pass

  def read_text(self, *args, **kwargs):
    _path = args[0] if len(args) > 0 else kwargs.get("path")
    _content = None
    with open(_path, 'r', encoding='UTF8') as f:
      _content = f.readlines()
    return _content

  def filename(self, *args, **kwargs):
    _file_path = args[0] if len(args) > 0 else kwargs.get("file_path")
    _with_ext = args[1] if len(args) > 1 else kwargs.get("with_ext", False)
    _with_dir = args[2] if len(args) > 2 else kwargs.get("with_dir", False)
    _num_ext = args[3] if len(args) > 3 else kwargs.get("num_ext", 1)

    if not _file_path:
      return None

    if _with_dir is False:
      _file_path = OS.path.basename(_file_path)

    if _with_ext is True:
      return str(_file_path)

    _file_path = _file_path.rsplit(".", _num_ext)

    if len(_file_path):
      return _file_path[0]

    return None

  def search_dirs(self, *args, **kwargs):
    _source = args[0] if len(args) > 0 else kwargs.get("dir", getattr(self, "dir"))
    _pattern = args[1] if len(args) > 1 else kwargs.get("pattern", "/*/")
    return self.search(_source, _pattern)

  def search_files(self, *args, **kwargs):
    _source = args[0] if len(args) > 0 else kwargs.get("dir", getattr(self, "dir"))
    _pattern = args[1] if len(args) > 1 else kwargs.get("pattern", ["*"])

    return self.search(_source, _pattern)

  def search(self, *args, **kwargs):
    _results = []
    _source = args[0] if len(args) > 0 else kwargs.get("source", getattr(self, "source"))
    _pattern = args[1] if len(args) > 1 else kwargs.get("pattern", "*")

    if not _source or not _pattern:
      return _results

    if isinstance(_pattern, str):
      _pattern = [_pattern]

    for _p in _pattern:
      _results.extend([str(f) for f in PATH(_source).glob(_p)])

    return _results

  def flatten_args(self, *args, **kwargs):
    _args = args[0] if len(args) > 0 else kwargs.get("mapping", [])
    _flattened = {}
    if isinstance(_args, (dict)):
      _flattened = {_k: _v[0] if len(_v) == 1 else _v for _k, _v in _args.items()}
    return _flattened

  def unregistered_arg_parser(self, *args, **kwargs):
    # New arguments should start with -n/--name
    # Values are infinite???
    _un_args = args[0] if len(args) > 0 else kwargs.get("unregistered_args", [])

    _arg_aggregator = {}
    _key = None
    for _ua in _un_args:
      if _ua.startswith(("-", "--")) and not _ua.lstrip("-").isdigit():
        _key = _ua.strip("-")
        _key, _attached_value = _key.split("=", 1) if "=" in _key else (_key, "")

        if not _key in _arg_aggregator.keys():
          _arg_aggregator[_key] = []

        _arg_aggregator[_key].append(_attached_value) if len(_attached_value) > 0 else None

      elif _key and _key in _arg_aggregator.keys():
        _arg_aggregator[_key].append(_ua)
    return self.flatten_args(_arg_aggregator)

  def check_path(self, *args, **kwargs):
    _path = args[0] if len(args) > 0 else kwargs.get("path")
    _result = OS.path.exists(_path) if _path else None
    return _result

  def create_dir(self, *args, **kwargs):
    _dir_paths = args[0] if len(args) > 0 else kwargs.get("dirs")

    if isinstance(_dir_paths, str):
      _dir_paths = [_dir_paths]

    _dir_created = {}
    for _d in _dir_paths:
      if not OS.path.exists(_d):
        self.log_info(f"Path does not exist. Creating {_d}...")
        _res = OS.makedirs(_d)
        _dir_created[_d] = _res

    return _dir_created

  def validate_dir(self, *args, **kwargs):
    _dir = args[0] if len(args) > 0 else kwargs.get("dir")
    if not self.check_path(_dir):
      _res = self.create_dir(_dir, **kwargs)
      if _dir in _res.keys():
        self.log_info(f"Directory created.")
      else:
        self.log_info(f"Failed to create directory {_dir}.")
    return _dir

  def get_file_types(self, *args, **kwargs):
    _source = args[0] if len(args) > 0 else kwargs.get("source", getattr(self, "source", OS.getcwd()))
    _ext = args[1] if len(args) > 1 else kwargs.get("ext", getattr(self, "ext", ()))
    _matches = []

    if not all((_source, len(_ext) > 0)):
      return _matches

    for _root, _dir_names, _file_names in OS.walk(_source):
      for filename in _file_names:
        if filename.endswith(_ext):
          _matches.append(OS.path.join(_root, filename))
    return _matches

  def move(self, *args, **kwargs):
    _source = args[0] if len(args) > 0 else kwargs.get("source")

    if self.copy(*args, **kwargs):
      return self.delete_path(_source)
    else:
      return False

  def copy(self, *args, **kwargs):
    _source = args[0] if len(args) > 0 else kwargs.get("source")
    _destination = args[1] if len(args) > 1 else kwargs.get("destination")

    if not all([_source, _destination]):
      self.log_info(f"Source or Destination is not specified.")
      return False

    self.validate_dir(OS.path.dirname(_destination))

    self.log_info(f"Copying... {_source} to {_destination}.")
    SHUTIL.copyfile(_source, _destination)
    return self.check_path(_destination)

  def ext(self, *args, **kwargs):
    """ Returns File Extension """
    _file_path = args[0] if len(args) > 0 else kwargs.get("file_path")
    _num_ext = args[1] if len(args) > 1 else kwargs.get("num_ext", 1)
    _delimiter = args[2] if len(args) > 2 else kwargs.get("delimiter", ".")

    _file_path = OS.path.basename(_file_path)
    _file_path = _file_path.rsplit(_delimiter, _num_ext)
    _file_path = f"{_delimiter}".join(_file_path[-_num_ext:])
    return _file_path

  def change_ext(self, *args, **kwargs):
    _fp = args[0] if len(args) > 0 else kwargs.get("file")
    _to = args[1] if len(args) > 1 else kwargs.get("to")
    _from = args[2] if len(args) > 2 else kwargs.get("from")
    _num_ext = args[3] if len(args) > 3 else kwargs.get("num_ext", 1)

    _current_ext = self.ext(_fp, _num_ext)

    if _from is not None:
      if _current_ext == _from:
        _f_wo_ext = self.filename(_fp, with_dir = True, num_ext = _num_ext)
      else:
        WARN("From and Current extensions are not same.")
        return _fp
    else:
      _f_wo_ext = self.filename(_fp, with_dir = True, num_ext = _num_ext)

    return ".".join((_f_wo_ext, _to))

  def get_parts(self, *args, **kwargs):
    _text = args[0] if len(args) > 0 else kwargs.get("text")
    _position = args[1] if len(args) > 1 else kwargs.get("position", -3)
    _delimiter = args[2] if len(args) > 2 else kwargs.get("delimiter", "/")

    _text = _text.split(_delimiter)
    return _text[int(_position)] if abs(int(_position)) <= len(_text) else _text[-1]

  def delete_path(self, *args, **kwargs):
    _path = args[0] if len(args) > 0 else kwargs.get("path")

    if self.check_path(_path) and OS.path.isfile(_path):
      self.log_info(f"Deleting {_path}.")
      OS.remove(_path)
      return True
    self.log_error(f"{_path} is either a dir or doesn't exist.")
    return False

  def log_error(self, *args, **kwargs):
    return self.log(*args, **kwargs)

  def log_info(self, *args, **kwargs):
    return self.log(*args, **kwargs)

  def log(self, *args, **kwargs):
    for _message in args:
      print(_message)