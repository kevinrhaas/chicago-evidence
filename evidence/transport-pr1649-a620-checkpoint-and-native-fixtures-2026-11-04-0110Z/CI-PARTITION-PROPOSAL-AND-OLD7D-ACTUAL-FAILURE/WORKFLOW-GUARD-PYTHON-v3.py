from pathlib import Path
import json, re, sys
source = Path(sys.argv[1]).read_text()
def valid(text):
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#'))
    if '\njobs:\n' not in text: return False
    text = text.split('\njobs:\n', 1)[1]
    jobs = {}
    for match in re.finditer(r'^  ([a-z][a-z0-9-]*):\s*$', text, re.M):
        start = match.end(); following = re.search(r'^  [a-z][a-z0-9-]*:\s*$', text[start:], re.M)
        jobs[match.group(1)] = text[start:start + following.start()] if following else text[start:]
    if set(jobs) != {'check-part', 'gate'}: return False
    part, gate = jobs['check-part'], jobs['gate']
    if re.search(r'^\s+(?:include|exclude):', part, re.M): return False
    if re.findall(r'^\s+if:\s*(.+)$', gate, re.M) != ['${{ always() }}']: return False
    required = [
        '    name: gate part ${{ matrix.part }}/8',
        '    runs-on: ubuntu-latest', '      fail-fast: false', '      max-parallel: 8',
        '          fetch-depth: 0', '          filter: blob:none',
        "          C4D_GATE_REQUIRE_READERS: '1'", "          C4D_GATE_REQUIRE_BASE: '1'",
        '          CHECK_JOBS: ${{ steps.jobs.outputs.n }}',
        '        run: timeout --kill-after=5s 600s ./tools/check.sh --part "${{ matrix.part }}/8"',
        '          node chicago/4d/tools/check-changelog-entry.mjs',
        '          "${{ github.event.pull_request.base.sha }}"',
        '          "${{ github.event.pull_request.head.sha }}"',
    ]
    if any(line not in part.splitlines() for line in required): return False
    matrix = re.search(r'^        part: (\[[^\n]+\])$', part, re.M)
    if not matrix or json.loads(matrix.group(1)) != list(range(1, 9)): return False
    if re.findall(r'^\s+if:\s*(.+)$', part, re.M) != ["github.event_name == 'pull_request'"]: return False
    if 'continue-on-error:' in text: return False
    for line in ['    name: gate', '    needs: check-part', '    if: ${{ always() }}',
                 '    runs-on: ubuntu-latest', '          PARTS_RESULT: ${{ needs.check-part.result }}',
                 '        run: test "$PARTS_RESULT" = success']:
        if line not in gate.splitlines(): return False
    if len(re.findall(r'^\s+run:', gate, re.M)) != 1: return False
    return True
assert valid(source), 'native CI partition or final required gate changed'
controls = [
    source.replace('part: [1, 2, 3, 4, 5, 6, 7, 8]', 'part: [1, 2, 3, 4, 5, 6, 7]'),
    source.replace('600s ./tools/check.sh', '601s ./tools/check.sh'),
    source.replace('/8"', '/4"'),
    source.replace('timeout --kill-after=5s 600s ./tools/check.sh --part "${{ matrix.part }}/8"', 'true'),
    source.replace("C4D_GATE_REQUIRE_READERS: '1'", "C4D_GATE_REQUIRE_READERS: '0'"),
    source.replace("C4D_GATE_REQUIRE_BASE: '1'", "C4D_GATE_REQUIRE_BASE: '0'"),
    source.replace('fetch-depth: 0', 'fetch-depth: 1'),
    source.replace('    steps:\n', '    if: false\n    steps:\n', 1),
    source.replace('    if: ${{ always() }}\n', ''),
    source.replace('test "$PARTS_RESULT" = success', 'test "$PARTS_RESULT" != failure'),
    source.replace('    name: gate\n', '    name: different-check\n'),
    source.replace('        part: [1, 2, 3, 4, 5, 6, 7, 8]', '        part: [1, 2, 3, 4, 5, 6, 7, 8]\n        exclude:\n          - part: 8'),
    source.replace('        part: [1, 2, 3, 4, 5, 6, 7, 8]', '        part: [1, 2, 3, 4, 5, 6, 7, 8]\n        include:\n          - part: 1'),
    source.replace('    if: ${{ always() }}\n', '    if: ${{ always() }}\n    if: false\n'),
]
for i, broken in enumerate(controls, 1):
    assert not valid(broken), f'unsafe CI shape control {i} passed'
print(f'CI partition: required gate and all eight native parts; {len(controls)} refusal controls pass')