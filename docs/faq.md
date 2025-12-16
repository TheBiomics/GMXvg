# ❓ Frequently Asked Questions (FAQ)

## 🚀 Getting Started

### Q: What is GMXvg and who is it for?
**A:** GMXvg is a tool that converts GROMACS molecular dynamics simulation data (.xvg files) into publication-ready plots. It's designed for researchers, students, and anyone working with GROMACS simulation data.

### Q: Do I need to know programming to use GMXvg?
**A:** Not at all! GMXvg works with simple command-line commands:
```bash
gmxvg
```

### Q: What are .xvg files?
**A:** XVG files are text files containing numerical data from GROMACS molecular dynamics simulations. They track things like:
- Structural changes (RMSD, RMSF)
- Energy changes over time
- Temperature and pressure
- Molecular interactions

## 🔧 Installation & Setup

### Q: How do I install GMXvg?
**A:** Simply run:
```bash
pip install gmxvg
```

### Q: GMXvg won't install. What should I do?
**A:** Try these steps:
1. Update pip: `pip install --upgrade pip`
2. Install with user flag: `pip install --user gmxvg`
3. Check Python version: `python --version` (need 3.6+)
4. On some systems, use `pip3` instead of `pip`

### Q: I get "command not found" when running gmxvg
**A:** This usually means:
1. GMXvg isn't installed properly - try reinstalling
2. It's not in your PATH - try `python -m gmxvg` instead
3. You're using the wrong terminal/command prompt

## 📊 Using GMXvg

### Q: How do I create my first plot?
**A:** Navigate to your folder with .xvg files and run:
```bash
gmxvg
```

### Q: My plots look strange/wrong. What should I do?
**A:**
1. Check your .xvg file in a text editor - is it formatted correctly?
2. Look at the axis labels - do they make sense?
3. Try different output formats: `gmxvg -e png`
4. Compare with example plots to see if yours are reasonable

### Q: GMXvg says "No .xvg files found"
**A:** Check that:
- You're in the right directory (`ls *.xvg` or `dir *.xvg`)
- Files have the .xvg extension
- Use `-b /path/to/files` to specify a different directory

### Q: Can I analyze files in multiple folders?
**A:** Yes! Use:
```bash
gmxvg -md folder1 folder2 folder3
```

### Q: How do I create high-quality plots for publication?
**A:** Use:
```bash
gmxvg -d 600 -e png pdf svg
```
This creates 600 DPI plots in multiple formats.

## 📈 Understanding Results

### Q: What does RMSD tell me?
**A:** RMSD (Root Mean Square Deviation) measures how much your molecule's structure changes over time:
- **Low values (0.1-0.3 nm)**: Structure is stable
- **High values (>0.5 nm)**: Large structural changes
- **Plateaus**: Structure has stabilized
- **Continuous increase**: Structure may be unfolding

### Q: How do I know if my simulation is good quality?
**A:** Look for:
- **RMSD that levels off** (reaches equilibrium)
- **Energy that stabilizes** (not continuously changing)
- **Temperature close to target** (within ±10K)
- **Smooth curves** (not jagged or spiky)

### Q: What's the difference between RMSD and RMSF?
**A:**
- **RMSD**: How much the whole structure moves over time
- **RMSF**: How much each part of the structure fluctuates
- Think of RMSD as "building sway" and RMSF as "which floors shake the most"

### Q: My plots look strange/wrong. What should I do?
**A:**
1. Try enhanced mode: `gmxvg --enhanced`
2. Check your .xvg file in a text editor - is it formatted correctly?
3. Look at the axis labels - do they make sense?
4. Compare with example plots to see if yours are reasonable

## 🎨 Customization

### Q: Can I change colors, fonts, or styles?
**A:** Currently, GMXvg uses smart defaults. For advanced customization, you can:
1. Use the Python API for full control
2. Edit the output files with image editing software
3. Request specific features on GitHub

### Q: How do I create plots for presentations vs. publications?
**A:**
- **Presentations**: `gmxvg -d 300 -e png` (clear, not too large)
- **Publications**: `gmxvg -d 600 -e png pdf svg` (high quality, multiple formats)
- **Quick analysis**: `gmxvg -d 150 -e jpg` (fast, small files)

### Q: Can I merge data from multiple simulations?
**A:** Yes! Use merge patterns:
```bash
gmxvg --merge-patterns "*rmsd*.xvg" "*energy*.xvg"
```

## 🐛 Troubleshooting

### Q: I get import errors when using Python
**A:** Install missing dependencies:
```bash
pip install matplotlib pandas numpy
```

### Q: Plots are created but they're blank
**A:** This usually means:
- Your .xvg file is empty or corrupted
- The data format isn't recognized
- Try opening the .xvg file in a text editor to check the content

### Q: GMXvg is very slow
**A:**
- Use lower DPI for testing: `-d 150`
- Process fewer files at once
- Check if you have enough disk space
- Close other programs that might be using resources

### Q: Can I run GMXvg on a cluster/server?
**A:** Yes, but you may need to:
- Use `matplotlib.use('Agg')` backend for no-display environments
- Install X11 forwarding for remote display
- Run in batch mode with scripts

## 💡 Advanced Usage

### Q: Can I use GMXvg in my own Python scripts?
**A:** Absolutely! Here's a simple example:
```python
from gmxvg import GMXvg

# Create analyzer
plotter = GMXvg(path_base="/path/to/files")
plotter.export_xvg()
```

### Q: How do I automate analysis for many simulations?
**A:** Create a script:
```bash
#!/bin/bash
for dir in sim1 sim2 sim3; do
    cd $dir
    gmxvg
    cd ..
done
```

### Q: Can I export the raw data?
**A:** Yes! Use:
```bash
gmxvg --flag-export-csv yes
```
This creates a CSV file with all the numerical data.

## 🤝 Getting More Help

### Q: Where can I get additional help?
**A:**
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Full reference at [link]
- **Community Forum**: Ask questions and share knowledge
- **Email Support**: For urgent issues

### Q: How can I contribute to GMXvg?
**A:** We welcome contributions!
- Report bugs and suggest features
- Share example files and use cases
- Improve documentation
- Submit code improvements
- Help other users in the community

### Q: Is GMXvg free?
**A:** Yes! GMXvg is open source and completely free to use for academic, commercial, or personal projects.

---

**Don't see your question here?**
- Check the [Interactive Tutorial](notebook.ipynb) for hands-on examples
- Ask on our [Community Forum](link) for personalized help
- Report issues on [GitHub](link) if you think you've found a bug
