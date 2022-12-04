#!/usr/bin/env python

import argparse as ARGUMENT
import os as OS

from gmxvg import GMXVGHelper

def main():
  print(f"{GMXVGHelper.name} v{GMXVGHelper.version} {GMXVGHelper.release_date}")
  print("=" * 80)
  print(f"Other available options are:")
  print(f"csv_filename, csv_filepath, path_base, path_move, path_copy, pattern_xvg, merge_patterns,")
  print(f"export_ext, dpi, flag_plot_mean, flag_plot_std, flag_export_csv, flag_export_plot, output_files")
  print("=" * 80)
  _plotter = GMXVGHelper()
  _parser = ARGUMENT.ArgumentParser(prog=GMXVGHelper.name)

  _parser.add_argument('-b', '--path_base', nargs = None, default = OS.getcwd(), help = 'Provide base directory. Default: %(default)s.')
  _parser.add_argument('-e', '--export_ext', nargs = "*", default = ["jpg"], help = 'Output formats. Default: %(default)s.')
  _parser.add_argument('-d', '--dpi', nargs = "*", default = [300], help = 'Output quality. Default: %(default)s.')

  _reg_args, _unreg_args = _parser.parse_known_args()
  _reg_args = vars(_reg_args)
  _reg_args = {_k: _reg_args[_k] for _k in _reg_args.keys() if _reg_args[_k] is not None}

  _params = _plotter.unregistered_arg_parser(_unreg_args)
  _params.update(_reg_args)
  _plotter.export_xvg(**_params)

if __name__ == "__main__":
  main()
