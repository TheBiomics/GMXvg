[![PyPI Downloads](https://static.pepy.tech/badge/gmxvg)](https://pepy.tech/projects/gmxvg)

# 🧬 GMXvg: GROMACS .xvg File Plotting Tool

**Transform your GROMACS simulation data into publication-ready plots**

GMXvg is a command-line utility designed for converting and plotting GROMACS XVG files. It simplifies the process of handling XVG files by automatically discovering all XVG files in the current or subdirectories and converting them to specified file formats, with JPG as the default format. Additionally, GMXvg logs the summary of plots in a CSV file, providing quick access to plot values along with their standard deviation.

## 🌟 Features

- **Automatic discovery** - Finds all .xvg files in directories
- **Multiple formats** - Export to JPG, PNG, PDF, SVG, and more
- **Batch processing** - Analyze hundreds of files at once
- **Statistical summaries** - Automatic calculation of means and standard deviations
- **Customizable** - Full control over plot appearance and output quality
- **Cross-platform** - Can be installed and used on Windows, MacOS, and Linux

## 🚀 Quick Start (3 Easy Steps!)

### Step 1: Install
```bash
pip install gmxvg
```

### Step 2: Check it works
```bash
gmxvg --version
```

### Step 3: Create your first plot
```bash
# If you have .xvg files in your current folder:
gmxvg

# Or specify a folder:
gmxvg -b /path/to/your/xvg/files
```

That's it! 🎉 Your plots will be created automatically.

## 📊 What Can You Analyze?

GMXvg works with all standard GROMACS output files including:

| File Type | Description |
|-----------|-------------|
| **RMSD** | Root Mean Square Deviation - structural stability |
| **RMSF** | Root Mean Square Fluctuation - flexibility analysis |
| **Energy** | Potential, kinetic, and total energy plots |
| **Temperature** | System temperature monitoring |
| **Pressure** | System pressure analysis |
| **Hydrogen Bonds** | Molecular interaction analysis |

## 💡 Examples

### Basic Usage
```bash
# Plot all .xvg files in current directory
gmxvg

# Plot files in a specific directory
gmxvg -b /path/to/simulation/results

# Create high-resolution plots for publication
gmxvg -d 600 -e png pdf

# Plot multiple directories at once
gmxvg -md /path/to/folder1 /path/to/folder2 /path/to/folder3
```

## 📚 Learning Resources

- **[Interactive Tutorial](docs/notebook.ipynb)** - Hands-on examples in Jupyter notebook
- **[FAQ](docs/faq.md)** - Common questions and answers

## 🏥 Troubleshooting

### Common Issues

**"No .xvg files found"**
- Make sure you're in the right directory
- Check if files have the .xvg extension
- Use `-b` to specify the correct path or start terminal from the directory containing your graphs

**"Import error"**
- Try: `pip install --upgrade gmxvg`
- Make sure you have Python 3.6+

**"Plots look strange"**
- Check if your .xvg files are properly formatted

### Getting Help

- 💬 **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/GMXvg/issues)
- 📖 **Documentation**: [Full documentation](https://gmxvg.readthedocs.io)

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Report bugs** - Found something broken? Let us know!
2. **Suggest features** - What would make GMXvg better for you?
3. **Share examples** - Help others by sharing your use cases
4. **Improve documentation** - Help make GMXvg even more user-friendly

## 🙏 Acknowledgments

- Built for the molecular dynamics community
- Powered by [python](https://python.org), [matplotlib](https://matplotlib.org/) and [pandas](https://pandas.pydata.org/)
- Inspired by the need to make scientific data analysis accessible to everyone

## 💡 Inspiration

This project is our small contribution to the molecular dynamics community. We believe that powerful data analysis tools should be accessible to everyone - from students learning computational biology to experienced researchers publishing groundbreaking papers. By simplifying the process of creating publication-ready plots from GROMACS data, we hope to save valuable time that can be better spent on scientific discovery.


---

**Ready to start analyzing your molecular dynamics data?**
[Install GMXvg now](#-quick-start-3-easy-steps) and create your first plot in under 2 minutes! 🚀
