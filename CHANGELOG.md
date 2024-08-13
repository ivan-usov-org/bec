# CHANGELOG

## v2.21.3 (2024-08-13)

### Fix

* fix: fix bug in bluesky emitter get descriptor method ([`27fa758`](https://gitlab.psi.ch/bec/bec/-/commit/27fa7584cd61c6453db01ab05f49b9c712155641))

## v2.21.2 (2024-08-13)

### Fix

* fix(bec_lib): raise on rpc status failure ([`efc07ff`](https://gitlab.psi.ch/bec/bec/-/commit/efc07ff4ff6ddf810d3a40ec52b35877e7ae67a7))

### Test

* test: fixed test for status wait ([`4c5dd4a`](https://gitlab.psi.ch/bec/bec/-/commit/4c5dd4ab40a0c8d2ebef38d36ec61c230243f649))

## v2.21.1 (2024-08-13)

### Fix

* fix(redis_connector): fixed support for bundle message ([`ef637c0`](https://gitlab.psi.ch/bec/bec/-/commit/ef637c0e59f94ad471ec1dce5906a56ae0299f9a))

* fix(bec_lib): fixed reported msg type for device_config endpoint ([`28f9882`](https://gitlab.psi.ch/bec/bec/-/commit/28f98822173cba43860dcd20f890fee93a978d6a))

* fix(bec_lib): added check to ensure becmessage type is correct ([`c8b4ab9`](https://gitlab.psi.ch/bec/bec/-/commit/c8b4ab9d99530351fa2005b69e118a5fb563d1e3))

### Refactor

* refactor: minor cleanup ([`f08c652`](https://gitlab.psi.ch/bec/bec/-/commit/f08c652dd6eca114331be4b915bec66fe911ff12))

* refactor(scan_bundler): moved specific bec emitter methods from emitterbase to bec emitter ([`b0bc0da`](https://gitlab.psi.ch/bec/bec/-/commit/b0bc0da54f66e5ad4d26471c88eb7d1c8910bead))

## v2.21.0 (2024-08-13)

### Documentation

* docs(messaging): added first draft of bec messaging docs ([`efbeca3`](https://gitlab.psi.ch/bec/bec/-/commit/efbeca3c322fa62a95b51ebc5670a6d446dcdebc))

### Feature

* feat: Add metadata entry to _info for signal and device ([`fe4979a`](https://gitlab.psi.ch/bec/bec/-/commit/fe4979adbd4804c6f3b69902ade0d22c1b70f8cd))

### Test

* test: fix tests for adapted device_info ([`8778843`](https://gitlab.psi.ch/bec/bec/-/commit/877884336b52aa9e66e8b463fcb3bc7abcd654d1))

### Unknown

* docs (data_access): Data Access, messaging and event system. ([`27c838d`](https://gitlab.psi.ch/bec/bec/-/commit/27c838db04749e8051f57582c65492243b967094))

## v2.20.2 (2024-08-01)

### Ci

* ci: made jobs interruptible ([`1fc6bc4`](https://gitlab.psi.ch/bec/bec/-/commit/1fc6bc4b22c48715eff4d27709cffc5c08037769))

* ci: added support for child pipelines ([`d3385f6`](https://gitlab.psi.ch/bec/bec/-/commit/d3385f66e50e6b19e79030ec0af13054a7ab2f47))

### Fix

* fix: do not import cli.launch.main in __init__

This has the side effect of reconfiguring loggers to the level specified
in the main module (INFO in general) ([`45b3263`](https://gitlab.psi.ch/bec/bec/-/commit/45b32632181fff18758e2195b84f8254f365465a))

## v2.20.1 (2024-07-25)

### Ci

* ci: added child_pipeline_branch var ([`8ca8478`](https://gitlab.psi.ch/bec/bec/-/commit/8ca8478019b532db2ab2f5c0fbc8297ca9d56327))

* ci: added inputs to beamline trigger pipelines ([`5e11c0c`](https://gitlab.psi.ch/bec/bec/-/commit/5e11c0c06543a5d6f875575fe2a3cf9748421c5d))

* ci: cleanup and moved beamline trigger pipelines to awi utils ([`3030451`](https://gitlab.psi.ch/bec/bec/-/commit/303045198ec77c7a6b7ef5d5e7c4ab308c14a52f))

* ci: wip - downstream pipeline args for ophyd ([`81b1682`](https://gitlab.psi.ch/bec/bec/-/commit/81b168299bf9f05085b61eafe94aa3bc279c41b4))

* ci: wip - downstream pipeline args for ophyd ([`a5712c3`](https://gitlab.psi.ch/bec/bec/-/commit/a5712c379da39861b69bbb9129ea91eac6bbfda0))

### Fix

* fix: unpack args and kwargs in scaninfo ([`2955a85`](https://gitlab.psi.ch/bec/bec/-/commit/2955a855ca742e4cafcf33cc262b439c5afb2b5e))

### Test

* test: fix msg in init scan info ([`1357b21`](https://gitlab.psi.ch/bec/bec/-/commit/1357b216a83d130efb3ba9af21c0a1eef7d3a9e1))

## v2.20.0 (2024-07-25)

### Build

* build(ci): pass ophyd_devices branch to child pipeline ([`a3e2b2e`](https://gitlab.psi.ch/bec/bec/-/commit/a3e2b2e37634fe7f445cce7e0ff2ac0b01d093b3))

### Feature

* feat: add device_monitor plugin for client ([`c9a6f3b`](https://gitlab.psi.ch/bec/bec/-/commit/c9a6f3b1fad8cbb455c6a79379e03efa73fe984d))

### Refactor

* refactor: renamed DeviceMonitor2DMessage ([`0bb42d0`](https://gitlab.psi.ch/bec/bec/-/commit/0bb42d01bf7d7a03cf8e2a0859582ab14d8c99b8))

* refactor: renamed device_monitor to device_monitor_2d, adapted SUB_EVENT name ([`c7b59b5`](https://gitlab.psi.ch/bec/bec/-/commit/c7b59b59c16ac18134ab73bf020137d28da56775))

### Unknown

* test (device_monitor): add end-2-end test for device_monitor ([`4c578ce`](https://gitlab.psi.ch/bec/bec/-/commit/4c578ce15545e70072471e8def3bee2108b03ffb))

## v2.19.1 (2024-07-25)

### Fix

* fix: add velocity vs exp_time check for contline_scan to make it more robust ([`2848682`](https://gitlab.psi.ch/bec/bec/-/commit/2848682644624c024ac37fe946fbd2b6ddc377dc))

## v2.19.0 (2024-07-19)

### Feature

* feat: add &#34;parse_cmdline_args&#34; to bec_service, to handle common arguments parsing in services

Add &#34;--log-level&#34; and &#34;--file-log-level&#34; to be able to change log level from the command line ([`41b8005`](https://gitlab.psi.ch/bec/bec/-/commit/41b80058f8409131be483950dfb88e7b93282bff))

### Fix

* fix: prevent already configured logger to be re-configured ([`dfdc397`](https://gitlab.psi.ch/bec/bec/-/commit/dfdc39776e1cadffc53cf0193d2fa1791df821d5))

* fix: make a CONSOLE_LOG level to be able to filter console log messages and fix extra line feed ([`7f73606`](https://gitlab.psi.ch/bec/bec/-/commit/7f73606dfc4b4b97afe1f85a641626f0ab134b34))

### Refactor

* refactor: use &#39;parse_cmdline_args&#39; in servers ([`06902f7`](https://gitlab.psi.ch/bec/bec/-/commit/06902f78240c5ded0674349a125fd80f30aab580))

### Unknown

* tests: update tests following new &#34;parse_cmdline_args&#34; function ([`7e46cf9`](https://gitlab.psi.ch/bec/bec/-/commit/7e46cf94ef0454cf7d2299fad0bdcf7005fc8482))

* refactor, fix #318: use &#39;parse_cmdline_args&#39; for BEC IPython client ([`814b6b2`](https://gitlab.psi.ch/bec/bec/-/commit/814b6b21c6ae62fa71f8574a87d0e6279f32e266))

## v2.18.3 (2024-07-08)

### Fix

* fix(bec_lib): fixed bug that caused the specified service config to be overwritten by defaults ([`5cf162c`](https://gitlab.psi.ch/bec/bec/-/commit/5cf162c19d573afde19f795a968f1513461aec9a))

## v2.18.2 (2024-07-08)

### Fix

* fix(bec_lib): accept config as input to ServiceConfig ([`86714ae`](https://gitlab.psi.ch/bec/bec/-/commit/86714ae57b5952eaa739a5ba60d20aa6ab51bf91))

### Test

* test: fixed test for triggered devices ([`05e82ef`](https://gitlab.psi.ch/bec/bec/-/commit/05e82efe088a9ad0ac24542099c1008562287dbf))

## v2.18.1 (2024-07-04)

### Documentation

* docs: improve docs ([`b25a670`](https://gitlab.psi.ch/bec/bec/-/commit/b25a6704adf405344b3acfb2417cf5896fa77009))

### Test

* test: fix tests due to config changes ([`22c1e57`](https://gitlab.psi.ch/bec/bec/-/commit/22c1e5734e0171e8e2a526e947e3f7d8098dad06))
