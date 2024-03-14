# Changelog

<!--next-version-placeholder-->

## v1.14.5 (2024-03-14)

### Fix

* **bec_lib:** Fixed status timeout ([`c4f0a18`](https://gitlab.psi.ch/bec/bec/-/commit/c4f0a18e7317caf54e95e7c7b1f09bf033e65380))

### Documentation

* **bec_lib:** Improved doc string for device module ([`c605846`](https://gitlab.psi.ch/bec/bec/-/commit/c605846adeee080dbdecd55d5f758e2acd884d83))
* **bec_lib:** Added module docs ([`7031c24`](https://gitlab.psi.ch/bec/bec/-/commit/7031c2483163eb3268760b5ecd4888c9c5b6b372))

## v1.14.4 (2024-03-12)

### Fix

* **bec_lib:** Don't call rpc on jedi completer ([`8a6a968`](https://gitlab.psi.ch/bec/bec/-/commit/8a6a968cc8c31fbb5fb20ce872b8bbdc76039ee8))
* **bec_lib:** Added tab complete for property vars ([`ef531d0`](https://gitlab.psi.ch/bec/bec/-/commit/ef531d0d4a1848ac5917b56eebea385fac9b7a4c))

### Documentation

* Updated readme ([`c490574`](https://gitlab.psi.ch/bec/bec/-/commit/c490574b9bafc217bf29bec9b087fa75c50abab6))

## v1.14.3 (2024-03-12)

### Fix

* **bec_lib:** Fixed dataset number setter ([`5dcffe0`](https://gitlab.psi.ch/bec/bec/-/commit/5dcffe022c2a5d2c1e2cb50265f5d0b1cefe547a))

## v1.14.2 (2024-03-12)

### Fix

* Remove debug prints from livetable ([`7efb387`](https://gitlab.psi.ch/bec/bec/-/commit/7efb3878d8687ba4e747c99e517d4c6df40c6965))
* Add recovery_config files to .gitignore ([`6201757`](https://gitlab.psi.ch/bec/bec/-/commit/62017574baea74dfff5f4d13ea1d1886ee6581a8))

## v1.14.1 (2024-03-11)

### Fix

* **scan_server:** Added cm for preventing race conditions within queue updates ([`b98dd52`](https://gitlab.psi.ch/bec/bec/-/commit/b98dd52d6ac4bce23c0916028810340e1af74649))

## v1.14.0 (2024-03-10)

### Feature

* Added support for computed signals ([`720d6e2`](https://gitlab.psi.ch/bec/bec/-/commit/720d6e210df11071f0d5c30442e6e50e34833844))

### Fix

* **bec_lib:** Fixed signal update ([`689e2d9`](https://gitlab.psi.ch/bec/bec/-/commit/689e2d968c4967bcaf8d19e2756997898671bf79))
* **scihub:** Rejected config should raise ([`af2e4c5`](https://gitlab.psi.ch/bec/bec/-/commit/af2e4c58e1143b39e58f5e4f292d66dfcd36123f))

## v1.13.3 (2024-03-10)

### Fix

* **bec_lib:** Fixed bug that caused data to be modified when using xadd; closes #220 ([`3dbb8a0`](https://gitlab.psi.ch/bec/bec/-/commit/3dbb8a00a1439e3030d9406a223040ef99cb60a8))

## v1.13.2 (2024-03-10)

### Fix

* **bec_lib:** Shutdown loguru ([`3f8d655`](https://gitlab.psi.ch/bec/bec/-/commit/3f8d655b2e199268bd23746fd0fe96bc316fcb8c))
* **bec_lib:** Daemonized connector threads ([`be1f3fd`](https://gitlab.psi.ch/bec/bec/-/commit/be1f3fd140af8fdf6216f41b92e92ed9126d3791))

## v1.13.1 (2024-03-10)

### Fix

* **scan_server:** Fixed flomni init; added tests ([`a3ceac7`](https://gitlab.psi.ch/bec/bec/-/commit/a3ceac7a95f593da23575aaf60693519d4789764))

## v1.13.0 (2024-03-10)

### Feature

* Remove asyncio from BECIPythonclient to support jupyter notebook output for progressbar ([`f9c1e81`](https://gitlab.psi.ch/bec/bec/-/commit/f9c1e818e0c1aa43947c6c82e052af3f162338fa))

## v1.12.9 (2024-03-06)

### Fix

* **bec_lib:** Fixed support for lists in redis stream subscriptions ([`d4b7b42`](https://gitlab.psi.ch/bec/bec/-/commit/d4b7b42f4608464da417435350a0c73f7665a44f))
* **bec_lib:** Added missing unsubscribe from streams ([`75cd651`](https://gitlab.psi.ch/bec/bec/-/commit/75cd6512ea4e0b00ad320d16f4298ca9f79d8105))
* **bec_lib:** Fixed support for redis streams ([`7578395`](https://gitlab.psi.ch/bec/bec/-/commit/757839534c75bd3a8110256cdfd770f770a195e0))

### Documentation

* **bec_lib:** Improved endpoint doc strings ([`656478f`](https://gitlab.psi.ch/bec/bec/-/commit/656478f784440b91ada8fb1da1d3957276079765))
* **bec_lib:** Updated doc strings ([`969b0a0`](https://gitlab.psi.ch/bec/bec/-/commit/969b0a02f842a8d9666277fa5c4cc98344b8b0f6))

## v1.12.8 (2024-03-06)

### Fix

* Added backward compatibility for scan numbers and dataset numbers ([`9ff2278`](https://gitlab.psi.ch/bec/bec/-/commit/9ff2278c38b9fcb671c5591f15fda9473155fbe3))
* Account is now a variablemessage ([`79d57b5`](https://gitlab.psi.ch/bec/bec/-/commit/79d57b509d20451c73a0442adf477ae4299e9dc6))
* Pre-scan macros are now using a VariableMessage ([`4239576`](https://gitlab.psi.ch/bec/bec/-/commit/4239576c94c44041f395261b42de1056de8c0d76))
* Logbook is now using a credentialsmessage ([`b62960f`](https://gitlab.psi.ch/bec/bec/-/commit/b62960f6e697b116ffc4f3c5fded0c6bcd9ea4e2))
* Scan_number and dataset_number is now a VariableMessage ([`f698605`](https://gitlab.psi.ch/bec/bec/-/commit/f698605579766536f1ec1e653e9d5e3dfd44166e))

### Documentation

* Updated contributing.md ([`af2bd27`](https://gitlab.psi.ch/bec/bec/-/commit/af2bd273d510f08f420f39ec519d1a97ac8a1cb1))
* Typo ([`4ac0bbc`](https://gitlab.psi.ch/bec/bec/-/commit/4ac0bbca1631ed5226458307f7ad35d155617328))
* Fixed last comments ([`aadbb01`](https://gitlab.psi.ch/bec/bec/-/commit/aadbb01a947ae5419dff7c18837ab8ea9b75d78c))
* Adress comments ([`d556f84`](https://gitlab.psi.ch/bec/bec/-/commit/d556f842353e7ef335309fb42025d00de193b627))
* Update documentation on the simulation ([`0ec3dac`](https://gitlab.psi.ch/bec/bec/-/commit/0ec3dac85fd03413c2cf79b5881e8dffbecd2877))

## v1.12.7 (2024-03-04)

### Fix

* **scihub:** Fixed scibec upload for large scans ([`2b680ee`](https://gitlab.psi.ch/bec/bec/-/commit/2b680eee1ea51c1875ef8e1fea9f3135a3e52899))

## v1.12.6 (2024-03-01)

### Fix

* Fix dap test, cleanup redudant config values ([`4f63fef`](https://gitlab.psi.ch/bec/bec/-/commit/4f63fef18c512eadbf339629e9780b82d878ea37))

## v1.12.5 (2024-03-01)

### Fix

* **scan_server:** Fixed queue pop for pending requests ([`14f94cd`](https://gitlab.psi.ch/bec/bec/-/commit/14f94cd96071feb0885b010af7576532baea553e))

## v1.12.4 (2024-02-27)

### Fix

* **bec_lib:** Exclude disabled devices in device filters ([`388baae`](https://gitlab.psi.ch/bec/bec/-/commit/388baae9f117120f4f3db29e0c0db03cbb78b54c))

## v1.12.3 (2024-02-27)

### Fix

* **scan_server:** Stage should only include monitored, baseline and async devices ([`05a83bd`](https://gitlab.psi.ch/bec/bec/-/commit/05a83bd4ac1fe898863f24bac1a139da0836a46a))

## v1.12.2 (2024-02-26)

### Fix

* **disconnection:** Mitigate effects on disconnection from redis ([`4d73cf8`](https://gitlab.psi.ch/bec/bec/-/commit/4d73cf8a071493ec997ca08efc8518672c7f5034))
* **redis_connector:** Add producer(), consumer() for compatibility with old code ([`f60a012`](https://gitlab.psi.ch/bec/bec/-/commit/f60a012ef6453742bb8c830e479325bfb9254b87))
* **scan_manager:** Ensure robustness in __str__ ([`db53b1f`](https://gitlab.psi.ch/bec/bec/-/commit/db53b1f5dc73279c6764d1f4dd875f32304d1f5d))
* **tests:** Ensure redis is installed ([`bbd036e`](https://gitlab.psi.ch/bec/bec/-/commit/bbd036e769bb6093d1890fceb23e005baa644888))

## v1.12.1 (2024-02-24)

### Fix

* **scan_server:** Fixed expected message type for device progress update ([`1236069`](https://gitlab.psi.ch/bec/bec/-/commit/1236069b3604607288f9f0e1dccd3994d014f928))

## v1.12.0 (2024-02-24)

### Feature

* Added flomni scan and user scripts ([`c376de8`](https://gitlab.psi.ch/bec/bec/-/commit/c376de8e8436380f65ba96b2e88572077830f1d9))

## v1.11.1 (2024-02-23)

### Fix

* **scan_bundler:** Fixed scan bundler update ([`2e5b147`](https://gitlab.psi.ch/bec/bec/-/commit/2e5b147a2c9ccd6ca7169f45f0431ed1df902b0f))
* **scan_server:** Reverted changes to monitor scan ([`636e060`](https://gitlab.psi.ch/bec/bec/-/commit/636e0609f2d05ea079661872858084b3f9b3847e))
* **file_writer:** Fixed data update ([`16f8f30`](https://gitlab.psi.ch/bec/bec/-/commit/16f8f30ea6fc15173abbfccee65b869018659bca))
* **scan_server:** Fixed inheritance for flyers ([`5f80220`](https://gitlab.psi.ch/bec/bec/-/commit/5f80220fa2d062112dd5770b3485dd478ead63f8))

## v1.11.0 (2024-02-23)

### Feature

* Add Ophyd DeviceProxy to backend for simulation framework, delayed init of proxies ([`d37c5e7`](https://gitlab.psi.ch/bec/bec/-/commit/d37c5e739120baad5ffef22888ba264a74663e63))

## v1.10.0 (2024-02-23)

### Feature

* **scihub:** Added config reply handler for device_server updates ([`29a1d19`](https://gitlab.psi.ch/bec/bec/-/commit/29a1d19504d6cbfb4a4601106d5341aadb0f43f7))
* **device_server:** Connection errors and init errors are separated and forwarded ([`c2214b8`](https://gitlab.psi.ch/bec/bec/-/commit/c2214b86468a2ac590ee3fd5eda19734dbac1c26))
* **bec_lib:** Report on failed devices; save recovery file to disk ([`8062503`](https://gitlab.psi.ch/bec/bec/-/commit/806250300e472a780329e6438c1891565481d8f7))
* **bec_lib:** Added config history endpoint ([`ee7ecef`](https://gitlab.psi.ch/bec/bec/-/commit/ee7ecef8d52320356f2190620bc3e42fa37db304))

### Fix

* **bec_lib:** Fixed service init ([`b09b5ff`](https://gitlab.psi.ch/bec/bec/-/commit/b09b5ff7cddd0d13c6c4a2d55d00914b131e59fd))
* **bec_lib:** Fix after refactoring ([`0337f13`](https://gitlab.psi.ch/bec/bec/-/commit/0337f13d0453ca1fac77413d757746f2bc06eb95))
* **scihub:** Added updated config flag to detect failed validations ([`3a133bf`](https://gitlab.psi.ch/bec/bec/-/commit/3a133bf7d44a9578587e5bbee484183a21e9cc7c))
* **bec_lib:** Fixed config helper for failed config updates ([`f603419`](https://gitlab.psi.ch/bec/bec/-/commit/f6034191f5763495130cab25edc5d600d0da274d))
* **bec_lib:** Fixed bl_checks cleanup ([`05b00da`](https://gitlab.psi.ch/bec/bec/-/commit/05b00dadbbabffc5efd32e9621336e335564db76))
* **bec_lib:** Fixed service id assignment ([`3826d41`](https://gitlab.psi.ch/bec/bec/-/commit/3826d410527177acce339e307a17c2943a921aa4))
* **bec_lib:** Save guard device manager init ([`fcbc240`](https://gitlab.psi.ch/bec/bec/-/commit/fcbc2402e437a756c11b09f5d1ce9a5351a0cc54))

## v1.9.0 (2024-02-22)

### Feature

* **bec_lib:** Added json serializer ([`25366c0`](https://gitlab.psi.ch/bec/bec/-/commit/25366c09638cf4e005ee4a75d64cf8f9eeba00ca))

### Fix

* **scihub:** Fixed data serialization before upload to scibec ([`eae1d61`](https://gitlab.psi.ch/bec/bec/-/commit/eae1d617d6c44a933e7e86ea86e35d380d323f6a))
* **scihub:** Fixed error handling ([`fd3cb02`](https://gitlab.psi.ch/bec/bec/-/commit/fd3cb025c50c61f3384d44abc8c234371952d731))

## v1.8.0 (2024-02-20)

### Feature

* **bec_lib:** Added async data handler ([`da46c27`](https://gitlab.psi.ch/bec/bec/-/commit/da46c278425fe31aa2a597c9d55065653ae63fbd))

### Fix

* **bec_lib:** Fixed typo in xrange ([`0fe0a6e`](https://gitlab.psi.ch/bec/bec/-/commit/0fe0a6e119ed01ebb38ac0b07c05d7f42a19ecf3))

### Documentation

* **developer:** Added instructions on how to set up vscode ([`94d63e6`](https://gitlab.psi.ch/bec/bec/-/commit/94d63e60b754a926e953208b325b943aa2c387e8))

## v1.7.3 (2024-02-19)

### Fix

* **rpc:** Fixed rpc calls with empty list as return value ([`a781369`](https://gitlab.psi.ch/bec/bec/-/commit/a781369e469a1196b7e88c6fa3593ee40439ec1e))

## v1.7.2 (2024-02-19)

### Fix

* **endpoints:** Added gui_instruction_response endpoint ([`9a838bb`](https://gitlab.psi.ch/bec/bec/-/commit/9a838bbe8e7fab974982654bdc9f69a14edf7a20))
* **live_table:** Fixed live table for string values ([`3b04d31`](https://gitlab.psi.ch/bec/bec/-/commit/3b04d319f9f8d56a8e8c2d6fec9802cc7e747ad3))

## v1.7.1 (2024-02-16)

### Fix

* **bec_lib.device:** Made device.position a property to be compliant with ophyd ([`4060b86`](https://gitlab.psi.ch/bec/bec/-/commit/4060b8651b99e3e86e440bcd02d148722ea5403b))

## v1.7.0 (2024-02-14)

### Feature

* **scan_worker:** Emitted readout priority contains all devices, not just the modification ([`21187ad`](https://gitlab.psi.ch/bec/bec/-/commit/21187adb48495422aa9c0f0adbeeaa23b2d6c8a5))
* **devicemanager:** Added filter methods for continuous and on_request devices ([`708aaff`](https://gitlab.psi.ch/bec/bec/-/commit/708aaff918e7e858c3c1070057a17cedab248c88))

### Fix

* **devicemanager:** Fixed bug after refactoring ([`37a58ef`](https://gitlab.psi.ch/bec/bec/-/commit/37a58ef5ce83a1c1a4a483c07e08e4f5dd437dda))

## v1.6.0 (2024-02-14)

### Feature

* **file_writer:** Added support for user-defined file suffixes ([`505df05`](https://gitlab.psi.ch/bec/bec/-/commit/505df053c1b5801cc86e5e6d1f3e58a94edeaf22))

## v1.5.1 (2024-02-14)

### Fix

* **dap:** Dap service should now raise on unknown dap service cls; another provider may be responsible for it ([`85969f5`](https://gitlab.psi.ch/bec/bec/-/commit/85969f5d5393166996dbabbeefc06ef464576ee5))

## v1.5.0 (2024-02-13)

### Feature

* **scan_data:** Added baseline data ([`41bf2d1`](https://gitlab.psi.ch/bec/bec/-/commit/41bf2d1bd4d139f801d36d8cb4a0f9c837ac5d09))

### Fix

* **bluesky_emitter:** Fixed device info access ([`06b2373`](https://gitlab.psi.ch/bec/bec/-/commit/06b2373fea588433026079ed3d0a5b140d3f57f9))
* **scan_bundler:** Added metadata to baseline reading ([`9294562`](https://gitlab.psi.ch/bec/bec/-/commit/9294562f3bb377531f2fc558a655e8f7016feb38))
* **scan_manager:** Added baseline consumer ([`ce9681c`](https://gitlab.psi.ch/bec/bec/-/commit/ce9681c1859fd56c82bab206c8886f2851e4cc5d))

## v1.4.0 (2024-02-13)

### Feature

* Added support for customized lmfit params ([`f175fd7`](https://gitlab.psi.ch/bec/bec/-/commit/f175fd7c55b82dbb0d8b080ee8a93cd8be52d816))

### Fix

* **dap:** Output fit is fitted to full scope, not only the trimmed ([`58f3cb1`](https://gitlab.psi.ch/bec/bec/-/commit/58f3cb17209acbae58720bcb1d6e8ec3bac28162))

### Documentation

* **plugins:** Added plugin docs ([`c14c526`](https://gitlab.psi.ch/bec/bec/-/commit/c14c526a85a9e67e1bca866fcae749975acc5f30))

## v1.3.0 (2024-02-12)

### Feature

* **dap:** Added option to filter x range before fitting data ([`7068c1f`](https://gitlab.psi.ch/bec/bec/-/commit/7068c1f738d9876ef13cb62d797ba15fada3bd98))
* **dap:** Added input_data and plot options ([`c4029a0`](https://gitlab.psi.ch/bec/bec/-/commit/c4029a098db66baf1741bf4bcc1bbd71d14aca7f))
* **DAP:** Added option to customize results based on the dap service ([`dd48519`](https://gitlab.psi.ch/bec/bec/-/commit/dd4851941c14b1ace0227ab3ff28b50826c22f89))
* Added support for customized dap plugins objects ([`cf8430f`](https://gitlab.psi.ch/bec/bec/-/commit/cf8430f8787c8028d518c17fea5f00aba6e94093))

### Fix

* **dap:** Added input into to the dap metadata ([`0156f61`](https://gitlab.psi.ch/bec/bec/-/commit/0156f611f110f5ae31e163b9630d19a4112e98d0))

### Documentation

* **dap:** Added data fitting to user docs ([`b881b08`](https://gitlab.psi.ch/bec/bec/-/commit/b881b081726c659056c5120e0a71e09d41ef8881))
* Fixed typo ophyd.md ([`c1f4b38`](https://gitlab.psi.ch/bec/bec/-/commit/c1f4b388032689cf4f2d9492f6e49d32851b6035))
* **ophyd:** Fixed ophyd config description ([`6a272de`](https://gitlab.psi.ch/bec/bec/-/commit/6a272dede1d23ac7af9bb158105b2d5eb2c7445b))

## v1.2.1 (2024-02-10)

### Fix

* **compat python 3.11:** Ensure "kind" test works for numbers too ([`697ae59`](https://gitlab.psi.ch/bec/bec/-/commit/697ae59a6671aba27c098460e0d4ab59de62187d))

## v1.2.0 (2024-02-09)

### Feature

* **bec_lib.utils:** Add user_access decorator to bec_lib.utils. ([`0b309ce`](https://gitlab.psi.ch/bec/bec/-/commit/0b309ce8887b40cf907b19421adbbd47f30a8207))

## v1.1.3 (2024-02-09)

### Fix

* **serializer:** Fixed serialization for set ([`bcd2e06`](https://gitlab.psi.ch/bec/bec/-/commit/bcd2e06449923b0f2f92f64703a70e6de99e72d2))

## v1.1.2 (2024-02-09)

### Fix

* Fixed xread decoding ([`c684a76`](https://gitlab.psi.ch/bec/bec/-/commit/c684a76a5eff0bf478121dcde25e9e4447e839dc))
* Fixed init config script ([`f0f9fe3`](https://gitlab.psi.ch/bec/bec/-/commit/f0f9fe304f24cb61053ce12d785b82745a14210e))
* Removed outdated msgpack packing ([`15f8e21`](https://gitlab.psi.ch/bec/bec/-/commit/15f8e213053a635da4ed8d54bcb562a690e71517))
* **redis_connector:** Encode/decode stream data ([`a7bafa6`](https://gitlab.psi.ch/bec/bec/-/commit/a7bafa6a0c99395068ef090d149732b4fa4f5eb5))
* **serialization:** Move BECMessage check in .loads() in the BEC message decoder ([`de8333b`](https://gitlab.psi.ch/bec/bec/-/commit/de8333b164033ff0c0a300278e5494f5cc8f7879))

## v1.1.1 (2024-02-08)

### Fix

* Bugfix for .put and cached readback, ([`880eb77`](https://gitlab.psi.ch/bec/bec/-/commit/880eb77fd0a065cadde14bc33294b069d16fd0c6))

## v1.1.0 (2024-02-08)

### Feature

* Lmfit serializer ([`ed679bb`](https://gitlab.psi.ch/bec/bec/-/commit/ed679bb6650dcd7d77ebbe16212745ac985eeba8))
* Dap services ([`2b08662`](https://gitlab.psi.ch/bec/bec/-/commit/2b08662c08baf89ecbbd051a428914b78bbbcd97))
* Added dap endpoints and messages ([`6dc09cf`](https://gitlab.psi.ch/bec/bec/-/commit/6dc09cf6e5ea26f8b64e266776322cbee19550bc))

### Fix

* Fixed support for scan items as args ([`b15e38b`](https://gitlab.psi.ch/bec/bec/-/commit/b15e38bd39511e09ed4e456843e54e755a1c10ce))
* Fixed typo ([`4c8dd55`](https://gitlab.psi.ch/bec/bec/-/commit/4c8dd5570cde952a24b60ac4a9eb6227d2b5d364))
* Preliminary fix for missing xadd serialization ([`11b8326`](https://gitlab.psi.ch/bec/bec/-/commit/11b8326393e0b21f0f2ad140c826af18619193f0))
* Fixed scan_data for .get default values ([`aa403c4`](https://gitlab.psi.ch/bec/bec/-/commit/aa403c4a53a7c2462d623097a2f3275f2e7c1c90))
* Fixed dataclass for availableresourcemessage ([`cfc5237`](https://gitlab.psi.ch/bec/bec/-/commit/cfc5237025806d91eb32f2ebe135e2ddb55e8c1a))
* Fixed multiple model imports ([`a5f1447`](https://gitlab.psi.ch/bec/bec/-/commit/a5f1447c8734f88734f9828753f7bfd567128b8e))
* Fixed plugin handling for multiple service provider ([`ef4b66f`](https://gitlab.psi.ch/bec/bec/-/commit/ef4b66fd928600e40c06880cba807e667b1b4ed2))
* Fixed support for multiple dap services ([`e2595bc`](https://gitlab.psi.ch/bec/bec/-/commit/e2595bc22535de384d2747bbb5d4c225507f2a11))
* Accept args, kwargs in new client ([`47f4ecf`](https://gitlab.psi.ch/bec/bec/-/commit/47f4ecff540e03004ad16afaa6d11150efd0d3ba))
* Use service id property for status updates ([`5d33146`](https://gitlab.psi.ch/bec/bec/-/commit/5d33146b0cf7e6f9f23f98275e2697459d3692dd))
* Fixed dap loading ([`0c71b5f`](https://gitlab.psi.ch/bec/bec/-/commit/0c71b5f7c2c7d198ced36de9ced40bf99287025a))
* Fixed xread ([`f1219ae`](https://gitlab.psi.ch/bec/bec/-/commit/f1219ae0f051a872bdbb6e5d5e68c8e8b16232ea))
* Fixed xread when no id is specified ([`4a42277`](https://gitlab.psi.ch/bec/bec/-/commit/4a4227731ffeb117f4a5b8fb5f3ce6045f1f8eb8))
* Improved error handling for scihub ([`5d8028d`](https://gitlab.psi.ch/bec/bec/-/commit/5d8028db6bb9c510a8738ddba1545797b07dd7eb))

## v1.0.0 (2024-02-07)

### Fix

* **messages:** Set msg_type of ScanQueueMessage to "scan_queue_message" ([`8b125a0`](https://gitlab.psi.ch/bec/bec/-/commit/8b125a05b95084c676552c483b4d35eaa45724a2))
* **AlarmMessage:** Content member (dict) changed to msg (str) ([`3d087ef`](https://gitlab.psi.ch/bec/bec/-/commit/3d087ef87d1480ff4c96873e658441a833f477c6))
* **global var:** Remove builtins.__BEC_SERVICE__ ([`80fddc5`](https://gitlab.psi.ch/bec/bec/-/commit/80fddc5a4c3ec16d0ac464c79dcfba6bf449242e))
* **scan_manager:** Publish available scans using a BECMessage ([`ac5fafc`](https://gitlab.psi.ch/bec/bec/-/commit/ac5fafc7fa30dc8006edb7554c9e261c30edc9a0))

### Breaking

* content member (dict) changed to msg (str) ([`3d087ef`](https://gitlab.psi.ch/bec/bec/-/commit/3d087ef87d1480ff4c96873e658441a833f477c6))
* messages refactoring, new serialization module ([`8bbfd10`](https://gitlab.psi.ch/bec/bec/-/commit/8bbfd10ca7db4b8376478a421633fe3e94cd9f0e))
* remove builtins.__BEC_SERVICE__ ([`80fddc5`](https://gitlab.psi.ch/bec/bec/-/commit/80fddc5a4c3ec16d0ac464c79dcfba6bf449242e))

## v0.61.0 (2024-02-06)

### Feature

* **ipython:** Represent objects using '__str__' rather than '__repr__' ([`1e2af9a`](https://gitlab.psi.ch/bec/bec/-/commit/1e2af9ae519382fe490162dff60b1056b9f50fdf))

### Fix

* **flake8:** Apply flake8 to fix inconsistencies ([`2eafba9`](https://gitlab.psi.ch/bec/bec/-/commit/2eafba951ae7180131bebf705466cdb2968bddba))

## v0.60.3 (2024-02-05)

### Fix

* Scan_to_csv can handle ScanReport and ScanItem, runs on multiple scans; closes #80, #104 ([`1ff19a1`](https://gitlab.psi.ch/bec/bec/-/commit/1ff19a156d9614fb1d9583c28d8181341ad5ebb4))

### Documentation

* Fixed docstrings ([`f1e8662`](https://gitlab.psi.ch/bec/bec/-/commit/f1e86627773659b76b8cff199709611d23a0c558))
* Complement documentation ([`b4ac84a`](https://gitlab.psi.ch/bec/bec/-/commit/b4ac84a960db767eed0d6686ab242d52e7c3ac06))
* Updated landing page readme ([`c30eb2e`](https://gitlab.psi.ch/bec/bec/-/commit/c30eb2e67e89542d87a7aef8d7e445165f827239))
* Added references to the user guide ([`a25c4b2`](https://gitlab.psi.ch/bec/bec/-/commit/a25c4b2bb0ef7d98ef72c0bfefd6b435d4bb1db0))

## v0.60.2 (2024-02-02)

### Fix

* Fixed scihub shutdown procedure ([`dfc6dd4`](https://gitlab.psi.ch/bec/bec/-/commit/dfc6dd4aaba1d5a9fcda51b2e8d30e9a431f237f))

## v0.60.1 (2024-02-02)

### Fix

* Fixed serializer for 3.9 ([`5c6f250`](https://gitlab.psi.ch/bec/bec/-/commit/5c6f250950438deccfe61dadaf6f2224ebae6243))
* Fixed signature serializer for union operator; cleanup ([`4dd682b`](https://gitlab.psi.ch/bec/bec/-/commit/4dd682b3e7aaae1c40ed775554496c674f44658e))

## v0.60.0 (2024-02-01)

### Feature

* **run environment:** Allow to run service using the current Conda environment, if any ([`4b3bb4a`](https://gitlab.psi.ch/bec/bec/-/commit/4b3bb4a2a87d2d3024637500ad00e13dca80cac2))

## v0.59.6 (2024-02-01)

### Fix

* Fixed scibec login update ([`f1d8faf`](https://gitlab.psi.ch/bec/bec/-/commit/f1d8fafeaf3fd961fb4e3fa07a845a037fc27d1b))

## v0.59.5 (2024-01-31)

### Fix

* Fixed get_software_triggered_devices to excluded disabled devices, complement test case ([`37e74dc`](https://gitlab.psi.ch/bec/bec/-/commit/37e74dc206e906a15d19a261fc768b86d70cfdc1))

## v0.59.4 (2024-01-31)

### Fix

* Fixed event name for scan status callbacks ([`ed43260`](https://gitlab.psi.ch/bec/bec/-/commit/ed43260b60297d4e6b8dddc8c853b53b653c9ce1))

## v0.59.3 (2024-01-30)

### Fix

* Fixed rpc calls on device properties ([`f778302`](https://gitlab.psi.ch/bec/bec/-/commit/f77830296605e64c66b9ae3c8c9d760db720fe23))

## v0.59.2 (2024-01-30)

### Fix

* Added put as trigger for an update of the config cache ([`5f19da9`](https://gitlab.psi.ch/bec/bec/-/commit/5f19da921eafab72d0f64f437e4d49fa7afff988))
* Fixed status callback for cbs where the device is passed on ([`d110711`](https://gitlab.psi.ch/bec/bec/-/commit/d1107119da4b40f0ed119ed578593a75b49f1f38))
* Fixed rpc configuration updates to also update the cache ([`e4ef9b7`](https://gitlab.psi.ch/bec/bec/-/commit/e4ef9b725fc29502b175a20df2adf0c418024db7))

## v0.59.1 (2024-01-29)

### Fix

* Fixed bug in device limit update ([`c347a84`](https://gitlab.psi.ch/bec/bec/-/commit/c347a84ad17c23f20866d90c019b7c705e52110a))

## v0.59.0 (2024-01-25)

### Feature

* Add softwareTrigger to dev._config ([`675e74b`](https://gitlab.psi.ch/bec/bec/-/commit/675e74b42e2038d219e59e5b24b5a94ae6d4ca54))

### Fix

* Fix configupdate for readOnly ([`371175a`](https://gitlab.psi.ch/bec/bec/-/commit/371175a2959d3c668a660f7cce87fa27fbc12769))

### Documentation

* Complement documentation ([`356374e`](https://gitlab.psi.ch/bec/bec/-/commit/356374e59ccc2653e979fefd0bc8b571717ed126))

## v0.58.1 (2024-01-25)

### Fix

* Minor client improvements ([`b58aa12`](https://gitlab.psi.ch/bec/bec/-/commit/b58aa12c16dc2a9c8adde4685ce5e90ccc95cfc7))

## v0.58.0 (2024-01-24)

### Feature

* Added context manager for scan export ([`00e4fbf`](https://gitlab.psi.ch/bec/bec/-/commit/00e4fbfe4567bb75151f310703ac22f4bb2eb483))

### Fix

* Fixed scan_to_csv export and scan_export cm ([`07654ec`](https://gitlab.psi.ch/bec/bec/-/commit/07654ec0432201d44a4311d09efa62084f65c49e))
* Fixed cm exit ([`09d231a`](https://gitlab.psi.ch/bec/bec/-/commit/09d231a783036b71e8a9d9edfaa7408ae8b69fd7))
* Fixed context manager ([`52a2cdc`](https://gitlab.psi.ch/bec/bec/-/commit/52a2cdc8d1596e988d4a7f18acef4a179fc820ad))

### Documentation

* Updated the docs ([`979e1d6`](https://gitlab.psi.ch/bec/bec/-/commit/979e1d6b84beb6223384a2996b1fb2acdfa00d41))

## v0.57.2 (2024-01-24)

### Fix

* Fixed scihub error handling ([`a58b23d`](https://gitlab.psi.ch/bec/bec/-/commit/a58b23d1007f01ae2b892c49904382d896696d4a))

### Documentation

* Added ophyd-test to documentation ([`5809882`](https://gitlab.psi.ch/bec/bec/-/commit/58098821e950ed15e70c558cb389766ff3165779))

## v0.57.1 (2024-01-24)

### Fix

* Remove deviceType from device config and backend; closes #171 ([`3cb7ae7`](https://gitlab.psi.ch/bec/bec/-/commit/3cb7ae7cf97b1772e8c4f614bf67c87eeb36724f))

## v0.57.0 (2024-01-24)

### Feature

* Made some methods staticmethods to simplify their access ([`bbddd50`](https://gitlab.psi.ch/bec/bec/-/commit/bbddd50f5eb5aa53e8e65b5d2b139dc74fa24ed3))

### Fix

* Added default schema ([`0f8875d`](https://gitlab.psi.ch/bec/bec/-/commit/0f8875d1faaf2ee5629d5096bb5e1660dd045f80))

## v0.56.3 (2024-01-23)

### Fix

* Disabled config updates on scibec ([`78b5cd6`](https://gitlab.psi.ch/bec/bec/-/commit/78b5cd66d1391fd855d1913b1a1ea655c86787a6))
* Add 'add' to message again ([`d99230a`](https://gitlab.psi.ch/bec/bec/-/commit/d99230a45fefa412c5b2678c554575b1b27afc13))
* Bugfix for deviceConfigMessage validation ([`1c2a7d1`](https://gitlab.psi.ch/bec/bec/-/commit/1c2a7d1850911ee9a8c45f04dea0622d056785a7))

## v0.56.2 (2024-01-23)

### Fix

* Fixed client shutdown; closes #168 ([`869215b`](https://gitlab.psi.ch/bec/bec/-/commit/869215bdc28bf8f4a90ea9ca0a9c017d26fe7d9b))

## v0.56.1 (2024-01-23)

### Fix

* **service:** Use thread termination event to wait instead of time.sleep ([`fd39c7c`](https://gitlab.psi.ch/bec/bec/-/commit/fd39c7c667d3f06cc411501feaf6a9e614071516))

## v0.56.0 (2024-01-19)

### Feature

* Upgraded to new scibec structure ([`b72894a`](https://gitlab.psi.ch/bec/bec/-/commit/b72894a5f6d2d013fe66df28ca7de29e89125890))
* Added filecontent message ([`cade103`](https://gitlab.psi.ch/bec/bec/-/commit/cade10350cb4b83ee4819f81c178548cf5694a4b))
* Added file content and credential messages ([`416dd7e`](https://gitlab.psi.ch/bec/bec/-/commit/416dd7e1138ce37955fdb7fbfdfd1854771afc2a))
* Added scibec and file content endpoint ([`b366414`](https://gitlab.psi.ch/bec/bec/-/commit/b366414e5ca66b37c309fae7cc33651e989db0fe))

### Fix

* Fixed scibec readonly token update ([`b6ce07e`](https://gitlab.psi.ch/bec/bec/-/commit/b6ce07e65bbcacb36f1cec716db03ffaaff2a009))

## v0.55.0 (2024-01-19)

### Feature

* Add sub for monitor, and callback; closes #158 ([`4767272`](https://gitlab.psi.ch/bec/bec/-/commit/4767272778693d8abd2db81aecf77ebd5d5f3109))
* Add monitor endpoint, device_monitor,  and DeviceMonitor message ([`0a292b0`](https://gitlab.psi.ch/bec/bec/-/commit/0a292b0363479c288be029be35b8560b79a69d29))

### Fix

* Add valid check for actions in DeviceConfigMessage ([`3a52b19`](https://gitlab.psi.ch/bec/bec/-/commit/3a52b1914534c373057e419eb6cec247575929a5))

### Documentation

* Updated scanqueuemessage doc string ([`fd89d86`](https://gitlab.psi.ch/bec/bec/-/commit/fd89d8648f84c8029e141b646b99b2c9c13a68e1))
* Reviewed docstring of BECMessages ([`a4be91f`](https://gitlab.psi.ch/bec/bec/-/commit/a4be91f37c43de4d19101578a94a62d629309427))

## v0.54.0 (2024-01-18)

### Feature

* **config:** Allow both .yaml and .yml files as valid config files ([`a1ca26d`](https://gitlab.psi.ch/bec/bec/-/commit/a1ca26dbd21823ae21eef359b8592a8c8749d300))

## v0.53.0 (2024-01-12)

### Feature

* GUI config dialog for BECMonitor can be opened from bec IPYTHON client ([`bceb55d`](https://gitlab.psi.ch/bec/bec/-/commit/bceb55d18880f773cb9cabd265e53793b211a3f5))

### Fix

* Bec_plotter.py fixed redis source format for new config style ([`6ce1e3a`](https://gitlab.psi.ch/bec/bec/-/commit/6ce1e3a4845db248a89617573fb30350554364da))
* Bec_plotter.py live monitoring fixed to new config structure of BECMonitor ([`6dca909`](https://gitlab.psi.ch/bec/bec/-/commit/6dca90902c7ac8938c64ee2a2f00d2bd54c00c0b))

### Documentation

* BECPlotter docs updated in GUI section ([`6bf51ab`](https://gitlab.psi.ch/bec/bec/-/commit/6bf51abeeac9684c1ef78077f2f8abcf7133ee06))

## v0.52.9 (2023-12-22)

### Fix

* Read commented in DeviceBase ([`2365dff`](https://gitlab.psi.ch/bec/bec/-/commit/2365dff4a6a02d27e6cb1e28d3fd2b9dc7cb78b7))
* Wrong reference for 'monitor' - changed from DeviceBase to Device ([`17cc883`](https://gitlab.psi.ch/bec/bec/-/commit/17cc883355c21299a062fd5bf1490d0f033f0414))

## v0.52.8 (2023-12-18)

### Fix

* Fixed scan def cleanup ([`4be4252`](https://gitlab.psi.ch/bec/bec/-/commit/4be425277b561b9228982bc55d7f3980cf2bf98f))

## v0.52.7 (2023-12-18)

### Fix

* Fixed import of device manager ([`f162633`](https://gitlab.psi.ch/bec/bec/-/commit/f1626336b271b8a231ca46e175ae845ba4071eb6))
* Service should wait for device info ([`67b292f`](https://gitlab.psi.ch/bec/bec/-/commit/67b292fa0d5ab67cf945db6d12a1f92db642d3a3))
* Wait for scihub server to become ready ([`77232ac`](https://gitlab.psi.ch/bec/bec/-/commit/77232ac75f12acc9a754a2b5dcd76fa922340b7b))

## v0.52.6 (2023-12-18)

### Fix

* Fixed limit update for epics pvs; closes #113 ([`fce2520`](https://gitlab.psi.ch/bec/bec/-/commit/fce2520e38c80b1d2c01349b5f0d02d8eaf2a3bd))

## v0.52.5 (2023-12-18)

### Fix

* Fixed scan data namespace clash; closes #141 ([`8c4cee8`](https://gitlab.psi.ch/bec/bec/-/commit/8c4cee824bd0a2d623fd65f63f7a91347c79076d))

## v0.52.4 (2023-12-17)

### Fix

* Fixed config update ([`377e820`](https://gitlab.psi.ch/bec/bec/-/commit/377e82085c704fd2052f2bc3ad01fd1fe686a1c7))
* Fixed config update ([`76d1e06`](https://gitlab.psi.ch/bec/bec/-/commit/76d1e063794cadcf2dbfeefaa3fc0de9b04a7019))

## v0.52.3 (2023-12-16)

### Fix

* Fixed log level init ([`5280dad`](https://gitlab.psi.ch/bec/bec/-/commit/5280dadc0640eaf1d3fbdf2fd6b1ce37a9f8f8ff))
* Fixed bug in alarambase that would prohibit error propagation ([`4c88bc6`](https://gitlab.psi.ch/bec/bec/-/commit/4c88bc687d90acbd41d0312cda42d1c049dd9423))
* Fixed timeout error in config_helper ([`6e75ca7`](https://gitlab.psi.ch/bec/bec/-/commit/6e75ca73bdd11740bcb5fd71c8157d8d66f05b53))
* Removed bec logger overwrite that prohibited log outputs ([`acbcb69`](https://gitlab.psi.ch/bec/bec/-/commit/acbcb69eb22900ca6679d6b059189761a34f4ece))

## v0.52.2 (2023-12-15)

### Fix

* Fixed wm behaviour ([`4ea93dc`](https://gitlab.psi.ch/bec/bec/-/commit/4ea93dcd48a893e95e65a69c91b485d96c49df12))

## v0.52.1 (2023-12-15)

### Fix

* Fixed config_ack for incomplete messages ([`16c0a1d`](https://gitlab.psi.ch/bec/bec/-/commit/16c0a1d4d4d023239afb12862a5732ec5187cf6f))
* Added service acknowledgement for config updates; closes #79 ([`bc1c43e`](https://gitlab.psi.ch/bec/bec/-/commit/bc1c43e2da1775b191dd168ab96599a4ada425cc))

## v0.52.0 (2023-12-15)

### Feature

* Added channel monitor as cli script ([`31cc15f`](https://gitlab.psi.ch/bec/bec/-/commit/31cc15f204ded7d368ef384cdb04448c18c5bc3f))

## v0.51.0 (2023-12-14)

### Feature

* Added message endpoint for read_configuration ([`3faf40a`](https://gitlab.psi.ch/bec/bec/-/commit/3faf40a218716bfa1c4271b01d9f516f93e03807))

### Fix

* Fixed readout for omitted signals ([`532d142`](https://gitlab.psi.ch/bec/bec/-/commit/532d142860ddac19dc1581db895514608dcfb65f))
* Fixed bug in config readout ([`4a640e5`](https://gitlab.psi.ch/bec/bec/-/commit/4a640e5ea05e7842fbfda851d79b97af0a801720))
* Fixed read and read_config for cached readouts ([`ba2a797`](https://gitlab.psi.ch/bec/bec/-/commit/ba2a797dfbd67b98b931b5f299bf53a2f4ed71a2))
* Added read_config on init ([`3529108`](https://gitlab.psi.ch/bec/bec/-/commit/352910812487104a87b8d95dc37d1c2164574074))
* Fixed rpc calls for read_configuration ([`3a475e7`](https://gitlab.psi.ch/bec/bec/-/commit/3a475e7e6e0cf46420bfe99a7b9747110d608412))
* Added option to read configuration from redis ([`f7acd4c`](https://gitlab.psi.ch/bec/bec/-/commit/f7acd4cb0646a660676fd5561d23c00bc7157fcc))
* Fixed ctrl c for rpc calls for unresponsive backends ([`6341059`](https://gitlab.psi.ch/bec/bec/-/commit/6341059dd068daf5fd6cce4947901cc3c3dcbe31))

### Documentation

* Updated docs for cached config readouts ([`c33a66e`](https://gitlab.psi.ch/bec/bec/-/commit/c33a66ef00e096eb94f01b9205c2594fa5c81673))

## v0.50.2 (2023-12-11)

### Fix

* Remove redundant imports ([`4a27b9a`](https://gitlab.psi.ch/bec/bec/-/commit/4a27b9a1ecde763e913774f8c23b308f79e7a181))
* Fix devicemanger get_deviceType_devices bug and add test ([`4aa9ba4`](https://gitlab.psi.ch/bec/bec/-/commit/4aa9ba4a8ef26fef2ad51ef72cd600ce624b7542))

### Documentation

* Update user docs, read and get; closes #125, #150 ([`6cf5cfa`](https://gitlab.psi.ch/bec/bec/-/commit/6cf5cfa7a5456fb899fd649b89b2c22293d2a3d8))
* Fix docs, merge ophyd_devices into ophyd in developer documentation ([`26dabe6`](https://gitlab.psi.ch/bec/bec/-/commit/26dabe6f31333e8417ad569b484c80e1e4026f23))
* Address merge comments ([`c288a4e`](https://gitlab.psi.ch/bec/bec/-/commit/c288a4ee5341502abc08fd2d163462e1c8d95cbd))
* Add fields to developer.ophyd as fillers ([`3c64df3`](https://gitlab.psi.ch/bec/bec/-/commit/3c64df327af16485d68dc2d8d2b1a312af67f932))
* Update docs, change software limits for  motor ([`e2a41c8`](https://gitlab.psi.ch/bec/bec/-/commit/e2a41c8b12e74debfe68a3d44424bde5a5841984))
* Add docs for read and get interface access; closes #125 ([`fad8662`](https://gitlab.psi.ch/bec/bec/-/commit/fad86626a4ff3d2b11a1c3dc2cf34baeb0bb5777))
* Fix typos, add links to requirements ([`ab7a9fa`](https://gitlab.psi.ch/bec/bec/-/commit/ab7a9faf747cc8b4954050186113bdb2ab1ee4a7))

## v0.50.1 (2023-12-11)

### Fix

* Fixed decorator order and raised error for new typeguard version ([`8b610c2`](https://gitlab.psi.ch/bec/bec/-/commit/8b610c2ee88229122991892490b053fae3454b20))

## v0.50.0 (2023-12-11)

### Feature

* Relaxed rules on deviceConfig schema; removed need for adding name ([`26d3f45`](https://gitlab.psi.ch/bec/bec/-/commit/26d3f45c7838c0cc60b649b3051ee5ce4e758ad5))
* Removed acquisition group and status from device config ([`5f48362`](https://gitlab.psi.ch/bec/bec/-/commit/5f4836266761f880e98e0798d0046d477a4b1e43))

### Fix

* Fix baseline_update ([`c39bdc1`](https://gitlab.psi.ch/bec/bec/-/commit/c39bdc13b536e49909584c2398dd6ec595e67d27))
* Fixed bug and tests ([`beb0651`](https://gitlab.psi.ch/bec/bec/-/commit/beb065124d0fcac7df4469a76a552ff057bd6a52))
* Clean up device_manager and scan_worker, add tests for baseline_devices; closes #144, #98 ([`7d5c03b`](https://gitlab.psi.ch/bec/bec/-/commit/7d5c03b7b9a8683d59773fc0b7e5f0830e563519))
* Fixed update for deviceConfig ([`1b81ffb`](https://gitlab.psi.ch/bec/bec/-/commit/1b81ffb3323ed560f1791587f612b8dfb254f6c4))
* Fixed devicemanager for missing deviceConfig ([`daa0e8e`](https://gitlab.psi.ch/bec/bec/-/commit/daa0e8e5e24518839b68dfebaca74f579ca49a9f))
* Added implicit ophyd device name assignment ([`6b497e2`](https://gitlab.psi.ch/bec/bec/-/commit/6b497e2536a993a4ba870a146a5fc824408907bc))
* Fixed fly scan sim ([`50fc302`](https://gitlab.psi.ch/bec/bec/-/commit/50fc30216bd44ec46118fba5e37def56b859c8a5))
* Fixed config update in config handler ([`cdbaf0c`](https://gitlab.psi.ch/bec/bec/-/commit/cdbaf0c6c4132af326ece5feb35ba302efa84c72))
* Fixed config update in devicemanager ([`46d1cf9`](https://gitlab.psi.ch/bec/bec/-/commit/46d1cf97dffbc14f97eddfdc6dac0161e5861216))
* Fixed demo config ([`ab399cc`](https://gitlab.psi.ch/bec/bec/-/commit/ab399cc934f186d286595bfd325fe7d78f31351e))
* Allow empty signals ([`cdd1d0c`](https://gitlab.psi.ch/bec/bec/-/commit/cdd1d0cba0816692faeec9bd74ea97b4043579d3))
* Fixed scan server after config refactoring ([`9397918`](https://gitlab.psi.ch/bec/bec/-/commit/939791889f9403c597ce7cbcb5f5c401ae6747a1))
* Fixed bec_lib after refactoring ([`9317220`](https://gitlab.psi.ch/bec/bec/-/commit/93172203b6292dfe8399fb47a277263002f94f01))

### Documentation

* Update documentation to new config structure ([`f38ddc3`](https://gitlab.psi.ch/bec/bec/-/commit/f38ddc3854611d8bf63a776749d418af870511d3))

## v0.49.2 (2023-12-11)

### Fix

* Added wheel for bec server install ([`7f51416`](https://gitlab.psi.ch/bec/bec/-/commit/7f514168c027031d8dacd4b7ec539c78a468b543))

### Documentation

* Updated install information for bec dev ([`6ede847`](https://gitlab.psi.ch/bec/bec/-/commit/6ede847b3e02593241420c37425659429729f823))

## v0.49.1 (2023-12-08)

### Fix

* Fixed .get inconsistencies ([`83af812`](https://gitlab.psi.ch/bec/bec/-/commit/83af8127da11c80a47e05e375080c89bcc76716e))

## v0.49.0 (2023-12-07)

### Feature

* Added first version of bec_plotter ([`6c485c7`](https://gitlab.psi.ch/bec/bec/-/commit/6c485c7fcdcd2cbea3b5486c5df531c215e4fa13))
* Added gui endpoints and messages ([`6472e4e`](https://gitlab.psi.ch/bec/bec/-/commit/6472e4ef94b8100405e1c2e0011fd0a8c698a300))

### Fix

* Removed hard-coded link to widgets ([`3a99554`](https://gitlab.psi.ch/bec/bec/-/commit/3a99554b7e5310606a968c5e71eb7942d1381aaa))
* Fixed print_log; added tests ([`9028693`](https://gitlab.psi.ch/bec/bec/-/commit/9028693a3cd8ebc81ac6dc4832edc52732cd6444))
* Fixed show for manually closed figures ([`b68f38e`](https://gitlab.psi.ch/bec/bec/-/commit/b68f38e866a1a4806e7cc79c840cabfebbd27d38))
* Added missing set and append functions ([`716f80e`](https://gitlab.psi.ch/bec/bec/-/commit/716f80e2ca6d6383f8dc630680e54984d3375da6))

## v0.48.0 (2023-12-05)

### Feature

* Added support for namedtuple serialization for rpc ([`fd00974`](https://gitlab.psi.ch/bec/bec/-/commit/fd00974b05112a7c85eea412a1be89fee3b74822))

### Fix

* Fixed cached readout for .get; closes #137 ([`4fc35ca`](https://gitlab.psi.ch/bec/bec/-/commit/4fc35cadc161c1b39fc5a891ab7150f9b043b9f0))
* Fixed bug in readout for hinted and normal signals ([`bcd2433`](https://gitlab.psi.ch/bec/bec/-/commit/bcd243361af8eccd0771bc6950fcc3f86689c664))
* Made rpc interface more consistent with ophyd ([`e0e3a71`](https://gitlab.psi.ch/bec/bec/-/commit/e0e3a7158cee84c56f4ce82657e36ff88b18a36b))

### Documentation

* Fixed paragraph level ([`01bba51`](https://gitlab.psi.ch/bec/bec/-/commit/01bba51da191e07d3ada050a78e031248cb4dd50))
* Improved introduction ([`1c82e80`](https://gitlab.psi.ch/bec/bec/-/commit/1c82e80960d27e85b73e1f308f06f44ec5a54316))
* Cleanup developer docs; remove usage folder ([`329e30b`](https://gitlab.psi.ch/bec/bec/-/commit/329e30b722843d66396e3e4bd8fc0d12660a6f06))
* Resolved threadl small typo in install ([`3236d1e`](https://gitlab.psi.ch/bec/bec/-/commit/3236d1ea725ce78b13828cdf6588e5c836983ef7))
* Split ophyd and ophyd_devices ([`173eb26`](https://gitlab.psi.ch/bec/bec/-/commit/173eb26b0c7469413075bb3766edd4f0ae626866))
* Review install_developer_env ([`5e3c10a`](https://gitlab.psi.ch/bec/bec/-/commit/5e3c10aca6517e5e4aa5eb00fc585e07f091b48c))
* Review contributing section ([`f4ffff3`](https://gitlab.psi.ch/bec/bec/-/commit/f4ffff3414baa62446e2810cbd389111d8d53183))
* Reviewd architecture section ([`1ac315d`](https://gitlab.psi.ch/bec/bec/-/commit/1ac315dc61094eee3d84f8cc2b3cf5b6331b04ba))
* Review developer page ([`c35e0be`](https://gitlab.psi.ch/bec/bec/-/commit/c35e0be40d13724d684109dcaea827a14d2a6dae))
* Rem typo and add link in data_access ([`b5c7453`](https://gitlab.psi.ch/bec/bec/-/commit/b5c7453445c565e99703436b88420d7b8f98d197))
* Rem typos in cli section ([`ede65af`](https://gitlab.psi.ch/bec/bec/-/commit/ede65af1c3c189bca137567096537709332c2b18))

## v0.47.0 (2023-11-28)

### Feature

* Added support for starting the bec client with a config ([`0379031`](https://gitlab.psi.ch/bec/bec/-/commit/0379031fa7653e3cb647ef35cab95426bf5b1130))

### Documentation

* Fixed link; minor changes ([`6acbb66`](https://gitlab.psi.ch/bec/bec/-/commit/6acbb66ed7472fb369623e2ad55cc2c1835886ed))
* Fixed typos and links in user section ([`dc0d611`](https://gitlab.psi.ch/bec/bec/-/commit/dc0d611ddc88f5c35922fd5366e20e51c34e1053))
* Refactoring of user section ([`487582d`](https://gitlab.psi.ch/bec/bec/-/commit/487582d0a124b01c40c8b324f169e92f3d74d978))

## v0.46.1 (2023-11-28)

### Fix

* Fixed ctrl-c behaviour for report.wait; closes #138 ([`728b43c`](https://gitlab.psi.ch/bec/bec/-/commit/728b43c3f98c26dd337bdfff8bb4afc2fd684b80))

## v0.46.0 (2023-11-28)

### Feature

* Added version flag to bec cli ([`438e625`](https://gitlab.psi.ch/bec/bec/-/commit/438e6258dfd9806227d9ae89f2ae892c557e386a))

## v0.45.4 (2023-11-28)

### Fix

* Fixed device read for nested devices; closes #134 ([`eda60c5`](https://gitlab.psi.ch/bec/bec/-/commit/eda60c529afea248104279b3152ef9cfcb44b228))

## v0.45.3 (2023-11-28)

### Fix

* Fixed import in spec_hli ([`d5bc55a`](https://gitlab.psi.ch/bec/bec/-/commit/d5bc55aa8b047fafb59900394292e62d1a5c1b05))
* Added missing file ([`e82604c`](https://gitlab.psi.ch/bec/bec/-/commit/e82604cab5c48e228dbdd0016725c0d3ddc3c659))

## v0.45.2 (2023-11-27)

### Fix

* Fixed stop instruction for halt ([`6eb1081`](https://gitlab.psi.ch/bec/bec/-/commit/6eb10810d6de19bbeb9170fd78259864c3ca682c))

## v0.45.1 (2023-11-27)

### Fix

* Add short delay in case of connection error ([`95106d6`](https://gitlab.psi.ch/bec/bec/-/commit/95106d6136d2d0a6fb476a422d970dcf830519de))

### Documentation

* Update docstrings for endpoints ([`945297d`](https://gitlab.psi.ch/bec/bec/-/commit/945297d4ac4be12c204546f5568a89eb4efb148b))
* Include comments upon merge request ([`e3c3607`](https://gitlab.psi.ch/bec/bec/-/commit/e3c3607fef0cb1238b9d3a60a61b3576a5660c14))
* Fix style ([`cb531c2`](https://gitlab.psi.ch/bec/bec/-/commit/cb531c2de16ea41a31c3bf80a31b463c5fbae28d))
* Remove typo ([`e017900`](https://gitlab.psi.ch/bec/bec/-/commit/e01790062b93a132a6581cd023f215b87e30fc8e))
* Add gauss_scatter_plot ([`bf138ca`](https://gitlab.psi.ch/bec/bec/-/commit/bf138ca380261e2dcaf6659fceb9ab8f6daa4129))
* Reviewed user documentation ([`15316ca`](https://gitlab.psi.ch/bec/bec/-/commit/15316caedb0ffa9846b199cc795e3bea3e031386))
* Refactor device configuration.md ([`12bd969`](https://gitlab.psi.ch/bec/bec/-/commit/12bd969d59dafde22cdd1fd1d0b6c15a16629a52))
* Update user guide for installation ([`aa5a245`](https://gitlab.psi.ch/bec/bec/-/commit/aa5a245b46b46255b78b4f5d1a71898f6c2257bf))

## v0.45.0 (2023-11-24)

### Feature

* Add load_demo_config method ([`20dfc64`](https://gitlab.psi.ch/bec/bec/-/commit/20dfc6497266bb0dde52cd71bd4e88ce7f364571))

## v0.44.2 (2023-11-23)

### Fix

* Fixed config_init path to config file. again. ([`6b714ef`](https://gitlab.psi.ch/bec/bec/-/commit/6b714ef375dd2e9599d462b4091194fbec264f94))
* Fixed config_init path to config file ([`e1a2429`](https://gitlab.psi.ch/bec/bec/-/commit/e1a2429fac8756832bcc9937262fb72a8aace592))
* Fixed packaging of demo_config and openapi_schema ([`7f8b1b1`](https://gitlab.psi.ch/bec/bec/-/commit/7f8b1b1bbe8dee285b71e221161f0c86ad49dd01))

### Documentation

* Fixed link to conventionalcommits ([`6731a55`](https://gitlab.psi.ch/bec/bec/-/commit/6731a559422f7760a39fe160f22298022174bff1))
* Added placeholder for developer doc ([`f5a9f7d`](https://gitlab.psi.ch/bec/bec/-/commit/f5a9f7dfa6ebf9d23b53fa33764f684228690c11))
* Fixed page navigation ([`033c535`](https://gitlab.psi.ch/bec/bec/-/commit/033c53529e4947422968b258d26347c74b983d3d))

## v0.44.1 (2023-11-22)

### Fix

* Fixed startup script by adding main guard ([`f6b5e9e`](https://gitlab.psi.ch/bec/bec/-/commit/f6b5e9e3c708162eb9f07c118e0226d5395f7f20))

## v0.44.0 (2023-11-21)

### Feature

* Added GUI config endpoint ([`67903a4`](https://gitlab.psi.ch/bec/bec/-/commit/67903a47bdcace6fcb9043aa6ad2bcb512260e12))

## v0.43.0 (2023-11-21)

### Feature

* Added scan_data to simplify the access to the scan storage ([`6cfff5a`](https://gitlab.psi.ch/bec/bec/-/commit/6cfff5a529650094aa602d3669d96a7637bb79a1))

### Fix

* Fixed scan_data len dunder ([`b037b91`](https://gitlab.psi.ch/bec/bec/-/commit/b037b91c53b1bbc40224f712bc10787e981add39))

## v0.42.10 (2023-11-19)

### Fix

* Fixed rpc func name compilation ([`c576669`](https://gitlab.psi.ch/bec/bec/-/commit/c57666949582663124f8b7b02f1707f41164f35c))
* Changes related to new read signature ([`80ee353`](https://gitlab.psi.ch/bec/bec/-/commit/80ee35371291831e5a9a3be3a7d9a09fadf710c2))
* Fixed readback data mixin ([`a396f12`](https://gitlab.psi.ch/bec/bec/-/commit/a396f12ec434359ba8735ad466d6fbd75a74aca1))
* Read through rpc updates the redis entries ([`52f9a4e`](https://gitlab.psi.ch/bec/bec/-/commit/52f9a4eceef70b1fb9df428ff9740eac7a45ea2f))

## v0.42.9 (2023-11-19)

### Fix

* Clean up  __init__ ([`ab9a5e3`](https://gitlab.psi.ch/bec/bec/-/commit/ab9a5e3fa516dbb599400f2cf796169af98ec5e2))

### Documentation

* Fix typo ([`77f4072`](https://gitlab.psi.ch/bec/bec/-/commit/77f407233421bd4838e8d22f53b3342cd67e47e1))
* Add module docstring ([`81d40a2`](https://gitlab.psi.ch/bec/bec/-/commit/81d40a233148a34ab7fa71c16afc7ab361632e36))

## v0.42.8 (2023-11-18)

### Fix

* Fixed ctrl c behaviour for rpc calls; closes #119 ([`9986a72`](https://gitlab.psi.ch/bec/bec/-/commit/9986a7292629668b6f398bee411bada04b535adc))
* Added status eq dunder ([`f1327d4`](https://gitlab.psi.ch/bec/bec/-/commit/f1327d409117f91f17917d6fe30a1dae8e4cbb90))

## v0.42.7 (2023-11-18)

### Fix

* Fixed signature serializer for py >3.9 ([`6281716`](https://gitlab.psi.ch/bec/bec/-/commit/6281716b2974a7b074aa4b6ef465427f3603937e))
* Fixed signature serializer for typing.Literal ([`5d4cd1c`](https://gitlab.psi.ch/bec/bec/-/commit/5d4cd1c1918b4f417b9ebb51e5a12b5692bd7384))

## v0.42.6 (2023-11-18)

### Fix

* Include all needed files in packaged distro ([`2b3eddc`](https://gitlab.psi.ch/bec/bec/-/commit/2b3eddcff62d3a8085f2f8d1a5826020ecd87107))

## v0.42.5 (2023-11-17)

### Fix

* Fixed creation of nested device components; needed for DynamicComponents ([`407f990`](https://gitlab.psi.ch/bec/bec/-/commit/407f99049091f78efc3b8fac6bb7046cc0a6b623))

## v0.42.4 (2023-11-17)

### Fix

* Removed redundant name in config output ([`5a81c21`](https://gitlab.psi.ch/bec/bec/-/commit/5a81c2134593b702fcd6f2645e952caa7cdaf2d2))

## v0.42.3 (2023-11-12)

### Fix

* Added missing init file ([`109453c`](https://gitlab.psi.ch/bec/bec/-/commit/109453c1ccb3ebc8506e57f549549f99b38e4c8f))

## v0.42.2 (2023-11-10)

### Fix

* Bec_service test ([`97d3d1f`](https://gitlab.psi.ch/bec/bec/-/commit/97d3d1f18f07101a860952f40a96b7cfd633fb3c))
* Resolve a circular import in logbook_connector ([`8efd02c`](https://gitlab.psi.ch/bec/bec/-/commit/8efd02cda483aaa29cdb6bbb9867a67037a25111))

## v0.42.1 (2023-11-09)

### Fix

* Fixed bec service update routine for missing messages; closes #114 ([`dc37058`](https://gitlab.psi.ch/bec/bec/-/commit/dc370584c9265b4fc28e79bd2bd9609c826668f8))

## v0.42.0 (2023-11-07)

### Feature

* Added scan base class to scan info ([`5ecc189`](https://gitlab.psi.ch/bec/bec/-/commit/5ecc1893439c46578b9da48913f80ff72d7b1fb9))

## v0.41.0 (2023-11-06)

### Feature

* Changed arg_bundle_size from int to dict; closes #111 ([`1a8cc7c`](https://gitlab.psi.ch/bec/bec/-/commit/1a8cc7c448edd3f712cf2fc20070abefad69dd66))

### Fix

* Fixed scan signature for scan defs and group def ([`3589e3e`](https://gitlab.psi.ch/bec/bec/-/commit/3589e3e36fc4222592dcf9912a9be45b8cc91eea))

## v0.40.0 (2023-11-06)

### Feature

* Added log to report on missing device status updates ([`261497a`](https://gitlab.psi.ch/bec/bec/-/commit/261497ad985bd52ab9db38086cd5421bc03331d2))

## v0.39.0 (2023-11-02)

### Feature

* Changed arg_input from list to dict to provide a full signature ([`c7d8b1a`](https://gitlab.psi.ch/bec/bec/-/commit/c7d8b1afd510cbb63f097b74121bb1b7b9e89ffc))

### Fix

* Added missing type hints to scan signatures ([`6b21908`](https://gitlab.psi.ch/bec/bec/-/commit/6b2190899d16d5bc1b1a582ca5f7159f1be6a56d))
* Removed helper plugin ([`87100ca`](https://gitlab.psi.ch/bec/bec/-/commit/87100caaf07851ce758dfa5e42f5c121eff2b886))

## v0.38.1 (2023-11-02)

### Fix

* Fixed nested get for missing fields ([`9be82f1`](https://gitlab.psi.ch/bec/bec/-/commit/9be82f12c6b42e99c61eeacc6185c663f95c9ab6))

## v0.38.0 (2023-11-01)

### Feature

* Added config option to abort on ctrl_c; closes #95 ([`705daa6`](https://gitlab.psi.ch/bec/bec/-/commit/705daa6d9e9642fdea85adafa12e4946e69bcd6c))

## v0.37.0 (2023-11-01)

### Feature

* Added option to specify monitored devices per scan; closes #100 ([`d3da613`](https://gitlab.psi.ch/bec/bec/-/commit/d3da613bfdf3721f5c52f5491bf64b01317a4126))

### Fix

* Fixed readout_priority update ([`aee1bda`](https://gitlab.psi.ch/bec/bec/-/commit/aee1bdae1461dd1bb8c0f959c8bce97605074d9d))

## v0.36.3 (2023-11-01)

### Fix

* Added missing timestamp to flyer update ([`091df2f`](https://gitlab.psi.ch/bec/bec/-/commit/091df2f0a136a78423159faa35308d44f68f535c))

## v0.36.2 (2023-10-31)

### Fix

* Fixed error that caused the scan worker to shut down instead of raising for scan abortion ([`f1e8bfb`](https://gitlab.psi.ch/bec/bec/-/commit/f1e8bfba80468dc9aa7d057ecb57ef383c215c71))
* Added device name to flyer readout ([`cd82727`](https://gitlab.psi.ch/bec/bec/-/commit/cd827271bb738ced288450dc79b7dc0316e6b0b9))

## v0.36.1 (2023-10-30)

### Fix

* Add '.[dev]' to bash scripts to avoid escape char in certain shells while install ([`0d5168d`](https://gitlab.psi.ch/bec/bec/-/commit/0d5168dcedf32902ffd866c45d85457c4f22e7e7))

## v0.36.0 (2023-10-30)

### Feature

* Added complete call to all devices; closes #93 ([`042e51e`](https://gitlab.psi.ch/bec/bec/-/commit/042e51e857cad3198823c9227e593b15ba1a233f))

### Fix

* Fixed bug in complete for all devices ([`08d34a8`](https://gitlab.psi.ch/bec/bec/-/commit/08d34a8418b768209b0721ac876b76575699ae7e))

### Documentation

* Updated introduction; added scripts and scan defs ([`b9f2eab`](https://gitlab.psi.ch/bec/bec/-/commit/b9f2eab7297fd38085d1d77e0dd66aa070fe051e))

## v0.35.1 (2023-10-06)

### Fix

* Changed progress update from devicestatus to progress message ([`03595b4`](https://gitlab.psi.ch/bec/bec/-/commit/03595b42f78f45f2c5d2e7bf10e860a3ee5297d4))

## v0.35.0 (2023-10-06)

### Feature

* Grid fly scan with standard epics owis motors ([`552aff5`](https://gitlab.psi.ch/bec/bec/-/commit/552aff5bd9fd0bb61e3f50133d4bbf52cc824857))

### Fix

* Fixed stage instruction for detectors ([`ac7a386`](https://gitlab.psi.ch/bec/bec/-/commit/ac7a386acf62d381ad096d816da6db30bcfa5ce7))
* Optimize staging of devices in scanserver and device server ([`2c66dbb`](https://gitlab.psi.ch/bec/bec/-/commit/2c66dbbe4667120195151f49acfe5b45527e21b9))
* Sgalil scan corrections ([`2f8fce5`](https://gitlab.psi.ch/bec/bec/-/commit/2f8fce52207fdbab2a5db562ca7cfa3beb814e41))
* Adjusted sgalil_grid scan for updated mcs operation ([`b7a722c`](https://gitlab.psi.ch/bec/bec/-/commit/b7a722c0ef4ce14fd6843c368bf076bd1024db23))
* Online changes e20643, file writer bugfix and add scanabortion check in sgalil_grid ([`195a8dd`](https://gitlab.psi.ch/bec/bec/-/commit/195a8dd7541fa12ff5f4d9c9cc0a70651af805b1))
* Fixed scan bundler for async fly scans ([`d7a6b0f`](https://gitlab.psi.ch/bec/bec/-/commit/d7a6b0fee010877dfd18cbf23ff55126a399dec9))
* Enabled scilog ([`64e82c6`](https://gitlab.psi.ch/bec/bec/-/commit/64e82c67782a701f5eeb04a3a9c1ce42832c1fdf))
* Fixed bl_check repeat ([`62aa0ae`](https://gitlab.psi.ch/bec/bec/-/commit/62aa0aed78c23ea0c117f84ba54d5f267f35eed4))
* Fixed primary readout for sgalil scan ([`4231d00`](https://gitlab.psi.ch/bec/bec/-/commit/4231d00e19aacc039ee9cc9f4a1f18294ea18ab0))
* Added missing pre scan to acquire ([`d746093`](https://gitlab.psi.ch/bec/bec/-/commit/d7460938041dac4be45fa39cbdaa957dda5f88ca))
* Fixed tmux launch for mono environments ([`5be5dda`](https://gitlab.psi.ch/bec/bec/-/commit/5be5dda1cfd3adfadae5e314a8ba87b394e8227a))
* Fixed scan progress for messages without scanID ([`64f3b13`](https://gitlab.psi.ch/bec/bec/-/commit/64f3b13e9710dbfb207c11fbd683db9cb9462dda))

## v0.34.2 (2023-10-05)

### Fix

* Fixed bug for aborted scans ([`e7d73e5`](https://gitlab.psi.ch/bec/bec/-/commit/e7d73e5b2b2cccb829e401b209605523f6b7dbce))

## v0.34.1 (2023-10-02)

### Fix

* Write files on abort and halt ([`910a92f`](https://gitlab.psi.ch/bec/bec/-/commit/910a92f4784c93119e63c9abad24ec1315718a45))

## v0.34.0 (2023-09-07)

### Feature

* Added progress endpoint and message ([`ad60b78`](https://gitlab.psi.ch/bec/bec/-/commit/ad60b7821a1de36645e2c70023ea73bb7d141e39))

### Fix

* Added missing primary readings to sgalil grid ([`e52390a`](https://gitlab.psi.ch/bec/bec/-/commit/e52390a2269370f6806f93896234bc076a0731f4))

## v0.33.0 (2023-09-07)

### Feature

* Add sgalilg_grid to scan_plugins and make scantype flyscan scan possible ([`a5ba186`](https://gitlab.psi.ch/bec/bec/-/commit/a5ba186ad14283fae7c5160180a759e29f78137d))

### Fix

* File_writer and scan_ser for falcon and eiger9m and sgalil grid scan ([`cec0b34`](https://gitlab.psi.ch/bec/bec/-/commit/cec0b342f0c518bb37c4403cb55336792a192cec))
* Online fix for file writer ([`de5ba09`](https://gitlab.psi.ch/bec/bec/-/commit/de5ba09954468bf696e2aa27f00532fe7780ef27))
* Add file_writer plugin cSAXS and file_event for new file from device ([`0fdf164`](https://gitlab.psi.ch/bec/bec/-/commit/0fdf1647aaf153d480f952ff1515fda2a1a1640d))
* Add frames_per_trigger to scans and scan server ([`0c66dc3`](https://gitlab.psi.ch/bec/bec/-/commit/0c66dc33593379c7e2bee8499af8d6cecf32b761))
* Add eiger9m to cSAXS nexus file writer plugin ([`375150c`](https://gitlab.psi.ch/bec/bec/-/commit/375150ce58e00f2b6f53d713ac35cebdb087b6ad))
* Add file_writer plugin cSAXS and file_event for new file from device ([`b1f4fcc`](https://gitlab.psi.ch/bec/bec/-/commit/b1f4fccaaaec9cded2182554900ca48ceeb2fdc3))
* Add frames_per_trigger to scans and scan server ([`51c8a54`](https://gitlab.psi.ch/bec/bec/-/commit/51c8a54f01c6b5a0a09c90cb5a21e5640b3cd884))
* Add eiger9m to cSAXS nexus file writer plugin ([`8ba441f`](https://gitlab.psi.ch/bec/bec/-/commit/8ba441f55fdb9659aff12d2535799f268af1d815))

## v0.32.0 (2023-09-06)

### Feature

* Added pre_scan ([`7f23482`](https://gitlab.psi.ch/bec/bec/-/commit/7f23482b5cf273f06776e497783f44361a2cb58f))

### Fix

* Removed pre move from fly scan ([`ed095b0`](https://gitlab.psi.ch/bec/bec/-/commit/ed095b00cbebc50ebecaabc696b8aaf4a728270d))
* Removed pre move from fly scan ([`f8ad2f8`](https://gitlab.psi.ch/bec/bec/-/commit/f8ad2f8a2781fa38000c29b39772132eaa63e4ce))

### Documentation

* Added premove and enforce_sync doc ([`fd38985`](https://gitlab.psi.ch/bec/bec/-/commit/fd38985767ead15678f45ac60d0ee59bb8ee8df6))

## v0.31.0 (2023-09-05)

### Feature

* Added support for loading the service config from plugins ([`f3d3679`](https://gitlab.psi.ch/bec/bec/-/commit/f3d3679e216492d8dfaf35ff00f75520652863fc))

## v0.30.1 (2023-09-05)

### Fix

* Added sleep before polling for status ([`c8acaa4`](https://gitlab.psi.ch/bec/bec/-/commit/c8acaa4b71504a8b34c9f05f4ef6af5ab444a424))
* Removed hard-coded trigger wait; waiting for status instead ([`086c863`](https://gitlab.psi.ch/bec/bec/-/commit/086c8634e30baf4ae1b74ae61bd3f8070c69d320))

## v0.30.0 (2023-09-04)

### Feature

* Beamline check ([`cae5f61`](https://gitlab.psi.ch/bec/bec/-/commit/cae5f61924744d0358527b074958bdfe102bb2cd))
* Added preliminary version of bl_checks ([`bfa1d67`](https://gitlab.psi.ch/bec/bec/-/commit/bfa1d678735cc8dcfb303446517254290c7c7921))

## v0.29.0 (2023-09-04)

### Feature

* Added bec_plugins as source for devices ([`bbcdbc0`](https://gitlab.psi.ch/bec/bec/-/commit/bbcdbc0123566f4bea811fb9c873e059b4eb4a7c))

### Fix

* Fixed signal init ([`41282e5`](https://gitlab.psi.ch/bec/bec/-/commit/41282e57678d6a39a1f40fdf828e2fdb2ddc0193))

## v0.28.0 (2023-09-02)

### Feature

* Added progress bar based on async devices ([`11e5f96`](https://gitlab.psi.ch/bec/bec/-/commit/11e5f96b7575e0a811f45914e99ada6d2c449648))
* Added scan progress ([`9f6a044`](https://gitlab.psi.ch/bec/bec/-/commit/9f6a044fe316c804e2e4dfc34435c9eb71cd109b))
* Added xrange ([`f4f38d6`](https://gitlab.psi.ch/bec/bec/-/commit/f4f38d6deab2026177126e58cf1eac20490d9942))

### Fix

* Fixed scan_progress import ([`5eda477`](https://gitlab.psi.ch/bec/bec/-/commit/5eda477723d4dfc0387e0293713ef8e197a58f53))
* Ipython client should use default service config ([`9b89aec`](https://gitlab.psi.ch/bec/bec/-/commit/9b89aecfdc0449a9d40aae642dccf2408989c6d1))

## v0.27.0 (2023-08-31)

### Feature

* Added get_last; changed streams to stream suffix ([`e84601f`](https://gitlab.psi.ch/bec/bec/-/commit/e84601f487d4943c63a31f12b42d656dc9a4c690))

## v0.26.0 (2023-08-31)

### Feature

* Add new endpoint for async device readback ([`5535797`](https://gitlab.psi.ch/bec/bec/-/commit/5535797e1e25121d7a3997d78aa6c43eff17e086))

### Fix

* Fixed xadd for pipelines ([`d19fce7`](https://gitlab.psi.ch/bec/bec/-/commit/d19fce7d21a12eac2f8ac9b083fff464e5d0da9e))
* Bugfix ([`57c989c`](https://gitlab.psi.ch/bec/bec/-/commit/57c989cfe204a657bcefac2364a6a0ad98a77ff1))
* Adjust xadd to allow streams to expire ([`33fbded`](https://gitlab.psi.ch/bec/bec/-/commit/33fbdedd3eed52ded4eb53043bc7407997d51e4a))
* Online changes ([`9b07e0f`](https://gitlab.psi.ch/bec/bec/-/commit/9b07e0f8a2d774a9a6a07ab9faa9167585532dcd))

## v0.25.0 (2023-08-31)

### Feature

* Added support for startup scripts from plugins ([`d35caf5`](https://gitlab.psi.ch/bec/bec/-/commit/d35caf5ae40b5b46f3b2adad139cad66b3091857))

## v0.24.0 (2023-08-31)

### Feature

* Added global var service config to simplify sharing the config with other classes ([`75f1f9c`](https://gitlab.psi.ch/bec/bec/-/commit/75f1f9cd4ebc6938f2cf47103fb64eef8be57ae3))
* Added option to update the worker config directly ([`a417fd8`](https://gitlab.psi.ch/bec/bec/-/commit/a417fd8a18cadb4b480da243149c1186f3a07d88))
* Added available resource endpoint/message ([`5f5c80c`](https://gitlab.psi.ch/bec/bec/-/commit/5f5c80c2866236226dca717de0c67b32f5692ab9))

### Fix

* Fixed worker manager ([`fa62a8a`](https://gitlab.psi.ch/bec/bec/-/commit/fa62a8a9c96da44439ba71ae82d8020c8a2a0de5))

## v0.23.1 (2023-08-31)

### Fix

* Removed bec prefix from file path ([`9a3b20f`](https://gitlab.psi.ch/bec/bec/-/commit/9a3b20f085232369c9320bb8f54b93fb6b0b1686))

## v0.23.0 (2023-08-29)

### Feature

* Added device precision ([`4177fe6`](https://gitlab.psi.ch/bec/bec/-/commit/4177fe6038a10e2f285fc18c13ef6a77022b17e5))
* Added support for user scripts from plugins and home directory ([`cd59267`](https://gitlab.psi.ch/bec/bec/-/commit/cd59267e780586b002cd80c692a0f38c213f999d))

### Fix

* Fixed live table for hinted signals ([`4334567`](https://gitlab.psi.ch/bec/bec/-/commit/43345676533a402fac517fd467c98b46f35658aa))

## v0.22.0 (2023-08-24)

### Feature

* Added acquisition config and readout_time ([`f631759`](https://gitlab.psi.ch/bec/bec/-/commit/f63175941bbf7d9f5448ff58b9ea942bd2e1b9a4))

## v0.21.1 (2023-08-21)

### Fix

* Fixed bug in device config update ([`940737f`](https://gitlab.psi.ch/bec/bec/-/commit/940737fe6c8295423390a76b784a5984a93c7043))

## v0.21.0 (2023-08-20)

### Feature

* Inject device_manager based on signature ([`4eb9cf4`](https://gitlab.psi.ch/bec/bec/-/commit/4eb9cf494c805cdf751e459f0b9d0b7aa3ebee91))

## v0.20.0 (2023-08-20)

### Feature

* Added device precision to rpc base class ([`2c7b55f`](https://gitlab.psi.ch/bec/bec/-/commit/2c7b55f828f3f68ff05095a007724e499797126b))
* Added option to specify thread names ([`cae0ba2`](https://gitlab.psi.ch/bec/bec/-/commit/cae0ba2d3ea659a7de3936acdc257e1aa0991311))
* Added support for multiple queues; still WIP ([`9019cc2`](https://gitlab.psi.ch/bec/bec/-/commit/9019cc2c7443c38c47160af843eef7e3f070a25b))

### Fix

* Fixed interceptions for multiple queues ([`4e5d0da`](https://gitlab.psi.ch/bec/bec/-/commit/4e5d0da38b06f11e6abe5ce23687cdf237c9ffeb))
* Removed primary queue from init; cleanup ([`bb04271`](https://gitlab.psi.ch/bec/bec/-/commit/bb042716fecbc3035483184e494e9e4f3d2d82da))

## v0.19.0 (2023-08-20)

### Feature

* Added dap to client ([`0ea549a`](https://gitlab.psi.ch/bec/bec/-/commit/0ea549a599f4ac3dccffe7fa2f148e48a0c5d7c1))
* Add bec_worker_manager.py ([`f0ba36d`](https://gitlab.psi.ch/bec/bec/-/commit/f0ba36db869b8a0e06918ef1fd9fc44a87cbd217))
* Pluging support for data_processing ([`9e33418`](https://gitlab.psi.ch/bec/bec/-/commit/9e334185260e5f92964e1f3f5b5d6d3a86d4c1d6))

### Fix

* Remove parameters for saxs_imaging_processor ([`39c7a9c`](https://gitlab.psi.ch/bec/bec/-/commit/39c7a9c0be0a0b9861961e5443f313e11fb35748))
* Fixed dap worker for plugins ([`e2f3d8f`](https://gitlab.psi.ch/bec/bec/-/commit/e2f3d8f29ddc771798d0e2cc43f7f0d85db00fe9))

## v0.18.1 (2023-08-19)

### Fix

* Removed timeout ([`29df4ac`](https://gitlab.psi.ch/bec/bec/-/commit/29df4ac19ac189f4d7666c2c47c4539cf5e94372))
* Fixed bug in wait function for aborted move commands ([`019fcda`](https://gitlab.psi.ch/bec/bec/-/commit/019fcdaa074dcb67c84132cb038067dca8578830))

## v0.18.0 (2023-08-15)

### Feature

* Scan signature is now exported; simplified scan init ([`f35b04a`](https://gitlab.psi.ch/bec/bec/-/commit/f35b04a676a8c6aa972f031d83cb637b346d5d4f))

### Fix

* Fixed typo in round_roi_scan init; added test ([`75f2217`](https://gitlab.psi.ch/bec/bec/-/commit/75f221758f939c510a7766101cc3faa0250a0b6b))
* Fixed bug in unpack_scan_args for empty lists ([`a693f84`](https://gitlab.psi.ch/bec/bec/-/commit/a693f84816d9074a3f4664a8530d0b130702f7a2))
* Added missing file ([`f55a518`](https://gitlab.psi.ch/bec/bec/-/commit/f55a518b9103f93b54c872fb4387956cb783d5b8))

## v0.17.2 (2023-08-10)

### Fix

* Added MessageObject eq dunder ([`563c628`](https://gitlab.psi.ch/bec/bec/-/commit/563c6285092b9d8e33e8c93dea95986b87f5c67a))

## v0.17.1 (2023-08-10)

### Fix

* Fixed default config ([`8ad8d84`](https://gitlab.psi.ch/bec/bec/-/commit/8ad8d84e00a62306d43862192c8a16b09e17a17b))

## v0.17.0 (2023-08-10)

### Feature

* Added stream consumer ([`b4043e9`](https://gitlab.psi.ch/bec/bec/-/commit/b4043e970ac0d3fe2bbd6cb8d386967aefcf812d))

### Fix

* Fixed scans if redis is not available ([`b0467a8`](https://gitlab.psi.ch/bec/bec/-/commit/b0467a86aaf4741484ef0fb66e6441e742142cb5))
* Fixed scan number if redis is not available ([`8514d2d`](https://gitlab.psi.ch/bec/bec/-/commit/8514d2d6384516f53fd75d4ef671e24f32fad0f4))
* Fixed bec_service if service keys are not available ([`9b71f77`](https://gitlab.psi.ch/bec/bec/-/commit/9b71f77dacf0fe1313fe6f0c1e9de73572286b96))

## v0.16.3 (2023-08-06)

### Fix

* Catch redis connection errors ([`31efa96`](https://gitlab.psi.ch/bec/bec/-/commit/31efa96cec20540a00f0be199e8fda4fa04fdc68))
* Fixed default arg for initialize ([`b65aba8`](https://gitlab.psi.ch/bec/bec/-/commit/b65aba8a5fcdb8f2f5eeb488725144f46267f074))
* Wait for bec server should only be done for ipython, not the bec lib ([`9dfe389`](https://gitlab.psi.ch/bec/bec/-/commit/9dfe38943f2b8d6be051612de9f31ad8171f1073))
* Scanbundler sets status to running ([`d0d46ba`](https://gitlab.psi.ch/bec/bec/-/commit/d0d46ba76b1351f5431d7c93a6d6591c250563d7))

### Documentation

* Updated style; added css ([`6ec5fac`](https://gitlab.psi.ch/bec/bec/-/commit/6ec5facd0cdf0588c6545828c53ccc9e8ed29875))
* Added simple ophyd description; added file_manager description ([`48cfcb6`](https://gitlab.psi.ch/bec/bec/-/commit/48cfcb6c6242c381aea71d0e1c686d10e3fb2c1b))

## v0.16.2 (2023-08-05)

### Fix

* Fixed check_storage for already removed scan storage items ([`4a4dace`](https://gitlab.psi.ch/bec/bec/-/commit/4a4daceaf4b7c579cb4adead784f9900b675b5dc))

## v0.16.1 (2023-08-05)

### Fix

* Added thread lock to file writer ([`27e85bb`](https://gitlab.psi.ch/bec/bec/-/commit/27e85bb8b0e5afc0c70618438506727cea883253))

## v0.16.0 (2023-08-04)

### Feature

* Added support for file references and external links in the bec master file ([`9a59bdc`](https://gitlab.psi.ch/bec/bec/-/commit/9a59bdce90110fded772bf4efd84b10e019a7837))
* Added done entry to filemessage ([`2c62fd7`](https://gitlab.psi.ch/bec/bec/-/commit/2c62fd72b16cc62840daba929c1afd8dc26956d0))
* Added support for endpoints with and without suffix ([`ce0e54e`](https://gitlab.psi.ch/bec/bec/-/commit/ce0e54e561ad5ef03898e749e7333dc7535bf0d2))

### Fix

* Removed dummy link ([`de2c8ab`](https://gitlab.psi.ch/bec/bec/-/commit/de2c8ab2c51357dd23e9efbf8481fa99adb11326))
* Removed unnecessary config assignment in client ([`9360570`](https://gitlab.psi.ch/bec/bec/-/commit/93605707bd1ec1efea51407c593b25e0e5b75620))

### Documentation

* Added missing reference file ([`df19570`](https://gitlab.psi.ch/bec/bec/-/commit/df19570c9d658b35a04dbe7112c454793a8a2e54))
* Added logo ([`3c40a28`](https://gitlab.psi.ch/bec/bec/-/commit/3c40a2856c7678d14517bfcae6fe2c935756f68d))
* Fixed requirements ([`76e9342`](https://gitlab.psi.ch/bec/bec/-/commit/76e93429f6eb3851c5fabc78ff425e28b3ba2427))
* Added glossary ([`b54e56f`](https://gitlab.psi.ch/bec/bec/-/commit/b54e56fe8fd7f29b2499770c7c392cdcf7e72fe8))
* Fixed indent ([`fe07a70`](https://gitlab.psi.ch/bec/bec/-/commit/fe07a702df434714fd500fc983502e106e410bee))
* Fixed references ([`20254fb`](https://gitlab.psi.ch/bec/bec/-/commit/20254fb628206f934238f40765a3fa5d15c3274c))
* Updated developer instructions ([`823094a`](https://gitlab.psi.ch/bec/bec/-/commit/823094acb1b06074ef3180d2717986020b911b4f))
* Redesigned documentation ([`ecf3ee9`](https://gitlab.psi.ch/bec/bec/-/commit/ecf3ee93de1fd0ea0f4694150c8c07fcc21da4b5))

## v0.15.0 (2023-08-03)

### Feature

* Added option to specify config path as service config ([`1a776de`](https://gitlab.psi.ch/bec/bec/-/commit/1a776de8118de7428b0c6b4e3693eaf619651192))

### Documentation

* Updated sphinx conf file to deal with md files; added copy button ([`7f48ce6`](https://gitlab.psi.ch/bec/bec/-/commit/7f48ce6aa1f2000993a4fb31e23a3efa3c122a57))
* Minor improvements for scan_to_csv docs ([`21d371a`](https://gitlab.psi.ch/bec/bec/-/commit/21d371a80b8009e1df3c9d4148191f05a36a0abf))

## v0.14.8 (2023-07-26)

### Fix

* Adapt write_to_csv to write multiple scan_reports for context manager ([`7118863`](https://gitlab.psi.ch/bec/bec/-/commit/71188638323f27f0ae7f643a0e8b3ade12579899))

## v0.14.7 (2023-07-25)

### Fix

* Fixed build ([`4eccc99`](https://gitlab.psi.ch/bec/bec/-/commit/4eccc996694d9b260d1df40cc5b2c74ccb587dbe))

## v0.14.6 (2023-07-25)

### Fix

* Fixed bec_client install ([`bacda25`](https://gitlab.psi.ch/bec/bec/-/commit/bacda2580a47773bc4bdabc231049fb6470e7445))

## v0.14.5 (2023-07-24)

### Fix

* Fixed install ([`3f42f2f`](https://gitlab.psi.ch/bec/bec/-/commit/3f42f2f3e1d35e9d6f825a8f9865ab3dabf61be2))

## v0.14.4 (2023-07-24)

### Fix

* Added missing init files ([`1ea9764`](https://gitlab.psi.ch/bec/bec/-/commit/1ea976411d320959a7826e6f09301df90b56517a))
* Added missing init files ([`29cf132`](https://gitlab.psi.ch/bec/bec/-/commit/29cf132a06ebcec7f1e1a8f084d35da0195d4489))
* Fixed build for device_server ([`fc90bfb`](https://gitlab.psi.ch/bec/bec/-/commit/fc90bfb9aab5ef42a9c6160be71357f0df5d21bc))

## v0.14.3 (2023-07-24)

### Fix

* Fixed bec-server version ([`72fdd91`](https://gitlab.psi.ch/bec/bec/-/commit/72fdd91da495e2150463c8aa64cab1a86577289e))

## v0.14.2 (2023-07-24)

### Fix

* Fixed version update for bec-server ([`ae4673f`](https://gitlab.psi.ch/bec/bec/-/commit/ae4673fac049e7bff799efb7566ea5a8fba56c57))

## v0.14.1 (2023-07-24)

### Fix

* Update version number directly to fix pip install without -e ([`91ffa4b`](https://gitlab.psi.ch/bec/bec/-/commit/91ffa4b3c554ab4f0f038958344b81202e251433))

## v0.14.0 (2023-07-21)

### Feature

* Add new functions to save scan to dict and csv ([`effb642`](https://gitlab.psi.ch/bec/bec/-/commit/effb642a4d3a099dd05e0f3b96ac727564e01999))

### Fix

* Fix writer functions ([`fda9d07`](https://gitlab.psi.ch/bec/bec/-/commit/fda9d07e65039e833f51192d4a66a48875c3be46))
* Code update ([`86b1985`](https://gitlab.psi.ch/bec/bec/-/commit/86b198595db33e1af6b8d2a26151658118b2ebe3))

### Documentation

* Updated build dependencies ([`8dd2116`](https://gitlab.psi.ch/bec/bec/-/commit/8dd21165f2079c64ac4e738d0f84926fd60cf887))

## v0.13.3 (2023-07-21)

### Fix

* Fixed tmux launch ([`e4d7840`](https://gitlab.psi.ch/bec/bec/-/commit/e4d78402c0f0feca7d0731498b3b34701d9bc9a6))
* Fixed single env install ([`929689c`](https://gitlab.psi.ch/bec/bec/-/commit/929689cb8e7d1fccda0ab2a5a6372e2d48696193))
* Fixed bec_server install ([`2ebf580`](https://gitlab.psi.ch/bec/bec/-/commit/2ebf580ede20c594951bde73f2a570b744904509))

## v0.13.2 (2023-07-21)

### Fix

* Pip install dev environment ([`750fe66`](https://gitlab.psi.ch/bec/bec/-/commit/750fe66ed3c7c813b9ea154055f6a6f599fadc9a))

### Documentation

* Removed user api for now ([`d8fd1d0`](https://gitlab.psi.ch/bec/bec/-/commit/d8fd1d0b984f4a32d090cfbebcf9a6511f734e09))
* Fixed dependencies; added missing files ([`87e7ec2`](https://gitlab.psi.ch/bec/bec/-/commit/87e7ec2671578ffb2f5c6db1f5d98fcdebaeb61f))
* Added missing glossary file ([`2529891`](https://gitlab.psi.ch/bec/bec/-/commit/2529891a2ca39e773651c3b96d70584c55115eab))
* Improved documentation; added how tos; added glossary ([`99f0c96`](https://gitlab.psi.ch/bec/bec/-/commit/99f0c9636b36f89dc156959184cdd31d65ffee5c))

## v0.13.1 (2023-07-18)

### Fix

* Fixed bug in BECMessage str dunder ([`65e76a9`](https://gitlab.psi.ch/bec/bec/-/commit/65e76a93ceec953434e23432b9c5e912eabcb2c0))

## v0.13.0 (2023-07-14)

### Feature

* Triggering release after refactoring (file_writer_mixin) ([`e4a51b6`](https://gitlab.psi.ch/bec/bec/-/commit/e4a51b67a63bdde93c91e07e7428759c4eb44d56))

## v0.12.0 (2023-07-12)

### Feature

* Added message version 1.2 for better performance ([`f46b29a`](https://gitlab.psi.ch/bec/bec/-/commit/f46b29a2427137be86903df7da6684613698d0c7))
* Added message version 1.2 for better performance ([`fe2bd6c`](https://gitlab.psi.ch/bec/bec/-/commit/fe2bd6c935b511d26a649f89f4ba5b44ed01b7f0))

### Fix

* Fixed bundled messages for 1.2 ([`9381c7d`](https://gitlab.psi.ch/bec/bec/-/commit/9381c7d64684c332b90480aa8c7a6774baf3b5dd))
* Improvements / fixes for redis streams ([`3f09cc3`](https://gitlab.psi.ch/bec/bec/-/commit/3f09cc3cd153e629ee550072d7fc5c31100594be))
* Improvements / fixes for redis streams ([`72e4f94`](https://gitlab.psi.ch/bec/bec/-/commit/72e4f943b684e53e16ed11538d0807d012e9e357))

## v0.11.0 (2023-07-12)

### Feature

* Added redis stream methods to RedisProducer ([`e8352aa`](https://gitlab.psi.ch/bec/bec/-/commit/e8352aa606dc999f0e1bf1bd891a7852a489509d))

## v0.10.2 (2023-07-11)

### Fix

* Added missing x coords to lmfit processor ([`ddfe9df`](https://gitlab.psi.ch/bec/bec/-/commit/ddfe9df6a11f506e52f00be59f76b43c910d0504))

## v0.10.1 (2023-07-11)

### Fix

* Fixed relative path in client init; needed for pypi ([`0d9ed33`](https://gitlab.psi.ch/bec/bec/-/commit/0d9ed33a2d63e54ac12bf9cd5dcc6d4250e70bc4))

## v0.10.0 (2023-07-08)

### Feature

* Added install_bec_dev script ([`db9539a`](https://gitlab.psi.ch/bec/bec/-/commit/db9539aba203e7e299620f76dfd1f3843ebfecbd))
* Simplified bec-server interaction; removed hard-coded service config path ([`5dd1eb7`](https://gitlab.psi.ch/bec/bec/-/commit/5dd1eb7cd0ea0d401c411c9e46b8a567e58c9687))
* Added default service config ([`b1a4b4f`](https://gitlab.psi.ch/bec/bec/-/commit/b1a4b4f75cad19e849d573beb767b18c6d93a308))
* Added clis to all services; added bec_server ([`f563800`](https://gitlab.psi.ch/bec/bec/-/commit/f563800268e7047fd9baa05e48070475688b244f))

### Fix

* Added missing services to the build script ([`6d45485`](https://gitlab.psi.ch/bec/bec/-/commit/6d45485b5a83d02612595c25a3fd3ec90f0c57b6))
* Fixed bug in ipython live update ([`a6a2c28`](https://gitlab.psi.ch/bec/bec/-/commit/a6a2c28a6a111ff552277686d7455eec9cbd56d1))
* Fixed missing files ([`047082b`](https://gitlab.psi.ch/bec/bec/-/commit/047082b38b7f4145c469a76f439fcac241a92b60))
* Adjusted import routine for plugins ([`38c4c8c`](https://gitlab.psi.ch/bec/bec/-/commit/38c4c8c93e79a37314ad5579feb77455d2a5e38f))
* Fixed bug in install script ([`1a7a4d8`](https://gitlab.psi.ch/bec/bec/-/commit/1a7a4d8a745ea29af4ccdc03b6b4d608b6b18fa8))
* Fixed bug in install script ([`05bf99a`](https://gitlab.psi.ch/bec/bec/-/commit/05bf99af739b4023ad75780fe2808f71adcc508f))
* Improved tmux_launcher to handle merged and separated envs ([`088b1a4`](https://gitlab.psi.ch/bec/bec/-/commit/088b1a4a1956209c11c5a31f5c09eca8aed6b86a))

### Documentation

* Updated deployment instructions ([`390db04`](https://gitlab.psi.ch/bec/bec/-/commit/390db0442266f1d4fc36bf8beb70715ccb692eea))
* Updated documentation for new deployment ([`dfc8c92`](https://gitlab.psi.ch/bec/bec/-/commit/dfc8c9247d6b4891cdfb489be2bd3dfba5fe8f40))

## v0.9.2 (2023-07-04)

### Fix

* Added reset_device function ([`f235a17`](https://gitlab.psi.ch/bec/bec/-/commit/f235a1735f67f25eab9ae4ed746a1c101da43dc9))
* Fixed re-enabling devices ([`3f11144`](https://gitlab.psi.ch/bec/bec/-/commit/3f111442584b9abf39382620ccf137c93c89d6a8))
* Improved getattr handling for dunder methods; added comment ([`a6c49b3`](https://gitlab.psi.ch/bec/bec/-/commit/a6c49b34ad2a6960c9db57b6ab6336bb94b432d9))
* Fixed bug in client callbacks that caused rejected scans to get stuck ([`2611f5b`](https://gitlab.psi.ch/bec/bec/-/commit/2611f5b4232fed7d930b21059c2cd0e8a1098a3a))
* Fixed bug in ipython_live_updates in case of missing status messages ([`39c4323`](https://gitlab.psi.ch/bec/bec/-/commit/39c4323303287617918d7cd7101332b338026954))

## v0.9.1 (2023-07-03)

### Fix

* Fixed bug in device_manager that killed tab-completion ([`32d313a`](https://gitlab.psi.ch/bec/bec/-/commit/32d313a04feee1437b4aff547b3ba998266d78af))

## v0.9.0 (2023-07-02)

### Feature

* Add support for scan plugins set through environment vars ([`5ad0d9b`](https://gitlab.psi.ch/bec/bec/-/commit/5ad0d9bbe49c5a0aa1bed74f19caf8df553ee98e))

## v0.8.1 (2023-07-02)

### Fix

* Fixed ipython client startup script for new lib name ([`b2f5f3c`](https://gitlab.psi.ch/bec/bec/-/commit/b2f5f3c2631d749ade619fd32b3f10671f9f3f1c))

### Documentation

* Added data_processing services; changed default python version to 3.9 ([`233f682`](https://gitlab.psi.ch/bec/bec/-/commit/233f68216ff12ce223ea4024fe190e237df21afe))
* Updated doc with proper semver ([`71aa1d7`](https://gitlab.psi.ch/bec/bec/-/commit/71aa1d715a47a9b42888147611ffc8af8d46714c))

## v0.8.0 (2023-06-28)

### Feature

* Renamed primary devices to monitored devices; closes #75 ([`1370db4`](https://gitlab.psi.ch/bec/bec/-/commit/1370db4c70b08702c29e3728b8d0c3229d0188f3))

## v0.7.1 (2023-06-28)

### Fix

* Remove outdated requirements.txt files ([`f781571`](https://gitlab.psi.ch/bec/bec/-/commit/f7815714ff9c9ab6c5b697edc651c376c8052e70))
* Setup files cleanup ([`f60889a`](https://gitlab.psi.ch/bec/bec/-/commit/f60889a87e16ff767806d47bd82a988f50fb091d))

## v0.7.0 (2023-06-28)

### Feature

* Renamed bec_client_lib to bec_lib ([`a944e43`](https://gitlab.psi.ch/bec/bec/-/commit/a944e43e1a8db55959a042a8203040fa2c5484ba))

### Documentation

* Updated readme for new bec_lib ([`6e0bf12`](https://gitlab.psi.ch/bec/bec/-/commit/6e0bf12a0ae1885245961461f0bcef09ad13c2ec))

## v0.6.14 (2023-06-27)

### Fix

* Testing build ([`6849b95`](https://gitlab.psi.ch/bec/bec/-/commit/6849b9583ff0b3c5f4b49180f78b1ef612669145))

### Documentation

* Added scan server readme ([`1663087`](https://gitlab.psi.ch/bec/bec/-/commit/1663087ff8866dff31a6974474b56dd3e73ffb1d))
* Added readme for bec-client-lib ([`bd39147`](https://gitlab.psi.ch/bec/bec/-/commit/bd391470f86ece1e26b629c75341b2ee2c941da4))

## v0.6.13 (2023-06-27)

### Fix

* Added env vars ([`3d33d4b`](https://gitlab.psi.ch/bec/bec/-/commit/3d33d4bc32d2daac29cef6e71d5e0d48aba54f7e))

## v0.6.12 (2023-06-27)

### Fix

* Build test ([`899cfab`](https://gitlab.psi.ch/bec/bec/-/commit/899cfaba35fe40457635d3c8b9840da762e4b0ba))
* Build process with env var ([`3c5f351`](https://gitlab.psi.ch/bec/bec/-/commit/3c5f35166af19faa51fef75aed48a3ded0a186e4))

## v0.6.11 (2023-06-27)

### Fix

* Testing build ([`5f20c5e`](https://gitlab.psi.ch/bec/bec/-/commit/5f20c5e32d304e973bf02e496b1c0bcc6990a302))

## v0.6.10 (2023-06-27)

### Fix

* Testing build ([`d5fb551`](https://gitlab.psi.ch/bec/bec/-/commit/d5fb5511c79dfc598089d42a184fca26a35e6b3b))

## v0.6.9 (2023-06-27)

### Fix

* Fixed build script ([`5bba42a`](https://gitlab.psi.ch/bec/bec/-/commit/5bba42a898c2b8ec5735d1f059012ac60e2222a9))

## v0.6.8 (2023-06-27)

### Fix

* Testing release ([`240d402`](https://gitlab.psi.ch/bec/bec/-/commit/240d4020b80f371d3001a59fe55ac1433edb93d9))

## v0.6.7 (2023-06-27)

### Fix

* Fixed and improved setup.cfg files ([`b04a97e`](https://gitlab.psi.ch/bec/bec/-/commit/b04a97edbb4309d0364f19df528401ad29c62c9b))

### Documentation

* Improved config helper doc strings ([`08f6ff4`](https://gitlab.psi.ch/bec/bec/-/commit/08f6ff444e24395ee759f203123d9962441f59dd))

## v0.6.6 (2023-06-25)

### Fix

* Fixed file writer for empty time stamps ([`bc5fbf6`](https://gitlab.psi.ch/bec/bec/-/commit/bc5fbf651c39c562de2b2568011c47094e155017))

## v0.6.5 (2023-06-25)

### Fix

* Fixed timestamps for h5 files; closes #76 ([`36ab89e`](https://gitlab.psi.ch/bec/bec/-/commit/36ab89e51e031697f1611a1a1c5b946d3c7c1c2a))

## v0.6.4 (2023-06-23)

### Fix

* Added missing remove_device_tag function ([`a0884ce`](https://gitlab.psi.ch/bec/bec/-/commit/a0884cea22ee32026753b0cec449c7003a2b49b5))

## v0.6.3 (2023-06-23)

### Fix

* Fixed typo ([`3cc4418`](https://gitlab.psi.ch/bec/bec/-/commit/3cc44186ab8ada514c7d950bd2acbb5b03ac8e25))
* Version variable is pulled from semantic release file ([`6669bce`](https://gitlab.psi.ch/bec/bec/-/commit/6669bce3e178ca71d664adf9a7493e7ecad4589d))

## v0.6.2 (2023-06-23)

### Fix

* Fixed scan item for intermediate repr queries ([`a915a69`](https://gitlab.psi.ch/bec/bec/-/commit/a915a6906667cff85ab62e22a9bb0ec8f96a2656))
* Fixed scan item for intermediate repr queries ([`9decff2`](https://gitlab.psi.ch/bec/bec/-/commit/9decff27a74af7d84f41ddd8f9b3585e1d353a88))

## v0.6.1 (2023-06-23)

### Fix

* Fixed monitor scan for numpy v1.25 ([`870c033`](https://gitlab.psi.ch/bec/bec/-/commit/870c03344cd55d22a89d236d88ec60e7677ed20e))

### Documentation

* Improved doc strings for scans ([`25fe364`](https://gitlab.psi.ch/bec/bec/-/commit/25fe3641442f1fe31000685664881aaa01c9cfb3))

## v0.6.0 (2023-06-22)

### Feature

* Add to_pandas method to scan items ([`858bb78`](https://gitlab.psi.ch/bec/bec/-/commit/858bb7816d02e0326492cc6d53a18d3b4fa646e9))

## v0.5.0 (2023-06-20)

### Feature

* Added bec data processing service ([`17213da`](https://gitlab.psi.ch/bec/bec/-/commit/17213da46b236cb5ff7155890e4319308350ba4c))
* Added dap message and endpoint ([`e1aa5e1`](https://gitlab.psi.ch/bec/bec/-/commit/e1aa5e199b10cf9c7570967c01a5f3b48bfe1fc6))

### Documentation

* Add commit message info to readme ([`2d8038b`](https://gitlab.psi.ch/bec/bec/-/commit/2d8038bac7ecb3563025ceddfe08b177f94bdf6c))

## v0.4.9 (2023-06-19)

### Fix

* Raise when device does not exist; added str dunder for devices ([`12e2d29`](https://gitlab.psi.ch/bec/bec/-/commit/12e2d29dad71c11586cee06cb0688557c3cb4bb2))

### Documentation

* Added more doc strings ([`c8cc156`](https://gitlab.psi.ch/bec/bec/-/commit/c8cc15632d4221877a19296bb7d8b7742c1e4ccd))

## v0.4.8 (2023-06-19)

### Fix

* Removed changelog dependency ([`2be1c67`](https://gitlab.psi.ch/bec/bec/-/commit/2be1c67cbc7a025314a665c6d272ac2874e02fee))

## v0.4.7 (2023-06-19)

### Fix

* Fixed typo ([`f59e73c`](https://gitlab.psi.ch/bec/bec/-/commit/f59e73cbb11c1242115b1b42b97cbeb0f0f6252b))
* Fixed weird semantic-release syntax ([`eabb210`](https://gitlab.psi.ch/bec/bec/-/commit/eabb210b6e0e68269854026a8a71c07cd9274c04))

## v0.4.6 (2023-06-19)

### Fix

* Removed pypi upload ([`0b28025`](https://gitlab.psi.ch/bec/bec/-/commit/0b280253701b5e49ea37512cda6bad888e4b8149))

## v0.4.5 (2023-06-19)

### Fix

* Removed build ([`1171e65`](https://gitlab.psi.ch/bec/bec/-/commit/1171e651959df0b07f4e9ce096a8b6e4e77b132b))

## v0.4.4 (2023-06-19)

### Fix

* Disabled upload to repository ([`2e56468`](https://gitlab.psi.ch/bec/bec/-/commit/2e564681016b1b369c65087ab447444eca8a2c9a))

## v0.4.3 (2023-06-19)

### Fix

* Pull from origin ([`6c659a9`](https://gitlab.psi.ch/bec/bec/-/commit/6c659a94c4dbd5b7a4a3718c08b6fd1b117c3602))
* Checkout master instead of commit ([`33e0669`](https://gitlab.psi.ch/bec/bec/-/commit/33e0669323e3fb01d079fb56018349d190537101))
* Added git pull ([`7e77444`](https://gitlab.psi.ch/bec/bec/-/commit/7e77444a70647706ae448186fb44c64a3622880c))
* Fixed domain name ([`a3c2e5f`](https://gitlab.psi.ch/bec/bec/-/commit/a3c2e5ff85dbdd6badc182828ee85b6e01dc6377))
* Added hvcs domain ([`32856c5`](https://gitlab.psi.ch/bec/bec/-/commit/32856c50047c6a91a10f2a3666738dc6b7f16737))

## v0.4.2 (2023-06-19)

### Fix

* Changed semantic-release version to publish ([`5e12ef4`](https://gitlab.com/bec/bec/-/commit/5e12ef43171b6b75abd666aabd9060f132e53fce))
* Delete all local tags before adding new ones ([`b8d71f5`](https://gitlab.com/bec/bec/-/commit/b8d71f5cabf80d099bf76687758f398bff9214e1))
* Only run semver on master; added git tag log ([`b63d128`](https://gitlab.com/bec/bec/-/commit/b63d128cefb50dfdb52328bae7032a22cd9d5934))
* Np.vstack must receive tuple ([`3286d46`](https://gitlab.com/bec/bec/-/commit/3286d46163e4ce7d262c170a0d04a59f287b40c1))

## v0.4.1 (2023-06-19)


