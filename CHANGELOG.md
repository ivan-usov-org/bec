# CHANGELOG

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
