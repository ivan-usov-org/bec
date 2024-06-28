# CHANGELOG

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
