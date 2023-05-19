import ezdxf
import sys

from line import Line
from pathlib import Path
from ezdxf.sections.table import LayerTable
from point import Point


class DXF_Editor:

    def __init__(self, file_path):
        try:
            self.dxf_path = Path(file_path)
            self.doc = ezdxf.readfile(self.dxf_path)
            self.msp = self.doc.modelspace()
        except IOError:
            print(f"Not a DXF file or a generic I/O error.")
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file.")
            sys.exit(2)

    def set_lines(self, write_to):
        lines = self.msp.query("LINE")
        collected_lines = []
        with open(write_to, "w") as f:
            for line in lines:
                # Write to file the line coordinates
                line_start = line.dxf.start
                line_end = line.dxf.end
                start = Point(line_start[0], line_start[1])
                end = Point(line_end[0], line_end[1], False)
                new_line = Line(start, end)
                collected_lines.append(new_line)
                f.write("Start %s " % line_start)
                f.write(" End %s\n" % line_end)
        self.collected_lines = collected_lines
        return self.collected_lines
