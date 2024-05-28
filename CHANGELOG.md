# CHANGELOG



## v2.12.4 (2024-05-28)

### Ci

* ci: added development pages ([`4a9f4f8`](https://gitlab.psi.ch/bec/bec/-/commit/4a9f4f83fae16f40df679cddc5bf816e3b77deff))

### Documentation

* docs: fixed broken links ([`5dfcbe6`](https://gitlab.psi.ch/bec/bec/-/commit/5dfcbe6d132dd199be9f42980ed254efb2dc0e82))

* docs: added reference to gitlab issues ([`7277ac3`](https://gitlab.psi.ch/bec/bec/-/commit/7277ac3c40f86ff465f7af69a060fb9d5f2d4acc))

* docs: fixed api reference; added reference to scanbase ([`121e592`](https://gitlab.psi.ch/bec/bec/-/commit/121e5922eb3806eff88f49b5378b1f12056be132))

* docs: cleanup ([`7254755`](https://gitlab.psi.ch/bec/bec/-/commit/7254755aacda0f9c50b09237a59cd3584fb48e74))

* docs: added reference to user docs for loading new device configs ([`fd29dfb`](https://gitlab.psi.ch/bec/bec/-/commit/fd29dfb5f7d63d864e08adae1b5128f0f0fed14a))

* docs: added linkify ([`3a363f5`](https://gitlab.psi.ch/bec/bec/-/commit/3a363f5f52b644bc2542913cf4e9acf224ef69f9))

* docs: improvements for the dev docs ([`e5a98d7`](https://gitlab.psi.ch/bec/bec/-/commit/e5a98d718d06004819b32db1fabf77e634bdefd0))

* docs: restructured developer docs ([`7fd66f8`](https://gitlab.psi.ch/bec/bec/-/commit/7fd66f895905cb3e46ee90b98bfac8985837d6ca))

* docs: added docs for developing scans ([`5f44521`](https://gitlab.psi.ch/bec/bec/-/commit/5f4452110519404573484d2c6a95d8a46c325a1f))

* docs: fixed dependency for building sphinx ([`9cbde72`](https://gitlab.psi.ch/bec/bec/-/commit/9cbde72505723b5e4da94eeab4c8313e29c295c5))

* docs: fixed api reference ([`29862dc`](https://gitlab.psi.ch/bec/bec/-/commit/29862dca51873d4c22db6a693014ecf7addb4447))

### Fix

* fix: create readme for tests_dap_services ([`104c847`](https://gitlab.psi.ch/bec/bec/-/commit/104c847b55427c3ac78afb3af9e71154deff7d9e))

### Refactor

* refactor: renamed move_and_wait to move_scan_motors_and_wait ([`eaa8bd8`](https://gitlab.psi.ch/bec/bec/-/commit/eaa8bd8e67aa75a00d6a5b3e2494ed9828e7d6cf))

* refactor: deprecated scan report hint ([`0382ac5`](https://gitlab.psi.ch/bec/bec/-/commit/0382ac52dd9d68e6871866311416632ee39ed232))


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
