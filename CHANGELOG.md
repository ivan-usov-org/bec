# CHANGELOG

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

### Fix

* fix: add async monitor to config and fix dap tests due to API changes in ophyd ([`f9ec240`](https://gitlab.psi.ch/bec/bec/-/commit/f9ec2403db1dc64d2a975814976f6560336ec184))

* fix: bugfix within scibec metadata handler to accomodate changes of metadata ([`eef2764`](https://gitlab.psi.ch/bec/bec/-/commit/eef2764f448b749345e53158ecccf09ea4f463cb))

### Test

* test: fix tests due to config changes ([`22c1e57`](https://gitlab.psi.ch/bec/bec/-/commit/22c1e5734e0171e8e2a526e947e3f7d8098dad06))

## v2.18.0 (2024-07-03)

### Build

* build: added tomli dependency ([`d1b7841`](https://gitlab.psi.ch/bec/bec/-/commit/d1b78417c03db383f11385add1362be2a6ce7175))

### Ci

* ci: added phoenix, sim and superxas pipelines ([`3e91a99`](https://gitlab.psi.ch/bec/bec/-/commit/3e91a99945f73bf8fa7b4ddb6dacbab4614d6bdf))

### Feature

* feat(bec_lib): added service version tag to service info ([`326cd21`](https://gitlab.psi.ch/bec/bec/-/commit/326cd218d0a4e1e1444f88964365954fca426900))

## v2.17.6 (2024-07-02)

### Fix

* fix(device_server): fixed readout of objects that are neither devices nor signals ([`b4ee786`](https://gitlab.psi.ch/bec/bec/-/commit/b4ee7865cabe9010b49e928d4aa5f6107afd2df4))

## v2.17.5 (2024-07-01)

### Fix

* fix(device_server): fixed bug that caused alarms not to be raised ([`7a5fa85`](https://gitlab.psi.ch/bec/bec/-/commit/7a5fa85c0f715602b1edec5b5a499c2139b86b7e))

## v2.17.4 (2024-07-01)

### Fix

* fix(rpc): fixed bug that caused get to not update the cache ([`814f501`](https://gitlab.psi.ch/bec/bec/-/commit/814f50132e4018efaafc1f687cc3678bde4af316))

### Refactor

* refactor(device_server): rpc_mixin cleanup ([`58c0425`](https://gitlab.psi.ch/bec/bec/-/commit/58c0425772e2eee871aecbdb8a9dc88f4c0cb39e))

## v2.17.3 (2024-06-28)

### Fix

* fix: fixed cont_line_scan ([`d9df652`](https://gitlab.psi.ch/bec/bec/-/commit/d9df652e0464ce44eccb4b79c6bc63a54890edef))

* fix: bugfix on dtype int/float missmatch for self.positions ([`37c4868`](https://gitlab.psi.ch/bec/bec/-/commit/37c4868b13df95c56792c89be7171859ba9d9295))

### Test

* test: fix tests ([`b5ee738`](https://gitlab.psi.ch/bec/bec/-/commit/b5ee738153a2fc20d89822018cd420fbab415bba))

## v2.17.2 (2024-06-28)

### Build

* build: fakeredis dependency version update after fakeredis has been fixed ([`33db330`](https://gitlab.psi.ch/bec/bec/-/commit/33db33033c4d8028cffe84b154300e926c365315))

### Documentation

* docs: fix redis install for psi-maintained ([`bed9e90`](https://gitlab.psi.ch/bec/bec/-/commit/bed9e90183a236880d3e54d93571cdf4ad2ce9a5))

### Fix

* fix: fixed bug where a failed device status would not cause the scan to abort ([`2b93187`](https://gitlab.psi.ch/bec/bec/-/commit/2b93187c3522e99b09c68bc3b844e3ea6ffd1adf))

## v2.17.1 (2024-06-25)

### Fix

* fix: configure logger levels for BECIPythonClient in constructor ([`72b6e3e`](https://gitlab.psi.ch/bec/bec/-/commit/72b6e3e543a64d86a615cf400fa5057317a722ad))

* fix: _update_sinks applies different level for each logger ([`7ed5d6a`](https://gitlab.psi.ch/bec/bec/-/commit/7ed5d6ae82f0605de1f0422a0c6c658cec230159))

* fix: set level for each logger to the given value ([`1428ba2`](https://gitlab.psi.ch/bec/bec/-/commit/1428ba27f9239aa67fcb4b9111980d1d0955de32))

* fix: remove redundant update of loggers ([`8b82f35`](https://gitlab.psi.ch/bec/bec/-/commit/8b82f357970daab1ad0cac9ea36b42f460b1afd2))

### Refactor

* refactor: renaming of _update_logger_level to _update_console_logger_level ([`03a58d6`](https://gitlab.psi.ch/bec/bec/-/commit/03a58d6f1d035cfc0a31d4f6c61436825d0fd31a))

## v2.17.0 (2024-06-25)

### Feature

* feat(bec_lib): added option to name the logger ([`5d6cc7d`](https://gitlab.psi.ch/bec/bec/-/commit/5d6cc7dd05ee49e5afd526409fb100b50aa9c56d))

### Fix

* fix(logger): do not enqueue log messages

Enqueing log messages is useful when multiple processes (launched with
multiprocess module) are logging to the same log file, which is not the
use case for BEC - it creates processing threads, which can be avoided ([`1318b22`](https://gitlab.psi.ch/bec/bec/-/commit/1318b221cb6c26650535019175c74d748b003ea8))

* fix: logger: make console_log opt-in instead of having it by default and removing for certain classes ([`1d1f795`](https://gitlab.psi.ch/bec/bec/-/commit/1d1f795f9143363fa73a7cc9d5e7827d613552c1))

* fix: logger: log stderr to sys.__stderr__ to be compatible with sys.stderr redirection ([`9824ee4`](https://gitlab.psi.ch/bec/bec/-/commit/9824ee43aaf283c743762affead3c3b9e517abce))

### Test

* test: made completer test more targeted towards the completion results ([`cc5503f`](https://gitlab.psi.ch/bec/bec/-/commit/cc5503f86c32e266ef4755c78f01eed40cbad808))
