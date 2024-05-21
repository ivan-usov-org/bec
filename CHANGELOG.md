# CHANGELOG



## v2.12.3 (2024-05-21)

### Fix

* fix: renamed table_wait to scan_progress ([`855f9a8`](https://gitlab.psi.ch/bec/bec/-/commit/855f9a8412e9c0d8b02d131ece533b4d85882b36))

* fix: renamed scan_progress to device_progress ([`d344e85`](https://gitlab.psi.ch/bec/bec/-/commit/d344e8513781f29a1390adc92826f23d1702964b))


## v2.12.2 (2024-05-17)

### Fix

* fix(scihub): added experimentId to scan entries in BEC db ([`8ba7213`](https://gitlab.psi.ch/bec/bec/-/commit/8ba7213e29ac0335bca126b9d8a08a9ec46e469f))


## v2.12.1 (2024-05-17)

### Fix

* fix: race condition when reading new value from stream ([`87cc71a`](https://gitlab.psi.ch/bec/bec/-/commit/87cc71aa91c9d35b6483f4ef6c5de3c59575e9dc))

* fix: import &#39;dap_plugin_objects&#39; at last minute to speed up initial import ([`d7db6be`](https://gitlab.psi.ch/bec/bec/-/commit/d7db6befe9b8e4689ed37ccad44f8a5d06694180))

* fix: messages import made lazy to speed up initial import time

TODO: put back imports as normal when Pydantic gets faster ([`791be9b`](https://gitlab.psi.ch/bec/bec/-/commit/791be9b25aa618d508feed99a201e0c58b56f3ce))

* fix: do not import modules if only for type checking (faster import) ([`1c628fd`](https://gitlab.psi.ch/bec/bec/-/commit/1c628fd6105ef5df99e97c8945d3382c45ef5350))

* fix: clean all imports from bec_lib, remove use of @threadlocked ([`8a017ef`](https://gitlab.psi.ch/bec/bec/-/commit/8a017ef3d7666f173a70f2e6a8606d73b1af0095))

* fix: use lazy import to reduce bec_lib import time ([`649502e`](https://gitlab.psi.ch/bec/bec/-/commit/649502e364e4e4c0ea53f932418c479f2d6978d4))

* fix: solve scope problem with &#39;name&#39; variable in lambda ([`417e73e`](https://gitlab.psi.ch/bec/bec/-/commit/417e73e5d65f0c774c92889a44d1262c7f4f343b))


## v2.12.0 (2024-05-16)

### Feature

* feat(scan_bundler): added scan progress ([`27befe9`](https://gitlab.psi.ch/bec/bec/-/commit/27befe966607a3ae319dbee3af9e59ef0d044bc8))


## v2.11.1 (2024-05-16)

### Ci

* ci: cleanup ARGs in dockerfiles ([`b670d1a`](https://gitlab.psi.ch/bec/bec/-/commit/b670d1aa6b6e2af0cb09e7dbc77ea5d1bc66593b))

* ci: run AdditionalTests jobs on pipeline start

This is a followup to !573 ([`c9ece7e`](https://gitlab.psi.ch/bec/bec/-/commit/c9ece7ef2f1f9b052ed9b92bcb29463cf8371c64))

### Documentation

* docs(bec_lib): improved scripts documentation ([`79f487e`](https://gitlab.psi.ch/bec/bec/-/commit/79f487ea8b9dc135102204872390631e59a60e54))

### Fix

* fix(bec_lib): fixed loading scripts from plugins

User scripts from plugins were still relying on the old plugin structure ([`3264434`](https://gitlab.psi.ch/bec/bec/-/commit/3264434d40647d260400045f7bbd4c2ee9bb2c4e))


## v2.11.0 (2024-05-15)

### Feature

* feat: add utility function to determine instance of an object by class name ([`0ccd13c`](https://gitlab.psi.ch/bec/bec/-/commit/0ccd13cd738dc12d4a587b4c5e0d6b447d7cfc50))

* feat: add utilities to lazy import a module ([`a37ae57`](https://gitlab.psi.ch/bec/bec/-/commit/a37ae577f68c154dc3da544816b7c7f0cb532c50))

* feat: add &#39;Proxy&#39; to bec_lib utils ([`11a3f6d`](https://gitlab.psi.ch/bec/bec/-/commit/11a3f6daa46b3e6a82b66bd781b7590d01478b54))

### Style

* style: create directory to contain utils ([`549994d`](https://gitlab.psi.ch/bec/bec/-/commit/549994d0fdffcd4f5ed0948e1cd4cd4a0d0092af))


## v2.10.4 (2024-05-14)

### Build

* build: fixed fakeredis version for now ([`51dfe69`](https://gitlab.psi.ch/bec/bec/-/commit/51dfe69298170eba7220fcb506d99515c46ea32a))

### Ci

* ci: update dependencies and add ci job to check for package versions ([`2aafb24`](https://gitlab.psi.ch/bec/bec/-/commit/2aafb249e8f0b8afa8ede0dc4ba0a811ecb2a70f))

### Fix

* fix: disabled script linter for now ([`5c5c18e`](https://gitlab.psi.ch/bec/bec/-/commit/5c5c18ef0eab33ebaa33d1a0daa846ea7f2f59a8))


## v2.10.3 (2024-05-08)

### Fix

* fix: upgraded to ophyd_devices v1 ([`3077dbe`](https://gitlab.psi.ch/bec/bec/-/commit/3077dbe22ae50e6aae317c72022df6ea88b14cce))


## v2.10.2 (2024-05-08)

### Ci

* ci: added ds pipeline for tomcat ([`55d210c`](https://gitlab.psi.ch/bec/bec/-/commit/55d210c7ae06ea509328510e6aec636caf009cfd))

### Fix

* fix(RedisConnector): add &#39;from_start&#39; support in &#39;register&#39; for streams ([`f059bf9`](https://gitlab.psi.ch/bec/bec/-/commit/f059bf9318038404ebbcc82b5abf5cd148486021))

### Refactor

* refactor(bec_startup): default gui is BECDockArea (gui variable) with fig in first dock ([`7dc2426`](https://gitlab.psi.ch/bec/bec/-/commit/7dc242689f0966d692d3aeb77ca7689ea8709680))


## v2.10.1 (2024-05-07)

### Build

* build: fixed dependency range ([`c10ac5e`](https://gitlab.psi.ch/bec/bec/-/commit/c10ac5e78887844e46b965a707351d663ac4bcf8))

### Ci

* ci: moved from multi-project pipelines to parent-child pipelines ([`9eff5ca`](https://gitlab.psi.ch/bec/bec/-/commit/9eff5ca3580c3536e1edff5ade264dc6fc3f6f6e))

* ci: changed repo name to bec_widgets in downstream tests ([`698029b`](https://gitlab.psi.ch/bec/bec/-/commit/698029b637b1c84c5b1e836d8c6fbc8c8c7e3e0e))

### Fix

* fix: upgraded plugin setup tools ([`ea38501`](https://gitlab.psi.ch/bec/bec/-/commit/ea38501ea7ae4a62d6525b00608484ff1be540a1))


## v2.10.0 (2024-05-03)

### Feature

* feat: add client message handler to send info messages from services to clients; closes 258 ([`c0a0e3e`](https://gitlab.psi.ch/bec/bec/-/commit/c0a0e3e44299b350790687db436771c6b456567a))


## v2.9.6 (2024-05-02)

### Fix

* fix(scihub): fixed scibec connector for new api ([`fc94c82`](https://gitlab.psi.ch/bec/bec/-/commit/fc94c827e40f12293c59b139ccd455df8b8b4d70))


## v2.9.5 (2024-05-02)

### Fix

* fix: use the right redis fixture in &#34;bec_servers&#34; fixture to prevent multiple redis processes to be started ([`51d65e2`](https://gitlab.psi.ch/bec/bec/-/commit/51d65e2e9547765c34cc4a0a43f1adca90e7e5c3))

* fix: do not try to populate `user_global_ns` if IPython interpreter is not there ([`cf07feb`](https://gitlab.psi.ch/bec/bec/-/commit/cf07febc5cf0fdadec0e9658c2469ce1adb1a369))

### Test

* test: added more tests for scan queue ([`b664b92`](https://gitlab.psi.ch/bec/bec/-/commit/b664b92aae917d2067bfca48a60eeaf44ced0c98))


## v2.9.4 (2024-05-01)

### Refactor

* refactor: added isort params to pyproject ([`0a1beae`](https://gitlab.psi.ch/bec/bec/-/commit/0a1beae06ae128d9817272644d2f38ca761756ab))

* refactor(bec_lib): cleanup ([`6bf0998`](https://gitlab.psi.ch/bec/bec/-/commit/6bf0998c71387307ad8d842931488ec2aea566a8))
