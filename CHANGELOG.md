# CHANGELOG



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

### Fix

* fix: fixed device server startup for CA override ([`773572b`](https://gitlab.psi.ch/bec/bec/-/commit/773572b33b23230b06ea6cc7b8e7e5ab3f792f3e))


## v2.7.0 (2024-04-19)

### Ci

* ci: skip trailing comma for black ([`fe657b6`](https://gitlab.psi.ch/bec/bec/-/commit/fe657b6adc416e7bc63b0a1e2970fdddcca63c29))

* ci: removed pipeline as trigger source for downstream jobs ([`92bb7ef`](https://gitlab.psi.ch/bec/bec/-/commit/92bb7ef3c59f14d25db63615a86445454201aafd))

* ci: update default ophyd branch to main ([`3334a7f`](https://gitlab.psi.ch/bec/bec/-/commit/3334a7f8e70d220daeaef51ac39328e3019a9bf0))

### Feature

* feat: move cSAXS plugin files from core ([`0a609a5`](https://gitlab.psi.ch/bec/bec/-/commit/0a609a56c0295026d04c4f5dea51800ad4ab8edf))

### Unknown

* flomni config ([`92fcb3b`](https://gitlab.psi.ch/bec/bec/-/commit/92fcb3b4024a4729a85673747c72c6abd1d1a4ef))


## v2.6.0 (2024-04-19)

### Ci

* ci: fixed build process during e2e test ([`369af7c`](https://gitlab.psi.ch/bec/bec/-/commit/369af7c2006114ece464f5cf96c332c059ab3154))

* ci: stop after two failures ([`90b7f45`](https://gitlab.psi.ch/bec/bec/-/commit/90b7f45c135f63b7384ef5feaee71902fb11ec74))

### Feature

* feat(bec_client): added support for plugin-based startup scripts ([`aec75b4`](https://gitlab.psi.ch/bec/bec/-/commit/aec75b4966e570bd3e16ac295b09009eb1589acd))

* feat(file_writer): added support for file writer layout plugins ([`a6578fb`](https://gitlab.psi.ch/bec/bec/-/commit/a6578fb13349c0cabd24d313a7d58f63772fa584))

* feat(scan_server): added support for plugins ([`23f8721`](https://gitlab.psi.ch/bec/bec/-/commit/23f872127b06d321564fa343b069ae962ba2b6c6))

* feat(bec_lib): added plugin helper ([`7f1b789`](https://gitlab.psi.ch/bec/bec/-/commit/7f1b78978bbe2ad61e490416e44bc23001757d5e))

### Refactor

* refactor: removed outdated xml writer ([`c9bd092`](https://gitlab.psi.ch/bec/bec/-/commit/c9bd0928ea9f42e6b11aadd6ac42d7fe5e649ec7))

* refactor: minor cleanup ([`b7bd584`](https://gitlab.psi.ch/bec/bec/-/commit/b7bd584898a8ca6f11ff79e11fda2727d0fc6381))

* refactor: moved to dot notation for specifying device classes ([`1f21b90`](https://gitlab.psi.ch/bec/bec/-/commit/1f21b90ba31ec8eb8ae2922a7d1353c2e8ea48f6))
