#!/usr/bin/env python3
"""Validate QA obligation coverage for Writer Input Package runs.

Usage:
  python3 scripts/validate_obligation_coverage.py qa.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_CONTRACTS = {
    "structure_contract",
    "behavior_contract",
    "expression_contract",
    "acceptance_contract",
}
ALLOWED_RESULTS = {"PASS", "PARTIAL", "WARNING", "FAIL"}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_obligation_coverage.py qa.json")
        return 2

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures: list[str] = []
    coverage = data.get("obligation_coverage")
    if not isinstance(coverage, list) or not coverage:
        failures.append("missing obligation_coverage list")
    else:
        seen_contracts = set()
        for index, item in enumerate(coverage, start=1):
            if not item.get("obligation"):
                failures.append(f"coverage item {index} missing obligation")
            contract = item.get("source_contract")
            if contract not in REQUIRED_CONTRACTS | {"material_package"}:
                failures.append(f"coverage item {index} has invalid source_contract: {contract}")
            else:
                if contract in REQUIRED_CONTRACTS:
                    seen_contracts.add(contract)
            result = item.get("result")
            if result not in ALLOWED_RESULTS:
                failures.append(f"coverage item {index} has invalid result: {result}")
            evidence = item.get("evidence")
            if result == "PASS" and (not isinstance(evidence, list) or not evidence):
                failures.append(f"coverage item {index} PASS requires evidence")
            if result in {"PARTIAL", "WARNING", "FAIL"} and not item.get("problem"):
                failures.append(f"coverage item {index} {result} requires problem")

        missing = REQUIRED_CONTRACTS - seen_contracts
        for contract in sorted(missing):
            failures.append(f"missing coverage for {contract}")

    if failures:
        print("Fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
