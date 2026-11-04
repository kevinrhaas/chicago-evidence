from pathlib import Path
import unittest,sys
p=Path('/tmp/wolf-poster-source-20261103/chicago/4d/tools/test_frame_tavern_picture_features.py')
sys.path.insert(0,str(p.parent))
ns={'__name__':'proposal_owner','__file__':str(p)}
exec(compile(Path('/tmp/smoke-yard-shadow-triage-20261104/test_frame_tavern_picture_features_PROPOSAL.py').read_text(),str(p),'exec'),ns)
cls=ns['PictureFeatures']
suite=unittest.TestSuite(cls(name) for name in ['test_occupied_annex_components_preserve_the_open_bay','test_green_tree_yard_shed_and_enclosed_shoulder_are_mutually_exclusive'])
r=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if r.wasSuccessful() else 1)
