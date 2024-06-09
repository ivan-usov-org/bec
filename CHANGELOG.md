# CHANGELOG



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
