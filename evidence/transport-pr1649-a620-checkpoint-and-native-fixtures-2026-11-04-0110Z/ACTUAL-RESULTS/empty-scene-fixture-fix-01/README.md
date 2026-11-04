# Empty-scene fixture dependency repair

The native7d gate had one failure among1154steps. Its isolated actual main boot block did not supply the newlyused `draws` and `prepareSceneDirectoryPerson` dependencies, so the production error catcher correctly reported `draws is not defined` to the fixture. The expected options list also missed the new port. Production main defines `draws` from the actual scene-layer list.

The one-file patch supplies those real interface bindings. It retains all previous unsupported-scene, failed-fetch, Light, lazy-import, exact callback and error assertions, adds the optional port to exact key checking, and proves actual empty supported rows do not trigger card preparation or model activity at any tier.

The existing native fixture passed in0.3674seconds in a shadow whose unchanged readers symlink to the actual current ROOT. Original120-second supervisor cap, resources and cleanup passed. ROOT stayed on81bbb with an unchanged semantic index and no tracked changes. No browser, app edit, full gate, commit or merge was performed.

The raw log retains a THREE warning from an empty add; no warning is suppressed and no additional app fix is proposed here.
