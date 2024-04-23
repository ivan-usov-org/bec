# CHANGELOG



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

### Documentation

* docs(dev/install): fixed install guide for developers bec_client -&gt; bec_ipython_client ([`a8d270e`](https://gitlab.psi.ch/bec/bec/-/commit/a8d270e0d702e4750b63631bf9fb34e4f30ed610))

* docs: fixed version update for sphinx ([`8366896`](https://gitlab.psi.ch/bec/bec/-/commit/836689667c03c0aa1a35db97ca772f2ae05f5f79))

### Feature

* feat(bec_client): added support for plugin-based startup scripts ([`aec75b4`](https://gitlab.psi.ch/bec/bec/-/commit/aec75b4966e570bd3e16ac295b09009eb1589acd))

* feat(file_writer): added support for file writer layout plugins ([`a6578fb`](https://gitlab.psi.ch/bec/bec/-/commit/a6578fb13349c0cabd24d313a7d58f63772fa584))

* feat(scan_server): added support for plugins ([`23f8721`](https://gitlab.psi.ch/bec/bec/-/commit/23f872127b06d321564fa343b069ae962ba2b6c6))

* feat(bec_lib): added plugin helper ([`7f1b789`](https://gitlab.psi.ch/bec/bec/-/commit/7f1b78978bbe2ad61e490416e44bc23001757d5e))

### Refactor

* refactor: removed outdated xml writer ([`c9bd092`](https://gitlab.psi.ch/bec/bec/-/commit/c9bd0928ea9f42e6b11aadd6ac42d7fe5e649ec7))

* refactor: minor cleanup ([`b7bd584`](https://gitlab.psi.ch/bec/bec/-/commit/b7bd584898a8ca6f11ff79e11fda2727d0fc6381))

* refactor: moved to dot notation for specifying device classes ([`1f21b90`](https://gitlab.psi.ch/bec/bec/-/commit/1f21b90ba31ec8eb8ae2922a7d1353c2e8ea48f6))


## v2.5.0 (2024-04-18)

### Build

* build: fix path to bec_ipython_client version ([`4420148`](https://gitlab.psi.ch/bec/bec/-/commit/4420148a09e2f92354aa20be75a9d3b0f19f4514))

* build: removed wheel dependency ([`ff0d2a1`](https://gitlab.psi.ch/bec/bec/-/commit/ff0d2a1ebb266d08d93aa088ff3151d27c828446))

* build: moved to pyproject ([`f7f7eba`](https://gitlab.psi.ch/bec/bec/-/commit/f7f7eba2316ec78f2f46a59c52234f827d509101))

* build(bec_lib): upgraded to fpdf2 ([`c9818c3`](https://gitlab.psi.ch/bec/bec/-/commit/c9818c35e4b1f3732ae6403c534bb505ad1121fc))

### Ci

* ci: exit job if no artifacts need to be uploaded to pypi ([`2e00112`](https://gitlab.psi.ch/bec/bec/-/commit/2e00112447e5aee5ce91bc0fa9f51e9faf0f4ee5))

* ci: updated ci for pyproject ([`3b541fb`](https://gitlab.psi.ch/bec/bec/-/commit/3b541fb7600e499046d053f21a399de01263fb24))

* ci: migrate docker to gitlab Dependency Proxy

Related to 1108662db13e8142b37cb3645ff7e9bc94d242b8

The docker-compose file/command might need further fixes, once the related end-2-end tests are activated. ([`80270f8`](https://gitlab.psi.ch/bec/bec/-/commit/80270f81968bfb717a0c631f0a87a0b809912f6a))

### Feature

* feat: added pytest-bec-e2e plugin ([`deaa2b0`](https://gitlab.psi.ch/bec/bec/-/commit/deaa2b022ae636d77401f905ed522024b44721f5))

### Test

* test(device_server): fixed leaking threads in device server tests ([`ae65328`](https://gitlab.psi.ch/bec/bec/-/commit/ae653282bc107077f54e79b822e9dea188d53eca))


## v2.4.2 (2024-04-16)

### Ci

* ci: pull images via gitlab dependency proxy ([`1108662`](https://gitlab.psi.ch/bec/bec/-/commit/1108662db13e8142b37cb3645ff7e9bc94d242b8))

### Fix

* fix(ci): add rules to trigger child pipelines ([`5a1894b`](https://gitlab.psi.ch/bec/bec/-/commit/5a1894bfca881b9791704c8a6aeb274e2f002a51))

### Unknown

* refacto: bec_client renamed bec_ipython_client ([`d3ad8ca`](https://gitlab.psi.ch/bec/bec/-/commit/d3ad8ca432bbd0f62bfb1a44231a4de90f3603f8))

* tests: new fixtures &#39;test_config_yaml&#39; and device manager ([`5547793`](https://gitlab.psi.ch/bec/bec/-/commit/5547793375e041af655e9e5aec9220c03b439874))

* tests: move end2end fixtures to bec client ([`66fa939`](https://gitlab.psi.ch/bec/bec/-/commit/66fa9394dbd34f62d9238358c6848f5338769a2c))


## v2.4.1 (2024-04-16)

### Ci

* ci: updated default BECWidgets branch name to main ([`c41fe08`](https://gitlab.psi.ch/bec/bec/-/commit/c41fe0845532a05a7dfbd2f9aec038b1801e29c3))

### Fix

* fix(client): resolve on done ([`5ea7ed3`](https://gitlab.psi.ch/bec/bec/-/commit/5ea7ed3e3e4b7b9edfff5008321eaf5e5cdaf9ae))


## v2.4.0 (2024-04-15)

### Ci

* ci: remove AdditionalTests dependency on tests job ([`54b139f`](https://gitlab.psi.ch/bec/bec/-/commit/54b139f40cebba03f1302f7828d30a9602cc807d))

### Feature

* feat(flomni): scan status for tomography ([`eca3e64`](https://gitlab.psi.ch/bec/bec/-/commit/eca3e64facd2b1faa46787d9d70f8ce027df645f))


## v2.3.0 (2024-04-12)

### Ci

* ci: specify main branch for semver job ([`31a54ca`](https://gitlab.psi.ch/bec/bec/-/commit/31a54cab9325fa0932a2189b4032404036cfbbe6))

* ci: changes due to renaming of master to main ([`291779f`](https://gitlab.psi.ch/bec/bec/-/commit/291779f4c362b5241b5ca636408cb4b36e4f551d))

### Feature

* feat: rename spec_hli to bec_hli, add load_hli function to BECIPythonCLient; closes #263 ([`6974cb2`](https://gitlab.psi.ch/bec/bec/-/commit/6974cb2f13e865d1395eda2274ac25abd6e44ef8))

### Refactor

* refactor: use callback_handler for namespace updates of clients and add tests ([`0a832a1`](https://gitlab.psi.ch/bec/bec/-/commit/0a832a149dbbc37627ff84674a6d38f5697db8ab))


## v2.2.1 (2024-04-12)

### Documentation

* docs: added link to BECFigure docs ([`6d13618`](https://gitlab.psi.ch/bec/bec/-/commit/6d13618a6fec7104bcb72cb32745ad645851bec3))

### Fix

* fix(client): removed outdated bec plotter; to be replaced by BECFigure once ready ([`52b33d8`](https://gitlab.psi.ch/bec/bec/-/commit/52b33d8b65a9496fa38719cb30ba5666cccd4b55))

### Unknown

* tests: use of subprocess.Popen instead of multiprocessing.Process (#256) ([`8ae98ec`](https://gitlab.psi.ch/bec/bec/-/commit/8ae98ec2992dae23634db649f0bdbdc795b2efb0))
