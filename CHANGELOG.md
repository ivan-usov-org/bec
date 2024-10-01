# CHANGELOG

## v2.34.2 (2024-10-01)

### Fix

* fix: fixed min version of msgpack ([`00d9572`](https://gitlab.psi.ch/bec/bec/-/commit/00d957267a70bbe56f25a36f8b8ae9d7dcbd97d6))

## v2.34.1 (2024-10-01)

### Fix

* fix: min version for typeguard to support literals is 4.1.5 ([`c2e05c0`](https://gitlab.psi.ch/bec/bec/-/commit/c2e05c04febf8ef019f6c08fdf890627158bb5a4))

## v2.34.0 (2024-10-01)

### Build

* build: updated numpy and hiredis version ([`88f5e9d`](https://gitlab.psi.ch/bec/bec/-/commit/88f5e9d508d924d7e364808b2a8476a72bb365a4))

### Feature

* feat(utils): added plugin repo license ([`d32ed2b`](https://gitlab.psi.ch/bec/bec/-/commit/d32ed2b6deb4bbb6fbfb5833ad5c341249967b39))

### Refactor

* refactor: allow rgb array data within DeviceMonitor2DMessage ([`eb3c302`](https://gitlab.psi.ch/bec/bec/-/commit/eb3c30287410f76eadacadb3e53f98e6d44c4406))

## v2.33.0 (2024-09-18)

### Feature

* feat(interactive scans): added support for interactive scans

This commit adds support for interactive scans. This is a new feature that allows users to interactively define scans in the BEC client. The user can specify the scan parameters in a context manager and then run the scan interactively by accessing the device objects directly. Dedicated trigger and read function are provided to perform larger actions. ([`d842e20`](https://gitlab.psi.ch/bec/bec/-/commit/d842e20dc8df809413a4017539019d8d644bcf68))

### Fix

* fix(interactive_scan): fixed bug in scan number calculation; simplified interface ([`ca4eb1e`](https://gitlab.psi.ch/bec/bec/-/commit/ca4eb1e5d42b272f5de4620ac73d5ae415136415))

* fix(interactive_scan): fixed default exp_time ([`e9839bf`](https://gitlab.psi.ch/bec/bec/-/commit/e9839bf79b44a004b1d3050d8cf3d71c86fff5e4))

* fix(scan_worker): exp time is optional; default 0 ([`90b07ed`](https://gitlab.psi.ch/bec/bec/-/commit/90b07ed690da05e397bc6971d497b09d583e0ac4))

* fix(rpc): check for alarms during rpc calls ([`99a1553`](https://gitlab.psi.ch/bec/bec/-/commit/99a1553794766ebbe9441a16b29a91be5dfba162))

### Refactor

* refactor(bec_lib): minor cleanup for cli scan context managers ([`c67e80a`](https://gitlab.psi.ch/bec/bec/-/commit/c67e80a29a1aa50566192f5f45d2e895256cfc40))

### Test

* test(dmmock): fixed mocked devicemanager to avoid leakage between tests ([`020856d`](https://gitlab.psi.ch/bec/bec/-/commit/020856d4febba1fa24e073fe27e6165b8ccdd450))

## v2.32.0 (2024-09-18)

### Feature

* feat(endpoint): added device_raw endpoint ([`1a9bb96`](https://gitlab.psi.ch/bec/bec/-/commit/1a9bb962f28f8f0c4319c9ee3177a6ca8cc660d1))

* feat(scan queue): added support for changing the order of scans in the queue ([`7eb4ead`](https://gitlab.psi.ch/bec/bec/-/commit/7eb4ead57d163e045a88f3af906aa928cc2bca0f))

## v2.31.2 (2024-09-13)

### Fix

* fix(dap): dap service should run independent of scan segment callbacks ([`026b12f`](https://gitlab.psi.ch/bec/bec/-/commit/026b12f2025ea33fd0be52518345834198364119))

## v2.31.1 (2024-09-12)

### Ci

* ci: fetch all tags ([`77be5e1`](https://gitlab.psi.ch/bec/bec/-/commit/77be5e1369d31d96cfee2a3fecf049dc1a1b70dc))

* ci: unshallow fetch to retrieve all commits for the changelog ([`395ccee`](https://gitlab.psi.ch/bec/bec/-/commit/395ccee57053e8bd55e31e8d2eab27478fa99d88))

### Fix

* fix: get &#34;egu&#34; (engineering units) from device from configuration, not through RPC call ([`7331d3c`](https://gitlab.psi.ch/bec/bec/-/commit/7331d3c4171465fa89597450a1c17beeaac2dc38))

## v2.31.0 (2024-09-05)

### Feature

* feat(scan_report): added public files to scan item and report on the master file in scan report ([`adca248`](https://gitlab.psi.ch/bec/bec/-/commit/adca248dfd592b1cdbfa2cddf1a10c13ac11e176))

### Test

* test: added test for file events ([`b976fb4`](https://gitlab.psi.ch/bec/bec/-/commit/b976fb4a084910da5ae0a4fac32d1152b0f1cc04))

## v2.30.2 (2024-09-05)

### Fix

* fix: updated device_config of pseudo_signal1 ([`529663f`](https://gitlab.psi.ch/bec/bec/-/commit/529663f4fdef795c7863622ee01328bf3a1385a6))

### Refactor

* refactor: ScanItem attributes bec and callback made private ([`a70af8f`](https://gitlab.psi.ch/bec/bec/-/commit/a70af8f58cba31294a6b84bb1b45d62f2dcb4cc0))

* refactor: refactoring to make scan_manager optional kwarg ([`a5ccefa`](https://gitlab.psi.ch/bec/bec/-/commit/a5ccefa978aa2b3c79d7b4617614bbde689036a0))

### Test

* test: fix tests ([`46738ad`](https://gitlab.psi.ch/bec/bec/-/commit/46738ad259c9e99095067b67ffbacbaff83115ea))

## v2.30.1 (2024-09-05)

### Fix

* fix: fix hints for devices of type ophyd.signal ([`1b8b2c7`](https://gitlab.psi.ch/bec/bec/-/commit/1b8b2c7b490113e0b7acd3a070c9bec1c1626b4f))

* fix: bugfix in cont_line_scan; reworked device and signal mocks ([`c91dcf4`](https://gitlab.psi.ch/bec/bec/-/commit/c91dcf4d37bc1add18d2f0682af97358e4abdee6))

### Refactor

* refactor: reworked R/W info in device info; removed bug for devices with type Signal ([`d0ee4ec`](https://gitlab.psi.ch/bec/bec/-/commit/d0ee4ec5544dcc400568dc5311cea0e1d4074c8e))

## v2.30.0 (2024-09-04)

### Feature

* feat(logger): added option to disable modules; added retention and rotation; changed log format for stderr ([`868f40d`](https://gitlab.psi.ch/bec/bec/-/commit/868f40db8e1420dab7eaf3fed6eed2e8313ab539))

## v2.29.0 (2024-09-02)

### Ci

* ci: prefill variables for manual pipeline start ([`d4b4bf8`](https://gitlab.psi.ch/bec/bec/-/commit/d4b4bf816a73923a90d0e7d1d5158f0e26016e92))

### Feature

* feat(config): added support for adding and removing devices ([`070b041`](https://gitlab.psi.ch/bec/bec/-/commit/070b0417d80c56b69093c768d25238cb0465de36))

### Fix

* fix(device_manager): fixed init value for failed devices ([`61c4fb6`](https://gitlab.psi.ch/bec/bec/-/commit/61c4fb69cdc068bdc997a53b26fccc15f00217b1))

## v2.28.0 (2024-09-02)

### Feature

* feat(queue schedule): added endpoint and queue schedule methods ([`0c7e0eb`](https://gitlab.psi.ch/bec/bec/-/commit/0c7e0eb37f3d88e94bbb0ae0ee346b9736bc582c))

## v2.27.0 (2024-08-30)

### Documentation

* docs(stubs): improvements to the stubs doc strings ([`89b4353`](https://gitlab.psi.ch/bec/bec/-/commit/89b4353433c603398e8c87da36e6ebc7aa2fc47c))

* docs(stubs): minor improvements to the wait docstring ([`9db0c03`](https://gitlab.psi.ch/bec/bec/-/commit/9db0c03bec9aa2fa50e2ad727d0a43727c2db482))

### Feature

* feat(endpoint): added stop_all_devices endpoint ([`13beb51`](https://gitlab.psi.ch/bec/bec/-/commit/13beb51a520e9ef6569fff45807bd50d076ce787))

### Fix

* fix(ipython client): fixed magic command for resume ([`2289036`](https://gitlab.psi.ch/bec/bec/-/commit/228903628b3dd624a20bea48ccf65ec9ff1cc5ed))

* fix(queue): moved queue modifications to dedicated message for the device server ([`3e0e5cf`](https://gitlab.psi.ch/bec/bec/-/commit/3e0e5cf9a8ab477acdbeb85b703beb86207fec18))

### Refactor

* refactor(docs): new bec logo ([`4070521`](https://gitlab.psi.ch/bec/bec/-/commit/4070521e6c4b6b8ee6b29730fdefb5def2f5be22))

## v2.26.0 (2024-08-22)

### Feature

* feat(bec_lib): print all asap client messages during rpc ([`5de3235`](https://gitlab.psi.ch/bec/bec/-/commit/5de3235788f5bc573e2b1daa2c81c977e200e921))

## v2.25.1 (2024-08-22)

### Fix

* fix: try/expect CONSOLE logger changed order ([`ca36128`](https://gitlab.psi.ch/bec/bec/-/commit/ca3612816bcb1bd86bc2480724fad57ce9af9892))

## v2.25.0 (2024-08-22)

### Feature

* feat(server): added endpoint and handler to restart server through redis ([`9bde681`](https://gitlab.psi.ch/bec/bec/-/commit/9bde68138c5930c0f050ffd9ee6fcd21a294a488))

## v2.24.0 (2024-08-21)

### Feature

* feat(lmfit): added fallback to hinted signals; added oversampling option ([`b66b928`](https://gitlab.psi.ch/bec/bec/-/commit/b66b9286899a69ab8bc71ec2a65e16189e52cb07))

## v2.23.2 (2024-08-21)

### Fix

* fix(docs): scan gui config tutorial added to toc ([`343309f`](https://gitlab.psi.ch/bec/bec/-/commit/343309ff5e224227e15076fc94a124a4c76262b4))

## v2.23.1 (2024-08-19)

### Fix

* fix(serialization): added json decoder as fallback option for raw messages ([`5e7f630`](https://gitlab.psi.ch/bec/bec/-/commit/5e7f630ce7b2e7a3ff3337d966155e4b5f5cc7ff))

### Test

* test: wait for dap to finish ([`be0d589`](https://gitlab.psi.ch/bec/bec/-/commit/be0d589ae89cc663687402fd4c2fb0a738643f22))

## v2.23.0 (2024-08-17)

### Feature

* feat(client): added client event for updated devices ([`7573ce1`](https://gitlab.psi.ch/bec/bec/-/commit/7573ce1b52e47106dfa7ab8b814420aeb1d14591))

## v2.22.1 (2024-08-16)

### Fix

* fix: remove unused imports, add missing import ([`92b5e4a`](https://gitlab.psi.ch/bec/bec/-/commit/92b5e4a50b45ee9d960fcf9839500fc420b9e0be))

### Test

* test: add connector unregister test with &#39;patterns&#39; ([`7f93933`](https://gitlab.psi.ch/bec/bec/-/commit/7f93933847dd387847930fb81171ca29f1b2d3be))

## v2.22.0 (2024-08-16)

### Ci

* ci: use target branch instead of default pipeline branch for e2e tests ([`83e0097`](https://gitlab.psi.ch/bec/bec/-/commit/83e00970d1e5f105ee3e05bce6fd7376bd9698e4))

* ci: install ophyd_devices from the repo ([`1e805b4`](https://gitlab.psi.ch/bec/bec/-/commit/1e805b47c6df2bc08966ffd250ba0b3f22ab9563))

### Documentation

* docs: update dev docs

renamed bec_config to bec_service_config; removed pmodule instructions as they are not available anymore ([`82ffc52`](https://gitlab.psi.ch/bec/bec/-/commit/82ffc521760fda34c594f89f10c174ae0b959710))

### Feature

* feat(device_server): gracefully handle timeouts

Failed config updates should only lead to config flush if the object initialization fails. If we simply can&#39;t connect to the signals, the device should be disabled. ([`ec5abd6`](https://gitlab.psi.ch/bec/bec/-/commit/ec5abd6dde4c71e41395ee6f532f27f24215e168))

### Fix

* fix: fixed bug in client fixture for loading configs ([`7636f4d`](https://gitlab.psi.ch/bec/bec/-/commit/7636f4d15a36a4f32a202643771e4b5d97ff5ae6))

* fix(client): handle deviceconfigerrors more gracefully in the console ([`433b831`](https://gitlab.psi.ch/bec/bec/-/commit/433b8313021eb89fd7135fa79504ba34270d12eb))

### Test

* test: fixed data access in dummy controller device ([`624c257`](https://gitlab.psi.ch/bec/bec/-/commit/624c25763fdef2a9ee913e5936311f421bd9b8d6))

* test: use simpositionerwithcontroller for controller access ([`49b53a9`](https://gitlab.psi.ch/bec/bec/-/commit/49b53a95d9317c6ec1bf14c81e2b3886788690d5))

* test: ensure BECClient singleton is reset ([`75dd67b`](https://gitlab.psi.ch/bec/bec/-/commit/75dd67ba17ab0d79881501f2f902ef0a8c2233a2))

### Unknown

* wip ([`a39a6c1`](https://gitlab.psi.ch/bec/bec/-/commit/a39a6c197a1a297a67e11b15d5ccbce7dbe3b95c))

## v2.21.5 (2024-08-14)

### Fix

* fix(tmux): retry tmux launch on error

Sometimes, restarting the tmux client is flaky ([`8ba44f6`](https://gitlab.psi.ch/bec/bec/-/commit/8ba44f6eef7bd9f118933ba03900134d9bb6cf32))

## v2.21.4 (2024-08-14)

### Fix

* fix(client): fixed client init of singleton instance ([`cfae861`](https://gitlab.psi.ch/bec/bec/-/commit/cfae8617fdb7f7a7fc613206f0f27d7274d899c1))

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

* fix: logger: do not update sinks twice in __init__ ([`051d6ad`](https://gitlab.psi.ch/bec/bec/-/commit/051d6ade9224f5aeb919bbe96e84dc49f4720482))

* fix: client: do not configure logging in _start_services()

Logging is already configured because BECClient inherits from BECService,
and BECService configures logging when client is started ([`4809dc5`](https://gitlab.psi.ch/bec/bec/-/commit/4809dc512eec418e08bfa79b40d3b3b75a4498da))

### Test

* test: made completer test more targeted towards the completion results ([`cc5503f`](https://gitlab.psi.ch/bec/bec/-/commit/cc5503f86c32e266ef4755c78f01eed40cbad808))

## v2.16.3 (2024-06-25)

### Fix

* fix(scan_server): sync fly scans should not retrieve scan motors ([`6dc16b4`](https://gitlab.psi.ch/bec/bec/-/commit/6dc16b4a89323c984b77f04cb76eacd442286e5b))

## v2.16.2 (2024-06-25)

### Fix

* fix(scan_server): ensure that scan server rpc calls use a unique request id ([`f3f6966`](https://gitlab.psi.ch/bec/bec/-/commit/f3f69669dd15d6d2284afbba336576603d77169b))

## v2.16.1 (2024-06-24)

### Fix

* fix(dap): fixed auto-run and added e2e test ([`5de45d0`](https://gitlab.psi.ch/bec/bec/-/commit/5de45d059c7bcfa6e7df769b72128bed7f0dbcda))

## v2.16.0 (2024-06-21)

### Feature

* feat(scan_server): added support for additional gui config ([`c6987b6`](https://gitlab.psi.ch/bec/bec/-/commit/c6987b6ec220ab98690b10bdbeef9823a0c7ed8a))

## v2.15.0 (2024-06-21)

### Feature

* feat(file_writer): separated device collection from metadata ([`75e6df4`](https://gitlab.psi.ch/bec/bec/-/commit/75e6df47f722439df827a307c61849a3828925da))

## v2.14.5 (2024-06-21)

### Fix

* fix(bec_lib): fixed pydantic type for scanqueuemodifications ([`6bf60f9`](https://gitlab.psi.ch/bec/bec/-/commit/6bf60f98fcaf80e1ab19ab2752d2d2e71f005225))

## v2.14.4 (2024-06-20)

### Documentation

* docs: added reference to epics configs ([`76c2c52`](https://gitlab.psi.ch/bec/bec/-/commit/76c2c5285ccc28f701614b9a8aed1b6f03d566ed))

### Fix

* fix: fix bug in emit service info and metrics ([`abf77c8`](https://gitlab.psi.ch/bec/bec/-/commit/abf77c80804afbb5fbe4d328f88ce4ab88c4710e))

### Test

* test: add tests for metrics ([`1ceae8b`](https://gitlab.psi.ch/bec/bec/-/commit/1ceae8ba0ce78aa074ea7ed1f0bd374b7ced632f))

## v2.14.3 (2024-06-17)

### Documentation

* docs: improved dev install instructions ([`d43cd25`](https://gitlab.psi.ch/bec/bec/-/commit/d43cd25786aa0e3892592350feb4def8ab541120))

* docs: adjusted init for flyer class ([`fa0c96f`](https://gitlab.psi.ch/bec/bec/-/commit/fa0c96f2dba82b22395cc91fb5b8fe63956e698c))

* docs: moved scanbase code to end of section to not tempt readers to jump directly into the code ([`ff9d4ad`](https://gitlab.psi.ch/bec/bec/-/commit/ff9d4ad9508ffda81c49977519cf5d2fc95676d7))

### Fix

* fix(file_writer): fixed file writer messages to report successful only after it is written ([`27a0f89`](https://gitlab.psi.ch/bec/bec/-/commit/27a0f8920ce17116aad10b422d0c5b2ad33ca20c))

### Refactor

* refactor(scan_server): cleanup of scan args ([`d61f58c`](https://gitlab.psi.ch/bec/bec/-/commit/d61f58c362021f29b937a088b6a0a892cacc9176))

## v2.14.2 (2024-06-12)

### Fix

* fix(bec_lib): fixed access to global vars ([`f621ef2`](https://gitlab.psi.ch/bec/bec/-/commit/f621ef280e5121a44277d1b51de586d8eae82be5))

## v2.14.1 (2024-06-12)

### Documentation

* docs: fixed broken link to hdfgroup ([`afbb3ff`](https://gitlab.psi.ch/bec/bec/-/commit/afbb3ffb7988573f018ae607ea49ca43331db399))

* docs: fixed link to file writer docs ([`01ac862`](https://gitlab.psi.ch/bec/bec/-/commit/01ac8629f50c05c2d69f832b7c2291f50f07a087))

### Fix

* fix: use endpoints instead of simple strings to avoid warning ([`62b2c10`](https://gitlab.psi.ch/bec/bec/-/commit/62b2c106de24c5de955fc619fa6b95f949295d21))

* fix: in set_and_publish, do not call set() to not have a warning ([`700584c`](https://gitlab.psi.ch/bec/bec/-/commit/700584ce3516ba59be56dcfa62cb57a7d693f69f))

## v2.14.0 (2024-06-09)

### Documentation

* docs: improved file writer docs; added plugin info ([`5eefa67`](https://gitlab.psi.ch/bec/bec/-/commit/5eefa6726b4e1d0312d2dc04fe36f3d9ba036c0f))

### Feature

* feat(file_writer): introduced defaultwriter class to simplify the plugin development ([`03c9592`](https://gitlab.psi.ch/bec/bec/-/commit/03c9592b6a72689b4c022678528bfd150bc2f837))

### Fix

* fix(file_writer): set status to running after init ([`f4d494b`](https://gitlab.psi.ch/bec/bec/-/commit/f4d494b8dc1949842fea9b613b1394af603d29a7))

### Refactor

* refactor(file_writer): cleanup ([`8b5abd4`](https://gitlab.psi.ch/bec/bec/-/commit/8b5abd4522424fc898da485c0a9f84018c3d3f08))

### Test

* test(file_writer): added tests to load format from plugins ([`9adbdaf`](https://gitlab.psi.ch/bec/bec/-/commit/9adbdaf0fae5f1f9332790a46073613602c821bc))

## v2.13.8 (2024-06-07)

### Documentation

* docs: move file_writer to extra section in docs ([`8d4a712`](https://gitlab.psi.ch/bec/bec/-/commit/8d4a71269be9350d9f9d55395b851d7f9a997253))

* docs: review documentation for ophyd, scan metadata and file_writer customizations ([`cb4a2f6`](https://gitlab.psi.ch/bec/bec/-/commit/cb4a2f6e62cbf4d756f575e594722a6971cf5258))

* docs: added two more optional steps to the fly scan tutorial ([`ef1a757`](https://gitlab.psi.ch/bec/bec/-/commit/ef1a757a248c36aba9e6ef82ca53fb1bab3be3e2))

### Fix

* fix: add scan_metadata to documentation ([`183152f`](https://gitlab.psi.ch/bec/bec/-/commit/183152fac63e174e5db4c7c0b1a064cddc25702e))

* fix: fix bec.file_writer option to configure writer from command line ([`83334f1`](https://gitlab.psi.ch/bec/bec/-/commit/83334f18c4ac2c8ce1881ac37231c03022f12442))

### Refactor

* refactor: add system_config and review docs ([`a481fda`](https://gitlab.psi.ch/bec/bec/-/commit/a481fdadfe0c1e005b7a9bd35c7a3b8dd15e9756))

* refactor: add changes from MR !614; improve kwargs handling for scan requests ([`3fece3a`](https://gitlab.psi.ch/bec/bec/-/commit/3fece3a063e4b10ed4ed6923a4b7044b0170efb5))

* refactor: remove bec.file_writer, and moved info to metadata, renamed md to metadata in kwargs from scans ([`92bd51e`](https://gitlab.psi.ch/bec/bec/-/commit/92bd51e788233c1597b0aeb317b16642312b9cb0))

## v2.13.7 (2024-06-06)

### Documentation

* docs: refactored scan docs ([`08e0978`](https://gitlab.psi.ch/bec/bec/-/commit/08e0978d2b7a137700fa1c552cbe079a290f32f5))

* docs: added test instructions to fly scan tutorial ([`7cd40ff`](https://gitlab.psi.ch/bec/bec/-/commit/7cd40ffcf597e3b64e87d9206468118b400754d7))

* docs: added tutorial for defining a new fly scan ([`df1fe4d`](https://gitlab.psi.ch/bec/bec/-/commit/df1fe4d64f97244862126d218be7fe9e2ebea925))

### Fix

* fix: adapt to pytest-redis 3.1 ([`0a987c0`](https://gitlab.psi.ch/bec/bec/-/commit/0a987c0815a3173e43dce22e2accef0e87ea284d))

## v2.13.6 (2024-06-05)

### Ci

* ci: fixed pytest redis version for now ([`c6f1204`](https://gitlab.psi.ch/bec/bec/-/commit/c6f12042d3a0d00b1ab9c69a17e829adf76a2c12))

### Fix

* fix: handle redis connection failures more gracefully ([`49425c7`](https://gitlab.psi.ch/bec/bec/-/commit/49425c7eed456f446c837e09c4fa88afedba31ae))

* fix(bec_ipython_client): fixed support for loading hlis from plugins ([`45869aa`](https://gitlab.psi.ch/bec/bec/-/commit/45869aab773d4e288f7c2d4152be140f91f5bb79))

## v2.13.5 (2024-06-05)

### Fix

* fix(bec_lib): fixed msg type serialization ([`05c24e8`](https://gitlab.psi.ch/bec/bec/-/commit/05c24e880bfbf2257c973ec4b451f93918290915))

## v2.13.4 (2024-06-05)

### Fix

* fix(bec_ipython_client): fixed gui startup ([`8f4d89e`](https://gitlab.psi.ch/bec/bec/-/commit/8f4d89e7a49dc7ca9cbbe64e832ddef19b418f16))

## v2.13.3 (2024-06-04)

### Fix

* fix(scan_server): fixed order of reported devices in readout priority ([`64ecbb6`](https://gitlab.psi.ch/bec/bec/-/commit/64ecbb6856de8b108e75f9a4bd2736adb5b4ca74))

## v2.13.2 (2024-06-03)

### Fix

* fix(bec_lib): fixed serialization for message endpoints ([`1be3830`](https://gitlab.psi.ch/bec/bec/-/commit/1be38300abcd0c7cc4a5f5dcf3c72cf19deb27d6))

## v2.13.1 (2024-06-03)

### Fix

* fix: fixed support for mv during scan defs; closes #308 ([`835bf50`](https://gitlab.psi.ch/bec/bec/-/commit/835bf5004ad1c9aaec1792ed20f3ffc613584d31))

## v2.13.0 (2024-06-03)

### Documentation

* docs: improved scan stub docs and glossary ([`e04cf65`](https://gitlab.psi.ch/bec/bec/-/commit/e04cf65f9cbcff4ea8fe3676813e4dce663757a4))

### Feature

* feat(scan_server): added set_with_response and request_is_completed stubs ([`8ac80c1`](https://gitlab.psi.ch/bec/bec/-/commit/8ac80c11ce0e83bb782254b06e2552e8a15c1002))

* feat(scan_server): convert arg inputs to supported scan arg types ([`30b4528`](https://gitlab.psi.ch/bec/bec/-/commit/30b4528de5e448a0c3477d49dff727703de3ed17))

### Fix

* fix(scan_server): worker respects use_scan_progress_report ([`3ad46ef`](https://gitlab.psi.ch/bec/bec/-/commit/3ad46efb148ab9c32e34a6500f1f1af0dbd7144c))

* fix(ipython_client): readback callback must listen to instruction RID ([`c4551d3`](https://gitlab.psi.ch/bec/bec/-/commit/c4551d3b953bc97557e285f350e81b000f7c2cbe))

* fix: minor cleanup ([`8d4a066`](https://gitlab.psi.ch/bec/bec/-/commit/8d4a066832dc45d67b77d13b484d7cd2e565c2f9))

* fix(scan_server): fixed default args ([`0f42a49`](https://gitlab.psi.ch/bec/bec/-/commit/0f42a4926de28252f01d9f9fab53244cc099ca21))

* fix(scan_server): simplify scan args ([`005ff56`](https://gitlab.psi.ch/bec/bec/-/commit/005ff5685609b403b35131cdff0380d8e5b2b742))

* fix(bec_lib): convert devices to strings for scan requests ([`3b176f7`](https://gitlab.psi.ch/bec/bec/-/commit/3b176f7b97087fe87fcfaacd4d575c27be4cbcaf))

### Refactor

* refactor(scan_server): cleanup of scan args ([`3acc13a`](https://gitlab.psi.ch/bec/bec/-/commit/3acc13a8c4fa45765c1b29f446c01df21b056135))

### Test

* test(scan_server): added test for convert_arg_input ([`a302844`](https://gitlab.psi.ch/bec/bec/-/commit/a302844d70659e2d1b074a76c2649a2c15bf0754))

* test: added tests for stubs and contlineflyscan ([`8fed5f6`](https://gitlab.psi.ch/bec/bec/-/commit/8fed5f64a09ea28bb911aaf57a96ba4b50498a56))

## v2.12.6 (2024-05-31)

### Fix

* fix: end the color sequence ([`22be4c4`](https://gitlab.psi.ch/bec/bec/-/commit/22be4c4c6b54133277411e837e9c102aa39685d3))

## v2.12.5 (2024-05-28)

### Fix

* fix: remove deprecated arg speed from deviceconfig ([`67f0bea`](https://gitlab.psi.ch/bec/bec/-/commit/67f0beac75bbeecf69768662e373b96a0839f122))

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

## v2.2.0 (2024-04-11)

### Feature

* feat: add bec_service names to log files ([`329e9ed`](https://gitlab.psi.ch/bec/bec/-/commit/329e9eda5b31f033af4535c01545b4d1ceeb12c6))

## v2.1.0 (2024-04-11)

### Ci

* ci(bec-widgets): environmental variable added to test script for ci ([`8e2fa9b`](https://gitlab.psi.ch/bec/bec/-/commit/8e2fa9b910e2d52da60b0e4db00e608b511eb7ee))

### Feature

* feat(connector): add &#39;unregister&#39; method to cancel subscription to pub/sub ([`e87812a`](https://gitlab.psi.ch/bec/bec/-/commit/e87812a816d06cd19e23705ff4221efe261b588c))

* feat(redis connector): add _execute_callback method, to be able to overwrite how callbacks are run ([`1ddc7ee`](https://gitlab.psi.ch/bec/bec/-/commit/1ddc7eec53994e793cee371cae64474136faf963))

### Fix

* fix(test_fake_redis): TestMessage fixed to pydantic BaseModel ([`eb9c812`](https://gitlab.psi.ch/bec/bec/-/commit/eb9c8125290615c0e15ffa70567ff198d22c30d5))

* fix(redis_connector): support dict in convert_endpointinfo ([`d2942b1`](https://gitlab.psi.ch/bec/bec/-/commit/d2942b1436ed7ddc3c31feb61510f0dc9f6f7f5a))

* fix: .shutdown() will cleanly stop all threads ([`c1c7dd7`](https://gitlab.psi.ch/bec/bec/-/commit/c1c7dd7beaeb46d1ababd301b99d01266baeb26c))

* fix: ensure &#34;newest_only&#34; works as expected in test ([`dc85f49`](https://gitlab.psi.ch/bec/bec/-/commit/dc85f494ed93727e7eb3b207cdddb2db60ceb3f5))

* fix(redis connector): prevent multiple identical connections in &#39;register&#39; ([`344ef50`](https://gitlab.psi.ch/bec/bec/-/commit/344ef508c0be199d5d8ab9b4c4bff3e4778acb87))

### Refactor

* refactor: (un)register to work with pub/sub or stream endpoints ([`93a5a28`](https://gitlab.psi.ch/bec/bec/-/commit/93a5a2854b7408f7ff4ba32863f2cb3918b885e5))

* refactor: make &#39;(un)register_stream&#39; similar to pub/sub registration API

- StreamTopicInfo renamed to StreamSubscriptionInfo
- &#34;cb&#34; field renamed to &#34;cb_ref&#34; (because it is really a weakref)
- removed StreamRegisterMixin class
    - merged with RedisConnector, since there is no other class to mix
      with
- removed need for custom stream listeners
    - differenciation between &#39;direct&#39; reading and &#39;bunch&#39; reading is
      made with a specialized StreamSubscriptionInfo object called
      &#39;DirectReadingStreamSubscriptionInfo&#39;
- use a single events queue for all messages
    - all messages callbacks treated the same, by the same thread
- pay attention to registering multiple times a stream to the same
  callback, and prevent newest_only=True streams to also be registered
with the same callback with newest_only=False ([`e1ad412`](https://gitlab.psi.ch/bec/bec/-/commit/e1ad412be7d224b6169db7cf45b105b287334781))

### Unknown

* tests: improve test_redis_connector_register_stream_newest_only ([`913dd6d`](https://gitlab.psi.ch/bec/bec/-/commit/913dd6dca24cfb23fa562b968062b67db03615d9))

## v2.0.3 (2024-04-11)

### Documentation

* docs(developer): updated developer instructions after bec server refactoring ([`792c5cd`](https://gitlab.psi.ch/bec/bec/-/commit/792c5cdb95e7838d3198171e0dac2533ba73a8a4))

### Fix

* fix: fixed entry points ([`82b4689`](https://gitlab.psi.ch/bec/bec/-/commit/82b4689beb96b3a11ea1c2d5203167cb45746ffa))

### Unknown

* feature/repeat_proj_at_zero ([`8e9ea06`](https://gitlab.psi.ch/bec/bec/-/commit/8e9ea0628482ed241da87f10daa525b7211682a2))

* feature/default_alignment_values_and_signal_check_in_scan ([`d94cff7`](https://gitlab.psi.ch/bec/bec/-/commit/d94cff7649cbeb79dba299748f37b5678aecadf2))

* feature/flomni_updates ([`632fd0c`](https://gitlab.psi.ch/bec/bec/-/commit/632fd0c5fa7bbb88111bf95f647cb86aded8cecf))

## v2.0.2 (2024-04-11)

### Build

* build: fixed install script ([`9813e51`](https://gitlab.psi.ch/bec/bec/-/commit/9813e51f878504d28c3c3f6c11098570c9d78b70))

### Fix

* fix: add raise condition for fetching path from service_config for recovery_device_config dumps ([`0a9a674`](https://gitlab.psi.ch/bec/bec/-/commit/0a9a6747da87e318ed8ec6e4c6e594f05fa7070a))

## v2.0.1 (2024-04-11)

### Fix

* fix: fixed build during semver job ([`0bb8cb0`](https://gitlab.psi.ch/bec/bec/-/commit/0bb8cb0bfbf2ce9ac69f7522ddf92e68eb2aa1e4))

### Unknown

* feature/default_alignment_values_and_signal_check_in_scan ([`b7f28b2`](https://gitlab.psi.ch/bec/bec/-/commit/b7f28b24894ce92defdb2a03de83f5fca2cb755d))

## v2.0.0 (2024-04-10)

### Breaking

* refactor!: moved services to bec_server

All services are now in the bec_server package. This is a breaking change as the standalone import of the services will no longer work. ([`405d12e`](https://gitlab.psi.ch/bec/bec/-/commit/405d12e74a3c7a27aa0e357a1d8438dc5f35b079))

### Ci

* ci: fixed semver job ([`905c46a`](https://gitlab.psi.ch/bec/bec/-/commit/905c46a085a2310fb99aa87f63a8ab17290149cf))

* ci: removed test utils from coverage ([`e9e366c`](https://gitlab.psi.ch/bec/bec/-/commit/e9e366ca1c33e701e1fe7addcf23d2cd0ad58fe1))

### Unknown

* feature/flomni_updates ([`2a7a93e`](https://gitlab.psi.ch/bec/bec/-/commit/2a7a93ef6e2471e2716a481e069e1dea4755b219))

## v1.24.1 (2024-04-10)

### Fix

* fix(scan_server): break out of run loop if signal event is set ([`6edac2f`](https://gitlab.psi.ch/bec/bec/-/commit/6edac2f54d1d1c33f8d1e7329298361a5b1c62f1))

* fix(scan_server): set queue to stopped after reaching a limit error ([`8470f63`](https://gitlab.psi.ch/bec/bec/-/commit/8470f636a2d1db2ff6f1dd68e7db0e18555c085b))

* fix(flomni): wait for cleanup to be finished ([`8660096`](https://gitlab.psi.ch/bec/bec/-/commit/8660096e536f59f04b8fb3f179cdcf7bf078b1cf))

* fix(scan_server): reset worker to running after failed cleanup ([`fa6f2da`](https://gitlab.psi.ch/bec/bec/-/commit/fa6f2da8af434517da2001df9775a2b834132ec3))

* fix(scan_server): restart queue if worker died ([`a59eb9c`](https://gitlab.psi.ch/bec/bec/-/commit/a59eb9c8886a410f0dbaa4351b1b37de72dbdc20))

* fix(scan_server): error during return_to_start was not caught and caused the scan worker to shut down ([`1fa372b`](https://gitlab.psi.ch/bec/bec/-/commit/1fa372b59023210d602c5d5627e34107418e14b7))

### Refactor

* refactor(flomni): fixed formatter ([`bb1d138`](https://gitlab.psi.ch/bec/bec/-/commit/bb1d1380e4f0d8a3898b922e5aef5371ad82bc6d))

### Style

* style(scan_server): fixed formatter ([`9ae8a29`](https://gitlab.psi.ch/bec/bec/-/commit/9ae8a29fe4ed2b1e7b90c58c321180489a2a67e1))

### Unknown

* tests(scan_server): added more tests for the scan server ([`c4ce8c3`](https://gitlab.psi.ch/bec/bec/-/commit/c4ce8c3236d7276958b88f50a6aa603615bd5bb6))

## v1.24.0 (2024-04-10)

### Feature

* feat: Add check for logger to load correct config, add tests ([`2317fd3`](https://gitlab.psi.ch/bec/bec/-/commit/2317fd3df797468dcd583c70221f65a5b2f5ea9b))

### Refactor

* refactor: moved messages to pydantic ([`95ac205`](https://gitlab.psi.ch/bec/bec/-/commit/95ac2055eb30015d9690faf004c5665fa8a4a555))

### Unknown

* tests: fix logger config in scihub ([`3fa544b`](https://gitlab.psi.ch/bec/bec/-/commit/3fa544bef91c5d5f18784f02ac74f1fc87069769))

## v1.23.1 (2024-04-09)

### Fix

* fix: add random order to full end-2-end tests ([`8a47f76`](https://gitlab.psi.ch/bec/bec/-/commit/8a47f76f25b65b9252fa90055074267e207512ae))

* fix: fix logs for ci pipeline ([`28d3dda`](https://gitlab.psi.ch/bec/bec/-/commit/28d3dda2c398baa7251da0b64e42b7704177ffc9))

### Refactor

* refactor(scan_bundler): added more logger outputs ([`8642495`](https://gitlab.psi.ch/bec/bec/-/commit/8642495afa651ba4d70edcc4baf499c44c621eba))

* refactor(bec_lib): prevent devices to appear in multiple args ([`be2330c`](https://gitlab.psi.ch/bec/bec/-/commit/be2330c2219073d6d047b7a5702be8b23994f20e))

* refactor: renamed pointID to point_id ([`d08526f`](https://gitlab.psi.ch/bec/bec/-/commit/d08526f6e9992bfd08a987b8ff4e0d741f558e8e))

## v1.23.0 (2024-04-08)

### Feature

* feat: adapt file writing; log files to common dir and refactoring of filewriter ([`246f271`](https://gitlab.psi.ch/bec/bec/-/commit/246f271bc9404d38e4100c8dbd0094af7b1136f6))

### Fix

* fix: Fix .deepcopy vs copy for metadata from client ([`9ad68ab`](https://gitlab.psi.ch/bec/bec/-/commit/9ad68ab69a67b1fce61682a6fd24716df10b2208))

## v1.22.2 (2024-04-08)

### Documentation

* docs(developer): fixed isort description ([`cb41c6f`](https://gitlab.psi.ch/bec/bec/-/commit/cb41c6f1acadd8652634b76c58a740046f7bf834))

### Fix

* fix(issue #253): split startup in bec entry point in 2 parts, ensure globals are in IPython namespace ([`42625c3`](https://gitlab.psi.ch/bec/bec/-/commit/42625c357e0a74824f79ef59d22cd622da4e4d52))

### Unknown

* added golden ratio options ([`9964f88`](https://gitlab.psi.ch/bec/bec/-/commit/9964f88f92fd7598ce6df397dd4ea111cdcfab46))

* added golden ratio options ([`a3eed5d`](https://gitlab.psi.ch/bec/bec/-/commit/a3eed5d4078b9b308cab6bb12c5e3c84c50b6214))

* golden ratio tomography ([`cb88c4c`](https://gitlab.psi.ch/bec/bec/-/commit/cb88c4cea831a4a24db7489cc6a519b173586fcf))

## v1.22.1 (2024-04-04)

### Ci

* ci: added isort to ci checks ([`7ebf090`](https://gitlab.psi.ch/bec/bec/-/commit/7ebf090f156f0434a0faee84d3ca4aa181d48319))

* ci: allow failure of multi-host test to avoid blocking the pipeline ([`23c0e78`](https://gitlab.psi.ch/bec/bec/-/commit/23c0e783117aaa88eaaa3065e16bd4a8a4df0138))

* ci: fixed support for ophyd branches other than master ([`3bbb03b`](https://gitlab.psi.ch/bec/bec/-/commit/3bbb03bbfacc29b1a2c7f7beff96b85041a3c8ab))

### Documentation

* docs: refactor summary, configure in docs ([`536f2ef`](https://gitlab.psi.ch/bec/bec/-/commit/536f2efc0cbc9e877dfc6c908e413910e5460cb8))

* docs: adapt user installation; closes #246 ([`e669252`](https://gitlab.psi.ch/bec/bec/-/commit/e6692524136595ed20640db49db4420278e3d5cc))

* docs: fix wording ([`8dd3ee0`](https://gitlab.psi.ch/bec/bec/-/commit/8dd3ee0946728fe394e8863d04934d70c1e96ba7))

* docs: address comments ([`2de2e1b`](https://gitlab.psi.ch/bec/bec/-/commit/2de2e1b4bc5fb4cd3060e082fd641dc1c9cafb74))

* docs: Update documentation about ophyd devices ([`04b3bb0`](https://gitlab.psi.ch/bec/bec/-/commit/04b3bb03b9c9697217e7b2fa703581a29a8b61f4))

* docs: add documentation for pytest fixtures provided as pytest plugins ([`4b3851e`](https://gitlab.psi.ch/bec/bec/-/commit/4b3851e2825c5676e6ae8cdf4334296a69546d02))

* docs: added isort to developer instructions ([`720e3c3`](https://gitlab.psi.ch/bec/bec/-/commit/720e3c39eec764824efe5e30edebd449fab1e92d))

### Fix

* fix(bec_client): unnecessary complex exit thread ([`9377a84`](https://gitlab.psi.ch/bec/bec/-/commit/9377a84f8b3e3ffc70bd81a08878d634a4f63db7))

### Refactor

* refactor: bec startup script using setup entry point ([`ca16c1b`](https://gitlab.psi.ch/bec/bec/-/commit/ca16c1bb6ed7430ad49340478d315032962352fc))

### Unknown

* tests: fix test_scans filename in end-2-end-conda-* tests ([`5ea3b50`](https://gitlab.psi.ch/bec/bec/-/commit/5ea3b50199d3f0450630fac67cd8bb7cf68c7cad))

* tests: exclude bec_lib.tests ([`2efb038`](https://gitlab.psi.ch/bec/bec/-/commit/2efb0385b3d0f1acf2034999d52e359946972f19))

* doc: add docstring and documentation for computedsignal; close #221 #229 #230 ([`df34f2a`](https://gitlab.psi.ch/bec/bec/-/commit/df34f2a4808d98eaf0d66a351ceed496b2b19234))

## v1.22.0 (2024-03-28)

### Build

* build: added isort to setups and pre-commit ([`424377b`](https://gitlab.psi.ch/bec/bec/-/commit/424377b8f2cee203aa1f1422cf8704bd20533556))

### Ci

* ci: added web as trigger for downstream pipelines ([`b46aac7`](https://gitlab.psi.ch/bec/bec/-/commit/b46aac7a8ae6d3eeacacb7dc673e42ad7f55c97f))

* ci: added CI variables for downstream pipelines and web source ([`b3ebe4e`](https://gitlab.psi.ch/bec/bec/-/commit/b3ebe4e35dc29c03caa4e3a7dae3bdc24542bbe0))

### Documentation

* docs(scan_server): improved docs for scan stubs ([`c5f18e5`](https://gitlab.psi.ch/bec/bec/-/commit/c5f18e56a5f382a18ffc048907fea917f101bf75))

### Feature

* feat: &#39;bec_services_config_file_path&#39; and &#39;bec_test_config_file_path&#39; fixtures ([`d3f3071`](https://gitlab.psi.ch/bec/bec/-/commit/d3f30712f957ecdaa5bd52d98e4acce060a8b1d9))

* feat(tests): fixtures for end-2-end tests (available as a pytest plugin) ([`b24f65a`](https://gitlab.psi.ch/bec/bec/-/commit/b24f65a2a16f7048c9370ef576dede63da40e00e))

### Fix

* fix: temporary make &#39;end-2-end tests with multiple hosts&#39; manual ([`54bfe36`](https://gitlab.psi.ch/bec/bec/-/commit/54bfe36fe6becc80b3b893def94a14e0ed1ecdab))

* fix: temporary fix, do not check for dangling threads in device server tests ([`a1cddc0`](https://gitlab.psi.ch/bec/bec/-/commit/a1cddc0639b509531341beb24003479158ea8cd7))

* fix(tests): rename files to prevent error during tests collection with 2 files with same name ([`6fcef45`](https://gitlab.psi.ch/bec/bec/-/commit/6fcef459b855968e3e179d1d4ae48a0f00487bd2))

* fix(tests): ensure all tests do not leak threads ([`f371098`](https://gitlab.psi.ch/bec/bec/-/commit/f37109873a0c173dc56a254fdcfca52d8c3ad215))

### Refactor

* refactor(CI): end-to-end tests on the same host, with flushing and on multiple hosts, without flushing

Environment variables are used to parametrize dockerfile and scripts
Introduce &#39;buildah&#39; and &#39;podman&#39; instead of docker to build and run
images.
Simplification of Dockerfiles and CI scripts. ([`57f4115`](https://gitlab.psi.ch/bec/bec/-/commit/57f4115dfb24012ca49ab57d51ab0c1d94fe68c3))

* refactor(tests): new &#39;subprocess_start&#39; with &#39;no-tmux&#39; option ([`b5ca2c3`](https://gitlab.psi.ch/bec/bec/-/commit/b5ca2c30dd99fb8be5081b6a22fcd8f9b7b367bb))

* refactor: renamed queueID to queue_id ([`996809f`](https://gitlab.psi.ch/bec/bec/-/commit/996809f3a0915e3562c5d6f5cf9266b13508e6b6))

* refactor: renamed scanID to scan_id ([`01b4e9c`](https://gitlab.psi.ch/bec/bec/-/commit/01b4e9cc68efc3770a328e2165b69026186359c1))

### Style

* style: fix pep8 compliance ([`9b6ac54`](https://gitlab.psi.ch/bec/bec/-/commit/9b6ac547e7158df9351f485543c849419bc00858))

* style: apply isort to the whole codebase, clean unused imports ([`2d66967`](https://gitlab.psi.ch/bec/bec/-/commit/2d66967e04a3cbcecde4027d4f0f5ecb1c3c640d))

### Test

* test(scan_bundler): refactored scan bundler tests and added thread check ([`8f29b44`](https://gitlab.psi.ch/bec/bec/-/commit/8f29b44ddedda424664cc6a6753fbc533b767cef))

### Unknown

* flomni-tomo_scan_improvements ([`d873e49`](https://gitlab.psi.ch/bec/bec/-/commit/d873e49ebfe98ddb5381fc052002af8b3613fece))

## v1.21.1 (2024-03-22)

### Fix

* fix: fixed cleanup execution ([`fd02675`](https://gitlab.psi.ch/bec/bec/-/commit/fd02675256bd5160c8d658871019bff3705d60cd))

* fix(bec_client): report cleanup ([`e7e5413`](https://gitlab.psi.ch/bec/bec/-/commit/e7e5413ac4e0e6f829797c314f558a26accc78be))

* fix(scan_server): shut down scan if scan worker is stopped ([`9e626a0`](https://gitlab.psi.ch/bec/bec/-/commit/9e626a0c2fd15e77259fc8a1c32fc97892e5a830))

### Refactor

* refactor(scan_bundler): reduced logger level for msgs without scanID ([`e6c7098`](https://gitlab.psi.ch/bec/bec/-/commit/e6c7098f7da52a6b2b39a3a19a4694b1f8ef374b))

* refactor(bec_client): fixed formatter ([`53070d9`](https://gitlab.psi.ch/bec/bec/-/commit/53070d94d7063abf9bdc6e7ca154728be5a0a95f))

### Unknown

* flomni-improvements ([`03f9eeb`](https://gitlab.psi.ch/bec/bec/-/commit/03f9eeb4721a1e9be4395d942a4530a8e0e45ec2))

* flomni-improvements ([`cf90614`](https://gitlab.psi.ch/bec/bec/-/commit/cf90614bb27ac1adbf3147a21b90a69b312ab5dd))

## v1.21.0 (2024-03-21)

### Feature

* feat: add &#34;count&#34; keyword arg to stream connector .get_last(), to retrieve last &#34;count&#34; items

count=1 by default ([`e281b6a`](https://gitlab.psi.ch/bec/bec/-/commit/e281b6aaa10567538476e71fa307fc266216ef9a))

### Fix

* fix: validate endpoint for .get_last (#236), enhance endpoint validation ([`da5df48`](https://gitlab.psi.ch/bec/bec/-/commit/da5df48008216cd609d47bebbf9a6f90b050ba53))

## v1.20.6 (2024-03-20)

### Fix

* fix: get username using standard &#34;getpass&#34; module ([`06b4afa`](https://gitlab.psi.ch/bec/bec/-/commit/06b4afae4d2979e0bddc22d185d272b1f232c548))

## v1.20.5 (2024-03-20)

### Fix

* fix(bec_lib): fixed error propagation after client refactoring ([`eb5774a`](https://gitlab.psi.ch/bec/bec/-/commit/eb5774a5da157834ff0a4f0e1e03ac6b7237267d))

### Test

* test(bec_lib): fixed tests for endpoint structure ([`6270107`](https://gitlab.psi.ch/bec/bec/-/commit/62701077bd0cfe19762cb9eca2fc95d7d53c6609))

## v1.20.4 (2024-03-20)

### Fix

* fix(device_server): fixed readback for automonitor ([`7a3e1c2`](https://gitlab.psi.ch/bec/bec/-/commit/7a3e1c21ee200484942ad0eafe748640ebeaf1f8))

## v1.20.3 (2024-03-20)

### Fix

* fix(bec_lib): fixed client shutdown for failed inits ([`fc8ff9b`](https://gitlab.psi.ch/bec/bec/-/commit/fc8ff9bd7508119c303f5c589e05aab0ade17d77))

## v1.20.2 (2024-03-20)

### Fix

* fix(scan_server): improved shutdown procedure ([`2417eb5`](https://gitlab.psi.ch/bec/bec/-/commit/2417eb5e321944b10ef2568135828121f0023537))

* fix(scan_server): fixed queue update ([`926f028`](https://gitlab.psi.ch/bec/bec/-/commit/926f0287be5dffe63c9e318b19908431abbc54de))

### Refactor

* refactor: cleanup of BECClient ([`d1834a1`](https://gitlab.psi.ch/bec/bec/-/commit/d1834a13c121432f08367775f17bd84498b9cb1a))

### Test

* test: reduced time for flyer sim ([`70b4b55`](https://gitlab.psi.ch/bec/bec/-/commit/70b4b55c31f8b3d434dcf05013f0424d8571e5ae))

## v1.20.1 (2024-03-20)

### Fix

* fix(bec_lib): fixed return value for put; closes #234 ([`9109177`](https://gitlab.psi.ch/bec/bec/-/commit/9109177a2e395eefb87f96750d3068e6936b2a25))

* fix(bec_lib): added queue update ([`1ee251d`](https://gitlab.psi.ch/bec/bec/-/commit/1ee251d6e75fd84c9644e8cdc7b61ba99d0d155c))

## v1.20.0 (2024-03-20)

### Documentation

* docs: added reference to bec-server attach ([`b92d757`](https://gitlab.psi.ch/bec/bec/-/commit/b92d757c059f457a81a0324ca079f757f5e03d3b))

### Feature

* feat(bec_server): added cli option to attach to the tmux session ([`5115c31`](https://gitlab.psi.ch/bec/bec/-/commit/5115c316763c5674fd438ee0702e8f42c2f92109))

## v1.19.0 (2024-03-19)

### Feature

* feat(device_server): added subscription to all auto monitored signals ([`816da5c`](https://gitlab.psi.ch/bec/bec/-/commit/816da5cbc673b788973bd302fbf55cfd787e1c50))

## v1.18.1 (2024-03-18)

### Fix

* fix(bec_lib): added pyepics compliant wait function to put ([`eb15e3a`](https://gitlab.psi.ch/bec/bec/-/commit/eb15e3ae493d5046c20965846c702f6acfb055dc))

* fix: unified access to limits; closes #233 ([`648b720`](https://gitlab.psi.ch/bec/bec/-/commit/648b720a9828c7ed6d7ac3c3750b80d18b8d0e24))

## v1.18.0 (2024-03-18)

### Feature

* feat(device_server): simplified access to ophyd objects in the device server ([`9af29e4`](https://gitlab.psi.ch/bec/bec/-/commit/9af29e48668d91a1e79da6c0c70608a24ad1cddc))

## v1.17.0 (2024-03-15)

### Feature

* feat(bec_client): becfigure start automatically on startup ([`9092122`](https://gitlab.psi.ch/bec/bec/-/commit/9092122e67bf78b62d4d2afe4fdeaa2fd154495f))

### Fix

* fix(bec_client): fixed gui shutdown procedure ([`15649ac`](https://gitlab.psi.ch/bec/bec/-/commit/15649acc5eae4a45b20ec8f2039c4d4f32bc41fd))

## v1.16.1 (2024-03-15)

### Fix

* fix: fix scan_export and unit tests ([`914b332`](https://gitlab.psi.ch/bec/bec/-/commit/914b332781683b2c738b3693341cebdcb799393e))

* fix(scan_bundler): allow missing entries in scan info ([`7349545`](https://gitlab.psi.ch/bec/bec/-/commit/7349545ee056da9ec226dc6be9dff12748ce2066))

* fix(scan_segments): segments should not include the entire scan status ([`46ae12c`](https://gitlab.psi.ch/bec/bec/-/commit/46ae12ccbe9c643f42a6d90014e0f37ecd16589d))

### Test

* test: fix formatting ([`14a0088`](https://gitlab.psi.ch/bec/bec/-/commit/14a0088dea830e82cae551d56c7c06aa5aa18eda))

## v1.16.0 (2024-03-15)

### Feature

* feat(device_server): added guards against using protected methods; closes #228 ([`67e8eeb`](https://gitlab.psi.ch/bec/bec/-/commit/67e8eeb255fabf44ed00605f056066b111791d2c))

* feat(bec_lib): added endpoint for gui heartbeats ([`01066dd`](https://gitlab.psi.ch/bec/bec/-/commit/01066dd777e5800f69709e9f76fc192bd9a75a25))

### Fix

* fix(bec_lib): fixed support in dap for scan reports ([`0666013`](https://gitlab.psi.ch/bec/bec/-/commit/0666013d909fa72f500179f0ce6926588bed9249))

## v1.15.0 (2024-03-15)

### Feature

* feat(bec_lib): added started flag to bec client ([`e8eba90`](https://gitlab.psi.ch/bec/bec/-/commit/e8eba9049ae33b5b83615ced8d2526dde54a5c7d))

## v1.14.6 (2024-03-15)

### Documentation

* docs: added bec_plugins link to developer.md ([`911192d`](https://gitlab.psi.ch/bec/bec/-/commit/911192d566255dcf19e5c80442baeddb13e26908))

### Fix

* fix(bec_lib): device.describe should not be an rpc method ([`42fae6a`](https://gitlab.psi.ch/bec/bec/-/commit/42fae6a70baa01565599899437a3bdca1d4783ee))

### Refactor

* refactor(bec_lib): minor cleanup of device status ([`1c6662c`](https://gitlab.psi.ch/bec/bec/-/commit/1c6662cfe3f67884bc3bb073d34ca56077a00a0f))

### Test

* test(bec_lib): minor cleanup ([`6316f4f`](https://gitlab.psi.ch/bec/bec/-/commit/6316f4f762e7f5665df7cb7581c7e73a4b0e4311))

## v1.14.5 (2024-03-14)

### Documentation

* docs(bec_lib): improved doc string for device module ([`c605846`](https://gitlab.psi.ch/bec/bec/-/commit/c605846adeee080dbdecd55d5f758e2acd884d83))

* docs(bec_lib): added module docs ([`7031c24`](https://gitlab.psi.ch/bec/bec/-/commit/7031c2483163eb3268760b5ecd4888c9c5b6b372))

### Fix

* fix(bec_lib): fixed status timeout ([`c4f0a18`](https://gitlab.psi.ch/bec/bec/-/commit/c4f0a18e7317caf54e95e7c7b1f09bf033e65380))

### Test

* test(scan_server): fixed thread leak in scan server tests ([`fe69b6e`](https://gitlab.psi.ch/bec/bec/-/commit/fe69b6e11cee239fc9799f135d83268761c3b6a8))

### Unknown

* small adjustments while working with flomni ([`5400e5f`](https://gitlab.psi.ch/bec/bec/-/commit/5400e5ffd5b81f9c5e7cedb7f043e523f641567f))

## v1.14.4 (2024-03-12)

### Documentation

* docs: updated readme ([`c490574`](https://gitlab.psi.ch/bec/bec/-/commit/c490574b9bafc217bf29bec9b087fa75c50abab6))

### Fix

* fix(bec_lib): don&#39;t call rpc on jedi completer ([`8a6a968`](https://gitlab.psi.ch/bec/bec/-/commit/8a6a968cc8c31fbb5fb20ce872b8bbdc76039ee8))

* fix(bec_lib): added tab complete for property vars ([`ef531d0`](https://gitlab.psi.ch/bec/bec/-/commit/ef531d0d4a1848ac5917b56eebea385fac9b7a4c))

### Refactor

* refactor(bec_lib): fixed type hint ([`8c8dffb`](https://gitlab.psi.ch/bec/bec/-/commit/8c8dffb5a6c1627cc2b02943e9ece4846db087ca))

### Unknown

* doc: psi-python311/2024.02 is now stable ([`bcf605b`](https://gitlab.psi.ch/bec/bec/-/commit/bcf605b0f6e5a220e81a672ec1114712f3860989))

## v1.14.3 (2024-03-12)

### Fix

* fix(bec_lib): fixed dataset number setter ([`5dcffe0`](https://gitlab.psi.ch/bec/bec/-/commit/5dcffe022c2a5d2c1e2cb50265f5d0b1cefe547a))

## v1.14.2 (2024-03-12)

### Fix

* fix: remove debug prints from livetable ([`7efb387`](https://gitlab.psi.ch/bec/bec/-/commit/7efb3878d8687ba4e747c99e517d4c6df40c6965))

* fix: add recovery_config files to .gitignore ([`6201757`](https://gitlab.psi.ch/bec/bec/-/commit/62017574baea74dfff5f4d13ea1d1886ee6581a8))

## v1.14.1 (2024-03-11)

### Ci

* ci: removed &#39;allow_failure&#39; flag from bec-widgets ([`ad5e101`](https://gitlab.psi.ch/bec/bec/-/commit/ad5e101bb6961a9c83bc8b31e1d91daf91c71197))

### Fix

* fix(scan_server): added cm for preventing race conditions within queue updates ([`b98dd52`](https://gitlab.psi.ch/bec/bec/-/commit/b98dd52d6ac4bce23c0916028810340e1af74649))

### Test

* test: cache test config ([`ec33aa5`](https://gitlab.psi.ch/bec/bec/-/commit/ec33aa5fdf48dc39db10b603dac67c018f44eacb))

### Unknown

* various_fixes_and_printouts ([`8ed1130`](https://gitlab.psi.ch/bec/bec/-/commit/8ed113076de0adaf4c1b49919290e2ae7c4e55ba))

## v1.14.0 (2024-03-10)

### Ci

* ci: added pseudo signal to config ([`eeb83d3`](https://gitlab.psi.ch/bec/bec/-/commit/eeb83d3ba04746019dbc0c36ec6c817a39b7d72f))

### Feature

* feat: added support for computed signals ([`720d6e2`](https://gitlab.psi.ch/bec/bec/-/commit/720d6e210df11071f0d5c30442e6e50e34833844))

### Fix

* fix(bec_lib): fixed signal update ([`689e2d9`](https://gitlab.psi.ch/bec/bec/-/commit/689e2d968c4967bcaf8d19e2756997898671bf79))

* fix(scihub): rejected config should raise ([`af2e4c5`](https://gitlab.psi.ch/bec/bec/-/commit/af2e4c58e1143b39e58f5e4f292d66dfcd36123f))

### Test

* test(bec_lib): added tests for computed signal ([`286e05d`](https://gitlab.psi.ch/bec/bec/-/commit/286e05d2b34e44be7f1a9f2baaec50d71098568f))

* test: added e2e test for pseudo signal ([`8b85165`](https://gitlab.psi.ch/bec/bec/-/commit/8b85165bc4afcb044048e3b239b4dc7465d2636b))

## v1.13.3 (2024-03-10)

### Fix

* fix(bec_lib): fixed bug that caused data to be modified when using xadd; closes #220 ([`3dbb8a0`](https://gitlab.psi.ch/bec/bec/-/commit/3dbb8a00a1439e3030d9406a223040ef99cb60a8))

## v1.13.2 (2024-03-10)

### Fix

* fix(bec_lib): shutdown loguru ([`3f8d655`](https://gitlab.psi.ch/bec/bec/-/commit/3f8d655b2e199268bd23746fd0fe96bc316fcb8c))

* fix(bec_lib): daemonized connector threads ([`be1f3fd`](https://gitlab.psi.ch/bec/bec/-/commit/be1f3fd140af8fdf6216f41b92e92ed9126d3791))

## v1.13.1 (2024-03-10)

### Fix

* fix(scan_server): fixed flomni init; added tests ([`a3ceac7`](https://gitlab.psi.ch/bec/bec/-/commit/a3ceac7a95f593da23575aaf60693519d4789764))

### Test

* test: fixed compliance with fakeredis &gt; 2.21.1 ([`56c0d7a`](https://gitlab.psi.ch/bec/bec/-/commit/56c0d7ad6ce42b715750daf136cc7fa74fa9c3d1))

* test: fixed flomni fermat scan tests ([`8c53e5b`](https://gitlab.psi.ch/bec/bec/-/commit/8c53e5b090d947261376565da130da1cd55ca3e6))

* test: fixed test ([`04d8f1b`](https://gitlab.psi.ch/bec/bec/-/commit/04d8f1b0d5102212a53c2ee7e47d6169209812cf))

## v1.13.0 (2024-03-10)

### Feature

* feat: remove asyncio from BECIPythonclient to support jupyter notebook output for progressbar ([`f9c1e81`](https://gitlab.psi.ch/bec/bec/-/commit/f9c1e818e0c1aa43947c6c82e052af3f162338fa))

### Refactor

* refactor: remove all pytest-asyncio and asyncio dependencies ([`7413841`](https://gitlab.psi.ch/bec/bec/-/commit/741384130ff64cb995fe809aa7cc08af6fcf557d))

### Test

* test: remove asyncio from tests ([`1de701c`](https://gitlab.psi.ch/bec/bec/-/commit/1de701cd9b5d60a11fff7b915ad23f69431c16ae))

### Unknown

* added some verbosity to init routine ([`bc4f984`](https://gitlab.psi.ch/bec/bec/-/commit/bc4f984ceb4163f21c3f40c599b8072ba75de38e))

* added some verbosity to init routine ([`63fdf5a`](https://gitlab.psi.ch/bec/bec/-/commit/63fdf5adf24995d22cfdf7ddf7be900c11a3b973))

## v1.12.9 (2024-03-06)

### Ci

* ci: pylint cleanup ([`776f5cb`](https://gitlab.psi.ch/bec/bec/-/commit/776f5cb8967df1210a3df35a450c85d9d63eb90c))

### Documentation

* docs(bec_lib): improved endpoint doc strings ([`656478f`](https://gitlab.psi.ch/bec/bec/-/commit/656478f784440b91ada8fb1da1d3957276079765))

* docs(bec_lib): updated doc strings ([`969b0a0`](https://gitlab.psi.ch/bec/bec/-/commit/969b0a02f842a8d9666277fa5c4cc98344b8b0f6))

### Fix

* fix(bec_lib): fixed support for lists in redis stream subscriptions ([`d4b7b42`](https://gitlab.psi.ch/bec/bec/-/commit/d4b7b42f4608464da417435350a0c73f7665a44f))

* fix(bec_lib): added missing unsubscribe from streams ([`75cd651`](https://gitlab.psi.ch/bec/bec/-/commit/75cd6512ea4e0b00ad320d16f4298ca9f79d8105))

* fix(bec_lib): fixed support for redis streams ([`7578395`](https://gitlab.psi.ch/bec/bec/-/commit/757839534c75bd3a8110256cdfd770f770a195e0))

### Refactor

* refactor(bec_lib): changed connector to use abstract methods ([`d35b992`](https://gitlab.psi.ch/bec/bec/-/commit/d35b992262f6b7f95b60b46dba6412dc3368785b))

### Test

* test(bec_lib): added more tests for the redis connector ([`7ca93d7`](https://gitlab.psi.ch/bec/bec/-/commit/7ca93d74121c753a33ef9a1170accb85bd8a2515))

* test(bec_lib): minor cleanup ([`93c8ec6`](https://gitlab.psi.ch/bec/bec/-/commit/93c8ec66f9984b603926b29b831dc6f62f2af44e))

## v1.12.8 (2024-03-06)

### Ci

* ci: drop python/3.9 ([`d16268c`](https://gitlab.psi.ch/bec/bec/-/commit/d16268ce81e67b9d6cb5e1f153d52d61366c2b80))

### Documentation

* docs: updated contributing.md ([`af2bd27`](https://gitlab.psi.ch/bec/bec/-/commit/af2bd273d510f08f420f39ec519d1a97ac8a1cb1))

* docs: typo ([`4ac0bbc`](https://gitlab.psi.ch/bec/bec/-/commit/4ac0bbca1631ed5226458307f7ad35d155617328))

* docs: fixed last comments ([`aadbb01`](https://gitlab.psi.ch/bec/bec/-/commit/aadbb01a947ae5419dff7c18837ab8ea9b75d78c))

* docs: adress comments ([`d556f84`](https://gitlab.psi.ch/bec/bec/-/commit/d556f842353e7ef335309fb42025d00de193b627))

* docs: update documentation on the simulation ([`0ec3dac`](https://gitlab.psi.ch/bec/bec/-/commit/0ec3dac85fd03413c2cf79b5881e8dffbecd2877))

### Fix

* fix: added backward compatibility for scan numbers and dataset numbers ([`9ff2278`](https://gitlab.psi.ch/bec/bec/-/commit/9ff2278c38b9fcb671c5591f15fda9473155fbe3))

* fix: account is now a variablemessage ([`79d57b5`](https://gitlab.psi.ch/bec/bec/-/commit/79d57b509d20451c73a0442adf477ae4299e9dc6))

* fix: pre-scan macros are now using a VariableMessage ([`4239576`](https://gitlab.psi.ch/bec/bec/-/commit/4239576c94c44041f395261b42de1056de8c0d76))

* fix: logbook is now using a credentialsmessage ([`b62960f`](https://gitlab.psi.ch/bec/bec/-/commit/b62960f6e697b116ffc4f3c5fded0c6bcd9ea4e2))

* fix: scan_number and dataset_number is now a VariableMessage ([`f698605`](https://gitlab.psi.ch/bec/bec/-/commit/f698605579766536f1ec1e653e9d5e3dfd44166e))

### Refactor

* refactor: removed remaining loads/dumps ([`2fd1953`](https://gitlab.psi.ch/bec/bec/-/commit/2fd1953a551bcb1a0868034b28c629a2add64790))

* refactor: endpoints return EndpointInfo object instead of string ([`a4adb64`](https://gitlab.psi.ch/bec/bec/-/commit/a4adb64f5fb083e4d3c20fe30247ce3b480e68cb))

### Test

* test(scan_server): fixed threading-related issue that caused test to fail from time to time ([`ae07b9f`](https://gitlab.psi.ch/bec/bec/-/commit/ae07b9fab67cbcdef88ced4cb14c6c546568936f))

## v1.12.7 (2024-03-04)

### Ci

* ci: fixed pylint check ([`7094092`](https://gitlab.psi.ch/bec/bec/-/commit/7094092f130547b6f12ff3dbec95a1e4553cfca2))

* ci: removed flaky from ci pipeline ([`9b54ebb`](https://gitlab.psi.ch/bec/bec/-/commit/9b54ebb3ac6eae7e29896644c9545385e9ac41e5))

### Fix

* fix(scihub): fixed scibec upload for large scans ([`2b680ee`](https://gitlab.psi.ch/bec/bec/-/commit/2b680eee1ea51c1875ef8e1fea9f3135a3e52899))

### Refactor

* refactor(file_writer): cleanup ([`d0a04de`](https://gitlab.psi.ch/bec/bec/-/commit/d0a04de641db149097aa4cc6015dd0492c1aac3e))

### Test

* test: replaced flaky with pytest-retry ([`c2c5d33`](https://gitlab.psi.ch/bec/bec/-/commit/c2c5d33f04654c4d88b08b92567a862bc47577eb))

## v1.12.6 (2024-03-01)

### Fix

* fix: fix dap test, cleanup redudant config values ([`4f63fef`](https://gitlab.psi.ch/bec/bec/-/commit/4f63fef18c512eadbf339629e9780b82d878ea37))

### Test

* test: add proxy to test config ([`cb26a2a`](https://gitlab.psi.ch/bec/bec/-/commit/cb26a2a59211ad5a695593b0e7131a9d51c4f2ac))

## v1.12.5 (2024-03-01)

### Fix

* fix(scan_server): fixed queue pop for pending requests ([`14f94cd`](https://gitlab.psi.ch/bec/bec/-/commit/14f94cd96071feb0885b010af7576532baea553e))

## v1.12.4 (2024-02-27)

### Fix

* fix(bec_lib): exclude disabled devices in device filters ([`388baae`](https://gitlab.psi.ch/bec/bec/-/commit/388baae9f117120f4f3db29e0c0db03cbb78b54c))

### Test

* test(config): made disabled device a monitored device ([`3979a1e`](https://gitlab.psi.ch/bec/bec/-/commit/3979a1e5e21b79f2171f831f5badfad3c1cb3209))

### Unknown

* update flomni config ([`89807cf`](https://gitlab.psi.ch/bec/bec/-/commit/89807cfee9fbed486bb76ab16eb1d159ce8214ce))

## v1.12.3 (2024-02-27)

### Fix

* fix(scan_server): stage should only include monitored, baseline and async devices ([`05a83bd`](https://gitlab.psi.ch/bec/bec/-/commit/05a83bd4ac1fe898863f24bac1a139da0836a46a))

## v1.12.2 (2024-02-26)

### Fix

* fix(disconnection): mitigate effects on disconnection from redis ([`4d73cf8`](https://gitlab.psi.ch/bec/bec/-/commit/4d73cf8a071493ec997ca08efc8518672c7f5034))

* fix(redis_connector): add producer(), consumer() for compatibility with old code

With deprecation warnings ([`f60a012`](https://gitlab.psi.ch/bec/bec/-/commit/f60a012ef6453742bb8c830e479325bfb9254b87))

* fix(scan_manager): ensure robustness in __str__ ([`db53b1f`](https://gitlab.psi.ch/bec/bec/-/commit/db53b1f5dc73279c6764d1f4dd875f32304d1f5d))

* fix(tests): ensure redis is installed ([`bbd036e`](https://gitlab.psi.ch/bec/bec/-/commit/bbd036e769bb6093d1890fceb23e005baa644888))

### Unknown

* refactor!(connector): unify connector/redis_connector in one class ([`b92a79b`](https://gitlab.psi.ch/bec/bec/-/commit/b92a79b0c063d07bd811a35b4a72104a22f2b60e))

## v1.12.1 (2024-02-24)

### Fix

* fix(scan_server): fixed expected message type for device progress update ([`1236069`](https://gitlab.psi.ch/bec/bec/-/commit/1236069b3604607288f9f0e1dccd3994d014f928))

## v1.12.0 (2024-02-24)

### Feature

* feat: added flomni scan and user scripts ([`c376de8`](https://gitlab.psi.ch/bec/bec/-/commit/c376de8e8436380f65ba96b2e88572077830f1d9))

### Refactor

* refactor: minor cleanup ([`b8f8467`](https://gitlab.psi.ch/bec/bec/-/commit/b8f846749b8042e6c6ce6bcb1f05bc191da96f42))

## v1.11.1 (2024-02-23)

### Fix

* fix(scan_bundler): fixed scan bundler update ([`2e5b147`](https://gitlab.psi.ch/bec/bec/-/commit/2e5b147a2c9ccd6ca7169f45f0431ed1df902b0f))

* fix(scan_server): reverted changes to monitor scan ([`636e060`](https://gitlab.psi.ch/bec/bec/-/commit/636e0609f2d05ea079661872858084b3f9b3847e))

* fix(file_writer): fixed data update ([`16f8f30`](https://gitlab.psi.ch/bec/bec/-/commit/16f8f30ea6fc15173abbfccee65b869018659bca))

* fix(scan_server): fixed inheritance for flyers ([`5f80220`](https://gitlab.psi.ch/bec/bec/-/commit/5f80220fa2d062112dd5770b3485dd478ead63f8))

### Refactor

* refactor: renamed enforce_sync to monitor_sync ([`63a8dd8`](https://gitlab.psi.ch/bec/bec/-/commit/63a8dd814c99296646c1429af6c31a5d625c5a8d))

## v1.11.0 (2024-02-23)

### Feature

* feat: Add Ophyd DeviceProxy to backend for simulation framework, delayed init of proxies ([`d37c5e7`](https://gitlab.psi.ch/bec/bec/-/commit/d37c5e739120baad5ffef22888ba264a74663e63))

## v1.10.0 (2024-02-23)

### Ci

* ci: added nightly e2e test ([`1fe6805`](https://gitlab.psi.ch/bec/bec/-/commit/1fe680555098e960689ad423e0f2473807640d40))

### Feature

* feat(scihub): added config reply handler for device_server updates ([`29a1d19`](https://gitlab.psi.ch/bec/bec/-/commit/29a1d19504d6cbfb4a4601106d5341aadb0f43f7))

* feat(device_server): connection errors and init errors are separated and forwarded ([`c2214b8`](https://gitlab.psi.ch/bec/bec/-/commit/c2214b86468a2ac590ee3fd5eda19734dbac1c26))

* feat(bec_lib): report on failed devices; save recovery file to disk ([`8062503`](https://gitlab.psi.ch/bec/bec/-/commit/806250300e472a780329e6438c1891565481d8f7))

* feat(bec_lib): added config history endpoint ([`ee7ecef`](https://gitlab.psi.ch/bec/bec/-/commit/ee7ecef8d52320356f2190620bc3e42fa37db304))

### Fix

* fix(bec_lib): fixed service init ([`b09b5ff`](https://gitlab.psi.ch/bec/bec/-/commit/b09b5ff7cddd0d13c6c4a2d55d00914b131e59fd))

* fix(bec_lib): fix after refactoring ([`0337f13`](https://gitlab.psi.ch/bec/bec/-/commit/0337f13d0453ca1fac77413d757746f2bc06eb95))

* fix(scihub): added updated config flag to detect failed validations ([`3a133bf`](https://gitlab.psi.ch/bec/bec/-/commit/3a133bf7d44a9578587e5bbee484183a21e9cc7c))

* fix(bec_lib): fixed config helper for failed config updates ([`f603419`](https://gitlab.psi.ch/bec/bec/-/commit/f6034191f5763495130cab25edc5d600d0da274d))

* fix(bec_lib): fixed bl_checks cleanup ([`05b00da`](https://gitlab.psi.ch/bec/bec/-/commit/05b00dadbbabffc5efd32e9621336e335564db76))

* fix(bec_lib): fixed service id assignment ([`3826d41`](https://gitlab.psi.ch/bec/bec/-/commit/3826d410527177acce339e307a17c2943a921aa4))

* fix(bec_lib): save guard device manager init ([`fcbc240`](https://gitlab.psi.ch/bec/bec/-/commit/fcbc2402e437a756c11b09f5d1ce9a5351a0cc54))

### Refactor

* refactor(bec_lib): minor cleanup ([`16b9e9c`](https://gitlab.psi.ch/bec/bec/-/commit/16b9e9ca322f3d7474f9230d9b13c887ca20569c))

### Test

* test(bec_lib): added config test for invalid device class ([`32df081`](https://gitlab.psi.ch/bec/bec/-/commit/32df081906db6c80dfb572828bc06446b7134cba))

* test(scibec): fixed expected return values ([`79cd2ff`](https://gitlab.psi.ch/bec/bec/-/commit/79cd2ff2f696713f405ce575bb8dbce26e49e8e8))

* test(bec_lib): added tests for config updates; added threads check ([`67b96b9`](https://gitlab.psi.ch/bec/bec/-/commit/67b96b9a6f96346e23f9b0eac9b3ac642e447d13))

* test: fixed tests ([`e5aeb51`](https://gitlab.psi.ch/bec/bec/-/commit/e5aeb510bfd0a477d817a45007a66b89f83bdd7f))

## v1.9.0 (2024-02-22)

### Feature

* feat(bec_lib): added json serializer ([`25366c0`](https://gitlab.psi.ch/bec/bec/-/commit/25366c09638cf4e005ee4a75d64cf8f9eeba00ca))

### Fix

* fix(scihub): fixed data serialization before upload to scibec ([`eae1d61`](https://gitlab.psi.ch/bec/bec/-/commit/eae1d617d6c44a933e7e86ea86e35d380d323f6a))

* fix(scihub): fixed error handling ([`fd3cb02`](https://gitlab.psi.ch/bec/bec/-/commit/fd3cb025c50c61f3384d44abc8c234371952d731))

## v1.8.0 (2024-02-20)

### Ci

* ci: added all logs from client ([`da59e01`](https://gitlab.psi.ch/bec/bec/-/commit/da59e01042a199f95506d568c13fa74866c29af0))

### Documentation

* docs(developer): added instructions on how to set up vscode ([`94d63e6`](https://gitlab.psi.ch/bec/bec/-/commit/94d63e60b754a926e953208b325b943aa2c387e8))

### Feature

* feat(bec_lib): added async data handler ([`da46c27`](https://gitlab.psi.ch/bec/bec/-/commit/da46c278425fe31aa2a597c9d55065653ae63fbd))

### Fix

* fix(bec_lib): fixed typo in xrange ([`0fe0a6e`](https://gitlab.psi.ch/bec/bec/-/commit/0fe0a6e119ed01ebb38ac0b07c05d7f42a19ecf3))

### Refactor

* refactor(bec_lib): merged scan data and baseline data; added async data storage ([`06ed833`](https://gitlab.psi.ch/bec/bec/-/commit/06ed833ab2ef338c3c443d127acb123e1744ed44))

* refactor(file_writer): use async data handler ([`00d1fe0`](https://gitlab.psi.ch/bec/bec/-/commit/00d1fe0afac64304e074d90b0e9893cf09021785))

### Test

* test(pdf_writer): added tests ([`f64bdea`](https://gitlab.psi.ch/bec/bec/-/commit/f64bdea7978c7ba5d98cb8b6933c91b54dd2865f))

* test(async_data): added more tests ([`fb7c84f`](https://gitlab.psi.ch/bec/bec/-/commit/fb7c84fcc6b60f021684b3bd14e9ce22e5e3af72))

* test(bec_lib): updated test data to new xrange return values ([`0b5660f`](https://gitlab.psi.ch/bec/bec/-/commit/0b5660f1d41978dda6a8d37805e390fc292fd316))

* test(file_writer): updated test data to new xrange return values ([`d5cfbb3`](https://gitlab.psi.ch/bec/bec/-/commit/d5cfbb37538618fe2be5aaee10d9b0ac9122df7c))

## v1.7.3 (2024-02-19)

### Fix

* fix(rpc): fixed rpc calls with empty list as return value ([`a781369`](https://gitlab.psi.ch/bec/bec/-/commit/a781369e469a1196b7e88c6fa3593ee40439ec1e))

## v1.7.2 (2024-02-19)

### Fix

* fix(endpoints): added gui_instruction_response endpoint ([`9a838bb`](https://gitlab.psi.ch/bec/bec/-/commit/9a838bbe8e7fab974982654bdc9f69a14edf7a20))

* fix(live_table): fixed live table for string values ([`3b04d31`](https://gitlab.psi.ch/bec/bec/-/commit/3b04d319f9f8d56a8e8c2d6fec9802cc7e747ad3))

## v1.7.1 (2024-02-16)

### Fix

* fix(bec_lib.device): made device.position a property to be compliant with ophyd ([`4060b86`](https://gitlab.psi.ch/bec/bec/-/commit/4060b8651b99e3e86e440bcd02d148722ea5403b))

### Test

* test(e2e): added wait to set ([`27c53da`](https://gitlab.psi.ch/bec/bec/-/commit/27c53dab774f68a2eec2c833f2b9316d2775ee51))

## v1.7.0 (2024-02-14)

### Feature

* feat(scan_worker): emitted readout priority contains all devices, not just the modification ([`21187ad`](https://gitlab.psi.ch/bec/bec/-/commit/21187adb48495422aa9c0f0adbeeaa23b2d6c8a5))

* feat(devicemanager): added filter methods for continuous and on_request devices ([`708aaff`](https://gitlab.psi.ch/bec/bec/-/commit/708aaff918e7e858c3c1070057a17cedab248c88))

### Fix

* fix(devicemanager): fixed bug after refactoring ([`37a58ef`](https://gitlab.psi.ch/bec/bec/-/commit/37a58ef5ce83a1c1a4a483c07e08e4f5dd437dda))

### Test

* test(devicemanager): updated test cases ([`ff17e50`](https://gitlab.psi.ch/bec/bec/-/commit/ff17e508e6016163b9ddc32aa91f48a35de26b0b))

## v1.6.0 (2024-02-14)

### Feature

* feat(file_writer): added support for user-defined file suffixes ([`505df05`](https://gitlab.psi.ch/bec/bec/-/commit/505df053c1b5801cc86e5e6d1f3e58a94edeaf22))

### Test

* test: added tests for file suffix checks ([`7dc6c12`](https://gitlab.psi.ch/bec/bec/-/commit/7dc6c12872546656a22f05f5c8901cf4ca07d42e))

* test: refactored scan object tests ([`989aea4`](https://gitlab.psi.ch/bec/bec/-/commit/989aea4531da77025a3b8a8c837ba5e568cf77bd))

## v1.5.1 (2024-02-14)

### Fix

* fix(dap): dap service should now raise on unknown dap service cls; another provider may be responsible for it ([`85969f5`](https://gitlab.psi.ch/bec/bec/-/commit/85969f5d5393166996dbabbeefc06ef464576ee5))

## v1.5.0 (2024-02-13)

### Feature

* feat(scan_data): added baseline data ([`41bf2d1`](https://gitlab.psi.ch/bec/bec/-/commit/41bf2d1bd4d139f801d36d8cb4a0f9c837ac5d09))

### Fix

* fix(bluesky_emitter): fixed device info access ([`06b2373`](https://gitlab.psi.ch/bec/bec/-/commit/06b2373fea588433026079ed3d0a5b140d3f57f9))

* fix(scan_bundler): added metadata to baseline reading ([`9294562`](https://gitlab.psi.ch/bec/bec/-/commit/9294562f3bb377531f2fc558a655e8f7016feb38))

* fix(scan_manager): added baseline consumer ([`ce9681c`](https://gitlab.psi.ch/bec/bec/-/commit/ce9681c1859fd56c82bab206c8886f2851e4cc5d))

### Refactor

* refactor(scan_data): removed unused variable ([`ef07a32`](https://gitlab.psi.ch/bec/bec/-/commit/ef07a328bd05cd18e107229f56639a7492f3ba84))

## v1.4.0 (2024-02-13)

### Build

* build(plugins): added device server ([`3139ea0`](https://gitlab.psi.ch/bec/bec/-/commit/3139ea09906c3d4569d8043fb05b1c21e290aeb6))

* build(plugins): added helper script to create default plugin structure ([`04dc5bf`](https://gitlab.psi.ch/bec/bec/-/commit/04dc5bfb66a7600c7c8de32cb7acbac9fd3b32f0))

### Ci

* ci: added pipeline as trigger for e2e tests ([`766795a`](https://gitlab.psi.ch/bec/bec/-/commit/766795a91e5a3b3a4820a08ade4bc53d120b7105))

### Documentation

* docs(plugins): added plugin docs ([`c14c526`](https://gitlab.psi.ch/bec/bec/-/commit/c14c526a85a9e67e1bca866fcae749975acc5f30))

### Feature

* feat: added support for customized lmfit params ([`f175fd7`](https://gitlab.psi.ch/bec/bec/-/commit/f175fd7c55b82dbb0d8b080ee8a93cd8be52d816))

### Fix

* fix(dap): output fit is fitted to full scope, not only the trimmed ([`58f3cb1`](https://gitlab.psi.ch/bec/bec/-/commit/58f3cb17209acbae58720bcb1d6e8ec3bac28162))

### Refactor

* refactor: fix typos and structure ([`4dd6263`](https://gitlab.psi.ch/bec/bec/-/commit/4dd6263c649afc8ea7a3faf33de2722152923156))

* refactor: add dap_services, renamed ophyd_devices to devices and hli to high_level_interface ([`0c33ba7`](https://gitlab.psi.ch/bec/bec/-/commit/0c33ba7616d170748a79aae9405e841b76097adc))

### Test

* test(dap): fixed return value ([`7aa90b6`](https://gitlab.psi.ch/bec/bec/-/commit/7aa90b6c01324126e847849277a8e69efe5caceb))

## v1.3.0 (2024-02-12)

### Build

* build(client): added flaky and pytest timeout dependencies ([`08103f5`](https://gitlab.psi.ch/bec/bec/-/commit/08103f5fd2674a2cdf55d96ce3653c9802dc2de2))

### Ci

* ci: added flaky ([`06fb8bf`](https://gitlab.psi.ch/bec/bec/-/commit/06fb8bfaf943d82b7492e755892c583701d33ab9))

### Documentation

* docs(dap): added data fitting to user docs ([`b881b08`](https://gitlab.psi.ch/bec/bec/-/commit/b881b081726c659056c5120e0a71e09d41ef8881))

* docs: fixed typo ophyd.md ([`c1f4b38`](https://gitlab.psi.ch/bec/bec/-/commit/c1f4b388032689cf4f2d9492f6e49d32851b6035))

* docs(ophyd): fixed ophyd config description ([`6a272de`](https://gitlab.psi.ch/bec/bec/-/commit/6a272dede1d23ac7af9bb158105b2d5eb2c7445b))

### Feature

* feat(dap): added option to filter x range before fitting data ([`7068c1f`](https://gitlab.psi.ch/bec/bec/-/commit/7068c1f738d9876ef13cb62d797ba15fada3bd98))

* feat(dap): added input_data and plot options ([`c4029a0`](https://gitlab.psi.ch/bec/bec/-/commit/c4029a098db66baf1741bf4bcc1bbd71d14aca7f))

* feat(DAP): added option to customize results based on the dap service ([`dd48519`](https://gitlab.psi.ch/bec/bec/-/commit/dd4851941c14b1ace0227ab3ff28b50826c22f89))

* feat: added support for customized dap plugins objects ([`cf8430f`](https://gitlab.psi.ch/bec/bec/-/commit/cf8430f8787c8028d518c17fea5f00aba6e94093))

### Fix

* fix(dap): added input into to the dap metadata ([`0156f61`](https://gitlab.psi.ch/bec/bec/-/commit/0156f611f110f5ae31e163b9630d19a4112e98d0))

### Refactor

* refactor: removed outdated worker manager ([`ba74299`](https://gitlab.psi.ch/bec/bec/-/commit/ba74299a1dbd3aa3fd8ba38134889eb00df03142))

* refactor: added str method to message objects ([`f9b2813`](https://gitlab.psi.ch/bec/bec/-/commit/f9b2813a1deda03d5c1061fcbe7a20442405e056))

### Test

* test: fixed test as get data returns a np array instead of list ([`867773b`](https://gitlab.psi.ch/bec/bec/-/commit/867773be376c0e7c43890337b4f86ceace8b4472))

* test: fixed test after modifying dap interface ([`d57e95e`](https://gitlab.psi.ch/bec/bec/-/commit/d57e95e20d2951746c86a51a1f2d307a4b7d2448))

* test: fixed import for dap plugins ([`b119e46`](https://gitlab.psi.ch/bec/bec/-/commit/b119e464d6d3f6b325ec3dd53454bab7ff10a1fe))

* test: added more tests for bec scans ([`101bc1f`](https://gitlab.psi.ch/bec/bec/-/commit/101bc1ff1578e54b0dbd5b11ea3a92e7c32e5a96))

* test: use dev dependencies instead of hard-coded deps in Dockerfile ([`53bb5a6`](https://gitlab.psi.ch/bec/bec/-/commit/53bb5a61290da65791525d4bf6f7c11998eee90b))

* test: marked mv as flaky ([`496442a`](https://gitlab.psi.ch/bec/bec/-/commit/496442a6c8b1009c5f152a5863dc17a7cfc9a3c6))

## v1.2.1 (2024-02-10)

### Fix

* fix(compat python 3.11): ensure &#34;kind&#34; test works for numbers too ([`697ae59`](https://gitlab.psi.ch/bec/bec/-/commit/697ae59a6671aba27c098460e0d4ab59de62187d))

### Refactor

* refactor(configs): cleanup configs and removed old SynDevices, exchanged with SimCamera/SimMonitor/SimPositioner ([`3293925`](https://gitlab.psi.ch/bec/bec/-/commit/3293925256b1c7e1f9c99d93d05a2047ececb91f))

* refactor: clean up SimMonitor related changes ([`782dea8`](https://gitlab.psi.ch/bec/bec/-/commit/782dea87f303a9a25fa98496dbf9710dfba337e5))

## v1.2.0 (2024-02-09)

### Feature

* feat(bec_lib.utils): add user_access decorator to bec_lib.utils.

refactor: add check if method is in USER_ACCESS already

test: add test for decorator ([`0b309ce`](https://gitlab.psi.ch/bec/bec/-/commit/0b309ce8887b40cf907b19421adbbd47f30a8207))

### Refactor

* refactor: cleanup ([`5b46810`](https://gitlab.psi.ch/bec/bec/-/commit/5b46810270f722f4844a4d88136f41f6ebdeebe4))

## v1.1.3 (2024-02-09)

### Ci

* ci: added missing docker file to build dap ([`950504c`](https://gitlab.psi.ch/bec/bec/-/commit/950504c72836ed192d29c6fdb93169b08c6f8e52))

* ci: added dap to e2e tests ([`6f4fb10`](https://gitlab.psi.ch/bec/bec/-/commit/6f4fb10a28d8b47f1f29ac53d43ecc107a58e316))

### Fix

* fix(serializer): fixed serialization for set ([`bcd2e06`](https://gitlab.psi.ch/bec/bec/-/commit/bcd2e06449923b0f2f92f64703a70e6de99e72d2))

### Refactor

* refactor(serializer): cleanup ([`211e614`](https://gitlab.psi.ch/bec/bec/-/commit/211e614ed3032202b5684431d3855d8c82606ef1))

### Test

* test: fixed sim type for dap test ([`7e9da19`](https://gitlab.psi.ch/bec/bec/-/commit/7e9da194459acded34924331c09c92977c4b2363))

* test: added e2e test for dap and sim fit ([`7f257a9`](https://gitlab.psi.ch/bec/bec/-/commit/7f257a929c486d0280c91ea8351a015a63b5e232))

## v1.1.2 (2024-02-09)

### Fix

* fix: fixed xread decoding ([`c684a76`](https://gitlab.psi.ch/bec/bec/-/commit/c684a76a5eff0bf478121dcde25e9e4447e839dc))

* fix: fixed init config script ([`f0f9fe3`](https://gitlab.psi.ch/bec/bec/-/commit/f0f9fe304f24cb61053ce12d785b82745a14210e))

* fix: removed outdated msgpack packing

fix: fixed return values of configs ([`15f8e21`](https://gitlab.psi.ch/bec/bec/-/commit/15f8e213053a635da4ed8d54bcb562a690e71517))

* fix(redis_connector): encode/decode stream data ([`a7bafa6`](https://gitlab.psi.ch/bec/bec/-/commit/a7bafa6a0c99395068ef090d149732b4fa4f5eb5))

* fix(serialization): move BECMessage check in .loads() in the BEC message decoder

This allows to call .loads() on any bytes string ([`de8333b`](https://gitlab.psi.ch/bec/bec/-/commit/de8333b164033ff0c0a300278e5494f5cc8f7879))

## v1.1.1 (2024-02-08)

### Fix

* fix: bugfix for .put and cached readback, ([`880eb77`](https://gitlab.psi.ch/bec/bec/-/commit/880eb77fd0a065cadde14bc33294b069d16fd0c6))

### Refactor

* refactor: simplified updated logic ([`75e06d3`](https://gitlab.psi.ch/bec/bec/-/commit/75e06d3ee3296d636bd88e71ad519bcd6989d29e))

### Test

* test: add modified test including .put from client ([`a8204ac`](https://gitlab.psi.ch/bec/bec/-/commit/a8204ac84820562374d335cbbb5584ad14d879af))

## v1.1.0 (2024-02-08)

### Build

* build: added lmfit dependency ([`c90f24f`](https://gitlab.psi.ch/bec/bec/-/commit/c90f24fa644875866255bba0abbed96f1b783d23))

### Feature

* feat: lmfit serializer ([`ed679bb`](https://gitlab.psi.ch/bec/bec/-/commit/ed679bb6650dcd7d77ebbe16212745ac985eeba8))

* feat: dap services ([`2b08662`](https://gitlab.psi.ch/bec/bec/-/commit/2b08662c08baf89ecbbd051a428914b78bbbcd97))

* feat: added dap endpoints and messages ([`6dc09cf`](https://gitlab.psi.ch/bec/bec/-/commit/6dc09cf6e5ea26f8b64e266776322cbee19550bc))

### Fix

* fix: fixed support for scan items as args ([`b15e38b`](https://gitlab.psi.ch/bec/bec/-/commit/b15e38bd39511e09ed4e456843e54e755a1c10ce))

* fix: fixed typo ([`4c8dd55`](https://gitlab.psi.ch/bec/bec/-/commit/4c8dd5570cde952a24b60ac4a9eb6227d2b5d364))

* fix: preliminary fix for missing xadd serialization ([`11b8326`](https://gitlab.psi.ch/bec/bec/-/commit/11b8326393e0b21f0f2ad140c826af18619193f0))

* fix: fixed scan_data for .get default values ([`aa403c4`](https://gitlab.psi.ch/bec/bec/-/commit/aa403c4a53a7c2462d623097a2f3275f2e7c1c90))

* fix: fixed dataclass for availableresourcemessage ([`cfc5237`](https://gitlab.psi.ch/bec/bec/-/commit/cfc5237025806d91eb32f2ebe135e2ddb55e8c1a))

* fix: fixed multiple model imports ([`a5f1447`](https://gitlab.psi.ch/bec/bec/-/commit/a5f1447c8734f88734f9828753f7bfd567128b8e))

* fix: fixed plugin handling for multiple service provider ([`ef4b66f`](https://gitlab.psi.ch/bec/bec/-/commit/ef4b66fd928600e40c06880cba807e667b1b4ed2))

* fix: fixed support for multiple dap services ([`e2595bc`](https://gitlab.psi.ch/bec/bec/-/commit/e2595bc22535de384d2747bbb5d4c225507f2a11))

* fix: accept args, kwargs in new client ([`47f4ecf`](https://gitlab.psi.ch/bec/bec/-/commit/47f4ecff540e03004ad16afaa6d11150efd0d3ba))

* fix: use service id property for status updates ([`5d33146`](https://gitlab.psi.ch/bec/bec/-/commit/5d33146b0cf7e6f9f23f98275e2697459d3692dd))

* fix: fixed dap loading ([`0c71b5f`](https://gitlab.psi.ch/bec/bec/-/commit/0c71b5f7c2c7d198ced36de9ced40bf99287025a))

* fix: fixed xread ([`f1219ae`](https://gitlab.psi.ch/bec/bec/-/commit/f1219ae0f051a872bdbb6e5d5e68c8e8b16232ea))

* fix: fixed xread when no id is specified ([`4a42277`](https://gitlab.psi.ch/bec/bec/-/commit/4a4227731ffeb117f4a5b8fb5f3ce6045f1f8eb8))

* fix: improved error handling for scihub ([`5d8028d`](https://gitlab.psi.ch/bec/bec/-/commit/5d8028db6bb9c510a8738ddba1545797b07dd7eb))

### Refactor

* refactor: cleanup after rebasing ([`514a516`](https://gitlab.psi.ch/bec/bec/-/commit/514a51624bd94fb4af55fcedba37bb155db29dc1))

* refactor: renamed fit to run and added service property to override default method name

test: fixed tests after renaming fit to run

test: fixed test after refactoring

test: added more tests ([`d510ae2`](https://gitlab.psi.ch/bec/bec/-/commit/d510ae2b61472d258f887c8c8ea4d3c653d5a723))

* refactor: cleanup and formatting ([`9a98dba`](https://gitlab.psi.ch/bec/bec/-/commit/9a98dbafd4f91189d5a8a5a97bb45568bbdedace))

* refactor: removed outdated dap files ([`bd2a4dd`](https://gitlab.psi.ch/bec/bec/-/commit/bd2a4ddd75d6d16dc22d16a50a408b85c7119b05))

* refactor: added private method to simplify the on_scan_status update routine ([`8b223a1`](https://gitlab.psi.ch/bec/bec/-/commit/8b223a1e914f4af2af9e0ed49dd609ad2dce5163))

* refactor: cleanup ([`9d1a494`](https://gitlab.psi.ch/bec/bec/-/commit/9d1a494d9d19cfd50c2a92954c6eb1213a8af3f0))

### Test

* test: more tests ([`aa9ff2d`](https://gitlab.psi.ch/bec/bec/-/commit/aa9ff2d3d0fdf0db102748a9c5968e969824b34f))

* test: added tests for dap plugins ([`b09524e`](https://gitlab.psi.ch/bec/bec/-/commit/b09524eb0b1a2686e2d377f9836139a948c25b8d))

## v1.0.0 (2024-02-07)

### Breaking

* fix(AlarmMessage)!: content member (dict) changed to msg (str)

In practice it was already used as a message. ([`3d087ef`](https://gitlab.psi.ch/bec/bec/-/commit/3d087ef87d1480ff4c96873e658441a833f477c6))

* refactor(messages)!: messages refactoring, new serialization module

To have a better separation of concern between messages and how they are conveyed in connectors.
BECMessage can be simple dataclasses, leaving the serialization to the connector which transport those.
The serialization module itself can be isolated, and in the case of msgpack it can be extended to
understand how to encode/decode BECMessage, to simplify writing code like with BundleMessage or to
be able to automatically encode numpy or BECStatus objects.
Finally, client objects (producers and consumers) can receive BECMessage objects instead of having
to dump or load themselves. ([`8bbfd10`](https://gitlab.psi.ch/bec/bec/-/commit/8bbfd10ca7db4b8376478a421633fe3e94cd9f0e))

* fix(global var)!: remove builtins.__BEC_SERVICE__ ([`80fddc5`](https://gitlab.psi.ch/bec/bec/-/commit/80fddc5a4c3ec16d0ac464c79dcfba6bf449242e))

### Fix

* fix(messages): set msg_type of ScanQueueMessage to &#34;scan_queue_message&#34;

This allows &#39;shortcut lookup&#39; for message class ([`8b125a0`](https://gitlab.psi.ch/bec/bec/-/commit/8b125a05b95084c676552c483b4d35eaa45724a2))

* fix(scan_manager): publish available scans using a BECMessage ([`ac5fafc`](https://gitlab.psi.ch/bec/bec/-/commit/ac5fafc7fa30dc8006edb7554c9e261c30edc9a0))

### Refactor

* refactor(connector): add message type check in &#34;send&#34;, use &#34;raw_send&#34; to publish arbitrary bytes ([`d4c4cba`](https://gitlab.psi.ch/bec/bec/-/commit/d4c4cbaaf26644d33c8e3685aef498e9db42790a))

## v0.61.0 (2024-02-06)

### Feature

* feat(ipython): represent objects using &#39;__str__&#39; rather than &#39;__repr__&#39; ([`1e2af9a`](https://gitlab.psi.ch/bec/bec/-/commit/1e2af9ae519382fe490162dff60b1056b9f50fdf))

### Fix

* fix(flake8): apply flake8 to fix inconsistencies ([`2eafba9`](https://gitlab.psi.ch/bec/bec/-/commit/2eafba951ae7180131bebf705466cdb2968bddba))

## v0.60.3 (2024-02-05)

### Ci

* ci: dockerfile accepts build var for python version ([`7b5391a`](https://gitlab.psi.ch/bec/bec/-/commit/7b5391a4f01a8acfcdc9c4eda7ef6065685d9dd3))

* ci: reverted changes to .gitlab-ci.yml ([`22261ad`](https://gitlab.psi.ch/bec/bec/-/commit/22261ad411c6d6f0b1cef201021656fba08072b6))

* ci: updated .gitlab-ci.yml ([`f862074`](https://gitlab.psi.ch/bec/bec/-/commit/f8620748646febc2df195fa32664795ec1a56c27))

* ci: updated .gitlab-ci.yml ([`22a1995`](https://gitlab.psi.ch/bec/bec/-/commit/22a19958e71fa8ecd44a4b99626b4b406f747031))

* ci: updated .gitlab-ci.yml file ([`7edf969`](https://gitlab.psi.ch/bec/bec/-/commit/7edf96964953f999b83797662f9534af4439325e))

* ci: moved branch exclusion to job ([`d8381b9`](https://gitlab.psi.ch/bec/bec/-/commit/d8381b9850c6d77a6f1d3cb55bcbf31a266b79fc))

* ci: excluded dev branch from pipeline ([`9a7e817`](https://gitlab.psi.ch/bec/bec/-/commit/9a7e817e541a599dcee06ef2be7b93329f8f3632))

* ci: removed no-ci ([`c696317`](https://gitlab.psi.ch/bec/bec/-/commit/c696317f68ae0fd7f0130a800ad570b29af3b8f2))

* ci: added development tag update ([`05c4328`](https://gitlab.psi.ch/bec/bec/-/commit/05c432852cb976e85e7f18a0ee5b997645883d0a))

* ci: changed job order for dev rtd deployment ([`a7afda9`](https://gitlab.psi.ch/bec/bec/-/commit/a7afda9d789010f8e800910e687635d58aaf9ed8))

* ci: added rtd deployment to dev on MR ([`b897c4f`](https://gitlab.psi.ch/bec/bec/-/commit/b897c4fd0509104223f7d60344b49728e7f80cc9))

### Documentation

* docs: fixed docstrings ([`f1e8662`](https://gitlab.psi.ch/bec/bec/-/commit/f1e86627773659b76b8cff199709611d23a0c558))

* docs: complement documentation ([`b4ac84a`](https://gitlab.psi.ch/bec/bec/-/commit/b4ac84a960db767eed0d6686ab242d52e7c3ac06))

* docs: updated landing page readme ([`c30eb2e`](https://gitlab.psi.ch/bec/bec/-/commit/c30eb2e67e89542d87a7aef8d7e445165f827239))

* docs: added references to the user guide ([`a25c4b2`](https://gitlab.psi.ch/bec/bec/-/commit/a25c4b2bb0ef7d98ef72c0bfefd6b435d4bb1db0))

### Fix

* fix: scan_to_csv can handle ScanReport and ScanItem, runs on multiple scans; closes #80, #104 ([`1ff19a1`](https://gitlab.psi.ch/bec/bec/-/commit/1ff19a156d9614fb1d9583c28d8181341ad5ebb4))

## v0.60.2 (2024-02-02)

### Fix

* fix: fixed scihub shutdown procedure ([`dfc6dd4`](https://gitlab.psi.ch/bec/bec/-/commit/dfc6dd4aaba1d5a9fcda51b2e8d30e9a431f237f))

### Refactor

* refactor: cleanup ([`afe8e24`](https://gitlab.psi.ch/bec/bec/-/commit/afe8e24f40ab53516311cddf9a4113090cff3534))

### Test

* test: added scilog tests ([`f8bf994`](https://gitlab.psi.ch/bec/bec/-/commit/f8bf9943b18d8e94c7113862e987d7dd3be8764c))

* test: allow for some jitter ([`d560432`](https://gitlab.psi.ch/bec/bec/-/commit/d5604323b6a33f86ecaae2e66a2cba0802cdd469))

* test: added shutdown methods to consumer mocks ([`4d827fe`](https://gitlab.psi.ch/bec/bec/-/commit/4d827fe16c982684fcca2e63f6bad1e486215309))

## v0.60.1 (2024-02-02)

### Fix

* fix: fixed serializer for 3.9 ([`5c6f250`](https://gitlab.psi.ch/bec/bec/-/commit/5c6f250950438deccfe61dadaf6f2224ebae6243))

* fix: fixed signature serializer for union operator; cleanup ([`4dd682b`](https://gitlab.psi.ch/bec/bec/-/commit/4dd682b3e7aaae1c40ed775554496c674f44658e))

### Refactor

* refactor: cleanup ([`1f802a0`](https://gitlab.psi.ch/bec/bec/-/commit/1f802a08bbd24d7f23b0481b82bd6ed07e665758))

## v0.60.0 (2024-02-01)

### Feature

* feat(run environment): allow to run service using the current Conda environment, if any ([`4b3bb4a`](https://gitlab.psi.ch/bec/bec/-/commit/4b3bb4a2a87d2d3024637500ad00e13dca80cac2))

## v0.59.6 (2024-02-01)

### Fix

* fix: fixed scibec login update ([`f1d8faf`](https://gitlab.psi.ch/bec/bec/-/commit/f1d8fafeaf3fd961fb4e3fa07a845a037fc27d1b))

## v0.59.5 (2024-01-31)

### Fix

* fix: fixed get_software_triggered_devices to excluded disabled devices, complement test case ([`37e74dc`](https://gitlab.psi.ch/bec/bec/-/commit/37e74dc206e906a15d19a261fc768b86d70cfdc1))

## v0.59.4 (2024-01-31)

### Fix

* fix: fixed event name for scan status callbacks ([`ed43260`](https://gitlab.psi.ch/bec/bec/-/commit/ed43260b60297d4e6b8dddc8c853b53b653c9ce1))

### Test

* test: fixed test for scan status events ([`ce67a29`](https://gitlab.psi.ch/bec/bec/-/commit/ce67a291eb188b40dc4259e611608417c3bdcd9e))

## v0.59.3 (2024-01-30)

### Fix

* fix: fixed rpc calls on device properties ([`f778302`](https://gitlab.psi.ch/bec/bec/-/commit/f77830296605e64c66b9ae3c8c9d760db720fe23))

## v0.59.2 (2024-01-30)

### Fix

* fix: added put as trigger for an update of the config cache ([`5f19da9`](https://gitlab.psi.ch/bec/bec/-/commit/5f19da921eafab72d0f64f437e4d49fa7afff988))

* fix: fixed status callback for cbs where the device is passed on ([`d110711`](https://gitlab.psi.ch/bec/bec/-/commit/d1107119da4b40f0ed119ed578593a75b49f1f38))

* fix: fixed rpc configuration updates to also update the cache ([`e4ef9b7`](https://gitlab.psi.ch/bec/bec/-/commit/e4ef9b725fc29502b175a20df2adf0c418024db7))

### Test

* test: fixed typo ([`4fae99c`](https://gitlab.psi.ch/bec/bec/-/commit/4fae99c0db47bd9971ea220d2f23d5dd7176db6f))

* test: fixed typo ([`2405053`](https://gitlab.psi.ch/bec/bec/-/commit/2405053ff08b1bb530ae0f64cd9f07a128b199ed))

* test: added e2e test for read_configuration and limit updates ([`7cdf4c3`](https://gitlab.psi.ch/bec/bec/-/commit/7cdf4c3d47f1f8da5c0f8dccf0dd987772ed0154))

## v0.59.1 (2024-01-29)

### Fix

* fix: fixed bug in device limit update ([`c347a84`](https://gitlab.psi.ch/bec/bec/-/commit/c347a84ad17c23f20866d90c019b7c705e52110a))

### Refactor

* refactor: fixed formatting for black24 ([`6d05dc2`](https://gitlab.psi.ch/bec/bec/-/commit/6d05dc2f7f920721d6f7421153d31bff20d0004b))

* refactor: add sotwaretrigger to repr and show_all ([`d0d8db0`](https://gitlab.psi.ch/bec/bec/-/commit/d0d8db0c46f403fd0060fdd45e8d3054a7c006f7))

### Unknown

* feature: added option to wait for all signals to connect ([`f5e0629`](https://gitlab.psi.ch/bec/bec/-/commit/f5e062981151db965ec5831bfaaeb8934d046100))

## v0.59.0 (2024-01-25)

### Documentation

* docs: complement documentation ([`356374e`](https://gitlab.psi.ch/bec/bec/-/commit/356374e59ccc2653e979fefd0bc8b571717ed126))

### Feature

* feat: add softwareTrigger to dev._config ([`675e74b`](https://gitlab.psi.ch/bec/bec/-/commit/675e74b42e2038d219e59e5b24b5a94ae6d4ca54))

### Fix

* fix: fix configupdate for readOnly ([`371175a`](https://gitlab.psi.ch/bec/bec/-/commit/371175a2959d3c668a660f7cce87fa27fbc12769))

### Refactor

* refactor: add softwareTrigger to avail keys in scibec/config_helper ([`5bc85d2`](https://gitlab.psi.ch/bec/bec/-/commit/5bc85d282fc50ce82d681ba334c234b0666991e8))

* refactor: remove DEBUG level scan_server ([`8246365`](https://gitlab.psi.ch/bec/bec/-/commit/82463655aa910afc5347fabcd7652d79c0d0764a))

* refactor: renamed detectors to get_software_triggered_devices and fixed access; closes #172, #173 ([`98c7136`](https://gitlab.psi.ch/bec/bec/-/commit/98c7136a3af29e03bce526189796f3fdf32820f5))

### Test

* test: complement config_update_test with onFailure key ([`b69dccb`](https://gitlab.psi.ch/bec/bec/-/commit/b69dccbf9693116a0e61c8633ca095a2dc0f263c))

* test: add test for config_handler; available keys for update ([`eed15d6`](https://gitlab.psi.ch/bec/bec/-/commit/eed15d6e8a864cf8327027e5c12b050a25e5e42c))

* test: add test for get_software_triggered_devices ([`70ec095`](https://gitlab.psi.ch/bec/bec/-/commit/70ec095e36a9a37dccd94ae63eb46fc6c763083c))

## v0.58.1 (2024-01-25)

### Fix

* fix: minor client improvements ([`b58aa12`](https://gitlab.psi.ch/bec/bec/-/commit/b58aa12c16dc2a9c8adde4685ce5e90ccc95cfc7))

## v0.58.0 (2024-01-24)

### Documentation

* docs: updated the docs ([`979e1d6`](https://gitlab.psi.ch/bec/bec/-/commit/979e1d6b84beb6223384a2996b1fb2acdfa00d41))

### Feature

* feat: added context manager for scan export ([`00e4fbf`](https://gitlab.psi.ch/bec/bec/-/commit/00e4fbfe4567bb75151f310703ac22f4bb2eb483))

### Fix

* fix: fixed scan_to_csv export and scan_export cm ([`07654ec`](https://gitlab.psi.ch/bec/bec/-/commit/07654ec0432201d44a4311d09efa62084f65c49e))

* fix: fixed cm exit ([`09d231a`](https://gitlab.psi.ch/bec/bec/-/commit/09d231a783036b71e8a9d9edfaa7408ae8b69fd7))

* fix: fixed context manager ([`52a2cdc`](https://gitlab.psi.ch/bec/bec/-/commit/52a2cdc8d1596e988d4a7f18acef4a179fc820ad))

### Refactor

* refactor: remove unnecessary imports after merge resolve ([`2d46e5d`](https://gitlab.psi.ch/bec/bec/-/commit/2d46e5d8bd322c5a179aeca01de72f7f62dc6bfa))

### Test

* test: removed time.sleep due to merge resolve ([`f2a947b`](https://gitlab.psi.ch/bec/bec/-/commit/f2a947b967ce941b8c90d2fd6e7d2061a3cdef01))

* test: add end-2-end test for scan_export_cm; closes #81,#161 ([`425a658`](https://gitlab.psi.ch/bec/bec/-/commit/425a658e6ab074b569ecf7cb885662d85939c063))

* test: add and fixed tests for scan_to_csv and scan_export_cm ([`260ff38`](https://gitlab.psi.ch/bec/bec/-/commit/260ff38d6223c4b34ba78d54dae10ce9e904974c))

* test: latency bodge ([`f6de378`](https://gitlab.psi.ch/bec/bec/-/commit/f6de378f5a930249acb906b3fc2277b8a275a1d5))

* test: added tests for metadata handler; closes #174 ([`624613c`](https://gitlab.psi.ch/bec/bec/-/commit/624613c3bdbde8974f019c3a3314ec1b2b854732))

## v0.57.2 (2024-01-24)

### Documentation

* docs: added ophyd-test to documentation ([`5809882`](https://gitlab.psi.ch/bec/bec/-/commit/58098821e950ed15e70c558cb389766ff3165779))

### Fix

* fix: fixed scihub error handling ([`a58b23d`](https://gitlab.psi.ch/bec/bec/-/commit/a58b23d1007f01ae2b892c49904382d896696d4a))

## v0.57.1 (2024-01-24)

### Fix

* fix: remove deviceType from device config and backend; closes #171 ([`3cb7ae7`](https://gitlab.psi.ch/bec/bec/-/commit/3cb7ae7cf97b1772e8c4f614bf67c87eeb36724f))

### Test

* test: remove test_wait_for_trigger temporary due to dependency on deviceType ([`a039cd5`](https://gitlab.psi.ch/bec/bec/-/commit/a039cd56cd3785a7680ec1102e2f2f33fecbfb07))

## v0.57.0 (2024-01-24)

### Feature

* feat: made some methods staticmethods to simplify their access ([`bbddd50`](https://gitlab.psi.ch/bec/bec/-/commit/bbddd50f5eb5aa53e8e65b5d2b139dc74fa24ed3))

### Fix

* fix: added default schema ([`0f8875d`](https://gitlab.psi.ch/bec/bec/-/commit/0f8875d1faaf2ee5629d5096bb5e1660dd045f80))

### Refactor

* refactor: moved scibec validator to bec_lib ([`d338efe`](https://gitlab.psi.ch/bec/bec/-/commit/d338efeb52cb8bbd304e33c3c38cfde4b9a48338))

## v0.56.3 (2024-01-23)

### Fix

* fix: disabled config updates on scibec ([`78b5cd6`](https://gitlab.psi.ch/bec/bec/-/commit/78b5cd66d1391fd855d1913b1a1ea655c86787a6))

* fix: add &#39;add&#39; to message again ([`d99230a`](https://gitlab.psi.ch/bec/bec/-/commit/d99230a45fefa412c5b2678c554575b1b27afc13))

* fix: bugfix for deviceConfigMessage validation ([`1c2a7d1`](https://gitlab.psi.ch/bec/bec/-/commit/1c2a7d1850911ee9a8c45f04dea0622d056785a7))

### Test

* test: added e2e test for config updates ([`01a5c78`](https://gitlab.psi.ch/bec/bec/-/commit/01a5c7801cb0e6ce0505be2b999f1791c6b7b21e))

* test: added test for DeviceConfigMessage actions ([`ce1adf4`](https://gitlab.psi.ch/bec/bec/-/commit/ce1adf48000674392ec178a82f909193c184e271))

## v0.56.2 (2024-01-23)

### Fix

* fix: fixed client shutdown; closes #168 ([`869215b`](https://gitlab.psi.ch/bec/bec/-/commit/869215bdc28bf8f4a90ea9ca0a9c017d26fe7d9b))

## v0.56.1 (2024-01-23)

### Fix

* fix(service): use thread termination event to wait instead of time.sleep ([`fd39c7c`](https://gitlab.psi.ch/bec/bec/-/commit/fd39c7c667d3f06cc411501feaf6a9e614071516))

## v0.56.0 (2024-01-19)

### Build

* build: added py-scibec dependency ([`eeedcc1`](https://gitlab.psi.ch/bec/bec/-/commit/eeedcc1b53ae8d3f92e47dc79ec4f22a7a713a02))

### Ci

* ci: trigger pipelines should only run merge requests ([`fbf013d`](https://gitlab.psi.ch/bec/bec/-/commit/fbf013ddcf386f4db0be211f24c7f1b87818a386))

### Feature

* feat: upgraded to new scibec structure ([`b72894a`](https://gitlab.psi.ch/bec/bec/-/commit/b72894a5f6d2d013fe66df28ca7de29e89125890))

* feat: added filecontent message ([`cade103`](https://gitlab.psi.ch/bec/bec/-/commit/cade10350cb4b83ee4819f81c178548cf5694a4b))

* feat: added file content and credential messages ([`416dd7e`](https://gitlab.psi.ch/bec/bec/-/commit/416dd7e1138ce37955fdb7fbfdfd1854771afc2a))

* feat: added scibec and file content endpoint ([`b366414`](https://gitlab.psi.ch/bec/bec/-/commit/b366414e5ca66b37c309fae7cc33651e989db0fe))

### Fix

* fix: fixed scibec readonly token update ([`b6ce07e`](https://gitlab.psi.ch/bec/bec/-/commit/b6ce07e65bbcacb36f1cec716db03ffaaff2a009))

### Refactor

* refactor: cleanup and tests for new scibec connector ([`daea3a3`](https://gitlab.psi.ch/bec/bec/-/commit/daea3a31cea04c8647ec5da1432272333ad1b409))

* refactor: removed scibec and mongodb config settings ([`8c9ff08`](https://gitlab.psi.ch/bec/bec/-/commit/8c9ff08310ba593c3c09d225b7c4fd350dd44c4c))

* refactor: moved repeated timer to separate file ([`5dd9e28`](https://gitlab.psi.ch/bec/bec/-/commit/5dd9e28a23f861fb8fabe69508307630d52ad50d))

### Test

* test: fixed test data ([`2af044b`](https://gitlab.psi.ch/bec/bec/-/commit/2af044b2c6ed7b16e046c7a001151dc8b6625a7e))

## v0.55.0 (2024-01-19)

### Ci

* ci: made bec-widgets job optional for now ([`e662e01`](https://gitlab.psi.ch/bec/bec/-/commit/e662e01b2077d835915088847cd354ddc0d8fc6f))

### Documentation

* docs: updated scanqueuemessage doc string ([`fd89d86`](https://gitlab.psi.ch/bec/bec/-/commit/fd89d8648f84c8029e141b646b99b2c9c13a68e1))

* docs: reviewed docstring of BECMessages ([`a4be91f`](https://gitlab.psi.ch/bec/bec/-/commit/a4be91f37c43de4d19101578a94a62d629309427))

### Feature

* feat: add sub for monitor, and callback; closes #158 ([`4767272`](https://gitlab.psi.ch/bec/bec/-/commit/4767272778693d8abd2db81aecf77ebd5d5f3109))

* feat: add monitor endpoint, device_monitor,  and DeviceMonitor message ([`0a292b0`](https://gitlab.psi.ch/bec/bec/-/commit/0a292b0363479c288be029be35b8560b79a69d29))

### Fix

* fix: add valid check for actions in DeviceConfigMessage ([`3a52b19`](https://gitlab.psi.ch/bec/bec/-/commit/3a52b1914534c373057e419eb6cec247575929a5))

### Refactor

* refactor: change datatype from value to np.ndarray ([`96abc04`](https://gitlab.psi.ch/bec/bec/-/commit/96abc040bce09a44174cc97aa535f879694e84dd))

* refactor: refactor devicemonitormessage, remove datatype ([`e612ce9`](https://gitlab.psi.ch/bec/bec/-/commit/e612ce9746360222bcf2d9f36bfebee49dccce4b))

### Test

* test: add test for monitor cb ([`f802e60`](https://gitlab.psi.ch/bec/bec/-/commit/f802e60b5c3e6025610b3adf8c206f673452c4bc))

## v0.54.0 (2024-01-18)

### Ci

* ci: added ophyd_devices trigger job ([`6e22b5c`](https://gitlab.psi.ch/bec/bec/-/commit/6e22b5c525380f6ee37e23c8df20e9d16969b09a))

* ci: added trigger job for bec-widgets ([`acf18ce`](https://gitlab.psi.ch/bec/bec/-/commit/acf18ceeeb5541a5fb373a6aa17d8b78f395949c))

### Feature

* feat(config): allow both .yaml and .yml files as valid config files ([`a1ca26d`](https://gitlab.psi.ch/bec/bec/-/commit/a1ca26dbd21823ae21eef359b8592a8c8749d300))

### Unknown

* refacto(config): dynamically import modules from ophyd_devices in _get_device_class

Unify code to search for a class from a &#34;dev_type&#34; string in the form
[module:][submodule:]class_name ([`3e5521b`](https://gitlab.psi.ch/bec/bec/-/commit/3e5521bfa6bf3325dffb5b23b5907c8daae37bc8))

## v0.53.0 (2024-01-12)

### Documentation

* docs: BECPlotter docs updated in GUI section ([`6bf51ab`](https://gitlab.psi.ch/bec/bec/-/commit/6bf51abeeac9684c1ef78077f2f8abcf7133ee06))

### Feature

* feat: GUI config dialog for BECMonitor can be opened from bec IPYTHON client ([`bceb55d`](https://gitlab.psi.ch/bec/bec/-/commit/bceb55d18880f773cb9cabd265e53793b211a3f5))

### Fix

* fix: bec_plotter.py fixed redis source format for new config style ([`6ce1e3a`](https://gitlab.psi.ch/bec/bec/-/commit/6ce1e3a4845db248a89617573fb30350554364da))

* fix: bec_plotter.py live monitoring fixed to new config structure of BECMonitor ([`6dca909`](https://gitlab.psi.ch/bec/bec/-/commit/6dca90902c7ac8938c64ee2a2f00d2bd54c00c0b))

### Refactor

* refactor: clean up print statements ([`ba7e08c`](https://gitlab.psi.ch/bec/bec/-/commit/ba7e08cd38b42823709d85589878cb0fa40a6308))

* refactor: bec_plotter.py changed attribute names for setting new configs ([`46682e6`](https://gitlab.psi.ch/bec/bec/-/commit/46682e626aaa5dbf21911f8a3336e7f86f6ddce7))

### Test

* test: test_bec_plotter.py all tests fixed ([`d6d888f`](https://gitlab.psi.ch/bec/bec/-/commit/d6d888f197e4f61bf825a8bc4ed8db47ca3d61bb))

* test: test_bec_plotter.py setting &#39;scan_segment&#39; sources and labels fixed, redis tests disabled ([`e3c2509`](https://gitlab.psi.ch/bec/bec/-/commit/e3c2509e103971f7e0b446bddcdb7a9ad2d99296))

### Unknown

* doc: bec_plotter.py docstring fixed, documentation updated ([`87074a8`](https://gitlab.psi.ch/bec/bec/-/commit/87074a8e5e3930a38135bcaa53629536f5f4c137))

## v0.52.9 (2023-12-22)

### Ci

* ci: fix cobertura for gitlab/16

Fix #156 ([`7bffd0e`](https://gitlab.psi.ch/bec/bec/-/commit/7bffd0e4f84b4f7b629de1a52c3b6d75c75761c4))

* ci: revert to ophyd master ([`e06ef69`](https://gitlab.psi.ch/bec/bec/-/commit/e06ef69b779854216db53e7a31d8a3734040cf05))

### Fix

* fix: read commented in DeviceBase ([`2365dff`](https://gitlab.psi.ch/bec/bec/-/commit/2365dff4a6a02d27e6cb1e28d3fd2b9dc7cb78b7))

* fix: wrong reference for &#39;monitor&#39; - changed from DeviceBase to Device ([`17cc883`](https://gitlab.psi.ch/bec/bec/-/commit/17cc883355c21299a062fd5bf1490d0f033f0414))

### Test

* test: added tests for describe and describe_configuration ([`f08b7d4`](https://gitlab.psi.ch/bec/bec/-/commit/f08b7d414a7244d7b56d2eb6f5b01d85c0df98f9))

## v0.52.8 (2023-12-18)

### Fix

* fix: fixed scan def cleanup ([`4be4252`](https://gitlab.psi.ch/bec/bec/-/commit/4be425277b561b9228982bc55d7f3980cf2bf98f))

## v0.52.7 (2023-12-18)

### Ci

* ci: fixed scihub log path ([`794556d`](https://gitlab.psi.ch/bec/bec/-/commit/794556d265d7ff28578625d3c63de1f8a65dcc0e))

* ci: added logs for scihub and dap ([`51ff5df`](https://gitlab.psi.ch/bec/bec/-/commit/51ff5dff3a80503c3d0f24e0bcd353752a2eb787))

* ci: preliminary fixed ophyd devices branch ([`e24f046`](https://gitlab.psi.ch/bec/bec/-/commit/e24f0464b56c258c83b9dbd928132e4875a5fa4c))

### Fix

* fix: fixed import of device manager ([`f162633`](https://gitlab.psi.ch/bec/bec/-/commit/f1626336b271b8a231ca46e175ae845ba4071eb6))

* fix: service should wait for device info ([`67b292f`](https://gitlab.psi.ch/bec/bec/-/commit/67b292fa0d5ab67cf945db6d12a1f92db642d3a3))

* fix: wait for scihub server to become ready ([`77232ac`](https://gitlab.psi.ch/bec/bec/-/commit/77232ac75f12acc9a754a2b5dcd76fa922340b7b))

### Refactor

* refactor: changes related to devicemanager refactoring ([`c01e6df`](https://gitlab.psi.ch/bec/bec/-/commit/c01e6df2c1355e0387141aed4f90af58bc9be2a0))

* refactor: deprecated devicemanager_client ([`9acba36`](https://gitlab.psi.ch/bec/bec/-/commit/9acba36aa20057454b10336d0ce97991d121875e))

### Test

* test: fixed tests - service are now waiting for device server ([`b70421c`](https://gitlab.psi.ch/bec/bec/-/commit/b70421c30965fa9eb4969d9b070167ba9700977d))

* test: fixed test after device_manager refactoring ([`14b2c9d`](https://gitlab.psi.ch/bec/bec/-/commit/14b2c9dbdf68e761ba1678d7b4b939ef5ba8f1fb))

## v0.52.6 (2023-12-18)

### Fix

* fix: fixed limit update for epics pvs; closes #113 ([`fce2520`](https://gitlab.psi.ch/bec/bec/-/commit/fce2520e38c80b1d2c01349b5f0d02d8eaf2a3bd))

## v0.52.5 (2023-12-18)

### Fix

* fix: fixed scan data namespace clash; closes #141 ([`8c4cee8`](https://gitlab.psi.ch/bec/bec/-/commit/8c4cee824bd0a2d623fd65f63f7a91347c79076d))

## v0.52.4 (2023-12-17)

### Fix

* fix: fixed config update ([`377e820`](https://gitlab.psi.ch/bec/bec/-/commit/377e82085c704fd2052f2bc3ad01fd1fe686a1c7))

* fix: fixed config update ([`76d1e06`](https://gitlab.psi.ch/bec/bec/-/commit/76d1e063794cadcf2dbfeefaa3fc0de9b04a7019))

### Test

* test: test to ensure rid is forwarded ([`b24c5eb`](https://gitlab.psi.ch/bec/bec/-/commit/b24c5eb50e164d2cc2ee5bed6a0b0f5486e446a6))

## v0.52.3 (2023-12-16)

### Ci

* ci: removed test utils from coverage report ([`2f110d3`](https://gitlab.psi.ch/bec/bec/-/commit/2f110d34994540fcd9510dcc653f64f6e2bdfc86))

### Fix

* fix: fixed log level init ([`5280dad`](https://gitlab.psi.ch/bec/bec/-/commit/5280dadc0640eaf1d3fbdf2fd6b1ce37a9f8f8ff))

* fix: fixed bug in alarambase that would prohibit error propagation ([`4c88bc6`](https://gitlab.psi.ch/bec/bec/-/commit/4c88bc687d90acbd41d0312cda42d1c049dd9423))

* fix: fixed timeout error in config_helper ([`6e75ca7`](https://gitlab.psi.ch/bec/bec/-/commit/6e75ca73bdd11740bcb5fd71c8157d8d66f05b53))

* fix: removed bec logger overwrite that prohibited log outputs ([`acbcb69`](https://gitlab.psi.ch/bec/bec/-/commit/acbcb69eb22900ca6679d6b059189761a34f4ece))

### Refactor

* refactor: added console log ([`d0c898b`](https://gitlab.psi.ch/bec/bec/-/commit/d0c898b53efa62bda2e97bf7dd2f1b985fed1151))

* refactor: added dedicated console log file ([`05a59d3`](https://gitlab.psi.ch/bec/bec/-/commit/05a59d37f2e253189eeba84e9e5cccbfa60834b1))

* refactor: changed log level for clearing the alarm stack from warning to info ([`e9e341d`](https://gitlab.psi.ch/bec/bec/-/commit/e9e341dfed5af5f1ae1e59f1c0700e447838e966))

### Test

* test: added wait_for_service_response tests ([`339d95f`](https://gitlab.psi.ch/bec/bec/-/commit/339d95fd3552404bb0f22dbd730068bba39f2020))

## v0.52.2 (2023-12-15)

### Fix

* fix: fixed wm behaviour ([`4ea93dc`](https://gitlab.psi.ch/bec/bec/-/commit/4ea93dcd48a893e95e65a69c91b485d96c49df12))

## v0.52.1 (2023-12-15)

### Fix

* fix: fixed config_ack for incomplete messages ([`16c0a1d`](https://gitlab.psi.ch/bec/bec/-/commit/16c0a1d4d4d023239afb12862a5732ec5187cf6f))

* fix: added service acknowledgement for config updates; closes #79 ([`bc1c43e`](https://gitlab.psi.ch/bec/bec/-/commit/bc1c43e2da1775b191dd168ab96599a4ada425cc))

### Refactor

* refactor: added bec service to builtins ([`1d4ae20`](https://gitlab.psi.ch/bec/bec/-/commit/1d4ae20b1a6d846db62806c0669f285a9724c760))

### Test

* test: fixed device server tests for config update ([`1fbf50c`](https://gitlab.psi.ch/bec/bec/-/commit/1fbf50cf42e2c147f117bb0bcfbcdab82198ccb7))

* test: fixed scan guard tests for service response ([`b8300c0`](https://gitlab.psi.ch/bec/bec/-/commit/b8300c06daab3b7dac74bcb4ece34e8fdee78e5c))

* test: fixed tests for config ack ([`2e7a09b`](https://gitlab.psi.ch/bec/bec/-/commit/2e7a09b1ce7ce17d4eb4854563477edb524c6a73))

## v0.52.0 (2023-12-15)

### Feature

* feat: added channel monitor as cli script ([`31cc15f`](https://gitlab.psi.ch/bec/bec/-/commit/31cc15f204ded7d368ef384cdb04448c18c5bc3f))

### Refactor

* refactor: cleanup and tests ([`ab89952`](https://gitlab.psi.ch/bec/bec/-/commit/ab899524b4270872c57b8f937708781b22ade4c4))

* refactor: update configs; relates to 2db65a385524b81bef1943a2a91693f327de4213 ([`8dbf4c7`](https://gitlab.psi.ch/bec/bec/-/commit/8dbf4c79d4f83e661a7e55839608194c6b681b65))

## v0.51.0 (2023-12-14)

### Build

* build: fixed install script to update the conda deps if they are outdated ([`abedd5e`](https://gitlab.psi.ch/bec/bec/-/commit/abedd5e95489c20519e48215f58ed5d7a9eca824))

* build: fix python requirement ([`4bfe93f`](https://gitlab.psi.ch/bec/bec/-/commit/4bfe93f6e2a5dc7b4fc778b043e5ccb5ba234674))

### Documentation

* docs: updated docs for cached config readouts ([`c33a66e`](https://gitlab.psi.ch/bec/bec/-/commit/c33a66ef00e096eb94f01b9205c2594fa5c81673))

### Feature

* feat: added message endpoint for read_configuration ([`3faf40a`](https://gitlab.psi.ch/bec/bec/-/commit/3faf40a218716bfa1c4271b01d9f516f93e03807))

### Fix

* fix: fixed readout for omitted signals ([`532d142`](https://gitlab.psi.ch/bec/bec/-/commit/532d142860ddac19dc1581db895514608dcfb65f))

* fix: fixed bug in config readout ([`4a640e5`](https://gitlab.psi.ch/bec/bec/-/commit/4a640e5ea05e7842fbfda851d79b97af0a801720))

* fix: fixed read and read_config for cached readouts ([`ba2a797`](https://gitlab.psi.ch/bec/bec/-/commit/ba2a797dfbd67b98b931b5f299bf53a2f4ed71a2))

* fix: added read_config on init ([`3529108`](https://gitlab.psi.ch/bec/bec/-/commit/352910812487104a87b8d95dc37d1c2164574074))

* fix: fixed rpc calls for read_configuration ([`3a475e7`](https://gitlab.psi.ch/bec/bec/-/commit/3a475e7e6e0cf46420bfe99a7b9747110d608412))

* fix: added option to read configuration from redis ([`f7acd4c`](https://gitlab.psi.ch/bec/bec/-/commit/f7acd4cb0646a660676fd5561d23c00bc7157fcc))

* fix: fixed ctrl c for rpc calls for unresponsive backends ([`6341059`](https://gitlab.psi.ch/bec/bec/-/commit/6341059dd068daf5fd6cce4947901cc3c3dcbe31))

### Refactor

* refactor: cleanup ([`d142862`](https://gitlab.psi.ch/bec/bec/-/commit/d14286295ae0097b81c25fd9ac755e39186fe53d))

### Test

* test: added tests for read_configuration ([`fed2c9f`](https://gitlab.psi.ch/bec/bec/-/commit/fed2c9f35a63f5da371c6815914960935afd0239))

* test: fixed dm client tests for rpc interface ([`b0903ba`](https://gitlab.psi.ch/bec/bec/-/commit/b0903ba15ad673a322fd6330cb0bf3f15811f952))

* test: fixed test for omitted signals ([`cd07fd2`](https://gitlab.psi.ch/bec/bec/-/commit/cd07fd2385bbfcc54a543648abbc87a2ffff8a87))

## v0.50.2 (2023-12-11)

### Build

* build: pin typeguard/4.0.1

All typeguard/3.x versions, and 4.0.0 have an issue with class property decorator ([`1c44912`](https://gitlab.psi.ch/bec/bec/-/commit/1c44912a9027474a954b37cd89119879df3fcf66))

### Ci

* ci: include python312 ([`36e33cb`](https://gitlab.psi.ch/bec/bec/-/commit/36e33cbf807ba1a9b8b3d4ba09af5a565221d30b))

* ci: default to python39 ([`ad10fb9`](https://gitlab.psi.ch/bec/bec/-/commit/ad10fb93f512c5bf36179caa38d5b3605943a64a))

### Documentation

* docs: update user docs, read and get; closes #125, #150 ([`6cf5cfa`](https://gitlab.psi.ch/bec/bec/-/commit/6cf5cfa7a5456fb899fd649b89b2c22293d2a3d8))

* docs: fix docs, merge ophyd_devices into ophyd in developer documentation ([`26dabe6`](https://gitlab.psi.ch/bec/bec/-/commit/26dabe6f31333e8417ad569b484c80e1e4026f23))

* docs: address merge comments ([`c288a4e`](https://gitlab.psi.ch/bec/bec/-/commit/c288a4ee5341502abc08fd2d163462e1c8d95cbd))

* docs: add fields to developer.ophyd as fillers ([`3c64df3`](https://gitlab.psi.ch/bec/bec/-/commit/3c64df327af16485d68dc2d8d2b1a312af67f932))

* docs: update docs, change software limits for  motor ([`e2a41c8`](https://gitlab.psi.ch/bec/bec/-/commit/e2a41c8b12e74debfe68a3d44424bde5a5841984))

* docs: add docs for read and get interface access; closes #125 ([`fad8662`](https://gitlab.psi.ch/bec/bec/-/commit/fad86626a4ff3d2b11a1c3dc2cf34baeb0bb5777))

* docs: fix typos, add links to requirements ([`ab7a9fa`](https://gitlab.psi.ch/bec/bec/-/commit/ab7a9faf747cc8b4954050186113bdb2ab1ee4a7))

### Fix

* fix: remove redundant imports ([`4a27b9a`](https://gitlab.psi.ch/bec/bec/-/commit/4a27b9a1ecde763e913774f8c23b308f79e7a181))

* fix: fix devicemanger get_deviceType_devices bug and add test ([`4aa9ba4`](https://gitlab.psi.ch/bec/bec/-/commit/4aa9ba4a8ef26fef2ad51ef72cd600ce624b7542))

### Refactor

* refactor: adapt python310 Union and Optional style ([`a68a809`](https://gitlab.psi.ch/bec/bec/-/commit/a68a809c4b832db9c59a8cef65f9f7f8c22ebac8))

* refactor: replace deprecated imports from typing ([`ac14a73`](https://gitlab.psi.ch/bec/bec/-/commit/ac14a73e8b088b09070f18daa431cb239d0cd2e5))

## v0.50.1 (2023-12-11)

### Build

* build: support &#34;typeguard&gt;=3&#34; ([`1ac5e5e`](https://gitlab.psi.ch/bec/bec/-/commit/1ac5e5e8d39f169c514a4189a9bad829c8c641f5))

### Fix

* fix: fixed decorator order and raised error for new typeguard version ([`8b610c2`](https://gitlab.psi.ch/bec/bec/-/commit/8b610c2ee88229122991892490b053fae3454b20))

### Refactor

* refactor: removed scibec ([`ac0b93d`](https://gitlab.psi.ch/bec/bec/-/commit/ac0b93d4f115ca0cede09184e09f12838f967efd))

## v0.50.0 (2023-12-11)

### Documentation

* docs: update documentation to new config structure ([`f38ddc3`](https://gitlab.psi.ch/bec/bec/-/commit/f38ddc3854611d8bf63a776749d418af870511d3))

### Feature

* feat: relaxed rules on deviceConfig schema; removed need for adding name ([`26d3f45`](https://gitlab.psi.ch/bec/bec/-/commit/26d3f45c7838c0cc60b649b3051ee5ce4e758ad5))

* feat: removed acquisition group and status from device config ([`5f48362`](https://gitlab.psi.ch/bec/bec/-/commit/5f4836266761f880e98e0798d0046d477a4b1e43))

### Fix

* fix: fix baseline_update ([`c39bdc1`](https://gitlab.psi.ch/bec/bec/-/commit/c39bdc13b536e49909584c2398dd6ec595e67d27))

* fix: fixed bug and tests ([`beb0651`](https://gitlab.psi.ch/bec/bec/-/commit/beb065124d0fcac7df4469a76a552ff057bd6a52))

* fix: clean up device_manager and scan_worker, add tests for baseline_devices; closes #144, #98 ([`7d5c03b`](https://gitlab.psi.ch/bec/bec/-/commit/7d5c03b7b9a8683d59773fc0b7e5f0830e563519))

* fix: fixed update for deviceConfig ([`1b81ffb`](https://gitlab.psi.ch/bec/bec/-/commit/1b81ffb3323ed560f1791587f612b8dfb254f6c4))

* fix: fixed devicemanager for missing deviceConfig ([`daa0e8e`](https://gitlab.psi.ch/bec/bec/-/commit/daa0e8e5e24518839b68dfebaca74f579ca49a9f))

* fix: added implicit ophyd device name assignment ([`6b497e2`](https://gitlab.psi.ch/bec/bec/-/commit/6b497e2536a993a4ba870a146a5fc824408907bc))

* fix: fixed fly scan sim ([`50fc302`](https://gitlab.psi.ch/bec/bec/-/commit/50fc30216bd44ec46118fba5e37def56b859c8a5))

* fix: fixed config update in config handler ([`cdbaf0c`](https://gitlab.psi.ch/bec/bec/-/commit/cdbaf0c6c4132af326ece5feb35ba302efa84c72))

* fix: fixed config update in devicemanager ([`46d1cf9`](https://gitlab.psi.ch/bec/bec/-/commit/46d1cf97dffbc14f97eddfdc6dac0161e5861216))

* fix: fixed demo config ([`ab399cc`](https://gitlab.psi.ch/bec/bec/-/commit/ab399cc934f186d286595bfd325fe7d78f31351e))

* fix: allow empty signals ([`cdd1d0c`](https://gitlab.psi.ch/bec/bec/-/commit/cdd1d0cba0816692faeec9bd74ea97b4043579d3))

* fix: fixed scan server after config refactoring ([`9397918`](https://gitlab.psi.ch/bec/bec/-/commit/939791889f9403c597ce7cbcb5f5c401ae6747a1))

* fix: fixed bec_lib after refactoring ([`9317220`](https://gitlab.psi.ch/bec/bec/-/commit/93172203b6292dfe8399fb47a277263002f94f01))

### Refactor

* refactor: removed name and labels from config ([`4e83b65`](https://gitlab.psi.ch/bec/bec/-/commit/4e83b65c995ae51b286cf020d5868fc8d500db17))

* refactor: removed old e2e config ([`a84b07d`](https://gitlab.psi.ch/bec/bec/-/commit/a84b07dea7a1163fba69271400dbab44be3a7c69))

### Test

* test: fixed fly sim test ([`ddfe126`](https://gitlab.psi.ch/bec/bec/-/commit/ddfe126e8786a2d9c8d08da2ee5b907c7fa5241b))

* test: fixed tests after config refactoring ([`c9d703f`](https://gitlab.psi.ch/bec/bec/-/commit/c9d703f78e5426038370ae20a062d4137702c988))

## v0.49.2 (2023-12-11)

### Ci

* ci: added issue templates ([`a207011`](https://gitlab.psi.ch/bec/bec/-/commit/a2070113c7497c5f16cbd618c34b2fc91f6e4232))

* ci: updated heading in default mr template ([`abbb761`](https://gitlab.psi.ch/bec/bec/-/commit/abbb761838ab893516133e5a0ebbb45875e7e613))

* ci: updated default mr template ([`350545c`](https://gitlab.psi.ch/bec/bec/-/commit/350545ce67eb13e1ada9c1839ce8814d6c76c776))

* ci: added merge request template ([`d690f06`](https://gitlab.psi.ch/bec/bec/-/commit/d690f0670a72d11875aa3c233bf634512314bc83))

### Documentation

* docs: updated install information for bec dev ([`6ede847`](https://gitlab.psi.ch/bec/bec/-/commit/6ede847b3e02593241420c37425659429729f823))

### Fix

* fix: added wheel for bec server install ([`7f51416`](https://gitlab.psi.ch/bec/bec/-/commit/7f514168c027031d8dacd4b7ec539c78a468b543))

## v0.49.1 (2023-12-08)

### Fix

* fix: fixed .get inconsistencies ([`83af812`](https://gitlab.psi.ch/bec/bec/-/commit/83af8127da11c80a47e05e375080c89bcc76716e))

## v0.49.0 (2023-12-07)

### Feature

* feat: added first version of bec_plotter ([`6c485c7`](https://gitlab.psi.ch/bec/bec/-/commit/6c485c7fcdcd2cbea3b5486c5df531c215e4fa13))

* feat: added gui endpoints and messages ([`6472e4e`](https://gitlab.psi.ch/bec/bec/-/commit/6472e4ef94b8100405e1c2e0011fd0a8c698a300))

### Fix

* fix: removed hard-coded link to widgets ([`3a99554`](https://gitlab.psi.ch/bec/bec/-/commit/3a99554b7e5310606a968c5e71eb7942d1381aaa))

* fix: fixed print_log; added tests ([`9028693`](https://gitlab.psi.ch/bec/bec/-/commit/9028693a3cd8ebc81ac6dc4832edc52732cd6444))

* fix: fixed show for manually closed figures ([`b68f38e`](https://gitlab.psi.ch/bec/bec/-/commit/b68f38e866a1a4806e7cc79c840cabfebbd27d38))

* fix: added missing set and append functions ([`716f80e`](https://gitlab.psi.ch/bec/bec/-/commit/716f80e2ca6d6383f8dc630680e54984d3375da6))

### Refactor

* refactor: minor refactoring; added test for print_log ([`6dd3dfe`](https://gitlab.psi.ch/bec/bec/-/commit/6dd3dfea4e9781f23466b244472ea816056b5d41))

* refactor: cleanup ([`1561631`](https://gitlab.psi.ch/bec/bec/-/commit/1561631eb932488cf1d9c4dd146f9fbdf0c8a4db))

### Test

* test: added tests for bec plotter ([`0a70743`](https://gitlab.psi.ch/bec/bec/-/commit/0a707436c7a2631613cbafaaa22a2f37b8d253bd))

## v0.48.0 (2023-12-05)

### Documentation

* docs: fixed paragraph level ([`01bba51`](https://gitlab.psi.ch/bec/bec/-/commit/01bba51da191e07d3ada050a78e031248cb4dd50))

* docs: improved introduction ([`1c82e80`](https://gitlab.psi.ch/bec/bec/-/commit/1c82e80960d27e85b73e1f308f06f44ec5a54316))

* docs: cleanup developer docs; remove usage folder ([`329e30b`](https://gitlab.psi.ch/bec/bec/-/commit/329e30b722843d66396e3e4bd8fc0d12660a6f06))

* docs: resolved threadl small typo in install ([`3236d1e`](https://gitlab.psi.ch/bec/bec/-/commit/3236d1ea725ce78b13828cdf6588e5c836983ef7))

* docs: split ophyd and ophyd_devices ([`173eb26`](https://gitlab.psi.ch/bec/bec/-/commit/173eb26b0c7469413075bb3766edd4f0ae626866))

* docs: review install_developer_env ([`5e3c10a`](https://gitlab.psi.ch/bec/bec/-/commit/5e3c10aca6517e5e4aa5eb00fc585e07f091b48c))

* docs: review contributing section ([`f4ffff3`](https://gitlab.psi.ch/bec/bec/-/commit/f4ffff3414baa62446e2810cbd389111d8d53183))

* docs: reviewd architecture section ([`1ac315d`](https://gitlab.psi.ch/bec/bec/-/commit/1ac315dc61094eee3d84f8cc2b3cf5b6331b04ba))

* docs: review developer page ([`c35e0be`](https://gitlab.psi.ch/bec/bec/-/commit/c35e0be40d13724d684109dcaea827a14d2a6dae))

* docs: rem typo and add link in data_access ([`b5c7453`](https://gitlab.psi.ch/bec/bec/-/commit/b5c7453445c565e99703436b88420d7b8f98d197))

* docs: rem typos in cli section ([`ede65af`](https://gitlab.psi.ch/bec/bec/-/commit/ede65af1c3c189bca137567096537709332c2b18))

### Feature

* feat: added support for namedtuple serialization for rpc ([`fd00974`](https://gitlab.psi.ch/bec/bec/-/commit/fd00974b05112a7c85eea412a1be89fee3b74822))

### Fix

* fix: fixed cached readout for .get; closes #137 ([`4fc35ca`](https://gitlab.psi.ch/bec/bec/-/commit/4fc35cadc161c1b39fc5a891ab7150f9b043b9f0))

* fix: fixed bug in readout for hinted and normal signals ([`bcd2433`](https://gitlab.psi.ch/bec/bec/-/commit/bcd243361af8eccd0771bc6950fcc3f86689c664))

* fix: made rpc interface more consistent with ophyd ([`e0e3a71`](https://gitlab.psi.ch/bec/bec/-/commit/e0e3a7158cee84c56f4ce82657e36ff88b18a36b))

### Refactor

* refactor: removed device_server_config_response endpoint; closes #142 ([`6a0a1be`](https://gitlab.psi.ch/bec/bec/-/commit/6a0a1bea803cc94cc80904e1116f8da182a6b2c0))

* refactor: remove :sub :val :stream remnants ([`ade6ae4`](https://gitlab.psi.ch/bec/bec/-/commit/ade6ae4585098b2c5f4cdcc96e3fbbc11ff8c5d6))

## v0.47.0 (2023-11-28)

### Documentation

* docs: fixed link; minor changes ([`6acbb66`](https://gitlab.psi.ch/bec/bec/-/commit/6acbb66ed7472fb369623e2ad55cc2c1835886ed))

* docs: fixed typos and links in user section ([`dc0d611`](https://gitlab.psi.ch/bec/bec/-/commit/dc0d611ddc88f5c35922fd5366e20e51c34e1053))

* docs: refactoring of user section ([`487582d`](https://gitlab.psi.ch/bec/bec/-/commit/487582d0a124b01c40c8b324f169e92f3d74d978))

### Feature

* feat: added support for starting the bec client with a config ([`0379031`](https://gitlab.psi.ch/bec/bec/-/commit/0379031fa7653e3cb647ef35cab95426bf5b1130))

## v0.46.1 (2023-11-28)

### Fix

* fix: fixed ctrl-c behaviour for report.wait; closes #138 ([`728b43c`](https://gitlab.psi.ch/bec/bec/-/commit/728b43c3f98c26dd337bdfff8bb4afc2fd684b80))

## v0.46.0 (2023-11-28)

### Feature

* feat: added version flag to bec cli ([`438e625`](https://gitlab.psi.ch/bec/bec/-/commit/438e6258dfd9806227d9ae89f2ae892c557e386a))

## v0.45.4 (2023-11-28)

### Fix

* fix: fixed device read for nested devices; closes #134 ([`eda60c5`](https://gitlab.psi.ch/bec/bec/-/commit/eda60c529afea248104279b3152ef9cfcb44b228))

## v0.45.3 (2023-11-28)

### Fix

* fix: fixed import in spec_hli ([`d5bc55a`](https://gitlab.psi.ch/bec/bec/-/commit/d5bc55aa8b047fafb59900394292e62d1a5c1b05))

* fix: added missing file ([`e82604c`](https://gitlab.psi.ch/bec/bec/-/commit/e82604cab5c48e228dbdd0016725c0d3ddc3c659))

### Refactor

* refactor: moved scan report to separate file ([`045526a`](https://gitlab.psi.ch/bec/bec/-/commit/045526a9ad21ae7756f9e62607a6f1d086c2db04))

## v0.45.2 (2023-11-27)

### Fix

* fix: fixed stop instruction for halt ([`6eb1081`](https://gitlab.psi.ch/bec/bec/-/commit/6eb10810d6de19bbeb9170fd78259864c3ca682c))

## v0.45.1 (2023-11-27)

### Documentation

* docs: update docstrings for endpoints

These updates are based on their actual usage in the code ([`945297d`](https://gitlab.psi.ch/bec/bec/-/commit/945297d4ac4be12c204546f5568a89eb4efb148b))

* docs: include comments upon merge request ([`e3c3607`](https://gitlab.psi.ch/bec/bec/-/commit/e3c3607fef0cb1238b9d3a60a61b3576a5660c14))

* docs: fix style ([`cb531c2`](https://gitlab.psi.ch/bec/bec/-/commit/cb531c2de16ea41a31c3bf80a31b463c5fbae28d))

* docs: remove typo ([`e017900`](https://gitlab.psi.ch/bec/bec/-/commit/e01790062b93a132a6581cd023f215b87e30fc8e))

* docs: add gauss_scatter_plot ([`bf138ca`](https://gitlab.psi.ch/bec/bec/-/commit/bf138ca380261e2dcaf6659fceb9ab8f6daa4129))

* docs: reviewed user documentation ([`15316ca`](https://gitlab.psi.ch/bec/bec/-/commit/15316caedb0ffa9846b199cc795e3bea3e031386))

* docs: refactor device configuration.md ([`12bd969`](https://gitlab.psi.ch/bec/bec/-/commit/12bd969d59dafde22cdd1fd1d0b6c15a16629a52))

* docs: update user guide for installation ([`aa5a245`](https://gitlab.psi.ch/bec/bec/-/commit/aa5a245b46b46255b78b4f5d1a71898f6c2257bf))

### Fix

* fix: add short delay in case of connection error ([`95106d6`](https://gitlab.psi.ch/bec/bec/-/commit/95106d6136d2d0a6fb476a422d970dcf830519de))

## v0.45.0 (2023-11-24)

### Feature

* feat: add load_demo_config method ([`20dfc64`](https://gitlab.psi.ch/bec/bec/-/commit/20dfc6497266bb0dde52cd71bd4e88ce7f364571))

## v0.44.2 (2023-11-23)

### Documentation

* docs: fixed link to conventionalcommits ([`6731a55`](https://gitlab.psi.ch/bec/bec/-/commit/6731a559422f7760a39fe160f22298022174bff1))

* docs: added placeholder for developer doc ([`f5a9f7d`](https://gitlab.psi.ch/bec/bec/-/commit/f5a9f7dfa6ebf9d23b53fa33764f684228690c11))

* docs: fixed page navigation ([`033c535`](https://gitlab.psi.ch/bec/bec/-/commit/033c53529e4947422968b258d26347c74b983d3d))

### Fix

* fix: fixed config_init path to config file. again. ([`6b714ef`](https://gitlab.psi.ch/bec/bec/-/commit/6b714ef375dd2e9599d462b4091194fbec264f94))

* fix: fixed config_init path to config file ([`e1a2429`](https://gitlab.psi.ch/bec/bec/-/commit/e1a2429fac8756832bcc9937262fb72a8aace592))

* fix: fixed packaging of demo_config and openapi_schema ([`7f8b1b1`](https://gitlab.psi.ch/bec/bec/-/commit/7f8b1b1bbe8dee285b71e221161f0c86ad49dd01))

## v0.44.1 (2023-11-22)

### Fix

* fix: fixed startup script by adding main guard ([`f6b5e9e`](https://gitlab.psi.ch/bec/bec/-/commit/f6b5e9e3c708162eb9f07c118e0226d5395f7f20))

## v0.44.0 (2023-11-21)

### Feature

* feat: added GUI config endpoint ([`67903a4`](https://gitlab.psi.ch/bec/bec/-/commit/67903a47bdcace6fcb9043aa6ad2bcb512260e12))

## v0.43.0 (2023-11-21)

### Ci

* ci: added missing scihub tests to additional test jobs ([`9345b15`](https://gitlab.psi.ch/bec/bec/-/commit/9345b15e7a602a71c3d8e9e33cbbb0ab845f3b51))

### Feature

* feat: added scan_data to simplify the access to the scan storage ([`6cfff5a`](https://gitlab.psi.ch/bec/bec/-/commit/6cfff5a529650094aa602d3669d96a7637bb79a1))

### Fix

* fix: fixed scan_data len dunder ([`b037b91`](https://gitlab.psi.ch/bec/bec/-/commit/b037b91c53b1bbc40224f712bc10787e981add39))

### Refactor

* refactor: revert commits that added temp module stubs

Fix path to test_service_config.yaml
This reverts commit 109453c1ccb3ebc8506e57f549549f99b38e4c8f
This reverts commit b73e9b3baac660bb7af3fc049c27e3bdb294bba9.
This reverts commit 108dc1179cf191c98b7891605d665371b5a2bca2. ([`5d254db`](https://gitlab.psi.ch/bec/bec/-/commit/5d254db6b78e684747f2350aacde845935313165))

* refactor: avoid using bec message aliases ([`331e653`](https://gitlab.psi.ch/bec/bec/-/commit/331e653ee60fad81da511728f369dd7bfed5e1ff))

* refactor: avoid logger &lt;-&gt; messages circular import

This is a preventive measure. The logger module needs LogMessage, and
messages module needs bec_logger, so as one possible fix, delay
LogMessage access in logger. ([`ddc12ba`](https://gitlab.psi.ch/bec/bec/-/commit/ddc12ba9bca8beeae3fb8e80bb11f99e217589be))

* refactor: remove redundant BMessage from test_scans ([`7ed8937`](https://gitlab.psi.ch/bec/bec/-/commit/7ed8937dec7a473953ad1dfb1ac68f50dbc8fc79))

### Test

* test: fixed tests for new scan data structure ([`cbc3870`](https://gitlab.psi.ch/bec/bec/-/commit/cbc38708840b70c185a652990583e64a8018b4a5))

* test: added test for diid&gt;=target_diid ([`298faaf`](https://gitlab.psi.ch/bec/bec/-/commit/298faaf14064aef3d74f1b7d2b77ef86605bd8e9))

## v0.42.10 (2023-11-19)

### Fix

* fix: fixed rpc func name compilation ([`c576669`](https://gitlab.psi.ch/bec/bec/-/commit/c57666949582663124f8b7b02f1707f41164f35c))

* fix: changes related to new read signature ([`80ee353`](https://gitlab.psi.ch/bec/bec/-/commit/80ee35371291831e5a9a3be3a7d9a09fadf710c2))

* fix: fixed readback data mixin ([`a396f12`](https://gitlab.psi.ch/bec/bec/-/commit/a396f12ec434359ba8735ad466d6fbd75a74aca1))

* fix: read through rpc updates the redis entries ([`52f9a4e`](https://gitlab.psi.ch/bec/bec/-/commit/52f9a4eceef70b1fb9df428ff9740eac7a45ea2f))

### Refactor

* refactor: made rpc a public method of rpc mixin ([`1bb2f0c`](https://gitlab.psi.ch/bec/bec/-/commit/1bb2f0c101aa6c8406e20d87d36582bc59d2cb55))

* refactor: moved rpc_mixin to separate file ([`35ea586`](https://gitlab.psi.ch/bec/bec/-/commit/35ea586f5a8220a7a8421136a598f38469fb2d08))

* refactor: moved rpc logic to separate mixin class ([`ba3e780`](https://gitlab.psi.ch/bec/bec/-/commit/ba3e780400db04ab11d808a8291bc03e6dbeb1c6))

* refactor: clean up ([`d362aae`](https://gitlab.psi.ch/bec/bec/-/commit/d362aae393288f4795724b88fda9cb6f1062a679))

* refactor: improved dev.show_all ([`f491d40`](https://gitlab.psi.ch/bec/bec/-/commit/f491d40bac12550ecbc5234e9254b749c88f5bf5))

### Test

* test: fixed floating point precision for table report ([`6e5a827`](https://gitlab.psi.ch/bec/bec/-/commit/6e5a8272f8c2d1158ca1c816e0720fce588594a2))

* test: fixed show_all test ([`de375b7`](https://gitlab.psi.ch/bec/bec/-/commit/de375b7579adec4dba5da2ef127bf4fd549eb195))

* test: added tests for rpc mixin class ([`773168e`](https://gitlab.psi.ch/bec/bec/-/commit/773168e2da87625fe9ee96824c53e88ce005ecb8))

* test: updated rpc test ([`16d4d86`](https://gitlab.psi.ch/bec/bec/-/commit/16d4d8618ad850de7229c315fe6af0e03aaab9d4))

## v0.42.9 (2023-11-19)

### Documentation

* docs: fix typo ([`77f4072`](https://gitlab.psi.ch/bec/bec/-/commit/77f407233421bd4838e8d22f53b3342cd67e47e1))

* docs: add module docstring ([`81d40a2`](https://gitlab.psi.ch/bec/bec/-/commit/81d40a233148a34ab7fa71c16afc7ab361632e36))

### Fix

* fix: clean up  __init__ ([`ab9a5e3`](https://gitlab.psi.ch/bec/bec/-/commit/ab9a5e3fa516dbb599400f2cf796169af98ec5e2))

### Refactor

* refactor: move velo and acc calc. in separate function and call it from scan_core ([`7c3ed51`](https://gitlab.psi.ch/bec/bec/-/commit/7c3ed5198cd7c8345d7066999867ac7e2d55efb7))

* refactor: finished refactoring of scan ([`dfe8f1b`](https://gitlab.psi.ch/bec/bec/-/commit/dfe8f1ba1a0927464eebe5131acc32bf980a0805))

* refactor: cleaned up scan core and removed hard coded speec/acc from stages ([`ccb5b03`](https://gitlab.psi.ch/bec/bec/-/commit/ccb5b03add6424085abaefbc941b1bf160a16296))

* refactor: fix docstring ([`4e9eaad`](https://gitlab.psi.ch/bec/bec/-/commit/4e9eaad4ac5c2a815898b76acd3cbbb2a5ec7338))

### Test

* test: remove redundant lines ([`afc2cc7`](https://gitlab.psi.ch/bec/bec/-/commit/afc2cc7fe7dd9e7bad8d89ce9c471d7eb6fe1280))

* test: add test to owis_grid ([`830d70d`](https://gitlab.psi.ch/bec/bec/-/commit/830d70d7fb91244e7f9d1fd912a6aae1c373cc21))

### Unknown

* fixed update initial motor params, fixed tests and add owis_grid to __init__ ([`f5f989d`](https://gitlab.psi.ch/bec/bec/-/commit/f5f989d176d2cb39e51f0482ad7cbf3835a478a8))

## v0.42.8 (2023-11-18)

### Fix

* fix: fixed ctrl c behaviour for rpc calls; closes #119 ([`9986a72`](https://gitlab.psi.ch/bec/bec/-/commit/9986a7292629668b6f398bee411bada04b535adc))

* fix: added status eq dunder ([`f1327d4`](https://gitlab.psi.ch/bec/bec/-/commit/f1327d409117f91f17917d6fe30a1dae8e4cbb90))

### Test

* test: refactored test to use dev fixture instead of bec_client ([`fc39c4a`](https://gitlab.psi.ch/bec/bec/-/commit/fc39c4ad1eae3cdaf6cea75618a55db9649f8779))

## v0.42.7 (2023-11-18)

### Fix

* fix: fixed signature serializer for py &gt;3.9 ([`6281716`](https://gitlab.psi.ch/bec/bec/-/commit/6281716b2974a7b074aa4b6ef465427f3603937e))

* fix: fixed signature serializer for typing.Literal ([`5d4cd1c`](https://gitlab.psi.ch/bec/bec/-/commit/5d4cd1c1918b4f417b9ebb51e5a12b5692bd7384))

### Refactor

* refactor: added type hints for optim_trajectory; closes #117 ([`9689606`](https://gitlab.psi.ch/bec/bec/-/commit/968960646cfe5d19a327a63c33be60a32ab0752c))

* refactor: updated bec_lib import to new bec_lib structure ([`c47a46f`](https://gitlab.psi.ch/bec/bec/-/commit/c47a46f049c36b224c9bee7977e0d1a7a2e43936))

* refactor: improved pylint score ([`fb1c015`](https://gitlab.psi.ch/bec/bec/-/commit/fb1c0154a5be7171a33a32d1ec698915a119ca7f))

## v0.42.6 (2023-11-18)

### Fix

* fix: include all needed files in packaged distro

Fix #118 ([`2b3eddc`](https://gitlab.psi.ch/bec/bec/-/commit/2b3eddcff62d3a8085f2f8d1a5826020ecd87107))

## v0.42.5 (2023-11-17)

### Fix

* fix: fixed creation of nested device components; needed for DynamicComponents ([`407f990`](https://gitlab.psi.ch/bec/bec/-/commit/407f99049091f78efc3b8fac6bb7046cc0a6b623))

### Test

* test: added dm client test for nested signals ([`fe11076`](https://gitlab.psi.ch/bec/bec/-/commit/fe110764c26a68661ff06633f94cdcebfda6352a))

* test: added test for dyn device components ([`0f3ab89`](https://gitlab.psi.ch/bec/bec/-/commit/0f3ab898757af672149deaf8c374436fd0824476))

### Unknown

* doc: added doc strings ([`7c0ca1b`](https://gitlab.psi.ch/bec/bec/-/commit/7c0ca1b5fe566303083a02c6ba597e456dcce343))

## v0.42.4 (2023-11-17)

### Ci

* ci: testing pylint_check ([`087c5a3`](https://gitlab.psi.ch/bec/bec/-/commit/087c5a30984b2cde5363a5390446f1a9d960575f))

* ci: testing pylint_check ([`55648d3`](https://gitlab.psi.ch/bec/bec/-/commit/55648d3cc89a447880f608f9711c90724555fbd7))

* ci: testing pylint_check ([`d162f84`](https://gitlab.psi.ch/bec/bec/-/commit/d162f8414f44556b3efce41f11c73166300ff6e6))

* ci: improved pylint check ([`972c544`](https://gitlab.psi.ch/bec/bec/-/commit/972c544f3071268a784dce14fb316c8b8fcdaea2))

* ci: made pylint check optional ([`b6aca18`](https://gitlab.psi.ch/bec/bec/-/commit/b6aca18455a30c1d02c61e90bb1862dcb2739471))

* ci: testing pylint_check ([`e0166d4`](https://gitlab.psi.ch/bec/bec/-/commit/e0166d40f6d5ebb6df98e3e49622868fb669c245))

* ci: updated pylint check to handle floating point comparison&#34; ([`10bebbb`](https://gitlab.psi.ch/bec/bec/-/commit/10bebbb6fbc6b58522ccaa758d44b174e77942f4))

* ci: testing pylint_check ([`e1074dd`](https://gitlab.psi.ch/bec/bec/-/commit/e1074dd1a005abc409ac38f5ff377e1a87ba0873))

* ci: fixed pylint test ([`a9bbece`](https://gitlab.psi.ch/bec/bec/-/commit/a9bbecec011cf4c780f7f485c35bb8893d4a57c2))

* ci: testing pylint ([`b1bbee1`](https://gitlab.psi.ch/bec/bec/-/commit/b1bbee16ed6a9169912c27e7ec7a1b1fed13f342))

* ci: added pylint-check to .gitlab-ci.yml ([`e33ce81`](https://gitlab.psi.ch/bec/bec/-/commit/e33ce811413be6bfcd67a1fb06f4f0265eebc921))

### Fix

* fix: removed redundant name in config output ([`5a81c21`](https://gitlab.psi.ch/bec/bec/-/commit/5a81c2134593b702fcd6f2645e952caa7cdaf2d2))

### Refactor

* refactor: improved setup.py ([`45b6a93`](https://gitlab.psi.ch/bec/bec/-/commit/45b6a937b7333f1d96fee14a22550b51cd3f9be2))

## v0.42.3 (2023-11-12)

### Fix

* fix: added missing init file ([`109453c`](https://gitlab.psi.ch/bec/bec/-/commit/109453c1ccb3ebc8506e57f549549f99b38e4c8f))

## v0.42.2 (2023-11-10)

### Fix

* fix: bec_service test ([`97d3d1f`](https://gitlab.psi.ch/bec/bec/-/commit/97d3d1f18f07101a860952f40a96b7cfd633fb3c))

* fix: resolve a circular import in logbook_connector ([`8efd02c`](https://gitlab.psi.ch/bec/bec/-/commit/8efd02cda483aaa29cdb6bbb9867a67037a25111))

### Refactor

* refactor: warn about importing from old module paths ([`b73e9b3`](https://gitlab.psi.ch/bec/bec/-/commit/b73e9b3baac660bb7af3fc049c27e3bdb294bba9))

* refactor: move Alarms enum into alarms_handler ([`943b10d`](https://gitlab.psi.ch/bec/bec/-/commit/943b10dac0f9e21bd42145486552a8fb26ee6d11))

* refactor: make all type checking imports conditional ([`cc9227f`](https://gitlab.psi.ch/bec/bec/-/commit/cc9227f893e63fc594e5236414250f6960e096f4))

* refactor: rename module BECMessage  -&gt; messages

This should help to avoid confusion between BECMessage module and
BECMessage class located in the same module ([`06f2d78`](https://gitlab.psi.ch/bec/bec/-/commit/06f2d781ae445a3e03afce821b2f732d7f6e3f90))

* refactor: temporarily add module stubs ([`108dc11`](https://gitlab.psi.ch/bec/bec/-/commit/108dc1179cf191c98b7891605d665371b5a2bca2))

* refactor: flatten bec_lib structure ([`524ef24`](https://gitlab.psi.ch/bec/bec/-/commit/524ef24da05fce33ad09e420f669fb50684af139))

* refactor: make bec_lib imports absolute ([`7166c8b`](https://gitlab.psi.ch/bec/bec/-/commit/7166c8b5eef21a9146f5d5d78c6a83e3ddf8f03f))

* refactor: move bec_lib test utils out of core folder ([`de5da55`](https://gitlab.psi.ch/bec/bec/-/commit/de5da559a651450bcab8ca40f553ca60ab27845f))

* refactor: move scripts into util_scripts folder ([`bbd0eee`](https://gitlab.psi.ch/bec/bec/-/commit/bbd0eee6bb04447456869304f5df1a1926ad7477))

* refactor: remove unused imports in bec_lib ([`171a5c6`](https://gitlab.psi.ch/bec/bec/-/commit/171a5c6609da76b3f17848ba01b50806e389255c))

* refactor: remove session_manager and singleton_threadpool ([`d54453d`](https://gitlab.psi.ch/bec/bec/-/commit/d54453d7e7120555ae97584572ccc834d5050379))

* refactor: run isort on all files

$ isort . --profile=black --line-width=100 --multi-line=3 --trailing-comma ([`146898e`](https://gitlab.psi.ch/bec/bec/-/commit/146898ec3fd56e2fdf6df49999be80ab4778b618))

* refactor: major scan worker refactoring; added separate device validation mixin ([`0c7ae79`](https://gitlab.psi.ch/bec/bec/-/commit/0c7ae795c41ba5f71b315da2d3a7c7895a0cf74c))

### Test

* test: fixed test for refactored worker ([`2da7dd3`](https://gitlab.psi.ch/bec/bec/-/commit/2da7dd385f1d7edbb9408a3af2edf458b7f4cea2))

## v0.42.1 (2023-11-09)

### Ci

* ci: disabled scibec end2end for now; re-enable once scibec is running ([`93ab2c3`](https://gitlab.psi.ch/bec/bec/-/commit/93ab2c37e106d86640d53fcdd8b8107e6901296b))

* ci: changed default order ([`53954d3`](https://gitlab.psi.ch/bec/bec/-/commit/53954d3bdc149d73d1cf013875dd269aa9d95cb9))

### Fix

* fix: fixed bec service update routine for missing messages; closes #114 ([`dc37058`](https://gitlab.psi.ch/bec/bec/-/commit/dc370584c9265b4fc28e79bd2bd9609c826668f8))

## v0.42.0 (2023-11-07)

### Feature

* feat: added scan base class to scan info ([`5ecc189`](https://gitlab.psi.ch/bec/bec/-/commit/5ecc1893439c46578b9da48913f80ff72d7b1fb9))

### Refactor

* refactor: added scancomponent base class ([`41206ef`](https://gitlab.psi.ch/bec/bec/-/commit/41206efc1395fb3d6ace3bf9799876aab453a73a))

## v0.41.0 (2023-11-06)

### Feature

* feat: changed arg_bundle_size from int to dict; closes #111 ([`1a8cc7c`](https://gitlab.psi.ch/bec/bec/-/commit/1a8cc7c448edd3f712cf2fc20070abefad69dd66))

### Fix

* fix: fixed scan signature for scan defs and group def ([`3589e3e`](https://gitlab.psi.ch/bec/bec/-/commit/3589e3e36fc4222592dcf9912a9be45b8cc91eea))

### Unknown

* Remove key/channel postfixes ([`d2bd559`](https://gitlab.psi.ch/bec/bec/-/commit/d2bd559c3ecd42cf9ff994c96679a70c3ca3b1ad))

## v0.40.0 (2023-11-06)

### Feature

* feat: added log to report on missing device status updates ([`261497a`](https://gitlab.psi.ch/bec/bec/-/commit/261497ad985bd52ab9db38086cd5421bc03331d2))

## v0.39.0 (2023-11-02)

### Feature

* feat: changed arg_input from list to dict to provide a full signature ([`c7d8b1a`](https://gitlab.psi.ch/bec/bec/-/commit/c7d8b1afd510cbb63f097b74121bb1b7b9e89ffc))

### Fix

* fix: added missing type hints to scan signatures ([`6b21908`](https://gitlab.psi.ch/bec/bec/-/commit/6b2190899d16d5bc1b1a582ca5f7159f1be6a56d))

* fix: removed helper plugin ([`87100ca`](https://gitlab.psi.ch/bec/bec/-/commit/87100caaf07851ce758dfa5e42f5c121eff2b886))

## v0.38.1 (2023-11-02)

### Fix

* fix: fixed nested get for missing fields ([`9be82f1`](https://gitlab.psi.ch/bec/bec/-/commit/9be82f12c6b42e99c61eeacc6185c663f95c9ab6))

### Test

* test: added test for nested get ([`f5fddaf`](https://gitlab.psi.ch/bec/bec/-/commit/f5fddafdf3fe33b3382180a03601f37dfe7f67ef))

## v0.38.0 (2023-11-01)

### Feature

* feat: added config option to abort on ctrl_c; closes #95 ([`705daa6`](https://gitlab.psi.ch/bec/bec/-/commit/705daa6d9e9642fdea85adafa12e4946e69bcd6c))

## v0.37.0 (2023-11-01)

### Feature

* feat: added option to specify monitored devices per scan; closes #100 ([`d3da613`](https://gitlab.psi.ch/bec/bec/-/commit/d3da613bfdf3721f5c52f5491bf64b01317a4126))

### Fix

* fix: fixed readout_priority update ([`aee1bda`](https://gitlab.psi.ch/bec/bec/-/commit/aee1bdae1461dd1bb8c0f959c8bce97605074d9d))

### Test

* test: fixed test for monitored devices ([`c20a6b2`](https://gitlab.psi.ch/bec/bec/-/commit/c20a6b2d9d44d68e71f4e678c31b472709a9c142))

## v0.36.3 (2023-11-01)

### Fix

* fix: added missing timestamp to flyer update ([`091df2f`](https://gitlab.psi.ch/bec/bec/-/commit/091df2f0a136a78423159faa35308d44f68f535c))

## v0.36.2 (2023-10-31)

### Fix

* fix: fixed error that caused the scan worker to shut down instead of raising for scan abortion ([`f1e8bfb`](https://gitlab.psi.ch/bec/bec/-/commit/f1e8bfba80468dc9aa7d057ecb57ef383c215c71))

* fix: added device name to flyer readout ([`cd82727`](https://gitlab.psi.ch/bec/bec/-/commit/cd827271bb738ced288450dc79b7dc0316e6b0b9))

### Refactor

* refactor: reduced log level for completing a device ([`221478c`](https://gitlab.psi.ch/bec/bec/-/commit/221478c15cdd85e6f8532c2c7f642afd7ec02de0))

### Unknown

* Delete bec_config_dev.yaml ([`b2bd4df`](https://gitlab.psi.ch/bec/bec/-/commit/b2bd4df78a40826c3083a940eeb632c15065c5ad))

* docs:fix typo in docstring ([`b90a4e2`](https://gitlab.psi.ch/bec/bec/-/commit/b90a4e2d1eb1679d155c427bae009626b70c60e7))

## v0.36.1 (2023-10-30)

### Fix

* fix: add &#39;.[dev]&#39; to bash scripts to avoid escape char in certain shells while install ([`0d5168d`](https://gitlab.psi.ch/bec/bec/-/commit/0d5168dcedf32902ffd866c45d85457c4f22e7e7))

## v0.36.0 (2023-10-30)

### Documentation

* docs: updated introduction; added scripts and scan defs ([`b9f2eab`](https://gitlab.psi.ch/bec/bec/-/commit/b9f2eab7297fd38085d1d77e0dd66aa070fe051e))

### Feature

* feat: added complete call to all devices; closes #93 ([`042e51e`](https://gitlab.psi.ch/bec/bec/-/commit/042e51e857cad3198823c9227e593b15ba1a233f))

### Fix

* fix: fixed bug in complete for all devices ([`08d34a8`](https://gitlab.psi.ch/bec/bec/-/commit/08d34a8418b768209b0721ac876b76575699ae7e))

### Refactor

* refactor: cleanup ([`dfc0abe`](https://gitlab.psi.ch/bec/bec/-/commit/dfc0abe7b6c7b6aaab2b637460f8776dc5153419))

* refactor: cleanup ([`cc5f5ac`](https://gitlab.psi.ch/bec/bec/-/commit/cc5f5ac3a26d7f9bde55b359c06cd6375a37d37a))

* refactor: merged wait for stage ([`2b9d39d`](https://gitlab.psi.ch/bec/bec/-/commit/2b9d39da73acbb5659a4919fef35607e6a674639))

### Test

* test: added test for complete with list of devices ([`ec016e4`](https://gitlab.psi.ch/bec/bec/-/commit/ec016e4466ec25ddc7f68ee5597fd7f285d086e9))

### Unknown

* doc: update rtd docs ([`2130a05`](https://gitlab.psi.ch/bec/bec/-/commit/2130a050486e1a906c08181fe2924f10ace57288))

* Update scans.py ([`af59b79`](https://gitlab.psi.ch/bec/bec/-/commit/af59b790cbfa56b384c9c9a7277b48525d4c1cd2))

## v0.35.1 (2023-10-06)

### Fix

* fix: changed progress update from devicestatus to progress message ([`03595b4`](https://gitlab.psi.ch/bec/bec/-/commit/03595b42f78f45f2c5d2e7bf10e860a3ee5297d4))

### Test

* test: fixed test for new progress messages ([`1190461`](https://gitlab.psi.ch/bec/bec/-/commit/1190461c82d28dbe23fdc3a245dfcf2e754eb248))

## v0.35.0 (2023-10-06)

### Feature

* feat: grid fly scan with standard epics owis motors ([`552aff5`](https://gitlab.psi.ch/bec/bec/-/commit/552aff5bd9fd0bb61e3f50133d4bbf52cc824857))

### Fix

* fix: fixed stage instruction for detectors ([`ac7a386`](https://gitlab.psi.ch/bec/bec/-/commit/ac7a386acf62d381ad096d816da6db30bcfa5ce7))

* fix: optimize staging of devices in scanserver and device server ([`2c66dbb`](https://gitlab.psi.ch/bec/bec/-/commit/2c66dbbe4667120195151f49acfe5b45527e21b9))

* fix: sgalil scan corrections ([`2f8fce5`](https://gitlab.psi.ch/bec/bec/-/commit/2f8fce52207fdbab2a5db562ca7cfa3beb814e41))

* fix: adjusted sgalil_grid scan for updated mcs operation ([`b7a722c`](https://gitlab.psi.ch/bec/bec/-/commit/b7a722c0ef4ce14fd6843c368bf076bd1024db23))

* fix: online changes e20643, file writer bugfix and add scanabortion check in sgalil_grid ([`195a8dd`](https://gitlab.psi.ch/bec/bec/-/commit/195a8dd7541fa12ff5f4d9c9cc0a70651af805b1))

* fix: fixed scan bundler for async fly scans ([`d7a6b0f`](https://gitlab.psi.ch/bec/bec/-/commit/d7a6b0fee010877dfd18cbf23ff55126a399dec9))

* fix: enabled scilog ([`64e82c6`](https://gitlab.psi.ch/bec/bec/-/commit/64e82c67782a701f5eeb04a3a9c1ce42832c1fdf))

* fix: fixed bl_check repeat ([`62aa0ae`](https://gitlab.psi.ch/bec/bec/-/commit/62aa0aed78c23ea0c117f84ba54d5f267f35eed4))

* fix: fixed primary readout for sgalil scan ([`4231d00`](https://gitlab.psi.ch/bec/bec/-/commit/4231d00e19aacc039ee9cc9f4a1f18294ea18ab0))

* fix: added missing pre scan to acquire ([`d746093`](https://gitlab.psi.ch/bec/bec/-/commit/d7460938041dac4be45fa39cbdaa957dda5f88ca))

* fix: fixed tmux launch for mono environments ([`5be5dda`](https://gitlab.psi.ch/bec/bec/-/commit/5be5dda1cfd3adfadae5e314a8ba87b394e8227a))

* fix: fixed scan progress for messages without scanID ([`64f3b13`](https://gitlab.psi.ch/bec/bec/-/commit/64f3b13e9710dbfb207c11fbd683db9cb9462dda))

### Refactor

* refactor: cleanup ([`a3b70e5`](https://gitlab.psi.ch/bec/bec/-/commit/a3b70e5b61f42cf3cfc582c044f193d5bdd27219))

* refactor: cleanup ([`766b1bd`](https://gitlab.psi.ch/bec/bec/-/commit/766b1bd06f6fd624c17f56680d99901cf3d70501))

* refactor: fixed formatter ([`b7ad6fe`](https://gitlab.psi.ch/bec/bec/-/commit/b7ad6fefc778c8e417e67aa49c336698d5fc428f))

* refactor: fix formatting for online changes ([`7232aef`](https://gitlab.psi.ch/bec/bec/-/commit/7232aeffc8fbfa053685aeb9d156e50080976da1))

### Unknown

* fix black formatting ([`7823624`](https://gitlab.psi.ch/bec/bec/-/commit/782362409effa84e7af53c0b6e9cfb53a6197a00))

## v0.34.2 (2023-10-05)

### Fix

* fix: fixed bug for aborted scans ([`e7d73e5`](https://gitlab.psi.ch/bec/bec/-/commit/e7d73e5b2b2cccb829e401b209605523f6b7dbce))

## v0.34.1 (2023-10-02)

### Fix

* fix: write files on abort and halt ([`910a92f`](https://gitlab.psi.ch/bec/bec/-/commit/910a92f4784c93119e63c9abad24ec1315718a45))

## v0.34.0 (2023-09-07)

### Feature

* feat: added progress endpoint and message ([`ad60b78`](https://gitlab.psi.ch/bec/bec/-/commit/ad60b7821a1de36645e2c70023ea73bb7d141e39))

### Fix

* fix: added missing primary readings to sgalil grid ([`e52390a`](https://gitlab.psi.ch/bec/bec/-/commit/e52390a2269370f6806f93896234bc076a0731f4))

## v0.33.0 (2023-09-07)

### Feature

* feat: add sgalilg_grid to scan_plugins and make scantype flyscan scan possible ([`a5ba186`](https://gitlab.psi.ch/bec/bec/-/commit/a5ba186ad14283fae7c5160180a759e29f78137d))

### Fix

* fix: add file_writer plugin cSAXS and file_event for new file from device ([`b1f4fcc`](https://gitlab.psi.ch/bec/bec/-/commit/b1f4fccaaaec9cded2182554900ca48ceeb2fdc3))

* fix: add frames_per_trigger to scans and scan server ([`51c8a54`](https://gitlab.psi.ch/bec/bec/-/commit/51c8a54f01c6b5a0a09c90cb5a21e5640b3cd884))

* fix: add eiger9m to cSAXS nexus file writer plugin ([`8ba441f`](https://gitlab.psi.ch/bec/bec/-/commit/8ba441f55fdb9659aff12d2535799f268af1d815))

* fix: file_writer and scan_ser for falcon and eiger9m and sgalil grid scan ([`cec0b34`](https://gitlab.psi.ch/bec/bec/-/commit/cec0b342f0c518bb37c4403cb55336792a192cec))

* fix: online fix for file writer ([`de5ba09`](https://gitlab.psi.ch/bec/bec/-/commit/de5ba09954468bf696e2aa27f00532fe7780ef27))

* fix: add file_writer plugin cSAXS and file_event for new file from device ([`0fdf164`](https://gitlab.psi.ch/bec/bec/-/commit/0fdf1647aaf153d480f952ff1515fda2a1a1640d))

* fix: add frames_per_trigger to scans and scan server ([`0c66dc3`](https://gitlab.psi.ch/bec/bec/-/commit/0c66dc33593379c7e2bee8499af8d6cecf32b761))

* fix: add eiger9m to cSAXS nexus file writer plugin ([`375150c`](https://gitlab.psi.ch/bec/bec/-/commit/375150ce58e00f2b6f53d713ac35cebdb087b6ad))

### Refactor

* refactor: cleanup after merge ([`f528612`](https://gitlab.psi.ch/bec/bec/-/commit/f5286126ff0203c34bb57799080decfd1ffeb0d5))

### Test

* test: fixed tests ([`31fca80`](https://gitlab.psi.ch/bec/bec/-/commit/31fca804cd14b2916241117e9b595118fd2abc9c))

### Unknown

* Merge branch &#39;saxs_online_changes&#39; of https://gitlab.psi.ch/bec/bec into saxs_online_changes

Conflicts:
	file_writer/file_writer/cli/launch.py
	file_writer/file_writer_plugins/cSAXS.py ([`6f8420e`](https://gitlab.psi.ch/bec/bec/-/commit/6f8420efc982d37c1e2e34f717b5713fb4ba85f4))

## v0.32.0 (2023-09-06)

### Documentation

* docs: added premove and enforce_sync doc ([`fd38985`](https://gitlab.psi.ch/bec/bec/-/commit/fd38985767ead15678f45ac60d0ee59bb8ee8df6))

### Feature

* feat: added pre_scan ([`7f23482`](https://gitlab.psi.ch/bec/bec/-/commit/7f23482b5cf273f06776e497783f44361a2cb58f))

### Fix

* fix: removed pre move from fly scan ([`ed095b0`](https://gitlab.psi.ch/bec/bec/-/commit/ed095b00cbebc50ebecaabc696b8aaf4a728270d))

* fix: removed pre move from fly scan ([`f8ad2f8`](https://gitlab.psi.ch/bec/bec/-/commit/f8ad2f8a2781fa38000c29b39772132eaa63e4ce))

## v0.31.0 (2023-09-05)

### Feature

* feat: added support for loading the service config from plugins ([`f3d3679`](https://gitlab.psi.ch/bec/bec/-/commit/f3d3679e216492d8dfaf35ff00f75520652863fc))

### Test

* test: fixed test for trigger ([`23af7b5`](https://gitlab.psi.ch/bec/bec/-/commit/23af7b52c62cd42242c5ec931101cbaf20dd2573))

* test: fixed test for trigger ([`54ba69b`](https://gitlab.psi.ch/bec/bec/-/commit/54ba69b9834d602bda0ec7f3006bced4371f7b40))

## v0.30.1 (2023-09-05)

### Fix

* fix: added sleep before polling for status ([`c8acaa4`](https://gitlab.psi.ch/bec/bec/-/commit/c8acaa4b71504a8b34c9f05f4ef6af5ab444a424))

* fix: removed hard-coded trigger wait; waiting for status instead ([`086c863`](https://gitlab.psi.ch/bec/bec/-/commit/086c8634e30baf4ae1b74ae61bd3f8070c69d320))

### Test

* test: fixed test for new wait ([`9aefe83`](https://gitlab.psi.ch/bec/bec/-/commit/9aefe83b02b3b99d1633bd48ffd701fd2cbfaf2b))

## v0.30.0 (2023-09-04)

### Feature

* feat: beamline check ([`cae5f61`](https://gitlab.psi.ch/bec/bec/-/commit/cae5f61924744d0358527b074958bdfe102bb2cd))

* feat: added preliminary version of bl_checks ([`bfa1d67`](https://gitlab.psi.ch/bec/bec/-/commit/bfa1d678735cc8dcfb303446517254290c7c7921))

### Refactor

* refactor: refactored beamline checks to simplify unit tests ([`e9d0fbe`](https://gitlab.psi.ch/bec/bec/-/commit/e9d0fbe44403013430380bd1a8f98d951bbb25be))

## v0.29.0 (2023-09-04)

### Feature

* feat: added bec_plugins as source for devices ([`bbcdbc0`](https://gitlab.psi.ch/bec/bec/-/commit/bbcdbc0123566f4bea811fb9c873e059b4eb4a7c))

### Fix

* fix: fixed signal init ([`41282e5`](https://gitlab.psi.ch/bec/bec/-/commit/41282e57678d6a39a1f40fdf828e2fdb2ddc0193))

## v0.28.0 (2023-09-02)

### Feature

* feat: added progress bar based on async devices ([`11e5f96`](https://gitlab.psi.ch/bec/bec/-/commit/11e5f96b7575e0a811f45914e99ada6d2c449648))

* feat: added scan progress ([`9f6a044`](https://gitlab.psi.ch/bec/bec/-/commit/9f6a044fe316c804e2e4dfc34435c9eb71cd109b))

* feat: added xrange ([`f4f38d6`](https://gitlab.psi.ch/bec/bec/-/commit/f4f38d6deab2026177126e58cf1eac20490d9942))

### Fix

* fix: fixed scan_progress import ([`5eda477`](https://gitlab.psi.ch/bec/bec/-/commit/5eda477723d4dfc0387e0293713ef8e197a58f53))

* fix: ipython client should use default service config ([`9b89aec`](https://gitlab.psi.ch/bec/bec/-/commit/9b89aecfdc0449a9d40aae642dccf2408989c6d1))

### Refactor

* refactor: removed code duplication ([`d0bc94b`](https://gitlab.psi.ch/bec/bec/-/commit/d0bc94b671c4ce2851ac7d3c9c3a209b79a6cb36))

### Test

* test: added xrange and get_last tests ([`1a24616`](https://gitlab.psi.ch/bec/bec/-/commit/1a24616cb3b2e8a44860a8e34f9294e635449505))

* test: added more file_manager tests ([`54517ca`](https://gitlab.psi.ch/bec/bec/-/commit/54517cabef2158bc33dcd7e30cb7de352c0a94bc))

* test: added more file_manager tests ([`153c38a`](https://gitlab.psi.ch/bec/bec/-/commit/153c38aea6c9f47123b47655fb1d20ff4b79fa1c))

## v0.27.0 (2023-08-31)

### Feature

* feat: added get_last; changed streams to stream suffix ([`e84601f`](https://gitlab.psi.ch/bec/bec/-/commit/e84601f487d4943c63a31f12b42d656dc9a4c690))

### Unknown

* tests: fixed tests for new stream suffix ([`1137e31`](https://gitlab.psi.ch/bec/bec/-/commit/1137e3188d4f6cf14b1d17b669c2e81fcad98d91))

## v0.26.0 (2023-08-31)

### Feature

* feat: add new endpoint for async device readback ([`5535797`](https://gitlab.psi.ch/bec/bec/-/commit/5535797e1e25121d7a3997d78aa6c43eff17e086))

### Fix

* fix: fixed xadd for pipelines ([`d19fce7`](https://gitlab.psi.ch/bec/bec/-/commit/d19fce7d21a12eac2f8ac9b083fff464e5d0da9e))

* fix: bugfix ([`57c989c`](https://gitlab.psi.ch/bec/bec/-/commit/57c989cfe204a657bcefac2364a6a0ad98a77ff1))

* fix: adjust xadd to allow streams to expire ([`33fbded`](https://gitlab.psi.ch/bec/bec/-/commit/33fbdedd3eed52ded4eb53043bc7407997d51e4a))

* fix: online changes ([`9b07e0f`](https://gitlab.psi.ch/bec/bec/-/commit/9b07e0f8a2d774a9a6a07ab9faa9167585532dcd))

### Test

* test: added test for obj destruction ([`79c9e3c`](https://gitlab.psi.ch/bec/bec/-/commit/79c9e3c841c888680df4f0ed6e65f4f20cda359d))

## v0.25.0 (2023-08-31)

### Feature

* feat: added support for startup scripts from plugins ([`d35caf5`](https://gitlab.psi.ch/bec/bec/-/commit/d35caf5ae40b5b46f3b2adad139cad66b3091857))

## v0.24.0 (2023-08-31)

### Ci

* ci: removed repo updates ([`8ba01d8`](https://gitlab.psi.ch/bec/bec/-/commit/8ba01d84fa7b9c7661e0fb742aa9cd9193926625))

### Feature

* feat: added global var service config to simplify sharing the config with other classes ([`75f1f9c`](https://gitlab.psi.ch/bec/bec/-/commit/75f1f9cd4ebc6938f2cf47103fb64eef8be57ae3))

* feat: added option to update the worker config directly ([`a417fd8`](https://gitlab.psi.ch/bec/bec/-/commit/a417fd8a18cadb4b480da243149c1186f3a07d88))

* feat: added available resource endpoint/message ([`5f5c80c`](https://gitlab.psi.ch/bec/bec/-/commit/5f5c80c2866236226dca717de0c67b32f5692ab9))

### Fix

* fix: fixed worker manager ([`fa62a8a`](https://gitlab.psi.ch/bec/bec/-/commit/fa62a8a9c96da44439ba71ae82d8020c8a2a0de5))

## v0.23.1 (2023-08-31)

### Fix

* fix: removed bec prefix from file path ([`9a3b20f`](https://gitlab.psi.ch/bec/bec/-/commit/9a3b20f085232369c9320bb8f54b93fb6b0b1686))

### Test

* test: fixed test for new base path ([`3c55393`](https://gitlab.psi.ch/bec/bec/-/commit/3c553933ac4350300c8ece72c13a6f741216d760))

## v0.23.0 (2023-08-29)

### Feature

* feat: added device precision ([`4177fe6`](https://gitlab.psi.ch/bec/bec/-/commit/4177fe6038a10e2f285fc18c13ef6a77022b17e5))

* feat: added support for user scripts from plugins and home directory ([`cd59267`](https://gitlab.psi.ch/bec/bec/-/commit/cd59267e780586b002cd80c692a0f38c213f999d))

### Fix

* fix: fixed live table for hinted signals ([`4334567`](https://gitlab.psi.ch/bec/bec/-/commit/43345676533a402fac517fd467c98b46f35658aa))

### Refactor

* refactor: fixed formatting ([`dbca77e`](https://gitlab.psi.ch/bec/bec/-/commit/dbca77ec5e46d3498a5a82bd4202082ce904c35c))

* refactor: fixed formatter ([`0446717`](https://gitlab.psi.ch/bec/bec/-/commit/044671730ed31916a5936f2b5bd104c65db081d0))

### Test

* test: added tests for live feedback ([`aa2d685`](https://gitlab.psi.ch/bec/bec/-/commit/aa2d68535e7f30e489a7e2735a7cd472c4973335))

## v0.22.0 (2023-08-24)

### Feature

* feat: added acquisition config and readout_time ([`f631759`](https://gitlab.psi.ch/bec/bec/-/commit/f63175941bbf7d9f5448ff58b9ea942bd2e1b9a4))

## v0.21.1 (2023-08-21)

### Fix

* fix: fixed bug in device config update ([`940737f`](https://gitlab.psi.ch/bec/bec/-/commit/940737fe6c8295423390a76b784a5984a93c7043))

### Refactor

* refactor: removed outdated/unused monitor_devices ([`73c0348`](https://gitlab.psi.ch/bec/bec/-/commit/73c03484fb7b7d1b2b5ed7bb40dd13bc31c38496))

### Test

* test: fixed test ([`9aeadff`](https://gitlab.psi.ch/bec/bec/-/commit/9aeadff27a63edf338a65412a398d9ff3223c9fe))

## v0.21.0 (2023-08-20)

### Feature

* feat: inject device_manager based on signature ([`4eb9cf4`](https://gitlab.psi.ch/bec/bec/-/commit/4eb9cf494c805cdf751e459f0b9d0b7aa3ebee91))

## v0.20.0 (2023-08-20)

### Feature

* feat: added device precision to rpc base class ([`2c7b55f`](https://gitlab.psi.ch/bec/bec/-/commit/2c7b55f828f3f68ff05095a007724e499797126b))

* feat: added option to specify thread names ([`cae0ba2`](https://gitlab.psi.ch/bec/bec/-/commit/cae0ba2d3ea659a7de3936acdc257e1aa0991311))

* feat: added support for multiple queues; still WIP ([`9019cc2`](https://gitlab.psi.ch/bec/bec/-/commit/9019cc2c7443c38c47160af843eef7e3f070a25b))

### Fix

* fix: fixed interceptions for multiple queues ([`4e5d0da`](https://gitlab.psi.ch/bec/bec/-/commit/4e5d0da38b06f11e6abe5ce23687cdf237c9ffeb))

* fix: removed primary queue from init; cleanup ([`bb04271`](https://gitlab.psi.ch/bec/bec/-/commit/bb042716fecbc3035483184e494e9e4f3d2d82da))

### Refactor

* refactor: added thread names ([`746cff2`](https://gitlab.psi.ch/bec/bec/-/commit/746cff26dd156566d15a0678db28fddce720492f))

* refactor: renamed primary to monitored ([`863dbc8`](https://gitlab.psi.ch/bec/bec/-/commit/863dbc86bbd6c53052c9066e65bd64f7c02dbaa8))

* refactor: renamed stream to readout_priority ([`1802e29`](https://gitlab.psi.ch/bec/bec/-/commit/1802e29b3d3dd4d00b89c6ea66881ab8143e15c7))

## v0.19.0 (2023-08-20)

### Feature

* feat: added dap to client ([`0ea549a`](https://gitlab.psi.ch/bec/bec/-/commit/0ea549a599f4ac3dccffe7fa2f148e48a0c5d7c1))

* feat: add bec_worker_manager.py ([`f0ba36d`](https://gitlab.psi.ch/bec/bec/-/commit/f0ba36db869b8a0e06918ef1fd9fc44a87cbd217))

* feat: pluging support for data_processing ([`9e33418`](https://gitlab.psi.ch/bec/bec/-/commit/9e334185260e5f92964e1f3f5b5d6d3a86d4c1d6))

### Fix

* fix: remove parameters for saxs_imaging_processor ([`39c7a9c`](https://gitlab.psi.ch/bec/bec/-/commit/39c7a9c0be0a0b9861961e5443f313e11fb35748))

* fix: fixed dap worker for plugins ([`e2f3d8f`](https://gitlab.psi.ch/bec/bec/-/commit/e2f3d8f29ddc771798d0e2cc43f7f0d85db00fe9))

### Test

* test: added missing tests ([`30b3cb1`](https://gitlab.psi.ch/bec/bec/-/commit/30b3cb18ff70ff3db93a7fc585a1287df905ceb3))

* test: added logger output ([`11d7b41`](https://gitlab.psi.ch/bec/bec/-/commit/11d7b411c0466ab12f311a5c0fe9fb954a79f238))

* test: ensure that values are beyond limits ([`7c5c3ff`](https://gitlab.psi.ch/bec/bec/-/commit/7c5c3ff73599b4cdb95d68b5c442214ac5ca6204))

## v0.18.1 (2023-08-19)

### Ci

* ci: fixed path to explorer ([`3a319e2`](https://gitlab.psi.ch/bec/bec/-/commit/3a319e2006ef1b0edcc16a606e1dcefb08d2b505))

* ci: disabled end2end test with API server for now until the server is back in operation ([`9303171`](https://gitlab.psi.ch/bec/bec/-/commit/930317156cb09e9473eff36d875ae4252176bb7b))

* ci: added dummy functional account ([`c468a7a`](https://gitlab.psi.ch/bec/bec/-/commit/c468a7ab18d3c676628ed14826148e073633d750))

* ci: fixed path to openapi file ([`6bb20c2`](https://gitlab.psi.ch/bec/bec/-/commit/6bb20c2d2d64ffa967a21695ffe33478a7a0e9ab))

### Fix

* fix: removed timeout ([`29df4ac`](https://gitlab.psi.ch/bec/bec/-/commit/29df4ac19ac189f4d7666c2c47c4539cf5e94372))

* fix: fixed bug in wait function for aborted move commands ([`019fcda`](https://gitlab.psi.ch/bec/bec/-/commit/019fcdaa074dcb67c84132cb038067dca8578830))

### Refactor

* refactor: improved scan report ([`2ebe440`](https://gitlab.psi.ch/bec/bec/-/commit/2ebe44053523ed14b69552daf63fa088e2ee0e1a))

* refactor: removed outdated timeout function ([`caf64e3`](https://gitlab.psi.ch/bec/bec/-/commit/caf64e31bc603b4df3bd84d8101d671de8a75b36))

### Test

* test: fixed import ([`72b61d0`](https://gitlab.psi.ch/bec/bec/-/commit/72b61d05bf31f6164dd7fb015217cc43a364fcc7))

### Unknown

* ci update ([`63a4209`](https://gitlab.psi.ch/bec/bec/-/commit/63a420962e36bf8085a9d7b41773d38cf1acc32d))

* ci update ([`fb2bd31`](https://gitlab.psi.ch/bec/bec/-/commit/fb2bd311472bc77bbd4703aa2a2133fcddb5b7c5))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`79d81af`](https://gitlab.psi.ch/bec/bec/-/commit/79d81afcfcd1917ae73d1cd9f298726217ebc5d3))

* ci update ([`d2f8eba`](https://gitlab.psi.ch/bec/bec/-/commit/d2f8eba62c60d2ddcaad28b1511a4ae63b1de4c5))

* ci update ([`f3dda89`](https://gitlab.psi.ch/bec/bec/-/commit/f3dda89b3b772c6eac5c857c606ea7d293d85b4c))

## v0.18.0 (2023-08-15)

### Ci

* ci: allow repo update to fail ([`e2b9a5e`](https://gitlab.psi.ch/bec/bec/-/commit/e2b9a5e76f9d5324198f0bba4b340a54c80d2783))

### Feature

* feat: scan signature is now exported; simplified scan init ([`f35b04a`](https://gitlab.psi.ch/bec/bec/-/commit/f35b04a676a8c6aa972f031d83cb637b346d5d4f))

### Fix

* fix: fixed typo in round_roi_scan init; added test ([`75f2217`](https://gitlab.psi.ch/bec/bec/-/commit/75f221758f939c510a7766101cc3faa0250a0b6b))

* fix: fixed bug in unpack_scan_args for empty lists ([`a693f84`](https://gitlab.psi.ch/bec/bec/-/commit/a693f84816d9074a3f4664a8530d0b130702f7a2))

* fix: added missing file ([`f55a518`](https://gitlab.psi.ch/bec/bec/-/commit/f55a518b9103f93b54c872fb4387956cb783d5b8))

## v0.17.2 (2023-08-10)

### Ci

* ci: added workflow to avoid detached pipelines ([`26eb77d`](https://gitlab.psi.ch/bec/bec/-/commit/26eb77dbfdddc1b018fa571166d9622ec73c0036))

### Fix

* fix: added MessageObject eq dunder ([`563c628`](https://gitlab.psi.ch/bec/bec/-/commit/563c6285092b9d8e33e8c93dea95986b87f5c67a))

### Refactor

* refactor: moved trim to separate function ([`dc954e2`](https://gitlab.psi.ch/bec/bec/-/commit/dc954e2b3c380b665d695cf5616480ae51dec2c1))

### Test

* test: added redis connector tests ([`2f30c64`](https://gitlab.psi.ch/bec/bec/-/commit/2f30c64cd76f15b81b9f128d9a5562f35be85a8a))

## v0.17.1 (2023-08-10)

### Fix

* fix: fixed default config ([`8ad8d84`](https://gitlab.psi.ch/bec/bec/-/commit/8ad8d84e00a62306d43862192c8a16b09e17a17b))

### Refactor

* refactor: unified service configs ([`89d4bb3`](https://gitlab.psi.ch/bec/bec/-/commit/89d4bb37c3d30b5c0649b524a9eca6f7bdba8a19))

## v0.17.0 (2023-08-10)

### Build

* build: added bec rtd ([`495a2bb`](https://gitlab.psi.ch/bec/bec/-/commit/495a2bb3a88c4b521225aff43ef310a24ec8fbd9))

### Feature

* feat: added stream consumer ([`b4043e9`](https://gitlab.psi.ch/bec/bec/-/commit/b4043e970ac0d3fe2bbd6cb8d386967aefcf812d))

### Fix

* fix: fixed scans if redis is not available ([`b0467a8`](https://gitlab.psi.ch/bec/bec/-/commit/b0467a86aaf4741484ef0fb66e6441e742142cb5))

* fix: fixed scan number if redis is not available ([`8514d2d`](https://gitlab.psi.ch/bec/bec/-/commit/8514d2d6384516f53fd75d4ef671e24f32fad0f4))

* fix: fixed bec_service if service keys are not available ([`9b71f77`](https://gitlab.psi.ch/bec/bec/-/commit/9b71f77dacf0fe1313fe6f0c1e9de73572286b96))

### Refactor

* refactor: reverted to decorators with warning ([`dc0e61b`](https://gitlab.psi.ch/bec/bec/-/commit/dc0e61be09b918df3aecdcbc4cdd98067510eec5))

## v0.16.3 (2023-08-06)

### Documentation

* docs: updated style; added css ([`6ec5fac`](https://gitlab.psi.ch/bec/bec/-/commit/6ec5facd0cdf0588c6545828c53ccc9e8ed29875))

* docs: added simple ophyd description; added file_manager description ([`48cfcb6`](https://gitlab.psi.ch/bec/bec/-/commit/48cfcb6c6242c381aea71d0e1c686d10e3fb2c1b))

### Fix

* fix: catch redis connection errors ([`31efa96`](https://gitlab.psi.ch/bec/bec/-/commit/31efa96cec20540a00f0be199e8fda4fa04fdc68))

* fix: fixed default arg for initialize ([`b65aba8`](https://gitlab.psi.ch/bec/bec/-/commit/b65aba8a5fcdb8f2f5eeb488725144f46267f074))

* fix: wait for bec server should only be done for ipython, not the bec lib ([`9dfe389`](https://gitlab.psi.ch/bec/bec/-/commit/9dfe38943f2b8d6be051612de9f31ad8171f1073))

* fix: scanbundler sets status to running ([`d0d46ba`](https://gitlab.psi.ch/bec/bec/-/commit/d0d46ba76b1351f5431d7c93a6d6591c250563d7))

### Test

* test: fixed client tests for new wait_for_server procedure ([`1934827`](https://gitlab.psi.ch/bec/bec/-/commit/19348275eb0a7f9690621e53a4237a2db62b12bf))

* test: fixed cached readout signature ([`74d63a1`](https://gitlab.psi.ch/bec/bec/-/commit/74d63a19d2cbc3f84710227632171489f3ca5a93))

* test: fixed referenced readout ([`8ec7b23`](https://gitlab.psi.ch/bec/bec/-/commit/8ec7b2329dda24548338d4c2d1bac39f4e0b208a))

## v0.16.2 (2023-08-05)

### Fix

* fix: fixed check_storage for already removed scan storage items ([`4a4dace`](https://gitlab.psi.ch/bec/bec/-/commit/4a4daceaf4b7c579cb4adead784f9900b675b5dc))

## v0.16.1 (2023-08-05)

### Fix

* fix: added thread lock to file writer ([`27e85bb`](https://gitlab.psi.ch/bec/bec/-/commit/27e85bb8b0e5afc0c70618438506727cea883253))

## v0.16.0 (2023-08-04)

### Build

* build: added option to install bec without redis / tmux ([`588968e`](https://gitlab.psi.ch/bec/bec/-/commit/588968e2fa29f25d2f2ced59821e7d57ef3e1cf9))

### Documentation

* docs: added missing reference file ([`df19570`](https://gitlab.psi.ch/bec/bec/-/commit/df19570c9d658b35a04dbe7112c454793a8a2e54))

* docs: added logo ([`3c40a28`](https://gitlab.psi.ch/bec/bec/-/commit/3c40a2856c7678d14517bfcae6fe2c935756f68d))

* docs: fixed requirements ([`76e9342`](https://gitlab.psi.ch/bec/bec/-/commit/76e93429f6eb3851c5fabc78ff425e28b3ba2427))

* docs: added glossary ([`b54e56f`](https://gitlab.psi.ch/bec/bec/-/commit/b54e56fe8fd7f29b2499770c7c392cdcf7e72fe8))

* docs: fixed indent ([`fe07a70`](https://gitlab.psi.ch/bec/bec/-/commit/fe07a702df434714fd500fc983502e106e410bee))

* docs: fixed references ([`20254fb`](https://gitlab.psi.ch/bec/bec/-/commit/20254fb628206f934238f40765a3fa5d15c3274c))

* docs: updated developer instructions ([`823094a`](https://gitlab.psi.ch/bec/bec/-/commit/823094acb1b06074ef3180d2717986020b911b4f))

* docs: redesigned documentation ([`ecf3ee9`](https://gitlab.psi.ch/bec/bec/-/commit/ecf3ee93de1fd0ea0f4694150c8c07fcc21da4b5))

### Feature

* feat: added support for file references and external links in the bec master file ([`9a59bdc`](https://gitlab.psi.ch/bec/bec/-/commit/9a59bdce90110fded772bf4efd84b10e019a7837))

* feat: added done entry to filemessage ([`2c62fd7`](https://gitlab.psi.ch/bec/bec/-/commit/2c62fd72b16cc62840daba929c1afd8dc26956d0))

* feat: added support for endpoints with and without suffix ([`ce0e54e`](https://gitlab.psi.ch/bec/bec/-/commit/ce0e54e561ad5ef03898e749e7333dc7535bf0d2))

### Fix

* fix: removed dummy link ([`de2c8ab`](https://gitlab.psi.ch/bec/bec/-/commit/de2c8ab2c51357dd23e9efbf8481fa99adb11326))

* fix: removed unnecessary config assignment in client ([`9360570`](https://gitlab.psi.ch/bec/bec/-/commit/93605707bd1ec1efea51407c593b25e0e5b75620))

### Test

* test: fixed file writer test for new message endpoint ([`57e31b7`](https://gitlab.psi.ch/bec/bec/-/commit/57e31b7da61fe555d2051bb0b8e38ad4752d3c9f))

### Unknown

* doc: updated developer instructions ([`9e3bfc8`](https://gitlab.psi.ch/bec/bec/-/commit/9e3bfc8139c2fa140ee15b55b4aed4190587a7a4))

## v0.15.0 (2023-08-03)

### Documentation

* docs: updated sphinx conf file to deal with md files; added copy button ([`7f48ce6`](https://gitlab.psi.ch/bec/bec/-/commit/7f48ce6aa1f2000993a4fb31e23a3efa3c122a57))

* docs: minor improvements for scan_to_csv docs ([`21d371a`](https://gitlab.psi.ch/bec/bec/-/commit/21d371a80b8009e1df3c9d4148191f05a36a0abf))

### Feature

* feat: added option to specify config path as service config ([`1a776de`](https://gitlab.psi.ch/bec/bec/-/commit/1a776de8118de7428b0c6b4e3693eaf619651192))

### Unknown

* re-enabled napoleon extension for google-style doc strings ([`c5f9ca6`](https://gitlab.psi.ch/bec/bec/-/commit/c5f9ca6c8c15ab97f1ac7843e7e2e0e4351d601d))

## v0.14.8 (2023-07-26)

### Fix

* fix: adapt write_to_csv to write multiple scan_reports for context manager ([`7118863`](https://gitlab.psi.ch/bec/bec/-/commit/71188638323f27f0ae7f643a0e8b3ade12579899))

### Test

* test: update test case ([`9390ace`](https://gitlab.psi.ch/bec/bec/-/commit/9390ace664692640df44b2ad1fb524338bf29747))

## v0.14.7 (2023-07-25)

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`94850bb`](https://gitlab.psi.ch/bec/bec/-/commit/94850bb270fae80fd32f808226a932c6952a5fed))

## v0.14.6 (2023-07-25)

### Fix

* fix: fixed build ([`4eccc99`](https://gitlab.psi.ch/bec/bec/-/commit/4eccc996694d9b260d1df40cc5b2c74ccb587dbe))

* fix: fixed bec_client install ([`bacda25`](https://gitlab.psi.ch/bec/bec/-/commit/bacda2580a47773bc4bdabc231049fb6470e7445))

## v0.14.5 (2023-07-24)

### Fix

* fix: fixed install ([`3f42f2f`](https://gitlab.psi.ch/bec/bec/-/commit/3f42f2f3e1d35e9d6f825a8f9865ab3dabf61be2))

### Refactor

* refactor: fixed formatter ([`b28b19f`](https://gitlab.psi.ch/bec/bec/-/commit/b28b19f191c922752498c06a7f6d97a9618b3359))

## v0.14.4 (2023-07-24)

### Fix

* fix: added missing init files ([`1ea9764`](https://gitlab.psi.ch/bec/bec/-/commit/1ea976411d320959a7826e6f09301df90b56517a))

* fix: added missing init files ([`29cf132`](https://gitlab.psi.ch/bec/bec/-/commit/29cf132a06ebcec7f1e1a8f084d35da0195d4489))

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`4840e52`](https://gitlab.psi.ch/bec/bec/-/commit/4840e52044701a756f9b7ac7af8ab30dc32f0e24))

## v0.14.3 (2023-07-24)

### Fix

* fix: fixed build for device_server ([`fc90bfb`](https://gitlab.psi.ch/bec/bec/-/commit/fc90bfb9aab5ef42a9c6160be71357f0df5d21bc))

* fix: fixed bec-server version ([`72fdd91`](https://gitlab.psi.ch/bec/bec/-/commit/72fdd91da495e2150463c8aa64cab1a86577289e))

## v0.14.2 (2023-07-24)

### Fix

* fix: fixed version update for bec-server ([`ae4673f`](https://gitlab.psi.ch/bec/bec/-/commit/ae4673fac049e7bff799efb7566ea5a8fba56c57))

## v0.14.1 (2023-07-24)

### Fix

* fix: update version number directly to fix pip install without -e ([`91ffa4b`](https://gitlab.psi.ch/bec/bec/-/commit/91ffa4b3c554ab4f0f038958344b81202e251433))

## v0.14.0 (2023-07-21)

### Ci

* ci: removed docs build ([`6d37777`](https://gitlab.psi.ch/bec/bec/-/commit/6d377772039ce9da269b35f18e650dee1ef6a0a5))

* ci: enforce sphinx version ([`84d0a69`](https://gitlab.psi.ch/bec/bec/-/commit/84d0a6923b19f634a475cb87c94d91b61190ad13))

### Documentation

* docs: updated build dependencies ([`8dd2116`](https://gitlab.psi.ch/bec/bec/-/commit/8dd21165f2079c64ac4e738d0f84926fd60cf887))

### Feature

* feat: add new functions to save scan to dict and csv ([`effb642`](https://gitlab.psi.ch/bec/bec/-/commit/effb642a4d3a099dd05e0f3b96ac727564e01999))

### Fix

* fix: fix writer functions ([`fda9d07`](https://gitlab.psi.ch/bec/bec/-/commit/fda9d07e65039e833f51192d4a66a48875c3be46))

* fix: code update ([`86b1985`](https://gitlab.psi.ch/bec/bec/-/commit/86b198595db33e1af6b8d2a26151658118b2ebe3))

### Test

* test: add first tests ([`2899c4b`](https://gitlab.psi.ch/bec/bec/-/commit/2899c4ba1b768b5b7993125bfb8917d5759f1d33))

## v0.13.3 (2023-07-21)

### Build

* build: added black and pylint as dev dependencies ([`3f02a27`](https://gitlab.psi.ch/bec/bec/-/commit/3f02a27ec47a5f1abd859d5f21c28b1da4c33400))

### Fix

* fix: fixed tmux launch ([`e4d7840`](https://gitlab.psi.ch/bec/bec/-/commit/e4d78402c0f0feca7d0731498b3b34701d9bc9a6))

* fix: fixed single env install ([`929689c`](https://gitlab.psi.ch/bec/bec/-/commit/929689cb8e7d1fccda0ab2a5a6372e2d48696193))

* fix: fixed bec_server install ([`2ebf580`](https://gitlab.psi.ch/bec/bec/-/commit/2ebf580ede20c594951bde73f2a570b744904509))

### Refactor

* refactor: cleanup ([`bc58541`](https://gitlab.psi.ch/bec/bec/-/commit/bc585414021fc18b7dc848ff22a5ce6e1672201a))

* refactor: cleanup ([`424e7a1`](https://gitlab.psi.ch/bec/bec/-/commit/424e7a1db25ef1d1c99da5a3fd8914c1c27123c0))

## v0.13.2 (2023-07-21)

### Documentation

* docs: removed user api for now ([`d8fd1d0`](https://gitlab.psi.ch/bec/bec/-/commit/d8fd1d0b984f4a32d090cfbebcf9a6511f734e09))

* docs: fixed dependencies; added missing files ([`87e7ec2`](https://gitlab.psi.ch/bec/bec/-/commit/87e7ec2671578ffb2f5c6db1f5d98fcdebaeb61f))

* docs: added missing glossary file ([`2529891`](https://gitlab.psi.ch/bec/bec/-/commit/2529891a2ca39e773651c3b96d70584c55115eab))

* docs: improved documentation; added how tos; added glossary ([`99f0c96`](https://gitlab.psi.ch/bec/bec/-/commit/99f0c9636b36f89dc156959184cdd31d65ffee5c))

### Fix

* fix: pip install dev environment ([`750fe66`](https://gitlab.psi.ch/bec/bec/-/commit/750fe66ed3c7c813b9ea154055f6a6f599fadc9a))

## v0.13.1 (2023-07-18)

### Ci

* ci: fixed python-semantic-release version to 7.* ([`3b203f8`](https://gitlab.psi.ch/bec/bec/-/commit/3b203f873dac520e2a26540107b4474931b31cfe))

### Fix

* fix: fixed bug in BECMessage str dunder ([`65e76a9`](https://gitlab.psi.ch/bec/bec/-/commit/65e76a93ceec953434e23432b9c5e912eabcb2c0))

## v0.13.0 (2023-07-14)

### Ci

* ci: renamed unittest stage to test ([`e990a44`](https://gitlab.psi.ch/bec/bec/-/commit/e990a44f7df88fec8c47089dc8d15065cf273d1c))

* ci: added secret detection ([`ab9a833`](https://gitlab.psi.ch/bec/bec/-/commit/ab9a833a2e60715781ef62d78a5ddd264cd89fc2))

### Feature

* feat: triggering release after refactoring (file_writer_mixin) ([`e4a51b6`](https://gitlab.psi.ch/bec/bec/-/commit/e4a51b67a63bdde93c91e07e7428759c4eb44d56))

### Refactor

* refactor: moved file writer functions to bec_lib ([`742dfff`](https://gitlab.psi.ch/bec/bec/-/commit/742dfff8ba40cb99d4451a4d10788c1e563a1b7c))

## v0.12.0 (2023-07-12)

### Feature

* feat: added message version 1.2 for better performance ([`f46b29a`](https://gitlab.psi.ch/bec/bec/-/commit/f46b29a2427137be86903df7da6684613698d0c7))

### Fix

* fix: improvements / fixes for redis streams ([`3f09cc3`](https://gitlab.psi.ch/bec/bec/-/commit/3f09cc3cd153e629ee550072d7fc5c31100594be))

### Test

* test: improved tests for redis connector ([`5d892fe`](https://gitlab.psi.ch/bec/bec/-/commit/5d892fe34550883b2a9714b6c8ee7d243e8ecfd5))

### Unknown

* Merge branch &#39;message_update&#39; of gitlab.psi.ch:bec/bec into message_update ([`bbdd7c1`](https://gitlab.psi.ch/bec/bec/-/commit/bbdd7c19eb1c92ea4c92a5235012e4c323062f66))

## v0.11.0 (2023-07-12)

### Feature

* feat: added message version 1.2 for better performance ([`fe2bd6c`](https://gitlab.psi.ch/bec/bec/-/commit/fe2bd6c935b511d26a649f89f4ba5b44ed01b7f0))

* feat: added redis stream methods to RedisProducer ([`e8352aa`](https://gitlab.psi.ch/bec/bec/-/commit/e8352aa606dc999f0e1bf1bd891a7852a489509d))

### Fix

* fix: fixed bundled messages for 1.2 ([`9381c7d`](https://gitlab.psi.ch/bec/bec/-/commit/9381c7d64684c332b90480aa8c7a6774baf3b5dd))

* fix: improvements / fixes for redis streams ([`72e4f94`](https://gitlab.psi.ch/bec/bec/-/commit/72e4f943b684e53e16ed11538d0807d012e9e357))

## v0.10.2 (2023-07-11)

### Fix

* fix: added missing x coords to lmfit processor ([`ddfe9df`](https://gitlab.psi.ch/bec/bec/-/commit/ddfe9df6a11f506e52f00be59f76b43c910d0504))

## v0.10.1 (2023-07-11)

### Fix

* fix: fixed relative path in client init; needed for pypi ([`0d9ed33`](https://gitlab.psi.ch/bec/bec/-/commit/0d9ed33a2d63e54ac12bf9cd5dcc6d4250e70bc4))

## v0.10.0 (2023-07-08)

### Build

* build: fixed bec-server config parser ([`85ecf30`](https://gitlab.psi.ch/bec/bec/-/commit/85ecf3083a304e8f505188a11486657b33b29f86))

### Ci

* ci: changed init order ([`331d282`](https://gitlab.psi.ch/bec/bec/-/commit/331d282a0b8a73452b06da53e85fca95ccc9fac6))

* ci: fixed ci path ([`96c44f6`](https://gitlab.psi.ch/bec/bec/-/commit/96c44f6c5f31537a41a4c055bfd827ae586cc833))

* ci: added en2end test ([`103bc9d`](https://gitlab.psi.ch/bec/bec/-/commit/103bc9d0e022ea2b4ae9ed26914a07e5c573cab5))

* ci: added en2end test ([`1980e87`](https://gitlab.psi.ch/bec/bec/-/commit/1980e871c119cc4e16d8564d1d51757de9f483d0))

* ci: added en2end test ([`4376a98`](https://gitlab.psi.ch/bec/bec/-/commit/4376a9876d78bae182252b5051e020c4afd7e286))

* ci: added en2end test ([`7c57bc5`](https://gitlab.psi.ch/bec/bec/-/commit/7c57bc5a33cc2d0dc9406c564d16d91d8278faa2))

* ci: added tmux ([`f7c9f49`](https://gitlab.psi.ch/bec/bec/-/commit/f7c9f49c875a2d2fdc9d1bd448df54460b33c30e))

* ci: added tmux ([`a709030`](https://gitlab.psi.ch/bec/bec/-/commit/a709030b5c5da412cd80176debdeef3b9526931c))

* ci: added tmux ([`1212ef4`](https://gitlab.psi.ch/bec/bec/-/commit/1212ef41226f238a4be98b25624ad8f0d41f74ad))

* ci: added end2end test with conda ([`779507b`](https://gitlab.psi.ch/bec/bec/-/commit/779507ba61e2a552422eb9b2f5800964b3c8270b))

* ci: added end2end test with conda ([`a131196`](https://gitlab.psi.ch/bec/bec/-/commit/a1311964be6751c630ae227d8b4d06600c1afa06))

* ci: added end2end test with conda ([`69092ff`](https://gitlab.psi.ch/bec/bec/-/commit/69092ff6f8833a10dd5485e60690315c8fa59f20))

* ci: added end2end test with conda ([`9f49a16`](https://gitlab.psi.ch/bec/bec/-/commit/9f49a166631c0ea2bafa92960c063c980bec1539))

* ci: added end2end test with conda ([`c7307ed`](https://gitlab.psi.ch/bec/bec/-/commit/c7307ed93a240c12c93455c31f67e06a8e791781))

* ci: added end2end test with conda ([`acf4e11`](https://gitlab.psi.ch/bec/bec/-/commit/acf4e11544498fd16e138e303ab1446ea3bd46e7))

### Documentation

* docs: updated deployment instructions ([`390db04`](https://gitlab.psi.ch/bec/bec/-/commit/390db0442266f1d4fc36bf8beb70715ccb692eea))

* docs: updated documentation for new deployment ([`dfc8c92`](https://gitlab.psi.ch/bec/bec/-/commit/dfc8c9247d6b4891cdfb489be2bd3dfba5fe8f40))

### Feature

* feat: added install_bec_dev script ([`db9539a`](https://gitlab.psi.ch/bec/bec/-/commit/db9539aba203e7e299620f76dfd1f3843ebfecbd))

* feat: simplified bec-server interaction; removed hard-coded service config path ([`5dd1eb7`](https://gitlab.psi.ch/bec/bec/-/commit/5dd1eb7cd0ea0d401c411c9e46b8a567e58c9687))

* feat: added default service config ([`b1a4b4f`](https://gitlab.psi.ch/bec/bec/-/commit/b1a4b4f75cad19e849d573beb767b18c6d93a308))

* feat: added clis to all services; added bec_server ([`f563800`](https://gitlab.psi.ch/bec/bec/-/commit/f563800268e7047fd9baa05e48070475688b244f))

### Fix

* fix: added missing services to the build script ([`6d45485`](https://gitlab.psi.ch/bec/bec/-/commit/6d45485b5a83d02612595c25a3fd3ec90f0c57b6))

* fix: fixed bug in ipython live update ([`a6a2c28`](https://gitlab.psi.ch/bec/bec/-/commit/a6a2c28a6a111ff552277686d7455eec9cbd56d1))

* fix: fixed missing files ([`047082b`](https://gitlab.psi.ch/bec/bec/-/commit/047082b38b7f4145c469a76f439fcac241a92b60))

* fix: adjusted import routine for plugins ([`38c4c8c`](https://gitlab.psi.ch/bec/bec/-/commit/38c4c8c93e79a37314ad5579feb77455d2a5e38f))

* fix: fixed bug in install script ([`1a7a4d8`](https://gitlab.psi.ch/bec/bec/-/commit/1a7a4d8a745ea29af4ccdc03b6b4d608b6b18fa8))

* fix: fixed bug in install script ([`05bf99a`](https://gitlab.psi.ch/bec/bec/-/commit/05bf99af739b4023ad75780fe2808f71adcc508f))

* fix: improved tmux_launcher to handle merged and separated envs ([`088b1a4`](https://gitlab.psi.ch/bec/bec/-/commit/088b1a4a1956209c11c5a31f5c09eca8aed6b86a))

### Refactor

* refactor: refactored tmux launch ([`72bdf58`](https://gitlab.psi.ch/bec/bec/-/commit/72bdf5824b6ebd7f4aadd5e5d6f094bbe5f31331))

* refactor: unified optional dependency messages ([`35c4c6a`](https://gitlab.psi.ch/bec/bec/-/commit/35c4c6aecd7e8478c1f62eab129db19bb0d3c4bf))

### Test

* test: fixed tests ([`aae5e1a`](https://gitlab.psi.ch/bec/bec/-/commit/aae5e1a05033709f8caccce34372f4caed13da42))

* test: added more tests ([`441afec`](https://gitlab.psi.ch/bec/bec/-/commit/441afec08bc4e244ca86524eac724e9ee6616721))

* test: fixed formatting ([`9d1b1c9`](https://gitlab.psi.ch/bec/bec/-/commit/9d1b1c9d3ae1a324ea9134ce8652963f82375009))

* test: fixed threading problem in callback test ([`6d56d90`](https://gitlab.psi.ch/bec/bec/-/commit/6d56d901b137070e65d51d140f2035128a4b4f7a))

## v0.9.2 (2023-07-04)

### Build

* build: added dev option ([`e669fb9`](https://gitlab.psi.ch/bec/bec/-/commit/e669fb918804517dc3969ed0dc95977de69c2a90))

### Fix

* fix: added reset_device function ([`f235a17`](https://gitlab.psi.ch/bec/bec/-/commit/f235a1735f67f25eab9ae4ed746a1c101da43dc9))

* fix: fixed re-enabling devices ([`3f11144`](https://gitlab.psi.ch/bec/bec/-/commit/3f111442584b9abf39382620ccf137c93c89d6a8))

* fix: improved getattr handling for dunder methods; added comment ([`a6c49b3`](https://gitlab.psi.ch/bec/bec/-/commit/a6c49b34ad2a6960c9db57b6ab6336bb94b432d9))

* fix: fixed bug in client callbacks that caused rejected scans to get stuck ([`2611f5b`](https://gitlab.psi.ch/bec/bec/-/commit/2611f5b4232fed7d930b21059c2cd0e8a1098a3a))

* fix: fixed bug in ipython_live_updates in case of missing status messages ([`39c4323`](https://gitlab.psi.ch/bec/bec/-/commit/39c4323303287617918d7cd7101332b338026954))

### Refactor

* refactor: removed unnecessary return ([`ba1f856`](https://gitlab.psi.ch/bec/bec/-/commit/ba1f8563ae74dbe9d5f09a67b8ad87f1d294e699))

### Test

* test: fixed client test ([`396f60f`](https://gitlab.psi.ch/bec/bec/-/commit/396f60f687f52a255cb7171dd6bd3369d939daac))

* test: fixed client test ([`e0330df`](https://gitlab.psi.ch/bec/bec/-/commit/e0330df80c21d2c2c9d502b7fe3406726f6a479b))

* test: improved client tests ([`a857cff`](https://gitlab.psi.ch/bec/bec/-/commit/a857cffa7907698ed9a64fffb7cda368201d1a77))

* test: added ipython client tests ([`a927938`](https://gitlab.psi.ch/bec/bec/-/commit/a927938c53856331fe3107ccc5767543d1dc64b7))

* test: added config handler tests ([`734c6d0`](https://gitlab.psi.ch/bec/bec/-/commit/734c6d0a36eafcef4c4c3398b3f7600b10c8ee5f))

* test: fixed test ([`0f1161b`](https://gitlab.psi.ch/bec/bec/-/commit/0f1161bd828d77b853373ddad9510218e9c48646))

## v0.9.1 (2023-07-03)

### Fix

* fix: fixed bug in device_manager that killed tab-completion ([`32d313a`](https://gitlab.psi.ch/bec/bec/-/commit/32d313a04feee1437b4aff547b3ba998266d78af))

## v0.9.0 (2023-07-02)

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`cbe0a84`](https://gitlab.psi.ch/bec/bec/-/commit/cbe0a8444456c56815b568440033258deab42589))

## v0.8.1 (2023-07-02)

### Ci

* ci: updated docker-compose.yaml ([`3f7a41f`](https://gitlab.psi.ch/bec/bec/-/commit/3f7a41fd971a4cd2b83e0b5603bded7755915f9b))

### Documentation

* docs: added data_processing services; changed default python version to 3.9 ([`233f682`](https://gitlab.psi.ch/bec/bec/-/commit/233f68216ff12ce223ea4024fe190e237df21afe))

* docs: updated doc with proper semver ([`71aa1d7`](https://gitlab.psi.ch/bec/bec/-/commit/71aa1d715a47a9b42888147611ffc8af8d46714c))

### Feature

* feat: add support for scan plugins set through environment vars ([`5ad0d9b`](https://gitlab.psi.ch/bec/bec/-/commit/5ad0d9bbe49c5a0aa1bed74f19caf8df553ee98e))

### Fix

* fix: fixed ipython client startup script for new lib name ([`b2f5f3c`](https://gitlab.psi.ch/bec/bec/-/commit/b2f5f3c2631d749ade619fd32b3f10671f9f3f1c))

### Unknown

* ci update ([`9ab13fc`](https://gitlab.psi.ch/bec/bec/-/commit/9ab13fc4f6666f5a12a2a4fa4f1e08e79b0ef2ed))

## v0.8.0 (2023-06-28)

### Feature

* feat: renamed primary devices to monitored devices; closes #75 ([`1370db4`](https://gitlab.psi.ch/bec/bec/-/commit/1370db4c70b08702c29e3728b8d0c3229d0188f3))

## v0.7.1 (2023-06-28)

### Ci

* ci: reverted to ophyd_devices master branch ([`79d5881`](https://gitlab.psi.ch/bec/bec/-/commit/79d58812cfc618b631dd265942a1bbc2c47052e4))

### Fix

* fix: remove outdated requirements.txt files ([`f781571`](https://gitlab.psi.ch/bec/bec/-/commit/f7815714ff9c9ab6c5b697edc651c376c8052e70))

* fix: setup files cleanup ([`f60889a`](https://gitlab.psi.ch/bec/bec/-/commit/f60889a87e16ff767806d47bd82a988f50fb091d))

## v0.7.0 (2023-06-28)

### Ci

* ci: fixed ophyd_devices_branch ([`3974cd4`](https://gitlab.psi.ch/bec/bec/-/commit/3974cd49a640d959983de560862b93cb9046c23f))

### Documentation

* docs: updated readme for new bec_lib ([`6e0bf12`](https://gitlab.psi.ch/bec/bec/-/commit/6e0bf12a0ae1885245961461f0bcef09ad13c2ec))

### Feature

* feat: renamed bec_client_lib to bec_lib ([`a944e43`](https://gitlab.psi.ch/bec/bec/-/commit/a944e43e1a8db55959a042a8203040fa2c5484ba))

## v0.6.14 (2023-06-27)

### Ci

* ci: added job stage dependency to deploy stage ([`15ebb27`](https://gitlab.psi.ch/bec/bec/-/commit/15ebb275975f862ab15724c623950917ec53858e))

* ci: changes build order ([`c7afe0f`](https://gitlab.psi.ch/bec/bec/-/commit/c7afe0f15e23d2047bae5d207f6ccc6effef5a21))

### Documentation

* docs: added scan server readme ([`1663087`](https://gitlab.psi.ch/bec/bec/-/commit/1663087ff8866dff31a6974474b56dd3e73ffb1d))

* docs: added readme for bec-client-lib ([`bd39147`](https://gitlab.psi.ch/bec/bec/-/commit/bd391470f86ece1e26b629c75341b2ee2c941da4))

### Fix

* fix: testing build ([`6849b95`](https://gitlab.psi.ch/bec/bec/-/commit/6849b9583ff0b3c5f4b49180f78b1ef612669145))

## v0.6.13 (2023-06-27)

### Fix

* fix: added env vars ([`3d33d4b`](https://gitlab.psi.ch/bec/bec/-/commit/3d33d4bc32d2daac29cef6e71d5e0d48aba54f7e))

## v0.6.12 (2023-06-27)

### Fix

* fix: build test ([`899cfab`](https://gitlab.psi.ch/bec/bec/-/commit/899cfaba35fe40457635d3c8b9840da762e4b0ba))

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`8109c21`](https://gitlab.psi.ch/bec/bec/-/commit/8109c21a84b5a4bb1fdd87eafd8bc9de9f58d05a))

## v0.6.11 (2023-06-27)

### Fix

* fix: build process with env var ([`3c5f351`](https://gitlab.psi.ch/bec/bec/-/commit/3c5f35166af19faa51fef75aed48a3ded0a186e4))

* fix: testing build ([`5f20c5e`](https://gitlab.psi.ch/bec/bec/-/commit/5f20c5e32d304e973bf02e496b1c0bcc6990a302))

## v0.6.10 (2023-06-27)

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`170ef69`](https://gitlab.psi.ch/bec/bec/-/commit/170ef697acc68e19d3c3eb68dd6f10b9ce77de8f))

## v0.6.9 (2023-06-27)

### Fix

* fix: testing build ([`d5fb551`](https://gitlab.psi.ch/bec/bec/-/commit/d5fb5511c79dfc598089d42a184fca26a35e6b3b))

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`edabe65`](https://gitlab.psi.ch/bec/bec/-/commit/edabe65c90730855c81aefb215f7e6ec2852f223))

## v0.6.8 (2023-06-27)

### Ci

* ci: added external shell script for build process ([`1d801c7`](https://gitlab.psi.ch/bec/bec/-/commit/1d801c7feb28a5e286a605aaa78034c0a6f5b785))

### Fix

* fix: fixed build script ([`5bba42a`](https://gitlab.psi.ch/bec/bec/-/commit/5bba42a898c2b8ec5735d1f059012ac60e2222a9))

* fix: testing release ([`240d402`](https://gitlab.psi.ch/bec/bec/-/commit/240d4020b80f371d3001a59fe55ac1433edb93d9))

## v0.6.7 (2023-06-27)

### Ci

* ci: set testpypi as target repository ([`d0d8aff`](https://gitlab.psi.ch/bec/bec/-/commit/d0d8afff556ebe151949d860e012ee899ac0c956))

* ci: added pypi builds ([`0579200`](https://gitlab.psi.ch/bec/bec/-/commit/0579200acb6898e9fec881e11d57c12f84b54db9))

* ci: removed static mongodb version ([`55f0716`](https://gitlab.psi.ch/bec/bec/-/commit/55f071631df53932863f934369bb14c67b592bab))

* ci: fixed docker image; moved docker compose to private registry ([`3e9dc7f`](https://gitlab.psi.ch/bec/bec/-/commit/3e9dc7f459ca13a7390c201ec33132a4262973a1))

* ci: moved to morgana-harbor registry ([`de370db`](https://gitlab.psi.ch/bec/bec/-/commit/de370db0376150293d9f1209a8923038e618d67b))

* ci: fixed missing pytest dependency ([`4ccc66a`](https://gitlab.psi.ch/bec/bec/-/commit/4ccc66a3a73c28d4a2312bfa0e850f3eb02d6f17))

### Documentation

* docs: improved config helper doc strings ([`08f6ff4`](https://gitlab.psi.ch/bec/bec/-/commit/08f6ff444e24395ee759f203123d9962441f59dd))

### Fix

* fix: fixed and improved setup.cfg files ([`b04a97e`](https://gitlab.psi.ch/bec/bec/-/commit/b04a97edbb4309d0364f19df528401ad29c62c9b))

### Test

* test: added config_helper tests ([`dd10525`](https://gitlab.psi.ch/bec/bec/-/commit/dd10525df4507c87c9d040412f62807b2fcd3f0b))

## v0.6.6 (2023-06-25)

### Fix

* fix: fixed file writer for empty time stamps ([`bc5fbf6`](https://gitlab.psi.ch/bec/bec/-/commit/bc5fbf651c39c562de2b2568011c47094e155017))

## v0.6.5 (2023-06-25)

### Ci

* ci: fix async callback test ([`08cfdff`](https://gitlab.psi.ch/bec/bec/-/commit/08cfdffb5a2c85e4d5f6fcbb33f01d7e1b9573ea))

### Fix

* fix: fixed timestamps for h5 files; closes #76 ([`36ab89e`](https://gitlab.psi.ch/bec/bec/-/commit/36ab89e51e031697f1611a1a1c5b946d3c7c1c2a))

### Refactor

* refactor: minor refactoring ([`1800e78`](https://gitlab.psi.ch/bec/bec/-/commit/1800e788c08cdd00505f1084735762d967ed25e8))

## v0.6.4 (2023-06-23)

### Fix

* fix: added missing remove_device_tag function ([`a0884ce`](https://gitlab.psi.ch/bec/bec/-/commit/a0884cea22ee32026753b0cec449c7003a2b49b5))

### Test

* test: added more device_manager tests ([`08e60a0`](https://gitlab.psi.ch/bec/bec/-/commit/08e60a0513cedcbc41d61272932b2e6cd412cad1))

## v0.6.3 (2023-06-23)

### Ci

* ci: fixed docker setup ([`89c3b96`](https://gitlab.psi.ch/bec/bec/-/commit/89c3b96b5c651657c613df9cc12b8ed43d968553))

### Fix

* fix: fixed typo ([`3cc4418`](https://gitlab.psi.ch/bec/bec/-/commit/3cc44186ab8ada514c7d950bd2acbb5b03ac8e25))

* fix: version variable is pulled from semantic release file ([`6669bce`](https://gitlab.psi.ch/bec/bec/-/commit/6669bce3e178ca71d664adf9a7493e7ecad4589d))

## v0.6.2 (2023-06-23)

### Fix

* fix: fixed scan item for intermediate repr queries ([`a915a69`](https://gitlab.psi.ch/bec/bec/-/commit/a915a6906667cff85ab62e22a9bb0ec8f96a2656))

### Refactor

* refactor: use scan item repr in scan report ([`85d0c44`](https://gitlab.psi.ch/bec/bec/-/commit/85d0c44cff1d478c784dfa9226d7f7d2d34a956f))

### Test

* test: added scan item tests ([`8e63cfc`](https://gitlab.psi.ch/bec/bec/-/commit/8e63cfcc9b587f51fab5dc5418d55dc362832234))

### Unknown

* Merge branch &#39;scan_server_tests&#39; of gitlab.psi.ch:bec/bec into scan_server_tests ([`1d336cb`](https://gitlab.psi.ch/bec/bec/-/commit/1d336cb5e00cc33c4156efc4ab2522cef98d62e6))

## v0.6.1 (2023-06-23)

### Ci

* ci: fixed branch reset ([`6eeb8b0`](https://gitlab.psi.ch/bec/bec/-/commit/6eeb8b087421c0f1d2d4ba8fb9cdfe92e147d3ff))

### Documentation

* docs: improved doc strings for scans ([`25fe364`](https://gitlab.psi.ch/bec/bec/-/commit/25fe3641442f1fe31000685664881aaa01c9cfb3))

### Fix

* fix: fixed scan item for intermediate repr queries ([`9decff2`](https://gitlab.psi.ch/bec/bec/-/commit/9decff27a74af7d84f41ddd8f9b3585e1d353a88))

* fix: fixed monitor scan for numpy v1.25 ([`870c033`](https://gitlab.psi.ch/bec/bec/-/commit/870c03344cd55d22a89d236d88ec60e7677ed20e))

### Refactor

* refactor: use scan item repr in scan report ([`33dda01`](https://gitlab.psi.ch/bec/bec/-/commit/33dda012ccdde515fdbf2f6811895a0f59c9e376))

* refactor: minor cleanup ([`5e40221`](https://gitlab.psi.ch/bec/bec/-/commit/5e4022161774f3b6125176041877852d7163fafd))

### Test

* test: fixed scan item test ([`1b27b54`](https://gitlab.psi.ch/bec/bec/-/commit/1b27b54fa8338d3c05984645599c99115025b689))

* test: added scan item tests ([`2eff23b`](https://gitlab.psi.ch/bec/bec/-/commit/2eff23bd7d59e89ebb948a3cc6da21e3ce1cd73d))

* test: added scan server tests ([`4f0b9b0`](https://gitlab.psi.ch/bec/bec/-/commit/4f0b9b046920470f073bcb5be1e181fa12eb3a74))

* test: more scan server tests ([`00ad593`](https://gitlab.psi.ch/bec/bec/-/commit/00ad593d5cdb56d876a8ca3148c8e3dc0c9261dd))

## v0.6.0 (2023-06-22)

### Ci

* ci: fixed switch to branch/tag ([`251d7d5`](https://gitlab.psi.ch/bec/bec/-/commit/251d7d57786afcea1e8c8d0fed39ae3fb91087dc))

### Feature

* feat: add to_pandas method to scan items ([`858bb78`](https://gitlab.psi.ch/bec/bec/-/commit/858bb7816d02e0326492cc6d53a18d3b4fa646e9))

## v0.5.0 (2023-06-20)

### Ci

* ci: removed workflow for now ([`191c92e`](https://gitlab.psi.ch/bec/bec/-/commit/191c92eed3cc51e7a0b83eda8f78c06e4ac9dc7d))

### Documentation

* docs: add commit message info to readme ([`2d8038b`](https://gitlab.psi.ch/bec/bec/-/commit/2d8038bac7ecb3563025ceddfe08b177f94bdf6c))

### Feature

* feat: added bec data processing service ([`17213da`](https://gitlab.psi.ch/bec/bec/-/commit/17213da46b236cb5ff7155890e4319308350ba4c))

* feat: added dap message and endpoint ([`e1aa5e1`](https://gitlab.psi.ch/bec/bec/-/commit/e1aa5e199b10cf9c7570967c01a5f3b48bfe1fc6))

## v0.4.9 (2023-06-19)

### Documentation

* docs: added more doc strings ([`c8cc156`](https://gitlab.psi.ch/bec/bec/-/commit/c8cc15632d4221877a19296bb7d8b7742c1e4ccd))

### Fix

* fix: raise when device does not exist; added str dunder for devices ([`12e2d29`](https://gitlab.psi.ch/bec/bec/-/commit/12e2d29dad71c11586cee06cb0688557c3cb4bb2))

### Test

* test: fixed device init ([`6339246`](https://gitlab.psi.ch/bec/bec/-/commit/6339246cb18e0f1b15f435fdcce06a7d264a17a5))

* test: fixed tests for unknown devices ([`4d10165`](https://gitlab.psi.ch/bec/bec/-/commit/4d10165a81c7d87076544e335b2ce8c8a483cd02))

## v0.4.8 (2023-06-19)

### Ci

* ci: added default run ([`b04e38c`](https://gitlab.psi.ch/bec/bec/-/commit/b04e38cef5128e0c2f08e88125c4dfaa7055fede))

* ci: added workflow ([`4383157`](https://gitlab.psi.ch/bec/bec/-/commit/438315712643a879e5a883d69a8c94de0a05f8f4))

### Fix

* fix: removed changelog dependency ([`2be1c67`](https://gitlab.psi.ch/bec/bec/-/commit/2be1c67cbc7a025314a665c6d272ac2874e02fee))

### Unknown

* Update .gitlab-ci.yml ([`352f899`](https://gitlab.psi.ch/bec/bec/-/commit/352f8996626d1ab07edde18aa1b7c99f1ebfc7b7))

* Update .gitlab-ci.yml ([`bf4c85d`](https://gitlab.psi.ch/bec/bec/-/commit/bf4c85d07d6e40b08e6e2db7d3d632c4dc1c6e27))

* Update .gitlab-ci.yml ([`8a9d5a3`](https://gitlab.psi.ch/bec/bec/-/commit/8a9d5a30eeba89387f6d6e596297df4ad6f2fb84))

## v0.4.7 (2023-06-19)

### Fix

* fix: fixed typo ([`f59e73c`](https://gitlab.psi.ch/bec/bec/-/commit/f59e73cbb11c1242115b1b42b97cbeb0f0f6252b))

* fix: fixed weird semantic-release syntax ([`eabb210`](https://gitlab.psi.ch/bec/bec/-/commit/eabb210b6e0e68269854026a8a71c07cd9274c04))

## v0.4.6 (2023-06-19)

### Fix

* fix: removed pypi upload ([`0b28025`](https://gitlab.psi.ch/bec/bec/-/commit/0b280253701b5e49ea37512cda6bad888e4b8149))

## v0.4.5 (2023-06-19)

### Fix

* fix: removed build ([`1171e65`](https://gitlab.psi.ch/bec/bec/-/commit/1171e651959df0b07f4e9ce096a8b6e4e77b132b))

## v0.4.4 (2023-06-19)

### Fix

* fix: disabled upload to repository ([`2e56468`](https://gitlab.psi.ch/bec/bec/-/commit/2e564681016b1b369c65087ab447444eca8a2c9a))

## v0.4.3 (2023-06-19)

### Fix

* fix: pull from origin ([`6c659a9`](https://gitlab.psi.ch/bec/bec/-/commit/6c659a94c4dbd5b7a4a3718c08b6fd1b117c3602))

* fix: checkout master instead of commit ([`33e0669`](https://gitlab.psi.ch/bec/bec/-/commit/33e0669323e3fb01d079fb56018349d190537101))

* fix: added git pull ([`7e77444`](https://gitlab.psi.ch/bec/bec/-/commit/7e77444a70647706ae448186fb44c64a3622880c))

* fix: fixed domain name ([`a3c2e5f`](https://gitlab.psi.ch/bec/bec/-/commit/a3c2e5ff85dbdd6badc182828ee85b6e01dc6377))

* fix: added hvcs domain ([`32856c5`](https://gitlab.psi.ch/bec/bec/-/commit/32856c50047c6a91a10f2a3666738dc6b7f16737))

### Unknown

* Update .gitlab-ci.yml ([`84c5b02`](https://gitlab.psi.ch/bec/bec/-/commit/84c5b0234bef53da7815922d1532eb8243c0f702))

* Update .gitlab-ci.yml ([`b8d3c21`](https://gitlab.psi.ch/bec/bec/-/commit/b8d3c21d0f23736b0830f7b9ed3eda476a3a61bb))

## v0.4.2 (2023-06-19)

### Fix

* fix: changed semantic-release version to publish ([`5e12ef4`](https://gitlab.psi.ch/bec/bec/-/commit/5e12ef43171b6b75abd666aabd9060f132e53fce))

* fix: delete all local tags before adding new ones ([`b8d71f5`](https://gitlab.psi.ch/bec/bec/-/commit/b8d71f5cabf80d099bf76687758f398bff9214e1))

* fix: only run semver on master; added git tag log ([`b63d128`](https://gitlab.psi.ch/bec/bec/-/commit/b63d128cefb50dfdb52328bae7032a22cd9d5934))

* fix: np.vstack must receive tuple ([`3286d46`](https://gitlab.psi.ch/bec/bec/-/commit/3286d46163e4ce7d262c170a0d04a59f287b40c1))

### Unknown

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`dd53c7e`](https://gitlab.psi.ch/bec/bec/-/commit/dd53c7eb9c6a3bacd83c293c7d96d8b150db3f9c))

* Semantic release ([`83f809b`](https://gitlab.psi.ch/bec/bec/-/commit/83f809bbf76642d87e0704bb7cca566e8607452b))

## v0.4.1 (2023-06-19)

## v0.4.0 (2023-06-16)

### Ci

* ci: upgraded docker and dind version to 23 ([`7e0c73a`](https://gitlab.psi.ch/bec/bec/-/commit/7e0c73aa9445e09fc2e812c13b6c594ee19a1c6f))

* ci: removed ophyd_devices branch ([`61fae3c`](https://gitlab.psi.ch/bec/bec/-/commit/61fae3c79563306a24b2ebb827984aa046d67810))

* ci: fixed dockerfile ([`c263548`](https://gitlab.psi.ch/bec/bec/-/commit/c263548947a4f8632b698f590c72ef30a63f66f0))

* ci: fixed dockerfile ([`5a1e5ba`](https://gitlab.psi.ch/bec/bec/-/commit/5a1e5baca0e71dd5bc42ada493c430730a296b75))

* ci: added bec_client_lib to ci tests ([`2c50442`](https://gitlab.psi.ch/bec/bec/-/commit/2c504421bc97f3afa1d7a14ba9a8d4bffbd1ddaa))

* ci: added bec_client_lib to ci tests ([`af13f0b`](https://gitlab.psi.ch/bec/bec/-/commit/af13f0b3868897ce8f397d526cb07bc4b1a6f98e))

* ci: fixed test init ([`732995a`](https://gitlab.psi.ch/bec/bec/-/commit/732995af833de8a2e8d1211284b88d09abae2ee1))

* ci: fixed python image ([`dfa9cdf`](https://gitlab.psi.ch/bec/bec/-/commit/dfa9cdfc0630af6feb6f3cbcebb95e531c9e1831))

* ci: fixed build order ([`ec5b0a3`](https://gitlab.psi.ch/bec/bec/-/commit/ec5b0a351f8a025ffb37ba9522a13ce19c5b2bce))

* ci: fixed bug in ci file ([`4dae74f`](https://gitlab.psi.ch/bec/bec/-/commit/4dae74f5642b84b3e64f37a37c7746b27373bfb0))

* ci: added python3.11 tests; added end2end tests without scibec ([`8a538de`](https://gitlab.psi.ch/bec/bec/-/commit/8a538de290712eed482e8a274ab9d92efeae9b67))

* ci: removed light end2end for now ([`33b2e76`](https://gitlab.psi.ch/bec/bec/-/commit/33b2e7694bb05038eb561380cbb24cf438e2a144))

* ci: added end2end-light ([`6dfb75b`](https://gitlab.psi.ch/bec/bec/-/commit/6dfb75b88526fcf904aadfd840b99e2a7be77e33))

* ci: moved from alpine to 3.8 ([`8e5464b`](https://gitlab.psi.ch/bec/bec/-/commit/8e5464bfeeb6c75abf87c8e4959701134be41e1e))

* ci: update openapi schema file during the pipeline ([`079a3e0`](https://gitlab.psi.ch/bec/bec/-/commit/079a3e06c82acf50d3fa6d3cf626d755c02cfba7))

* ci: removed pytest parallel ([`f732736`](https://gitlab.psi.ch/bec/bec/-/commit/f73273662ade38e3dfb76ceed9f378cbf1ed168d))

* ci: added pytest parallel ([`ba3d52f`](https://gitlab.psi.ch/bec/bec/-/commit/ba3d52ff31824682a07717e3a9af0d1bc9d41e9b))

* ci: added pytest parallel ([`20e0549`](https://gitlab.psi.ch/bec/bec/-/commit/20e054907d1363ce5ef413ae68dfc79ae2d7e930))

* ci: added needs ([`58d77e2`](https://gitlab.psi.ch/bec/bec/-/commit/58d77e2f6e48adfb96feb4c1877f475939f2890b))

* ci: added pipeline report ([`9b3cde4`](https://gitlab.psi.ch/bec/bec/-/commit/9b3cde4f62c74039c19212f051f39d3d9aff11b1))

* ci: fixed typo ([`f970c97`](https://gitlab.psi.ch/bec/bec/-/commit/f970c9785c13db19e1a446f0a4b3116de315d6ce))

* ci: added tests for different python versions ([`6af39af`](https://gitlab.psi.ch/bec/bec/-/commit/6af39af1648397a8ca21c9cd3e4a977729dcecac))

* ci: moved requirements to requirements.txt file ([`411a310`](https://gitlab.psi.ch/bec/bec/-/commit/411a310e65b67d7489e7cecc8996108ef7f3ff59))

* ci: fixed path to test_config ([`0120ccc`](https://gitlab.psi.ch/bec/bec/-/commit/0120ccca26919861d2f0a59f86643a62fe4245ea))

* ci: fixed path to test_config ([`04613a7`](https://gitlab.psi.ch/bec/bec/-/commit/04613a7bf0db86d7568b0712fd156bd45fb9aae9))

* ci: cleanup ([`ecfd39e`](https://gitlab.psi.ch/bec/bec/-/commit/ecfd39e33e95020172c80203cac65b13cc4bb021))

* ci: added logger to waiting function ([`5f9345a`](https://gitlab.psi.ch/bec/bec/-/commit/5f9345ae6ff00ab655ac49c38e2f685da2fb0aca))

### Documentation

* docs: added missing file ([`f8fa8f4`](https://gitlab.psi.ch/bec/bec/-/commit/f8fa8f4136068b2370c8f63c23eb29c1cbd84a39))

* docs: updated instructions for creating a new config file ([`0491837`](https://gitlab.psi.ch/bec/bec/-/commit/0491837041323afe71d64bc2971207741dab7145))

* docs: updated docs for new redis config ([`e88fa30`](https://gitlab.psi.ch/bec/bec/-/commit/e88fa309c7806f3a6488728a5463434373d4dd55))

* docs: updated drawings ([`009ed3b`](https://gitlab.psi.ch/bec/bec/-/commit/009ed3b830fd648ad98929db3d4194feca6b1be7))

* docs: added bec context image ([`3b1d9e7`](https://gitlab.psi.ch/bec/bec/-/commit/3b1d9e7f9fb4d1331d54f6672548c35575104207))

* docs: added bec context image ([`581792c`](https://gitlab.psi.ch/bec/bec/-/commit/581792c674c90709edd18349c994d1b8e95eb87a))

* docs: update drawings ([`40459f6`](https://gitlab.psi.ch/bec/bec/-/commit/40459f67c09bdc965c34678af485ad4943bca460))

* docs: updated BEC c4 drawing ([`7ccb80d`](https://gitlab.psi.ch/bec/bec/-/commit/7ccb80d2d32ae3871b35b482ec818d778108ac8a))

* docs: added bec architecture ([`5be499c`](https://gitlab.psi.ch/bec/bec/-/commit/5be499cc8ed0cc40198ef4286cbb5ce43b149b93))

* docs: updated drawio ([`4b7981e`](https://gitlab.psi.ch/bec/bec/-/commit/4b7981e9cf3c9ca1d234f4679710e2d7d8cbde44))

* docs: updated config db drawing ([`e39c3f4`](https://gitlab.psi.ch/bec/bec/-/commit/e39c3f489eb4d47d0709be27accfc25d63c98e1c))

* docs: cleanup ([`1381f74`](https://gitlab.psi.ch/bec/bec/-/commit/1381f74e43bcd74302f4a5827f4897c8067e1a8e))

* docs: updated tutorial ([`0a8b7dc`](https://gitlab.psi.ch/bec/bec/-/commit/0a8b7dc5268adbd47e5c2b5a48c79fc53ba890c6))

* docs: removed switcher ([`c802d9e`](https://gitlab.psi.ch/bec/bec/-/commit/c802d9e40809388f940422d159095f3a3bd62c11))

* docs: added version switcher ([`eaaff10`](https://gitlab.psi.ch/bec/bec/-/commit/eaaff100a12e888b5904a5709e20f00c522c44d2))

* docs: fixed requirements formatting ([`e6beda3`](https://gitlab.psi.ch/bec/bec/-/commit/e6beda3b9c8d634efa1f855ca94fb91d167d4a95))

* docs: fixed requirements formatting ([`783d406`](https://gitlab.psi.ch/bec/bec/-/commit/783d406eea778228898e0070a0a31b5847346494))

* docs: improved doc string for lamNI move to scan center ([`6cc3e51`](https://gitlab.psi.ch/bec/bec/-/commit/6cc3e51d57565076d4d47f7e5e150b828fa45475))

### Feature

* feat: added option to override the singleton client ([`db0f2f7`](https://gitlab.psi.ch/bec/bec/-/commit/db0f2f7864323feadcb8bbcf56614682316ec692))

* feat: first version of bec_client_lib ([`cd58b13`](https://gitlab.psi.ch/bec/bec/-/commit/cd58b1358ca4cc9e0855b6c1ec0034ab1fcfd14f))

* feat: first version of bec_client_lib ([`d66149d`](https://gitlab.psi.ch/bec/bec/-/commit/d66149db27ed60e7656c4d98a994db1779c85bd7))

* feat: improved becmessage repr for easy loading from string ([`acc5949`](https://gitlab.psi.ch/bec/bec/-/commit/acc59499532e0a415c08e70b7a45b87cf7b72022))

* feat: added scan_item repr ([`b611fbb`](https://gitlab.psi.ch/bec/bec/-/commit/b611fbbda2abc1ceae57b3d78f75c69889c64eaa))

* feat: added event callback ([`9e11f66`](https://gitlab.psi.ch/bec/bec/-/commit/9e11f66d8040052f7d36269b2cecce32d02eae5d))

* feat: added semver to ci ([`672a6ad`](https://gitlab.psi.ch/bec/bec/-/commit/672a6adef4060e92882e907c1f329ebce90972da))

* feat: added customized alarm handling for bec errors in ipython ([`fa9723b`](https://gitlab.psi.ch/bec/bec/-/commit/fa9723b28230cb0d64815b75d4295dedf76f62cd))

* feat: added _raised_alarms ([`ae5ba37`](https://gitlab.psi.ch/bec/bec/-/commit/ae5ba37716634705d4abcd621c6fca3a04f65356))

* feat: added device description to device report ([`5b34204`](https://gitlab.psi.ch/bec/bec/-/commit/5b34204336349a255b4df3a17b98b81dba4adaf6))

* feat: file writer raises minor error when file is not written ([`3800917`](https://gitlab.psi.ch/bec/bec/-/commit/3800917695eca93738ab42f0704df46b5692bb07))

* feat: added xtreme plugin ([`342c2a6`](https://gitlab.psi.ch/bec/bec/-/commit/342c2a6f148fe26ca9d160576cca1e2871e324fe))

* feat: added settling time; fixed burst_at_each_point; removed exp_time as req kwarg ([`12ae5c7`](https://gitlab.psi.ch/bec/bec/-/commit/12ae5c715ef4bfda3fb19273f51a49cf7f5df251))

* feat: added readout_priority as replacement for scan_motors ([`adedc1b`](https://gitlab.psi.ch/bec/bec/-/commit/adedc1b83bf45f888092538c51bd778f47f09dc1))

* feat: added event publisher to scihub ([`a2efb91`](https://gitlab.psi.ch/bec/bec/-/commit/a2efb91d1b57945418bac6650bb6c014a5047063))

* feat: added baseline publisher ([`165e59e`](https://gitlab.psi.ch/bec/bec/-/commit/165e59e1948d521d7ac660e0c705a49c697acd76))

* feat: added baseline endpoint ([`f630272`](https://gitlab.psi.ch/bec/bec/-/commit/f630272fee3b67f65addb897e5c15f3ff6395595))

* feat: added support for rpc status ([`87716db`](https://gitlab.psi.ch/bec/bec/-/commit/87716dbbafedc8f69210b9aa9da927653a0593b1))

* feat: added support for rpc status return values ([`1fcd6ff`](https://gitlab.psi.ch/bec/bec/-/commit/1fcd6ffb25c43e9fc6e17b1e6628232c232b3727))

* feat: added scoped import for ophyd devices ([`e644c19`](https://gitlab.psi.ch/bec/bec/-/commit/e644c19e061631086386e184b21545e5afdcf5e7))

* feat: added option to hide the table and only show the progressbar ([`c0d76b1`](https://gitlab.psi.ch/bec/bec/-/commit/c0d76b1c5af46d3b366089b5ed0551d813a24cff))

* feat: added support for nested dataset id cms ([`ada6493`](https://gitlab.psi.ch/bec/bec/-/commit/ada649387b3abd9dba5b53319f11c4ad195f477a))

* feat: online backend changes to support scan and dataset entries ([`06be92c`](https://gitlab.psi.ch/bec/bec/-/commit/06be92c21d8fec6488d65e97a10525604e037cfc))

* feat: added event controller ([`e25d077`](https://gitlab.psi.ch/bec/bec/-/commit/e25d0773c9e87b6eaf2e239617668b7ffc0c83ad))

* feat: upgraded scibec to new db structure ([`84d76d3`](https://gitlab.psi.ch/bec/bec/-/commit/84d76d3a6d3e19c81c97a3185785cbcc30ce84df))

* feat: added support for new scibec structure ([`b65259d`](https://gitlab.psi.ch/bec/bec/-/commit/b65259d4492a0fe9dc7efba577dec80fc3b65327))

* feat: active account is now pulled from redis ([`0837bc8`](https://gitlab.psi.ch/bec/bec/-/commit/0837bc8959a81be4e08952d332b7e05ca0e1f14f))

* feat: added scilog to scihub ([`7c297b3`](https://gitlab.psi.ch/bec/bec/-/commit/7c297b32d85c5822a95665cdf3e6f3d800d1ae1c))

* feat: added logbook and account endpoints ([`ae13604`](https://gitlab.psi.ch/bec/bec/-/commit/ae13604b344f40ad86377f36d46519db957768ab))

* feat: added console log; added target account property ([`7a77429`](https://gitlab.psi.ch/bec/bec/-/commit/7a77429a4cebb7c10a1100dbe291ed057089d33d))

* feat: added hyst_scan; online changes ([`ff5706c`](https://gitlab.psi.ch/bec/bec/-/commit/ff5706c03dc001374055c1985fe4f44af005c494))

* feat: added support for intermediate scan_report_instructions ([`03027f3`](https://gitlab.psi.ch/bec/bec/-/commit/03027f3ae02cff96492bdda1a4ea05d359e7a9a8))

* feat: added otf scan ([`09f636e`](https://gitlab.psi.ch/bec/bec/-/commit/09f636e61849c6f1090198d98e9571adba3e457e))

* feat: added complete and support for new kickoff signature ([`c7c1c44`](https://gitlab.psi.ch/bec/bec/-/commit/c7c1c44be608f9d96b594fc2098f91cf5a0562bc))

* feat: added flyer event and callback ([`636ee79`](https://gitlab.psi.ch/bec/bec/-/commit/636ee7950080db477a97acc3c9da6b696988ada5))

* feat: added becmessage version 1.1; added option to select compression ([`0de43a8`](https://gitlab.psi.ch/bec/bec/-/commit/0de43a800f916b61c393384c038ef3425e3b9cc5))

* feat: improved device info ([`1fd83d4`](https://gitlab.psi.ch/bec/bec/-/commit/1fd83d4c6a8e3937425e120b12e446b5ff6cde17))

* feat: added scan history ([`cb3ce8b`](https://gitlab.psi.ch/bec/bec/-/commit/cb3ce8b91b5d8cac445baef8d2182395b0277dbc))

* feat: added metadata to callbacks ([`1a14e00`](https://gitlab.psi.ch/bec/bec/-/commit/1a14e0000eaced0eefcbf14b41cc0bfee2fe3d2d))

* feat: added scan callbacks ([`3ebc910`](https://gitlab.psi.ch/bec/bec/-/commit/3ebc9108928e3a753f7db4c1cf39bcf866f372f3))

* feat: added config action set ([`511cbcb`](https://gitlab.psi.ch/bec/bec/-/commit/511cbcbf4072011cd05ae0fe9a80977c08aa4a29))

* feat: added scihub service ([`bbabee1`](https://gitlab.psi.ch/bec/bec/-/commit/bbabee1c0c76433b0cfa1e967ebcce55f62739cd))

* feat: decoupled scibec from core services; added config to redis ([`d846d55`](https://gitlab.psi.ch/bec/bec/-/commit/d846d55cde40b124db7756caadcaa36968d034f9))

* feat: added bec metrics ([`a3fa79b`](https://gitlab.psi.ch/bec/bec/-/commit/a3fa79bb9fa39c5ed6b6d3f8b8b80c1f922fd5c1))

* feat: added monitor scan ([`8ac476e`](https://gitlab.psi.ch/bec/bec/-/commit/8ac476e178979f5091e7a9c918fecb80756999b8))

* feat: added time scan ([`e77c5a6`](https://gitlab.psi.ch/bec/bec/-/commit/e77c5a6bb0da5f7bc071655132768e46b090c528))

* feat: added list scan ([`32fab04`](https://gitlab.psi.ch/bec/bec/-/commit/32fab041a2a4bf81b6f082187638415407cbd56a))

* feat: added linter to check the imported user scripts ([`6cc2e6a`](https://gitlab.psi.ch/bec/bec/-/commit/6cc2e6a700509e4ce9e30339ff603b19423e0eb5))

* feat: added emitter log ([`07bbaa0`](https://gitlab.psi.ch/bec/bec/-/commit/07bbaa05f325cc7aed25c19531b130ebd2ec3840))

* feat: made emitter modular ([`63cc4ff`](https://gitlab.psi.ch/bec/bec/-/commit/63cc4ffe93351ca1a808eed1ec16f6f7f61add43))

* feat: added bec cli command; added bec_startup script ([`15e71e0`](https://gitlab.psi.ch/bec/bec/-/commit/15e71e073226f3eb895f7a8829dafffc7a0071a5))

* feat: added scan_report_devices ([`558416a`](https://gitlab.psi.ch/bec/bec/-/commit/558416a2f8530d9df2147f5c8f415f12bacca746))

* feat: added scan report instructions ([`35cd892`](https://gitlab.psi.ch/bec/bec/-/commit/35cd892d2bdbaa5922bad1c52bf13bef7f99e21c))

* feat: added multiple iterations for corridor optim ([`1dff48e`](https://gitlab.psi.ch/bec/bec/-/commit/1dff48ea049948614dfe269f5588eeac8b3495d1))

* feat: added phase plates ([`97ea86c`](https://gitlab.psi.ch/bec/bec/-/commit/97ea86c710de0738951f0d6889e2a4cfcdd55817))

* feat: added user params to lamni config ([`48c9f94`](https://gitlab.psi.ch/bec/bec/-/commit/48c9f94b545a76d1ccf1dfab444534859a3f4835))

* feat: added access to optics mixin from align ([`4089f35`](https://gitlab.psi.ch/bec/bec/-/commit/4089f35d5ea97fb4ef0bfc12295addf1da45b696))

* feat: added logbook message for beam checks ([`f72881d`](https://gitlab.psi.ch/bec/bec/-/commit/f72881d66ec09254afd54b294b56bfb169bf5872))

* feat: added scilog export for lamni ([`f6def4f`](https://gitlab.psi.ch/bec/bec/-/commit/f6def4f6ff86130be7efb831e45497c65422086e))

* feat: added show_all; minor improvements ([`03e63ce`](https://gitlab.psi.ch/bec/bec/-/commit/03e63cef167acce0764b4162ced7cee9022d5a66))

* feat: added script to test the validity of configs ([`2958427`](https://gitlab.psi.ch/bec/bec/-/commit/2958427d64381c7e7f49381cb0251342993cdc38))

* feat: added device_schema ([`8b26e81`](https://gitlab.psi.ch/bec/bec/-/commit/8b26e8153251ba06ad7bf471826f9f42ad28c1aa))

* feat: added beamline info ([`f80de69`](https://gitlab.psi.ch/bec/bec/-/commit/f80de691d6be48cc02ae1cd4c2a151f35de030ce))

* feat: moved beam checks to redis ([`69e8a2b`](https://gitlab.psi.ch/bec/bec/-/commit/69e8a2bdbd9fd3de60351d0ae308f4b34de59ef9))

* feat: added test config cSAXS ([`539ae01`](https://gitlab.psi.ch/bec/bec/-/commit/539ae01a64eb02cd00fab695e78929aa34456398))

* feat: added user functions to show all commands ([`8259cd3`](https://gitlab.psi.ch/bec/bec/-/commit/8259cd3a5488f51c527dd29bab3451d9cb36a629))

* feat: added option to change the readout priority ([`28e1500`](https://gitlab.psi.ch/bec/bec/-/commit/28e15001fc94d8c26ff79e665e870b22b1a2d4a1))

* feat: added wm ([`7a29d43`](https://gitlab.psi.ch/bec/bec/-/commit/7a29d43383bc9224560919c46d232ef242760fa8))

* feat: added option to skip the signal filtering ([`a593424`](https://gitlab.psi.ch/bec/bec/-/commit/a593424fe2815e42f8315dbce91aa43a797e4b7f))

* feat: added on_failure options to device_server ([`b96a931`](https://gitlab.psi.ch/bec/bec/-/commit/b96a93141f2ed8077864119605fe87f45daba421))

* feat: added acquisition priority ([`13927dc`](https://gitlab.psi.ch/bec/bec/-/commit/13927dc8d6d872f0bb0893d2d19001edd3df765d))

* feat: added show_tags ([`45dcf76`](https://gitlab.psi.ch/bec/bec/-/commit/45dcf767a0b7815d5e3afda57a23e4a940e1cc5e))

* feat: added support for device tags ([`d00a81d`](https://gitlab.psi.ch/bec/bec/-/commit/d00a81dde7920cdc02c0a1ea5c7315716e2ef195))

* feat: added on_failure updates to device_manager ([`ac3cfaa`](https://gitlab.psi.ch/bec/bec/-/commit/ac3cfaa5599be8182f898055d90404b6e417a5ca))

* feat: added semver log to pre-commit ([`b9f6bb5`](https://gitlab.psi.ch/bec/bec/-/commit/b9f6bb575921251f8d422ff6dcedb25a9a26af9a))

### Fix

* fix: fixed message reader for bundled messages ([`4d7b141`](https://gitlab.psi.ch/bec/bec/-/commit/4d7b141fb0c452eecf2f56330d3eacafb631923b))

* fix: fixed default writer ([`73f555f`](https://gitlab.psi.ch/bec/bec/-/commit/73f555f8457918251f46cef504268ddb7f5a95c8))

* fix: fixed async callbacks for BECClient ([`087595d`](https://gitlab.psi.ch/bec/bec/-/commit/087595dbf45a29818e6a53e631a9d7d5e4a71fa7))

* fix: fixed sync scan item callbacks ([`1ae04ac`](https://gitlab.psi.ch/bec/bec/-/commit/1ae04ac193ec9bb7a52cabf940a5aeb230288761))

* fix: fixed async callbacks for BECClient ([`337d6e6`](https://gitlab.psi.ch/bec/bec/-/commit/337d6e61723d6cbf1db7b096bd39bdab03b1d9b3))

* fix: fixed bec magics for new live_updates structure ([`5433b35`](https://gitlab.psi.ch/bec/bec/-/commit/5433b35d4a8c2230d9f506994eabb030a37d414b))

* fix: fixed ip exception handler for ScanInterruptions ([`074ec13`](https://gitlab.psi.ch/bec/bec/-/commit/074ec1362bd1dff4d634e55935b2aa6c1c511f41))

* fix: fixed feedback for queued scans ([`a5c16fe`](https://gitlab.psi.ch/bec/bec/-/commit/a5c16feff717e75e793555cea9f600976645832a))

* fix: fixed dependencies for bec_client_lib ([`b3ff495`](https://gitlab.psi.ch/bec/bec/-/commit/b3ff49510571bdf912070b343a5336fc77ed7bdb))

* fix: fixed bec_utils dependency ([`f000f1c`](https://gitlab.psi.ch/bec/bec/-/commit/f000f1c87a8694ffccdb0ba1e5ca7b945ea6486c))

* fix: checkout correct ophyd branch ([`1ec4567`](https://gitlab.psi.ch/bec/bec/-/commit/1ec4567918e2152d90e30080e619e2fe6975e389))

* fix: removed bec_utils after refactoring ([`03d6a27`](https://gitlab.psi.ch/bec/bec/-/commit/03d6a274d0ab26ea5f6536e952846e617d013d01))

* fix: fixed scan object for client lib; closes #74 ([`c285019`](https://gitlab.psi.ch/bec/bec/-/commit/c28501993a7696bdadb63011c339f049ec60f2c7))

* fix: fixed startup script after mixin changes ([`844cbc1`](https://gitlab.psi.ch/bec/bec/-/commit/844cbc1e0f67b95d1aee7a6af16e8bb170898a94))

* fix: fixed tests ([`dbd2e73`](https://gitlab.psi.ch/bec/bec/-/commit/dbd2e735a5886c55b1876baf3efe9f15cb956f5e))

* fix: bug fixes related to client_lib refactoring ([`79d5604`](https://gitlab.psi.ch/bec/bec/-/commit/79d5604e67443c161b56d7164774f81d596d86d5))

* fix: fixed client dependency ([`82e3384`](https://gitlab.psi.ch/bec/bec/-/commit/82e3384cd2ddb5bda45376f9bf2a26d3f29a49e3))

* fix: fixed startup script after mixin changes ([`e25c085`](https://gitlab.psi.ch/bec/bec/-/commit/e25c085d29ca4999d8e9e12abaaff72466c6f76c))

* fix: fixed tests ([`018d781`](https://gitlab.psi.ch/bec/bec/-/commit/018d781dbfa57209ab7cb5a6ab2b265a1b5df364))

* fix: bug fixes related to client_lib refactoring ([`0a58846`](https://gitlab.psi.ch/bec/bec/-/commit/0a588462f547707222c625676782ce77060e858f))

* fix: fixed client dependency ([`bd81815`](https://gitlab.psi.ch/bec/bec/-/commit/bd81815a7d3c7806d25664425f407e56a3396f1a))

* fix: removed wait for hidden reports ([`01c3850`](https://gitlab.psi.ch/bec/bec/-/commit/01c38501084d5138988ea9a2c8338c2d1316ccc7))

* fix: fixed bug in scans._run ([`2ea8c3e`](https://gitlab.psi.ch/bec/bec/-/commit/2ea8c3e33b2b136e5de33b744b2bb003a9eb31c9))

* fix: renamed data_segment to scan_segment ([`59dfa4e`](https://gitlab.psi.ch/bec/bec/-/commit/59dfa4e175bcea01db15af20afadb0400c20e834))

* fix: added fpdf dependency ([`d317dd8`](https://gitlab.psi.ch/bec/bec/-/commit/d317dd8229db6d1fc3cf1e65adc0e7f4bd34afaa))

* fix: testing semver publish ([`a0c70a5`](https://gitlab.psi.ch/bec/bec/-/commit/a0c70a51e2ef619004d69161a118f77525e1804a))

* fix: removed apk install; not needed for python image ([`0aa9ffc`](https://gitlab.psi.ch/bec/bec/-/commit/0aa9ffcd7939ca049a860f666bf3b24ce96b1325))

* fix: added username to semver deploy ([`1c3fc4d`](https://gitlab.psi.ch/bec/bec/-/commit/1c3fc4d01ed00120229559ed6a86fb2b1907d937))

* fix: removed needs from semver job ([`88f0136`](https://gitlab.psi.ch/bec/bec/-/commit/88f01360c48d26781b8a60c638abcd83a7ee4c08))

* fix: fixed alarm_handler verbosity; changed default to Minor ([`8e3f389`](https://gitlab.psi.ch/bec/bec/-/commit/8e3f3891ce77cf69f929becea1b5357fe5d6b412))

* fix: reset logbook info on init http error ([`e48c888`](https://gitlab.psi.ch/bec/bec/-/commit/e48c8883a8dc4c26bad7e0a9daa2389fdba94a88))

* fix: fixed serializer check ([`1d13e61`](https://gitlab.psi.ch/bec/bec/-/commit/1d13e61fadaf7c9ec644f172c002a9b20a723df2))

* fix: fixed bec messages for numpy data; fixed message reader ([`96a5f1b`](https://gitlab.psi.ch/bec/bec/-/commit/96a5f1b49d2a322c7c1d591f48d3ffc6f1e70091))

* fix: added error handling to catch failed device inits ([`8036c4b`](https://gitlab.psi.ch/bec/bec/-/commit/8036c4b26e8eda082cd0bfb541604d7e787dc676))

* fix: fixed stdout and stderr redirect for tmux init ([`561a144`](https://gitlab.psi.ch/bec/bec/-/commit/561a144fb9d74977d15cba6d698e2578ecf49457))

* fix: fixed bug in primary_devices ([`79a74b1`](https://gitlab.psi.ch/bec/bec/-/commit/79a74b1b898e24a010ff8484112080c8472f1cb4))

* fix: removed scan_motor usage ([`52ff75a`](https://gitlab.psi.ch/bec/bec/-/commit/52ff75a52502c78ee247b8bde2ce217c8275d58e))

* fix: primary devices must be unique ([`0e4119e`](https://gitlab.psi.ch/bec/bec/-/commit/0e4119ebefb6428ef78d6fd0b8ee5b24e358056c))

* fix: changes related to readout_priority ([`a65aa9d`](https://gitlab.psi.ch/bec/bec/-/commit/a65aa9d055d0b09aa02f2be40cb9377c9f1ccbd7))

* fix: fixed kickoff for old interface ([`8d38101`](https://gitlab.psi.ch/bec/bec/-/commit/8d38101c741ff9c44de16e98551ba99841ef8c39))

* fix: improvements for otf; added option to wait for kickoff ([`b685301`](https://gitlab.psi.ch/bec/bec/-/commit/b6853012288a9fb3ebd991552cde8bed2ea7ddd8))

* fix: reverted black for json files ([`458e33a`](https://gitlab.psi.ch/bec/bec/-/commit/458e33a0f5e1feac0a29b0bfe01ffbb81ef3a8ce))

* fix: fixed bug in primary devices ([`d675cf3`](https://gitlab.psi.ch/bec/bec/-/commit/d675cf3264244515d8309e945ac5a36b0522e45b))

* fix: fixed primary_device list for overlapping scan motors ([`19b52ee`](https://gitlab.psi.ch/bec/bec/-/commit/19b52eef9cf9fedb48eb5fc55cb5f26a329f462a))

* fix: fixed tomo scan file for repeated angles ([`d25d974`](https://gitlab.psi.ch/bec/bec/-/commit/d25d9740f88540cc3de288314e0cb93ded7a2591))

* fix: fixed model ([`3475112`](https://gitlab.psi.ch/bec/bec/-/commit/3475112ffa01d2d0e132faa7d8c849634a89c498))

* fix: fixed weird merge conflict ([`56bd317`](https://gitlab.psi.ch/bec/bec/-/commit/56bd317e0f7c44b755c7de91638c2ff3027b4871))

* fix: fixed bug for movements without report instructions ([`4716a54`](https://gitlab.psi.ch/bec/bec/-/commit/4716a54e290e8b092c883964934f0f78d360c522))

* fix: added missing files ([`97b374f`](https://gitlab.psi.ch/bec/bec/-/commit/97b374f024fdafb4a19a16a3a360c56a6007f071))

* fix: added missing websocket file ([`6669a39`](https://gitlab.psi.ch/bec/bec/-/commit/6669a396cac76921dbdcaf5bfd4441a212ad6b0b))

* fix: fixed formatter ([`02b20a0`](https://gitlab.psi.ch/bec/bec/-/commit/02b20a0ac8c064b6b2437a030c394c7722fc75bf))

* fix: fixed formatter ([`50d12f3`](https://gitlab.psi.ch/bec/bec/-/commit/50d12f3961bf7ef305d8c4138d1610e638c3403a))

* fix: fixed formatter ([`b080060`](https://gitlab.psi.ch/bec/bec/-/commit/b080060b2f9f9ed0bedad8f99bc50bf28c57db73))

* fix: fixed formatter ([`56f8a14`](https://gitlab.psi.ch/bec/bec/-/commit/56f8a14b41dd7376ab1403e59ab167501f7edb82))

* fix: fixed dependencies ([`61c03fe`](https://gitlab.psi.ch/bec/bec/-/commit/61c03fefa1a47a4c27ec87bd902d03b67db7c6cb))

* fix: increased node version to 14.21 ([`95e8e2a`](https://gitlab.psi.ch/bec/bec/-/commit/95e8e2aefd98ac66b0b0e5034c313e61014643df))

* fix: fixed missing package ([`77a9bde`](https://gitlab.psi.ch/bec/bec/-/commit/77a9bded34eac9529d392d424a1a9fecb1944f72))

* fix: fixed bug in scilog shutdown ([`c94613b`](https://gitlab.psi.ch/bec/bec/-/commit/c94613b30c23fd7d89fac4c3378125109ea09376))

* fix: fixes path to logbookmessage ([`c3bdee3`](https://gitlab.psi.ch/bec/bec/-/commit/c3bdee3734acb4096221385f2d283896c3be3468))

* fix: online changes lamni ([`c0dba49`](https://gitlab.psi.ch/bec/bec/-/commit/c0dba49377c16f54f000098c948b267a8d78979d))

* fix: lamni online changes ([`a11b09b`](https://gitlab.psi.ch/bec/bec/-/commit/a11b09b027a3cb2d7012c4124980abdd83bcb4db))

* fix: fixed bug for umv ([`3466e60`](https://gitlab.psi.ch/bec/bec/-/commit/3466e608f258b0f1af59325ec9858edd2f0c6c52))

* fix: fixed bug in scan worker max pointid assignment ([`d4cbead`](https://gitlab.psi.ch/bec/bec/-/commit/d4cbead1decbcfdf968660f03699a4dc3c6bb3e3))

* fix: fixed monitor scan update ([`0c468a5`](https://gitlab.psi.ch/bec/bec/-/commit/0c468a5717884e319826f85ccd1f09a5c9ce963f))

* fix: fixed encoding ([`8ca63da`](https://gitlab.psi.ch/bec/bec/-/commit/8ca63da3153725f5fccac68edeab712aba34378a))

* fix: fixed repr string ([`8dc2d6f`](https://gitlab.psi.ch/bec/bec/-/commit/8dc2d6f61a9259b28aa9e3ec91674aa10cc1151f))

* fix: fixed sub devices info name ([`a37e057`](https://gitlab.psi.ch/bec/bec/-/commit/a37e0572347c09bd1ecfeea8e08934cb20b3c836))

* fix: fixed merge conflict ([`0b66cb0`](https://gitlab.psi.ch/bec/bec/-/commit/0b66cb0ce5f9e41abfa2b32657deaaa1f2c495ee))

* fix: fixed file writer ([`7ff72f1`](https://gitlab.psi.ch/bec/bec/-/commit/7ff72f12ddfa6ca0d197ee3ec31515c3d2b7dacc))

* fix: fixed bug in file_writer ([`3f21d40`](https://gitlab.psi.ch/bec/bec/-/commit/3f21d406139ae0577ee5ef6752be448053ad9bc1))

* fix: fixed fly scan motors ([`245e1c8`](https://gitlab.psi.ch/bec/bec/-/commit/245e1c8d0e45417b852801e98d3982a8dcbda153))

* fix: fixed bug in monitor scan ([`6fe0984`](https://gitlab.psi.ch/bec/bec/-/commit/6fe0984fe007e81272568dbc116d1e1de45a4054))

* fix: moved flyer to hint-based ([`11fb30f`](https://gitlab.psi.ch/bec/bec/-/commit/11fb30f64320f712ec93b24323079db7fe4831cb))

* fix: fixed save_conig_file for locally created configs ([`81d82ed`](https://gitlab.psi.ch/bec/bec/-/commit/81d82ed8977f0f417ac6e8807d7eec8e383c8a16))

* fix: added sleep to ensure that the device server starts processing the data first. Should be changed to a reply from SciHub ([`e65a6a2`](https://gitlab.psi.ch/bec/bec/-/commit/e65a6a23cbab9bbd231459f0953392150b6fc7d4))

* fix: fixed logger for scan status paused and halted ([`c352ce0`](https://gitlab.psi.ch/bec/bec/-/commit/c352ce0128c8c8bfc05268282fea221809cf5569))

* fix: added scan status messages for halted and paused ([`c239c41`](https://gitlab.psi.ch/bec/bec/-/commit/c239c41394e47ea9abb8846fa18d483abbb8e8a5))

* fix: fixed scan interruption message ([`b822655`](https://gitlab.psi.ch/bec/bec/-/commit/b82265594cbaef68b13d6b1f3348315e91ec9221))

* fix: skip None callbacks ([`0a60289`](https://gitlab.psi.ch/bec/bec/-/commit/0a60289f0d0f3a5e23b683dafc316530010ab7b6))

* fix: only pause if queue is not empty ([`deca3d1`](https://gitlab.psi.ch/bec/bec/-/commit/deca3d1d77143379b559934e1307d2a85acea50a))

* fix: removed duplicated reload call ([`db043ea`](https://gitlab.psi.ch/bec/bec/-/commit/db043eaf47b983494ba8221ec646714e39d46665))

* fix: fixed bug in bec_client init ([`fff063c`](https://gitlab.psi.ch/bec/bec/-/commit/fff063ce2f8becdd9431eb441c525e9c12b6b43b))

* fix: fixed bug for undefined status callbacks ([`a6fe9e6`](https://gitlab.psi.ch/bec/bec/-/commit/a6fe9e614d9618be24c5da3d7604532fbfcb9fd4))

* fix: added bec status updates ([`01bf0a3`](https://gitlab.psi.ch/bec/bec/-/commit/01bf0a35dbe28928d634ce6c7e71e5948d2c53c0))

* fix: fixed rpc calls ([`183e5ae`](https://gitlab.psi.ch/bec/bec/-/commit/183e5aefafa06ed04836f03b9f7249a666ee05f5))

* fix: added config converter and validator in the absence of scibec ([`f0a7c9f`](https://gitlab.psi.ch/bec/bec/-/commit/f0a7c9faf2affbbcfdb4506e41e02866dcaa22e0))

* fix: added wait for device server before loading the session ([`1cff100`](https://gitlab.psi.ch/bec/bec/-/commit/1cff1009aa5e51f6788a2b50bce77fb0f87d1ea7))

* fix: fixed bug in init_config ([`6d33cbe`](https://gitlab.psi.ch/bec/bec/-/commit/6d33cbe6bb65d5e36dab7857f3359fd5dd1f7c68))

* fix: fixed bug in init_config ([`ace2b2f`](https://gitlab.psi.ch/bec/bec/-/commit/ace2b2f3377e7705bf4b200f1d74a73dbcaf98b0))

* fix: fixed path to config file ([`393db47`](https://gitlab.psi.ch/bec/bec/-/commit/393db479363cfe359440e79f47f250cf8b3b5638))

* fix: fixed bug in init_config ([`c9baaba`](https://gitlab.psi.ch/bec/bec/-/commit/c9baaba7f225c5f784e10286e3ccd5c4da0368ed))

* fix: added missing file ([`2cb3a5b`](https://gitlab.psi.ch/bec/bec/-/commit/2cb3a5b00f849ea52a234bd4a78550da878a076e))

* fix: fixed bug in ci file ([`64fd8d0`](https://gitlab.psi.ch/bec/bec/-/commit/64fd8d0696479fd03d9f898fe833e0754e03485b))

* fix: fixed bugs related to refactoring ([`a45d683`](https://gitlab.psi.ch/bec/bec/-/commit/a45d683f64bac1e5e62991a9d9afb66efdabb1fd))

* fix: fixes after refactoring ([`7547f8d`](https://gitlab.psi.ch/bec/bec/-/commit/7547f8d8c7cbeb3cf488f5673c1f1330ee7955e6))

* fix: added missing file ([`f256ec1`](https://gitlab.psi.ch/bec/bec/-/commit/f256ec1839ce1fdaea434452d253e998836a9736))

* fix: fixed bugs related to refactoring ([`2f61b32`](https://gitlab.psi.ch/bec/bec/-/commit/2f61b328cfb098e39f00f064bd1e4a17774d8e1c))

* fix: added redis config update to scihub init ([`821f940`](https://gitlab.psi.ch/bec/bec/-/commit/821f940470bd39b5bd6264bd02331db1d0263270))

* fix: fixed config ([`f7be217`](https://gitlab.psi.ch/bec/bec/-/commit/f7be2172a17d97e3b67f5ba91762accb82839276))

* fix: added missing files ([`baf2367`](https://gitlab.psi.ch/bec/bec/-/commit/baf23679afd4011b45bde8277dfb0d8cb085a670))

* fix: removed numpy dependency ([`f5b4a8a`](https://gitlab.psi.ch/bec/bec/-/commit/f5b4a8a0ac1b6ba48ab817fb60101811b4dd4854))

* fix: added scihub dependency ([`791fea1`](https://gitlab.psi.ch/bec/bec/-/commit/791fea1735e6fb02e627cb418cf6f0ce6f30fba7))

* fix: improvements and fixes for redis config ([`ec5f915`](https://gitlab.psi.ch/bec/bec/-/commit/ec5f9155ceac4d4df9eacd7ea5767d01d1c50029))

* fix: fixed file writer plugins ([`44e938e`](https://gitlab.psi.ch/bec/bec/-/commit/44e938ee74e4b3337b5185283ef31b9bde64c395))

* fix: fixed gitignore ([`270dc82`](https://gitlab.psi.ch/bec/bec/-/commit/270dc827300ba10157b0a7b72f684194cd50cc23))

* fix: added jsonschema to dependencies ([`a4bab2b`](https://gitlab.psi.ch/bec/bec/-/commit/a4bab2b715adfd4d1ba84fd0e23c5a7bedc9b2da))

* fix: added missing files ([`82953f9`](https://gitlab.psi.ch/bec/bec/-/commit/82953f9d4edf5638c1e2bbe8d1f69b8cc3bc1a74))

* fix: changes related to monitor scan ([`d2dbc2f`](https://gitlab.psi.ch/bec/bec/-/commit/d2dbc2fb28ac11e05ac5f1696fe4203597622f0e))

* fix: unused wait groups are ignored ([`06cd3d5`](https://gitlab.psi.ch/bec/bec/-/commit/06cd3d58c7c91da019af08ae9c23993d7d2c71e2))

* fix: fixed bug related to queue refactoring ([`2949236`](https://gitlab.psi.ch/bec/bec/-/commit/29492366e225c11e520751f60f41828eea1e8eb5))

* fix: fixed typo; fixed test ([`b2799f6`](https://gitlab.psi.ch/bec/bec/-/commit/b2799f61f7ba927da766a36628804d4471537066))

* fix: fixed DeviceManager import ([`41a19b1`](https://gitlab.psi.ch/bec/bec/-/commit/41a19b15fcdce6e0f58ccdf27936db7e738fdb6f))

* fix: fixed bug in live_table callback; #closes 64 ([`3c5e5b1`](https://gitlab.psi.ch/bec/bec/-/commit/3c5e5b12997f54ec9d31d64877f61ac1efa876a0))

* fix: fixed path to bec_config yaml file ([`9d18037`](https://gitlab.psi.ch/bec/bec/-/commit/9d180372d122b439766666f13a2f474cb40a8ad2))

* fix: fixed a typo ([`a314210`](https://gitlab.psi.ch/bec/bec/-/commit/a314210a01b976c930713cd4d6d7f844fc8be528))

* fix: cb must be specified ([`d79d005`](https://gitlab.psi.ch/bec/bec/-/commit/d79d005527f54a2a8f43dbd87a31c8544f73f4c5))

* fix: fixed kwargs forwarding for threaded consumer ([`5153847`](https://gitlab.psi.ch/bec/bec/-/commit/5153847674a377e205909ff8a6dc3a01e4223017))

* fix: change so that the topics creates a list only when topics is not None ([`e31fe6d`](https://gitlab.psi.ch/bec/bec/-/commit/e31fe6d8b729ac31512be93add108202efb23f0c))

* fix: fixed beamline mixin inheritance ([`897e5d1`](https://gitlab.psi.ch/bec/bec/-/commit/897e5d1a38282efe7faa3adb7b803e3f998f1e43))

* fix: fixed empty device messages ([`8bd4d3d`](https://gitlab.psi.ch/bec/bec/-/commit/8bd4d3d3fa4fb8eb12be19e79e9647b09842c503))

* fix: change message to logger for _trigger_device ([`5d662d1`](https://gitlab.psi.ch/bec/bec/-/commit/5d662d17ad099095350aea7ce2b6b878226d0847))

* fix: changed so that all fcns does the same ([`733ebc7`](https://gitlab.psi.ch/bec/bec/-/commit/733ebc70361d52e8991cab96020b85598c73934e))

* fix: fixed crash in exception ([`1f7e573`](https://gitlab.psi.ch/bec/bec/-/commit/1f7e57362edf75daa6e69a1b557fe393d2cf7623))

* fix: added check_alarms to wait function ([`d5abeb8`](https://gitlab.psi.ch/bec/bec/-/commit/d5abeb89fa9d259310bc048d9de5829d798af34d))

* fix: fixed callbacks for groups and scan defs; closes #32 ([`ed41416`](https://gitlab.psi.ch/bec/bec/-/commit/ed414167ad913cd22473c1da1b31d351e6e77ce1))

* fix: cleanup after lamni ([`ac2fbc1`](https://gitlab.psi.ch/bec/bec/-/commit/ac2fbc18db9eca42b5536044561491e633e7de93))

* fix: fixed userParameter assignment ([`7dc43fa`](https://gitlab.psi.ch/bec/bec/-/commit/7dc43fa29eff9fdf27bb7c97d7587095ca39ccbd))

* fix: fixed xrayeyealign init ([`a56a3a2`](https://gitlab.psi.ch/bec/bec/-/commit/a56a3a2266f81a1866b994f0c491f6933386caef))

* fix: fixed import bug ([`2813791`](https://gitlab.psi.ch/bec/bec/-/commit/2813791ae795fccfc1459f09d6d63c47d80cf864))

* fix: fixed bpm4i config ([`ed143e0`](https://gitlab.psi.ch/bec/bec/-/commit/ed143e0204b8d3461bc3228310fa67c92d25e19f))

* fix: added dummy fshon ([`2ef2d59`](https://gitlab.psi.ch/bec/bec/-/commit/2ef2d599199c3d1294113476ad08f78e32e8fd3f))

* fix: added bpm4i to default csaxs config ([`b04cf72`](https://gitlab.psi.ch/bec/bec/-/commit/b04cf72e5303483658cbae3d71378aa864d42233))

* fix: left align bl_show_all output ([`a35aa06`](https://gitlab.psi.ch/bec/bec/-/commit/a35aa0638405e01fd37f81cfcf523bb34eb8a33d))

* fix: disabled quadems for now as they fail to connect ([`0fc45ae`](https://gitlab.psi.ch/bec/bec/-/commit/0fc45ae58316077241c4619b504aa54c45c438d1))

* fix: subscriptions should only be added after the connection has been established ([`627cc45`](https://gitlab.psi.ch/bec/bec/-/commit/627cc45570ec6cf61e80f78241ce672e85a1ab90))

* fix: fixed bug in readoutPriority propert; fixed device status for strings ([`52ce000`](https://gitlab.psi.ch/bec/bec/-/commit/52ce0003e30bb4d0dee101b377a697c44f27a728))

* fix: fixed bl show output ([`58b1e25`](https://gitlab.psi.ch/bec/bec/-/commit/58b1e250fcd0f25aba85c4809218c2471eb797a0))

* fix: added threadlock to scan queue status ([`5912c0f`](https://gitlab.psi.ch/bec/bec/-/commit/5912c0f02b9ea44e8759c53a4b760e6d1b0bc910))

* fix: fixed default cSAXS config ([`95bc9a9`](https://gitlab.psi.ch/bec/bec/-/commit/95bc9a9f949b49d30395ac620e2fd2c738b63030))

* fix: fixed eiger1p5m config ([`fd795d8`](https://gitlab.psi.ch/bec/bec/-/commit/fd795d8f95101d49b8fb5cbfb98a0f7ccc1ff2c7))

* fix: fixed csaxs config ([`a03ae49`](https://gitlab.psi.ch/bec/bec/-/commit/a03ae49cd2a862f96bed1df0dc762b654f27ec3c))

* fix: fixed intermediate config write action ([`a48fff5`](https://gitlab.psi.ch/bec/bec/-/commit/a48fff5f013be19914f18f1aef960ac649ddd03c))

* fix: new scans clear the alarm stack ([`6cc2bcd`](https://gitlab.psi.ch/bec/bec/-/commit/6cc2bcdeb3ea484c4057a22c469fd47fedac9a54))

* fix: only alarms are raised; warnings are logged ([`7b01c63`](https://gitlab.psi.ch/bec/bec/-/commit/7b01c638a3aaf5c0b1056f1a80b2032628c7593e))

* fix: fixed abort level for alarms ([`548d55e`](https://gitlab.psi.ch/bec/bec/-/commit/548d55ea90aeccedcf7099a0c2e7ea43d4a037dd))

* fix: removed on_failure from scan_worker as it is now handled for each device individually ([`544d6fe`](https://gitlab.psi.ch/bec/bec/-/commit/544d6fec990e53a9d6ea03d8e52134b9ab4b699b))

* fix: fixed sls and cSAXS config for new db structure ([`6f898c6`](https://gitlab.psi.ch/bec/bec/-/commit/6f898c602d81d966ee059d2fe1808ecdf83fa3a2))

* fix: fixed test for merged db updates ([`ad56d59`](https://gitlab.psi.ch/bec/bec/-/commit/ad56d591e20bd5f8c616506104446d5bfa2e7bf5))

* fix: renamed deviceGroup to deviceTags ([`7e12750`](https://gitlab.psi.ch/bec/bec/-/commit/7e127509db7cda8fcf4f0156c9a969d306cd22f7))

* fix: moved onFailure from acquisition config to root ([`72249ca`](https://gitlab.psi.ch/bec/bec/-/commit/72249ca8730e4bcf4ab5e5863092faa8fe3ea4bc))

* fix: fixed pre/post commit ([`88d151f`](https://gitlab.psi.ch/bec/bec/-/commit/88d151fe2a56e1ff6e6e5d0729f1c324943c7b42))

* fix: fixed pre/post commit ([`2c3f36e`](https://gitlab.psi.ch/bec/bec/-/commit/2c3f36ec8c60c8b424ad838d452eeb5eb3c2fe8b))

* fix: added semver to all services ([`b32edb5`](https://gitlab.psi.ch/bec/bec/-/commit/b32edb549067334c8dfc68f060c112e8ba7230ad))

* fix: moved to separate release file ([`b29e191`](https://gitlab.psi.ch/bec/bec/-/commit/b29e191453c3fe26d80ed9e705bba4e71857b73f))

* fix: added semver log to pre-commit ([`aeb5fcb`](https://gitlab.psi.ch/bec/bec/-/commit/aeb5fcbed63037047d61bbe30a9a00996fe31d4c))

* fix: reset version ([`564e599`](https://gitlab.psi.ch/bec/bec/-/commit/564e59958a9083caf4bf64570835b4fc1263a6c1))

### Refactor

* refactor: added builtins to avoid pylint errors ([`7c9bae4`](https://gitlab.psi.ch/bec/bec/-/commit/7c9bae455d41773258b5da23b94cf63c792f8b94))

* refactor: removed unused endpoint device_last_read ([`97e09f0`](https://gitlab.psi.ch/bec/bec/-/commit/97e09f0a5545275f2922bc96dbacfad2fb0b1ddc))

* refactor: refactoring for live updates ([`36e66b6`](https://gitlab.psi.ch/bec/bec/-/commit/36e66b660045054a02e86c14043a87308c626d6d))

* refactor: removed remaining bec_utils files ([`7604797`](https://gitlab.psi.ch/bec/bec/-/commit/7604797b32e40bd29be2c53750ce0809a916db40))

* refactor: moved tests from utils to bec_client_lib ([`a47a75e`](https://gitlab.psi.ch/bec/bec/-/commit/a47a75e3917a45f4d8b43857979ce2c0b4a8e016))

* refactor: moved utils into bec_client_lib ([`f43d4eb`](https://gitlab.psi.ch/bec/bec/-/commit/f43d4ebac68e642eb8c151ebd6afb0d62709f249))

* refactor: cleanup ([`a651567`](https://gitlab.psi.ch/bec/bec/-/commit/a651567506a3828f09d7f3c0404c6305ef64b92d))

* refactor: moved wait_for_empty_queue to utils ([`73e7a64`](https://gitlab.psi.ch/bec/bec/-/commit/73e7a649855bb95c437ff707cd1223b2ee7f61ff))

* refactor: changes after rebase ([`4515618`](https://gitlab.psi.ch/bec/bec/-/commit/45156183b6e51190ddba11419b3d301dd51b7ef4))

* refactor: changed bl_show_all from inheritance to composition ([`b2e57e7`](https://gitlab.psi.ch/bec/bec/-/commit/b2e57e7d987d9c09e25fa29afadc0aa2be240747))

* refactor: changed bl_show_all from inheritance to composition ([`fb40a61`](https://gitlab.psi.ch/bec/bec/-/commit/fb40a61e77e6d38059cddecbfea295ac6c04db5f))

* refactor: cleanup ([`b730fbf`](https://gitlab.psi.ch/bec/bec/-/commit/b730fbf3b87733813c33edb9632b1a9f6b2dd8df))

* refactor: cleanup ([`893bc19`](https://gitlab.psi.ch/bec/bec/-/commit/893bc1909a731f5add76b7e7d3dfc7be443a0ec6))

* refactor: cleanup ([`0df7811`](https://gitlab.psi.ch/bec/bec/-/commit/0df7811680777fe860b24d5a434b337600cd54af))

* refactor: renamed ipython_live_updates ([`53f2876`](https://gitlab.psi.ch/bec/bec/-/commit/53f2876f7fa004545de77a47850581c45a1d10b0))

* refactor: use raise_alarms instead of looping through alarms ([`35784f3`](https://gitlab.psi.ch/bec/bec/-/commit/35784f37c38f9641de7a2bff6641241c43538456))

* refactor: fixed formatter ([`de81c30`](https://gitlab.psi.ch/bec/bec/-/commit/de81c3092483c4c618556a5ad858366ce222c6ef))

* refactor: fixed formatter ([`f749900`](https://gitlab.psi.ch/bec/bec/-/commit/f7499005a9bac7533007c6d4b302b91e989afa97))

* refactor: cleanup ([`d2459c9`](https://gitlab.psi.ch/bec/bec/-/commit/d2459c9a628420a69cadf0ad8fab1e6b697875b1))

* refactor: fixed formatting ([`9c72f89`](https://gitlab.psi.ch/bec/bec/-/commit/9c72f89144f58d5c9b08c6bf013a868693fda247))

* refactor: cleanup ([`8ebb7b2`](https://gitlab.psi.ch/bec/bec/-/commit/8ebb7b2430844e56855c34b70486f59d281d76bc))

* refactor: replaced jsonschema by fastjsonschema ([`d729fc2`](https://gitlab.psi.ch/bec/bec/-/commit/d729fc2b255b5e4ed3ae431a504be60d57f4aca8))

* refactor: moved config_helper from client to utils ([`5d326f9`](https://gitlab.psi.ch/bec/bec/-/commit/5d326f96eb05ab7f5558e153af0f7ebdfc3f4bae))

* refactor: changes related to new config management ([`d0134ca`](https://gitlab.psi.ch/bec/bec/-/commit/d0134ca4beca24206a20356cc43c3a065a9e5b94))

* refactor: replaced epylint by pylint.run ([`20f3804`](https://gitlab.psi.ch/bec/bec/-/commit/20f38044a27e0f42d16eb5f602cfb17a42bd7bdc))

* refactor: removed influxdb forwarder ([`9a5c003`](https://gitlab.psi.ch/bec/bec/-/commit/9a5c0035964e0f9a6fd4f04526eb5fb15027f859))

* refactor: removed DeviceManagerDeviceServer ([`6a04837`](https://gitlab.psi.ch/bec/bec/-/commit/6a04837697ba23e72af8c230fb5b77a8a99b7a02))

* refactor: upgraded to black 23.1 ([`989dd1f`](https://gitlab.psi.ch/bec/bec/-/commit/989dd1fd8742c1f143e5885b5c2dce1763074edb))

* refactor: upgraded to black 23.1 ([`49b938d`](https://gitlab.psi.ch/bec/bec/-/commit/49b938d391f66731ca4785a757678a4bb93e1a0a))

* refactor: upgraded to black 23.1 ([`36e5965`](https://gitlab.psi.ch/bec/bec/-/commit/36e5965d61a081f2ce0edf4d4f86f92a6b6af6db))

* refactor: minor refactoring for testing ([`f8c0ef6`](https://gitlab.psi.ch/bec/bec/-/commit/f8c0ef620adbf7691610a43a05be2369e93636b8))

* refactor: minor refactoring ([`98c870a`](https://gitlab.psi.ch/bec/bec/-/commit/98c870a662fa3ad72b7819296f3568eb7e134e1a))

* refactor: improvements for bluesky emitter ([`84310b8`](https://gitlab.psi.ch/bec/bec/-/commit/84310b8ef61f4dcccf83f9960b67dbd2c25d4dfa))

* refactor: added on_cleanup emitter ([`8791ca5`](https://gitlab.psi.ch/bec/bec/-/commit/8791ca572555ca0b83f25f973fb0801165e44f3d))

* refactor: removed pipeline ([`66b329e`](https://gitlab.psi.ch/bec/bec/-/commit/66b329eaf6b29b293cf6a07e50586d8933cf17c3))

* refactor: refactored emitterbase ([`d8a0d6a`](https://gitlab.psi.ch/bec/bec/-/commit/d8a0d6ad94dd8a29146edf5829ba8456605dae82))

* refactor: removed DeviceManagerSB ([`2e7321d`](https://gitlab.psi.ch/bec/bec/-/commit/2e7321d2d0758b34b7c3418c76d596b65fd5a8fa))

* refactor: moved emitterbase to new file ([`dce87ab`](https://gitlab.psi.ch/bec/bec/-/commit/dce87ab157af23107d8b5d0c96ef4e70694b391f))

* refactor: refactored scan bundler ([`6583509`](https://gitlab.psi.ch/bec/bec/-/commit/6583509fa91f33d0de0fa015e93a1ca59cce0ebe))

* refactor: minor refactoring ([`7ded49c`](https://gitlab.psi.ch/bec/bec/-/commit/7ded49c65bf390b26d00b8d9d20b883f3e530067))

* refactor: refactored device list extraction ([`f77bd80`](https://gitlab.psi.ch/bec/bec/-/commit/f77bd805694ab7a26b2ab0e10720d37006dbbeac))

* refactor: cleanup ([`cfd3b19`](https://gitlab.psi.ch/bec/bec/-/commit/cfd3b19b499af2161a657257e593b2dd71e354e4))

* refactor: added mixin class for redis consumer ([`6e81164`](https://gitlab.psi.ch/bec/bec/-/commit/6e81164bc06e80172bc2e5a24a15ded2018a6444))

* refactor: merged consumer and threaded consumer ([`0649f56`](https://gitlab.psi.ch/bec/bec/-/commit/0649f56b9dea3f91289d3c45eba54aba5b243d64))

* refactor: added support for bl_show_all plugins ([`737c386`](https://gitlab.psi.ch/bec/bec/-/commit/737c386e24618171d1cb4ef77935bdc44a968507))

* refactor: deviceinstructionmessage should always have at least one device ([`8f3d6df`](https://gitlab.psi.ch/bec/bec/-/commit/8f3d6df6a1c6b0130896071aad2418ca24fd30b1))

* refactor: only pass msg, not messageobjects ([`6a3d387`](https://gitlab.psi.ch/bec/bec/-/commit/6a3d387131e400e4bc3deab1f0a8d441e7af0610))

* refactor: simplified assert_device_is_enabled; added assert_devices_is_valid ([`0739de1`](https://gitlab.psi.ch/bec/bec/-/commit/0739de1d1f1272c6efec2173a4ed6ee38b4643b0))

* refactor: added option to specify the redis cls ([`13a672d`](https://gitlab.psi.ch/bec/bec/-/commit/13a672dc4a59fa1fb05cbc9753c8dd454c9e92a9))

* refactor: cleanup ([`cd7d63a`](https://gitlab.psi.ch/bec/bec/-/commit/cd7d63a23b0f9463393dfabce5fa7da925c09cd9))

* refactor: cleanup ([`8f9f865`](https://gitlab.psi.ch/bec/bec/-/commit/8f9f8659298662744a39aa0d6e3b12b8b7307b82))

* refactor: merged send_logbook_message and send_message to always send the linkType ([`e082ee6`](https://gitlab.psi.ch/bec/bec/-/commit/e082ee6a4b2ea05108c4f724a7f518ff7b6770e3))

* refactor: removed unused import ([`8c1ec1e`](https://gitlab.psi.ch/bec/bec/-/commit/8c1ec1e637183527da3e55899620d0e863661ad7))

* refactor: improved log messages for scanstatus ([`ce8300f`](https://gitlab.psi.ch/bec/bec/-/commit/ce8300f702253b32e33d02b08122bc6f816bac5e))

* refactor: added raise alarm / warning to failed readings in ds ([`f71c494`](https://gitlab.psi.ch/bec/bec/-/commit/f71c494123094fe3482c15a117761e571736e22b))

* refactor: renamed readoutPriority enums ([`c0873aa`](https://gitlab.psi.ch/bec/bec/-/commit/c0873aae87549921aa49d2c08963a991f387d67a))

* refactor: renamed priority to readoutPriority ([`abe358d`](https://gitlab.psi.ch/bec/bec/-/commit/abe358d956a699318503c22f1213b69d7b572969))

* refactor: merged config updates ([`62420f3`](https://gitlab.psi.ch/bec/bec/-/commit/62420f30a2c97636e1cc40cbfe1a6ee36286539a))

### Test

* test: added tests; added doc strings ([`2b51ceb`](https://gitlab.psi.ch/bec/bec/-/commit/2b51cebe1c4d7b140449bbbe034b5b05bf559253))

* test: improved tests ([`fd746cc`](https://gitlab.psi.ch/bec/bec/-/commit/fd746cc8bf4137792a7a33aa5aaec2aef84f1ba0))

* test: fixed fixture ([`bcd54ae`](https://gitlab.psi.ch/bec/bec/-/commit/bcd54aede82713ff29f8668359763c5be87c5730))

* test: fixed missing import ([`2c9b60a`](https://gitlab.psi.ch/bec/bec/-/commit/2c9b60a7da9dcbb3fab9b2384eabe01615abc50a))

* test: fixed missing import ([`7c5c7f8`](https://gitlab.psi.ch/bec/bec/-/commit/7c5c7f81875b2c99353f6e9ffef768ec94ca2683))

* test: fixed missing function after refactoring ([`8f8003b`](https://gitlab.psi.ch/bec/bec/-/commit/8f8003baa16c13d2be26d5ce0de3546e9a19d0e3))

* test: fixed bec client import for end2end tests ([`e84148e`](https://gitlab.psi.ch/bec/bec/-/commit/e84148ed3c2d8554a54d61de00ca55cbf2d606d9))

* test: fixed tests ([`2cb847e`](https://gitlab.psi.ch/bec/bec/-/commit/2cb847e3b16b076497599fb0901a790f74712043))

* test: moved tests to bec lib ([`93a251f`](https://gitlab.psi.ch/bec/bec/-/commit/93a251fc82109142a83229d221c943476735ce9a))

* test: fixed bec client import for end2end tests ([`e896edb`](https://gitlab.psi.ch/bec/bec/-/commit/e896edbd3b1d589ed0674c28f112bafeb90bc171))

* test: fixed tests ([`00c0c94`](https://gitlab.psi.ch/bec/bec/-/commit/00c0c940c8a5609733d79c8d13fa68775298cc43))

* test: added ScanObject tests ([`aa63ffb`](https://gitlab.psi.ch/bec/bec/-/commit/aa63ffb2c5fb65cf6466701fc4f599189b780015))

* test: added callback tests ([`4f547a7`](https://gitlab.psi.ch/bec/bec/-/commit/4f547a7dac5db2533dd4a59ceabd41dff297bf17))

* test: added callback_handler tests ([`58b347e`](https://gitlab.psi.ch/bec/bec/-/commit/58b347e0951eb6f5f43ce6337dc706d76447a1d2))

* test: added x-ray-eye align tests ([`bffb734`](https://gitlab.psi.ch/bec/bec/-/commit/bffb7341ca9de908d29f67caff5a3b019d53d7d5))

* test: added scan guard tests ([`a94e53e`](https://gitlab.psi.ch/bec/bec/-/commit/a94e53e047035bcc3ec9a681eb46985ddf419ce2))

* test: fixed tests for min positions ([`c2578f6`](https://gitlab.psi.ch/bec/bec/-/commit/c2578f648c03c85bd9f7abf78f8ea791e003862c))

* test: fixed tests for new default exp time ([`d6b2c67`](https://gitlab.psi.ch/bec/bec/-/commit/d6b2c67a9e2944e2a873945780fbdad39831b00b))

* test: fixed test for additional scan baseline ([`4f1b80e`](https://gitlab.psi.ch/bec/bec/-/commit/4f1b80e8423bfebe1e882710d024373a59be9086))

* test: fixed messages for new rpc defaults ([`b841eca`](https://gitlab.psi.ch/bec/bec/-/commit/b841ecaa64eb538a18d40866ff3dbf5b68bfa879))

* test: fixed tests for new kickoff interface ([`fb4fa18`](https://gitlab.psi.ch/bec/bec/-/commit/fb4fa183213b699ff415668a3e386ab8120d2ee5))

* test: fixed test for new data structure ([`a9837aa`](https://gitlab.psi.ch/bec/bec/-/commit/a9837aa4fa446cd115685abe0c9e6425c8e96f70))

* test: trigger ([`f11ac5a`](https://gitlab.psi.ch/bec/bec/-/commit/f11ac5aafb768ba837beed74c36b8c2d9e62e6f7))

* test: fixed scihub tests ([`13e77ba`](https://gitlab.psi.ch/bec/bec/-/commit/13e77ba2e31a63f7bd6a2f1ac7d9f68873e65f59))

* test: fixed test for new otf implementation ([`537203c`](https://gitlab.psi.ch/bec/bec/-/commit/537203ce0c35f559c9ceeb90b162530ba7a9a461))

* test: fixed lamni tests ([`b5e3919`](https://gitlab.psi.ch/bec/bec/-/commit/b5e391999fd8500ded6a50f40ae681a8e50d3aac))

* test: fixed bug in pipeline mock ([`d24de87`](https://gitlab.psi.ch/bec/bec/-/commit/d24de874c3d31c4a778f7d0ad2124db47d3e6cc1))

* test: disabled metrics and service info threads for tests ([`28d26b6`](https://gitlab.psi.ch/bec/bec/-/commit/28d26b6c39416e9da556f337dff42dc26e273e61))

* test: disabled service info and metrics messages for mocked scan server ([`41fcde8`](https://gitlab.psi.ch/bec/bec/-/commit/41fcde8df7aa5da7016091f45ea13a73b44b1c35))

* test: removed samx check ([`a11787e`](https://gitlab.psi.ch/bec/bec/-/commit/a11787e052cb85e8fa2fd68fb40ccaa3126b6801))

* test: fixed tests ([`79a02eb`](https://gitlab.psi.ch/bec/bec/-/commit/79a02ebc35782fbb8ccc71f8997f2224537d5828))

* test: improved tests for scibec ([`cea26bb`](https://gitlab.psi.ch/bec/bec/-/commit/cea26bb89797129dfea59f4e674fac060cb4fbfb))

* test: fixed test for updated rpc schema ([`b2284bc`](https://gitlab.psi.ch/bec/bec/-/commit/b2284bcf7678aa8845be3337074d2f32940362ba))

* test: fixed tests ([`8a1e761`](https://gitlab.psi.ch/bec/bec/-/commit/8a1e7613a4bad1b1dfaead53b4ba368f1ce5a537))

* test: added more tests ([`d84cc6b`](https://gitlab.psi.ch/bec/bec/-/commit/d84cc6b0ba90e8aa1b65b1b66897c70f8693a18e))

* test: added more scihub tests ([`f68d854`](https://gitlab.psi.ch/bec/bec/-/commit/f68d85425e8a67eb64ec6905e8845f788fe9a912))

* test: fixed bug in config handler test ([`c62d84e`](https://gitlab.psi.ch/bec/bec/-/commit/c62d84ea8ca5504f1e664cf2331f0f3c54fa4df9))

* test: renamed test to avoid collision with the device_server ([`809f001`](https://gitlab.psi.ch/bec/bec/-/commit/809f0010500f4578aafd4858cb9badf78bc5cf4f))

* test: added config_handler tests ([`0848413`](https://gitlab.psi.ch/bec/bec/-/commit/0848413d3aa4e87e54abe861790da726a48032ce))

* test: fixed bug in scihub test ([`12f623c`](https://gitlab.psi.ch/bec/bec/-/commit/12f623cda603fa8ab6802907a56e930293d74c23))

* test: fixed tests for new scihub integration ([`3424000`](https://gitlab.psi.ch/bec/bec/-/commit/3424000efe5cf34df122f4e4789b23a97b177d4f))

* test: added scan bundler test ([`ceccbf5`](https://gitlab.psi.ch/bec/bec/-/commit/ceccbf534eac9da61c0973e71eb1086b6cb59611))

* test: fixed sb test ([`0e56f95`](https://gitlab.psi.ch/bec/bec/-/commit/0e56f956af4c214dd0c27df1807cc4d807272ed6))

* test: added sleep to wait for limit updates ([`2eb9a36`](https://gitlab.psi.ch/bec/bec/-/commit/2eb9a36e994c214007e63d94986f4d03e205b910))

* test: added more tests ([`9b9bd59`](https://gitlab.psi.ch/bec/bec/-/commit/9b9bd5973b969bf633579618e8c24eaa4f27de7e))

* test: fixed tests for new wait group structure ([`f0616ea`](https://gitlab.psi.ch/bec/bec/-/commit/f0616ead21780b24edcfe5d85576ee79cd551299))

* test: improved client tests ([`e387660`](https://gitlab.psi.ch/bec/bec/-/commit/e3876609f22cb66a4933b494acf082c5c791590f))

* test: reverted changes in timeout tests ([`6f8358d`](https://gitlab.psi.ch/bec/bec/-/commit/6f8358d7e6cfbbe05947ea5798f9232ab602e590))

* test: improved scan bundler tests ([`7bbf3a1`](https://gitlab.psi.ch/bec/bec/-/commit/7bbf3a1c1ee4f130126f476b636beaf76aa9bec3))

* test: added test for emitter ([`01a9a6f`](https://gitlab.psi.ch/bec/bec/-/commit/01a9a6f0e6f40b17ff06f279e80cb57d5abc4e74))

* test: added cleanup test ([`1826f98`](https://gitlab.psi.ch/bec/bec/-/commit/1826f982ddbf07a88021244582ec1775f154adcf))

* test: added emitter tests ([`3b47a83`](https://gitlab.psi.ch/bec/bec/-/commit/3b47a838b18ea0a3307623bd83c31137b6156fa8))

* test: added tests for bec emitter ([`7984ef8`](https://gitlab.psi.ch/bec/bec/-/commit/7984ef8c3fca532438cd4df4dac885c2f33b5423))

* test: fixed test for refactored scan bundler ([`1466a07`](https://gitlab.psi.ch/bec/bec/-/commit/1466a07fbd75b1a28f2bcbc4e7304cc3fc774961))

* test: cleanup ([`2cf693e`](https://gitlab.psi.ch/bec/bec/-/commit/2cf693e141b5ae1fae91bd6d8406e6d1e012f6e5))

* test: ensured that scan id changes for different test cases ([`4cf853b`](https://gitlab.psi.ch/bec/bec/-/commit/4cf853b5b612a8c89687836a7b787ceee9d54c58))

* test: changed from magicmock to context manager in more tests ([`6d31eb5`](https://gitlab.psi.ch/bec/bec/-/commit/6d31eb57d4218e8903fcbb54b55b70479714f43f))

* test: changed from magicmock to context manager ([`32e1f3b`](https://gitlab.psi.ch/bec/bec/-/commit/32e1f3b5594076aecaebcee4168a867cf97aa4ad))

* test: added test for test_step_scan_update when there is no pointID ([`d4d9e76`](https://gitlab.psi.ch/bec/bec/-/commit/d4d9e76dc886e60fb62e1209c566ed75a8edb7d6))

* test: removed bec_client ([`0ca6d16`](https://gitlab.psi.ch/bec/bec/-/commit/0ca6d1648374e47eaef4d0f340df31881facb297))

* test: added optim_trajectory to fermat spiral test ([`7ad4a11`](https://gitlab.psi.ch/bec/bec/-/commit/7ad4a11c1c08a0fa9b96c53a3005ffdbe4d83f4d))

* test: fixed test ([`cdf75b8`](https://gitlab.psi.ch/bec/bec/-/commit/cdf75b84803774d64bcb68c5f12532e22ee756f2))

* test: improved get_devices_from_scan_data ([`0ff4b08`](https://gitlab.psi.ch/bec/bec/-/commit/0ff4b08acfadd18a877da7ea77807039a7187bc1))

* test: removed test_get_scan_status, worked on my computer but not on pipeline, pipeline should be fixed now ([`00f9531`](https://gitlab.psi.ch/bec/bec/-/commit/00f9531702d61ce75cb3332befc21d0a977d496a))

* test: first test for test_get_device_status ([`8bc0ae2`](https://gitlab.psi.ch/bec/bec/-/commit/8bc0ae27675c6e9ef024276373ca7dadbcb008a0))

* test: improved test_add_wait_group ([`984a5ac`](https://gitlab.psi.ch/bec/bec/-/commit/984a5ac4eb91e0d6b074d6480aac2420c47bf2d8))

* test: improved tes_get_fermat_spiral_pos ([`31eec19`](https://gitlab.psi.ch/bec/bec/-/commit/31eec194dc3387f658241e340e7958731bbbd0ba))

* test: cleanup ([`8256ded`](https://gitlab.psi.ch/bec/bec/-/commit/8256dedb77ca1b996b69f819631b0436933af5bc))

* test: test_redis_consumer_threaded_init ([`a64cc23`](https://gitlab.psi.ch/bec/bec/-/commit/a64cc235b289ba22e07cecebada115748acbcb76))

* test: minor cleanup ([`81f0a48`](https://gitlab.psi.ch/bec/bec/-/commit/81f0a48e59ac2fa03053603088f042ce42802b9e))

* test: moved test from utils to test dir ([`e13948d`](https://gitlab.psi.ch/bec/bec/-/commit/e13948d2b0697a06d420c45a35f5b14b09cd0a59))

* test: first tests for redis_connector ([`4791e10`](https://gitlab.psi.ch/bec/bec/-/commit/4791e104378da559393667d6c2ac91a2ff7b1e8e))

* test: expanded test_trigger_device, rearranged the order of the tests ([`4715628`](https://gitlab.psi.ch/bec/bec/-/commit/4715628c9dd82e89854111ac0bf53615565c2430))

* test: test_update_device_metadata ([`e72d4e0`](https://gitlab.psi.ch/bec/bec/-/commit/e72d4e07511fb174d49c2ad602f88d91d8aadaad))

* test: test_stop, test_start ([`34571d2`](https://gitlab.psi.ch/bec/bec/-/commit/34571d2d12ffa5e955685e068004e7fcc6b5235a))

* test: test_update_status ([`b663290`](https://gitlab.psi.ch/bec/bec/-/commit/b6632900393ec4f4e493ee434ff74df6381979c1))

* test: fixed test_handle_device_instructions ([`3b86d3e`](https://gitlab.psi.ch/bec/bec/-/commit/3b86d3e965198713694e091e8fea1256ef5c433d))

* test: added option to discard pipeline data ([`c44da88`](https://gitlab.psi.ch/bec/bec/-/commit/c44da888014d9a9bc4feb2b9b6156c6841e3b570))

* test: add test_assert_device_is_valid ([`0b35a4c`](https://gitlab.psi.ch/bec/bec/-/commit/0b35a4c66926b1e0aef8f2b3b08e5a851534fd86))

* test: added test_assert_device_is_enabled ([`4d091b8`](https://gitlab.psi.ch/bec/bec/-/commit/4d091b8fdf60004e0816c96d3d3aede3f8df91a9))

* test: improved test_read_device ([`5953765`](https://gitlab.psi.ch/bec/bec/-/commit/595376579b447803f8eed6fced56dc12bde7ec13))

* test: added device server tests ([`488654e`](https://gitlab.psi.ch/bec/bec/-/commit/488654e3a622bda2e58ef0aa4383cdd53207453e))

* test: added num_iterations for path optim ([`d94459c`](https://gitlab.psi.ch/bec/bec/-/commit/d94459c615c6d5c491e533f562827a5d05b68bec))

* test: fixed tests for left align bl_show_all; fixed lsamrot test ([`b9d4750`](https://gitlab.psi.ch/bec/bec/-/commit/b9d47507ca31d9687522af0213050e5c1f345b3f))

* test: added test for bl_info ([`5f06dcc`](https://gitlab.psi.ch/bec/bec/-/commit/5f06dcc7340df41d6141e7e435d2c30bb1206410))

* test: fixed lock acquire ([`6a2a710`](https://gitlab.psi.ch/bec/bec/-/commit/6a2a710273becdce1b39928dd54cefa93dc9fff2))

* test: added tests for tags ([`4f86f62`](https://gitlab.psi.ch/bec/bec/-/commit/4f86f626ad4258fb0f1a006f27036dd769b0a1f6))

* test: fixed tests for acquisition priority ([`2d1d64c`](https://gitlab.psi.ch/bec/bec/-/commit/2d1d64caf8d8b8379ab4ce247bdf8373c9034fb9))

### Unknown

* doc: added doc strings to endpoints ([`d5b3d5b`](https://gitlab.psi.ch/bec/bec/-/commit/d5b3d5b1bce80a260cc3fbedcbbc7bd6245a636d))

* Merge branch &#39;async_callback_fix&#39; of gitlab.psi.ch:bec/bec into async_callback_fix ([`61ecb02`](https://gitlab.psi.ch/bec/bec/-/commit/61ecb02639f213e317f26dee216e8e6216c591d3))

* Merge branch &#39;bec_lib&#39; of gitlab.psi.ch:bec/bec into bec_lib ([`3d87b66`](https://gitlab.psi.ch/bec/bec/-/commit/3d87b661c109d11de1668a17c48d7eff0c65f1ee))

* formatter: fixed formatter ([`dff6938`](https://gitlab.psi.ch/bec/bec/-/commit/dff69389f3225d5f3c4613c57ed8a646b1720962))

* formatter: fixed formatter ([`8f2f593`](https://gitlab.psi.ch/bec/bec/-/commit/8f2f5937f6de580f3d274a90e0c0e87b0a5dc3a5))

* Merge branch &#39;master&#39; into event_callbacks ([`81e9031`](https://gitlab.psi.ch/bec/bec/-/commit/81e9031a7fc5b021fb8ab332f0c7d5103280a746))

* Update .gitlab-ci.yml ([`deec158`](https://gitlab.psi.ch/bec/bec/-/commit/deec158e4e58bc703cd302a68045002c3014771d))

* Update .gitlab-ci.yml ([`51db896`](https://gitlab.psi.ch/bec/bec/-/commit/51db896dac8ce6dbfe69baa0206b429258a27510))

* Update .gitlab-ci.yml ([`923c979`](https://gitlab.psi.ch/bec/bec/-/commit/923c9791b2a1e01d0cb5cda8b5659a30b9f89857))

* Update .gitlab-ci.yml ([`7293481`](https://gitlab.psi.ch/bec/bec/-/commit/729348152e2bacb16d50c9cf15e5ed67b1c093e0))

* Update .gitlab-ci.yml; added debug flag ([`bfa6300`](https://gitlab.psi.ch/bec/bec/-/commit/bfa63008eb2d53780095af19df7dbec49a47a51a))

* Update .gitlab-ci.yml ([`902578b`](https://gitlab.psi.ch/bec/bec/-/commit/902578b2b0e10485374e14984c0209cdacc78e99))

* Merge branch &#39;semver&#39; into &#39;master&#39;

0.0.1

See merge request bec/bec!116 ([`9a27e29`](https://gitlab.psi.ch/bec/bec/-/commit/9a27e29c1c7ea54834a18f83b662c2e3d3568b9f))

* Merge branch &#39;master&#39; into semver ([`2f6c59f`](https://gitlab.psi.ch/bec/bec/-/commit/2f6c59f940d53c0a0fd8f50db1b4b9221859e66b))

* Merge branch &#39;scan_guard_tests&#39; into &#39;master&#39;

test: added scan guard tests

See merge request bec/bec!218 ([`b24df73`](https://gitlab.psi.ch/bec/bec/-/commit/b24df737703857167c89279145ff37984fb63598))

* Merge branch &#39;minor_update&#39; into &#39;master&#39;

fix: fixed alarm_handler verbosity; changed default to Minor

See merge request bec/bec!217 ([`d6c96fc`](https://gitlab.psi.ch/bec/bec/-/commit/d6c96fcbf43067b2ac777490b50cee2c3f79eeb1))

* Merge branch &#39;scilog_reset&#39; into &#39;master&#39;

fix: reset logbook info on init http error

See merge request bec/bec!216 ([`d9ada7b`](https://gitlab.psi.ch/bec/bec/-/commit/d9ada7bb6b01fbe874f8250d35f0e13eb23b4351))

* Merge branch &#39;bec_error_messages&#39; into &#39;master&#39;

Bec error messages

See merge request bec/bec!212 ([`f82d5a6`](https://gitlab.psi.ch/bec/bec/-/commit/f82d5a63e800cefe3f9183e2c4adcea0571c4cdb))

* Merge branch &#39;device_description&#39; into &#39;master&#39;

Device description

See merge request bec/bec!213 ([`27cc987`](https://gitlab.psi.ch/bec/bec/-/commit/27cc9874b95b06a87ca008c200617eb06a033728))

* Merge branch &#39;bec_message_update&#39; into &#39;master&#39;

fix: fixed bec messages for numpy data; fixed message reader

See merge request bec/bec!211 ([`13681e8`](https://gitlab.psi.ch/bec/bec/-/commit/13681e885de29652356929ae9aae2c2c9e4ac80d))

* Merge branch &#39;lamni_update_e20631&#39; into &#39;master&#39;

updates from e20631; closes #68; closes #67

Closes #67 and #68

See merge request bec/bec!203 ([`f9748d7`](https://gitlab.psi.ch/bec/bec/-/commit/f9748d7dbea8d2de5d39d224cbeead70e3575217))

* Merge branch &#39;master&#39; into lamni_update_e20631 ([`2997d1f`](https://gitlab.psi.ch/bec/bec/-/commit/2997d1f3b48631f667b597d6bb2bc66943897fc0))

* updates from e20631 ([`20b1e4b`](https://gitlab.psi.ch/bec/bec/-/commit/20b1e4b85b04ad0ec6e9a1670e700a2baa65c73e))

* Merge branch &#39;devicemanager_update&#39; into &#39;master&#39;

fix: added error handling to catch failed device inits

See merge request bec/bec!208 ([`87bc7cc`](https://gitlab.psi.ch/bec/bec/-/commit/87bc7cc9800b3c5b9cb1f769c37bd7645c5209f3))

* Merge branch &#39;xtreme_plugin&#39; into &#39;master&#39;

feat: added xtreme plugin

See merge request bec/bec!207 ([`c762bda`](https://gitlab.psi.ch/bec/bec/-/commit/c762bdaf12733f1577fafea5db3a499a5e1b591d))

* Merge branch &#39;settling_time&#39; into &#39;master&#39;

test: fixed tests for new default exp time

See merge request bec/bec!206 ([`32876ab`](https://gitlab.psi.ch/bec/bec/-/commit/32876ab7351054bc57c88954d32682e78bf8b3cb))

* Merge branch &#39;settling_time&#39; into &#39;master&#39;

feat: added settling time; fixed burst_at_each_point; removed exp_time as req kwarg

See merge request bec/bec!205 ([`2dccce2`](https://gitlab.psi.ch/bec/bec/-/commit/2dccce2995ab40a5212efbda8ccf0768b3feca2b))

* Merge branch &#39;bec_server_update&#39; into &#39;master&#39;

fix: fixed stdout and stderr redirect for tmux init

See merge request bec/bec!204 ([`7d436f8`](https://gitlab.psi.ch/bec/bec/-/commit/7d436f86c698003013de2584e23c6ce6e1515e4a))

* Merge branch &#39;device_events&#39; into &#39;master&#39;

Device events

See merge request bec/bec!202 ([`e9b217e`](https://gitlab.psi.ch/bec/bec/-/commit/e9b217e8916704384f2019a7f44c2280d2eefbb9))

* Merge branch &#39;master&#39; into device_events ([`b9cef06`](https://gitlab.psi.ch/bec/bec/-/commit/b9cef060ab3ab59f0fe6896ea37c7c405053bc55))

* Merge branch &#39;monitored_devices&#39; into &#39;master&#39;

Monitored devices

See merge request bec/bec!201 ([`603fb89`](https://gitlab.psi.ch/bec/bec/-/commit/603fb89862accdf9acf44e8e9cf25e7fe72579c1))

* Merge branch &#39;xtreme_hyst_scan&#39; into &#39;master&#39;

Xtreme hyst scan

See merge request bec/bec!200 ([`344103e`](https://gitlab.psi.ch/bec/bec/-/commit/344103e4263197cd32e095c946a820908907cc4a))

* Merge branch &#39;rpc_status&#39; into xtreme_hyst_scan ([`506e21c`](https://gitlab.psi.ch/bec/bec/-/commit/506e21cee5eb27d7a1106f7f8b997fc65553a5ef))

* Merge branch &#39;master&#39; into xtreme_hyst_scan ([`428ea0d`](https://gitlab.psi.ch/bec/bec/-/commit/428ea0dfede3bc1c9e4c0d825974289da6fa1fc0))

* Merge branch &#39;progressbar_update&#39; into &#39;master&#39;

feat: added option to hide the table and only show the progressbar

See merge request bec/bec!199 ([`7d9a05e`](https://gitlab.psi.ch/bec/bec/-/commit/7d9a05e72236f6c0c5694546dc8b22b44e7cdbff))

* Merge branch &#39;scan_motor_fix&#39; into &#39;master&#39;

Scan motor fix

See merge request bec/bec!198 ([`b63f480`](https://gitlab.psi.ch/bec/bec/-/commit/b63f480f491176036bdab18cb6217d9233873de5))

* Merge branch &#39;lamni_update&#39; into &#39;master&#39;

Lamni update

See merge request bec/bec!197 ([`ac12522`](https://gitlab.psi.ch/bec/bec/-/commit/ac12522ecb19530605db2d72bfef0ef4f8aecc0f))

* doc: fixed dataset_id_on_hold doc string ([`8dddb32`](https://gitlab.psi.ch/bec/bec/-/commit/8dddb32e890c547132911ed8f34d77bdbc3aa665))

* Delete config_session_start_e20632.yaml ([`e8e0b5f`](https://gitlab.psi.ch/bec/bec/-/commit/e8e0b5f23b8ae3c53584e59d1ff3c5a3a2de8438))

* Merge branch &#39;lamni_commissioning&#39; into &#39;master&#39;

Lamni commissioning

See merge request bec/bec!194 ([`134e83f`](https://gitlab.psi.ch/bec/bec/-/commit/134e83fe839b71ac0ae1aa2ba819efcbf7a16e6d))

* Merge branch &#39;online_backend_changes&#39; into lamni_commissioning ([`202b09f`](https://gitlab.psi.ch/bec/bec/-/commit/202b09f4635b60d5b41bf3bbd4f646cf46c8c004))

* Merge branch &#39;online_backend_changes&#39; of gitlab.psi.ch:bec/bec into online_backend_changes ([`3bffb53`](https://gitlab.psi.ch/bec/bec/-/commit/3bffb53514071ae9b56b6cbec4da32d9f923e54b))

* Merge branch &#39;lamni_updates&#39; into &#39;master&#39;

Lamni updates

See merge request bec/bec!192 ([`58dbefe`](https://gitlab.psi.ch/bec/bec/-/commit/58dbefe7feec08a8d8325bde0a00c7b4f5fdd678))

* Merge branch &#39;lamni_commissioning&#39; into online_backend_changes ([`06109fe`](https://gitlab.psi.ch/bec/bec/-/commit/06109fed17895c2a14b7cd66cf15bb85842d89b4))

* cleanup ([`f12f2ca`](https://gitlab.psi.ch/bec/bec/-/commit/f12f2ca81647b3e7bdf792381b8a5f90def3fcb8))

* Merge branch &#39;online_changes_e20632&#39; into &#39;lamni_commissioning&#39;

# Conflicts:
#   bec_client/bec_client/bin/bec_startup.py
#   bec_client/bec_client/callbacks/move_device.py
#   bec_client/bec_client/plugins/LamNI/x_ray_eye_align.py
#   device_server/launch.py
#   file_writer/file_writer_plugins/cSAXS.py
#   scibec/init_scibec/configs/lamni_config.py
#   scihub/scihub/scibec/scibec.py
#   scihub/scihub/scibec/scibec_connector.py
#   scihub/scihub/scibec/scibec_metadata_handler.py
#   scihub/scihub/scilog/scilog.py ([`09dd93f`](https://gitlab.psi.ch/bec/bec/-/commit/09dd93ffb520725d87455be1a03ca012d0667629))

* changes during the beamtime for e20632 ([`518ac84`](https://gitlab.psi.ch/bec/bec/-/commit/518ac8400fc7d765bb9ce9736c92c35329e18c07))

* ci update ([`fd41910`](https://gitlab.psi.ch/bec/bec/-/commit/fd41910f9d0614bd56f33ac9b219c4b360dd9b7d))

* online changes e21125 ([`99fe3ef`](https://gitlab.psi.ch/bec/bec/-/commit/99fe3efbb602400285b40356c039b82f3bb07aaf))

* online changes e21125 ([`fce507c`](https://gitlab.psi.ch/bec/bec/-/commit/fce507c0f5577e1ce118d2ac918ea16729063ae4))

* online changes e21125 ([`35abf28`](https://gitlab.psi.ch/bec/bec/-/commit/35abf28193a55eb5a66b77a647de85b98fd62372))

* ci update ([`543b83c`](https://gitlab.psi.ch/bec/bec/-/commit/543b83cacc6f73b7175a51bbdf0386a347565351))

* Merge branch &#39;scibec_model_update&#39; of gitlab.psi.ch:bec/bec into scibec_model_update ([`376b1d5`](https://gitlab.psi.ch/bec/bec/-/commit/376b1d5c5291d76e22753aafabc53aa0ede05abd))

* ci update ([`83a2dd5`](https://gitlab.psi.ch/bec/bec/-/commit/83a2dd5dc47d9ff38b0e7863b01adbef568ba332))

* ci update ([`fa8e17a`](https://gitlab.psi.ch/bec/bec/-/commit/fa8e17ab7b34e766b7223d28c6f5a58e54e2f6f4))

* Merge branch &#39;scibec_integration&#39; into scibec_model_update ([`fe40104`](https://gitlab.psi.ch/bec/bec/-/commit/fe401045b914071fc28e77222491636932dbaf42))

* Merge branch &#39;master&#39; into lamni_updates ([`ada10be`](https://gitlab.psi.ch/bec/bec/-/commit/ada10be811342ec5b265f7212486b078500433a3))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`4e7f9d5`](https://gitlab.psi.ch/bec/bec/-/commit/4e7f9d5e00fcb9eb0e564f3b373017f8d7f9bbc3))

* Merge branch &#39;scilog_support&#39; into &#39;master&#39;

Scilog support

See merge request bec/bec!191 ([`106c36a`](https://gitlab.psi.ch/bec/bec/-/commit/106c36ab7fc6c3be06d348800de402f462e50757))

* Merge branch &#39;scan_report_instructions&#39; into &#39;master&#39;

Scan report instructions

See merge request bec/bec!190 ([`64e3868`](https://gitlab.psi.ch/bec/bec/-/commit/64e3868afdada3388d08e71ffdd0f4a2b5e8dd3e))

* Merge branch &#39;otf_scan&#39; into &#39;master&#39;

feat: added otf scan

See merge request bec/bec!189 ([`bcfbc38`](https://gitlab.psi.ch/bec/bec/-/commit/bcfbc382da6b6dd5ac54dbcb6a1e84a8ffbd232d))

* Merge branch &#39;flyer_event&#39; into &#39;master&#39;

feat: added complete and support for new kickoff signature

See merge request bec/bec!188 ([`d1946a3`](https://gitlab.psi.ch/bec/bec/-/commit/d1946a389864bda3aaa71153fd28d992b6065c2e))

* Merge branch &#39;flyer_event&#39; into &#39;master&#39;

feat: added flyer event and callback

See merge request bec/bec!187 ([`8ec709e`](https://gitlab.psi.ch/bec/bec/-/commit/8ec709ee08f4124849b1d276a3dc6879c409f470))

* Merge branch &#39;numpy_encoding&#39; into &#39;master&#39;

feat: added becmessage version 1.1; added option to select compression

See merge request bec/bec!186 ([`1460bd4`](https://gitlab.psi.ch/bec/bec/-/commit/1460bd4cceaf7a760974a8074585aa416077d331))

* Merge branch &#39;metrics&#39; into &#39;master&#39;

Metrics

See merge request bec/bec!174 ([`bbceda6`](https://gitlab.psi.ch/bec/bec/-/commit/bbceda613e31230085e65e76c9c96f17cabf2c5e))

* ci update ([`fcb1882`](https://gitlab.psi.ch/bec/bec/-/commit/fcb188222d87c5e2257086d542a17c3d21e85279))

* Merge branch &#39;master&#39; into metrics ([`96ee6d4`](https://gitlab.psi.ch/bec/bec/-/commit/96ee6d4fe80bb7e5b98569c238476566b1ff4870))

* Merge branch &#39;device_info&#39; into &#39;master&#39;

feat: improved device info

See merge request bec/bec!184 ([`07b9e33`](https://gitlab.psi.ch/bec/bec/-/commit/07b9e335313a47221c36f04f5ac5184b4c130299))

* formatter: fixed formatting for setup.py ([`25b34e0`](https://gitlab.psi.ch/bec/bec/-/commit/25b34e00b0cffe96da390586335f17cb6db17194))

* Update setup.py ([`baa4790`](https://gitlab.psi.ch/bec/bec/-/commit/baa47902a37e0711487623ae2ada9a7660cd3c0a))

* Update setup.py ([`ac984d1`](https://gitlab.psi.ch/bec/bec/-/commit/ac984d14c7e94ee506b13a41b632137cd6bf800a))

* Merge branch &#39;scan_status&#39; into &#39;master&#39;

Scan status

See merge request bec/bec!182 ([`2e3521b`](https://gitlab.psi.ch/bec/bec/-/commit/2e3521bb9c4c75239357ebe3ae1b8add1a9442d0))

* Merge branch &#39;scan_callback&#39; into &#39;master&#39;

fix: skip None callbacks

See merge request bec/bec!181 ([`825d3ee`](https://gitlab.psi.ch/bec/bec/-/commit/825d3eee32e16d90103be82a90fd549e6eedbb0b))

* Merge branch &#39;scan_callback&#39; into &#39;master&#39;

feat: added scan callbacks

See merge request bec/bec!180 ([`608de2e`](https://gitlab.psi.ch/bec/bec/-/commit/608de2e656317828b893a02f5e54670ca781763f))

* Merge branch &#39;queue_abort&#39; into &#39;master&#39;

fix: only pause if queue is not empty

See merge request bec/bec!179 ([`290fa37`](https://gitlab.psi.ch/bec/bec/-/commit/290fa37bf15a5851dd27a41c4a42afab22e151d6))

* Update start_tmux_session.sh ([`577eea5`](https://gitlab.psi.ch/bec/bec/-/commit/577eea552e7eb85acaeb47241a8d90dd8bddcac2))

* Update .gitignore ([`b77156d`](https://gitlab.psi.ch/bec/bec/-/commit/b77156d8768fd0a1e5ea34e777cc3ee15be07615))

* Merge branch &#39;redis_config&#39; into &#39;master&#39;

Redis config

See merge request bec/bec!178 ([`544cea7`](https://gitlab.psi.ch/bec/bec/-/commit/544cea7b5b8b54d0927d3497d2c6dd759c4ec4ac))

* doc: updated doc ([`69ca275`](https://gitlab.psi.ch/bec/bec/-/commit/69ca275e2693b0aa2b0a7775663eff2dbf756116))

* doc: updated documentation ([`68885d5`](https://gitlab.psi.ch/bec/bec/-/commit/68885d5cab5b7e69ca3673dd91c4fbe5d3504bdb))

* added missing file ([`f6545c8`](https://gitlab.psi.ch/bec/bec/-/commit/f6545c818cca5120e5b9fefb3e914d3defd6f033))

* intermediate commit ([`2685225`](https://gitlab.psi.ch/bec/bec/-/commit/26852251c51dd8071e2e9069c2ef386cc045ac0b))

* Merge branch &#39;master&#39; into redis_config ([`5e661a6`](https://gitlab.psi.ch/bec/bec/-/commit/5e661a68b17893dfe6e26c4953c5495f40ff6cca))

* Merge branch &#39;ci_update&#39; into &#39;master&#39;

Ci update

See merge request bec/bec!177 ([`2a77ce6`](https://gitlab.psi.ch/bec/bec/-/commit/2a77ce6f2a87a57d480e3b4a9c58b992af6ab2ca))

* Ci update ([`02ffd3e`](https://gitlab.psi.ch/bec/bec/-/commit/02ffd3eab6b9ea2f9264b290603db4046280e03a))

* Merge branch &#39;ci_update&#39; into &#39;master&#39;

Ci update

See merge request bec/bec!176 ([`4bd41b6`](https://gitlab.psi.ch/bec/bec/-/commit/4bd41b6b6a76f9c0efb7a2885bb23d2747376316))

* Merge branch &#39;monitor_scan&#39; into &#39;master&#39;

fix: changes related to monitor scan

See merge request bec/bec!175 ([`2014b90`](https://gitlab.psi.ch/bec/bec/-/commit/2014b90be70c9ce7858c5ea6e5b9bf5faab44873))

* Merge branch &#39;monitor_scan&#39; into &#39;master&#39;

Monitor scan

See merge request bec/bec!173 ([`35b9944`](https://gitlab.psi.ch/bec/bec/-/commit/35b9944bc8df5560ff8efcf0532df16eafe153d7))

* Merge branch &#39;time_scan&#39; into &#39;master&#39;

feat: added time scan

See merge request bec/bec!172 ([`02846a0`](https://gitlab.psi.ch/bec/bec/-/commit/02846a05d927b68836dd836931482346dcfac789))

* Update Dockerfile ([`cad4818`](https://gitlab.psi.ch/bec/bec/-/commit/cad481888bbebe2d1f49202c4afbc47a5cf0e6b9))

* Update Dockerfile ([`adc9b42`](https://gitlab.psi.ch/bec/bec/-/commit/adc9b42b16397ffc3bbffa2a72fa466ad6c288d0))

* Update Dockerfile ([`4477c9c`](https://gitlab.psi.ch/bec/bec/-/commit/4477c9ce0572a654456fcd242c7dcc01e9fd7514))

* Update Dockerfile ([`dbb852f`](https://gitlab.psi.ch/bec/bec/-/commit/dbb852f186604681f4d175c4b225f14a5543a064))

* Update Dockerfile ([`1ec7eab`](https://gitlab.psi.ch/bec/bec/-/commit/1ec7eabf58bdff089f61c6f7f6888cb7ae007961))

* Update .gitlab-ci.yml ([`0157636`](https://gitlab.psi.ch/bec/bec/-/commit/01576368a9c052a9f95c38bb2b30de0f7a36e375))

* Update .gitlab-ci.yml ([`97c0ba6`](https://gitlab.psi.ch/bec/bec/-/commit/97c0ba6bdbdd3ddaf94225875569b8ae52bceacd))

* Merge branch &#39;monitor_scan&#39; into metrics ([`aec19ff`](https://gitlab.psi.ch/bec/bec/-/commit/aec19ff3d1bcb3ef65624c36f0a5da7367c9b2ef))

* Update .gitlab-ci.yml ([`115f063`](https://gitlab.psi.ch/bec/bec/-/commit/115f0635e372999dc60923803793d75cd25cc7b5))

* Update .gitlab-ci.yml ([`93a746e`](https://gitlab.psi.ch/bec/bec/-/commit/93a746ebd5bacdcad3a1a131fb07f13d687bc661))

* Merge branch &#39;list_scan&#39; into &#39;master&#39;

feat: added list scan

See merge request bec/bec!171 ([`493f961`](https://gitlab.psi.ch/bec/bec/-/commit/493f961cee411ee07601980fc5cbcb4d08a4840c))

* Merge branch &#39;scan_server_scan_worker_tests&#39; into &#39;master&#39;

Scan server scan worker tests

See merge request bec/bec!170 ([`ff7421f`](https://gitlab.psi.ch/bec/bec/-/commit/ff7421f5a8d5aac7c03ff8983f1bc788d0fecd61))

* tests: test_shutdown ([`e486568`](https://gitlab.psi.ch/bec/bec/-/commit/e48656813cc7c595dc484f327868fa6f49965adc))

* tests: test_cleanup ([`9a4f46c`](https://gitlab.psi.ch/bec/bec/-/commit/9a4f46cf2dd7f6448e76fb5d270534a24368977a))

* tests: test_reset ([`e400a91`](https://gitlab.psi.ch/bec/bec/-/commit/e400a9125a748ed3122dccec960996e95e933378))

* tests: test_process_instructions ([`274b6a6`](https://gitlab.psi.ch/bec/bec/-/commit/274b6a6528fe45a2d461bd00a07dacd0c558a138))

* tests: added test_unstage_device ([`ab76bb4`](https://gitlab.psi.ch/bec/bec/-/commit/ab76bb4644d020297bb13c4c73e8d6ee7b7250b9))

* tests: added test_stage_device ([`4514b25`](https://gitlab.psi.ch/bec/bec/-/commit/4514b25fdf43e07e207b9bbb265acf8ebef11f3a))

* tests: added test_initialize_scan_info ([`13ae292`](https://gitlab.psi.ch/bec/bec/-/commit/13ae2929a141e73455c3123256f06b1e65b91853))

* tests: added test_open_scan ([`246d6cf`](https://gitlab.psi.ch/bec/bec/-/commit/246d6cfa550df11ae9d3aaae2104173aa9099f0d))

* added current_instruction_queue_item to __init__ ([`397b0ab`](https://gitlab.psi.ch/bec/bec/-/commit/397b0ab1536e4b9c6d80a5c5198d4854078e2c3e))

* renamed _initialize_scan_info and added type hints ([`da21900`](https://gitlab.psi.ch/bec/bec/-/commit/da21900664e28ee63179d403394c7baafe113dbe))

* updated update_current_scan_info ([`750dd5c`](https://gitlab.psi.ch/bec/bec/-/commit/750dd5cc7a8877dc247d93269be388263f0a6375))

* added update_current_scan_info ([`262982b`](https://gitlab.psi.ch/bec/bec/-/commit/262982b275ba07b61dacfe96870e8fff0956a959))

* Merge branch &#39;client_test_update&#39; into &#39;master&#39;

test: improved client tests

See merge request bec/bec!169 ([`1876268`](https://gitlab.psi.ch/bec/bec/-/commit/18762688ec3806599322c845b4418885282b763c))

* Merge branch &#39;scan_server_scan_worker_tests&#39; into &#39;master&#39;

Scan server scan worker tests

See merge request bec/bec!168 ([`7dedb1b`](https://gitlab.psi.ch/bec/bec/-/commit/7dedb1bc1eb06b1ccd29c5c7806af94483529e22))

* Merge branch &#39;scan_server_scan_worker_tests&#39; of gitlab.psi.ch:bec/bec into scan_server_scan_worker_tests ([`8cc3bf9`](https://gitlab.psi.ch/bec/bec/-/commit/8cc3bf98b662e5739a9622017da7b5f4f25fb777))

* Merge branch &#39;master&#39; into &#39;scan_server_scan_worker_tests&#39;

Master

See merge request bec/bec!167 ([`f5fa5a4`](https://gitlab.psi.ch/bec/bec/-/commit/f5fa5a44e126948eb2d013b1e861b8273ff72ccb))

* Merge branch &#39;decouple_test_handle_device_instr&#39; into &#39;master&#39;

Decouple test handle device instr

See merge request bec/bec!165 ([`73d3d34`](https://gitlab.psi.ch/bec/bec/-/commit/73d3d349f7855e53649b233a6296a493d9643809))

* Merge branch &#39;master&#39; into &#39;decouple_test_handle_device_instr&#39;

Master

See merge request bec/bec!166 ([`5d3d944`](https://gitlab.psi.ch/bec/bec/-/commit/5d3d94494612470331af83509c2fa366b98e5e85))

* tests: added exception tests to handle_device_instructions ([`8effbb8`](https://gitlab.psi.ch/bec/bec/-/commit/8effbb8a712cf04dface43105467ea77e2b5bd58))

* tests:decoupled handle_instructions and changed from mock.magicmock to context managers ([`68fcbcf`](https://gitlab.psi.ch/bec/bec/-/commit/68fcbcfe439fbcda84141b20df3676148f3f3a1d))

* tests: fixed formatter and started with test_open_scan ([`f1d65ac`](https://gitlab.psi.ch/bec/bec/-/commit/f1d65acf6b132fefaf20d58369263e383c102fa2))

* tests: test_kickoff_devices ([`5aa5b71`](https://gitlab.psi.ch/bec/bec/-/commit/5aa5b7182a0995262ea13d4b061bfe1877f8b369))

* tests: test_read_devices ([`d8820c1`](https://gitlab.psi.ch/bec/bec/-/commit/d8820c12da30a5b8e89ec9c900cb187d0abdac7d))

* tests: changed from magicmock to context managers ([`35a7c3d`](https://gitlab.psi.ch/bec/bec/-/commit/35a7c3d1fabf38b23ee2ea00689b2b2ad5ad6834))

* tests: changed test_wait_for_device_server ([`7655b2f`](https://gitlab.psi.ch/bec/bec/-/commit/7655b2fb0cfefdb0d9da661381673cea9d6c29d8))

* tests: test_wait_for_stage ([`62240ad`](https://gitlab.psi.ch/bec/bec/-/commit/62240ad6ed02c249f6e51d93d7b1d21a31e583c2))

* tests: updated test_get_devices_from_instruction ([`c6029e8`](https://gitlab.psi.ch/bec/bec/-/commit/c6029e89e4d4fa1945bd8aedf8f02e536a167f77))

* Update .gitlab-ci.yml ([`888f1a5`](https://gitlab.psi.ch/bec/bec/-/commit/888f1a5432227c9e1f9f1cab1fa89fef43de2063))

* Update .gitlab-ci.yml ([`6c0eb94`](https://gitlab.psi.ch/bec/bec/-/commit/6c0eb940189bd4770972694a35ad358e9a92aacd))

* Update docker-compose.yaml ([`a391deb`](https://gitlab.psi.ch/bec/bec/-/commit/a391deb32e625e4f2369b662007135b7699eca1a))

* Update docker-compose.yaml ([`f20a58f`](https://gitlab.psi.ch/bec/bec/-/commit/f20a58f735a68f1f7ad9e49dc8a3953eeb0c6079))

* Merge branch &#39;script_linter&#39; into &#39;master&#39;

feat: added linter to check the imported user scripts; closes #61

Closes #61

See merge request bec/bec!164 ([`8e10bd3`](https://gitlab.psi.ch/bec/bec/-/commit/8e10bd308df73d04c698c5c937ccc5ce402fc277))

* Merge branch &#39;influxdb&#39; into &#39;master&#39;

refactor: removed influxdb forwarder

See merge request bec/bec!163 ([`9166557`](https://gitlab.psi.ch/bec/bec/-/commit/91665577501bd181b080ffc2ba3b72e40679fb2e))

* Merge branch &#39;unified_device_manager&#39; into &#39;master&#39;

refactor: removed DeviceManagerDeviceServer; closes #31

Closes #31

See merge request bec/bec!162 ([`58f6682`](https://gitlab.psi.ch/bec/bec/-/commit/58f6682c77824609f313ecf480acc132525359d4))

* Merge branch &#39;scan_queue_tests&#39; into &#39;master&#39;

Scan queue tests

See merge request bec/bec!161 ([`fe86a20`](https://gitlab.psi.ch/bec/bec/-/commit/fe86a20ab4ed6e7d9b91ea10cf135c96bf3feb97))

* Merge branch &#39;redesign_scan_bundler&#39; into &#39;master&#39;

started with decoupling of bluesky and bec emitters

See merge request bec/bec!160 ([`d73a16a`](https://gitlab.psi.ch/bec/bec/-/commit/d73a16aa611e1d38e95173efa4bdf0d6a6ecde12))

* Merge branch &#39;redesign_scan_bundler&#39; of gitlab.psi.ch:bec/bec into redesign_scan_bundler ([`59590ca`](https://gitlab.psi.ch/bec/bec/-/commit/59590ca08af813e1e57af4008b03c2ece62b69b4))

* Update .gitlab-ci.yml ([`78a0e69`](https://gitlab.psi.ch/bec/bec/-/commit/78a0e6982a7e4adb3d0b041b10eb75adc4615a68))

* Update .gitlab-ci.yml ([`1198ca7`](https://gitlab.psi.ch/bec/bec/-/commit/1198ca73deb5b6c8877e7009d87c3667187fce64))

* Update .gitlab-ci.yml ([`3c251b3`](https://gitlab.psi.ch/bec/bec/-/commit/3c251b396a59caaee19f17733fe13660aa242b17))

* Update .gitlab-ci.yml ([`10db09f`](https://gitlab.psi.ch/bec/bec/-/commit/10db09fc67aa1fd9f02eca0a5ef65218edcd2307))

* Update .gitlab-ci.yml ([`b2a4cc3`](https://gitlab.psi.ch/bec/bec/-/commit/b2a4cc327a61836ca2300163eaf82224333f0828))

* Update .gitlab-ci.yml ([`fe23473`](https://gitlab.psi.ch/bec/bec/-/commit/fe23473b3fb6d21469c8baaa58245ed33b586467))

* Update .gitlab-ci.yml ([`0fd394d`](https://gitlab.psi.ch/bec/bec/-/commit/0fd394dad731fcda5fd3afb630e6dabcc9b58f5c))

* Update .gitlab-ci.yml ([`b9a23f1`](https://gitlab.psi.ch/bec/bec/-/commit/b9a23f1173c96bb958afed35dfc8fc90efe19502))

* Update .gitlab-ci.yml ([`7f71d64`](https://gitlab.psi.ch/bec/bec/-/commit/7f71d64a9f807e70ece2b3fcd4402d8f9da022a7))

* Update .gitlab-ci.yml ([`f72c807`](https://gitlab.psi.ch/bec/bec/-/commit/f72c807aea5d881dd7b2167a59080362ab9433ff))

* Update .gitlab-ci.yml ([`52847fc`](https://gitlab.psi.ch/bec/bec/-/commit/52847fce3be8170f0b542d5bf860ee4d312721f4))

* Merge branch &#39;master&#39; into redesign_scan_bundler ([`c8d4ec7`](https://gitlab.psi.ch/bec/bec/-/commit/c8d4ec7eea27ff601aa521bbcc32bacbee5e1cb2))

* Merge branch &#39;test_scan_bundler&#39; into &#39;master&#39;

Test scan bundler

See merge request bec/bec!158 ([`25440a1`](https://gitlab.psi.ch/bec/bec/-/commit/25440a12fff2218483cd6da7c6a2f35cd5b44c5e))

* tests: added test_step_scan_update ([`cc20b13`](https://gitlab.psi.ch/bec/bec/-/commit/cc20b139da7101ae85352bd9b0a1d413a5777c0d))

* tests: added test_initialize_scan_container ([`edfd7a9`](https://gitlab.psi.ch/bec/bec/-/commit/edfd7a90893fa006bf27a5709de643f7b0ca5165))

* tests: added test_handle_scan_status_message ([`0af1521`](https://gitlab.psi.ch/bec/bec/-/commit/0af1521eacbbed286bffd5fc0587f6150c830211))

* tests: added test_scan_status_callback ([`1ea3785`](https://gitlab.psi.ch/bec/bec/-/commit/1ea37855471cc46b82cbc96f83a31f427c6ed52a))

* tests: added 3 tests ([`d44a0cf`](https://gitlab.psi.ch/bec/bec/-/commit/d44a0cf51ae6544d8fb58a6569310dc21c06cb6e))

* Delete coverage.xml ([`b895b39`](https://gitlab.psi.ch/bec/bec/-/commit/b895b39b5de8fed4ccae5f00e8f10a7b1519ac51))

* Delete coverage.xml ([`95d1efa`](https://gitlab.psi.ch/bec/bec/-/commit/95d1efa1ebc47a098eb271e797b6ada97254fede))

* removed blinkers ([`aaa6b03`](https://gitlab.psi.ch/bec/bec/-/commit/aaa6b036c21b1dec69871000368aa819dda0cd0d))

* Merge branch &#39;redesign_scan_bundler&#39; of gitlab.psi.ch:bec/bec into redesign_scan_bundler ([`ff438a0`](https://gitlab.psi.ch/bec/bec/-/commit/ff438a02819aa49fe699b42b30b5386e046981c9))

* Delete .coverage ([`ba7025f`](https://gitlab.psi.ch/bec/bec/-/commit/ba7025f7f7d2d3e900fc0aa6b91e13e359844ed6))

* removed unwanted files ([`dba7bb0`](https://gitlab.psi.ch/bec/bec/-/commit/dba7bb0a62d7f1c4483a2eb3a2e9af3a0de6fa94))

* Merge branch &#39;redesign_scan_bundler&#39; of gitlab.psi.ch:bec/bec into redesign_scan_bundler ([`f960a80`](https://gitlab.psi.ch/bec/bec/-/commit/f960a802cdf6ef336f6b8af04b95e1c9b404201d))

* Update setup.py ([`58c42dc`](https://gitlab.psi.ch/bec/bec/-/commit/58c42dc7832b807e1ced3406b77c1c90df5d5ea1))

* added blinker ([`232b7bd`](https://gitlab.psi.ch/bec/bec/-/commit/232b7bdf8a11650e29613c864dc8d7393f4e2e10))

* emitting from emitters ([`1281d78`](https://gitlab.psi.ch/bec/bec/-/commit/1281d788d53d4b6350c4bfbbba0344743151616b))

* refactoring with blinkers, not done yet ([`4c0018f`](https://gitlab.psi.ch/bec/bec/-/commit/4c0018f2d6e8353e8c1f5efa5acbd88322975943))

* Merge branch &#39;cherry-pick-7ac26a34&#39; into &#39;redesign_scan_bundler&#39;

started with decoupling of bluesky and bec emitters

See merge request bec/bec!159 ([`4e37e01`](https://gitlab.psi.ch/bec/bec/-/commit/4e37e0126ac67759cee8527dbaf5944242c39203))

* started with decoupling of bluesky and bec emitters


(cherry picked from commit 7ac26a34dd8ec4beaa6c6bb35ea50814ad893f6c) ([`7836dff`](https://gitlab.psi.ch/bec/bec/-/commit/7836dff5d0cf8583e6142d45e7ac78fb40679697))

* Merge branch &#39;round_scan_report_fix&#39; into &#39;master&#39;

Round scan report fix; closes #64

Closes #64

See merge request bec/bec!157 ([`1313073`](https://gitlab.psi.ch/bec/bec/-/commit/1313073a15652cd7fbf4f0bb492534c3022d35f5))

* Update conf.py ([`059600e`](https://gitlab.psi.ch/bec/bec/-/commit/059600e8580081fda1e7fc1eede2e1466b37f4f8))

* Merge branch &#39;doc_update&#39; into &#39;master&#39;

Doc update

See merge request bec/bec!156 ([`3b3dddb`](https://gitlab.psi.ch/bec/bec/-/commit/3b3dddbbe956bc4cff081b9cd9436bde49061f84))

* Merge branch &#39;doc_update&#39; into &#39;master&#39;

docs: update drawings

See merge request bec/bec!155 ([`e93efdd`](https://gitlab.psi.ch/bec/bec/-/commit/e93efdd6494cd26004a54ac9522e3ba11f58b3c8))

* Merge branch &#39;cli&#39; into &#39;master&#39;

feat: added bec cli command; added bec_startup script

See merge request bec/bec!154 ([`c39e769`](https://gitlab.psi.ch/bec/bec/-/commit/c39e769345b9d11abc3b631e776bc2b113e8fd1a))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`684dd1c`](https://gitlab.psi.ch/bec/bec/-/commit/684dd1ce6c6787f7bb82c2526747668a4eb9b6e2))

* Merge branch &#39;ci_anchor&#39; into &#39;master&#39;

Ci anchor

See merge request bec/bec!153 ([`451ffce`](https://gitlab.psi.ch/bec/bec/-/commit/451ffce9e1878b276d3537b1f828f29197469171))

* Update .gitlab-ci.yml ([`84aa748`](https://gitlab.psi.ch/bec/bec/-/commit/84aa748ff573566633d7298599427bdaff4572c9))

* Update .gitlab-ci.yml ([`29533e7`](https://gitlab.psi.ch/bec/bec/-/commit/29533e70674f34accb755863191fcfd9d70b3a4c))

* Merge branch &#39;scan_server_scan_worker_tests&#39; into &#39;master&#39;

More tests for scan_worker

See merge request bec/bec!152 ([`39b32de`](https://gitlab.psi.ch/bec/bec/-/commit/39b32de4a4104cdbfb5e7997f9171ecee3d57596))

* test:test_check_for_interruption ([`027e2c7`](https://gitlab.psi.ch/bec/bec/-/commit/027e2c7f6545e2e02bfbc76688381285916d5cd4))

* test:test_send_rpc ([`9236dcb`](https://gitlab.psi.ch/bec/bec/-/commit/9236dcb06ae59545490672d15e824cf8110905a6))

* test:test_trigger_devices ([`257336a`](https://gitlab.psi.ch/bec/bec/-/commit/257336a6e710b95a92c88d0fbacd91502346c1af))

* test:test_set_devices ([`d13b031`](https://gitlab.psi.ch/bec/bec/-/commit/d13b031a5eb8d4a677db23a7f90d3544f71b90ed))

* test:test_wait_for_device_server ([`b0bec67`](https://gitlab.psi.ch/bec/bec/-/commit/b0bec67db729dbeccfcac0abd5d6a3238c785671))

* test:test_wait_for_trigger ([`18a5cb2`](https://gitlab.psi.ch/bec/bec/-/commit/18a5cb2a36616a27c545dc4b5d8376283dc9c6c5))

* test:test_wait_for_read ([`6eb3e30`](https://gitlab.psi.ch/bec/bec/-/commit/6eb3e302ba48e5a83806c6fbc9896f34aaa0dc97))

* test:test_wait_for_devices ([`6227ba5`](https://gitlab.psi.ch/bec/bec/-/commit/6227ba52dcf25674d36a927abb0ec1486ac656a3))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`90ef9ec`](https://gitlab.psi.ch/bec/bec/-/commit/90ef9ec8048f851ff0f05c13fe4995e722e15beb))

* Merge branch &#39;scan_server_scans_tests&#39; into &#39;master&#39;

Improved tests using RequestBase

See merge request bec/bec!151 ([`5d57d5f`](https://gitlab.psi.ch/bec/bec/-/commit/5d57d5ff2ee4168106be29e58c6254ea37f85bca))

* Improved tests using RequestBase ([`5bdae0c`](https://gitlab.psi.ch/bec/bec/-/commit/5bdae0c0ac34d3f645e1690ab61831b126ac87cf))

* Merge branch &#39;scan_server_scans_tests&#39; into &#39;master&#39;

Scan server scans tests

See merge request bec/bec!149 ([`6596b34`](https://gitlab.psi.ch/bec/bec/-/commit/6596b3485667d3a23d917a3a942a381b259d7a53))

* test:test_line_scan_calculate_positions ([`04a05d6`](https://gitlab.psi.ch/bec/bec/-/commit/04a05d654cf8647de678573db3369cc042b888f0))

* test:test_round_scan_fly_sim_scan_core ([`92eeabb`](https://gitlab.psi.ch/bec/bec/-/commit/92eeabb2cc1faa4c50dd50eb57271229c0e166fe))

* test:test_round_scan_fly_sim_calculate_positions ([`78cca70`](https://gitlab.psi.ch/bec/bec/-/commit/78cca70f4c7a244181baee31dc6cb8088d96976e))

* test:test_round_scan_fly_sim_prepare_positions ([`a9e5d8e`](https://gitlab.psi.ch/bec/bec/-/commit/a9e5d8e2ae72601100eb228cc87cd3d3385cbd0d))

* test:test_round_scan_fly_sim_get_scan_motors ([`6e891b3`](https://gitlab.psi.ch/bec/bec/-/commit/6e891b30574c5a52668f4452a032ba1686c6e7de))

* test:test_scan_base ([`86a5ab2`](https://gitlab.psi.ch/bec/bec/-/commit/86a5ab29bed637caace209e561f4d23bc58900ed))

* test:test_scan_base_init, testing if scan_name ==&#34;&#34; ([`ef2c1d9`](https://gitlab.psi.ch/bec/bec/-/commit/ef2c1d9dad1dc66f5c916cb645186c81a4108c2a))

* test:test_request_get_scan_motors ([`3a3bf91`](https://gitlab.psi.ch/bec/bec/-/commit/3a3bf917015933ccf24c882e3f2404ef9b5bf75f))

* test:test_request_base_check_limits ([`9bbc0c7`](https://gitlab.psi.ch/bec/bec/-/commit/9bbc0c7e841fe93a6e0f326ab6d59b673c99f186))

* test:test_scan_report_devices ([`55c45e5`](https://gitlab.psi.ch/bec/bec/-/commit/55c45e50cff33c6bbca9a38d912b02f96713d0f3))

* test:test_get_fermat_spiral_pos ([`09d3eb0`](https://gitlab.psi.ch/bec/bec/-/commit/09d3eb0174f29bfb468695f76302e2d5da497b2c))

* Merge branch &#39;redis_connector_tests&#39; into &#39;master&#39;

Redis connector tests

See merge request bec/bec!148 ([`74ba5ba`](https://gitlab.psi.ch/bec/bec/-/commit/74ba5ba6f1ad542d2795c9bd55f4ee75fbfac531))

* import RedisConsumerMixin ([`62b1101`](https://gitlab.psi.ch/bec/bec/-/commit/62b1101f33b23414cb971dca478bd33fb5fffdd1))

* Merge branch &#39;redis_connector_tests&#39; of gitlab.psi.ch:bec/bec into redis_connector_tests ([`22ce00c`](https://gitlab.psi.ch/bec/bec/-/commit/22ce00cd7522b17cde5d1627c385f8a13dc766a6))

* test:test_mixin_init_redis_cls ([`add58a9`](https://gitlab.psi.ch/bec/bec/-/commit/add58a983cc12e5a98445e5d2bd5ab16771ee65f))

* test:test_mixin_init_topics_and_pattern ([`4ba2b01`](https://gitlab.psi.ch/bec/bec/-/commit/4ba2b0184951a8061e22e1180a852551e98a276b))

* test:test_redis_consumer_poll_messages ([`25b7dc5`](https://gitlab.psi.ch/bec/bec/-/commit/25b7dc51d6c3b80479ba420bcc7902538d0ecb08))

* test:test_redis_consumer_init and shutdown and added topics to consumer ([`ce97680`](https://gitlab.psi.ch/bec/bec/-/commit/ce97680213a50bb6829475d42028b6f85c9b1868))

* Merge branch &#39;redis_connector_tests&#39; of gitlab.psi.ch:bec/bec into redis_connector_tests ([`db2f45e`](https://gitlab.psi.ch/bec/bec/-/commit/db2f45e886ce493482011c151478e0d191fec39c))

* test:test_redis_consumer_init and shutdown ([`ce4a4ea`](https://gitlab.psi.ch/bec/bec/-/commit/ce4a4ea02219e9b9a75a0d064e5a8bdf103c2091))

* test:test_redis_consumer_initialize_connector ([`5f8d2b7`](https://gitlab.psi.ch/bec/bec/-/commit/5f8d2b7e4236354c4dcea166e9cd230c37969872))

* test:test_redis_connector_consumer ([`43a59d7`](https://gitlab.psi.ch/bec/bec/-/commit/43a59d75aa43b5f773b8e1ce91b1f328192b9d99))

* test:test_redis_connector_producer ([`9453ba5`](https://gitlab.psi.ch/bec/bec/-/commit/9453ba5d615eaeacfda45681eeb214567cee4c32))

* test:test_redis_connector_raise_alarm ([`6599a72`](https://gitlab.psi.ch/bec/bec/-/commit/6599a722df6f6d815d0721c5270fbcdf6b1e8304))

* test:test_redis_connector_log_error ([`a1e5d27`](https://gitlab.psi.ch/bec/bec/-/commit/a1e5d274c403ec74cebf305a086978877c553b11))

* test:test_redis_connector_log_message ([`de9f91f`](https://gitlab.psi.ch/bec/bec/-/commit/de9f91f432e9ac72fee2dea040ba545267acb58f))

* test:test_redis_connector_log_warning and created a connector mock object ([`f6cf55c`](https://gitlab.psi.ch/bec/bec/-/commit/f6cf55c25a4959082afec39ba6e0d894b2dc3b8e))

* test:test_redis_producer_get ([`8e85b27`](https://gitlab.psi.ch/bec/bec/-/commit/8e85b27321143754fd7ccf6fbae49cfe9fc1af75))

* test:test_redis_producer_delete ([`ac096ac`](https://gitlab.psi.ch/bec/bec/-/commit/ac096ac0e175b2803e0c85ac7983ecc443cfd035))

* test:test_redis_producer_pipeline ([`2cde8a0`](https://gitlab.psi.ch/bec/bec/-/commit/2cde8a00dfa5f3740c91901de04914a2b28a6cd3))

* test:test_redis_producer_keys ([`f1d07ad`](https://gitlab.psi.ch/bec/bec/-/commit/f1d07ad4cd49752d05bbc32607e32783b139569a))

* test:test_redis_producer_set ([`8614de2`](https://gitlab.psi.ch/bec/bec/-/commit/8614de23bd9b5daed8eda01d36c72fd1c3f18e1d))

* test:test_redis_producer_set_and_publish ([`677b821`](https://gitlab.psi.ch/bec/bec/-/commit/677b82188bb091d227db57ec53cecfb3c9de7b13))

* test:test_redis_producer_lrange ([`5b3815e`](https://gitlab.psi.ch/bec/bec/-/commit/5b3815e26c432d62b166c1e9029ecd74983d61f1))

* test:test_redis_producer_rpush and uese_pipe_fcn ([`01f351f`](https://gitlab.psi.ch/bec/bec/-/commit/01f351ffb4f03d044d3ff60a160378acc9f41605))

* test:test_redis_producer_lset ([`a8843c3`](https://gitlab.psi.ch/bec/bec/-/commit/a8843c31079ec587c7212c381d80e3bb903b480d))

* test:test_redis_producor_lpush ([`65804ab`](https://gitlab.psi.ch/bec/bec/-/commit/65804abda37aee59dda994f0d0118537bd4375de))

* test:test_redis_connector ([`c20fed1`](https://gitlab.psi.ch/bec/bec/-/commit/c20fed129027d9063865daa129e1673ec33be47a))

* Merge branch &#39;redis_connector_tests&#39; into &#39;master&#39;

test: first tests for redis_connector

See merge request bec/bec!147 ([`bcc927a`](https://gitlab.psi.ch/bec/bec/-/commit/bcc927ac1322ad20208b3e4779f90c9f434520aa))

* Merge branch &#39;master&#39; into redis_connector_tests ([`33b115e`](https://gitlab.psi.ch/bec/bec/-/commit/33b115e8e004756d5c45b95011f3b41ddf8e4ddf))

* Merge branch &#39;device_server_tests&#39; into &#39;master&#39;

Device server tests

See merge request bec/bec!146 ([`21d0d56`](https://gitlab.psi.ch/bec/bec/-/commit/21d0d563811ef7da2aa072d01ac3891f3b5f644d))

* Merge branch &#39;master&#39; into device_server_tests ([`876ee1f`](https://gitlab.psi.ch/bec/bec/-/commit/876ee1f51df14e65ff2efc1fb318ff2607fc2eec))

* Merge branch &#39;bl_show_all_plugins&#39; into &#39;master&#39;

refactor: added support for bl_show_all plugins

See merge request bec/bec!145 ([`0373e52`](https://gitlab.psi.ch/bec/bec/-/commit/0373e52db8924226933c05e3c7474fa444a56b3c))

* Merge branch &#39;device_server_tests&#39; into &#39;master&#39;

Device server tests

See merge request bec/bec!144 ([`494e86c`](https://gitlab.psi.ch/bec/bec/-/commit/494e86c24e8bd321b707b26f9aeec0ab76c68a98))

* Merge branch &#39;master&#39; into device_server_tests ([`12bd075`](https://gitlab.psi.ch/bec/bec/-/commit/12bd0755d11050a223bd1107defc169247712fad))

* Merge branch &#39;unit_test_report&#39; into &#39;master&#39;

test: added option to discard pipeline data

See merge request bec/bec!143 ([`27b04b2`](https://gitlab.psi.ch/bec/bec/-/commit/27b04b2987349bb77e7df17285905fa2b38e17fd))

* Update .gitlab-ci.yml ([`79a057d`](https://gitlab.psi.ch/bec/bec/-/commit/79a057d3e1b49986bfa924e062617537c0e3bf5e))

* Update requirements.txt ([`5dc3dc4`](https://gitlab.psi.ch/bec/bec/-/commit/5dc3dc4a7f502f7b05ae014a787651f8318e2836))

* test:started with test_handle_device_instructions ([`0340e06`](https://gitlab.psi.ch/bec/bec/-/commit/0340e06c4ca8e1b4f04c82446c1c3be780db38d5))

* Update .gitlab-ci.yml ([`91e94dc`](https://gitlab.psi.ch/bec/bec/-/commit/91e94dc4ac1f0317ea0929badf04280c400b931c))

* Update .gitlab-ci.yml ([`dd25ffe`](https://gitlab.psi.ch/bec/bec/-/commit/dd25ffe9b4e0141fc3ce7f469b9ff4423c64b936))

* Update .gitlab-ci.yml ([`18d4ac0`](https://gitlab.psi.ch/bec/bec/-/commit/18d4ac0a567d93e7af424338e5bd5d1717745468))

* Update .gitlab-ci.yml ([`8d32e96`](https://gitlab.psi.ch/bec/bec/-/commit/8d32e963871812091a9f409059c57a4e1cd6f3cd))

* Update .gitlab-ci.yml ([`81bd7db`](https://gitlab.psi.ch/bec/bec/-/commit/81bd7db8abc3bce48ceef9d9a410c0eed315e176))

* Update .gitlab-ci.yml ([`6d8b4fd`](https://gitlab.psi.ch/bec/bec/-/commit/6d8b4fd77adb0c062bba531f99b6effe2e6648e8))

* Update .gitlab-ci.yml ([`52077c7`](https://gitlab.psi.ch/bec/bec/-/commit/52077c725d84a26cbde9387ef48cc7c7276c16ec))

* Update .gitlab-ci.yml ([`bb47f92`](https://gitlab.psi.ch/bec/bec/-/commit/bb47f926c83c75a39100e4d3430189b2a9537dcd))

* Merge branch &#39;unit_test_report&#39; into &#39;master&#39;

device server tests

See merge request bec/bec!142 ([`35a1132`](https://gitlab.psi.ch/bec/bec/-/commit/35a113255a6c1bf9745acad8a1632d3c441e2245))

* Merge branch &#39;unit_test_report&#39; into &#39;master&#39;

Unit test report

See merge request bec/bec!141 ([`86a1eb9`](https://gitlab.psi.ch/bec/bec/-/commit/86a1eb91c615daec221c4b04c2799c14322a6eb9))

* Merge branch &#39;doc_update&#39; into &#39;master&#39;

docs: cleanup

See merge request bec/bec!140 ([`c8173ed`](https://gitlab.psi.ch/bec/bec/-/commit/c8173eddcc26bc249b429c87a013a3d9adc82607))

* Merge branch &#39;doc_update&#39; into &#39;master&#39;

docs: updated tutorial

See merge request bec/bec!139 ([`ffe74a5`](https://gitlab.psi.ch/bec/bec/-/commit/ffe74a53fadc94728065f4becc7edd8b03b735de))

* Merge branch &#39;python-version&#39; into &#39;master&#39;

ci: fixed typo

See merge request bec/bec!138 ([`c18b924`](https://gitlab.psi.ch/bec/bec/-/commit/c18b924886fe21f1523b8a3cb2e3e6834cce4bdd))

* Merge branch &#39;python-version&#39; into &#39;master&#39;

ci: added tests for different python versions

See merge request bec/bec!137 ([`e278d8f`](https://gitlab.psi.ch/bec/bec/-/commit/e278d8fbecfcff8b4b62c18be48daa5108110071))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`9ae0d0b`](https://gitlab.psi.ch/bec/bec/-/commit/9ae0d0b6239b64f5927789f9e6c7ec1de201c8ec))

* Update .gitlab-ci.yml ([`b368b2d`](https://gitlab.psi.ch/bec/bec/-/commit/b368b2d7b1913bbb5ac26752f0f14cad8dfd9bc0))

* Update .gitlab-ci.yml ([`eae24ca`](https://gitlab.psi.ch/bec/bec/-/commit/eae24ca3f5f33cf91ac90aa0f4c67c958b84a3b6))

* Update .gitlab-ci.yml ([`d205852`](https://gitlab.psi.ch/bec/bec/-/commit/d205852860f38a77d32543d0d348f101046cb8c8))

* Update .gitlab-ci.yml ([`150abd2`](https://gitlab.psi.ch/bec/bec/-/commit/150abd23c91d8b7323cc937e7cb56ee8ac3ec070))

* Update README.md ([`4ef3f91`](https://gitlab.psi.ch/bec/bec/-/commit/4ef3f918744c2af62e39da376d6c4b086c9c2340))

* Update .gitlab-ci.yml ([`55479eb`](https://gitlab.psi.ch/bec/bec/-/commit/55479ebfbc9d230e4cbd2f7c684f01e92f946f9f))

* doc: added requirements.txt for doc builds ([`57a607e`](https://gitlab.psi.ch/bec/bec/-/commit/57a607e56a34f16df8bb8ce18820b75fa82560c0))

* Add new file ([`0b89c46`](https://gitlab.psi.ch/bec/bec/-/commit/0b89c46415d58a5171264fa751106ffcf97d77ec))

* Update .gitlab-ci.yml ([`a27fb78`](https://gitlab.psi.ch/bec/bec/-/commit/a27fb782a9bd292fd31aba74211b0a6f5d3f343d))

* Merge branch &#39;doc_update&#39; into &#39;master&#39;

doc: updated documentation

See merge request bec/bec!135 ([`c18af1a`](https://gitlab.psi.ch/bec/bec/-/commit/c18af1a57431a0c7e1d5de30f429e97990153818))

* doc: updated documentation ([`16fdd21`](https://gitlab.psi.ch/bec/bec/-/commit/16fdd212cec4a226071aaad2500c5eb482d42f26))

* Merge branch &#39;scan_report_instructions&#39; into &#39;master&#39;

Scan report instructions

Closes #32

See merge request bec/bec!134 ([`0206631`](https://gitlab.psi.ch/bec/bec/-/commit/0206631b3fca2c163362e3072ae61b7b1fff2286))

* tests: fixed umv tests ([`13c0a8c`](https://gitlab.psi.ch/bec/bec/-/commit/13c0a8cb73be6baa34122c8258ebc3b7ae54b350))

* Merge branch &#39;master&#39; into scan_report_instructions ([`7bb0a09`](https://gitlab.psi.ch/bec/bec/-/commit/7bb0a09f0094e1088a156ffe1e3dafd9b6e28288))

* Update LICENSE ([`d529b0c`](https://gitlab.psi.ch/bec/bec/-/commit/d529b0ce70a5376f3eb3f4c50e8ab624aab8335d))

* Merge branch &#39;scan_report_devices&#39; into &#39;master&#39;

feat: added scan_report_devices

See merge request bec/bec!133 ([`4e2c3b7`](https://gitlab.psi.ch/bec/bec/-/commit/4e2c3b704e82c561098f8e47297cb4b17cd705ba))

* Add LICENSE ([`d36b257`](https://gitlab.psi.ch/bec/bec/-/commit/d36b257415c73bdac83cbe1432cbe907bd3f5ff9))

* Update bec_config_template.yaml ([`9a9193c`](https://gitlab.psi.ch/bec/bec/-/commit/9a9193cf759540e300830a81dae60df4e6beab5d))

* Merge branch &#39;master&#39; into semver ([`0b25ca6`](https://gitlab.psi.ch/bec/bec/-/commit/0b25ca6b4294a6c46e95887b06da6ebe5909ea1e))

* Merge branch &#39;cleanup&#39; into &#39;master&#39;

Cleanup

See merge request bec/bec!132 ([`9c508a9`](https://gitlab.psi.ch/bec/bec/-/commit/9c508a99276a14c8f33bd1969575c665ce37b93c))

* Merge branch &#39;cleanup&#39; into &#39;master&#39;

fix: cleanup after lamni

See merge request bec/bec!131 ([`8507f8a`](https://gitlab.psi.ch/bec/bec/-/commit/8507f8a01c3aeba54eaa5a6b14b573f21c3e1d9f))

* Merge branch &#39;epics_tests_csaxs&#39; into &#39;master&#39;

Epics tests csaxs

See merge request bec/bec!128 ([`8602307`](https://gitlab.psi.ch/bec/bec/-/commit/86023071f21b17af595fb2be93f45fda6c8c29fd))

* replaced hard-coded values by user params ([`adf1d7a`](https://gitlab.psi.ch/bec/bec/-/commit/adf1d7a2684805c8cb6397f1dee787c11a32ec0b))

* Merge branch &#39;epics_tests_csaxs&#39; into &#39;master&#39;

Epics tests csaxs

See merge request bec/bec!127 ([`a7bb20a`](https://gitlab.psi.ch/bec/bec/-/commit/a7bb20a8846d437a8a802c94e60bffccfddb9667))

* added sls_ring_current as monitored pv ([`ccc90ce`](https://gitlab.psi.ch/bec/bec/-/commit/ccc90ceeccb5095f5dbd7f7ce429de992dfeb974))

* Merge branch &#39;dev_container&#39; into &#39;master&#39;

feat: added scilog export for lamni

See merge request bec/bec!126 ([`2439949`](https://gitlab.psi.ch/bec/bec/-/commit/24399498ece5a0ad7ed088c31fb7dff693a87213))

* Merge branch &#39;dev_container&#39; into &#39;master&#39;

feat: added show_all; minor improvements

See merge request bec/bec!125 ([`f0632a5`](https://gitlab.psi.ch/bec/bec/-/commit/f0632a5afb7e88c86429f9d5db2a7cbff8e76e19))

* Merge branch &#39;csaxs_config_fix&#39; into &#39;master&#39;

Csaxs config fix

See merge request bec/bec!124 ([`533f85d`](https://gitlab.psi.ch/bec/bec/-/commit/533f85d7dae325ef75d7ab881685f998f86f62fb))

* fixed x12sa status pvs ([`661eae9`](https://gitlab.psi.ch/bec/bec/-/commit/661eae9aebff93f2da4c9da93730b12680d9fa8d))

* Merge branch &#39;csaxs_config_fix&#39; into &#39;master&#39;

fix: fixed csaxs config

See merge request bec/bec!123 ([`b95cee2`](https://gitlab.psi.ch/bec/bec/-/commit/b95cee24046cce6e1836baaa10941808054b706a))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

Scibec update

See merge request bec/bec!122 ([`e916f98`](https://gitlab.psi.ch/bec/bec/-/commit/e916f98e6b4bedb98b3ff7cb1ac19795920b782b))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

feat: added option to change the readout priority

See merge request bec/bec!121 ([`96331ad`](https://gitlab.psi.ch/bec/bec/-/commit/96331ad98de8d9d878e2e3eae0c35163303504dc))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

wm

See merge request bec/bec!120 ([`a891088`](https://gitlab.psi.ch/bec/bec/-/commit/a891088c196917236b9e501714f93106053f0736))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

added acquisition priority

See merge request bec/bec!118 ([`d6c6f80`](https://gitlab.psi.ch/bec/bec/-/commit/d6c6f802e754f35421f3a8fa63f6d841b9c16480))

* Merge branch &#39;master&#39; into scibec_update ([`adb9630`](https://gitlab.psi.ch/bec/bec/-/commit/adb9630d792355d19847509035d286e5a6e0072a))

* Merge branch &#39;cleanup&#39; into &#39;master&#39;

ci: cleanup

See merge request bec/bec!119 ([`27fa9bb`](https://gitlab.psi.ch/bec/bec/-/commit/27fa9bbfa678eb892e39865aec975fce4b7078a7))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

feat: added show_tags

See merge request bec/bec!117 ([`f467647`](https://gitlab.psi.ch/bec/bec/-/commit/f467647b8c53538f90144e346a714f86504a90f2))

* Merge branch &#39;scibec_update&#39; into &#39;master&#39;

renamed deviceGroup to deviceTags; added onFailure to config

See merge request bec/bec!110 ([`4fc97a1`](https://gitlab.psi.ch/bec/bec/-/commit/4fc97a1a78cfce3692d0fa24c85ed4b88a6f1381))

* Merge branch &#39;logbook&#39; into &#39;master&#39;

added pdf_writer and logbook connector

See merge request bec/bec!115 ([`d07b5f5`](https://gitlab.psi.ch/bec/bec/-/commit/d07b5f5977d237e11a2dff72a1f6ac0ffc04d0b1))

* fixed username detection ([`7d827a4`](https://gitlab.psi.ch/bec/bec/-/commit/7d827a447e59c1707bbd3164c1d42cc6edbc625f))

* added option to specify the font for the pdf writer ([`5bab580`](https://gitlab.psi.ch/bec/bec/-/commit/5bab5802d1b6008f9e57fdb872cba4724e9330c2))

* added pdf_writer and logbook connector ([`81baf5f`](https://gitlab.psi.ch/bec/bec/-/commit/81baf5f37d12a0f8184cf1920c390a4aee7c93e3))

* Merge branch &#39;client_refactor&#39; into &#39;master&#39;

pylint

See merge request bec/bec!114 ([`91bd914`](https://gitlab.psi.ch/bec/bec/-/commit/91bd914411e31ac2116ff2f91ac3a3bbbb10be17))

* pylint ([`e5d41bd`](https://gitlab.psi.ch/bec/bec/-/commit/e5d41bd2c07aa55423f108c678038f02201d8c35))

* Merge branch &#39;client_refactor&#39; into &#39;master&#39;

refactored becclient; added tests for user scripts mixin

See merge request bec/bec!113 ([`21d57d2`](https://gitlab.psi.ch/bec/bec/-/commit/21d57d2c7ca9115f772af61aac1be804c9f9bfa4))

* refactored becclient; added tests for user scripts mixin ([`8dc1eab`](https://gitlab.psi.ch/bec/bec/-/commit/8dc1eab4562af83350c37b0739dc4e31fba89585))

* Merge branch &#39;metadata_handler&#39; into &#39;master&#39;

added metadata handler

See merge request bec/bec!112 ([`0af48d4`](https://gitlab.psi.ch/bec/bec/-/commit/0af48d44784e482d499c3c3719ea716ef5625ebe))

* added scan tests ([`e14a6eb`](https://gitlab.psi.ch/bec/bec/-/commit/e14a6ebeacb8309a7359d77771d5407b75f6a362))

* added metadata handler ([`e667dc7`](https://gitlab.psi.ch/bec/bec/-/commit/e667dc75ba078e5812f2cd0dea0c486d4e0f145c))

* Merge branch &#39;ci_cleanup&#39; into &#39;master&#39;

cleanup

See merge request bec/bec!111 ([`6e8c9b8`](https://gitlab.psi.ch/bec/bec/-/commit/6e8c9b8d248067fc09eb3d262d1c8a10a76e1259))

* cleanup ([`450e0cf`](https://gitlab.psi.ch/bec/bec/-/commit/450e0cf78f47ddda6e7b3c4fbe30459e77044e0b))

* Merge branch &#39;acquisition_group&#39; into &#39;master&#39;

renamed device_group to acquisition_group

See merge request bec/bec!109 ([`4efbaa0`](https://gitlab.psi.ch/bec/bec/-/commit/4efbaa08bd41e11f27268f10cf2dceeedb228703))

* FEAT: added semver ([`d5f52bd`](https://gitlab.psi.ch/bec/bec/-/commit/d5f52bd4e1a74eb89239825130e27f43f38a2e18))

* renamed deviceGroup to deviceTags; added failure to acqusitionConfig ([`736f16c`](https://gitlab.psi.ch/bec/bec/-/commit/736f16c2574d6f0bbc27f4a3e06e8f31923a51d1))

* renamed device_group to acquisition_group ([`36a76c6`](https://gitlab.psi.ch/bec/bec/-/commit/36a76c6f3ed2dd19a30b9f3943655dfc6c6b9455))

* Merge branch &#39;ci_update&#39; into &#39;master&#39;

fixed paths to log files

See merge request bec/bec!108 ([`d045f9f`](https://gitlab.psi.ch/bec/bec/-/commit/d045f9fb1c8c6b91c80f51b126f3537657036ec0))

* fixed paths to log files ([`5a0300c`](https://gitlab.psi.ch/bec/bec/-/commit/5a0300c9dcaaae489b3f5e33822511d7f9e940d7))

* Merge branch &#39;beamline_mixin_tests&#39; into &#39;master&#39;

added tests for beamline mixin

See merge request bec/bec!107 ([`3b23d48`](https://gitlab.psi.ch/bec/bec/-/commit/3b23d483cc6756c1e9d91e66cc487e2c15e3d397))

* added tests for beamline mixin ([`7924978`](https://gitlab.psi.ch/bec/bec/-/commit/7924978170e1363854e4deb54d99220d5af92bbd))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!106 ([`302ff21`](https://gitlab.psi.ch/bec/bec/-/commit/302ff21bfae5f03cde95f0466c250fd47deda92d))

* bug fixes for beamline mixin ([`7680a53`](https://gitlab.psi.ch/bec/bec/-/commit/7680a53a4cebde9120e160fba4e19dabc1ea39ba))

* added operator_messages ([`14e4268`](https://gitlab.psi.ch/bec/bec/-/commit/14e4268f37d9a7bf747363191d02cea08243e1b6))

* bug fixes for sls info ([`0d27844`](https://gitlab.psi.ch/bec/bec/-/commit/0d27844f3f8b79e960713fe492df8debf66a3dbf))

* updated beamline mixin ([`2821f00`](https://gitlab.psi.ch/bec/bec/-/commit/2821f00c477d3e53ae79b58a0bdaa384a8791bdd))

* fixed lamni fermat pos test for new trajectory ([`a84d618`](https://gitlab.psi.ch/bec/bec/-/commit/a84d61852a42f4e15e685f7931363713465c9893))

* added scan msgs to open scan events ([`db85b8a`](https://gitlab.psi.ch/bec/bec/-/commit/db85b8a37ab06ff26b59a0779839eff2a97d3d11))

* fixed bug in file writer ([`a95730c`](https://gitlab.psi.ch/bec/bec/-/commit/a95730c345762a7b24a803e6f111b70802cd8015))

* Merge branch &#39;online_changes&#39; of gitlab.psi.ch:bec/bec into online_changes ([`de3e14e`](https://gitlab.psi.ch/bec/bec/-/commit/de3e14efb195938fca980bf907c8e439f6c651ff))

* online changes ([`57da942`](https://gitlab.psi.ch/bec/bec/-/commit/57da942c45e25de00615e105cb0d2f427c586464))

* baseline readings are now falling back to cached values on error ([`5ef3a7b`](https://gitlab.psi.ch/bec/bec/-/commit/5ef3a7b6c64cc88cdbe6df32c7c64181a8cad22d))

* changed default corridor axis to 1 ([`b5bc02d`](https://gitlab.psi.ch/bec/bec/-/commit/b5bc02d65c5c7452a9108fd7866447ba4cdc0a76))

* cleanup; added path optim as default ([`d76b670`](https://gitlab.psi.ch/bec/bec/-/commit/d76b670d37bb0a8faa0f7064a8eeaf512cdd3a1e))

* added option to load cached values if a new reading fails ([`6f70a8a`](https://gitlab.psi.ch/bec/bec/-/commit/6f70a8a58d72eb28bfe1aedb931f0333b34ef1f1))

* fixed read for non-standard signals ([`e7029c8`](https://gitlab.psi.ch/bec/bec/-/commit/e7029c85471d8d91efa93c3f8bbe996f228ae36a))

* fixed bug in config helper for non-existing enabled_set flags ([`876aaee`](https://gitlab.psi.ch/bec/bec/-/commit/876aaee9ae6e92886910466ae5a8eb2d15d94ca4))

* added combined test config for lamni ([`32108e0`](https://gitlab.psi.ch/bec/bec/-/commit/32108e0fef28eb6c48c904dac6a54a7da75b3fb6))

* removed simulations; added csaxs config ([`82c9bcb`](https://gitlab.psi.ch/bec/bec/-/commit/82c9bcbad34467cb8ecc01b913e77d6bb1745f6e))

* fixed mokev assignment ([`410c99b`](https://gitlab.psi.ch/bec/bec/-/commit/410c99b0496151e42dd38a1609996c6ca0ad0128))

* adjusted prettytable padding for max size header ([`a1fa6fa`](https://gitlab.psi.ch/bec/bec/-/commit/a1fa6fa6eab184fc8bdc0936434da161f000a79f))

* added beam checks; added sample database ([`07fb1c3`](https://gitlab.psi.ch/bec/bec/-/commit/07fb1c3cc7e6cdab511d7c558dcbf5ef47ade1dd))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

added requestID to restart request

See merge request bec/bec!105 ([`9e21791`](https://gitlab.psi.ch/bec/bec/-/commit/9e21791ddb1bc0134829433cdddf754e317e414a))

* fixed test ([`9bfb12f`](https://gitlab.psi.ch/bec/bec/-/commit/9bfb12fb995c69e69c751592bd99c03e03f1126f))

* added requestID to restart request ([`c86801f`](https://gitlab.psi.ch/bec/bec/-/commit/c86801fa700373103372d47d3344329cf8915bbd))

* added test config for cSAXS ([`22554fa`](https://gitlab.psi.ch/bec/bec/-/commit/22554fa0e7f3bbbf959a1af0e018b30b800615e1))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!104 ([`641feed`](https://gitlab.psi.ch/bec/bec/-/commit/641feeda7d560380245a71f3230f336f5fbaf21e))

* added activeEaccount to beamline model ([`2e451f9`](https://gitlab.psi.ch/bec/bec/-/commit/2e451f9a9a856812d29d7848088bc3ef03f3d543))

* updated demo.py ([`2eb8414`](https://gitlab.psi.ch/bec/bec/-/commit/2eb84142e72c5b3ec297e940e2f5b709ceaaa5da))

* added context manager for dataset management ([`5b7dc95`](https://gitlab.psi.ch/bec/bec/-/commit/5b7dc95871df6b2591914096dafc786f239dd510))

* added next_dataset_number to client ([`4492c22`](https://gitlab.psi.ch/bec/bec/-/commit/4492c22c3707270fd2150945e09cde5b841ceb20))

* added dataset_on_hold ([`e3c5a66`](https://gitlab.psi.ch/bec/bec/-/commit/e3c5a66f1080789036a7a7f63875045e91d6d38f))

* added dataset_number; scan number is now initialized to 1 anymore ([`f5434e6`](https://gitlab.psi.ch/bec/bec/-/commit/f5434e62bd6c35883658c6a6e22972225d19936b))

* added dataset_number endpoint ([`5d44895`](https://gitlab.psi.ch/bec/bec/-/commit/5d44895cdeb521a68a8bc37ec155833658385433))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

added soft link to eiger_4

See merge request bec/bec!103 ([`158fc2c`](https://gitlab.psi.ch/bec/bec/-/commit/158fc2cfaf6b72982d6ae51bddadc0ba551c61c0))

* added soft link to eiger_4 ([`799d81a`](https://gitlab.psi.ch/bec/bec/-/commit/799d81a143cfcb61b8357b42f023ab4a7308d198))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!102 ([`3bb5073`](https://gitlab.psi.ch/bec/bec/-/commit/3bb507352ab2e8b9bee9fa8e6ed16a325581bbe3))

* fixed file writer tests ([`c7f4bb7`](https://gitlab.psi.ch/bec/bec/-/commit/c7f4bb72fa64bd18c98ba36f3be1a667597cc7ae))

* fixed test for new lamni scan default ([`4960484`](https://gitlab.psi.ch/bec/bec/-/commit/49604846f356595ef2057a8182fef3deac91d5f0))

* refactored lamni config ([`c8c4d92`](https://gitlab.psi.ch/bec/bec/-/commit/c8c4d92761a13c078f1840cc9e302d6cdbb993c2))

* added sls_operator and sls_info ([`8d8a1e9`](https://gitlab.psi.ch/bec/bec/-/commit/8d8a1e96f004387534b5a7d8809fcea1107d880c))

* bug fixes ([`2f83ef6`](https://gitlab.psi.ch/bec/bec/-/commit/2f83ef6186573a1400fc73c51592a76068139187))

* added device manager to nexus writer; bug fixes ([`0496e23`](https://gitlab.psi.ch/bec/bec/-/commit/0496e23e1e3fa5d9d8c468b8768d0d9cf0a902ee))

* fixed bug in xray-eye-align output ([`b59c4d5`](https://gitlab.psi.ch/bec/bec/-/commit/b59c4d52d6c0f27e9a3f480b461aeffc76a7a9e0))

* formatter ([`84a4970`](https://gitlab.psi.ch/bec/bec/-/commit/84a4970c3789f8e68813adfda092fdf5f7637f5e))

* minor cleanup ([`792bb25`](https://gitlab.psi.ch/bec/bec/-/commit/792bb25113a1a060200d7c2e74461e9e48aac125))

* added traj optim; doc ([`9e2d2e6`](https://gitlab.psi.ch/bec/bec/-/commit/9e2d2e6fe1994306241a17502f46739f12648d71))

* removed automatic plugin import ([`589b321`](https://gitlab.psi.ch/bec/bec/-/commit/589b3214bfcc39e7e713bcd67ab155a4d6d492b9))

* added option to change the scan number from client ([`22c85e6`](https://gitlab.psi.ch/bec/bec/-/commit/22c85e6a4523b70b093f5ac790eb6884bcca1020))

* Merge branch &#39;detector_fixes&#39; into &#39;master&#39; ([`6775365`](https://gitlab.psi.ch/bec/bec/-/commit/6775365faeed3f260cf5003e3a6e563a6869fccf))

* added wait for service ([`90f4858`](https://gitlab.psi.ch/bec/bec/-/commit/90f4858b1411418e885d1beb9e6b4939c07d80bf))

* Merge branch &#39;detector_fixes&#39; into &#39;master&#39;

added stage response; added exp_time to scan status

See merge request bec/bec!100 ([`de2cd23`](https://gitlab.psi.ch/bec/bec/-/commit/de2cd23962db49bfff0c9387a1c9e1c0faabb3bb))

* added stage response; added exp_time to scan status ([`abeb10c`](https://gitlab.psi.ch/bec/bec/-/commit/abeb10c647b936543995af9a2b84850f813f6631))

* Merge branch &#39;client_callback&#39; into &#39;master&#39; ([`141c028`](https://gitlab.psi.ch/bec/bec/-/commit/141c028e7790922d039c2d76f50f189fac28cc2b))

* added callback_manager ([`ecf9eca`](https://gitlab.psi.ch/bec/bec/-/commit/ecf9eca4cfeba9f9e29ffaf2f38de8ad5ced5a78))

* added option to resume a callback ([`0cce5fc`](https://gitlab.psi.ch/bec/bec/-/commit/0cce5fc3c4d9c27c7409e4469d610da00ac19add))

* Merge branch &#39;scan_defs&#39; into &#39;master&#39;

bug fixes for scan defs

See merge request bec/bec!98 ([`2f6d8c8`](https://gitlab.psi.ch/bec/bec/-/commit/2f6d8c884ad439a323800215168e5f70e46fc32a))

* bug fixes for scan defs ([`ef1c477`](https://gitlab.psi.ch/bec/bec/-/commit/ef1c4771af534470b90984fc95285474db760879))

* Merge branch &#39;client_callback&#39; into &#39;master&#39;

cleanup

See merge request bec/bec!96 ([`5d84943`](https://gitlab.psi.ch/bec/bec/-/commit/5d8494301a3dc2b4bfe1ac7c96d64a8d309cfa85))

* removed plugins and scripts from coverage ([`167c2a6`](https://gitlab.psi.ch/bec/bec/-/commit/167c2a6311fc1693391a204d16306c54517bbd89))

* removed plugins and scripts from coverage ([`8c18336`](https://gitlab.psi.ch/bec/bec/-/commit/8c18336e2450ed7f1e35101512f14382046e1a41))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec into client_callback ([`2be5695`](https://gitlab.psi.ch/bec/bec/-/commit/2be569506b8ec2561a9ce29054db589735c48ef6))

* client setup cleanup ([`6f51381`](https://gitlab.psi.ch/bec/bec/-/commit/6f51381149cb507c3ee46b87e1e41b6f6f672633))

* Merge branch &#39;add_positions&#39; into &#39;master&#39;

added positions

See merge request bec/bec!95 ([`2719209`](https://gitlab.psi.ch/bec/bec/-/commit/2719209a124b3af2478261e7a2e4ef2feb6c3393))

* fixed precision error in lamni test ([`7152a0c`](https://gitlab.psi.ch/bec/bec/-/commit/7152a0cea87fcd2bdc65a15c86f5907b82584948))

* bug in open scan positions ([`22fcc37`](https://gitlab.psi.ch/bec/bec/-/commit/22fcc3736245a6c9bb355cac76dd8c2d6aaad451))

* added pos ([`30d6653`](https://gitlab.psi.ch/bec/bec/-/commit/30d6653dc3cccc6fde5dd1e7eb14b23dbf239a7c))

* added positions ([`8233d91`](https://gitlab.psi.ch/bec/bec/-/commit/8233d910007c4c9db48de4c002ab81fab8b9250d))

* Merge branch &#39;traj_optim&#39; into &#39;master&#39;

added trajectory optimization to scans; closes #39

Closes #39

See merge request bec/bec!94 ([`6532d21`](https://gitlab.psi.ch/bec/bec/-/commit/6532d21ef886d665210bb80933951b7b18a19303))

* added trajectory optimization to scans; closes #39 ([`4fb160a`](https://gitlab.psi.ch/bec/bec/-/commit/4fb160aea28639fb7e390cfadfdc4345d4978a94))

* Merge branch &#39;client_bug_fixes&#39; into &#39;master&#39;

bug fixes

See merge request bec/bec!93 ([`3732514`](https://gitlab.psi.ch/bec/bec/-/commit/37325149de8e43d3527d94baa30d966808ab4e75))

* fixed num points for fermat spiral test ([`5bdd2a6`](https://gitlab.psi.ch/bec/bec/-/commit/5bdd2a66de2a51fadea3e2cee87276820962c18d))

* bug fixes ([`acb4aea`](https://gitlab.psi.ch/bec/bec/-/commit/acb4aeab269cf39e97bb037ab0d4688346abdea2))

* Update setup.cfg ([`07c7444`](https://gitlab.psi.ch/bec/bec/-/commit/07c744437fafdc857c457a12ca243a692ea2793b))

* Merge branch &#39;path_optim&#39; into &#39;master&#39;

added path optimization

See merge request bec/bec!92 ([`a84d352`](https://gitlab.psi.ch/bec/bec/-/commit/a84d3521b083c2cbad3809df90f54bed1eb02c8a))

* added path optimization ([`358a37b`](https://gitlab.psi.ch/bec/bec/-/commit/358a37bb9b561823c503a54e90c9962ed5715eac))

* Merge branch &#39;file_writer_fix&#39; into &#39;master&#39;

fixed bug in file writer dir path

See merge request bec/bec!91 ([`fa5f3bd`](https://gitlab.psi.ch/bec/bec/-/commit/fa5f3bd77dbff74f6e3f3c825146a21703befab7))

* fixed bug in file writer dir path ([`b35acbc`](https://gitlab.psi.ch/bec/bec/-/commit/b35acbc55266541d2213f3c96b602ed4caa6e317))

* Merge branch &#39;abort_messages&#39; into &#39;master&#39;

added ipython magics for more consistency; closes #52

Closes #52

See merge request bec/bec!90 ([`b12bae0`](https://gitlab.psi.ch/bec/bec/-/commit/b12bae01bec4f72f3f0f180c9371dd40d3bc36c2))

* fixed bug for scripted clients ([`b741795`](https://gitlab.psi.ch/bec/bec/-/commit/b741795f5e01d186a67de0d2990e625f70d0787d))

* added ipython magics for more consistency; closes #52 ([`b73936f`](https://gitlab.psi.ch/bec/bec/-/commit/b73936f9c84a81704deaaffbfc87b79f53a9b091))

* Merge branch &#39;client_plugins&#39; into &#39;master&#39;

cleanup; moved scripts to plugins; closes #58

Closes #58

See merge request bec/bec!88 ([`a5590af`](https://gitlab.psi.ch/bec/bec/-/commit/a5590afd9f4a4842b76fb15a1ab1cfd16d41d98b))

* Merge branch &#39;master&#39; into client_plugins ([`bd95fb8`](https://gitlab.psi.ch/bec/bec/-/commit/bd95fb821d8d4b7fa659d356584a08c49fb56595))

* Merge branch &#39;config_update&#39; into &#39;master&#39;

added custom config update

See merge request bec/bec!87 ([`aa21aad`](https://gitlab.psi.ch/bec/bec/-/commit/aa21aad07642d1c19054c5add1ef1e69fe7ad986))

* added custom config update ([`2f34eba`](https://gitlab.psi.ch/bec/bec/-/commit/2f34ebae29593cd2ff38788b2b3be70e114c0fcf))

* Merge branch &#39;online_changes&#39; into &#39;master&#39; ([`340915c`](https://gitlab.psi.ch/bec/bec/-/commit/340915cc9d8eb4261c3469ea3f8677aea3e6ec32))

* fixed formatting ([`247baab`](https://gitlab.psi.ch/bec/bec/-/commit/247baab4a5fd5092dbb3443fb393ab25e9c18b81))

* Merge branch &#39;online_changes&#39; of gitlab.psi.ch:bec/bec into online_changes ([`268ce50`](https://gitlab.psi.ch/bec/bec/-/commit/268ce50c74890c9067a6c559381448af256637b9))

* online fixes for tomo ([`25781f3`](https://gitlab.psi.ch/bec/bec/-/commit/25781f303d5de32b6795d01d7f1542112e503fc6))

* Merge branch &#39;config_update&#39; into &#39;master&#39;

added user mixin for config updates

See merge request bec/bec!85 ([`32ba192`](https://gitlab.psi.ch/bec/bec/-/commit/32ba192642222a8bab42097b26942f806581a562))

* cleanup; moved scripts to plugins ([`eaf4aa0`](https://gitlab.psi.ch/bec/bec/-/commit/eaf4aa08ca9d53b8aa525a4ced4977aad277002b))

* added user mixin for config updates ([`578bb33`](https://gitlab.psi.ch/bec/bec/-/commit/578bb3328e56d8d9fd2a7c4187045a9770520e9b))

* Merge branch &#39;mem_leak&#39; into &#39;master&#39;

fixed mem leak in scan bundler

See merge request bec/bec!84 ([`e348a33`](https://gitlab.psi.ch/bec/bec/-/commit/e348a333974d77de90ac0788f5c7050b36d0079f))

* fixed mem leak in scan bundler ([`ce4a4e4`](https://gitlab.psi.ch/bec/bec/-/commit/ce4a4e445d82ad6edb893032a2cd143b9d723252))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!79 ([`99873c1`](https://gitlab.psi.ch/bec/bec/-/commit/99873c10fae1cb75cc364125c6ffb3bd29d20461))

* fixed mock for user parameter ([`f066207`](https://gitlab.psi.ch/bec/bec/-/commit/f066207f8dddf38fc31c9dae8a3e2b13922b8d93))

* formatting ([`b3052af`](https://gitlab.psi.ch/bec/bec/-/commit/b3052af8bb85a5b0ef9ffece621bd4aaf9e958c4))

* added tomoscripts to lamni ([`bf72ea5`](https://gitlab.psi.ch/bec/bec/-/commit/bf72ea5c20cd8092baee7afbf13801e0caaddd24))

* added tomo script ([`08cd8e9`](https://gitlab.psi.ch/bec/bec/-/commit/08cd8e92487b3f817c27d1bc4fb7bc4423ecb043))

* fixed path to matlab txt files ([`b2c9bed`](https://gitlab.psi.ch/bec/bec/-/commit/b2c9bedcafbf2d2ea74a2583b21f1214c84bfc5d))

* added real lamni scan command ([`8609484`](https://gitlab.psi.ch/bec/bec/-/commit/86094845a088174578fc641a1cdfa8b862484faa))

* fixed fov_offet scale ([`c8f285c`](https://gitlab.psi.ch/bec/bec/-/commit/c8f285cdcb67de2cf5c124868059b8256c2d116e))

* bug fixes for x_ray_eye_align ([`6f167b9`](https://gitlab.psi.ch/bec/bec/-/commit/6f167b97a5c2042bb410a076d3609e04f3965e22))

* added file writer to tmux; enabled mouse mode ([`10f335f`](https://gitlab.psi.ch/bec/bec/-/commit/10f335f068045328a65baf63035a3e2a8cec1c1c))

* fixed bug in scripts init ([`316c429`](https://gitlab.psi.ch/bec/bec/-/commit/316c42995b2922e8a562a07546c1e1b1022001a6))

* prel lamsni output ([`cf164db`](https://gitlab.psi.ch/bec/bec/-/commit/cf164db17d4509486030140e45949ce6fc801d26))

* prel lamsni output ([`89cd4c1`](https://gitlab.psi.ch/bec/bec/-/commit/89cd4c1493886056f5eda8edebfb4cdba4d6710b))

* added lsamx/lsamy center from config ([`50b52c7`](https://gitlab.psi.ch/bec/bec/-/commit/50b52c7df2a6a48986081aec8c44e26cc2dce87d))

* Merge branch &#39;observer&#39; into &#39;master&#39;

Observer

See merge request bec/bec!83 ([`338f17b`](https://gitlab.psi.ch/bec/bec/-/commit/338f17b02827aca472ede746a3566200fc4be2fd))

* removed tomo from demo ([`0b08bcd`](https://gitlab.psi.ch/bec/bec/-/commit/0b08bcdb0a99e5a8f1d8e421ba4d1d23cd66c1f8))

* added observer ([`dc9b50e`](https://gitlab.psi.ch/bec/bec/-/commit/dc9b50ecabc86df760ccebd7fb056812eba54a3e))

* added observer endpoint and message ([`7f4e9c2`](https://gitlab.psi.ch/bec/bec/-/commit/7f4e9c2550bcf6db7647764c9dcfe89c0169278b))

* Merge branch &#39;dm_cleanup&#39; into &#39;master&#39;

added test for rpc errors; closes #55

Closes #55

See merge request bec/bec!82 ([`50cfb00`](https://gitlab.psi.ch/bec/bec/-/commit/50cfb00ed1cb42440d339866da058573fe77dfbb))

* added test for rpc errors; closes #55 ([`c611de6`](https://gitlab.psi.ch/bec/bec/-/commit/c611de675feb76538274b02118a58abc7ef78693))

* Merge branch &#39;dm_cleanup&#39; into &#39;master&#39;

added test for user params; closes #57

Closes #57

See merge request bec/bec!81 ([`37b5122`](https://gitlab.psi.ch/bec/bec/-/commit/37b5122028a6fafe3b1fc92c6e4842b1f09486ab))

* added test for user params; closes #57 ([`c7bcb1c`](https://gitlab.psi.ch/bec/bec/-/commit/c7bcb1ce5d38c26e5d9f55fd5518e82e32077dfa))

* Merge branch &#39;dm_cleanup&#39; into &#39;master&#39;

dm cleanup; added more dm tests

See merge request bec/bec!80 ([`f3a29b5`](https://gitlab.psi.ch/bec/bec/-/commit/f3a29b577a8565050f843e8156b67441ea0b4c22))

* removed test dir from coverage ([`2083117`](https://gitlab.psi.ch/bec/bec/-/commit/20831178b11b7446ea816f682e08de5043c115c0))

* removed status callback ([`c126d95`](https://gitlab.psi.ch/bec/bec/-/commit/c126d956745adec36a6969097ee96c54e27eeba6))

* dm cleanup; added more dm tests ([`837e631`](https://gitlab.psi.ch/bec/bec/-/commit/837e631275e34903e6f06e56ee8b8be968037efd))

* Merge branch &#39;file_writer_path&#39; into &#39;master&#39;

File writer path

See merge request bec/bec!78 ([`2b50ebe`](https://gitlab.psi.ch/bec/bec/-/commit/2b50ebe8710c5678f91a295b8d54026731bd099d))

* number of leading zeros are now consistent with csaxs ([`b86dadf`](https://gitlab.psi.ch/bec/bec/-/commit/b86dadf5dceddc114b659284fdf3b02baa03dbd4))

* scan start at 1, not 0 ([`0ed9a28`](https://gitlab.psi.ch/bec/bec/-/commit/0ed9a28f6f6399d7053a0d244b8f38109ec81ba9))

* file writer now creates the target directory if needed ([`9e8074b`](https://gitlab.psi.ch/bec/bec/-/commit/9e8074b642a2d9d3c68bf4893258f902d6713bc2))

* Merge branch &#39;enabled_device_init&#39; into &#39;master&#39;

fixed init for re-enabled devices

See merge request bec/bec!77 ([`6f7a7c8`](https://gitlab.psi.ch/bec/bec/-/commit/6f7a7c8c4db77b81b50dccad25df0cfbd0bff8c7))

* fixed init for re-enabled devices ([`31fad67`](https://gitlab.psi.ch/bec/bec/-/commit/31fad671b1844f0c6a39572d723c767a9f0874eb))

* Merge branch &#39;device_stop&#39; into &#39;master&#39;

global vars

See merge request bec/bec!76 ([`b44ef25`](https://gitlab.psi.ch/bec/bec/-/commit/b44ef25d3221ad7999e31076b3a210109c91f416))

* changed global_vars from property to func to avoid ipython side-effects ([`30131ab`](https://gitlab.psi.ch/bec/bec/-/commit/30131aba5b3eb96e6b3eb699f4f4a2f955903d7b))

* Merge branch &#39;device_stop&#39; into &#39;master&#39;

fixed device stop for set-disabled devices

See merge request bec/bec!75 ([`2818925`](https://gitlab.psi.ch/bec/bec/-/commit/28189253b8ce3daf8db731498cbddf56b0d42997))

* fixed device stop for set-disabled devices ([`fa6bfd0`](https://gitlab.psi.ch/bec/bec/-/commit/fa6bfd0d214fd48c1f4cc501cd89809074617089))

* Merge branch &#39;dev_repr&#39; into &#39;master&#39;

Dev repr

See merge request bec/bec!74 ([`e01f18e`](https://gitlab.psi.ch/bec/bec/-/commit/e01f18e6caf185010cf89c332578e0f9fec5ec36))

* added user parameter to device repr ([`35a288d`](https://gitlab.psi.ch/bec/bec/-/commit/35a288d5515a4c165ffaabc8b20879fd88508f1a))

* Merge branch &#39;scan_report_fix&#39; into &#39;master&#39;

fixed scan report

See merge request bec/bec!73 ([`b2c2151`](https://gitlab.psi.ch/bec/bec/-/commit/b2c2151a9aad6dd004a8ccb180004d6c57b59620))

* fixed scan report ([`ed485e8`](https://gitlab.psi.ch/bec/bec/-/commit/ed485e874e86780e53cb968023f818936d75d2d1))

* Merge branch &#39;lamni_align&#39; into &#39;master&#39;

Lamni align

See merge request bec/bec!69 ([`60a7376`](https://gitlab.psi.ch/bec/bec/-/commit/60a7376c1ca971f121792f01490ffe503b24456c))

* added additional corrections to lamni class ([`0e9cefd`](https://gitlab.psi.ch/bec/bec/-/commit/0e9cefdb98948f5df80bbd1e81571cc5b08c9d8e))

* added additional correction script ([`d6d9235`](https://gitlab.psi.ch/bec/bec/-/commit/d6d9235f619d34c7ae31620400a927fa7b33e14c))

* removed lscans and load function after merging them into the lamni class ([`b77ac2a`](https://gitlab.psi.ch/bec/bec/-/commit/b77ac2a16d78dd8e4c19348a6ebaf7224f9724c2))

* added lamni class ([`03baf5f`](https://gitlab.psi.ch/bec/bec/-/commit/03baf5f72d1be05120feea14a592d320b6c269e0))

* added lscan and load function ([`25bf203`](https://gitlab.psi.ch/bec/bec/-/commit/25bf203c404fcfc98def714e9032b0be0a124272))

* Update .gitlab-ci.yml ([`b12ff4e`](https://gitlab.psi.ch/bec/bec/-/commit/b12ff4e05a4ed61f5de907115d1dcdae7d6cc7f9))

* Merge branch &#39;docs&#39; into &#39;master&#39;

Docs

See merge request bec/bec!72 ([`3f57d79`](https://gitlab.psi.ch/bec/bec/-/commit/3f57d7988bcd7b187943064fcf94f70e4547d4b6))

* added pages to gitlab-ci ([`2048126`](https://gitlab.psi.ch/bec/bec/-/commit/20481262dab903bfb5dbdd33739b76a3ff776b3c))

* added docs ([`1ee667c`](https://gitlab.psi.ch/bec/bec/-/commit/1ee667cc38101c57c651860ee9a6341ef2d3214d))

* Merge branch &#39;singleton_client&#39; into &#39;master&#39;

bug fixes for user params

See merge request bec/bec!71 ([`fd5d624`](https://gitlab.psi.ch/bec/bec/-/commit/fd5d6242871c150ee172b7856a39d83e0a9176ec))

* bug fix ([`e7a27be`](https://gitlab.psi.ch/bec/bec/-/commit/e7a27be27bed43c677e4088a320ff3b4f52c7a68))

* bug fixes for user params ([`b6e5e50`](https://gitlab.psi.ch/bec/bec/-/commit/b6e5e50ca4ea9389cd5e5f338d301e8c1f62fdd0))

* Merge branch &#39;singleton_client&#39; into &#39;master&#39;

added metadata and user params; closes #54

Closes #54

See merge request bec/bec!70 ([`d7c402f`](https://gitlab.psi.ch/bec/bec/-/commit/d7c402ff025d95e45e39d4e3cce0326e0d34ef43))

* added user parameter ([`c5273f1`](https://gitlab.psi.ch/bec/bec/-/commit/c5273f17662e0cd56950e78172818cba061fcbf6))

* fixed tests ([`2068e67`](https://gitlab.psi.ch/bec/bec/-/commit/2068e675fa127b2e22cba8c1ba1199a249fdfd94))

* fixed bug in file writer ([`946fd24`](https://gitlab.psi.ch/bec/bec/-/commit/946fd247a0e60e929a673053264d5d736493f5ce))

* added metadata pipeline ([`cfb2d89`](https://gitlab.psi.ch/bec/bec/-/commit/cfb2d8960403e83bab72dc081d013ac7cf269fde))

* updated tests ([`7902a20`](https://gitlab.psi.ch/bec/bec/-/commit/7902a20dc550c442dd9e1e4aacd0ad560495a223))

* becclient is now a singleton class ([`51aa37a`](https://gitlab.psi.ch/bec/bec/-/commit/51aa37a6b0bf0979e5059e1b3aee382c83c7c7c5))

* Merge branch &#39;load_scripts&#39; into &#39;master&#39;

Load scripts

See merge request bec/bec!68 ([`eab7072`](https://gitlab.psi.ch/bec/bec/-/commit/eab7072de6804c44b9617c2897d2a9ecc33b56e5))

* added list scripts function ([`a89ebf1`](https://gitlab.psi.ch/bec/bec/-/commit/a89ebf14208bf89b6abc6ba848008f91813ee0d0))

* added pyepics; added option to load /remove single script files ([`3a05e65`](https://gitlab.psi.ch/bec/bec/-/commit/3a05e6582ec6462f36ddf93c4a38c873d72a8914))

* added user functions for loading and removing scripts ([`69f58d7`](https://gitlab.psi.ch/bec/bec/-/commit/69f58d7db19466c1987e5b8aff324d3605197630))

* Merge branch &#39;config_reload&#39; into &#39;master&#39;

Config reload

See merge request bec/bec!66 ([`bf40543`](https://gitlab.psi.ch/bec/bec/-/commit/bf405438d0745935b064e9afe4246be5b068a7f3))

* Merge branch &#39;master&#39; into config_reload ([`0819920`](https://gitlab.psi.ch/bec/bec/-/commit/0819920b9dee7eb51f81ea5cb942939bcd702ea5))

* Merge branch &#39;client_renaming&#39; into &#39;master&#39;

renamed BKClient to BECClient

See merge request bec/bec!65 ([`db6babe`](https://gitlab.psi.ch/bec/bec/-/commit/db6babe4e55e19c0a45605d5334a1d9e6c64789d))

* fixed bug in live_table ([`988ab8b`](https://gitlab.psi.ch/bec/bec/-/commit/988ab8bac283b92d0b0f8d19c9e901790920a146))

* renamed BKClient to BECClient ([`650e5ba`](https://gitlab.psi.ch/bec/bec/-/commit/650e5baf9fd018567f06973a72b7c7bfa8122682))

* Merge branch &#39;global_var&#39; into &#39;master&#39;

added report on existing global variables

See merge request bec/bec!64 ([`c3ec629`](https://gitlab.psi.ch/bec/bec/-/commit/c3ec629e1374f2505fdf34df25868ba27e3b8282))

* added report on existing global variables ([`b376a07`](https://gitlab.psi.ch/bec/bec/-/commit/b376a075b37280f7ab2049f6d0603279fc254a38))

* Merge branch &#39;lamni_align&#39; into &#39;master&#39;

Lamni align

See merge request bec/bec!63 ([`67d7d12`](https://gitlab.psi.ch/bec/bec/-/commit/67d7d1278b1ac9015225387ff38358fa2053a1c3))

* bug fix ([`10d384d`](https://gitlab.psi.ch/bec/bec/-/commit/10d384dd17a22b99496e562b4302e983ba990e3b))

* updated align script with file writing ([`66fb146`](https://gitlab.psi.ch/bec/bec/-/commit/66fb1465cdde5fb625f606f024ccd74d96381caa))

* online bug fixes ([`2627046`](https://gitlab.psi.ch/bec/bec/-/commit/26270467d0843dbac1f8baf51cda003f775fc468))

* formatter ([`31e06d4`](https://gitlab.psi.ch/bec/bec/-/commit/31e06d481f6a676dae1795fed08afc9096ed55ac))

* x-ray-eye updates ([`a2146c1`](https://gitlab.psi.ch/bec/bec/-/commit/a2146c13160fc9eadb39dab7931b549b2218bcfd))

* Merge branch &#39;config_updates&#39; into &#39;master&#39;

Config updates response; closes #56

Closes #56

See merge request bec/bec!62 ([`ad2efa4`](https://gitlab.psi.ch/bec/bec/-/commit/ad2efa47587e4d2852996f9f16cc7c5fcaf4cc9c))

* fixed import ([`875cbf7`](https://gitlab.psi.ch/bec/bec/-/commit/875cbf77a10c59ed0dad304c9b1cda9e46b7d991))

* resolved test file conflict ([`4a53eb0`](https://gitlab.psi.ch/bec/bec/-/commit/4a53eb0dc94b4f9f2b58d8c1fc3a695189d2b4af))

* added more device manager tests ([`a88b66b`](https://gitlab.psi.ch/bec/bec/-/commit/a88b66b1c6431084f80f42daa0737d6f128e584e))

* added device manager tests ([`669d852`](https://gitlab.psi.ch/bec/bec/-/commit/669d852fb5f692b0321ceb8825df12585d11cb6c))

* dm cleanup ([`0bcd198`](https://gitlab.psi.ch/bec/bec/-/commit/0bcd198b39d56d97c1b3ef364dbe1104a7c2d047))

* added missing test file ([`fbe53f3`](https://gitlab.psi.ch/bec/bec/-/commit/fbe53f3177bf7b26161c1bf800967be0ddbde6e1))

* added more scibec tests ([`dbfe703`](https://gitlab.psi.ch/bec/bec/-/commit/dbfe703a2c0e4b043cdaa84358b83f8bae8425ba))

* improved service status updates ([`c4c08b8`](https://gitlab.psi.ch/bec/bec/-/commit/c4c08b8a2f44adb8d0196ef55e7f8f83b6100d36))

* bug fixes ([`2eb7424`](https://gitlab.psi.ch/bec/bec/-/commit/2eb7424806532c69d935793079f87d31d2712948))

* bug fix ([`a198875`](https://gitlab.psi.ch/bec/bec/-/commit/a198875b1aa3f26a07c0f1fd8d5fbc0feb647f8c))

* added demo_config ([`0d02d8d`](https://gitlab.psi.ch/bec/bec/-/commit/0d02d8dc3ce044a1ffde5b716bc7e39f884b46c5))

* fixed bug in scibec ([`02bb44f`](https://gitlab.psi.ch/bec/bec/-/commit/02bb44f46d550387920687c35b0003adbbd09236))

* changes to scibec init ([`84944ca`](https://gitlab.psi.ch/bec/bec/-/commit/84944cac4823135fd7e17c6e7906064aee50b68c))

* fixed tests ([`2474cc7`](https://gitlab.psi.ch/bec/bec/-/commit/2474cc7ff6bc25468cc008f85692a901a0da455e))

* bug fixes related to new config ([`4c84377`](https://gitlab.psi.ch/bec/bec/-/commit/4c843776048fa85d0f5bd24bf379051feb4604ce))

* updated tests to work with new config ([`2246a7c`](https://gitlab.psi.ch/bec/bec/-/commit/2246a7c46eaebe10aa46d044e43dfc779ba32538))

* refactored config creation ([`921fa10`](https://gitlab.psi.ch/bec/bec/-/commit/921fa1021dbabab655e968281955d9d8fefe6eaf))

* updated svg ([`b088a69`](https://gitlab.psi.ch/bec/bec/-/commit/b088a6950704fcd52ba47fc290765dfb647e135b))

* added svg file ([`65dd385`](https://gitlab.psi.ch/bec/bec/-/commit/65dd385ca8a107dd4a4310fd531f2a0c141a9a27))

* added missing scibec files ([`2696511`](https://gitlab.psi.ch/bec/bec/-/commit/2696511de05aef5dae8209b0342290f69a27b140))

* added missing session_manager ([`df66506`](https://gitlab.psi.ch/bec/bec/-/commit/df665066670076b27c259db38853097e05a31b8d))

* updated db drawing ([`017dfe5`](https://gitlab.psi.ch/bec/bec/-/commit/017dfe57059874b7aadd9d430020cbcc9e432d77))

* added db architecture drawing ([`4c98303`](https://gitlab.psi.ch/bec/bec/-/commit/4c98303850e333b45a747f88d18b9ed354bbca08))

* added option to reload the config; restructure of the db model ([`8cb2f0c`](https://gitlab.psi.ch/bec/bec/-/commit/8cb2f0c30b9f2985a4f6345f04a256f18b4f53b5))

* added x-ray-eye-align script ([`64763d0`](https://gitlab.psi.ch/bec/bec/-/commit/64763d03e8fceb5ead8a79e17f6d20fc54acab3c))

* added lamni_move_to_center scan ([`1116ba9`](https://gitlab.psi.ch/bec/bec/-/commit/1116ba92a50ebf91ddbe7c3e708a65e2e2013097))

* fixed test for request response ([`3ddbd87`](https://gitlab.psi.ch/bec/bec/-/commit/3ddbd87ac63fae43ed85457f16ad6195277f9bc3))

* added config handler test ([`44323dd`](https://gitlab.psi.ch/bec/bec/-/commit/44323ddf3b1ea467e26b993929d55b380c3cf2b0))

* fixed test ([`8058ac0`](https://gitlab.psi.ch/bec/bec/-/commit/8058ac001a326636c11eac980d170b1ec7746da6))

* added config_response message ([`4f068ce`](https://gitlab.psi.ch/bec/bec/-/commit/4f068ce42f114082c5be098562ea3570bf95a19a))

* fixed bug that caused rpc to fail silently ([`77728cd`](https://gitlab.psi.ch/bec/bec/-/commit/77728cd77b19160478953774e2a5b7e579023cb1))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

added enabled_set option

See merge request bec/bec!61 ([`979eada`](https://gitlab.psi.ch/bec/bec/-/commit/979eada2b21daeb602442881b13b690fe47458df))

* Merge branch &#39;master&#39; into online_changes ([`f40921d`](https://gitlab.psi.ch/bec/bec/-/commit/f40921dbcdd43005daa7ebe1fa958f3165049762))

* Merge branch &#39;lamni_disable_motors&#39; into &#39;master&#39;

redis global vars

See merge request bec/bec!59 ([`bb50fc6`](https://gitlab.psi.ch/bec/bec/-/commit/bb50fc6fea5676f17376b26580108f14939dce97))

* fixed tests ([`a4ca360`](https://gitlab.psi.ch/bec/bec/-/commit/a4ca36082bf4d6bb818202c073a16eb3c38e5207))

* fixed bug in global var ([`62b14cc`](https://gitlab.psi.ch/bec/bec/-/commit/62b14cc8d5d018b9e958cc813595c30d64e0f2f9))

* added global var methods to bec service ([`ba6fe4f`](https://gitlab.psi.ch/bec/bec/-/commit/ba6fe4fbad6d2bd77904607f9b85f09a62b39821))

* added enabled_set option ([`3d96d77`](https://gitlab.psi.ch/bec/bec/-/commit/3d96d776899630a2483301bd1ce013ec99688cbf))

* Merge branch &#39;lamni_disable_motors&#39; into &#39;master&#39;

Lamni disable motors

See merge request bec/bec!57 ([`62f3e4c`](https://gitlab.psi.ch/bec/bec/-/commit/62f3e4ceb69ced55e3738d637b999344be3e87ad))

* disabled lsamx / lsamy ([`a193c25`](https://gitlab.psi.ch/bec/bec/-/commit/a193c25b9399aa6b84f63f4e872621b6582bf8fc))

* cleanup ([`8f1becc`](https://gitlab.psi.ch/bec/bec/-/commit/8f1becc78c49f3b3e8cda5535866b26724fcfc38))

* Merge branch &#39;queue_repr&#39; into &#39;master&#39; ([`424456e`](https://gitlab.psi.ch/bec/bec/-/commit/424456e3c14a81d9d1bf5b261a67b419e6b5e8e4))

* added queue repr; closes #53 ([`50cd58f`](https://gitlab.psi.ch/bec/bec/-/commit/50cd58f7602e6e05079495a2ea9cb8b78ca71f4a))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

fixed bug that would leave the worker running on abortion

See merge request bec/bec!55 ([`ecc9a84`](https://gitlab.psi.ch/bec/bec/-/commit/ecc9a840ab1372538ef0972acb06c3a926ea3368))

* fixed bug that would leave the worker running on abortion ([`853a270`](https://gitlab.psi.ch/bec/bec/-/commit/853a2700c851ef6200bfb0697e65dff68b7144a0))

* Merge branch &#39;device_init&#39; into &#39;master&#39;

Device init

See merge request bec/bec!53 ([`3ae2c12`](https://gitlab.psi.ch/bec/bec/-/commit/3ae2c122e77095331c17dc48873ed46b1b851432))

* added test for unreachable devices ([`69fa7e1`](https://gitlab.psi.ch/bec/bec/-/commit/69fa7e1bc2228655cd2cb4c46aa2b8f7a205b15b))

* Merge branch &#39;callback_redesign&#39; into &#39;master&#39;

Callback refactor

See merge request bec/bec!52 ([`309c09e`](https://gitlab.psi.ch/bec/bec/-/commit/309c09e68b402979d3d9ec42ab37cf8b8d290291))

* renamed devicemanager to device_manager; added liveupdates ABC ([`7dc8f19`](https://gitlab.psi.ch/bec/bec/-/commit/7dc8f1965f39bcaa8ed433e5254f3cf8ed3eb7d1))

* excluded client unit tests from end2end tests ([`e7b9152`](https://gitlab.psi.ch/bec/bec/-/commit/e7b9152941272f00f06aa91608cb0115bd5e415e))

* refactored livetable ([`b8dac14`](https://gitlab.psi.ch/bec/bec/-/commit/b8dac14d6eb1fb6c962e4f0a87408f4dc0aed6b6))

* fixed test import bug ([`1d71859`](https://gitlab.psi.ch/bec/bec/-/commit/1d71859e9e15bf38600e045014f178cbf3288383))

* added missing test files ([`93c18fd`](https://gitlab.psi.ch/bec/bec/-/commit/93c18fdd54baa444d57d99d47b0eef7fc77e96fb))

* callback refactoring ([`93840a2`](https://gitlab.psi.ch/bec/bec/-/commit/93840a2f531ffb50718ba7f147cde85721df3753))

* refactored callbacks ([`2bb974d`](https://gitlab.psi.ch/bec/bec/-/commit/2bb974d9fe6047ec525c1f594e70ada3386523f0))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!54 ([`1ed3e60`](https://gitlab.psi.ch/bec/bec/-/commit/1ed3e605f129fadd40ce0b3572b350b180e71d99))

* Merge branch &#39;master&#39; into online_changes ([`940d5fa`](https://gitlab.psi.ch/bec/bec/-/commit/940d5fae7b5802fddba9ede9e3df3933c27c70bc))

* added doc string ([`beee979`](https://gitlab.psi.ch/bec/bec/-/commit/beee9799c18db021447910ab95a8263e5e737f41))

* Merge branch &#39;file_writer&#39; into &#39;master&#39;

File writer

See merge request bec/bec!49 ([`83dc71f`](https://gitlab.psi.ch/bec/bec/-/commit/83dc71f5889aae95cfcdd96ce9204126d681eaee))

* Merge branch &#39;file_writer&#39; of gitlab.psi.ch:bec/bec into file_writer ([`85ed31f`](https://gitlab.psi.ch/bec/bec/-/commit/85ed31ff18bc4879c388a2fcc651761d23f49fdd))

* Merge branch &#39;master&#39; into &#39;file_writer&#39;

# Conflicts:
#   .gitlab-ci.yml ([`f019c18`](https://gitlab.psi.ch/bec/bec/-/commit/f019c184daeb00b1a5e8c7396920f3e6a3734b3c))

* Merge branch &#39;master&#39; into file_writer ([`144e10d`](https://gitlab.psi.ch/bec/bec/-/commit/144e10d02a99f6182c59297869d664f7668eddf5))

* Merge branch &#39;queue_tests&#39; into &#39;master&#39;

queue cleanup and tests

See merge request bec/bec!51 ([`5c5860e`](https://gitlab.psi.ch/bec/bec/-/commit/5c5860e948c35f1fd35f638336b97c284ec1982b))

* added more scan tests ([`d38b308`](https://gitlab.psi.ch/bec/bec/-/commit/d38b30865fd6f020461352a9774564013cf04128))

* fixed merge-related bug ([`b32b385`](https://gitlab.psi.ch/bec/bec/-/commit/b32b385ece8dd0756040be533b004827ad7770b7))

* added more tests for scan positions ([`7f1619e`](https://gitlab.psi.ch/bec/bec/-/commit/7f1619e469693f989dda219c040f55444b85eb92))

* added pattern tests ([`94b08ef`](https://gitlab.psi.ch/bec/bec/-/commit/94b08ef2932508ef879990e8418018bc23aca191))

* Merge branch &#39;master&#39; into queue_tests ([`db49a00`](https://gitlab.psi.ch/bec/bec/-/commit/db49a00297353753a47cd18f3a6059dce259cdfd))

* Merge branch &#39;threaded_timeout&#39; into &#39;master&#39;

added singletonthreadpool and timeout decorator

See merge request bec/bec!50 ([`eff96c5`](https://gitlab.psi.ch/bec/bec/-/commit/eff96c5f133838b623da8222eb76984d3daec496))

* cleanup ([`a4a0f03`](https://gitlab.psi.ch/bec/bec/-/commit/a4a0f03de9f96fd2739821768cff8a2d8b97d46e))

* fixed typo in doc string ([`79ca802`](https://gitlab.psi.ch/bec/bec/-/commit/79ca8025f9d0e42c9a09406858455502418f92ed))

* added pre-scan-macro tests ([`feae112`](https://gitlab.psi.ch/bec/bec/-/commit/feae1124b5b2ddd29d64b03f10f2bea49b9d16b6))

* fixed bug in scan repeat ([`296136b`](https://gitlab.psi.ch/bec/bec/-/commit/296136b5f4e2ca97ff11a41759bad91f298ee6d0))

* renamed bkqueue to scan_queue ([`ea16ae6`](https://gitlab.psi.ch/bec/bec/-/commit/ea16ae6c8ddb87f2f34f7c1ed1a425745c444bd3))

* cleanup; added tests ([`9fa3595`](https://gitlab.psi.ch/bec/bec/-/commit/9fa35950cf67e64c90506769070b4b4c8157b25b))

* added bec_utils to pytest ([`e1d6b32`](https://gitlab.psi.ch/bec/bec/-/commit/e1d6b328c0bf6a76a27ea274f781ca2750b7dd81))

* added singletonthreadpool and timeout decorator ([`d152c46`](https://gitlab.psi.ch/bec/bec/-/commit/d152c4625625e61f5a3bc95074a25325caad40db))

* added end2end test for file writer; added file writer status message ([`5cea1c1`](https://gitlab.psi.ch/bec/bec/-/commit/5cea1c131e7632292440b34703c5832ffe06b005))

* fixed path to xml file ([`97e5bba`](https://gitlab.psi.ch/bec/bec/-/commit/97e5bba984bae09b0cf859148ecb11d16109b4d2))

* improved file writer tests ([`f27a8b2`](https://gitlab.psi.ch/bec/bec/-/commit/f27a8b20bb8c2973b4164985f75c4484df38aa79))

* updated dockerfile for file writer ([`5533cd8`](https://gitlab.psi.ch/bec/bec/-/commit/5533cd8aaf40fd07a679bdb9c9ff0528e1ae3271))

* added test dir ([`0f89a28`](https://gitlab.psi.ch/bec/bec/-/commit/0f89a28b1c993d992b7ca4b4977536e589edf4e4))

* added file writer ([`15f698f`](https://gitlab.psi.ch/bec/bec/-/commit/15f698f1b1d25e0d6faef129685f081e24fe3829))

* file writer update ([`1575a7a`](https://gitlab.psi.ch/bec/bec/-/commit/1575a7ad9b07823e8785d6c01cc241189f3298b4))

* added public_scan_baseline ([`24b3724`](https://gitlab.psi.ch/bec/bec/-/commit/24b3724fa55974fd9cb765868a8dc8d80c5c8a64))

* added baseline pub from scan bundler ([`44ef848`](https://gitlab.psi.ch/bec/bec/-/commit/44ef848375f1240af64b7621dd52fd4148825775))

* added ScanBaselineMessage ([`b723158`](https://gitlab.psi.ch/bec/bec/-/commit/b7231586fc4fcd8ec6eb68fdf0736e440407b84f))

* added scan stubs tests ([`cb47b2a`](https://gitlab.psi.ch/bec/bec/-/commit/cb47b2ab00bbca520c2c8a1b0fc78e5dbebfcc1c))

* fixed bug in scan stubs ([`1d33dec`](https://gitlab.psi.ch/bec/bec/-/commit/1d33dec62bf976e1e3ced55543d0ec5e40417c50))

* changed tolerance for galil ([`97b692a`](https://gitlab.psi.ch/bec/bec/-/commit/97b692a2a5e434fa02eb8901b9eec0af4a3ffc24))

* fixed bug in scan stubs ([`ff5cb72`](https://gitlab.psi.ch/bec/bec/-/commit/ff5cb72a99aadd345a67969a56f1008997e3700c))

* Fixed bug in config_handler init ([`913105d`](https://gitlab.psi.ch/bec/bec/-/commit/913105d721be35ebfd57fcbc6d768406950e03d6))

* fixed bug in devicemanager init ([`f2933bf`](https://gitlab.psi.ch/bec/bec/-/commit/f2933bf6ec8f96dbe58a10822b2730d6810f7a7a))

* added utils to coverage report ([`f76b135`](https://gitlab.psi.ch/bec/bec/-/commit/f76b1355edf11e335cb9c66eb567565c5dffaa21))

* Merge branch &#39;queue_reschedule&#39; into &#39;master&#39;

improved queue handling

See merge request bec/bec!47 ([`f43c91a`](https://gitlab.psi.ch/bec/bec/-/commit/f43c91a47ce9636f877bd3a0d43b1c0c70edd7da))

* bug fix ([`d7350c5`](https://gitlab.psi.ch/bec/bec/-/commit/d7350c506378575c5ad83c5af56a0f0e93673bce))

* added logger output to test ([`e11cc16`](https://gitlab.psi.ch/bec/bec/-/commit/e11cc16f7506eec0c824f10de56f61312602bdb5))

* replaced sleep time by wait until scan number is correct ([`c7f2b38`](https://gitlab.psi.ch/bec/bec/-/commit/c7f2b3868b6662b119bacca2b7e6f2d1ff9f7ef9))

* added sleep to ensure the scan number is updated ([`33b91c3`](https://gitlab.psi.ch/bec/bec/-/commit/33b91c3287784e51978732cb163db7283dd4c48d))

* bug fix ([`b8b618a`](https://gitlab.psi.ch/bec/bec/-/commit/b8b618a6c99c0d4ce7d7c82fb8165470722b5a85))

* added required kwarg relative ([`2abb293`](https://gitlab.psi.ch/bec/bec/-/commit/2abb293e1f8eb634f7a47a24e1917577c7a66e33))

* bug fix; added scan observer test without queue ([`d7c4b77`](https://gitlab.psi.ch/bec/bec/-/commit/d7c4b77dbd1becc69e222268feb7703263e6e1bc))

* Merge branch &#39;queue_reschedule&#39; of gitlab.psi.ch:bec/bec into queue_reschedule ([`ae87899`](https://gitlab.psi.ch/bec/bec/-/commit/ae878993845d4576940782a5c33361fc41b7f5c4))

* Merge branch &#39;master&#39; into &#39;queue_reschedule&#39;

# Conflicts:
#   bec_client/tests/end-2-end/test_scans.py ([`dc7acd6`](https://gitlab.psi.ch/bec/bec/-/commit/dc7acd69ef84f441cbbabdffd0d86e79960b58b3))

* Merge branch &#39;hli&#39; into &#39;master&#39;

added hli plugins; added spec hli; closes #49

Closes #49

See merge request bec/bec!46 ([`1044e34`](https://gitlab.psi.ch/bec/bec/-/commit/1044e34d82bf85f68fd647ed9da8d0f7ed3ff014))

* added hli plugins; added spec hli ([`a89cb57`](https://gitlab.psi.ch/bec/bec/-/commit/a89cb57e41ca2cb75be9628fdbb4d8e41afaff12))

* Merge branch &#39;mvr&#39; into &#39;master&#39;

added relative movements to umv and mv

See merge request bec/bec!45 ([`52011b7`](https://gitlab.psi.ch/bec/bec/-/commit/52011b784dd6d4038dfef8dfa69b6ee708ee37b6))

* added relative kwarg to all test scans ([`faf825d`](https://gitlab.psi.ch/bec/bec/-/commit/faf825da4a7e4eedaa85f0ba2362bbdd5f37a500))

* improved device repr ([`60cb47f`](https://gitlab.psi.ch/bec/bec/-/commit/60cb47fee1830b3a95e0169777050920664c29e2))

* Merge branch &#39;acquire&#39; into &#39;master&#39;

added acquire scan; closes #6

Closes #6

See merge request bec/bec!48 ([`2da6a0d`](https://gitlab.psi.ch/bec/bec/-/commit/2da6a0df0e63e09e933adec086ac3aa58e762c32))

* added acquire scan ([`cd1e320`](https://gitlab.psi.ch/bec/bec/-/commit/cd1e3207f063139126082d063e182037e83c97e2))

* minor improvements to scan abort test ([`864f4da`](https://gitlab.psi.ch/bec/bec/-/commit/864f4da58dee698a9d897a3f6567e01cf417cfb9))

* improvements for scan abort test ([`2a3ba9d`](https://gitlab.psi.ch/bec/bec/-/commit/2a3ba9d21ab39999661b36fb9754ec44f5c4bed6))

* minor improvements to device server ([`d7ed1e8`](https://gitlab.psi.ch/bec/bec/-/commit/d7ed1e820dc92511bf56d00e90fdd5fef5e0fdea))

* renamed repeat to restart ([`d51f095`](https://gitlab.psi.ch/bec/bec/-/commit/d51f095dc28a1ba25dff41299405f03f10ce7ddd))

* minor improvements to scan guard ([`524eb81`](https://gitlab.psi.ch/bec/bec/-/commit/524eb81b678309c694c32616096e5ae673c71d89))

* renamed repeat to restart; fixed for bug empty queues ([`c4090db`](https://gitlab.psi.ch/bec/bec/-/commit/c4090dbf82b4f74ac0a292eb56655827ca2cde44))

* renamed repeat to restart ([`86f1f8d`](https://gitlab.psi.ch/bec/bec/-/commit/86f1f8d6c897749e53722b877a620ed87f82070b))

* renamed repeat to restart ([`2479af5`](https://gitlab.psi.ch/bec/bec/-/commit/2479af5a15e2a1fb8e3cf04d88ae238fc212439b))

* added support for more advanced queue handling (repeat, insert at position) ([`40146bd`](https://gitlab.psi.ch/bec/bec/-/commit/40146bd067485446101d3909302fd52d1a9edb57))

* fixed fly scan positions generator ([`77786a0`](https://gitlab.psi.ch/bec/bec/-/commit/77786a01c0f63e49ae8c428f542eb14e49f37974))

* fixed wait; added req status for wait ([`5dd62f3`](https://gitlab.psi.ch/bec/bec/-/commit/5dd62f3b63db50561b49fedf6e133cc24ed0ec13))

* added relative movements to umv and mv ([`93bb4dc`](https://gitlab.psi.ch/bec/bec/-/commit/93bb4dc6c2b9b3593b6e4659fed033863cefeb68))

* added log messages for errors in scan guard ([`39f5878`](https://gitlab.psi.ch/bec/bec/-/commit/39f5878713bed91eb913926c04df25b58ecd17c9))

* changed dev.move to proper scan request ([`1ee461b`](https://gitlab.psi.ch/bec/bec/-/commit/1ee461b86e974ff39033b7483be62d1cfa459979))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes; closes #47

Closes #47

See merge request bec/bec!43 ([`81033b3`](https://gitlab.psi.ch/bec/bec/-/commit/81033b30c3b1d27b50e9b11c3b5cff71899c10f4))

* updated configs ([`b7536dc`](https://gitlab.psi.ch/bec/bec/-/commit/b7536dc65072174ac2176aab9ef054dd61a178c6))

* bug fix for signals ([`df7f936`](https://gitlab.psi.ch/bec/bec/-/commit/df7f93683af71290b8a3242553ffc0f75058e7a5))

* added stage test ([`2555c53`](https://gitlab.psi.ch/bec/bec/-/commit/2555c5329ff2729630cb3bb73ed96a673f4ad03b))

* added test placeholder ([`e54ef0c`](https://gitlab.psi.ch/bec/bec/-/commit/e54ef0c63fba1c082bdfd2e2bc452ef75ca41f08))

* refactoring; added test for device connection ([`d556ed9`](https://gitlab.psi.ch/bec/bec/-/commit/d556ed9c50530e73ccdd9479fa4ef4f4b1df539f))

* Merge branch &#39;master&#39; into online_changes ([`0b89974`](https://gitlab.psi.ch/bec/bec/-/commit/0b8997434f5d963edc167fece9947589130549c6))

* Merge branch &#39;scan_number&#39; into &#39;master&#39;

Scan number

See merge request bec/bec!44 ([`dbead68`](https://gitlab.psi.ch/bec/bec/-/commit/dbead680a5b97f00efdb0a73975573560ceee1a4))

* fixed bug in assertion ([`6ce6633`](https://gitlab.psi.ch/bec/bec/-/commit/6ce6633f8ac626af7a1141777580bcb5fbe411ed))

* added timeout to bec services ([`df3fa75`](https://gitlab.psi.ch/bec/bec/-/commit/df3fa75da670df588b34c4594fd8ad38b0070cb4))

* ensured that scan abortion is sent after pause ([`8b675e0`](https://gitlab.psi.ch/bec/bec/-/commit/8b675e08ff0a8e45ffc0a76f7a2ac1b623bf31ce))

* added logger info to scan modifications ([`19032c5`](https://gitlab.psi.ch/bec/bec/-/commit/19032c504485e178b8b154cba59dde982da05b62))

* added logger to thread exceptions ([`a91810c`](https://gitlab.psi.ch/bec/bec/-/commit/a91810c04d2a89af4cfc3bc8caf72a752e5d4da4))

* thread safety ([`025c36a`](https://gitlab.psi.ch/bec/bec/-/commit/025c36a56ebd6b08df0278674c5941ba11c11b58))

* fixed bug in config handler init ([`9116028`](https://gitlab.psi.ch/bec/bec/-/commit/9116028a8d5a87487c8e78fdfcd6b23b99d874a6))

* fixed bug in client callback ([`452ee1f`](https://gitlab.psi.ch/bec/bec/-/commit/452ee1f26cf11a80b33b4e45c059b041bf7844f2))

* fixed test ([`3561936`](https://gitlab.psi.ch/bec/bec/-/commit/35619361b70d746f13b357d7d161998f85f6b0cf))

* get the current scan queue info from redis ([`d5c2be6`](https://gitlab.psi.ch/bec/bec/-/commit/d5c2be6bf3005299fff80b3f527dcdd83525fbff))

* fixed test ([`c7e6233`](https://gitlab.psi.ch/bec/bec/-/commit/c7e623301b29031953c70a0f03d8b7645c93e6bb))

* fixed test ([`a3ecf7a`](https://gitlab.psi.ch/bec/bec/-/commit/a3ecf7a91eddec1b4503a5220bf4c8496bbf07ad))

* ensure that only existing storage units are removed ([`ef01f03`](https://gitlab.psi.ch/bec/bec/-/commit/ef01f03bcfac6201821370a4dceb18fdb957649c))

* abort scan test ([`405ef35`](https://gitlab.psi.ch/bec/bec/-/commit/405ef35788aea91c3a48b10cf51ca357cf79d7bc))

* scan number prediction ([`b2b7502`](https://gitlab.psi.ch/bec/bec/-/commit/b2b7502f734b07d161a8a7cc22b95ad2add068e5))

* scan number prediction ([`0907aa5`](https://gitlab.psi.ch/bec/bec/-/commit/0907aa59cbff20e265c0a0f7686061fa6837d752))

* added checks to tests to ensure that the scan number is correct ([`187cb41`](https://gitlab.psi.ch/bec/bec/-/commit/187cb4110a882c820cfd152963f6453ebbaff23b))

* added current scan number property to scan manager ([`1f39b8b`](https://gitlab.psi.ch/bec/bec/-/commit/1f39b8b7f5d129cd217782b2646b13cacb3006ed))

* prel commit for scan number prediction ([`cb324cb`](https://gitlab.psi.ch/bec/bec/-/commit/cb324cb1a916fa7269372371e884ed27c2f922e1))

* black ([`8d25960`](https://gitlab.psi.ch/bec/bec/-/commit/8d25960b143c2f9d5463434100cc63a75d2e437b))

* Merge branch &#39;online_changes&#39; of https://gitlab.psi.ch/bec/bec into online_changes ([`beea576`](https://gitlab.psi.ch/bec/bec/-/commit/beea5763f1a0da31346e473cef4904a84cdc0879))

* fixed device msg type error ([`dad7d02`](https://gitlab.psi.ch/bec/bec/-/commit/dad7d02155d46695a0e9e9b7e746ff76c9ab7c91))

* added scan guard tests ([`b9344cc`](https://gitlab.psi.ch/bec/bec/-/commit/b9344cc36647d9eee9a74cc15025b2015b8736f5))

* refactoring ([`aec8c0d`](https://gitlab.psi.ch/bec/bec/-/commit/aec8c0d18bee05762f0a76d433c13054519440e3))

* added scan worker tests ([`9970b10`](https://gitlab.psi.ch/bec/bec/-/commit/9970b10ad9ad5162462aebd030569a7ea77e7c73))

* fixed bug in device_server instructions ([`f63cf0d`](https://gitlab.psi.ch/bec/bec/-/commit/f63cf0d78f366433c9bc287761ca9f7b87597086))

* bug fix for failed movements ([`cfd854d`](https://gitlab.psi.ch/bec/bec/-/commit/cfd854d083fd7f43ac06f2bee71024d3c8badca3))

* bug fix for device lists ([`c876e19`](https://gitlab.psi.ch/bec/bec/-/commit/c876e19eb747cbbabf2b51cd12e8f44c38da105a))

* fixed bug in controller init; added sub to signals ([`ffbdf20`](https://gitlab.psi.ch/bec/bec/-/commit/ffbdf205d0b7a16aceefeee9a3c83607e93d972e))

* added support for kwargs of EpicsSignalBase ([`bf848e2`](https://gitlab.psi.ch/bec/bec/-/commit/bf848e2c3ee2faa91fafd3586bfd4553f7e99bc3))

* Merge branch &#39;revert-aa1f3dcd&#39; into &#39;master&#39;

Revert &#34;Merge branch &#39;revert-a1ead9b6&#39; into &#39;master&#39;&#34;

See merge request bec/bec!41 ([`2f7558f`](https://gitlab.psi.ch/bec/bec/-/commit/2f7558f6b52b0097d793938260740b065e63df7f))

* bug fix for basic requests ([`a7f40fe`](https://gitlab.psi.ch/bec/bec/-/commit/a7f40fec9c48ade9705cec707ba5d31407b325de))

* added scan_items test ([`95c5c99`](https://gitlab.psi.ch/bec/bec/-/commit/95c5c99bf2486c9308f506691e854c7111ef935d))

* fixed test for new abort handling ([`551b1d7`](https://gitlab.psi.ch/bec/bec/-/commit/551b1d7bd0b6255ff98657f992a730bf673f4ce6))

* changed abort handling; now within the instruction loop to avoid clearing the queue ([`89f2eb2`](https://gitlab.psi.ch/bec/bec/-/commit/89f2eb2503990cf9515896c5b29eecde7c4edad0))

* Revert &#34;Merge branch &#39;revert-a1ead9b6&#39; into &#39;master&#39;&#34;

This reverts merge request !40 ([`43681f9`](https://gitlab.psi.ch/bec/bec/-/commit/43681f96bab00097825ff12f822dd6c774a8190c))

* Merge branch &#39;revert-a1ead9b6&#39; into &#39;master&#39;

Revert &#34;Merge branch &#39;cleanup_after_stop&#39; into &#39;master&#39;&#34;

See merge request bec/bec!40 ([`aa1f3dc`](https://gitlab.psi.ch/bec/bec/-/commit/aa1f3dcd1a4af31edf0076805035e9673374ea91))

* Revert &#34;Merge branch &#39;cleanup_after_stop&#39; into &#39;master&#39;&#34;

This reverts merge request !39 ([`09bd00a`](https://gitlab.psi.ch/bec/bec/-/commit/09bd00a40529daef269e3c5595bf316e3f1dabd7))

* Merge branch &#39;cleanup_after_stop&#39; into &#39;master&#39;

cleanup after stop

See merge request bec/bec!39 ([`a1ead9b`](https://gitlab.psi.ch/bec/bec/-/commit/a1ead9b658f60d51747981bb92e81e2bed9d2769))

* tests ([`c8525ae`](https://gitlab.psi.ch/bec/bec/-/commit/c8525ae8115ff9270998dc654e568d907e00171d))

* fixed abort test ([`6c9dbd4`](https://gitlab.psi.ch/bec/bec/-/commit/6c9dbd41c27435175d2b38e27cc7d9a36ff22b74))

* cleanup after stop ([`e923488`](https://gitlab.psi.ch/bec/bec/-/commit/e9234888f3564fda4bde6666113e476fc51e4197))

* Merge branch &#39;detector_sim&#39; into &#39;master&#39;

detector sim

See merge request bec/bec!38 ([`ba962fc`](https://gitlab.psi.ch/bec/bec/-/commit/ba962fc49beb6eb504c0eeb7f3c8fd0f16565bc8))

* re-enabled detector sim ([`a45271f`](https://gitlab.psi.ch/bec/bec/-/commit/a45271f6d321418bff00cc6ee686322c68bd2323))

* Merge branch &#39;service_status&#39; into &#39;master&#39;

changes to ensure that services are unique and only launched once

See merge request bec/bec!37 ([`de94934`](https://gitlab.psi.ch/bec/bec/-/commit/de9493407b1160374c9477a38a1d48f676932f1a))

* created keys method for redis connector; fixed tests ([`134e758`](https://gitlab.psi.ch/bec/bec/-/commit/134e758eee8f6861f7d26e7b6334fcad755b22e5))

* changes to ensure that services are unique and only launched once ([`f9e9a3b`](https://gitlab.psi.ch/bec/bec/-/commit/f9e9a3b68bfd92e74495ac7c7b5414554f0c3c1e))

* Merge branch &#39;redis_buffer&#39; into &#39;master&#39;

Redis buffer for public data

See merge request bec/bec!36 ([`989dab5`](https://gitlab.psi.ch/bec/bec/-/commit/989dab58cd39b85959dcb3d7c55f654fdbd5d567))

* introduced a buffer for public data with a default expiration time of 30 min ([`5d6fd32`](https://gitlab.psi.ch/bec/bec/-/commit/5d6fd329815652975e921f13863b1d850d429935))

* Merge branch &#39;scan_server_tests&#39; into &#39;master&#39;

simplified scan_server test

See merge request bec/bec!35 ([`c89094c`](https://gitlab.psi.ch/bec/bec/-/commit/c89094c622be4d9f39edb18df642dc46151a4ba6))

* simplified scan_server test ([`b45bebb`](https://gitlab.psi.ch/bec/bec/-/commit/b45bebba80871b59715d11f81a1a898e3e926d31))

* Merge branch &#39;scan_server_tests&#39; into &#39;master&#39;

fixed typo in gitlab-ci

See merge request bec/bec!34 ([`30ea97a`](https://gitlab.psi.ch/bec/bec/-/commit/30ea97ae948b4f8ff25d18fa55970508149f8c28))

* fixed typo ([`865b120`](https://gitlab.psi.ch/bec/bec/-/commit/865b120e9e90e520ab90524fb15e2ba2c40eb430))

* Merge branch &#39;scan_server_tests&#39; into &#39;master&#39;

added more scan worker tests

See merge request bec/bec!33 ([`d315ca4`](https://gitlab.psi.ch/bec/bec/-/commit/d315ca40e7f9eea5fd7501226d1334ad4b8f0c11))

* fixed bug in producer mock ([`481d86d`](https://gitlab.psi.ch/bec/bec/-/commit/481d86d491362f6f8ca216a51b5c7ecec6e9690e))

* added more scan worker tests ([`65c99a6`](https://gitlab.psi.ch/bec/bec/-/commit/65c99a6dfe83d031c491203d385343927241241a))

* Merge branch &#39;trigger&#39; into &#39;master&#39;

detector trigger

See merge request bec/bec!32 ([`28f9b99`](https://gitlab.psi.ch/bec/bec/-/commit/28f9b99cf665d61412f47bc98b20173f26f2fbbc))

* added scan bundler test ([`595adc3`](https://gitlab.psi.ch/bec/bec/-/commit/595adc3fa72e09a0b82da98d8779623d64630e7a))

* re-enabled trigger ([`6b94747`](https://gitlab.psi.ch/bec/bec/-/commit/6b94747d98b19acbf9c92b89002bfea17c31f165))

* Merge branch &#39;scan_status&#39; into &#39;master&#39;

coverage

See merge request bec/bec!31 ([`c4dcda2`](https://gitlab.psi.ch/bec/bec/-/commit/c4dcda27f664a95aab5da2471c6309e353d89118))

* Update .gitlab-ci.yml ([`7e2805e`](https://gitlab.psi.ch/bec/bec/-/commit/7e2805e5930a9d505206870f8bca0b04083fbc22))

* code cov ([`44ba6a9`](https://gitlab.psi.ch/bec/bec/-/commit/44ba6a919f04f870ce0a3eca22bf16f56967cafc))

* combined tests ([`8385d3f`](https://gitlab.psi.ch/bec/bec/-/commit/8385d3fd4de7f87124bb616c8f3abd16f517e7b7))

* combined tests ([`e44075f`](https://gitlab.psi.ch/bec/bec/-/commit/e44075f17b06a3fc0e4c479f82ffe207ecd3611b))

* Merge branch &#39;scan_status&#39; into &#39;master&#39;

scan status; closes #33; closes #34; closes #45

Closes #45, #34, and #33

See merge request bec/bec!30 ([`8394387`](https://gitlab.psi.ch/bec/bec/-/commit/8394387c0c91bde39550ea884865e06f78529ecd))

* queue history and status items ([`6fed767`](https://gitlab.psi.ch/bec/bec/-/commit/6fed7674f2c173c90b978070b4d2bca931b3927d))

* cleanup ([`4c82c63`](https://gitlab.psi.ch/bec/bec/-/commit/4c82c63c0992bf896b0f7c47d1c5024ea1755acb))

* removed queue items are now append to a redis list ([`ee81c9a`](https://gitlab.psi.ch/bec/bec/-/commit/ee81c9a233dd8af4efea431951a316e7e5942363))

* removed queue items are now append to a redis list ([`de252ab`](https://gitlab.psi.ch/bec/bec/-/commit/de252ab0214240d6e77d45cee79e1f9241fcf0ef))

* added scan queue history ([`c866752`](https://gitlab.psi.ch/bec/bec/-/commit/c8667522bca5b059f8d9b84477ddd3d6318b3ecf))

* fixed ci log path for client ([`76d7375`](https://gitlab.psi.ch/bec/bec/-/commit/76d737513487179535cc2c2929eac7f00dd9ee1a))

* Merge branch &#39;client_improvements&#39; into &#39;master&#39;

client improvements

See merge request bec/bec!29 ([`8101851`](https://gitlab.psi.ch/bec/bec/-/commit/8101851c513ff8ab752dd702a3ced13903d6c5ff))

* minor changes to config handler ([`38f3036`](https://gitlab.psi.ch/bec/bec/-/commit/38f3036a945239a9083e819350880fc8974bdebc))

* client improvements ([`18da798`](https://gitlab.psi.ch/bec/bec/-/commit/18da7987fab243396c00f7d89129c042a71e6694))

* Merge branch &#39;config_handler&#39; into &#39;master&#39;

Config handler

See merge request bec/bec!28 ([`31743cd`](https://gitlab.psi.ch/bec/bec/-/commit/31743cd90acdfc9aa0687ced7064849d254b86c4))

* Merge branch &#39;scan_bundler_fix&#39; into config_handler ([`06c72aa`](https://gitlab.psi.ch/bec/bec/-/commit/06c72aa3bd068c2aaa2f1a37db3455d2e52de2f0))

* changed for config_handler ([`c8008bf`](https://gitlab.psi.ch/bec/bec/-/commit/c8008bf3d01f3f6a414156aa4b6d79eebf229d6c))

* added config_handler ([`ae1d8d9`](https://gitlab.psi.ch/bec/bec/-/commit/ae1d8d91d4df1c83143472fef6b328e01a024434))

* Merge branch &#39;scan_bundler_fix&#39; into &#39;master&#39;

Scan bundler fix

See merge request bec/bec!27 ([`e2eabe6`](https://gitlab.psi.ch/bec/bec/-/commit/e2eabe69e178788fb4e8ace455f9c307f3c3de46))

* added client log as artifact ([`4b115ba`](https://gitlab.psi.ch/bec/bec/-/commit/4b115baed3dca08b7f25869d6063014c869205cc))

* changed logger config for client with different log levels for each sink ([`2174291`](https://gitlab.psi.ch/bec/bec/-/commit/21742915817bf017f2a78fb736cce528bf2d9ddc))

* logger refactoring ([`a59c6e1`](https://gitlab.psi.ch/bec/bec/-/commit/a59c6e139bb74ce88137228fc42a156fb38a2ac6))

* added logger output for scan segments to client ([`027d6ca`](https://gitlab.psi.ch/bec/bec/-/commit/027d6ca2ef6956b93eb7cf03137c14a040f92521))

* bug fix for scan_bundler ([`8d822e6`](https://gitlab.psi.ch/bec/bec/-/commit/8d822e6d9411686624949aa6e3426371aab49321))

* changed to abs path ([`35d1bca`](https://gitlab.psi.ch/bec/bec/-/commit/35d1bca989552d2c4cd6960eebc6d63190a23b27))

* changed to ophyd devices env var ([`ef19877`](https://gitlab.psi.ch/bec/bec/-/commit/ef198779a4c7f86b2273085bd9e7010a0eaeb967))

* added OPHYD_DEVICES_PATH ([`b0f8c88`](https://gitlab.psi.ch/bec/bec/-/commit/b0f8c88e5b89c08703380d699df4dfabe6d19579))

* install ophyd_devices in parent directory ([`c014614`](https://gitlab.psi.ch/bec/bec/-/commit/c014614c9fa2cc67a23380781fa6441d79d3dff2))

* install ophyd_devices in parent directory ([`433c2f0`](https://gitlab.psi.ch/bec/bec/-/commit/433c2f0b8df0ca8c92b820b4e86266c12cec2ff5))

* added ophyd_devices to ci test ([`910a9b3`](https://gitlab.psi.ch/bec/bec/-/commit/910a9b350eb7717ed82cee1b3ced13855ead3ce6))

* added device_server tests to ci ([`65a62b1`](https://gitlab.psi.ch/bec/bec/-/commit/65a62b19a379e24b51e5325fd4d38fd54cb708b9))

* added device init test ([`8505e55`](https://gitlab.psi.ch/bec/bec/-/commit/8505e551983b5cf0ccf076cc33601a073fa78af0))

* Merge branch &#39;scan_bundler_fix&#39; into &#39;master&#39;

fixed bug in device init

See merge request bec/bec!26 ([`c8d318e`](https://gitlab.psi.ch/bec/bec/-/commit/c8d318eb79825cc15f63cc770a7356916b81f7b3))

* fixed bug in device init ([`666788d`](https://gitlab.psi.ch/bec/bec/-/commit/666788d54ba9bd030ef478772c92989d1314d263))

* Merge branch &#39;scan_bundler_fix&#39; into &#39;master&#39;

scan bundler fix

See merge request bec/bec!25 ([`d19a4fc`](https://gitlab.psi.ch/bec/bec/-/commit/d19a4fcd1db0381a1a45fe65f8a6bb4a470e89ed))

* removed eiger for now ([`0681d80`](https://gitlab.psi.ch/bec/bec/-/commit/0681d80998d08f3e4361c7376dcf9d8f8ed28c0f))

* disabled trigger ([`3988540`](https://gitlab.psi.ch/bec/bec/-/commit/39885403609a6a881d0704dafd02634f26fa84dd))

* disabled staging ([`1402de4`](https://gitlab.psi.ch/bec/bec/-/commit/1402de4c6220ae0acbddb5fe219633a1137f6ee2))

* fixed callback ([`c48e379`](https://gitlab.psi.ch/bec/bec/-/commit/c48e379e858424f5aced0a92fe03582e5876d758))

* debugging ([`956a1c7`](https://gitlab.psi.ch/bec/bec/-/commit/956a1c7c415de678ce8fbd3465358410fb5cb535))

* debugging ([`11f970c`](https://gitlab.psi.ch/bec/bec/-/commit/11f970cdd0ad54b4b8f06565b6a64bdd5ed8f17d))

* added scan_status_list; improvements for scan_bundler ([`0d6ff4e`](https://gitlab.psi.ch/bec/bec/-/commit/0d6ff4e487f1d33475368c8b7903d2270d4c7463))

* bug fix ([`8e8902d`](https://gitlab.psi.ch/bec/bec/-/commit/8e8902d4b169fe7880aa040a2a90e7511b456247))

* reduced timeout time ([`795920c`](https://gitlab.psi.ch/bec/bec/-/commit/795920ccf8ba2b22bb3ecc15382c2be7c10b515b))

* added more logging ([`8ae4208`](https://gitlab.psi.ch/bec/bec/-/commit/8ae4208553e970d6d3d6c17de91b218844b1e68e))

* added cleanup for unstaging ([`4ef8ba3`](https://gitlab.psi.ch/bec/bec/-/commit/4ef8ba35d767e6c1ad322e1b95bb44aea49545ce))

* ensured that devices are always unstaged before staging ([`5e94973`](https://gitlab.psi.ch/bec/bec/-/commit/5e94973f89c430dd57f9d2a25ecd39d28862b250))

* added detector sim to test config ([`f4ff599`](https://gitlab.psi.ch/bec/bec/-/commit/f4ff5991b8625e1f49862af5aa20fa0bbd1030fd))

* added device access to detector sims ([`9dd944f`](https://gitlab.psi.ch/bec/bec/-/commit/9dd944fc093f88c02242640140437140fc973659))

* added stage and unstage ([`2239ce9`](https://gitlab.psi.ch/bec/bec/-/commit/2239ce9aa9014c5223d385bdea3e4c957402301a))

* instead of staging, controller devices are now checked for controller.on methods; cleanup ([`99cfdaf`](https://gitlab.psi.ch/bec/bec/-/commit/99cfdafeb4e16191ce2930d0ce10638e994fe72a))

* added stage and unstage to the device server ([`0aa8ff0`](https://gitlab.psi.ch/bec/bec/-/commit/0aa8ff02f064c32e060c5d157274da7085c928aa))

* removed detectors from baseline devices ([`bf4bd5a`](https://gitlab.psi.ch/bec/bec/-/commit/bf4bd5ab254429051ec2070b2409d5eae3227b9b))

* cleanup ([`f793545`](https://gitlab.psi.ch/bec/bec/-/commit/f793545433ed3c3b99926e3caf05a84b5aaf0f27))

* added eiger detector ([`a6e2510`](https://gitlab.psi.ch/bec/bec/-/commit/a6e25105cee6790e8e26d1a820d2366bdcb4bbe1))

* added device trigger ([`db87997`](https://gitlab.psi.ch/bec/bec/-/commit/db879972cc24255f140cc8c01637af639d90689b))

* improved trigger handling ([`a1d8ce2`](https://gitlab.psi.ch/bec/bec/-/commit/a1d8ce2c4b6b960ede06989b2842b6156b753bd0))

* cleanup ([`71818a0`](https://gitlab.psi.ch/bec/bec/-/commit/71818a0b15df3f1921a15ad0d345a42d500bfc6d))

* moved to async sink ([`cf1b43b`](https://gitlab.psi.ch/bec/bec/-/commit/cf1b43b6ec88e117fe805e78418ce7407c97a7bc))

* added detectors query; added doc strings ([`131bac6`](https://gitlab.psi.ch/bec/bec/-/commit/131bac60c468b870ba11e22ffeed473d46c49c75))

* moved scan number to redis; closes #23 ([`0c37391`](https://gitlab.psi.ch/bec/bec/-/commit/0c37391794b2d094d5a139ef2d6def92d544dc68))

* added scan_number endpoint ([`cbad2c9`](https://gitlab.psi.ch/bec/bec/-/commit/cbad2c9bffa232fc8531fdc2ebe95ad5adfb1150))

* renamed device_msg_mixin to scan_stubs ([`022c719`](https://gitlab.psi.ch/bec/bec/-/commit/022c71911b10d2ff82fa3ba3713443e845f1c421))

* Merge branch &#39;fly_scan_test&#39; into &#39;master&#39;

Fly scan test

Closes #44

See merge request bec/bec!24 ([`fd2254e`](https://gitlab.psi.ch/bec/bec/-/commit/fd2254e299a0a5de4a55f777d24096cb14da7809))

* added params to flyer ([`615ee4f`](https://gitlab.psi.ch/bec/bec/-/commit/615ee4f06be149b461165e9f7d82734435709905))

* added sim flyer to test config ([`416d46f`](https://gitlab.psi.ch/bec/bec/-/commit/416d46f62ced3ee2d1ec1561895a2fb9372468bf))

* added fly scan test; closes #44 ([`f2ecc0f`](https://gitlab.psi.ch/bec/bec/-/commit/f2ecc0f40fa40c698d71c6857ee4a84a0973065f))

* Merge branch &#39;scan_stubs&#39; into &#39;master&#39;

refactoring for scan / scan stubs

See merge request bec/bec!23 ([`e088da0`](https://gitlab.psi.ch/bec/bec/-/commit/e088da0ff4214e57d0bda97ff8a5ec5a95126587))

* bug fix for empty device list ([`6d496d7`](https://gitlab.psi.ch/bec/bec/-/commit/6d496d71530d1a468b900c7a7ace9081f78bb10a))

* added doc strings; removed target param ([`80b0b47`](https://gitlab.psi.ch/bec/bec/-/commit/80b0b4701dfd22c258c9e7f7cc7b78e01d99cbcf))

* ensured that either devices or device groups are used but not both ([`4884107`](https://gitlab.psi.ch/bec/bec/-/commit/4884107f2dbc02b3b97db5c48b1b4fcb5ac813fe))

* bug fixes; enforced kwargs ([`c0bc367`](https://gitlab.psi.ch/bec/bec/-/commit/c0bc3672674c5e5ee024c26d65d168f1d4017f79))

* added missing device_mixin ([`e70043f`](https://gitlab.psi.ch/bec/bec/-/commit/e70043fa40d088bed777c146561a6051e8980706))

* refactoring for scan / scan stubs ([`9646d68`](https://gitlab.psi.ch/bec/bec/-/commit/9646d6860de848b96264a3bcd508b8a7c2bbc895))

* artifacts upload on failure ([`9b31a68`](https://gitlab.psi.ch/bec/bec/-/commit/9b31a682317a3fcac1f509184254e4cf30fb32ac))

* added client tests to ci ([`00bc9e1`](https://gitlab.psi.ch/bec/bec/-/commit/00bc9e1b3968496e468e16b95155cde653038bfe))

* added scan_bundler test to ci ([`70d41e0`](https://gitlab.psi.ch/bec/bec/-/commit/70d41e069d0bd2732a4d7795598927657f5a4f52))

* added scan bundler test ([`e886e8e`](https://gitlab.psi.ch/bec/bec/-/commit/e886e8e599b67f994d25b1666b4a88bb74133de1))

* added threadlocks to alarm handler; added doc strings ([`e5eb71e`](https://gitlab.psi.ch/bec/bec/-/commit/e5eb71e1a9495776917d3c3dc598e2ccc408efc5))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`a17df89`](https://gitlab.psi.ch/bec/bec/-/commit/a17df89455230263785413b5a101fe27f44113b6))

* Update .gitlab-ci.yml ([`7254fff`](https://gitlab.psi.ch/bec/bec/-/commit/7254fffec76cc31fa847de9bec7822c2b9593058))

* Update .gitlab-ci.yml ([`e20d885`](https://gitlab.psi.ch/bec/bec/-/commit/e20d885f5169253ddad99ad532891defd05e64a8))

* Update .gitlab-ci.yml ([`d627471`](https://gitlab.psi.ch/bec/bec/-/commit/d627471cffc6fcd975becf45943460f2fba8fd8c))

* added timeout for scanID search ([`2bcb11c`](https://gitlab.psi.ch/bec/bec/-/commit/2bcb11c8dc619c9fdc1c0012afa8e139712d3d6a))

* added expiration time for job artifacts ([`392950f`](https://gitlab.psi.ch/bec/bec/-/commit/392950fa25b4359f0392c1ccd1ac4e345bccffd5))

* added log artifacts for scan_bundler and device_server ([`fe0aacb`](https://gitlab.psi.ch/bec/bec/-/commit/fe0aacb6c9be4bfbda8223824dc90b1fb31c94ad))

* fixed scan server image name ([`265ba1e`](https://gitlab.psi.ch/bec/bec/-/commit/265ba1e9ca2538a41bcfe8680070cdfddb0c836b))

* added scanserver artifact ([`1ea2de7`](https://gitlab.psi.ch/bec/bec/-/commit/1ea2de7c5b4057697f153e798aaa6e9a77512757))

* fixed typo in test ([`899a2f3`](https://gitlab.psi.ch/bec/bec/-/commit/899a2f3755dd1f867024bab32397638a27df7842))

* added tolerances to lamnifermattests ([`e1b5bb6`](https://gitlab.psi.ch/bec/bec/-/commit/e1b5bb670e3feaacf4a5bb13c42ffecfc2dc2fe7))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`4d56709`](https://gitlab.psi.ch/bec/bec/-/commit/4d56709687d20ca8207abddc2a69cd0ae3171bf4))

* Update docker-compose.yaml ([`9edd5ef`](https://gitlab.psi.ch/bec/bec/-/commit/9edd5efae6aaebb50a37002bfd9d26ae11bc190e))

* Update docker-compose.yaml ([`128a353`](https://gitlab.psi.ch/bec/bec/-/commit/128a353b0e13fbb130546c634e16afc82fd2023f))

* Update docker-compose.yaml ([`5f9170e`](https://gitlab.psi.ch/bec/bec/-/commit/5f9170e1f2fa9385a4decf380e109fd8ef7d292c))

* Update docker-compose.yaml ([`95eb835`](https://gitlab.psi.ch/bec/bec/-/commit/95eb835478c1774f26701e84b783837fc32b9ecf))

* Update docker-compose.yaml ([`abe3885`](https://gitlab.psi.ch/bec/bec/-/commit/abe3885a0af0c19a35fd7fc1076dd9014ce8c443))

* Update docker-compose.yaml ([`d4a8559`](https://gitlab.psi.ch/bec/bec/-/commit/d4a8559d9f782b753d415b2d5d4d7b1222e3aec7))

* Update .gitlab-ci.yml ([`39cd4f4`](https://gitlab.psi.ch/bec/bec/-/commit/39cd4f46a6e456f20f08d3bf54e398f185835457))

* added file logger ([`ba9f81b`](https://gitlab.psi.ch/bec/bec/-/commit/ba9f81b215e63ba2b4e2ab1a7ce60c606937ebf0))

* cleanup ([`4e412cf`](https://gitlab.psi.ch/bec/bec/-/commit/4e412cf236bfe0e1f89227189d2455645ccc3a5b))

* added lamni test ([`7a7b4b2`](https://gitlab.psi.ch/bec/bec/-/commit/7a7b4b2d4db1d3e14b121c1859f4102164b58621))

* cleanup ([`0546c4d`](https://gitlab.psi.ch/bec/bec/-/commit/0546c4db0be100cccbee1e6fd48c44b06bcb5c0c))

* cleanup ([`d63debf`](https://gitlab.psi.ch/bec/bec/-/commit/d63debfb058eb9845a4c7fc0a1e67379c67aa1f0))

* cleanup ([`8d4c21c`](https://gitlab.psi.ch/bec/bec/-/commit/8d4c21c339fbe0c6e72d66f8a1fd135d6e0e9bf2))

* cleanup ([`dce58d6`](https://gitlab.psi.ch/bec/bec/-/commit/dce58d699b0cc8852d21a88d0faadc566b30ae40))

* added sleep to after test client init ([`9ed7ff5`](https://gitlab.psi.ch/bec/bec/-/commit/9ed7ff55509867763fe796e3fc946133e4cd7b86))

* improved thread cleanup routines ([`aedffff`](https://gitlab.psi.ch/bec/bec/-/commit/aedffff9466b5fa1015e65d151d479ccc2a8505d))

* added threadlock decorator ([`33014f4`](https://gitlab.psi.ch/bec/bec/-/commit/33014f4fc2e8d4c2d7d1fb3b2d39579966a42da5))

* wait for queue init ([`9976f89`](https://gitlab.psi.ch/bec/bec/-/commit/9976f89b12769c671dbcc4b66c799f83dc96add0))

* fixed bug in end2end test ([`d875ee5`](https://gitlab.psi.ch/bec/bec/-/commit/d875ee59eb28b8864b0c4e725130112927003f9e))

* fixed bug in get_queue ([`2777417`](https://gitlab.psi.ch/bec/bec/-/commit/2777417cc84cfbf13f7e4f88816d1fe823f58d2a))

* added direct check to ensure queue is empty ([`8272cb2`](https://gitlab.psi.ch/bec/bec/-/commit/8272cb2ada357ec26e93e42ff829f13658f66128))

* make sure that scan_bundler waits to receive all devices for a point ([`158ec52`](https://gitlab.psi.ch/bec/bec/-/commit/158ec52fa0379614744d369658e153d7e34bbdf4))

* unified producermock ([`adaddf1`](https://gitlab.psi.ch/bec/bec/-/commit/adaddf1a76b2cefcf085bb18c8638ffacd9087a0))

* reverted config change for end2end tests ([`e3d650f`](https://gitlab.psi.ch/bec/bec/-/commit/e3d650f0b0057720de3573e2f36993cc7ad5e436))

* cleanup ([`1dd3099`](https://gitlab.psi.ch/bec/bec/-/commit/1dd309929c2a0ff30c38c890389938ccd5ba3afa))

* fixed connector mock ([`f5d29b8`](https://gitlab.psi.ch/bec/bec/-/commit/f5d29b85a509a89f3dc95cf70b01a25f25045592))

* added scope fixtures; added wait function to ensure an empty queue ([`f85da8c`](https://gitlab.psi.ch/bec/bec/-/commit/f85da8c472b200ca37883ced29916548545761b9))

* cleanup ([`7879565`](https://gitlab.psi.ch/bec/bec/-/commit/787956540c00328f74dcb0d4db6a7392a6cf49c4))

* added rlock ([`657bb2f`](https://gitlab.psi.ch/bec/bec/-/commit/657bb2fd264231e1ea5b1d3f6110c31aa76eaa47))

* bug fix for scan items ([`7e44df7`](https://gitlab.psi.ch/bec/bec/-/commit/7e44df7756d9aef9422a1d3425d77f3ce1e5ceb5))

* added sent storage to sync_storage in scan bundler ([`fd1e165`](https://gitlab.psi.ch/bec/bec/-/commit/fd1e1657ee428b8fc57f06653f457697744cd553))

* queue sets and publishes ([`1992d25`](https://gitlab.psi.ch/bec/bec/-/commit/1992d25a85e34452a908660d392c0c036251187e))

* Merge branch &#39;scan_manager&#39; ([`1cb373a`](https://gitlab.psi.ch/bec/bec/-/commit/1cb373a32cdbdb92225fb0edcf4ad86623d850e4))

* added queue reset to test functions ([`b561ce3`](https://gitlab.psi.ch/bec/bec/-/commit/b561ce3a6d4a7116079b07af0923906af81c8051))

* added request_reset ([`42863f1`](https://gitlab.psi.ch/bec/bec/-/commit/42863f113f7364d89ffe04c33510702da4c899b0))

* Merge branch &#39;scan_manager&#39; into &#39;master&#39;

added implicit scan acceptance

See merge request bec/bec!22 ([`985074e`](https://gitlab.psi.ch/bec/bec/-/commit/985074e2cb19b6b91de74036d9d0487b9976c9c5))

* added implicit scan acceptance ([`61d7c1c`](https://gitlab.psi.ch/bec/bec/-/commit/61d7c1cb6bb1e858c2c708bc499ca1548e79da75))

* Merge branch &#39;scan_manager&#39; into &#39;master&#39;

client refactoring

See merge request bec/bec!21 ([`5219d8a`](https://gitlab.psi.ch/bec/bec/-/commit/5219d8a80512ec72a3de36a42f657de7d0be616e))

* bug fix in scan bundler ([`91baf55`](https://gitlab.psi.ch/bec/bec/-/commit/91baf55c42f47bbd1784c45567ab814ec48c210a))

* cleanup ([`9011740`](https://gitlab.psi.ch/bec/bec/-/commit/9011740163154cb0274726303ef277c2955ec3d8))

* major client refactoring ([`43fce58`](https://gitlab.psi.ch/bec/bec/-/commit/43fce581f00eae275ee83c37537bd77a4349452b))

* Merge branch &#39;fly_scan_improvements&#39; into &#39;master&#39;

cleanup

See merge request bec/bec!20 ([`a3a5a5b`](https://gitlab.psi.ch/bec/bec/-/commit/a3a5a5b3ef7c8e0c4c94dfa9f082e27899a21840))

* Merge branch &#39;master&#39; into fly_scan_improvements ([`50debe3`](https://gitlab.psi.ch/bec/bec/-/commit/50debe322686bee9ba9c016cb902e8a80d86c4d0))

* Merge branch &#39;fly_scan_improvements&#39; into &#39;master&#39;

added message bundle for lower latency

See merge request bec/bec!19 ([`f7a6c2d`](https://gitlab.psi.ch/bec/bec/-/commit/f7a6c2d684640a052eafe2de943bc5cdf12ccdae))

* fixed bug in scan_queue that would cause the scan update to stop ([`a7bb7a1`](https://gitlab.psi.ch/bec/bec/-/commit/a7bb7a1da2228227fab37fa1fb7054e80c42131a))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

added error handling for rpc calls; closes #40

Closes #40

See merge request bec/bec!18 ([`5955de7`](https://gitlab.psi.ch/bec/bec/-/commit/5955de7c4216fc245c683a222e593f375822705a))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

online changes for first fly scan with lamni

See merge request bec/bec!17 ([`6c06ee9`](https://gitlab.psi.ch/bec/bec/-/commit/6c06ee95331b4fdb6415a9013247a76a5848bce2))

* Update __init__.py ([`b355343`](https://gitlab.psi.ch/bec/bec/-/commit/b355343545ba475b7e9c0635d37f96b4d8bc0496))

* cleanup ([`b4de391`](https://gitlab.psi.ch/bec/bec/-/commit/b4de391f6b001285c7be8d5a7eb0d9bf693aa412))

* added cleanup routine ([`8ade3c9`](https://gitlab.psi.ch/bec/bec/-/commit/8ade3c93c980ff3fdef7bb551e4962fdb32f048e))

* made output of fly and step more consistent ([`c2bf1bc`](https://gitlab.psi.ch/bec/bec/-/commit/c2bf1bc3f0da11b628cc7202e3332f2d1fe78119))

* moved test utils to utils ([`15ea671`](https://gitlab.psi.ch/bec/bec/-/commit/15ea671c71c46347a514b0a8bc87fc121a574cbd))

* added message bundle for lower latency ([`6ea854a`](https://gitlab.psi.ch/bec/bec/-/commit/6ea854a3b5615d6c4fc05a32316e24dcc35937a5))

* added error handling for rpc calls; closes #40 ([`a4aa883`](https://gitlab.psi.ch/bec/bec/-/commit/a4aa8830e6046b996c86a90bbff9e133c2121331))

* added device disabled errors; fixed device update in DB ([`381e2a5`](https://gitlab.psi.ch/bec/bec/-/commit/381e2a58829f5ff198b755502399b26a2e362f09))

* reverted changes ([`da95e13`](https://gitlab.psi.ch/bec/bec/-/commit/da95e136f04767a54166473ed0481e8ad95941b7))

* Merge branch &#39;online_changes&#39; of gitlab.psi.ch:bec/bec into online_changes ([`0d125f9`](https://gitlab.psi.ch/bec/bec/-/commit/0d125f9e1204977f2eb2e0099cf2dc6e13feb850))

* Update .gitlab-ci.yml ([`30c6ff2`](https://gitlab.psi.ch/bec/bec/-/commit/30c6ff2b64848b3f3185c2aec664590a7cfb85bf))

* prel version of cont_line_scan ([`eb9cfd5`](https://gitlab.psi.ch/bec/bec/-/commit/eb9cfd5cb1b0f8a7648152537f5ce87893d6062b))

* added trigger endpoint ([`a340a7c`](https://gitlab.psi.ch/bec/bec/-/commit/a340a7ce8949751a385a3c4e7de51bce0c5576f9))

* fixed formatting ([`caa662e`](https://gitlab.psi.ch/bec/bec/-/commit/caa662e5b1636aafaf0a6d28e6f38707087b9c62))

* added producer to mocked initializer ([`b314254`](https://gitlab.psi.ch/bec/bec/-/commit/b314254d31f555af22d843af7bf09e24d3b87d8b))

* Merge branch &#39;master&#39; into &#39;online_changes&#39;

# Conflicts:
#   bec_client/bec_client/__init__.py ([`54cc5e1`](https://gitlab.psi.ch/bec/bec/-/commit/54cc5e16d22fcc54a6ef4fc859d8b4a6b2da3d78))

* Update __init__.py ([`6aef1c7`](https://gitlab.psi.ch/bec/bec/-/commit/6aef1c7460517785c47f90204c592fa8cca7098d))

* online changes for first fly scan with lamni ([`688b6bc`](https://gitlab.psi.ch/bec/bec/-/commit/688b6bc0acb1112a6cd0af81214031401638aa83))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

added pre scan macros; closes #38

Closes #38

See merge request bec/bec!16 ([`ad1bf0e`](https://gitlab.psi.ch/bec/bec/-/commit/ad1bf0ee654debbfb428443f87b398a3e1966cbc))

* added lrange, lpush, rpush functions to producermock ([`5c44742`](https://gitlab.psi.ch/bec/bec/-/commit/5c44742ae7ce898bcbcbdaf3d3165b648f066944))

* added pre scan macros ([`aec12f9`](https://gitlab.psi.ch/bec/bec/-/commit/aec12f993d7329936a2a29bab4394161a52a9e55))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!15 ([`3e7eec0`](https://gitlab.psi.ch/bec/bec/-/commit/3e7eec07f41305c5f60174aef61f632618a67d23))

* cleanup ([`186e30e`](https://gitlab.psi.ch/bec/bec/-/commit/186e30eb6c6eaa8d8b60ef47b99b87d0e2e3067e))

* renamed scantype to scan_type ([`4f151a0`](https://gitlab.psi.ch/bec/bec/-/commit/4f151a0f4e7e6eaabb6c01dfbc0bf557a465a9a5))

* Merge branch &#39;master&#39; into online_changes ([`65a2ff0`](https://gitlab.psi.ch/bec/bec/-/commit/65a2ff0b5c921bf48d9fde7956ea9bd23a03b493))

* added device storage for async readings ([`f2226f2`](https://gitlab.psi.ch/bec/bec/-/commit/f2226f2e44cf9802bbce448426beda8c3ffd59f0))

* changed signal handling for fly scans ([`ae51321`](https://gitlab.psi.ch/bec/bec/-/commit/ae5132142175bbdb5fa138c3396e810e886d9971))

* bug fix for bundler; added lock to queue update; added scan abort notification ([`37b0b72`](https://gitlab.psi.ch/bec/bec/-/commit/37b0b72f8f7c41a9a0cad22f02ffc73391f33ee5))

* removed debugging output to tests ([`5628c83`](https://gitlab.psi.ch/bec/bec/-/commit/5628c83272eba2d948604ee7548f542755e68b4d))

* added debugging output to tests ([`535d4a0`](https://gitlab.psi.ch/bec/bec/-/commit/535d4a08e27aa03ee121e5dbad2e7ae3d37f0994))

* added debugging output to tests ([`ff1e4be`](https://gitlab.psi.ch/bec/bec/-/commit/ff1e4becd0e909e49bdfe047d3bd7615b36f4645))

* removed timeout in scan bundler ([`5fa0e24`](https://gitlab.psi.ch/bec/bec/-/commit/5fa0e24d7e2977d70216b7cf2630fbef8c5aa670))

* changed default timeout to 200 s ([`522d8f1`](https://gitlab.psi.ch/bec/bec/-/commit/522d8f16f22b931c57a344c2be00af17f7e056e1))

* added explicit check for scan abort test ([`f1a464d`](https://gitlab.psi.ch/bec/bec/-/commit/f1a464d71ff16346b018ca176117f12b5f48621a))

* added more delay to scan abort test ([`614e6f5`](https://gitlab.psi.ch/bec/bec/-/commit/614e6f5f01fbe4512140a1d3ea29a34bce0751b4))

* cleanup ([`6f33e40`](https://gitlab.psi.ch/bec/bec/-/commit/6f33e4004e65f7801424e68213e4ec6801b5e1bc))

* avoid prel exit in client callback ([`25e2ebd`](https://gitlab.psi.ch/bec/bec/-/commit/25e2ebd361fdab3fbeef6ea07fcd75c8ef9bda44))

* added alarm check ([`d8b1561`](https://gitlab.psi.ch/bec/bec/-/commit/d8b1561501833636e0650a01034383f1f0987034))

* fixed bug in client callback ([`5c3ec5f`](https://gitlab.psi.ch/bec/bec/-/commit/5c3ec5f4ab7dc07edf89aed1b7e588528a6ff6fc))

* bug fix in client callback ([`d7e335d`](https://gitlab.psi.ch/bec/bec/-/commit/d7e335ddbe45e6bf20ae1a18d9a8ce85e364874c))

* Merge branch &#39;fly_scan&#39; into &#39;master&#39;

fly scan; closes #9 #10

Closes #10 and #9

See merge request bec/bec!14 ([`372072a`](https://gitlab.psi.ch/bec/bec/-/commit/372072a55f9b49fd653f91c9393546b63c80e2be))

* bug fixes for fly scan support ([`9fe9ade`](https://gitlab.psi.ch/bec/bec/-/commit/9fe9adec33fa2e1bb5d9145ab2c31c443f5406f1))

* bug fixes for fly scans; added parallelpool for scan bundler and device server ([`f4b7e67`](https://gitlab.psi.ch/bec/bec/-/commit/f4b7e67f5e221e8076c2d6941dc669a6a0aba343))

* scan bundler is now only triggered by scan msgs ([`006db98`](https://gitlab.psi.ch/bec/bec/-/commit/006db98983c373811e9b486ac8967c2dbbb71567))

* reduced logger output ([`c7e34b8`](https://gitlab.psi.ch/bec/bec/-/commit/c7e34b8f664b8ba9c3a749a4789169f6c22f9b0a))

* fixed bug in scan bundler ([`9d0dc7c`](https://gitlab.psi.ch/bec/bec/-/commit/9d0dc7c72bf94d88e91994da58562bcfe96acc71))

* Merge branch &#39;master&#39; into fly_scan ([`7a23c55`](https://gitlab.psi.ch/bec/bec/-/commit/7a23c5512ce6db19acaf2d754b1f01bfbceb0d5b))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

Online changes

See merge request bec/bec!13 ([`f1e832f`](https://gitlab.psi.ch/bec/bec/-/commit/f1e832f397d82f76a5cd63a037892cf4312bbf57))

* prel. fly scan implementation ([`ed4346c`](https://gitlab.psi.ch/bec/bec/-/commit/ed4346c0f7fcbabbc4ce02efce738130b2ea95c2))

* added limits to LamNI devices ([`9d52f5b`](https://gitlab.psi.ch/bec/bec/-/commit/9d52f5bdd08279c8f7a30781970cb07215fca7b4))

* added rpc output print to logger ([`b022848`](https://gitlab.psi.ch/bec/bec/-/commit/b022848f882562ab57db04d4f08049bf2f22d5bd))

* online changes for LamNIFermatScan ([`fb10b7f`](https://gitlab.psi.ch/bec/bec/-/commit/fb10b7f58350f1c43df8738c43d9db0fdc72d4d8))

* online changes ([`70f9b19`](https://gitlab.psi.ch/bec/bec/-/commit/70f9b196df4a14e9ae610036513c85accca6edd7))

* Merge branch &#39;online_changes&#39; of https://gitlab.psi.ch/bec/bec into online_changes ([`d5416fa`](https://gitlab.psi.ch/bec/bec/-/commit/d5416fad0b1166f0b51401f29be42969f3cacb7f))

* Update demo.py ([`69628df`](https://gitlab.psi.ch/bec/bec/-/commit/69628dfb5026220be2ad32f3b0467f5de9f7e835))

* added matplotlib for debugging plots ([`2c7687f`](https://gitlab.psi.ch/bec/bec/-/commit/2c7687fd1e602c6928b12d3c98e25486ff06eadd))

* figures saved to disk ([`5f93de3`](https://gitlab.psi.ch/bec/bec/-/commit/5f93de367e0372258fe0aa08e4e108d0904d101c))

* fixed formatting ([`f56d433`](https://gitlab.psi.ch/bec/bec/-/commit/f56d4331e86348bc0c56575480bb49227874d5c8))

* online_changes ([`806c4ff`](https://gitlab.psi.ch/bec/bec/-/commit/806c4ff2d62db345714f4f2398914c1d0235332d))

* Merge branch &#39;master&#39; into online_changes ([`60804bd`](https://gitlab.psi.ch/bec/bec/-/commit/60804bd0e6685058eeebc9c5667eab09baa4702b))

* reduced num points for queued scan test ([`32ec10c`](https://gitlab.psi.ch/bec/bec/-/commit/32ec10c3a8c2d789f4c1791be0986a35e9492201))

* added scan_type to open_scan message ([`b322077`](https://gitlab.psi.ch/bec/bec/-/commit/b3220772e7065bd14b114372d7cbbf154eb51e2f))

* splitted config attribute device_access into device_access and device_mapping ([`54caafa`](https://gitlab.psi.ch/bec/bec/-/commit/54caafa36d953b95560858747639803b9cf9c9b4))

* splitted config attribute device_access into device_access and device_mapping ([`0009529`](https://gitlab.psi.ch/bec/bec/-/commit/000952935f05f6cce7c6248b4734c932e9e9eda5))

* added req_done check to progress bar loop ([`21d45aa`](https://gitlab.psi.ch/bec/bec/-/commit/21d45aa3f48596f0753df5684ca5934646d84d3e))

* ensure queued scans finish before test completes ([`2612e89`](https://gitlab.psi.ch/bec/bec/-/commit/2612e895c388fc2e0a26f8e3ac9388c94244e8b7))

* online changes ([`a039780`](https://gitlab.psi.ch/bec/bec/-/commit/a03978097a26a579d3cb2290dc22e19c2a79376c))

* added debug output to req done ([`583bbba`](https://gitlab.psi.ch/bec/bec/-/commit/583bbbaefbe358be99cd0984eeb243f98b25ca40))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

lamni scan

See merge request bec/bec!12 ([`db5be5c`](https://gitlab.psi.ch/bec/bec/-/commit/db5be5cb0743126553485e11a72756eac20529dc))

* moved rpc to scans; exposed device_rpc user function ([`290f24e`](https://gitlab.psi.ch/bec/bec/-/commit/290f24edb31235718197e57d19e3dfa2fe71bb72))

* Merge branch &#39;master&#39; into online_changes ([`a98f358`](https://gitlab.psi.ch/bec/bec/-/commit/a98f358947547f0043498627774a3b7cc6ec189a))

* Merge branch &#39;online_changes&#39; of gitlab.psi.ch:bec/bec into online_changes ([`422d22b`](https://gitlab.psi.ch/bec/bec/-/commit/422d22b8c7601313c587f3fe9a66a31472b5964e))

* formatting ([`9124b78`](https://gitlab.psi.ch/bec/bec/-/commit/9124b78692003836c2db8b6b8ed554d4e20537ce))

* lamni fermat scan ([`9c173e3`](https://gitlab.psi.ch/bec/bec/-/commit/9c173e3a4a7f3b1e10df8e701175096c7991404e))

* lamni fermat scan ([`b1aaf41`](https://gitlab.psi.ch/bec/bec/-/commit/b1aaf418e4a7b6ec40442800ec43884717aebc40))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`4cfbba6`](https://gitlab.psi.ch/bec/bec/-/commit/4cfbba6304dfc185854e653c877a483ec530d954))

* changed ophyd repo to gitlab ([`5bf5515`](https://gitlab.psi.ch/bec/bec/-/commit/5bf55153fe6091809abf247c59ea53c4dece4c3d))

* added lock to queue update ([`70ad332`](https://gitlab.psi.ch/bec/bec/-/commit/70ad33270a9c6044f589bd5c39c34fcc899c2b69))

* added logger level to device_server ([`1fa7cad`](https://gitlab.psi.ch/bec/bec/-/commit/1fa7cada1e9e0df2621090758535e23295050221))

* added debug output ([`8de3156`](https://gitlab.psi.ch/bec/bec/-/commit/8de3156468baff7e5bd9c0d081ec1fe8a8749104))

* reduced points in queue scan test ([`2da3e46`](https://gitlab.psi.ch/bec/bec/-/commit/2da3e4626551398c4818c82f224a8262bf26c081))

* changed mv to umv ([`bde2c3c`](https://gitlab.psi.ch/bec/bec/-/commit/bde2c3cadd9e1a72863585aaf7fbd9eef21f5181))

* changed rlock to lock ([`61d01e6`](https://gitlab.psi.ch/bec/bec/-/commit/61d01e6f5a88d002ae14eca7adee9c0cd6e3e911))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`8a78dda`](https://gitlab.psi.ch/bec/bec/-/commit/8a78dda8f8a01d0299b7e60135a9e3ac78fcdf78))

* enabled random order for end2end tests ([`140aec2`](https://gitlab.psi.ch/bec/bec/-/commit/140aec29a4d71bbf3480eac499614f36f3c20621))

* enabled random test order ([`a044ec2`](https://gitlab.psi.ch/bec/bec/-/commit/a044ec2f74d02abd652c26eaad5e61aafc1f7a77))

* Update Dockerfile ([`ec161b2`](https://gitlab.psi.ch/bec/bec/-/commit/ec161b283e441c47f211e3bb6275cf068c78f936))

* added pytest-random-order as dependency ([`dc6d2dc`](https://gitlab.psi.ch/bec/bec/-/commit/dc6d2dcd102ccd1aa94ad07597809902e3c2214a))

* added rlock to find_scan ([`84a8087`](https://gitlab.psi.ch/bec/bec/-/commit/84a808796410c4aff1c41d1f53cff33f1dee36f1))

* stability improvements for end2end test ([`1624dac`](https://gitlab.psi.ch/bec/bec/-/commit/1624dac74eb961cde76df6e782c6e303987bf78e))

* removed simulate mode; closes #36 ([`7dbc3b1`](https://gitlab.psi.ch/bec/bec/-/commit/7dbc3b1bca3afd3b2d45f129a5c5da0a348f3336))

* cleanup ([`3380216`](https://gitlab.psi.ch/bec/bec/-/commit/33802162cba8645170b6059d53d54e82b4fe8b75))

* comments ([`02c31de`](https://gitlab.psi.ch/bec/bec/-/commit/02c31de76a79f20dfe41ed1d256597b440680512))

* comments ([`908081b`](https://gitlab.psi.ch/bec/bec/-/commit/908081b5854f30935682b33df3972e67a196765b))

* added test for scan queues ([`7bd2e34`](https://gitlab.psi.ch/bec/bec/-/commit/7bd2e346909d1433ad0b974751fce8cd55eb53a0))

* fixed leading whitespace error ([`b4c8bb9`](https://gitlab.psi.ch/bec/bec/-/commit/b4c8bb96a67daa4916102620f988d3d8efbd5681))

* fixed bug in end2end tests ([`4a279c6`](https://gitlab.psi.ch/bec/bec/-/commit/4a279c6cc31cd7897c9c58b0f7c578d59daad0eb))

* Merge branch &#39;online_changes&#39; into &#39;master&#39;

online changes for lamni

See merge request bec/bec!11 ([`ca75823`](https://gitlab.psi.ch/bec/bec/-/commit/ca758239005d4474d15c0aeb90ceab9ac1c33197))

* formatting ([`48c299c`](https://gitlab.psi.ch/bec/bec/-/commit/48c299c524111d06716ca2711e64e054a7a2f1b1))

* added comments ([`6c18edf`](https://gitlab.psi.ch/bec/bec/-/commit/6c18edfb914f84d72d96510595991d7451b77211))

* fixed labels update ([`d0e3606`](https://gitlab.psi.ch/bec/bec/-/commit/d0e3606c0706007774c35665f9612f6f72516c01))

* online changes for lamni ([`7b97d1b`](https://gitlab.psi.ch/bec/bec/-/commit/7b97d1b9b60535640e984c3a30c712b97219ee72))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`b9dc9b5`](https://gitlab.psi.ch/bec/bec/-/commit/b9dc9b56b21ba34e2497575160fb383725a00630))

* Update .gitlab-ci.yml ([`bf0a2e3`](https://gitlab.psi.ch/bec/bec/-/commit/bf0a2e37d98e2d74640eba136a41053c66beb147))

* fixed bug in progressbar ([`1ab64c6`](https://gitlab.psi.ch/bec/bec/-/commit/1ab64c6cf4a6caffccc3628827521973efa5fd60))

* updated pylintrc ([`faf30f5`](https://gitlab.psi.ch/bec/bec/-/commit/faf30f578f146f2fd1f30e4c9fbfa3d16118ea1b))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`3e1639e`](https://gitlab.psi.ch/bec/bec/-/commit/3e1639e362e352a600ad993d015c425a576a3112))

* Update .gitlab-ci.yml ([`eba50a0`](https://gitlab.psi.ch/bec/bec/-/commit/eba50a0fe5e2a4efc57d2bdd4050e61d3bd46f10))

* Update .gitlab-ci.yml ([`c985b7c`](https://gitlab.psi.ch/bec/bec/-/commit/c985b7c6b0cf66b1e7cfbc3b310ff5548a9b057b))

* added comments ([`12b8f0a`](https://gitlab.psi.ch/bec/bec/-/commit/12b8f0a45adb71e5b1f59ba830444626290cb75f))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`91278f4`](https://gitlab.psi.ch/bec/bec/-/commit/91278f4e8ae48acc9b19c24697f3bcc7524b9740))

* Update Dockerfile ([`068402f`](https://gitlab.psi.ch/bec/bec/-/commit/068402f51711c4165007883a7228adc6dd73a5f9))

* fixed tmux helper for new service names ([`e9b9938`](https://gitlab.psi.ch/bec/bec/-/commit/e9b993879e08490dc524fb71cc5686c2e3b41eeb))

* fixed paths for bec_server helper ([`fa8bd71`](https://gitlab.psi.ch/bec/bec/-/commit/fa8bd71036d8e6bd74d07f4a1a201e8d05f9b8f4))

* fixed launch_docker_services ([`b54fac0`](https://gitlab.psi.ch/bec/bec/-/commit/b54fac0f559b0648ac76d092dde668c80e3b51d7))

* change log level for starting messages; changed default log level of client to success ([`fd6f24e`](https://gitlab.psi.ch/bec/bec/-/commit/fd6f24e854ae07fa5f363ebda8c55ef9797445eb))

* changed timeout to 100s ([`b28d14c`](https://gitlab.psi.ch/bec/bec/-/commit/b28d14cf371bd7e4bdd2c635e809709667ce1e3b))

* fixed bug in client callback; added test ([`b561dd6`](https://gitlab.psi.ch/bec/bec/-/commit/b561dd60ee44e4ca1002dcf9e14a549b75b3ccfc))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`52786f7`](https://gitlab.psi.ch/bec/bec/-/commit/52786f7012e35af945bdd1605df8f7537ef2d494))

* Merge branch &#39;master&#39; of https://gitlab.psi.ch/bec/bec ([`e21a208`](https://gitlab.psi.ch/bec/bec/-/commit/e21a20839de1f35cb8d6542ed6d34e853edd3ce6))

* added helper scripts ([`4ce7f92`](https://gitlab.psi.ch/bec/bec/-/commit/4ce7f92419a812b75c1c69e6e95f1f4aebdeb6e0))

* fixed bug in raise_alarm ([`c65ac97`](https://gitlab.psi.ch/bec/bec/-/commit/c65ac978c331a487baff9565733971806a79298f))

* cleanup; fixed progressbar for mv ([`c660bce`](https://gitlab.psi.ch/bec/bec/-/commit/c660bcef01ff4da78ee69f5008f6dca7a5ce9285))

* cleanup ([`43973c1`](https://gitlab.psi.ch/bec/bec/-/commit/43973c125bee67d1e3d40d4e033fed5a08b7bffa))

* make sure the scan is aborted ([`025832e`](https://gitlab.psi.ch/bec/bec/-/commit/025832e94db4505c55482fe02138857a28f957fb))

* moved thread start closer to scan start ([`c2d19f6`](https://gitlab.psi.ch/bec/bec/-/commit/c2d19f6b1c6c2efee6e6479b05c61c457d282996))

* added more time between abort messages ([`04b147e`](https://gitlab.psi.ch/bec/bec/-/commit/04b147ea9ae1fd72a5e9b442ccc1d7f22b16eb51))

* added missing file ([`e2c350f`](https://gitlab.psi.ch/bec/bec/-/commit/e2c350ff482df2a71bfe0efe66f3cedde60e9ddf))

* cleanup ([`dacd6ac`](https://gitlab.psi.ch/bec/bec/-/commit/dacd6ac273c2e2d89dd916ea5083c574d1400a8a))

* cleanup ([`2028744`](https://gitlab.psi.ch/bec/bec/-/commit/202874489f440b59c0c3c81922751eaf7469ed1a))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`e4d5cad`](https://gitlab.psi.ch/bec/bec/-/commit/e4d5cad04d3f29b8669b87946c473477612cf050))

* Update .gitlab-ci.yml ([`14b055a`](https://gitlab.psi.ch/bec/bec/-/commit/14b055aae42fc007f15d0a1828c714decd3b2337))

* Update .gitlab-ci.yml ([`4f35617`](https://gitlab.psi.ch/bec/bec/-/commit/4f3561789cab7283e329791dbd1af1527703d7b7))

* added more end2end tests ([`7e175c4`](https://gitlab.psi.ch/bec/bec/-/commit/7e175c4d4e46ec4187445eb569b6f50a3396b807))

* Update .gitlab-ci.yml ([`98f8531`](https://gitlab.psi.ch/bec/bec/-/commit/98f85310e0cab4244f8c9d34240b46f0d255f414))

* Update .gitlab-ci.yml ([`b0d7305`](https://gitlab.psi.ch/bec/bec/-/commit/b0d7305695df231775527af6058a3243717bcc85))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`95c12a3`](https://gitlab.psi.ch/bec/bec/-/commit/95c12a3f5699350bcb5a48bdf44d6bf9c907f99b))

* Update Dockerfile ([`17af6b9`](https://gitlab.psi.ch/bec/bec/-/commit/17af6b9bb0ea761c93fa05d24df7d64474e26b55))

* Update .gitlab-ci.yml ([`c692ff7`](https://gitlab.psi.ch/bec/bec/-/commit/c692ff728cf785aced937b13080ff84df3c2c8a4))

* Update .gitlab-ci.yml ([`e979d58`](https://gitlab.psi.ch/bec/bec/-/commit/e979d58677d9b3e92d8d515e700319a2f0f3ebd2))

* Update .gitlab-ci.yml ([`9025b9c`](https://gitlab.psi.ch/bec/bec/-/commit/9025b9c94a18f4dde6700baee2ee91a654865e8b))

* Update .gitlab-ci.yml ([`44eb500`](https://gitlab.psi.ch/bec/bec/-/commit/44eb500649cc77574e8e4eb1f402b9a56795ddce))

* Update .gitlab-ci.yml ([`c2f29b6`](https://gitlab.psi.ch/bec/bec/-/commit/c2f29b6ca122714f212c8a49d8e2fb95324d6963))

* Update Dockerfile ([`e5fb345`](https://gitlab.psi.ch/bec/bec/-/commit/e5fb3454c939fcc51574ee63385afde01596f770))

* Update Dockerfile ([`9df451c`](https://gitlab.psi.ch/bec/bec/-/commit/9df451c2d878100d091b7204670dd2a60a12b565))

* Update Dockerfile ([`3961d2e`](https://gitlab.psi.ch/bec/bec/-/commit/3961d2eada70e94a5bbece7343a78b7e9849892c))

* Update Dockerfile ([`f11e4b2`](https://gitlab.psi.ch/bec/bec/-/commit/f11e4b275b3e782a45bc0d87a28dc0b76cfe2054))

* Update .gitlab-ci.yml ([`f365ac0`](https://gitlab.psi.ch/bec/bec/-/commit/f365ac0f6789b3bed2af5def7b44eeecd0ce1534))

* Update Dockerfile ([`178a621`](https://gitlab.psi.ch/bec/bec/-/commit/178a621b66765f7f91b39019f8704dc76366dfcd))

* Update .gitlab-ci.yml ([`f6a6980`](https://gitlab.psi.ch/bec/bec/-/commit/f6a698020f69a9c434aeb08741ace7af416a4273))

* added dockerfile for end2end ([`081a31f`](https://gitlab.psi.ch/bec/bec/-/commit/081a31f366526e0bdbac15c2944f25410c19516c))

* added init_scibec ([`40d64f4`](https://gitlab.psi.ch/bec/bec/-/commit/40d64f42be6e7183e57d036abc48fc1dac915142))

* Update docker-compose.yaml ([`604e475`](https://gitlab.psi.ch/bec/bec/-/commit/604e475964cc90adc59002b38105c124a0ebfb7e))

* Update docker-compose.yaml ([`6a8d117`](https://gitlab.psi.ch/bec/bec/-/commit/6a8d1178308ffff4bd305ca14e14a484882e0935))

* Update docker-compose.yaml ([`320f1c1`](https://gitlab.psi.ch/bec/bec/-/commit/320f1c110f2be3c0890783ce223cecb00a22412e))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`2a12278`](https://gitlab.psi.ch/bec/bec/-/commit/2a122783ce57f5bff1abe8eaec0705ae5730e97c))

* Update Dockerfile ([`37d712c`](https://gitlab.psi.ch/bec/bec/-/commit/37d712c16981f25fa9f1df6bc95d77679540e9c9))

* Update Dockerfile ([`d89be56`](https://gitlab.psi.ch/bec/bec/-/commit/d89be56c0c9cd9e9f69a8e034c3bac543e4d44d5))

* added argparse to update_sessions; added test_config ([`0552e8f`](https://gitlab.psi.ch/bec/bec/-/commit/0552e8f2796bc6492cd54a0b8b4056d4e33287ad))

* added g++ ([`3f1d80d`](https://gitlab.psi.ch/bec/bec/-/commit/3f1d80d32d011a00656115e5d519557ae9eed135))

* added gcc to alpine ([`97f7f3e`](https://gitlab.psi.ch/bec/bec/-/commit/97f7f3e6f8fdea35b1a262eefba84adec67ff667))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`9e3d42e`](https://gitlab.psi.ch/bec/bec/-/commit/9e3d42e3be828af06f975d47268ee25fb3ee874d))

* Update .gitlab-ci.yml ([`68c2ca0`](https://gitlab.psi.ch/bec/bec/-/commit/68c2ca010d9da447d1736767bdaf84fb319bd446))

* Update .gitlab-ci.yml ([`9a581d4`](https://gitlab.psi.ch/bec/bec/-/commit/9a581d4c702c8a524cd9453d8ae09008d40b73a0))

* Update .gitlab-ci.yml ([`d56bc02`](https://gitlab.psi.ch/bec/bec/-/commit/d56bc02b92d34d29008d1662e2c8eaff9ce30fc1))

* Update test_config.yaml ([`f8bf470`](https://gitlab.psi.ch/bec/bec/-/commit/f8bf470dccd0f5ea126731afca4f2e6528c397fe))

* Update test_config.yaml ([`401251b`](https://gitlab.psi.ch/bec/bec/-/commit/401251b96031b29711b4f5ed6ffbf60c4fd7038c))

* Update .gitlab-ci.yml ([`76d2dff`](https://gitlab.psi.ch/bec/bec/-/commit/76d2dff7ebb0da6d302f4a076aefe84125caa9c5))

* Update .gitlab-ci.yml ([`dcce82c`](https://gitlab.psi.ch/bec/bec/-/commit/dcce82c457067592e9d264eb7b113e10de3f158f))

* Update .gitlab-ci.yml ([`bb4e86b`](https://gitlab.psi.ch/bec/bec/-/commit/bb4e86bf0ade136887212aec7838f9bd357ed6e3))

* Update .gitlab-ci.yml ([`68f5f90`](https://gitlab.psi.ch/bec/bec/-/commit/68f5f90e24089197c29ad297fb48e1dc43dc5259))

* Update .gitlab-ci.yml ([`20645fc`](https://gitlab.psi.ch/bec/bec/-/commit/20645fc42931e793aa80b7ddcbaae05c3b31067d))

* Update .gitlab-ci.yml ([`1565f14`](https://gitlab.psi.ch/bec/bec/-/commit/1565f1453d02812d2162b36675671f14f7cc1bff))

* Update .gitlab-ci.yml ([`09e7121`](https://gitlab.psi.ch/bec/bec/-/commit/09e71211cc36e1da88bca7f326e93197fd4a3ec5))

* Update .gitlab-ci.yml ([`8b67f2a`](https://gitlab.psi.ch/bec/bec/-/commit/8b67f2a62abe42713503e2ff26650b8704ca50d3))

* Update .gitlab-ci.yml ([`c923a68`](https://gitlab.psi.ch/bec/bec/-/commit/c923a6807e81c865de8204797c48af1619a667f5))

* Update .gitlab-ci.yml ([`987f394`](https://gitlab.psi.ch/bec/bec/-/commit/987f394a0461d566d56e24e80384c6695bd2b48f))

* Update .gitlab-ci.yml ([`63e3dad`](https://gitlab.psi.ch/bec/bec/-/commit/63e3dad5ed398c2ced915f077ee1ff6a4c03314a))

* Update .gitlab-ci.yml ([`daec371`](https://gitlab.psi.ch/bec/bec/-/commit/daec3715c60a55025259ba085164788caeb3a196))

* Update .gitlab-ci.yml ([`895e640`](https://gitlab.psi.ch/bec/bec/-/commit/895e640430e360e04e5b295ebd839dd4bd829db0))

* Update .gitlab-ci.yml ([`303a244`](https://gitlab.psi.ch/bec/bec/-/commit/303a2445bbe4eb833b47ad05a7f96bda832adbfd))

* Update .gitlab-ci.yml ([`1f641d1`](https://gitlab.psi.ch/bec/bec/-/commit/1f641d13dc448e5cf036f4957e626b9d9445667e))

* Update .gitlab-ci.yml ([`678fbe9`](https://gitlab.psi.ch/bec/bec/-/commit/678fbe98917feb5dd16d0d243427fc5efd8bd926))

* Update .gitlab-ci.yml ([`aa573ea`](https://gitlab.psi.ch/bec/bec/-/commit/aa573ea1b671e1c9cd2d0cebe6e60356c9b09144))

* Update .gitlab-ci.yml ([`10320a8`](https://gitlab.psi.ch/bec/bec/-/commit/10320a838e6309d2f0b834201d233cbb4c7c8c1c))

* Update .gitlab-ci.yml ([`2aae4bb`](https://gitlab.psi.ch/bec/bec/-/commit/2aae4bbd7029a22e85d419129c81401689eb49a2))

* Update .gitlab-ci.yml ([`6f67fcf`](https://gitlab.psi.ch/bec/bec/-/commit/6f67fcf8f7cba75a0582a29679e1b67dd0d7d813))

* Update .gitlab-ci.yml ([`090ea92`](https://gitlab.psi.ch/bec/bec/-/commit/090ea92db2b19c62a607367e3f977f9d8fbd276b))

* Update .gitlab-ci.yml ([`99f91ce`](https://gitlab.psi.ch/bec/bec/-/commit/99f91ce88978053c6f6fd7a117702e6c4eb0ec70))

* Update .gitlab-ci.yml ([`61ab149`](https://gitlab.psi.ch/bec/bec/-/commit/61ab149ea8335c22b68586111e31376a6815ef3e))

* Update .gitlab-ci.yml ([`703f759`](https://gitlab.psi.ch/bec/bec/-/commit/703f759a8de8632f04acd64b83e2e6cd8c3b61f9))

* Update .gitlab-ci.yml ([`156b3f8`](https://gitlab.psi.ch/bec/bec/-/commit/156b3f82838a2980e0d3e2f1e521707f1114badd))

* Update .gitlab-ci.yml ([`70bcc32`](https://gitlab.psi.ch/bec/bec/-/commit/70bcc32db9999b206d6c31277bda85f3adcebf63))

* Update .gitlab-ci.yml ([`d375d55`](https://gitlab.psi.ch/bec/bec/-/commit/d375d55b4c829b4bf7cae533e6dba9842bd1b07e))

* origin moved to alpine ([`81427d8`](https://gitlab.psi.ch/bec/bec/-/commit/81427d84d7076e74a9688a2fad540ef5fffa018d))

* updated ci file ([`5d9b2a4`](https://gitlab.psi.ch/bec/bec/-/commit/5d9b2a453ee2eaaf0b71a36b2cb4a1f0fadd3c29))

* Update .gitlab-ci.yml ([`f83f174`](https://gitlab.psi.ch/bec/bec/-/commit/f83f174f8a66480a6d7c91a958fe68217106541e))

* Update .gitlab-ci.yml ([`3ebcfa2`](https://gitlab.psi.ch/bec/bec/-/commit/3ebcfa236f7980538092950c948bc64b667fbf22))

* enabled push to registry ([`8596fc8`](https://gitlab.psi.ch/bec/bec/-/commit/8596fc8108809cb8811a30edb18a2464deb749c9))

* fixed dockerfiles ([`832c6c5`](https://gitlab.psi.ch/bec/bec/-/commit/832c6c5a5ae78bd10280b79d4e6031dfdcc344b6))

* fixed path to new config file ([`03d5cde`](https://gitlab.psi.ch/bec/bec/-/commit/03d5cdee624933867bee09d0d4f69004388f83f9))

* Delete .gitmodules ([`b98a2fe`](https://gitlab.psi.ch/bec/bec/-/commit/b98a2fed719d6aab109c10ad81166ce9d2dfcabd))

* Update .gitlab-ci.yml ([`14db159`](https://gitlab.psi.ch/bec/bec/-/commit/14db1599de36dffacde3f1bea0a538f6292e0d37))

* added docker files ([`88ceca3`](https://gitlab.psi.ch/bec/bec/-/commit/88ceca38f0d46902c3eba4f1eeaba60abf67732c))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`3261152`](https://gitlab.psi.ch/bec/bec/-/commit/3261152ef6e7fb4b2516b6aaa54f22c41e7dfcaa))

* Update .gitlab-ci.yml ([`c10239f`](https://gitlab.psi.ch/bec/bec/-/commit/c10239fa15c7a048ca557d819ced9b369d87d0c8))

* added end2end tests ([`94cfa10`](https://gitlab.psi.ch/bec/bec/-/commit/94cfa10baf8e9f9d7636852bfa3267992bf614ed))

* cleanup ([`47e0222`](https://gitlab.psi.ch/bec/bec/-/commit/47e0222f25ce9b48eda90272b014cbdf486aa85a))

* cleanup ([`be2eaf2`](https://gitlab.psi.ch/bec/bec/-/commit/be2eaf203b4f1a8e577083b49c6976f0d8dec77b))

* added target pos ([`47c0e18`](https://gitlab.psi.ch/bec/bec/-/commit/47c0e1871f3d593537d49a7ece5fee13b50a46b0))

* cleanup ([`bcc862d`](https://gitlab.psi.ch/bec/bec/-/commit/bcc862d525d175c8a7294e5fcdb746cd104cc60a))

* fixed build process for device_server ([`942ec3a`](https://gitlab.psi.ch/bec/bec/-/commit/942ec3af39efdd52669d498c617a7fa2b6950a33))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`6572f21`](https://gitlab.psi.ch/bec/bec/-/commit/6572f21d0e35e1267bfd658d9a7abe80660a5c94))

* Update .gitlab-ci.yml ([`f55341a`](https://gitlab.psi.ch/bec/bec/-/commit/f55341a93b98fe710eeee68f19757b999f6a72ec))

* Update .gitlab-ci.yml ([`3cd01bd`](https://gitlab.psi.ch/bec/bec/-/commit/3cd01bdd7fba01983301529f1b194f765713d230))

* Update .gitlab-ci.yml ([`d552a8a`](https://gitlab.psi.ch/bec/bec/-/commit/d552a8a1b942c88b50220ae846c9ed5771065443))

* Update .gitlab-ci.yml ([`fd40b6a`](https://gitlab.psi.ch/bec/bec/-/commit/fd40b6a00551a4d08486a8cfd3e2f59d04fced25))

* Update .gitlab-ci.yml ([`adc08c6`](https://gitlab.psi.ch/bec/bec/-/commit/adc08c68799c463f8bce0c3ed01d8fb6e3adc102))

* updated dockerfile for device_server ([`483180a`](https://gitlab.psi.ch/bec/bec/-/commit/483180ae039c0dd7bec2a1c2eb77aa50a05a3425))

* added more general exception handling ([`8c6edfc`](https://gitlab.psi.ch/bec/bec/-/commit/8c6edfcd124f02ab4b0b3df76d1cc7c696655993))

*  minor update to lamni scan ([`8aad25b`](https://gitlab.psi.ch/bec/bec/-/commit/8aad25b3b73c205f27fdc0eb50973fd49309a90d))

* scan assembler raises scanabort if cls init fails ([`a7bc8d8`](https://gitlab.psi.ch/bec/bec/-/commit/a7bc8d8aca0b51d3787b731a16284ed9cf554f14))

* queue catches general scanabort errors ([`c919e00`](https://gitlab.psi.ch/bec/bec/-/commit/c919e005a655caf77a82ff40141a2fea0d304865))

* renamed to LamNIFermatScan ([`5ad056f`](https://gitlab.psi.ch/bec/bec/-/commit/5ad056fd95c5a52aef8c13d3678194813965f4e2))

* minor change in verbosity ([`8cfa3c0`](https://gitlab.psi.ch/bec/bec/-/commit/8cfa3c0733eb097f95babb49994e3c7526d0b53b))

* added more comments ([`2ab6ad6`](https://gitlab.psi.ch/bec/bec/-/commit/2ab6ad6274bc147cb289b294a9955142dcc871a7))

* added scan macro plugin; closes #26 ([`df4545e`](https://gitlab.psi.ch/bec/bec/-/commit/df4545e630070ab888970bd77274e3e3e650ece5))

* added some more comments to progressbar ([`c36b486`](https://gitlab.psi.ch/bec/bec/-/commit/c36b486dfd3e598dc2d77b3bfde8d5f00bb6c35f))

* minor cleanup ([`5474cba`](https://gitlab.psi.ch/bec/bec/-/commit/5474cba4bfe20251ec4cbc826e384128779e8174))

* Merge branch &#39;codereview&#39; into &#39;master&#39;

removed old koss directory

See merge request bec/bec!10 ([`df80c3a`](https://gitlab.psi.ch/bec/bec/-/commit/df80c3ad795eb8e9e6a32cd5c3ba1a1d34e114ce))

* removed old koss directory ([`51b9ce1`](https://gitlab.psi.ch/bec/bec/-/commit/51b9ce19364bbc63d693c0d3b9da6279e70870d2))

* Merge branch &#39;codereview&#39; into &#39;master&#39;

Codereview

See merge request bec/bec!9 ([`038eae8`](https://gitlab.psi.ch/bec/bec/-/commit/038eae8796aa15320152f3f6e123544e81b3d7fa))

* fixed tests ([`d15f617`](https://gitlab.psi.ch/bec/bec/-/commit/d15f617c1363785464cdde1b3abab7e011c5771f))

* Merge branch &#39;master&#39; into codereview ([`54e1f4c`](https://gitlab.psi.ch/bec/bec/-/commit/54e1f4c0cf9dacef04ef3a9f7ad9bb405bc26117))

* Merge branch &#39;logger&#39; into &#39;master&#39;

added new logger; closes #29 #30

Closes #30 and #29

See merge request bec/bec!8 ([`23b6a84`](https://gitlab.psi.ch/bec/bec/-/commit/23b6a84aa30e66227446e72598579ea5e15e34c4))

* added new logger ([`4935fcf`](https://gitlab.psi.ch/bec/bec/-/commit/4935fcfd35bc1a8fb6dccb4994f742751ba272ef))

* Merge branch &#39;renaming&#39; into &#39;master&#39;

renamed koss and opaas; closes #20

Closes #20

See merge request bec/bec!7 ([`20b0f35`](https://gitlab.psi.ch/bec/bec/-/commit/20b0f353ac4243b12ba27c87f6fac6997355ed89))

* renamed opaas to device_server ([`b2eb507`](https://gitlab.psi.ch/bec/bec/-/commit/b2eb50770adbb18f54e3210876900242aede0491))

* fixed ci file ([`a978678`](https://gitlab.psi.ch/bec/bec/-/commit/a978678c19d8c21ae3d5c6bb83a95c8ec40a4fbc))

* renamed koss to scan_server ([`b194c3b`](https://gitlab.psi.ch/bec/bec/-/commit/b194c3b63bc1d705853c85f1cfd59029354d970f))

* Merge branch &#39;progress_bar&#39; into &#39;master&#39;

bug fixes for mv

See merge request bec/bec!6 ([`e01d68a`](https://gitlab.psi.ch/bec/bec/-/commit/e01d68a24fdcb4f6cac2db512092fc50cd8a7374))

* fixed bug that caused mv not to send abort request ([`0ed4710`](https://gitlab.psi.ch/bec/bec/-/commit/0ed4710ac309d42cfb3dfc0016faaf256f64bb5f))

* fixed bug that caused mv to finish prematurely ([`3f1e4ca`](https://gitlab.psi.ch/bec/bec/-/commit/3f1e4ca4f0e6b9adf0224ab39736226ced4387a8))

* Merge branch &#39;progress_bar&#39; into &#39;master&#39;

bug fixes and cleanup

See merge request bec/bec!5 ([`d2829c0`](https://gitlab.psi.ch/bec/bec/-/commit/d2829c0539261c14a09572e9faab5ffcdd8c64f1))

* bug fixes and cleanup ([`d442604`](https://gitlab.psi.ch/bec/bec/-/commit/d442604b9bfc0069d7945cfa40be7f0b15a5c30e))

* Merge branch &#39;progress_bar&#39; into &#39;master&#39;

Progress bar; closes #28

Closes #22 and #28

See merge request bec/bec!4 ([`313797f`](https://gitlab.psi.ch/bec/bec/-/commit/313797f5df041edf3c187bfcdd7bb9beefb29c2d))

* move is now listening to req_done; closes #22 ([`0764797`](https://gitlab.psi.ch/bec/bec/-/commit/0764797570ff42485c427880a14d9a9cb3a5c94e))

* added progressbar ([`fbc0dba`](https://gitlab.psi.ch/bec/bec/-/commit/fbc0dbad9dd40c970dde3ceaabe495aa5e9e6f67))

* Merge branch &#39;master&#39; into progress_bar ([`f50a3b9`](https://gitlab.psi.ch/bec/bec/-/commit/f50a3b9e3e5fe23f1e4753dc94f71158d78b3fba))

* Merge branch &#39;config_updates&#39; into &#39;master&#39;

bug fixes for config updates

See merge request bec/bec!3 ([`c0986dc`](https://gitlab.psi.ch/bec/bec/-/commit/c0986dc2214976a09a5c9b64b04db31afc7e5f86))

* bug fixes for config updates ([`99c3c98`](https://gitlab.psi.ch/bec/bec/-/commit/99c3c982b1526e23537dc5131c6615e86d7c565e))

* added progressbar ([`7a16431`](https://gitlab.psi.ch/bec/bec/-/commit/7a16431f7e6fd197a0c531db8857b3fbba02a74c))

* Delete test_devicemanager.py ([`879a884`](https://gitlab.psi.ch/bec/bec/-/commit/879a884a1f52fc67e72ea4ed5026c8c171ac9142))

* naming (dm, qm) ([`0e12a58`](https://gitlab.psi.ch/bec/bec/-/commit/0e12a588d84dbf3b124c42039884fba5a67413b6))

* formatting ([`7afa33c`](https://gitlab.psi.ch/bec/bec/-/commit/7afa33c07cd13680dcc47f16d15863ff237c36c9))

* replaced ScanAcceptance with ScanRejection exception and ScanStatus object ([`34a03ad`](https://gitlab.psi.ch/bec/bec/-/commit/34a03ad3cd42822ee7a66326a905686ca40e5c00))

* refactor ([`d0a7d9e`](https://gitlab.psi.ch/bec/bec/-/commit/d0a7d9ed56ccc1a3718c74dd277fcf84bb4e1197))

* BMessage -&gt; BECMessage ([`116a813`](https://gitlab.psi.ch/bec/bec/-/commit/116a8137026052aac8ff43ff53336c60a0dff1ab))

* naming, refactor and comments ([`f074376`](https://gitlab.psi.ch/bec/bec/-/commit/f074376dd5345487ab39e26a50ec6f555237c617))

* renamed original ([`71c8e14`](https://gitlab.psi.ch/bec/bec/-/commit/71c8e14c800eaa40d4936b763b6514f0ade94ab7))

* comment ([`a1bf025`](https://gitlab.psi.ch/bec/bec/-/commit/a1bf025a9fba5f7865d59602fad460baaefe3dc7))

* re-wrote _update_available_scans; naming ([`d24d3cb`](https://gitlab.psi.ch/bec/bec/-/commit/d24d3cb397ac8677a16f077bb2dacff6f6dbd0b5))

* Update docker-compose.yaml; added redis ([`4804bb8`](https://gitlab.psi.ch/bec/bec/-/commit/4804bb8b7580d393aec69da23920304cc0bedc0b))

* Merge branch &#39;integ_tests&#39; into &#39;master&#39;

Integ tests

See merge request bec/bec!2 ([`714d5eb`](https://gitlab.psi.ch/bec/bec/-/commit/714d5ebe1333aaaa90252e5d6df0596eba0825e4))

* Integ tests ([`9c6f8f8`](https://gitlab.psi.ch/bec/bec/-/commit/9c6f8f8d61adaa630854b6d1531e3135f4c2d103))

* Merge branch &#39;config_updates&#39; into &#39;master&#39;

Config updates

Closes #5

See merge request bec/bec!1 ([`7862a93`](https://gitlab.psi.ch/bec/bec/-/commit/7862a9396f09d9e9bc54699e68bbd1dcd9c7f449))

* fixed tests ([`42767ef`](https://gitlab.psi.ch/bec/bec/-/commit/42767ef4b65e21d5b887a537f3c36a45e7d348b5))

* added support for enabling/disabling devices ([`2952a70`](https://gitlab.psi.ch/bec/bec/-/commit/2952a70516838b1617561c85b12bd265d3d3ac57))

* cleanup ([`638d300`](https://gitlab.psi.ch/bec/bec/-/commit/638d300bcca2d5abacff2ae4bbf774e3138d5c8f))

* added config update; closes #5 ([`ca11295`](https://gitlab.psi.ch/bec/bec/-/commit/ca11295d4ac7538de5da244f1b8a116601559689))

* added config update in opaas ([`3de5117`](https://gitlab.psi.ch/bec/bec/-/commit/3de51173fa813ae8f02189c571d27fcb4b348b88))

* import sorting ([`fe6dd17`](https://gitlab.psi.ch/bec/bec/-/commit/fe6dd176a84e59c08f25f78ab471711fd2ff7aff))

* replaced print commands by logger ([`eaf749e`](https://gitlab.psi.ch/bec/bec/-/commit/eaf749e246a7a2113b242659438dfa9377596c07))

* uncaught excpections in a connector thread are now killing the main thread and raised again ([`bf62081`](https://gitlab.psi.ch/bec/bec/-/commit/bf62081c9fe8cfa6238bf3e03be394bce0b2f642))

* cleanup ([`8b840a4`](https://gitlab.psi.ch/bec/bec/-/commit/8b840a43c46cb1ba188af9761e6476d62ca7fa9d))

* added missing packages to client ([`9ed2336`](https://gitlab.psi.ch/bec/bec/-/commit/9ed2336584d1cfd9ad93f848bea5c3a6e30a0126))

* added missing file_writer files ([`ed27ea3`](https://gitlab.psi.ch/bec/bec/-/commit/ed27ea3fff6cd4d35303eccd7fec1eaba4d711e5))

* added file_writer ([`1f1f07b`](https://gitlab.psi.ch/bec/bec/-/commit/1f1f07bd93cc10cda861ed70443c1a3373da9f6f))

* added elapsed time ([`7ea91a4`](https://gitlab.psi.ch/bec/bec/-/commit/7ea91a42e440cd0e2c4c6ca718179b9def9a8d6d))

* fixed formatting ([`09d8bc9`](https://gitlab.psi.ch/bec/bec/-/commit/09d8bc9231741afe6f1778d000d127f7be70835f))

* added device_access param ([`8fa9990`](https://gitlab.psi.ch/bec/bec/-/commit/8fa9990fc3f7b75640071a44413410c85f9f0187))

* Merge branch &#39;master&#39; of https://gitlab.psi.ch/bec/bec ([`1552d97`](https://gitlab.psi.ch/bec/bec/-/commit/1552d97874621d2add1480a62c40c98ff9048db2))

* added traceback to rpc error messages ([`18e5bf1`](https://gitlab.psi.ch/bec/bec/-/commit/18e5bf1abecd7566a179c57b54528802cca35516))

* fixed rpc calls with func args; closes #17 ([`efc9544`](https://gitlab.psi.ch/bec/bec/-/commit/efc9544a89f7d7811c63adaba15d09bc3c9c0978))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`0c4d823`](https://gitlab.psi.ch/bec/bec/-/commit/0c4d823a5ae398b6568044052652d886878826cf))

* moved req_done sub to status finished ([`ecbaeed`](https://gitlab.psi.ch/bec/bec/-/commit/ecbaeedc40a07709a2259c29000aa9a1f484dd28))

* added smaract ([`d0a080b`](https://gitlab.psi.ch/bec/bec/-/commit/d0a080bc6e2b276f0b7bb33dbb4992f0cfe990c3))

* temporaliy disabled func args for rpc calls ([`3cd6d38`](https://gitlab.psi.ch/bec/bec/-/commit/3cd6d381c4887622152df4f40024d9a7ad6796a5))

* fixed bug in device filtering ([`57233d6`](https://gitlab.psi.ch/bec/bec/-/commit/57233d648441f6fe2251cb93d117d855a3bd0d6c))

* ensured that scan motors are shown at the beginning ([`6a260eb`](https://gitlab.psi.ch/bec/bec/-/commit/6a260eb7eec9d6067b03a18bdb3d3ebd8258555b))

* added req_done subscriptions and corresponding alarm messages; improvements to clients alarm handling ([`c0409a1`](https://gitlab.psi.ch/bec/bec/-/commit/c0409a11f2a540510be965adb3869d185a959dc7))

* added tolerances ([`3e841e8`](https://gitlab.psi.ch/bec/bec/-/commit/3e841e821b261e9ca293b36f15833b78db773ed6))

* added tests for cleaning up the queue ([`1b06d4d`](https://gitlab.psi.ch/bec/bec/-/commit/1b06d4d788870741076671d966559f81eb485bdf))

* Merge branch &#39;master&#39; of gitlab.psi.ch:bec/bec ([`8585001`](https://gitlab.psi.ch/bec/bec/-/commit/85850013bd480218bb0ef8e8c383cd6fe6ca5c11))

* Update .gitlab-ci.yml ([`0e83d6a`](https://gitlab.psi.ch/bec/bec/-/commit/0e83d6a4ed9efd72a6549689c3deeb2ca4d3537c))

* Update .gitlab-ci.yml ([`419ada6`](https://gitlab.psi.ch/bec/bec/-/commit/419ada6d9d0b3b85fe27c3d09cd8c02a395d4fb7))

* fixed queue cleanup; closes #14 ([`08392f4`](https://gitlab.psi.ch/bec/bec/-/commit/08392f425eb6dac58b05cddf765611be74eb66a4))

* removed unused imports ([`ac17b4a`](https://gitlab.psi.ch/bec/bec/-/commit/ac17b4a9fe84d5b1e1d0e52e4d52ead8dd35e6f5))

* added rpc for custom user access; closes #16 ([`a8efe36`](https://gitlab.psi.ch/bec/bec/-/commit/a8efe36d50a1168a42347a864f6a66e63c4cfc95))

* added setup files ([`5672728`](https://gitlab.psi.ch/bec/bec/-/commit/56727286feb30f07ff1e44cf9ee178768cdf397b))

* renamed KMessage to BMessage ([`b1f2332`](https://gitlab.psi.ch/bec/bec/-/commit/b1f2332576cda9e39004aea2a4e3886cc9002e6c))

* removed outdated kafka and rabbitmq dependencies ([`6a6c344`](https://gitlab.psi.ch/bec/bec/-/commit/6a6c344f0eb21b1dea634875bf32bc4215039a78))

* renamed kafkamessage to becmessage ([`7524d9b`](https://gitlab.psi.ch/bec/bec/-/commit/7524d9b80b6d0af7348025ce18aaaa8e976c5153))

* removed outdated req. for client ([`cc6a6d2`](https://gitlab.psi.ch/bec/bec/-/commit/cc6a6d22800969fedcea32352b763bdf408c8921))

* fixed pre-commit for deleted files ([`79015e0`](https://gitlab.psi.ch/bec/bec/-/commit/79015e0a0fb98a17516bf7f2d7bd3267cb6a5881))

* renamed utils ([`1d568bc`](https://gitlab.psi.ch/bec/bec/-/commit/1d568bcea6f793c6c6719ba04ae4f26fc791f0c6))

* renamed bluekafka to bec ([`59059ea`](https://gitlab.psi.ch/bec/bec/-/commit/59059eaee28d534021ed984383e6fcaf99f56d21))

* added more files ([`bde409e`](https://gitlab.psi.ch/bec/bec/-/commit/bde409e4d22e59538f40aa219b12c05821435e07))

* export from internal git ([`f9d8159`](https://gitlab.psi.ch/bec/bec/-/commit/f9d81597cb6719e8f0fafff64cace7318be98251))

* Initial commit ([`61dca79`](https://gitlab.psi.ch/bec/bec/-/commit/61dca7923588597b553822022c271bfa36b4dd0a))
