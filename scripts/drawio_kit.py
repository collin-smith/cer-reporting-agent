"""Shared draw.io helpers for the article figures: AWS4 styles and colours, and a Diagram that collects cells and
writes a .drawio file. Same styles as make_agent_workflow_diagram.py and make_architecture_diagram.py."""

import pathlib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

PTS = (
    "points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],"
    "[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];"
)
ICON = (
    "sketch=0;" + PTS + "outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;dashed=0;"
    "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
    "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};"
)
RES = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=none;dashed=0;"
    "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
    "pointerEvents=1;shape=mxgraph.aws4.{icon};"
)
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;fontSize=11;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;"
    "arcSize=6;fontColor=#232F3E;{extra}"
)
EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;"
    "endArrow=block;endFill=1;strokeColor=#545B64;fontColor=#232F3E;labelBackgroundColor=#ffffff;{extra}"
)

# AWS category colours (from draw.io's Sidebar-AWS4.js)
STORAGE, COMPUTE, DATABASE, APPINT, AI, MGMT = "#7AA116", "#ED7100", "#C925D1", "#E7157B", "#01A88D", "#E7157B"
FINANCE = "#7AA116"
AGENT_FILL, AGENT_STROKE = "#E6F6F7", "#01A88D"  # agents: AI/ML teal
TOOL_FILL = "#FFFFFF"
NOTE_FILL, NOTE_STROKE = "#F5F5F5", "#545B64"
ESC_STROKE = "#DD344C"
GROUP = (
    "sketch=0;outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr};verticalAlign=top;align=left;spacingLeft=30;{extra}"
)
CODE_FILL, CODE_STROKE = "#FFFFFF", "#232F3E"  # our own Python code, not an AWS service

CHECK_FILL, CHECK_STROKE = "#EEF4FB", "#2A78D6"  # the checks: one style, distinct from the system
CHECK = f"fillColor={CHECK_FILL};strokeColor={CHECK_STROKE};strokeWidth=2;"
CENTER = "align=center;spacingLeft=0;verticalAlign=middle;"
TITLE = "text;html=1;align=left;verticalAlign=top;fontSize=16;fontColor=#232F3E;whiteSpace=wrap;"


class Diagram:
    def __init__(self):
        self.cells: list[str] = []

    def add(self, cid, value, style, x, y, w, h):
        self.cells.append(
            f'<mxCell id="{cid}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" '
            f'parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def box(self, cid, value, x, y, w, h, fill="none", stroke=NOTE_STROKE, extra=""):
        self.add(cid, value, BOX.format(extra=f"fillColor={fill};strokeColor={stroke};{extra}"), x, y, w, h)

    def icon(self, cid, label, fill, name, x, y, size=56):
        self.add(cid, label, ICON.format(fill=fill, icon=name), x, y, size, size)

    def res(self, cid, label, fill, name, x, y, size=48):
        self.add(cid, label, RES.format(fill=fill, icon=name), x, y, size, size)

    def group(self, cid, label, gr, extra, x, y, w, h):
        self.add(cid, label, GROUP.format(gr=gr, extra=extra), x, y, w, h)

    def edge(self, cid, src, dst, label="", dashed=False, extra="", points=()):
        style = EDGE.format(extra=("dashed=1;" if dashed else "") + extra)
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points) + "</Array>"
        self.cells.append(
            f'<mxCell id="{cid}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{src}" '
            f'target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )

    def write(self, path, name: str, width: int, height: int) -> None:
        xml = (
            f'<mxfile host="app.diagrams.net"><diagram id="d" name="{escape(name)}"><mxGraphModel dx="{width}" '
            f'dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            f'page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" background="#ffffff" math="0" '
            'shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(self.cells)
            + "</root></mxGraphModel></diagram></mxfile>"
        )
        ET.fromstring(xml)  # fails loudly if malformed
        pathlib.Path(path).write_text(xml, encoding="utf-8")
        print("wrote", path, len(self.cells), "cells")
