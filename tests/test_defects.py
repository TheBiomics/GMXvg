import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from gmxvg.GMXvg import GMXvg


def test_out_of_range_dpi_raises_error():
    """Defect 1: out-of-range DPI should raise ValueError, not silently produce zero plots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a valid .xvg file
        xvg_content = """@    title "Test"
@    xaxis  label "Time (ps)"
@    yaxis  label "Distance (nm)"
@    s0 legend "Test"
0 1.0
1 2.0
2 3.0
"""
        xvg_file = Path(tmpdir) / "test.xvg"
        xvg_file.write_text(xvg_content)

        # Test with out-of-range DPI (50 < 72) - should raise when calling _get_export_dpi directly
        g = GMXvg(path_base=tmpdir, export_dpi=["50"], flag_export_plot="Y")
        with pytest.raises(ValueError, match="No valid DPI values"):
            g._get_export_dpi()

        # Test with non-numeric DPI
        g = GMXvg(path_base=tmpdir, export_dpi=["abc"], flag_export_plot="Y")
        with pytest.raises(ValueError, match="No valid DPI values"):
            g._get_export_dpi()

        # Valid DPI should work
        g = GMXvg(path_base=tmpdir, export_dpi=["300"], flag_export_plot="Y")
        dpis = g._get_export_dpi()
        assert dpis == ["300"]


def test_batch_survives_malformed_file():
    """Defect 2: one malformed .xvg should not abort the whole batch - batch completes without crashing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Valid .xvg file
        valid_content = """@    title "Valid"
@    xaxis  label "Time (ps)"
@    yaxis  label "Distance (nm)"
@    s0 legend "Test"
0 1.0
1 2.0
2 3.0
"""
        # Malformed .xvg file - column/legend mismatch (logs error but doesn't raise)
        malformed_content = """@    title "Malformed"
@    xaxis  label "Time (ps)"
@    yaxis  label "Distance (nm)"
@    s0 legend "A"
@    s1 legend "B"
@    s2 legend "C"
0 1.0 2.0 3.0 4.0
1 2.0 3.0 4.0 5.0
"""
        valid_file = Path(tmpdir) / "valid.xvg"
        malformed_file = Path(tmpdir) / "malformed.xvg"
        valid_file.write_text(valid_content)
        malformed_file.write_text(malformed_content)

        g = GMXvg(path_base=tmpdir, export_dpi=["300"], flag_export_plot="Y", flag_export_csv="N")
        # Should not raise - batch should complete (logs warning for malformed file)
        g.plot()

        # Verify valid file produced output
        output_files = list(Path(tmpdir).glob("*300dpi*"))
        assert len(output_files) > 0, "Valid file should produce plot output"

        # Batch completed without crashing - that's the key assertion
        # (malformed file may produce a plot with default column names; the fix ensures no crash)


def test_escape_codes_convert():
    """Multi-char subscripts, superscripts and font switches must all be converted."""
    from gmxvg.GMXvg import GMXvg

    g = GMXvg()
    assert g._clean_text(r"Rg\sXY\N") == "Rg$_XY$"      # multi-char subscript
    assert g._clean_text(r"Rg\sX\N") == "Rg$_X$"        # single-char still works
    assert g._clean_text(r"nm\S2\N") == "nm$^2$"        # superscript
    assert g._clean_text(r"\f{Symbol}alpha") == "alpha"  # font switch stripped


def test_csv_output_filename_flag():
    """`-o NAME` must name the CSV. Regression: -o was registered variadic ("*"),
    yielding a list where a scalar was expected -> TypeError aborting the whole run."""
    with tempfile.TemporaryDirectory() as tmpdir:
        xvg = Path(tmpdir) / "valid.xvg"
        xvg.write_text(
            '@    title "Test"\n'
            '@    xaxis  label "Time (ps)"\n'
            '@    yaxis  label "Distance (nm)"\n'
            '@    s0 legend "Test"\n'
            "0 1.0\n1 2.0\n2 3.0\n"
        )
        proc = subprocess.run(
            [sys.executable, "-m", "gmxvg", "-b", tmpdir, "-e", "jpg",
             "-d", "300", "-c", "Y", "-o", "custom-name.csv"],
            capture_output=True, text=True, timeout=180,
        )
        assert proc.returncode == 0, proc.stderr
        assert "TypeError" not in proc.stderr, proc.stderr
        out = Path(tmpdir) / "custom-name.csv"
        assert out.exists(), f"expected {out}; stderr={proc.stderr}"
        assert len(out.read_text().strip().splitlines()) > 1