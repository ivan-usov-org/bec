# CHANGELOG



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

### Fix

* fix: unified device message signature ([`c54dfc1`](https://gitlab.psi.ch/bec/bec/-/commit/c54dfc166fe9dd925b15e8cc8750cebaec8896cb))

### Refactor

* refactor: added isort params to pyproject ([`0a1beae`](https://gitlab.psi.ch/bec/bec/-/commit/0a1beae06ae128d9817272644d2f38ca761756ab))

* refactor(bec_lib): cleanup ([`6bf0998`](https://gitlab.psi.ch/bec/bec/-/commit/6bf0998c71387307ad8d842931488ec2aea566a8))


## v2.9.3 (2024-05-01)

### Fix

* fix: fixed log message log type ([`af85937`](https://gitlab.psi.ch/bec/bec/-/commit/af8593794c2ea9d0b4851b367aca4e6546fc760f))

* fix: fixed log message signature and added literal checks; closes #277 ([`ca7c238`](https://gitlab.psi.ch/bec/bec/-/commit/ca7c23851976111d81c811bf16b6d6f371d24dc6))

* fix: logs should be send, not set_and_publish; closes #278 ([`3964870`](https://gitlab.psi.ch/bec/bec/-/commit/396487074905930c410978144e986d1b9b373a2c))

* fix: device_req_status only needs set ([`587cfcc`](https://gitlab.psi.ch/bec/bec/-/commit/587cfccbe576dcd2eb10fc16e225ee3175f8d2a0))


## v2.9.2 (2024-04-29)

### Fix

* fix(bec_startup): BECFigure starts up after client ([`6b48858`](https://gitlab.psi.ch/bec/bec/-/commit/6b488588fed818ee1fefae8d5620821381b2eee0))


## v2.9.1 (2024-04-29)

### Documentation

* docs: updated docs for bec plugins ([`29b89dd`](https://gitlab.psi.ch/bec/bec/-/commit/29b89dd0173dfd9a692040d0acbf14bf47a6a46c))

### Fix

* fix: renamed dap_services to services ([`62549f5`](https://gitlab.psi.ch/bec/bec/-/commit/62549f57c9a497f0feceb63a8facd66669f56437))

* fix: updated plugin helper script to new plugin structure ([`8e16efb`](https://gitlab.psi.ch/bec/bec/-/commit/8e16efb21a5f6f68eee61ff22a930bf9e7400110))


## v2.9.0 (2024-04-29)

### Documentation

* docs: added section on logging ([`ebcd2a4`](https://gitlab.psi.ch/bec/bec/-/commit/ebcd2a4dbc2a52dc1e8679e54784daa0f6a3901b))

### Feature

* feat(bec_lib): added log monitor as CLI tool ([`0b624a4`](https://gitlab.psi.ch/bec/bec/-/commit/0b624a4ab5039c157edc1a3b589ba462f82879dd))

* feat(bec_lib): added trace log with stack trace ([`650de81`](https://gitlab.psi.ch/bec/bec/-/commit/650de811090dc72407cfb746eb22aa883682d268))

### Test

* test(bec_lib): added test for log monitor ([`64d5c30`](https://gitlab.psi.ch/bec/bec/-/commit/64d5c304d98c04f5943dd6365de364974a6fc931))


## v2.8.0 (2024-04-27)

### Build

* build: fixed fpdf version ([`94b6995`](https://gitlab.psi.ch/bec/bec/-/commit/94b6995fd32224557b2fc8b3aeafcf73acdb8a2c))

### Feature

* feat(bec_lib): added option to combine yaml files ([`39bb628`](https://gitlab.psi.ch/bec/bec/-/commit/39bb6281bda2960de7e70c45463f62dde2b454f5))


## v2.7.3 (2024-04-26)

### Documentation

* docs: fixed bec config template ([`87d0986`](https://gitlab.psi.ch/bec/bec/-/commit/87d0986f21ba367dbb23db50c7c13f10b4007030))

* docs: review docs, fix ScanModificationMessage, monitor callback and DAPRequestMessage ([`6b89240`](https://gitlab.psi.ch/bec/bec/-/commit/6b89240f46b2f892847e81963b7898649cb1c8d9))

### Fix

* fix: fixed loading of plugin-based configs ([`f927735`](https://gitlab.psi.ch/bec/bec/-/commit/f927735cd4012d4e4182596dc2ac2735d5ec4697))

### Test

* test(bec_lib): added test for unregistering callbacks ([`6e14de3`](https://gitlab.psi.ch/bec/bec/-/commit/6e14de35dc43b7eed3244f5fe327d79ddc1302ae))


## v2.7.2 (2024-04-25)

### Fix

* fix(channel_monitor): register.start removed since connector.register do not have any .start method ([`1eaefc1`](https://gitlab.psi.ch/bec/bec/-/commit/1eaefc1c8ab08e8c4939c05912d476b08bdcc2c9))

* fix(redis_connector): unregister is not killing communication ([`b31d506`](https://gitlab.psi.ch/bec/bec/-/commit/b31d506c9f7b541e0b8022aafdb8d44e0478ea3c))

### Refactor

* refactor: add file_writer and readme for tests ([`d8f76f5`](https://gitlab.psi.ch/bec/bec/-/commit/d8f76f505726fe12bdf572a9b5659a3c04620fde))

### Unknown

* Refactor(bec_lib.utils_script): Update util script for new plugin structure ([`6e36eaf`](https://gitlab.psi.ch/bec/bec/-/commit/6e36eaf3b1c7c77ba78e956613c9ac7f3d6865db))


## v2.7.1 (2024-04-23)
