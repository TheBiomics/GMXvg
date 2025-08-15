from .__metadata__ import __version__, __description__, __build__, __name__
from .GMXvg import GMXvg

def xvgplot_cli():
  _m = GMXvg()
  _m.plot_cli()
