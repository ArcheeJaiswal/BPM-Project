"""
========================================================================================
BPMN 2.0 Organizational Swimlane Vector Renderer & Layout Engine
========================================================================================
Automatic layout algorithm specifically engineered for horizontal BPMN 2.0 swimlanes:
  - Dynamic topological column (rank) assignment for strictly left-to-right control flows.
  - Dynamic vertical track allocation within organizational lanes.
  - Dynamic calculation of swimlane heights and diagram width based on workflow complexity.
  - Orthogonal Manhattan connector routing with obstacle avoidance.
  - Gateway port separation: distinct diamond vertices (North, East, South) for split/join paths.
  - Standard BPMN 2.0 vector markers (User, Service, Send, Receive, Manual) without duplicate emojis.
  - Distinct BPMN 2.0 message flows (dashed line with open circle start and open triangular arrowhead).
  - Collision-free connector label pill badges.
========================================================================================
"""

from typing import Dict, Any, List, Tuple, Optional
import html
import re

# Regex to strip emoji characters from text labels to eliminate duplication
EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27ff]|[\u2300-\u23ff]|[\u2b50]|[\u200d]|[\ufe0f]",
    flags=re.UNICODE
)

def clean_text_label(text: str) -> str:
    """Strips leading/trailing emojis and cleans whitespace for publication-grade typography."""
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned = EMOJI_PATTERN.sub("", line).strip()
        if cleaned:
            cleaned_lines.append(cleaned)
    return "\n".join(cleaned_lines) if cleaned_lines else text.strip()


class BPMNSwimlaneEngine:
    """
    Automated horizontal BPMN 2.0 Swimlane layout and orthogonal routing engine.
    Calculates coordinates, dimensions, tracks, and non-overlapping connector paths dynamically.
    """

    def __init__(
        self,
        pool_title: str,
        lanes: List[Dict[str, Any]],
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        top_pool: Optional[Dict[str, Any]] = None,
        col_gap: int = 75,
        track_gap: int = 24
    ):
        self.pool_title = pool_title
        self.raw_lanes = lanes
        self.raw_nodes = nodes
        self.raw_edges = edges
        self.raw_top_pool = top_pool
        self.col_gap = col_gap
        self.track_gap = track_gap

        # Geometry specs
        self.pool_header_w = 40
        self.lane_header_w = 48
        self.header_total_w = self.pool_header_w + self.lane_header_w
        self.start_x = self.header_total_w + 24

        self.task_w = 155
        self.task_h = 54
        self.gw_size = 40
        self.event_r = 16

        # Calculated layout properties
        self.nodes_by_id: Dict[str, Dict[str, Any]] = {}
        self.lanes_by_id: Dict[str, Dict[str, Any]] = {}
        self.columns: Dict[str, int] = {}
        self.node_tracks: Dict[str, int] = {}
        self.node_boxes: Dict[str, Dict[str, Any]] = {}
        self.lane_geometry: Dict[str, Dict[str, Any]] = {}
        self.col_channels: Dict[int, float] = {}
        self.top_pool_y = 14
        self.top_pool_h = 95
        self.primary_pool_y = 127
        self.total_width = 2400
        self.total_height = 900

    def layout(self) -> List[Dict[str, Any]]:
        """Executes full automated layout pipeline and returns routed edges."""
        # 1. Clean labels and index nodes
        for n in self.raw_nodes:
            n_clean = dict(n)
            n_clean["label"] = clean_text_label(n.get("label", ""))
            self.nodes_by_id[n["id"]] = n_clean

        if self.raw_top_pool and "nodes" in self.raw_top_pool:
            for n in self.raw_top_pool["nodes"]:
                n_clean = dict(n)
                n_clean["label"] = clean_text_label(n.get("label", ""))
                n_clean["pool"] = "top_pool"
                self.nodes_by_id[n["id"]] = n_clean

        for l in self.raw_lanes:
            self.lanes_by_id[l["id"]] = l

        # 2. Assign topological columns (horizontal progression)
        self._assign_columns()

        # 3. Assign vertical tracks within lanes & dynamically calculate heights
        self._assign_tracks_and_lane_heights()

        # 4. Compute exact non-overlapping (x, y) coordinates
        self._compute_node_coordinates()

        # 5. Route all connectors with obstacle avoidance
        routed_edges = self._route_edges()
        return routed_edges

    def _assign_columns(self):
        """Topological rank assignment ensuring Left-to-Right progression."""
        in_degree = {nid: 0 for nid in self.nodes_by_id}
        adj = {nid: [] for nid in self.nodes_by_id}

        for e in self.raw_edges:
            src, dst = e["from"], e["to"]
            if e.get("dashed") or e.get("loopback") or e.get("violation"):
                continue  # skip feedback and cross-pool message flows during DAG ranking
            if src in adj and dst in adj:
                adj[src].append(dst)
                in_degree[dst] += 1

        ranks = {}
        queue = [nid for nid, deg in in_degree.items() if deg == 0 and self.nodes_by_id[nid].get("pool") != "top_pool"]
        for nid in queue:
            ranks[nid] = self.nodes_by_id[nid].get("col", 0)

        changed = True
        iterations = 0
        while changed and iterations < 50:
            changed = False
            iterations += 1
            for src, targets in adj.items():
                if src in ranks:
                    for dst in targets:
                        curr = ranks.get(dst, 0)
                        explicit_col = self.nodes_by_id[dst].get("col")
                        target_rank = explicit_col if explicit_col is not None else ranks[src] + 1
                        if target_rank > curr:
                            ranks[dst] = target_rank
                            changed = True

        # Assign portal nodes columns aligned with corresponding provider nodes
        for e in self.raw_edges:
            src, dst = e["from"], e["to"]
            if e.get("dashed"):
                if src in self.nodes_by_id and dst in self.nodes_by_id:
                    s_node = self.nodes_by_id[src]
                    d_node = self.nodes_by_id[dst]
                    if s_node.get("pool") == "top_pool" and d_node.get("pool") != "top_pool":
                        if dst in ranks:
                            ranks[src] = self.nodes_by_id[src].get("col", ranks[dst])
                    elif d_node.get("pool") == "top_pool" and s_node.get("pool") != "top_pool":
                        if src in ranks:
                            ranks[dst] = self.nodes_by_id[dst].get("col", ranks[src])

        for nid, n in self.nodes_by_id.items():
            if nid not in ranks:
                ranks[nid] = n.get("col", 0)

        self.columns = ranks

    def _assign_tracks_and_lane_heights(self):
        """Dynamically computes vertical tracks per lane and dynamic lane heights."""
        lane_nodes = {l["id"]: [] for l in self.raw_lanes}
        top_pool_nodes = []

        for nid, n in self.nodes_by_id.items():
            if n.get("pool") == "top_pool":
                top_pool_nodes.append(nid)
            else:
                lane_id = n.get("lane")
                if lane_id in lane_nodes:
                    lane_nodes[lane_id].append(nid)

        self.node_tracks = {}
        for lane_id, nids in lane_nodes.items():
            col_buckets = {}
            for nid in nids:
                c = self.columns.get(nid, 0)
                col_buckets.setdefault(c, []).append(nid)

            max_tracks = 1
            for c, bucket in col_buckets.items():
                if len(bucket) > max_tracks:
                    max_tracks = len(bucket)
                for track_idx, nid in enumerate(bucket):
                    hint = self.nodes_by_id[nid].get("track")
                    self.node_tracks[nid] = hint if hint is not None else track_idx

            pad_top = 24
            pad_bottom = 24
            lane_h = pad_top + max_tracks * self.task_h + (max_tracks - 1) * self.track_gap + pad_bottom
            lane_h = max(lane_h, 120)
            self.lane_geometry[lane_id] = {
                "tracks": max_tracks,
                "height": lane_h
            }

        for nid in top_pool_nodes:
            self.node_tracks[nid] = self.nodes_by_id[nid].get("track", 0)
        self.top_pool_h = 95

    def _compute_node_coordinates(self):
        """Computes exact non-overlapping (x, y) coordinates for all elements."""
        max_col = max(self.columns.values()) if self.columns else 0
        col_widths = {}
        for c in range(max_col + 1):
            col_nodes = [nid for nid, col in self.columns.items() if col == c]
            w_max = 0
            for nid in col_nodes:
                ntype = self.nodes_by_id[nid].get("type", "task")
                w = self.task_w if ntype == "task" else (self.event_r * 2 if "event" in ntype else self.gw_size)
                if w > w_max:
                    w_max = w
            col_widths[c] = max(w_max, self.gw_size)

        col_x = {}
        curr_x = self.start_x
        for c in range(max_col + 1):
            col_x[c] = curr_x
            self.col_channels[c] = curr_x + col_widths[c] + self.col_gap / 2
            curr_x += col_widths[c] + self.col_gap

        self.total_width = curr_x + 60

        curr_y = 14
        if self.raw_top_pool:
            self.top_pool_y = curr_y
            curr_y += self.top_pool_h + 18

        self.primary_pool_y = curr_y
        for l in self.raw_lanes:
            lid = l["id"]
            lh = self.lane_geometry[lid]["height"]
            self.lane_geometry[lid]["y"] = curr_y
            curr_y += lh

        self.total_height = curr_y + 20

        for nid, n in self.nodes_by_id.items():
            ntype = n.get("type", "task")
            nw = self.task_w if ntype == "task" else (self.event_r * 2 if "event" in ntype else self.gw_size)
            nh = self.task_h if ntype == "task" else (self.event_r * 2 if "event" in ntype else self.gw_size)

            c = self.columns.get(nid, 0)
            cx = col_x[c] + (col_widths[c] - nw) / 2

            track = self.node_tracks.get(nid, 0)
            if n.get("pool") == "top_pool":
                cy = self.top_pool_y + 22 + track * (self.task_h + self.track_gap) + (self.task_h - nh) / 2
            else:
                lid = n.get("lane")
                ly = self.lane_geometry[lid]["y"]
                cy = ly + 24 + track * (self.task_h + self.track_gap) + (self.task_h - nh) / 2

            self.node_boxes[nid] = {
                "id": nid, "x": cx, "y": cy, "w": nw, "h": nh,
                "cx": cx + nw / 2, "cy": cy + nh / 2,
                "left": cx, "right": cx + nw,
                "top": cy, "bottom": cy + nh,
                "type": ntype
            }

    def _segment_hits_box(self, p1: Tuple[float, float], p2: Tuple[float, float], box: Dict[str, Any]) -> bool:
        """Determines if a rectilinear segment intersects an obstacle bounding box."""
        x1, y1 = p1
        x2, y2 = p2
        bl, bt, br, bb = box["left"], box["top"], box["right"], box["bottom"]
        if y1 == y2:
            if bt < y1 < bb:
                minx, maxx = min(x1, x2), max(x1, x2)
                if minx < br and maxx > bl:
                    return True
        elif x1 == x2:
            if bl < x1 < br:
                miny, maxy = min(y1, y2), max(y1, y2)
                if miny < bb and maxy > bt:
                    return True
        return False

    def _path_has_collision(self, pts: List[Tuple[float, float]], ignore_nodes: Tuple[str, ...]) -> bool:
        """Determines if any segment of an orthogonal polyline hits any node obstacle."""
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            for nid, box in self.node_boxes.items():
                if nid in ignore_nodes:
                    continue
                if self._segment_hits_box(p1, p2, box):
                    return True
        return False

    def _route_edges(self) -> List[Dict[str, Any]]:
        """Orthogonal Manhattan routing with obstacle avoidance and port separation."""
        routed = []
        for e in self.raw_edges:
            src_id, dst_id = e["from"], e["to"]
            if src_id not in self.node_boxes or dst_id not in self.node_boxes:
                continue

            src = self.node_boxes[src_id]
            dst = self.node_boxes[dst_id]
            label = clean_text_label(e.get("label", ""))
            is_dashed = e.get("dashed", False)
            is_violation = e.get("violation", False)

            # Gateway port separation (North, East, South)
            if "gateway" in src["type"]:
                if dst["cy"] < src["cy"] - 10:
                    start_pt = (src["cx"], src["top"])     # North port for upper branch
                elif dst["cy"] > src["cy"] + 10:
                    start_pt = (src["cx"], src["bottom"])  # South port for lower branch
                else:
                    start_pt = (src["right"], src["cy"])   # East port for straight branch
            else:
                if is_dashed and abs(src["cx"] - dst["cx"]) < 60:
                    start_pt = (src["cx"], src["bottom"] if src["cy"] < dst["cy"] else src["top"])
                else:
                    start_pt = (src["right"], src["cy"])

            # Destination Gateway port separation
            if "gateway" in dst["type"]:
                if src["cy"] < dst["cy"] - 10:
                    end_pt = (dst["cx"], dst["top"])       # Enter North port
                elif src["cy"] > dst["cy"] + 10:
                    end_pt = (dst["cx"], dst["bottom"])    # Enter South port
                else:
                    end_pt = (dst["left"], dst["cy"])      # Enter West port
            else:
                if is_dashed and abs(src["cx"] - dst["cx"]) < 60:
                    end_pt = (dst["cx"], dst["top"] if src["cy"] < dst["cy"] else dst["bottom"])
                else:
                    end_pt = (dst["left"], dst["cy"])

            # Compute route
            if e.get("waypoints"):
                pts = e["waypoints"]
            elif abs(start_pt[1] - end_pt[1]) < 3 and start_pt[0] < end_pt[0]:
                pts = [start_pt, end_pt]
                if self._path_has_collision(pts, (src_id, dst_id)):
                    pts = self._route_around_obstacle(src, dst, start_pt, end_pt)
            elif abs(start_pt[0] - end_pt[0]) < 3:
                pts = [start_pt, end_pt]
                if self._path_has_collision(pts, (src_id, dst_id)):
                    pts = self._route_around_obstacle(src, dst, start_pt, end_pt)
            elif start_pt[0] < end_pt[0]:
                src_col = self.columns.get(src_id, 0)
                channel_x = self.col_channels.get(src_col, (start_pt[0] + end_pt[0]) / 2)

                if start_pt[0] == src["cx"]:
                    cand_pts = [start_pt, (start_pt[0], end_pt[1]), end_pt]
                elif end_pt[0] == dst["cx"]:
                    cand_pts = [start_pt, (end_pt[0], start_pt[1]), end_pt]
                else:
                    cand_pts = [start_pt, (channel_x, start_pt[1]), (channel_x, end_pt[1]), end_pt]

                if not self._path_has_collision(cand_pts, (src_id, dst_id)):
                    pts = cand_pts
                else:
                    pts = self._route_around_obstacle(src, dst, start_pt, end_pt)
            else:
                pts = self._route_loopback(src, dst, start_pt, end_pt)

            routed.append({
                "from": src_id, "to": dst_id,
                "label": label, "dashed": is_dashed, "violation": is_violation,
                "waypoints": pts, "label_pos": e.get("label_pos")
            })

        return routed

    def _route_around_obstacle(self, src: Dict[str, Any], dst: Dict[str, Any], start_pt: Tuple[float, float], end_pt: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Routes through obstacle-free horizontal and vertical channels."""
        src_col = self.columns.get(src["id"], 0)
        dst_col = self.columns.get(dst["id"], 0)
        ch_out = self.col_channels.get(src_col, src["right"] + 25)
        ch_in = self.col_channels.get(max(0, dst_col - 1), dst["left"] - 25)

        # Try corridor above src and dst
        bypass_y = min(src["top"], dst["top"]) - 18
        cand = [
            start_pt,
            (ch_out, start_pt[1]),
            (ch_out, bypass_y),
            (ch_in, bypass_y),
            (ch_in, end_pt[1]),
            end_pt
        ]
        if not self._path_has_collision(cand, (src["id"], dst["id"])):
            return cand

        # Try corridor below
        bypass_y = max(src["bottom"], dst["bottom"]) + 18
        cand = [
            start_pt,
            (ch_out, start_pt[1]),
            (ch_out, bypass_y),
            (ch_in, bypass_y),
            (ch_in, end_pt[1]),
            end_pt
        ]
        return cand

    def _route_loopback(self, src: Dict[str, Any], dst: Dict[str, Any], start_pt: Tuple[float, float], end_pt: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Routes feedback loopback flow via clear channel."""
        src_col = self.columns.get(src["id"], 0)
        dst_col = self.columns.get(dst["id"], 0)
        ch_in = self.col_channels.get(max(0, dst_col - 1), dst["left"] - 25)
        loop_y = max(src["bottom"], dst["bottom"]) + 24
        return [
            (src["cx"], src["bottom"]),
            (src["cx"], loop_y),
            (ch_in, loop_y),
            (ch_in, end_pt[1]),
            end_pt
        ]

    def render_svg(self, routed_edges: List[Dict[str, Any]]) -> str:
        """Renders complete publication-grade BPMN 2.0 SVG."""
        lanes_x = self.header_total_w + 14
        lanes_w = self.total_width - lanes_x - 24
        total_pool_h = self.total_height - self.primary_pool_y - 20

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.total_width} {self.total_height}" width="{self.total_width}" height="{self.total_height}" style="background-color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">',
            '<defs>',
            # Solid sequence flow arrowhead
            '  <marker id="sequence-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">',
            '    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#1E293B" />',
            '  </marker>',
            # Red violation sequence flow arrowhead
            '  <marker id="violation-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">',
            '    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#DC2626" />',
            '  </marker>',
            # Standard BPMN 2.0 message flow open arrowhead
            '  <marker id="message-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            '    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#FFFFFF" stroke="#475569" stroke-width="1.3" />',
            '  </marker>',
            # Standard BPMN 2.0 message flow start open circle
            '  <marker id="message-circle" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '    <circle cx="5" cy="5" r="3.2" fill="#FFFFFF" stroke="#475569" stroke-width="1.3" />',
            '  </marker>',
            '</defs>'
        ]

        # 1. Top Pool (Customer / Borrower Portal)
        if self.raw_top_pool:
            tp_title = self.raw_top_pool.get("title", "Customer Portal")
            tp_bg = self.raw_top_pool.get("bg", "#F0FDF4")
            # Pool border
            svg_parts.append(
                f'<rect x="14" y="{self.top_pool_y}" width="{self.total_width - 28}" height="{self.top_pool_h}" fill="{tp_bg}" stroke="#16A34A" stroke-width="2" rx="4" />'
            )
            # Left vertical rotated header
            svg_parts.append(
                f'<rect x="14" y="{self.top_pool_y}" width="{self.header_total_w}" height="{self.top_pool_h}" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.5" />'
            )
            svg_parts.append(
                f'<text x="-{self.top_pool_y + self.top_pool_h/2}" y="{14 + self.header_total_w/2 + 4}" transform="rotate(-90)" '
                f'text-anchor="middle" font-size="11.5" font-weight="bold" fill="#166534" letter-spacing="0.4px">{html.escape(tp_title)}</text>'
            )

        # 2. Primary Pool (Loan Provider)
        svg_parts.append(
            f'<rect x="14" y="{self.primary_pool_y}" width="{self.total_width - 28}" height="{total_pool_h}" fill="#FFFFFF" stroke="#0F172A" stroke-width="2" rx="4" />'
        )
        # Primary pool left header
        svg_parts.append(
            f'<rect x="14" y="{self.primary_pool_y}" width="{self.pool_header_w}" height="{total_pool_h}" fill="#F1F5F9" stroke="#0F172A" stroke-width="1.5" />'
        )
        svg_parts.append(
            f'<text x="-{self.primary_pool_y + total_pool_h/2}" y="{14 + self.pool_header_w/2 + 4}" transform="rotate(-90)" '
            f'text-anchor="middle" font-size="12" font-weight="bold" fill="#0F172A" letter-spacing="0.5px">'
            f'{html.escape(self.pool_title)}</text>'
        )

        # 3. Horizontal Lanes
        for i, lane in enumerate(self.raw_lanes):
            lid = lane["id"]
            ly = self.lane_geometry[lid]["y"]
            lh = self.lane_geometry[lid]["height"]
            bg = lane.get("bg", "#FFFFFF" if i % 2 == 0 else "#F8FAFC")
            title = lane.get("name", lid)

            # Lane background
            svg_parts.append(f'<rect x="{lanes_x}" y="{ly}" width="{lanes_w}" height="{lh}" fill="{bg}" stroke="none" />')
            # Lane left header
            svg_parts.append(
                f'<rect x="{14 + self.pool_header_w}" y="{ly}" width="{self.lane_header_w}" height="{lh}" fill="#FFFFFF" stroke="#334155" stroke-width="1.2" />'
            )
            svg_parts.append(
                f'<text x="-{ly + lh/2}" y="{14 + self.pool_header_w + self.lane_header_w/2 + 4}" transform="rotate(-90)" '
                f'text-anchor="middle" font-size="11" font-weight="600" fill="#1E293B">'
                f'{html.escape(title)}</text>'
            )
            # Lane divider line
            if i > 0:
                svg_parts.append(
                    f'<line x1="{lanes_x}" y1="{ly}" x2="{lanes_x + lanes_w}" y2="{ly}" stroke="#334155" stroke-width="1.2" />'
                )

        # 4. Render Edges (behind nodes)
        for e in routed_edges:
            svg_parts.append(self._render_edge_svg(e))

        # 5. Render Nodes (in front of edges)
        for nid, n in self.nodes_by_id.items():
            svg_parts.append(self._render_node_svg(nid))

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def _render_node_svg(self, nid: str) -> str:
        """Renders standard BPMN 2.0 task, gateway, or event with vector symbols and clean typography."""
        node = self.nodes_by_id[nid]
        box = self.node_boxes[nid]
        ntype = node.get("type", "task")
        task_type = node.get("task_type", "abstract")
        label = node.get("label", "")
        nx, ny, nw, nh = box["x"], box["y"], box["w"], box["h"]
        is_violation = node.get("is_violation", False)

        if ntype == "task":
            fill = node.get("fill", "#FFFFFF")
            stroke = "#DC2626" if is_violation else node.get("stroke", "#1E293B")
            stroke_w = 2.0 if is_violation else 1.5
            dash = 'stroke-dasharray="4,3"' if is_violation else ''

            # Standard BPMN Task Type vector icon in top-left corner
            icon_svg = self._get_bpmn_task_icon_svg(task_type, nx, ny)

            # Clean multi-line centered text
            lines = label.split("\n")
            line_height = 14
            start_text_y = ny + (nh - len(lines) * line_height) / 2 + 11
            text_spans = []
            for i, line in enumerate(lines):
                text_spans.append(f'<tspan x="{nx + nw/2}" y="{start_text_y + i * line_height}">{html.escape(line)}</tspan>')

            return (
                f'<g id="node_{nid}">'
                f'  <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="5" ry="5" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" {dash} />'
                f'  {icon_svg}'
                f'  <text text-anchor="middle" font-size="10.5" font-weight="500" fill="#0F172A">'
                f'    {"".join(text_spans)}'
                f'  </text>'
                f'</g>'
            )

        elif ntype.startswith("gateway"):
            cx, cy = box["cx"], box["cy"]
            hw = nw / 2
            hh = nh / 2
            pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"

            if "xor" in ntype:
                fill = "#FEF08A"
                stroke = "#CA8A04"
                sym_svg = f'<text x="{cx}" y="{cy + 6.5}" text-anchor="middle" font-size="20" font-weight="bold" fill="#854D0E">×</text>'
            elif "and" in ntype:
                fill = "#DBEAFE"
                stroke = "#2563EB"
                sym_svg = f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-size="22" font-weight="bold" fill="#1D4ED8">+</text>'
            elif "or" in ntype:
                fill = "#FEF3C7"
                stroke = "#D97706"
                sym_svg = f'<circle cx="{cx}" cy="{cy}" r="7.5" fill="none" stroke="#B45309" stroke-width="2.2" />'
            else:
                fill = "#FFFFFF"
                stroke = "#0F172A"
                sym_svg = ""

            subtext = f'<text x="{cx}" y="{ny - 8}" text-anchor="middle" font-size="10" font-weight="bold" fill="#1E293B">{html.escape(label)}</text>' if label else ''

            return (
                f'<g id="node_{nid}">'
                f'  <polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.8" />'
                f'  {sym_svg}'
                f'  {subtext}'
                f'</g>'
            )

        elif ntype == "start_event":
            cx, cy = box["cx"], box["cy"]
            r = self.event_r
            subtext = f'<text x="{cx}" y="{ny + r*2 + 13}" text-anchor="middle" font-size="9.5" fill="#15803D" font-weight="600">{html.escape(label)}</text>' if label else ''
            return (
                f'<g id="node_{nid}">'
                f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" />'
                f'  {subtext}'
                f'</g>'
            )

        elif ntype == "end_event":
            cx, cy = box["cx"], box["cy"]
            r = self.event_r
            subtext = f'<text x="{cx}" y="{ny + r*2 + 13}" text-anchor="middle" font-size="9.5" fill="#991B1B" font-weight="600">{html.escape(label)}</text>' if label else ''
            return (
                f'<g id="node_{nid}">'
                f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#FEE2E2" stroke="#DC2626" stroke-width="3.5" />'
                f'  {subtext}'
                f'</g>'
            )

        return ""

    def _get_bpmn_task_icon_svg(self, task_type: str, nx: float, ny: float) -> str:
        """Returns standard monochrome BPMN 2.0 task type vector symbol for card top-left corner."""
        ix = nx + 7
        iy = ny + 6

        if task_type == "user":
            # BPMN User Task: single person silhouette
            return (
                f'<g transform="translate({ix}, {iy})" fill="#475569">'
                f'  <circle cx="5" cy="4" r="2.2" />'
                f'  <path d="M 1.5 12 C 1.5 9.2, 3 8, 5 8 C 7 8, 8.5 9.2, 8.5 12 Z" />'
                f'</g>'
            )
        elif task_type == "service":
            # BPMN Service Task: cogs / gear symbol
            return (
                f'<g transform="translate({ix}, {iy})" stroke="#475569" stroke-width="1.2" fill="none">'
                f'  <circle cx="6" cy="6" r="3" />'
                f'  <path d="M 6 1 L 6 3 M 6 9 L 6 11 M 1 6 L 3 6 M 9 6 L 11 6 M 2.5 2.5 L 3.9 3.9 M 8.1 8.1 L 9.5 9.5 M 2.5 9.5 L 3.9 8.1 M 8.1 3.9 L 9.5 2.5" />'
                f'</g>'
            )
        elif task_type == "send":
            # BPMN Send Task: filled envelope
            return (
                f'<g transform="translate({ix}, {iy})" fill="#475569">'
                f'  <rect x="0" y="1.5" width="12" height="8" rx="1" />'
                f'  <path d="M 0 2.5 L 6 6.5 L 12 2.5" stroke="#FFFFFF" stroke-width="1" fill="none" />'
                f'</g>'
            )
        elif task_type == "receive":
            # BPMN Receive Task: open outlined envelope
            return (
                f'<g transform="translate({ix}, {iy})" stroke="#475569" stroke-width="1.2" fill="none">'
                f'  <rect x="0" y="1.5" width="12" height="8" rx="1" />'
                f'  <path d="M 0 2.5 L 6 6.5 L 12 2.5" />'
                f'</g>'
            )
        elif task_type == "manual":
            # BPMN Manual Task: document sheet
            return (
                f'<g transform="translate({ix}, {iy})" stroke="#475569" stroke-width="1.2" fill="none">'
                f'  <path d="M 1 1 L 7 1 L 10 4 L 10 12 L 1 12 Z" />'
                f'  <path d="M 7 1 L 7 4 L 10 4" />'
                f'  <line x1="3" y1="6" x2="8" y2="6" />'
                f'  <line x1="3" y1="8.5" x2="8" y2="8.5" />'
                f'</g>'
            )
        return ""

    def _render_edge_svg(self, edge: Dict[str, Any]) -> str:
        """Renders sequence flow or message flow with standard markers and collision-free label badge."""
        pts = edge["waypoints"]
        label = edge.get("label", "")
        is_dashed = edge.get("dashed", False)
        is_violation = edge.get("violation", False)

        if is_violation:
            stroke = "#DC2626"
            stroke_w = 2.0
            dash = 'stroke-dasharray="5,4"'
            marker_start = ""
            marker_end = 'marker-end="url(#violation-arrow)"'
        elif is_dashed:
            # Standard BPMN 2.0 Message Flow
            stroke = "#475569"
            stroke_w = 1.4
            dash = 'stroke-dasharray="6,4"'
            marker_start = 'marker-start="url(#message-circle)"'
            marker_end = 'marker-end="url(#message-arrow)"'
        else:
            # Standard BPMN 2.0 Sequence Flow
            stroke = "#1E293B"
            stroke_w = 1.5
            dash = ""
            marker_start = ""
            marker_end = 'marker-end="url(#sequence-arrow)"'

        path_d = f"M {pts[0][0]} {pts[0][1]}"
        for p in pts[1:]:
            path_d += f" L {p[0]} {p[1]}"

        # Label badge placement with obstacle clearance
        label_svg = ""
        if label:
            lx, ly = self._compute_label_position(edge, pts)
            lbl_w = len(label) * 6.2 + 10
            lbl_col = "#DC2626" if is_violation else "#334155"
            border_col = "#FCA5A5" if is_violation else "#CBD5E1"
            label_svg = (
                f'<g>'
                f'  <rect x="{lx - lbl_w/2}" y="{ly - 7}" width="{lbl_w}" height="14" fill="#FFFFFF" rx="3" stroke="{border_col}" stroke-width="0.8" />'
                f'  <text x="{lx}" y="{ly + 3}" text-anchor="middle" font-size="8.5" font-weight="600" fill="{lbl_col}">{html.escape(label)}</text>'
                f'</g>'
            )

        return f'<path d="{path_d}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}" {dash} {marker_start} {marker_end} />\n{label_svg}'

    def _compute_label_position(self, edge: Dict[str, Any], pts: List[Tuple[float, float]]) -> Tuple[float, float]:
        """Calculates collision-free coordinates for connector label pill badge."""
        if "label_pos" in edge and edge["label_pos"]:
            return edge["label_pos"]

        # Find the longest segment
        max_len = 0
        best_seg = (pts[0], pts[1])
        is_horiz = True

        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            seg_len = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
            if seg_len > max_len:
                max_len = seg_len
                best_seg = (p1, p2)
                is_horiz = (p1[1] == p2[1])

        p1, p2 = best_seg
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2

        if is_horiz:
            return (mid_x, mid_y - 8)
        else:
            return (mid_x, mid_y)


# ======================================================================================
# DECLARATIVE ARCHITECTURAL WORKFLOW SPECIFICATIONS (ZERO HARDCODED COORDINATES)
# ======================================================================================

def get_level1_spec(is_violating: bool = False) -> Tuple[str, List[Dict], List[Dict], List[Dict], Optional[Dict]]:
    """Level 1: Basic Loan Origination (Sequential Flow + Exclusive Decision)."""
    top_pool = {
        "title": "🏊 Pool: Customer / Borrower Portal",
        "nodes": [
            {"id": "p_start", "type": "start_event", "label": "Start", "col": 0},
            {"id": "p_submit", "type": "task", "task_type": "user", "label": "Access Portal &\nSubmit Application", "col": 1},
            {"id": "p_receive", "type": "task", "task_type": "receive", "label": "Receive Official\nDecision Letter", "col": 5},
            {"id": "p_end", "type": "end_event", "label": "Completed", "col": 6}
        ]
    }
    lanes = [
        {"id": "lane_intake", "name": "Front-Office Desk", "bg": "#EFF6FF"},
        {"id": "lane_risk", "name": "Credit & Risk Dept", "bg": "#FEFCE8"},
        {"id": "lane_officer", "name": "Loan Officer", "bg": "#FAF5FF"}
    ]
    nodes = [
        {"id": "t_recv", "type": "task", "task_type": "service", "lane": "lane_intake", "label": "Receive Application &\nCreate Loan Dossier", "col": 1},
        {"id": "xor_split", "type": "gateway_xor", "lane": "lane_intake", "label": "", "col": 2},
        {"id": "t_check", "type": "task", "task_type": "service", "lane": "lane_risk", "label": "Mandatory Credit Check\n(Prerequisite)", "col": 3, "fill": "#EFF6FF", "stroke": "#2563EB"},
        {"id": "xor_dec", "type": "gateway_xor", "lane": "lane_officer", "label": "Eligible?", "col": 4},
        {"id": "t_app", "type": "task", "task_type": "user", "lane": "lane_officer", "label": "Loan Officer\nApprove Loan", "col": 5, "track": 0, "fill": "#DCFCE7", "stroke": "#16A34A"},
        {"id": "t_rej", "type": "task", "task_type": "user", "lane": "lane_officer", "label": "Loan Officer\nReject Loan", "col": 5, "track": 1, "fill": "#FEE2E2", "stroke": "#DC2626"},
        {"id": "end_app", "type": "end_event", "lane": "lane_officer", "label": "Approved", "col": 6, "track": 0},
        {"id": "end_rej", "type": "end_event", "lane": "lane_officer", "label": "Rejected", "col": 6, "track": 1}
    ]
    edges = [
        {"from": "p_start", "to": "p_submit"},
        {"from": "p_receive", "to": "p_end"},
        {"from": "p_submit", "to": "t_recv", "dashed": True},
        {"from": "t_recv", "to": "xor_split"},
        {"from": "xor_split", "to": "t_check"},
        {"from": "t_check", "to": "xor_dec"},
        {"from": "xor_dec", "to": "t_app", "label": "Eligible"},
        {"from": "xor_dec", "to": "t_rej", "label": "Ineligible"},
        {"from": "t_app", "to": "end_app"},
        {"from": "t_rej", "to": "end_rej"},
        {"from": "t_app", "to": "p_receive", "dashed": True}
    ]
    if is_violating:
        edges.append({
            "from": "xor_split", "to": "t_app",
            "label": "⚠️ Skip Credit Check",
            "violation": True
        })
    return "🏦 Pool: Commercial Lending Institution (Single-Tier Process)", lanes, nodes, edges, top_pool


def get_level2_spec(is_violating: bool = False) -> Tuple[str, List[Dict], List[Dict], List[Dict], Optional[Dict]]:
    """Level 2: Medium (Parallel Concurrency via AND-Split Fork & AND-Join Sync)."""
    top_pool = {
        "title": "🏊 Pool: Customer / Borrower Portal",
        "nodes": [
            {"id": "p_start", "type": "start_event", "label": "Start", "col": 0},
            {"id": "p_submit", "type": "task", "task_type": "user", "label": "Access Portal &\nSubmit Commercial File", "col": 1},
            {"id": "p_receive", "type": "task", "task_type": "receive", "label": "Receive Official\nDecision Letter", "col": 6},
            {"id": "p_end", "type": "end_event", "label": "Completed", "col": 7}
        ]
    }
    lanes = [
        {"id": "lane_intake", "name": "Commercial Intake", "bg": "#EFF6FF"},
        {"id": "lane_audit", "name": "Technical & Collateral Audit", "bg": "#FEFCE8"},
        {"id": "lane_manager", "name": "Branch Underwriting", "bg": "#FAF5FF"}
    ]
    nodes = [
        {"id": "t_recv", "type": "task", "task_type": "service", "lane": "lane_intake", "label": "Commercial Intake &\nCreate Loan Dossier", "col": 1},
        {"id": "and_split", "type": "gateway_and", "lane": "lane_audit", "label": "", "col": 2},
        {"id": "t_check", "type": "task", "task_type": "service", "lane": "lane_audit", "label": "Mandatory Credit Risk\nAssessment", "col": 3, "track": 0, "fill": "#EFF6FF", "stroke": "#2563EB"},
        {"id": "t_collateral", "type": "task", "task_type": "service", "lane": "lane_audit", "label": "Collateral Valuation &\nAsset Vetting", "col": 3, "track": 1},
        {"id": "and_join", "type": "gateway_and", "lane": "lane_audit", "label": "", "col": 4},
        {"id": "xor_eval", "type": "gateway_xor", "lane": "lane_manager", "label": "Low Risk?", "col": 5},
        {"id": "t_app", "type": "task", "task_type": "user", "lane": "lane_manager", "label": "Branch Manager\nApprove Loan", "col": 6, "track": 0, "fill": "#DCFCE7", "stroke": "#16A34A"},
        {"id": "t_rej", "type": "task", "task_type": "user", "lane": "lane_manager", "label": "Branch Manager\nReject Loan", "col": 6, "track": 1, "fill": "#FEE2E2", "stroke": "#DC2626"},
        {"id": "end_app", "type": "end_event", "lane": "lane_manager", "label": "Approved", "col": 7, "track": 0},
        {"id": "end_rej", "type": "end_event", "lane": "lane_manager", "label": "Rejected", "col": 7, "track": 1}
    ]
    edges = [
        {"from": "p_start", "to": "p_submit"},
        {"from": "p_receive", "to": "p_end"},
        {"from": "p_submit", "to": "t_recv", "dashed": True},
        {"from": "t_recv", "to": "and_split"},
        {"from": "and_split", "to": "t_check"},
        {"from": "and_split", "to": "t_collateral"},
        {"from": "t_check", "to": "and_join"},
        {"from": "t_collateral", "to": "and_join"},
        {"from": "and_join", "to": "xor_eval"},
        {"from": "xor_eval", "to": "t_app", "label": "Approved"},
        {"from": "xor_eval", "to": "t_rej", "label": "Rejected"},
        {"from": "t_app", "to": "end_app"},
        {"from": "t_rej", "to": "end_rej"},
        {"from": "t_app", "to": "p_receive", "dashed": True}
    ]
    if is_violating:
        edges.append({
            "from": "t_collateral", "to": "t_app",
            "label": "⚠️ Skip Credit Assessment",
            "violation": True
        })
    return "🏦 Pool: Commercial Bank (Dual-Audit Concurrency)", lanes, nodes, edges, top_pool


def get_level3_spec(is_violating: bool = False) -> Tuple[str, List[Dict], List[Dict], List[Dict], Optional[Dict]]:
    """Level 3: Advanced Enterprise Origination (Parallel AND + Inclusive OR + Multi-Tier XOR + Rework Loop)."""
    top_pool = {
        "title": "🏊 Pool: Customer / Borrower Portal",
        "nodes": [
            {"id": "p_start", "type": "start_event", "label": "Start", "col": 0},
            {"id": "p_submit", "type": "task", "task_type": "user", "label": "Submit Syndicated\nLoan Request", "col": 1},
            {"id": "p_resubmit", "type": "task", "task_type": "user", "label": "Upload Requested\nDisclosures", "col": 7, "fill": "#FEF3C7"},
            {"id": "p_receive", "type": "task", "task_type": "receive", "label": "Receive Official\nDecision Letter", "col": 11},
            {"id": "p_end", "type": "end_event", "label": "Completed", "col": 12}
        ]
    }
    lanes = [
        {"id": "lane_broker", "name": "Commercial Credit Broker", "bg": "#EFF6FF"},
        {"id": "lane_audit", "name": "Technical & Collateral Audit", "bg": "#FEFCE8"},
        {"id": "lane_branch", "name": "Branch Credit Committee", "bg": "#FFF1F2"},
        {"id": "lane_executive", "name": "Senior Committee & Board", "bg": "#FAF5FF"}
    ]
    nodes = [
        # Lane 1: Commercial Credit Broker
        {"id": "t_recv", "type": "task", "task_type": "service", "lane": "lane_broker", "label": "Receive Application &\nCreate Loan Dossier", "col": 1},
        {"id": "t_broker_vet", "type": "task", "task_type": "user", "lane": "lane_broker", "label": "Check Customer\nStanding & Privileges", "col": 2},

        # Lane 2: Technical & Collateral Audit
        {"id": "and_split", "type": "gateway_and", "lane": "lane_audit", "label": "", "col": 3},
        {"id": "t_credit", "type": "task", "task_type": "service", "lane": "lane_audit", "label": "Mandatory Credit Risk\nAssessment", "col": 4, "track": 0, "fill": "#EFF6FF", "stroke": "#2563EB"},
        {"id": "or_split", "type": "gateway_or", "lane": "lane_audit", "label": "Collateral?", "col": 4, "track": 1},
        {"id": "t_prop", "type": "task", "task_type": "service", "lane": "lane_audit", "label": "Real Estate Appraisal\n(Collateral Track 1)", "col": 5, "track": 1},
        {"id": "t_guar", "type": "task", "task_type": "service", "lane": "lane_audit", "label": "Corporate Guarantor Audit\n(Collateral Track 2)", "col": 5, "track": 2},
        {"id": "or_join", "type": "gateway_or", "lane": "lane_audit", "label": "", "col": 6, "track": 1},
        {"id": "and_join", "type": "gateway_and", "lane": "lane_audit", "label": "", "col": 6, "track": 0},

        # Lane 3: Branch Credit Committee
        {"id": "xor_eval", "type": "gateway_xor", "lane": "lane_branch", "label": "Risk Tier?", "col": 7, "track": 1},
        {"id": "t_rework", "type": "task", "task_type": "service", "lane": "lane_branch", "label": "Request Additional Documents\n(Trigger Rework Loop)", "col": 7, "track": 0, "fill": "#FEF3C7", "stroke": "#D97706"},
        {"id": "t_low_app", "type": "task", "task_type": "user", "lane": "lane_branch", "label": "Standard Manager Approval\n(Low Risk)", "col": 8, "track": 0, "fill": "#DCFCE7", "stroke": "#16A34A"},
        {"id": "t_rej", "type": "task", "task_type": "user", "lane": "lane_branch", "label": "Reject Loan\n(Critical Risk)", "col": 8, "track": 1, "fill": "#FEE2E2", "stroke": "#DC2626"},
        {"id": "t_escalate", "type": "task", "task_type": "user", "lane": "lane_branch", "label": "Escalate to Senior Board\n(High Risk / Jumbo)", "col": 8, "track": 2, "fill": "#EDE9FE", "stroke": "#7C3AED"},
        {"id": "end_app_tier1", "type": "end_event", "lane": "lane_branch", "label": "Approved", "col": 9, "track": 0},
        {"id": "end_rej_tier1", "type": "end_event", "lane": "lane_branch", "label": "Rejected", "col": 9, "track": 1},

        # Lane 4: Senior Committee & Executive Board
        {"id": "t_comm_rev", "type": "task", "task_type": "user", "lane": "lane_executive", "label": "Senior Committee Review\n(Mandatory Governance)", "col": 9, "track": 0},
        {"id": "xor_comm", "type": "gateway_xor", "lane": "lane_executive", "label": "Vote?", "col": 10, "track": 0},
        {"id": "t_comm_app", "type": "task", "task_type": "user", "lane": "lane_executive", "label": "Committee Approve Loan", "col": 11, "track": 0, "fill": "#DCFCE7", "stroke": "#16A34A"},
        {"id": "t_comm_rej", "type": "task", "task_type": "user", "lane": "lane_executive", "label": "Committee Reject Loan", "col": 11, "track": 1, "fill": "#FEE2E2", "stroke": "#DC2626"},
        {"id": "end_app_tier2", "type": "end_event", "lane": "lane_executive", "label": "Disbursed", "col": 12, "track": 0},
        {"id": "end_rej_tier2", "type": "end_event", "lane": "lane_executive", "label": "Closed", "col": 12, "track": 1}
    ]
    edges = [
        {"from": "p_start", "to": "p_submit"},
        {"from": "p_receive", "to": "p_end"},
        {"from": "p_submit", "to": "t_recv", "dashed": True},
        {"from": "t_recv", "to": "t_broker_vet"},
        {"from": "t_broker_vet", "to": "and_split"},
        {"from": "and_split", "to": "t_credit"},
        {"from": "and_split", "to": "or_split"},
        {"from": "or_split", "to": "t_prop", "label": "Property"},
        {"from": "or_split", "to": "t_guar", "label": "Guarantor"},
        {"from": "t_prop", "to": "or_join"},
        {"from": "t_guar", "to": "or_join"},
        {"from": "t_credit", "to": "and_join"},
        {"from": "or_join", "to": "and_join"},
        {"from": "and_join", "to": "xor_eval"},
        {"from": "xor_eval", "to": "t_rework", "label": "Incomplete"},
        {"from": "t_rework", "to": "p_resubmit", "dashed": True},
        {"from": "p_resubmit", "to": "xor_eval", "dashed": True},
        {"from": "xor_eval", "to": "t_low_app", "label": "Low Risk"},
        {"from": "xor_eval", "to": "t_rej", "label": "Critical Risk"},
        {"from": "xor_eval", "to": "t_escalate", "label": "Jumbo Loan"},
        {"from": "t_low_app", "to": "end_app_tier1"},
        {"from": "t_rej", "to": "end_rej_tier1"},
        {"from": "t_escalate", "to": "t_comm_rev"},
        {"from": "t_comm_rev", "to": "xor_comm"},
        {"from": "xor_comm", "to": "t_comm_app", "label": "Approved"},
        {"from": "xor_comm", "to": "t_comm_rej", "label": "Rejected"},
        {"from": "t_comm_app", "to": "end_app_tier2"},
        {"from": "t_comm_rej", "to": "end_rej_tier2"},
        {"from": "t_comm_app", "to": "p_receive", "dashed": True}
    ]
    if is_violating:
        edges.append({
            "from": "t_escalate", "to": "t_comm_app",
            "label": "⚠️ Executive Override (Skip Governance)",
            "violation": True
        })
    return "🏦 Pool: Corporate Loan Provider (Multi-Tier Financial Institution)", lanes, nodes, edges, top_pool


# ======================================================================================
# PUBLIC API
# ======================================================================================

def get_swimlane_engine(level_key: str, variant: str = "compliant") -> BPMNSwimlaneEngine:
    """Initializes and executes the BPMNSwimlaneEngine for the specified model."""
    is_violating = (variant.lower() == "violating")
    if level_key == "level1":
        title, lanes, nodes, edges, top_pool = get_level1_spec(is_violating)
    elif level_key == "level2":
        title, lanes, nodes, edges, top_pool = get_level2_spec(is_violating)
    else:
        title, lanes, nodes, edges, top_pool = get_level3_spec(is_violating)

    engine = BPMNSwimlaneEngine(title, lanes, nodes, edges, top_pool)
    return engine


def get_swimlane_svg(level_key: str, variant: str = "compliant") -> str:
    """Returns publication-quality BPMN 2.0 SVG string generated purely by the automated engine."""
    engine = get_swimlane_engine(level_key, variant)
    routed_edges = engine.layout()
    return engine.render_svg(routed_edges)


def get_swimlane_dimensions(level_key: str, variant: str = "compliant") -> Tuple[int, int]:
    """Returns dynamically computed (width, height) for the responsive UI iframe."""
    engine = get_swimlane_engine(level_key, variant)
    engine.layout()
    return (int(engine.total_width), int(engine.total_height))
