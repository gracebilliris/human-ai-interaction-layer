#!/usr/bin/env bash
# verify_hashes.sh — Verify integrity of all released artefact files
# Run from the repository root.
set -euo pipefail

HASH_FILE="INTEGRITY.sha256"

if [ ! -f "$HASH_FILE" ]; then
  echo "ERROR: $HASH_FILE not found. Run from the repository root."
  exit 1
fi

echo "Verifying file integrity against $HASH_FILE ..."

PASS=0
FAIL=0
MISSING=0

while IFS='  ' read -r expected_hash filepath; do
  # Skip blank lines and comments
  [ -z "$expected_hash" ] && continue
  [[ "$expected_hash" == \#* ]] && continue

  if [ ! -f "$filepath" ]; then
    echo "MISSING: $filepath"
    MISSING=$((MISSING + 1))
    continue
  fi

  actual_hash=$(shasum -a 256 "$filepath" | awk '{print $1}')
  if [ "$actual_hash" = "$expected_hash" ]; then
    PASS=$((PASS + 1))
  else
    echo "MISMATCH: $filepath"
    echo "  expected: $expected_hash"
    echo "  actual:   $actual_hash"
    FAIL=$((FAIL + 1))
  fi
done < "$HASH_FILE"

echo ""
echo "Results: $PASS passed, $FAIL mismatched, $MISSING missing"

if [ $FAIL -gt 0 ] || [ $MISSING -gt 0 ]; then
  echo "VERIFICATION FAILED"
  exit 1
else
  echo "ALL FILES VERIFIED"
  exit 0
fi
