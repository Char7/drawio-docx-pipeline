#!/usr/bin/env python3
"""Pre-generation scope gate for diagrams containing AI source artwork.

Standard library only. Does NOT generate images, call a model, or approve content.
The JSON is a planning record; --ready additionally checks that generation is authorized.
"""
import argparse
import json
import math
import sys
from pathlib import Path

def positive_dimensions(value):
    return isinstance(value, list) and len(value) == 2 and all(
        isinstance(x, int) and not isinstance(x, bool) and 1 <= x <= 8192 for x in value
    )

def inspect(plan, ready=False):
    problems = []
    def check(cond, msg):
        if not cond:
            problems.append(msg)
    check(isinstance(plan, dict), "plan must be a JSON object")
    if not isinstance(plan, dict):
        return problems
    for field in ("figure_id", "indicator", "purpose", "grade"):
        check(isinstance(plan.get(field), str) and bool(plan.get(field).strip()), f"missing {field}")
    check(isinstance(plan.get("target_diagram"), dict), "target_diagram must be an object")
    budget = plan.get("generation_budget")
    check(isinstance(budget, dict), "generation_budget must be an object")
    assets = plan.get("assets")
    check(isinstance(assets, list) and bool(assets), "assets must be a non-empty list")
    if not isinstance(assets, list):
        return problems
    if isinstance(budget, dict):
        count = budget.get("initial_images")
        check(isinstance(count, int) and not isinstance(count, bool) and 0 < count <= len(assets),
              "generation_budget.initial_images must be 1..number of assets (no speculative extras)")
        check(budget.get("avoid_unneeded_collage") is True,
              "generation_budget.avoid_unneeded_collage must be true")
    seen = set()
    required_asset_fields = ("asset_id", "subject", "use", "scientific_reference",
                             "prompt", "negative_prompt", "preferred_background")
    for index, a in enumerate(assets, 1):
        tag = f"assets[{index}]"
        if not isinstance(a, dict):
            problems.append(f"{tag} must be an object")
            continue
        for k in required_asset_fields:
            check(isinstance(a.get(k), str) and bool(a.get(k).strip()), f"{tag}: missing {k}")
        name = a.get("asset_id")
        if isinstance(name, str):
            check(name not in seen, f"{tag}: duplicate asset_id {name}")
            seen.add(name)
        check(isinstance(a.get("required_visible_parts"), list)
              and bool(a.get("required_visible_parts")), f"{tag}: list required_visible_parts")
        check(isinstance(a.get("do_not_depict"), list) and bool(a.get("do_not_depict")),
              f"{tag}: list do_not_depict")
        for f in ("target_resolution_px", "planned_drawio_box_px"):
            check(positive_dimensions(a.get(f)), f"{tag}: invalid {f}")
        desired = a.get("target_aspect_ratio")
        try:
            num, den = [float(v) for v in desired.split(":")]
            assert math.isfinite(num) and math.isfinite(den) and num > 0 and den > 0
            actual = a["target_resolution_px"][0] / a["target_resolution_px"][1]
            check(abs(actual / (num / den) - 1) <= 0.15,
                  f"{tag}: requested dimensions vary >15% from target_aspect_ratio")
        except (TypeError, ValueError, AssertionError, IndexError, KeyError, ZeroDivisionError):
            problems.append(f"{tag}: invalid target_aspect_ratio or dimensions")
        cover = a.get("minimum_useful_subject_coverage")
        waste = a.get("maximum_expected_discard_fraction")
        check(isinstance(cover, (int,float)) and not isinstance(cover,bool) and 0.8 <= cover <= 1,
              f"{tag}: minimum useful subject coverage must be >=0.8")
        check(isinstance(waste, (int,float)) and not isinstance(waste,bool) and 0 <= waste <= 0.15,
              f"{tag}: expected discarded/cropped fraction must be <=0.15; rescope the prompt")
        check(isinstance(a.get("reuse_candidate"), str), f"{tag}: record reuse_candidate")
        check(a.get("preferred_background") in ("transparent", "white", "required_context_scene"),
              f"{tag}: preferred_background must be transparent, white or required_context_scene")
        if a.get("preferred_background") == "required_context_scene":
            check(bool(a.get("context_exception_reason")), f"{tag}: explain essential context")
        if ready:
            check(a.get("source_image_status") == "NOT_GENERATED",
                  f"{tag}: images already exist; review reuse before another generation")
    if ready:
        check(plan.get("generation_allowed") is True, "generation_allowed must be true")
        check(plan.get("asset_plan_status") == "PLANNED_FOR_GENERATION",
              "asset_plan_status must be PLANNED_FOR_GENERATION")
        check(plan.get("approval") != "APPROVED", "generation approval is not user media approval")
    return problems

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("--ready", action="store_true",
                    help="Fail unless the scope and generation gate are ready")
    args = ap.parse_args(argv)
    try:
        obj = json.loads(args.plan.read_text(encoding="utf-8-sig"))
        problems = inspect(obj, ready=args.ready)
    except (OSError, ValueError, UnicodeError) as exc:
        problems = [str(exc)]
    result = {"file": str(args.plan), "mode":"ready" if args.ready else "structure",
              "pass": not problems, "problems":problems}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not problems else 2

if __name__=="__main__":
    sys.exit(main())
