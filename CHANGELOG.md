# CHANGELOG

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
